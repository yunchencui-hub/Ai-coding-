#!/usr/bin/env python3
"""A tiny mutation tester: it tests your tests.

For every small change ("mutant") it can make to your code -- flip `<` to
`<=`, `+` to `-`, `and` to `or`, `True` to `False`, `10` to `11` -- it runs
your test command against the changed code. If the tests fail, the mutant is
"killed": good, your tests noticed. If the tests still pass, the mutant
"survived": some behaviour of your code is not pinned down by any assertion.

Work happens in a throwaway copy of --root, so your files are never touched.
Exit code is 1 when any mutant survives, which makes this usable as an agent
gate: "write tests until no mutant survives."

Some mutants cannot be killed because they do not change behaviour
("equivalent mutants"). Excuse one by putting `# mutate: skip -- <reason>`
on its line. Write the reason down; an unexplained skip is a hidden hole.

Usage:
    python tools/mutate.py --test "python -m pytest -q -x example/tests" example/shop
"""

from __future__ import annotations

import argparse
import ast
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from functools import partial
from pathlib import Path

EXIT_OK = 0
EXIT_SURVIVORS = 1
EXIT_RED_BASELINE = 3
SKIP_PRAGMA = "mutate: skip"

SYMBOLS = {
    ast.Lt: "<", ast.LtE: "<=", ast.Gt: ">", ast.GtE: ">=",
    ast.Eq: "==", ast.NotEq: "!=", ast.In: "in", ast.NotIn: "not in",
    ast.Is: "is", ast.IsNot: "is not",
    ast.Add: "+", ast.Sub: "-", ast.Mult: "*", ast.Div: "/", ast.FloorDiv: "//",
    ast.And: "and", ast.Or: "or",
}

# Each operator maps to the operators it may be swapped for. Comparisons get
# both a boundary shift (< to <=) and a negation (< to >=).
SWAPS = {
    ast.Lt: (ast.LtE, ast.GtE), ast.LtE: (ast.Lt, ast.Gt),
    ast.Gt: (ast.GtE, ast.LtE), ast.GtE: (ast.Gt, ast.Lt),
    ast.Eq: (ast.NotEq,), ast.NotEq: (ast.Eq,),
    ast.In: (ast.NotIn,), ast.NotIn: (ast.In,),
    ast.Is: (ast.IsNot,), ast.IsNot: (ast.Is,),
    ast.Add: (ast.Sub,), ast.Sub: (ast.Add,),
    ast.Mult: (ast.Div,), ast.Div: (ast.Mult,), ast.FloorDiv: (ast.Mult,),
    ast.And: (ast.Or,), ast.Or: (ast.And,),
}

IGNORED_DIRS = (".git", "__pycache__", "*.pyc", ".venv", ".pytest_cache", "htmlcov")


@dataclass(frozen=True)
class Mutant:
    path: Path  # relative to the project root
    index: int  # position among all mutation sites in the file
    line: int
    description: str


@dataclass(frozen=True)
class Result:
    mutant: Mutant
    outcome: str  # "killed", "survived" or "timeout"


def describe(old: ast.AST, new: type) -> str:
    return f"`{SYMBOLS[type(old)]}` -> `{SYMBOLS[new]}`"


def set_item(seq: list, index: int, value: object) -> None:
    seq[index] = value


def compare_mutations(node: ast.Compare) -> list:
    found = []
    for i, op in enumerate(node.ops):
        for new in SWAPS.get(type(op), ()):
            found.append((describe(op, new), partial(set_item, node.ops, i, new())))
    return found


def operator_mutations(node: ast.AST) -> list:
    return [
        (describe(node.op, new), partial(setattr, node, "op", new()))
        for new in SWAPS.get(type(node.op), ())
    ]


def constant_mutations(node: ast.Constant) -> list:
    value = node.value
    if isinstance(value, bool):
        return [(f"`{value}` -> `{not value}`", partial(setattr, node, "value", not value))]
    if isinstance(value, (int, float)):
        bumped = value + 1
        return [(f"`{value!r}` -> `{bumped!r}`", partial(setattr, node, "value", bumped))]
    return []


def negation_mutations(node: ast.UnaryOp) -> list:
    doubled = ast.UnaryOp(op=ast.Not(), operand=node.operand)
    return [("remove `not`", partial(setattr, node, "operand", doubled))]


