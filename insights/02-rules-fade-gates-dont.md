# Chapter 2: Rules fade, gates don't

> **In one breath:** Long instruction files get obeyed loosely, because models attend to the start and end of their context and lose the middle. So keep the prompt short and move every *checkable* rule into a tool the agent must satisfy before it can stop.

Insights: **I04 · I05 · I06**. Source concepts: C3, C4, C24.

---

## Explain it like I'm five

Before a birthday party you tell a kid fifty rules. Later they remember the first one ("say hi to grandma") and the last one ("don't eat all the cake"). Rules 17 through 43 are gone.

Now picture a different trick. The playroom door has a lock that only opens when the toys are back in the box. Nobody has to remember the rule, because the door enforces it, every time, and doesn't get tired.

- A **rule** in the prompt is the fifty-item speech.
- A **gate** is the locked door.

You still say a few things up front ("we're going to grandma's, be kind"), but anything a machine can check, the machine checks.

---

## The grown-up version

### I04 · Steering decays

Uncle Bob's experience with long rule files (`CLAUDE.md`, `AGENTS.md` and friends): agents treat them, in his Pirates of the Caribbean joke, as *"more like guidelines."* He attributes this to the "lost in the middle" effect. Models give more weight to the beginning and end of their context than to the middle, so the 50th and 80th instructions in a long file effectively vanish.

Matt Pocock links this to Dex Horthy's "smart zone / dumb zone" framing: past a certain fill level, a context window gets measurably worse at following instructions.

This matches published research. Liu et al.'s *Lost in the Middle* (TACL 2024) found a U-shaped accuracy curve over position in context. Later work on instruction density found that compliance drops as you pile on simultaneous instructions. See [SOURCES.md](../SOURCES.md).

His response is to trim the initial prompt to the bare minimum, so that what's there sits in the high-attention zone, and then to enforce everything else with deterministic tools after the fact.

### I05 · The deterministic-tool loop

A **gate** is a command with a pass/fail exit code: a test suite, a complexity score, a dependency checker. The instruction to the agent turns from "please write clean code" into:

> Keep changing the code until this tool says it's okay.

The agent can't negotiate with an exit code, forget it in the middle of a long context, or decide it's "more of a guideline". Uncle Bob is open that this trades speed for quality, which is why Chapter 1's productivity margin matters: you pay for gates in agent time.

### I06 · The reading asymmetry

Matt Pocock pointed out that if you hand an agent a spec, it will read it. Uncle Bob added the mirror image: humans don't read what agents write. So:

| Audience | Length | Why |
|---|---|---|
| Written **for agents** (specs, role prompts, rule files) | Can be long *if needed*, though front-load what matters (I04) | Agents read everything they're given |
| Written **for humans** (summaries, PR descriptions, reports) | Must be short | Humans skim or skip agent output |

---

## Picture it

```
 attention
   ^
   |##                                                ##
   |###                                             ###
   |#####                                        #####
   |  ########                              ########
   |        ##############################
   +------------------------------------------------------>
    start        the middle of a long prompt          end
   (rule 1)     (rules 17..43 live here, and fade)   (rule 50)

  THE GATE LOOP
  +-------------+     +-------------------+   exit 0   +--------+
  | agent edits | --> | run gate commands | ---------> |  done  |
  |   the code  | <-- | (tests, crap,     |            +--------+
  +-------------+ fail|  fence, mutate)   |
                      +-------------------+
```

---

## Why it matters to you

- **Your 400-line `CLAUDE.md` is probably mostly ignored.** The rules that matter most should be few and at the top. The rest should become checks.
- **Gates compose; prompt rules compete.** Adding a tenth gate doesn't weaken the other nine. Adding a tenth prompt rule dilutes all of them.
- **It makes agents trustworthy in a specific, checkable way.** You don't have to trust the agent. You have to trust the gate, and you can test the gate (this repo tests its own).

## Try it this week

Sort every line of your agent instruction file into one of two buckets:

| Bucket | Example rule | What to do |
|---|---|---|
| **Checkable** | "Functions must be small and tested" | Turn it into a gate: `python tools/crap.py --threshold 6 src/` |
| **Checkable** | "Respect the layering" | Turn it into a gate: `python tools/fence.py fence.toml` |
| **Checkable** | "Write meaningful tests" | Turn it into a gate: `python tools/mutate.py --test "pytest -x" src/` |
| **Checkable** | "Use our formatting" | Turn it into a gate: your formatter/linter in check mode |
| **Generative** | "This is a payments service; correctness beats speed" | Keep it in the prompt, near the top |
| **Generative** | "Prefer small, reversible steps" | Keep it in the prompt, near the top |

Then use [`playbook/CLAUDE.md.template`](../playbook/CLAUDE.md.template) as a starting point: a short priority zone plus one line telling the agent which command must pass.

## Watch out

- **Not everything is checkable.** Taste, product judgment and naming are hard to gate, which is why a short prompt plus human strategic review (Chapter 8) still matter.
- **A gate is only as good as what it measures.** Coverage can be gamed by tests that assert nothing, which is exactly why mutation testing exists (Chapter 3). Ask "what would a lazy agent do to pass this?"
- **Gates can be too slow.** If one takes 20 minutes, agents sit idle and your margin collapses. Scope gates to changed files where you can (diff-scoped mutation testing, `--changed` modes).

## Check yourself

<details><summary>1. Why do rules in the middle of a long instruction file get ignored?</summary>

Models attend most to the beginning and end of their context (primacy and recency), so instructions in the middle get less weight. The research name is "lost in the middle".
</details>

<details><summary>2. What makes a gate different from a rule?</summary>

A gate is a deterministic tool with a pass/fail result, and the agent loops until it passes. It doesn't live in the context window, so it can't be diluted or forgotten. A rule is text the model may or may not weight heavily.
</details>

<details><summary>3. You're writing (a) a spec for an agent and (b) a summary of the agent's work for your manager. How should their lengths differ?</summary>

The spec can be as long as it needs to be, since agents read what they're sent (but front-load the important parts). The summary must be short, because humans don't read long agent output.
</details>

---

Previous: [Chapter 1](01-fast-hands-slow-hands.md) · Next: [Chapter 3: Boring tools come back](03-boring-tools-come-back.md)
