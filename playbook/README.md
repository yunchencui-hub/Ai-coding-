# Playbook: apply the episode to your own codebase

The chapters explain the ideas. This page turns them into steps you can start on Monday, in an order where each step pays for itself before the next one. Every step names the chapter it comes from.

> **Ground rule:** add gates one at a time and measure your productivity margin as you go (Chapter 1). If a gate makes agents slower than you, it's too strict, too slow or badly scoped. Fix that before adding the next.

---

## Step 0: Take a baseline (1 hour)

- Time one typical small feature done the way you do it today. Write the number down.
- Get your current numbers: test coverage, a CRAP report, a mutation score on one module.

```bash
# In this repo (Python). See Chapter 3 for tools in other languages.
make crap
make mutate
```

## Step 1: Shrink the prompt (Chapter 2)

- Copy [`CLAUDE.md.template`](CLAUDE.md.template) to your repo as `CLAUDE.md` (or `AGENTS.md`).
- Keep only *generative* guidance in it: what the system is, what matters most, how to work.
- Move every *checkable* rule into Step 2. Aim for under ~40 lines.

## Step 2: Turn rules into gates (Chapters 2 and 3)

| Rule you used to write in the prompt | Gate that replaces it |
|---|---|
| "Keep functions small and well tested" | CRAP threshold (`tools/crap.py --threshold 6`) |
| "Write meaningful tests" | Mutation testing (`tools/mutate.py`) |
| "Respect the architecture / layering" | Dependency fence (`tools/fence.py`) |
| "Follow our style" | Formatter + linter in check mode |
| "Don't break existing features" | Acceptance tests (Gherkin) + executable QA script |
| "Don't leak secrets" | Secret scanner |

Wire them into **one command** (here: `make check`) and put one line in the prompt: *"Your work is done only when `make check` exits 0. If it fails, read the output, fix the cause, and run it again."*

**On a legacy codebase,** don't start with hard thresholds or nothing will pass. Start with a **ratchet**: gate only changed files (`tools/crap.py` accepts file paths, so feed it `git diff --name-only`), or fail only when a score gets worse than its baseline.

## Step 3: Draw the fence (Chapter 5)

1. Ask your agent: *"Describe this repo's modules and which depend on which. List cycles."* Expect surprises.
2. Decide the dependency directions **you** want. Write them as a fence file (format: [`example/fence.toml`](../example/fence.toml)).
3. Run `python tools/fence.py your-fence.toml`. For each violation choose a repair: **invert**, **interface**, or **split**.
4. Add the fence to `make check`. Protect the fence file (CODEOWNERS) so agents can't loosen it to pass.

## Step 4: Split into roles (Chapter 4)

Start with two seats and grow:

| Stage | Seats | Role prompts |
|---|---|---|
| Start | coder → cleaner | [`coder.md`](roles/coder.md), [`cleaner.md`](roles/cleaner.md) |
| Next | + hardener | [`hardener.md`](roles/hardener.md) |
| Full relay | specifier → coder → cleaner → hardener → QA | [`specifier.md`](roles/specifier.md), [`qa.md`](roles/qa.md) |

Rules for the relay:
- **One agent session per seat per story.** Born, do the task, die (I11).
- **Hand off through git commits plus a short structured note:** what changed, which gates pass, what's open.
- **Each seat ends only when its gate passes.**
- If a session drifts, **restart it**; don't argue with it (I12).

## Step 5: Work in small batches (Chapter 7)

- Feed one story at a time, two at most.
- After every one or two stories, spend 10 minutes as the "general": look at the fence report, the top of the CRAP report, and the module diagram. Adjust the structure before continuing.
- Don't ask agents for a giant plan up front, and don't trust a beautiful plan (I20).

## Step 6: Build your instruments (Chapters 5 and 7)

Point an agent at an exemplar and ask for a tailored version (I24):

> "Read `tools/crap.py` in this repository. Build an equivalent for our TypeScript monorepo: read the istanbul `coverage-final.json`, compute per-function cyclomatic complexity with the TypeScript compiler API, print the same table, exit 2 above a threshold of 6, and support checking only files changed since `main`. Include tests."

Other instruments worth having an agent build: an architecture viewer that renders your fence plus the actual imports, a dashboard of the margin per story, and a diff-scoped mutation runner.

## Step 7: Keep score (Chapter 1)

Track per story: human-estimate time, agents-plus-gates time, gate failures per seat, and defects found later. Revisit thresholds (6 vs 8) only with that data, not because an agent argued for it (I19).

---

## Example: one story through the relay, in this repo

The example shop already contains the artifacts each seat would produce:

| Seat | Artifact in this repo | Check |
|---|---|---|
| Specifier | [`example/features/checkout.feature`](../example/features/checkout.feature) | Reviewed by a human |
| Coder | [`example/shop/`](../example/shop/), [`example/tests/`](../example/tests/) | `python -m pytest` (the feature file runs as a test too) |
| Cleaner | the code as it is | `make crap` |
| Hardener | `test_line_item_is_immutable`, `test_receipts_cannot_be_altered` (added because two mutants survived) | `make mutate` |
| Architecture | [`example/fence.toml`](../example/fence.toml) and the `CartStore` interface | `make fence` |
| QA | [`example/features/qa-procedure.md`](../example/features/qa-procedure.md) | A human or a QA agent follows it |
