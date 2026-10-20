import ast
import json
import textwrap

import pytest

from tools import crap


def first_function(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source)).body[0]


def write_module(tmp_path, source: str):
    path = tmp_path / "mod.py"
    path.write_text(textwrap.dedent(source))
    return path


def write_coverage(tmp_path, path, executed, missing=()):
    report = {"files": {str(path): {"executed_lines": list(executed),
                                    "missing_lines": list(missing)}}}
    report_path = tmp_path / "coverage.json"
    report_path.write_text(json.dumps(report))
    return report_path


def test_straight_line_code_has_complexity_one():
    assert crap.cyclomatic_complexity(first_function("def f(x):\n    return x + 1\n")) == 1


def test_each_branching_statement_adds_one():
    func = first_function("""
        def f(x):
            if x:
                pass
            elif x > 1:
                pass
            for _ in x:
                pass
            while x:
                break
            try:
                pass
            except ValueError:
                pass
            return 1 if x else 2
    """)
    # if + elif + for + while + except + ternary = 6 decision points
    assert crap.cyclomatic_complexity(func) == 7


def test_boolean_operators_count_each_extra_operand():
    assert crap.cyclomatic_complexity(first_function("def f(a, b, c):\n    return a and b and c\n")) == 3


def test_comprehensions_count_the_loop_and_each_filter():
    func = first_function("def f(xs):\n    return [x for x in xs if x if x > 1]\n")
    assert crap.cyclomatic_complexity(func) == 4


def test_match_cases_each_count():
    func = first_function("""
        def f(x):
            match x:
                case 1:
                    return "one"
                case _:
                    return "other"
    """)
    assert crap.cyclomatic_complexity(func) == 3


def test_nested_functions_are_scored_separately():
    func = first_function("""
        def outer(x):
            def inner(y):
                if y:
                    return y
            return inner(x)
    """)
    assert crap.cyclomatic_complexity(func) == 1


@pytest.mark.parametrize("cc, coverage, expected", [
    (1, 1.0, 1.0),     # fully tested: CRAP equals CC
    (6, 1.0, 6.0),
    (2, 0.0, 6.0),     # untested: CC^2 + CC
    (5, 0.0, 30.0),
    (12, 0.45, 12**2 * 0.55**3 + 12),
])
def test_crap_formula(cc, coverage, expected):
    assert crap.crap_score(cc, coverage) == pytest.approx(expected)


def test_coverage_counts_only_statements_in_the_body():
    func = first_function("def f(x):\n    a = 1\n    b = 2\n    return a\n")
    # line 1 (the def) is executed at import time and must not count
    file_coverage = {"executed_lines": [1, 2, 3], "missing_lines": [4]}
    assert crap.coverage_fraction(func, file_coverage) == pytest.approx(2 / 3)


def test_coverage_ignores_lines_of_nested_functions():
    func = first_function("""
        def outer():
            def inner():
                return 1
            return 2
    """)
    file_coverage = {"executed_lines": [2, 3, 5], "missing_lines": [4]}
    assert crap.coverage_fraction(func, file_coverage) == 1.0


def test_a_file_missing_from_the_report_counts_as_untested():
    assert crap.coverage_fraction(first_function("def f():\n    return 1\n"), None) == 0.0


def test_a_function_with_no_statements_counts_as_covered():
    func = first_function("def f():\n    return 1\n")
    assert crap.coverage_fraction(func, {"executed_lines": [], "missing_lines": []}) == 1.0


def test_functions_are_named_by_their_enclosing_scopes():
    tree = ast.parse(textwrap.dedent("""
        def top(): pass
        class Box:
            def open(self):
                def helper(): pass
        async def fetch(): pass
    """))
    names = [name for name, _ in crap.find_functions(tree)]
    assert names == ["top", "Box.open", "Box.open.helper", "fetch"]


def test_test_files_are_not_scored(tmp_path):
    (tmp_path / "app.py").write_text("")
    (tmp_path / "test_app.py").write_text("")
    (tmp_path / "app_test.py").write_text("")
    single = tmp_path / "single.py"
    single.write_text("")
    found = crap.python_files([str(tmp_path), str(single)])
    assert [p.name for p in found] == ["app.py", "single.py"]


BRANCHY = """
def branchy(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
"""


def test_main_passes_when_every_function_is_under_the_threshold(tmp_path, capsys):
    module = write_module(tmp_path, BRANCHY)
    report = write_coverage(tmp_path, module, executed=[3, 4, 5, 6, 7])
    assert crap.main([str(module), "--coverage", str(report)]) == crap.EXIT_OK
    out = capsys.readouterr().out
    assert "branchy" in out and "0 over threshold" in out


def test_main_fails_and_explains_when_a_function_is_too_crappy(tmp_path, capsys):
    module = write_module(tmp_path, BRANCHY)
    report = write_coverage(tmp_path, module, executed=[3], missing=[4, 5, 6, 7])
    assert crap.main([str(module), "--coverage", str(report)]) == crap.EXIT_OVER_THRESHOLD
    out = capsys.readouterr().out
    assert "over threshold" in out and "splitting the function" in out


def test_main_can_emit_json(tmp_path, capsys):
    module = write_module(tmp_path, BRANCHY)
    report = write_coverage(tmp_path, module, executed=[3, 4, 5, 6, 7])
    crap.main([str(module), "--coverage", str(report), "--json"])
    [entry] = json.loads(capsys.readouterr().out)
    assert entry["function"] == "branchy"
    assert entry["complexity"] == 3
    assert entry["crap"] == 3.0
