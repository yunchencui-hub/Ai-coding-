#!/usr/bin/env python3
"""CRAP score gate for Python code.

    CRAP(fn) = CC^2 * (1 - coverage)^3 + CC        (Savoia & Evans, 2007)

CC is cyclomatic complexity (1 + the number of decision points) and coverage
is the fraction of the function's statements that your tests executed.
A fully tested function scores exactly its CC; an untested one is punished
quadratically.

The tool reads line coverage from a coverage.py JSON report, computes CC from
the AST, prints a table, and exits 2 when any function scores above
--threshold. That exit code is the point: an agent can be told "keep changing
the code until this command exits 0", which it cannot argue with or forget.

Usage:
    coverage run -m pytest && coverage json -o coverage.json
    python tools/crap.py --coverage coverage.json --threshold 6 src/
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

EXIT_OK = 0
EXIT_OVER_THRESHOLD = 2

FUNCTION_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)
NESTED_SCOPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
BRANCH_NODES = (
    ast.If,
    ast.IfExp,
    ast.For,
    ast.AsyncFor,
    ast.While,
    ast.ExceptHandler,
    ast.match_case,
)


@dataclass
class Score:
    location: str
    function: str
    complexity: int
    coverage: float
    crap: float


def crap_score(complexity: int, coverage: float) -> float:
    return complexity**2 * (1 - coverage) ** 3 + complexity


def decision_points(node: ast.AST) -> int:
    if isinstance(node, ast.BoolOp):
        return len(node.values) - 1
    if isinstance(node, ast.comprehension):
        return 1 + len(node.ifs)
    return 1 if isinstance(node, BRANCH_NODES) else 0


def own_nodes(func: ast.AST):
    """Yield every node in func's body, skipping nested functions and classes
    (those are scored on their own)."""
    stack = list(func.body)
    while stack:
        node = stack.pop()
        if isinstance(node, NESTED_SCOPES):
            continue
        yield node
        stack.extend(ast.iter_child_nodes(node))


def cyclomatic_complexity(func: ast.AST) -> int:
    return 1 + sum(decision_points(node) for node in own_nodes(func))


def body_lines(func: ast.AST) -> set[int]:
    """Source lines of func's body, minus the bodies of nested scopes."""
    lines = set(range(func.body[0].lineno, func.end_lineno + 1))
    for node in ast.walk(func):
        if node is not func and isinstance(node, NESTED_SCOPES):
            lines -= set(range(node.lineno, node.end_lineno + 1))
    return lines


def coverage_fraction(func: ast.AST, file_coverage: dict | None) -> float:
    if file_coverage is None:
        return 0.0  # never imported by any test: treat as untested
    executed = set(file_coverage["executed_lines"])
    statements = executed | set(file_coverage["missing_lines"])
    lines = body_lines(func) & statements
    if not lines:
        return 1.0  # nothing executable to cover
    return len(lines & executed) / len(lines)


def find_functions(tree: ast.AST) -> list[tuple[str, ast.AST]]:
    found: list[tuple[str, ast.AST]] = []
    _collect(tree, "", found)
    return found


def _collect(node: ast.AST, prefix: str, found: list) -> None:
    for child in ast.iter_child_nodes(node):
        child_prefix = prefix
        if isinstance(child, NESTED_SCOPES):
            child_prefix = f"{prefix}{child.name}."
        if isinstance(child, FUNCTION_NODES):
            found.append((prefix + child.name, child))
        _collect(child, child_prefix, found)


def python_files(paths: list[str]) -> list[Path]:
    files: set[Path] = set()
    for raw in paths:
        path = Path(raw)
        candidates = path.rglob("*.py") if path.is_dir() else [path]
        files.update(p for p in candidates if not is_test_file(p))
    return sorted(files)


def is_test_file(path: Path) -> bool:
    return path.name.startswith("test_") or path.name.endswith("_test.py")


def load_coverage(report_path: str) -> dict[Path, dict]:
    report = json.loads(Path(report_path).read_text())
    return {Path(name).resolve(): data for name, data in report["files"].items()}


def score_file(path: Path, coverage: dict[Path, dict]) -> list[Score]:
    tree = ast.parse(path.read_text(), filename=str(path))
    file_coverage = coverage.get(path.resolve())
    scores = []
    for name, func in find_functions(tree):
        cc = cyclomatic_complexity(func)
        cov = coverage_fraction(func, file_coverage)
        location = f"{path}:{func.lineno}"
        scores.append(Score(location, name, cc, cov, crap_score(cc, cov)))
    return scores


def render(scores: list[Score], threshold: float) -> str:
    lines = [f"CRAP report (threshold {threshold:g})", ""]
    lines.append(f"{'CRAP':>7} {'CC':>4} {'Cov%':>6}  Function")
    for s in sorted(scores, key=lambda s: s.crap, reverse=True):
        flag = "  <-- over threshold" if s.crap > threshold else ""
        lines.append(
            f"{s.crap:7.2f} {s.complexity:4d} {s.coverage * 100:6.1f}  "
            f"{s.location} {s.function}{flag}"
        )
    over = sum(s.crap > threshold for s in scores)
    lines += ["", f"{len(scores)} functions, {over} over threshold."]
    if over:
        lines.append("Fix by adding tests for uncovered paths or splitting the function.")
    return "\n".join(lines)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("paths", nargs="+", help="source files or directories")
    parser.add_argument("--coverage", default="coverage.json",
                        help="coverage.py JSON report (default: coverage.json)")
    parser.add_argument("--threshold", type=float, default=6.0,
                        help="fail if any function scores above this (default: 6)")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    return parser.parse_args(argv)


def report(scores: list[Score], args: argparse.Namespace) -> str:
    if args.json:
        return json.dumps([asdict(s) for s in scores], indent=2)
    return render(scores, args.threshold)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    coverage = load_coverage(args.coverage)
    scores = [s for f in python_files(args.paths) for s in score_file(f, coverage)]
    print(report(scores, args))
    over = any(s.crap > args.threshold for s in scores)
    return EXIT_OVER_THRESHOLD if over else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
