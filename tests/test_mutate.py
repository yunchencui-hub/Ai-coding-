import sys
from pathlib import Path

import pytest

from tools import mutate


def descriptions(source: str) -> list[str]:
    return sorted(m.description for m in mutate.enumerate_mutants(Path("m.py"), source))


def test_comparisons_get_a_boundary_shift_and_a_negation():
    assert descriptions("x = a < b\n") == ["`<` -> `<=`", "`<` -> `>=`"]


def test_arithmetic_and_boolean_operators_are_swapped():
    assert descriptions("x = a + b\ny = a and b\nz -= 1\n") == [
        "`+` -> `-`", "`-` -> `+`", "`1` -> `2`", "`and` -> `or`",
    ]


def test_booleans_flip_and_numbers_are_bumped_but_strings_are_left_alone():
    assert descriptions('x = True\ny = 2.5\nz = "text"\n') == [
        "`2.5` -> `3.5`", "`True` -> `False`",
    ]


def test_not_can_be_removed():
    source = "x = not a\n"
    assert descriptions(source) == ["remove `not`"]
    # `not not a` has the truthiness of `a`: the original `not` is cancelled.
    assert mutate.apply_mutant(source, 0) == "x = not not a"


def test_apply_mutant_changes_exactly_one_site():
    source = "def f(a, b):\n    return a < b\n"
    assert mutate.apply_mutant(source, 0) == "def f(a, b):\n    return a <= b"
    assert mutate.apply_mutant(source, 1) == "def f(a, b):\n    return a >= b"


def test_apply_mutant_rejects_an_unknown_site():
    with pytest.raises(IndexError):
        mutate.apply_mutant("x = 1\n", 5)


def test_lines_marked_skip_are_not_mutated():
    source = "x = a < b  # mutate: skip -- equivalent, see notes\ny = 1\n"
    mutants = mutate.enumerate_mutants(Path("m.py"), source)
    assert [(m.line, m.description) for m in mutants] == [(2, "`1` -> `2`")]


def test_a_test_command_that_hangs_counts_as_a_timeout(tmp_path):
    command = f'{sys.executable} -c "import time; time.sleep(5)"'
    assert mutate.run_tests(command, tmp_path, timeout=0.2) == "timeout"


def test_render_with_no_mutants_reports_a_perfect_score():
    assert "mutation score 100.0%" in mutate.render([])


ADULT = "def is_adult(age):\n    return age >= 18\n"
WEAK_CHECK = "import calc\nassert calc.is_adult(30)\nassert not calc.is_adult(5)\n"
STRONG_CHECK = WEAK_CHECK + "assert calc.is_adult(18)\nassert not calc.is_adult(17)\n"


def make_project(tmp_path, check: str) -> list[str]:
    (tmp_path / "calc.py").write_text(ADULT)
    (tmp_path / "check.py").write_text(check)
    command = f"{sys.executable} check.py"
    return [str(tmp_path / "calc.py"), "--root", str(tmp_path), "--test", command]


def test_weak_tests_let_boundary_mutants_survive(tmp_path, capsys):
    assert mutate.main(make_project(tmp_path, WEAK_CHECK)) == mutate.EXIT_SURVIVORS
    out = capsys.readouterr().out
    assert "calc.py:2  `>=` -> `>`" in out
    assert "calc.py:2  `18` -> `19`" in out
    assert "Write a test that fails on exactly that change" in out


def test_boundary_tests_kill_every_mutant(tmp_path, capsys):
    assert mutate.main(make_project(tmp_path, STRONG_CHECK)) == mutate.EXIT_OK
    assert "3 mutants: 3 killed, 0 survived" in capsys.readouterr().out


def test_mutation_never_edits_the_original_files(tmp_path):
    mutate.main(make_project(tmp_path, WEAK_CHECK))
    assert (tmp_path / "calc.py").read_text() == ADULT


def test_a_red_baseline_stops_the_run(tmp_path, capsys):
    args = make_project(tmp_path, "raise SystemExit(1)\n")
    assert mutate.main(args) == mutate.EXIT_RED_BASELINE
    assert "Tests must pass before mutation testing" in capsys.readouterr().out


def test_max_mutants_caps_the_run(tmp_path, capsys):
    mutate.main(make_project(tmp_path, STRONG_CHECK) + ["--max-mutants", "1"])
    assert "1 mutants: 1 killed" in capsys.readouterr().out
