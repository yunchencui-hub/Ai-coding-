import ast
import textwrap

from tools import fence


def make_project(tmp_path, files: dict[str, str], allow: str, source_line='source = "pkg"'):
    for name, body in files.items():
        path = tmp_path / "pkg" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(body))
    rules = tmp_path / "fence.toml"
    rules.write_text(f'package = "pkg"\n{source_line}\n\n[allow]\n{textwrap.dedent(allow)}')
    return rules


LAYERED = {
    "__init__.py": "from pkg import core, api\n",
    "core.py": "import os\n",
    "api.py": "from pkg.core import thing\nfrom . import core\n",
}


def test_clean_project_passes(tmp_path, capsys):
    rules = make_project(tmp_path, LAYERED, 'core = []\napi = ["core"]\n')
    assert fence.main([str(rules)]) == fence.EXIT_OK
    assert "All dependencies point the allowed way" in capsys.readouterr().out


def test_forbidden_import_is_reported_with_its_location(tmp_path, capsys):
    files = {**LAYERED, "core.py": "import pkg.api\n"}
    rules = make_project(tmp_path, files, 'core = []\napi = ["core"]\n')
    assert fence.main([str(rules)]) == fence.EXIT_VIOLATIONS
    out = capsys.readouterr().out
    assert "core.py:1  core -> api is not allowed (core may depend on: nothing)" in out
    assert "invert the dependency" in out


def test_module_missing_from_the_rules_is_a_violation(tmp_path):
    files = {**LAYERED, "extra.py": ""}
    rules = fence.load_rules(make_project(tmp_path, files, 'core = []\napi = ["core"]\n'))
    problems, _ = fence.check(rules)
    assert problems == ["module 'extra' is not in the rules file; add it to [allow]"]


def test_rules_that_permit_a_cycle_are_rejected(tmp_path):
    rules = fence.load_rules(make_project(tmp_path, LAYERED, 'core = ["api"]\napi = ["core"]\n'))
    problems, _ = fence.check(rules)
    assert problems == ["rules permit a dependency cycle: core -> api -> core"]


def test_acyclic_rules_have_no_cycle():
    assert fence.find_cycle({"a": ["b", "c"], "b": ["c"], "c": []}) is None


def test_subpackages_and_relative_imports_resolve_to_top_level_modules(tmp_path):
    files = {
        "core.py": "",
        "web/__init__.py": "",
        "web/views.py": "from ..core import thing\nfrom .helpers import x\n",
        "web/helpers.py": "",
    }
    rules = fence.load_rules(make_project(tmp_path, files, 'core = []\nweb = ["core"]\n'))
    edges = [e for f in fence.source_files(rules) for e in fence.edges_in(f, rules)]
    assert [(e.source, e.target) for e in edges] == [("web", "core")]


def test_source_defaults_to_the_rules_file_directory(tmp_path):
    (tmp_path / "a.py").write_text("")
    rules_path = tmp_path / "fence.toml"
    rules_path.write_text('package = "pkg"\n[allow]\na = []\n')
    assert fence.load_rules(rules_path).source == tmp_path


def test_imported_names_handles_every_import_form():
    def names(code, package=("pkg", "sub")):
        return fence.imported_names(ast.parse(code).body[0], list(package))

    assert names("import pkg.core, os") == ["pkg.core", "os"]
    assert names("from pkg import core") == ["pkg.core"]
    assert names("from . import core") == ["pkg.sub.core"]
    assert names("from .. import core") == ["pkg.core"]
    assert names("from ..core import thing") == ["pkg.core.thing"]


def test_only_imports_of_the_package_itself_are_internal():
    assert fence.internal_target("pkg.core.thing", "pkg") == "core"
    assert fence.internal_target("pkg", "pkg") is None
    assert fence.internal_target("pkgextra.core", "pkg") is None