def mutations_for(node: ast.AST) -> list:
    """Return (description, apply) pairs; apply() mutates the tree in place."""
    if isinstance(node, ast.Compare):
        return compare_mutations(node)
    if isinstance(node, (ast.BinOp, ast.BoolOp, ast.AugAssign)):
        return operator_mutations(node)
    if isinstance(node, ast.Constant):
        return constant_mutations(node)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
        return negation_mutations(node)
    return []


def sites(tree: ast.AST):
    """Yield (node, description, apply) in a deterministic order."""
    for node in ast.walk(tree):
        for description, apply in mutations_for(node):
            yield node, description, apply


def enumerate_mutants(path: Path, source: str) -> list[Mutant]:
    skipped = skipped_lines(source)
    mutants = []
    for index, (node, description, _) in enumerate(sites(ast.parse(source))):
        if node.lineno not in skipped:
            mutants.append(Mutant(path, index, node.lineno, description))
    return mutants


def skipped_lines(source: str) -> set[int]:
    return {n for n, line in enumerate(source.splitlines(), 1) if SKIP_PRAGMA in line}


def apply_mutant(source: str, index: int) -> str:
    tree = ast.parse(source)
    for position, (_, _, apply) in enumerate(sites(tree)):
        if position == index:
            apply()
            return ast.unparse(tree)
    raise IndexError(f"no mutation site #{index}")


def python_files(paths: list[str]) -> list[Path]:
    files: set[Path] = set()
    for raw in paths:
        path = Path(raw)
        candidates = path.rglob("*.py") if path.is_dir() else [path]
        files.update(p for p in candidates if not p.name.startswith("test_"))
    return sorted(files)


def plan(paths: list[str], root: Path) -> list[Mutant]:
    mutants = []
    for file in python_files(paths):
        relative = file.resolve().relative_to(root)
        mutants += enumerate_mutants(relative, file.read_text())
    return mutants


def run_tests(command: str, cwd: Path, timeout: float) -> str:
    # No .pyc files: a mutant with the same size and mtime as the original
    # could otherwise be shadowed by stale bytecode.
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, env=env,
                                capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "timeout"
    return "passed" if result.returncode == 0 else "failed"


OUTCOMES = {"passed": "survived", "failed": "killed", "timeout": "timeout"}


def run_mutant(mutant: Mutant, workspace: Path, command: str, timeout: float) -> Result:
    target = workspace / mutant.path
    original = target.read_text()
    target.write_text(apply_mutant(original, mutant.index))
    try:
        return Result(mutant, OUTCOMES[run_tests(command, workspace, timeout)])
    finally:
        target.write_text(original)


def render(results: list[Result]) -> str:
    survivors = [r for r in results if r.outcome == "survived"]
    killed = len(results) - len(survivors)
    score = 100.0 * killed / len(results) if results else 100.0
    lines = [f"{len(results)} mutants: {killed} killed, {len(survivors)} survived "
             f"(mutation score {score:.1f}%)"]
    for r in survivors:
        m = r.mutant
        lines.append(f"  SURVIVED  {m.path}:{m.line}  {m.description}")
    if survivors:
        lines.append("Each survivor is a change no test noticed. Write a test that "
                     "fails on exactly that change.")
    return "\n".join(lines)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="+", help="source files or directories to mutate")
    parser.add_argument("--test", required=True, help="test command; exit 0 means pass")
    parser.add_argument("--root", default=".", help="project root to copy (default: .)")
    parser.add_argument("--timeout", type=float, default=60.0,
                        help="seconds per test run; a timeout counts as killed")
    parser.add_argument("--max-mutants", type=int, default=None,
                        help="budget: stop after this many mutants")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.root).resolve()
    mutants = plan(args.paths, root)[: args.max_mutants]
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "work"
        shutil.copytree(root, workspace, ignore=shutil.ignore_patterns(*IGNORED_DIRS))
        if run_tests(args.test, workspace, args.timeout) != "passed":
            print("Tests must pass before mutation testing. Fix them first.")
            return EXIT_RED_BASELINE
        results = [run_mutant(m, workspace, args.test, args.timeout) for m in mutants]
    print(render(results))
    return EXIT_SURVIVORS if any(r.outcome == "survived" for r in results) else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
