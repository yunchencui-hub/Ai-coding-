import csv
import io
import json

from scripts import build

REAL_DATA = json.loads((build.ROOT / "data" / "insights.json").read_text())


def insight(**overrides):
    base = {
        "id": "I01", "chapter": 1, "title": "T", "eli5": "E", "takeaway": "K",
        "speaker": "S", "concepts": ["C1"], "confidence": "episode",
        "tags": ["x"], "cards": [{"q": "Q?", "a": "A."}],
    }
    return {**base, **overrides}


def make_root(tmp_path, insights=None):
    data = {
        "episode": {"title": "Ep", "host": "H", "guest": "G", "date": "2026-08-19",
                    "url": "https://example.com", "provenance": "test"},
        "chapters": [{"number": 1, "title": "One", "file": "insights/01-one.md"}],
        "insights": insights if insights is not None else [insight()],
    }
    for name, text in {
        "data/insights.json": json.dumps(data),
        "insights/01-one.md": "# One\nSee [two](02-two.md) and [tool](../tools/x.py).\n",
        "study/cheatsheet.md": "# Cheat",
        "study/critical-lens.md": "# Lens",
        "SOURCES.md": "# Sources",
    }.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return tmp_path


def test_the_real_insights_file_is_valid():
    assert build.validate(REAL_DATA, build.ROOT) == []


def test_the_real_insights_cover_all_28_ledger_concepts():
    covered = {c for i in REAL_DATA["insights"] for c in i["concepts"]}
    assert covered == {f"C{n}" for n in range(1, 29)}


def test_concept_ids_must_be_in_the_ledger_range():
    assert build.valid_concept("C1") and build.valid_concept("C28")
    assert not build.valid_concept("C0")
    assert not build.valid_concept("C29")
    assert not build.valid_concept("concept 3")


def test_each_kind_of_problem_is_reported():
    chapters = {1}
    assert build.insight_problems({"id": "I09"}, chapters)[0].startswith("I09: missing chapter, title")
    assert build.insight_problems(insight(chapter=9), chapters) == ["I01: unknown chapter"]
    assert build.insight_problems(insight(confidence="vibes"), chapters) == ["I01: unknown confidence label"]
    assert build.insight_problems(insight(cards=[]), chapters) == ["I01: needs at least one flashcard"]
    assert build.insight_problems(insight(concepts=["C99"]), chapters) == ["I01: concepts must be C1..C28"]


def test_duplicate_ids_and_missing_chapter_files_are_reported(tmp_path):
    assert build.duplicate_id_problems([insight(), insight()]) == ["duplicate id I01"]
    chapters = [{"number": 2, "file": "insights/nope.md"}]
    assert build.chapter_file_problems(chapters, tmp_path) == ["missing chapter file insights/nope.md"]


def test_flashcards_are_anki_ready_with_one_row_per_card():
    text = build.flashcards_csv(REAL_DATA)
    assert text.startswith("#separator:Comma\n#html:false\n#tags column:3\n")
    rows = list(csv.reader(io.StringIO(text.split("\n", 3)[3])))
    assert len(rows) == sum(len(i["cards"]) for i in REAL_DATA["insights"])
    question, answer, tags = rows[0]
    assert answer.endswith("[I01 · Get the human out of the code loop]")
    assert tags.split()[:3] == ["uncle-bob-ai", "ch01", "I01"]


def test_bundle_rewrites_sibling_links_and_keeps_relative_ones(tmp_path):
    root = make_root(tmp_path)
    data = json.loads((root / "data" / "insights.json").read_text())
    bundle = build.bundle_markdown(data, root)
    assert bundle.startswith("# All insights in one file: Ep")
    assert "](../insights/02-two.md)" in bundle
    assert "](../tools/x.py)" in bundle
    assert "| I01 | T | E | K |" in bundle
    assert bundle.index("# One") < bundle.index("# Cheat") < bundle.index("# Lens") < bundle.index("# Sources")


def test_build_then_check_round_trip(tmp_path, capsys):
    root = make_root(tmp_path)
    assert build.main(["--check"], root=root) == build.EXIT_STALE
    assert "stale: study/flashcards.csv" in capsys.readouterr().out
    assert build.main([], root=root) == build.EXIT_OK
    assert build.main(["--check"], root=root) == build.EXIT_OK


def test_invalid_data_stops_the_build(tmp_path, capsys):
    root = make_root(tmp_path, insights=[insight(confidence="vibes")])
    assert build.main([], root=root) == build.EXIT_INVALID
    assert "I01: unknown confidence label" in capsys.readouterr().out
    assert not (root / "dist").exists()
