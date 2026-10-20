#!/usr/bin/env python3
"""Dependency fence: a rules file says which module may import which.

A "module" is a top-level .py file or sub-package directly under the source
directory. The rules file lists, for every module, the other modules it is
allowed to import. Anything not listed is forbidden, and a module that is
missing from the rules is itself a violation, so new code has to be placed on
the map before it can merge.

When the fence fails, there are three standard repairs: invert the
dependency, insert an interface, or split the module.

Rules file (TOML):

    package = "shop"            # import name of the package
    source = "example/shop"     # directory holding it

    [allow]
    cart = []
    pricing = ["cart"]
    checkout = ["cart", "pricing"]

Usage:
    python tools/fence.py example/fence.toml
"""

from __future__ import annotations

import argparse
import ast
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

EXIT_OK = 0
EXIT_VIOLATIONS = 1


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    location: str


@dataclass(frozen=True)
class Rules:
    package: str
    source: Path
    allow: dict[str, list[str]]


def load_rules(path: Path) -> Rules:
    data = tomllib.loads(path.read_text())
    source = (path.parent / data["source"]) if "source" in data else path.parent
    return Rules(data["package"], source, {k: list(v) for k, v in data["allow"].items()})


def module_of(file: Path, source: Path) -> str:
    first = file.relative_to(source).parts[0]
    return first.removesuffix(".py")


def file_package(file: Path, rules: Rules) -> list[str]:
    return [rules.package, *file.relative_to(rules.source).parent.parts]


def imported_names(node: ast.AST, package: list[str]) -> list[str]:
    """Absolute dotted names an import statement refers to."""
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    base = package[: len(package) - node.level + 1] if node.level else []
    prefix = ".".join(base + ([node.module] if node.module else []))
    return [f"{prefix}.{alias.name}" for alias in node.names]


def internal_target(dotted: str, package: str) -> str | None:
    parts = dotted.split(".")
    if parts[0] == package and len(parts) > 1:
        return parts[1]
    return None


def edges_in(file: Path, rules: Rules) -> list[Edge]:
    tree = ast.parse(file.read_text(), filename=str(file))
    here = module_of(file, rules.source)
    package = file_package(file, rules)
    edges = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        for dotted in imported_names(node, package):
            target = internal_target(dotted, rules.package)
            if target and target != here:
                edges.append(Edge(here, target, f"{file}:{node.lineno}"))
    return edges


def source_files(rules: Rules) -> list[Path]:
    root_init = rules.source / "__init__.py"
    return sorted(p for p in rules.source.rglob("*.py") if p != root_init)


def check_edges(edges: list[Edge], rules: Rules) -> list[str]:
    problems = []
    for e in edges:
        allowed = rules.allow.get(e.source, [])
        if e.target not in allowed:
            may = ", ".join(allowed) or "nothing"
            problems.append(f"{e.location}  {e.source} -> {e.target} "
                            f"is not allowed ({e.source} may depend on: {may})")
    return problems


def check_unmapped(files: list[Path], rules: Rules) -> list[str]:
    modules = {module_of(f, rules.source) for f in files}
    return [f"module '{m}' is not in the rules file; add it to [allow]"
            for m in sorted(modules - rules.allow.keys())]


def find_cycle(allow: dict[str, list[str]]) -> list[str] | None:
    """Return one cycle permitted by the rules, or None."""
    visiting: list[str] = []
    done: set[str] = set()

    def visit(module: str) -> list[str] | None:
        if module in visiting:
            return visiting[visiting.index(module):] + [module]
        if module in done:
            return None
        visiting.append(module)
        for target in allow.get(module, []):
            cycle = visit(target)
            if cycle:
                return cycle
        visiting.pop()
        done.add(module)
        return None

    for module in allow:
        cycle = visit(module)
        if cycle:
            return cycle
    return None


def check(rules: Rules) -> tuple[list[str], int]:
    files = source_files(rules)
    edges = [e for f in files for e in edges_in(f, rules)]
    problems = check_unmapped(files, rules) + check_edges(edges, rules)
    cycle = find_cycle(rules.allow)
    if cycle:
        problems.append("rules permit a dependency cycle: " + " -> ".join(cycle))
    return problems, len(edges)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("rules", help="path to the fence TOML file")
    args = parser.parse_args(argv)
    rules = load_rules(Path(args.rules))
    problems, edge_count = check(rules)
    print(f"fence: {len(rules.allow)} modules, {edge_count} internal imports checked")
    for problem in problems:
        print(f"  VIOLATION  {problem}")
    if problems:
        print("Repairs: invert the dependency, insert an interface, or split the module.")
        return EXIT_VIOLATIONS
    print("All dependencies point the allowed way.")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
