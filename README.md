# AI coding insights: Uncle Bob on software fundamentals in the age of AI

A study kit built from the livestream **[LIVE: Uncle Bob on Software Fundamentals in the Age of AI](https://www.youtube.com/live/zcLPGC-tvgk)**, in which Matt Pocock talks with Robert C. Martin ("Uncle Bob") on 19 August 2026 about building software with coding agents.

It contains:

- **28 insights** explained like you're five, then the grown-up version
- **Flashcards, a quiz and a cheat sheet** for active recall
- **A critical lens:** where the speakers agree, where the argument is contested, and what it leaves out
- **A playbook** for applying it to your own codebase, with role prompts for an agent relay
- **Working tools** for the three gates the episode describes (CRAP score, mutation testing, dependency fence), tested and run against this repo in CI

> **Provenance note:** this was built from secondary sources (a community auto-caption analysis plus independent write-ups), not from watching the video directly. Ideas and attributions are cross-checked; exact quotes are close to verbatim, not certified. See [SOURCES.md](SOURCES.md) before quoting anything.

---

## The whole episode, explained like you're five (60 seconds)

You have a **robot helper that writes code ten times faster than you.** If you check every line it writes, everything goes at your speed, so you stop doing that. But the robot is messy, and mess makes even the robot confused. So instead of watching it, you build **checkpoints it can't sneak past**:

- a **"how scary is this function?" score** (CRAP),
- a **"does your proofreader really read?" test** (mutation testing),
- **house rules for which rooms connect to which**, with a guard at every door (the dependency fence).

You don't give the robot a fifty-rule speech, because it will forget the middle. The checkpoints do the remembering. You split the work into a **relay race** of fresh robots (one writes the plan, one codes, one cleans, one hardens the tests, one plays the customer), because a robot that runs too long gets confused by everything it heard earlier.

Since changes are now cheap, you **build a little, look, adjust**, instead of drawing giant plans. And your job becomes the **general's job**: deciding where to go and how the house is laid out. To do that well you need to have done the sergeant's job yourself first. The old rules of good software aren't dead. They're how *robots* stay sane too.

---

## Four ways to take this in

| You have... | Do this |
|---|---|
| **15 minutes** | Read the [cheat sheet](study/cheatsheet.md), then the "In one breath" box at the top of each [chapter](insights/README.md). |
| **A week, to really learn it** | Follow the study plan below. |
| **An afternoon, to try it** | Run the gates (Quick start), then follow the [playbook](playbook/README.md). |
| **An AI or notes app to feed** | Use [`dist/ALL-INSIGHTS.md`](dist/ALL-INSIGHTS.md) (everything in one file) or [`data/insights.json`](data/insights.json) (structured). |

### A study plan built on spaced repetition

| When | What | Time |
|---|---|---|
| Day 1 | Chapters [1](insights/01-fast-hands-slow-hands.md)-[2](insights/02-rules-fade-gates-dont.md); import the [flashcards](study/flashcards.csv) into Anki and do the ch01-ch02 cards | 40 min |
| Day 2 | Chapters [3](insights/03-boring-tools-come-back.md)-[4](insights/04-the-relay-race.md); run `make crap` and `make mutate`, and do the break-it exercise in Chapter 3 | 60 min |
| Day 3 | Chapters [5](insights/05-rooms-with-doors.md)-[6](insights/06-values-not-rituals.md); run `make fence` and read `example/shop/checkout.py` | 40 min |
| Day 4 | Chapters [7](insights/07-the-one-dollar-house.md)-[8](insights/08-the-general-and-the-sergeant.md); then the [critical lens](study/critical-lens.md) | 40 min |
| Day 5 | The [interleaved quiz](study/quiz.md), closed-book | 20 min |
| Day 8 | Quiz again, plus your due flashcards | 15 min |
| Day 21 | Quiz again; pick one [playbook](playbook/README.md) step and do it on a real project | 60 min |

Each chapter ends with **"Check yourself"** questions with hidden answers. Answer before you peek. Retrieval is what makes it stick.

**Importing the flashcards into Anki:** File → Import → `study/flashcards.csv`. The file's header lines tell Anki the separator and that column 3 holds tags, so cards are tagged by chapter (`ch01`...`ch08`) and insight (`I01`...`I28`).

---

## Quick start: run the gates

Requires Python 3.11+.

```bash
make install   # pytest + coverage (the tools themselves use only the standard library)
make check     # tests, CRAP gate, dependency fence, mutation testing, generated-file check
make help      # list every target
```

What `make check` does, and what you should see:

| Gate | Command | Passes when |
|---|---|---|
| Tests | `make test` | All tests pass, including the executable [feature file](example/features/checkout.feature) |
| CRAP | `make crap` | No function in `tools/`, `scripts/` or `example/shop/` scores above 6 |
| Fence | `make fence` | Every import in the example shop follows [`example/fence.toml`](example/fence.toml) |
| Mutation | `make mutate` | Every mutant of `example/shop` is killed by a test |
| Freshness | `make build-check` | The flashcards and bundle match their sources |

The repo holds itself to its own rules: the gate tools must pass the CRAP gate too. That caught a real problem while this repo was being built: the CRAP tool's own `main()` scored 7 and had to be split. Mutation testing also caught two untested behaviors in the example shop on its first run; that story is in [Chapter 3](insights/03-boring-tools-come-back.md).

---

## What's in here

```
README.md                  you are here
SOURCES.md                 provenance, verification table, confidence labels
insights/                  the 8 ELI5 chapters (28 insights) + index and concept map
study/
  cheatsheet.md            everything on one page
  quiz.md                  17 interleaved questions with hidden answers
  flashcards.csv           46 Anki-ready cards (generated from data/insights.json)
  critical-lens.md         agreements, tensions, counterpoints, open questions
playbook/
  README.md                7 steps to apply this to your codebase
  CLAUDE.md.template       a minimal agent instruction file
  roles/                   prompts for specifier, coder, cleaner, hardener, QA
tools/                     single-file, dependency-free gates (point your agent at them)
  crap.py                  CRAP score from coverage.py JSON + AST complexity; exit 2 over threshold
  mutate.py                mutation tester; exit 1 if any mutant survives
  fence.py                 dependency fence from a TOML rules file; exit 1 on violations
example/                   a small shop to practise on
  shop/                    cart, pricing, storage, checkout (with a CartStore interface)
  tests/                   unit tests + the feature-file runner
  features/                Gherkin spec (executable) + human QA procedure
  fence.toml               which shop module may import which
data/insights.json         every insight as structured data (ELI5, takeaway, speaker, confidence, cards)
dist/ALL-INSIGHTS.md       one-file bundle for NotebookLM / Claude Projects / Obsidian (generated)
scripts/build.py           validates the data, generates flashcards + bundle (--check for CI)
tests/                     tests for the tools and the build script
Makefile                   every command above
.github/workflows/ci.yml   runs `make check` on Python 3.11 and 3.13
```

## Using the tools on your own code

The tools are deliberately small, single files with no dependencies, so you can read them. The episode's advice applies: **point your agent at them and have it build a version for your stack** rather than copying them blindly. See [playbook Step 6](playbook/README.md#step-6-build-your-instruments-chapters-5-and-7). For a Python project they also work as they are:

```bash
coverage run -m pytest && coverage json -o coverage.json
python tools/crap.py --coverage coverage.json --threshold 6 src/
python tools/mutate.py --test "python -m pytest -x -q" src/mypackage
python tools/fence.py fence.toml
```

## Credits

The ideas belong to **Robert C. Martin** and **Matt Pocock** (and, through them, John Ousterhout, Dex Horthy, Alberto Savoia & Bob Evans, and the authors of the "old books"). The community concept ledger by [Island-Dev-Crew/uncle-bob-skills](https://github.com/Island-Dev-Crew/uncle-bob-skills) made the reconstruction traceable. Explanations, analogies, tools and study materials here are original. Full details in [SOURCES.md](SOURCES.md).
