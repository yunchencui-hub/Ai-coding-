# Chapter 3: Boring tools come back

> **In one breath:** Two great quality techniques were shelved for decades because they were too tedious for people: the CRAP score and mutation testing. Agents don't get bored, so these old tools are now practical, and they make strong gates.

Insights: **I07 · I08 · I09**. Source concepts: C6, C7, C8. Hands-on: [`tools/crap.py`](../tools/crap.py), [`tools/mutate.py`](../tools/mutate.py).

---

## Explain it like I'm five

**CRAP score: "how scary is this function?"** Picture a maze. A maze with many twisty paths is harder than a straight hallway. Now turn the lights off in parts of it. Dark, twisty mazes are the scariest. In code:

- twisty = many `if`s and loops (**complexity**),
- lights on = tested (**coverage**).

A twisty function with no tests gets a huge score. A twisty function that's fully tested scores the same as its number of paths. A simple, tested function scores 1.

**Mutation testing: "does your proofreader actually read?"** A teacher wants to know if your proofreading buddy is any good, so she sneaks one typo into your essay and hands it over. If the buddy says "looks perfect!", the buddy isn't really checking. Mutation testing does this to your tests. It sneaks a tiny bug into your code (changes `<` to `<=`) and sees whether any test complains.

**Why now?** Both jobs are dull: thousands of tiny, repetitive checks. People hated doing them. Robots don't mind.

---

## The grown-up version

### I07 · The CRAP metric as a gate

**C.R.A.P.** (Change Risk Anti-Patterns) was created by Alberto Savoia and Bob Evans in 2007:

```
CRAP(f) = CC(f)^2 * (1 - coverage(f))^3 + CC(f)
```

- `CC` is cyclomatic complexity: 1 + the number of decision points (`if`, loops, `and`/`or`, `except`, ...).
- `coverage` is the fraction of the function's statements executed by tests.

Useful facts to remember:

| Situation | Score |
|---|---|
| Fully tested | exactly `CC` |
| Untested | `CC^2 + CC` (CC 2, untested, scores 6; CC 5, untested, scores 30) |
| CC above your threshold | can never pass, whatever the coverage, so you must split the function |

Uncle Bob says he tried CRAP around 2000 but set it aside because going through every function by hand took forever. Now he simply asks an agent to run CRAP over what it just did and clean up whatever scores badly. He reads the score the friendly way: a score of 6 means six pathways through the function, all covered by tests.

He has published his own CRAP tools for Java, Go and Clojure (`unclebob/crap4java`, `crap4go`, `crap4clj`). This repo's [`tools/crap.py`](../tools/crap.py) is an independent Python implementation of the same published formula.

### I08 · Mutation testing as the merciless hardener

How it works:

1. Make a **mutant**: copy the code with one small change (flip `<` to `<=`, `+` to `-`, `True` to `False`, `10` to `11`).
2. Run the whole test suite against it.
3. If a test fails, the mutant is **killed** (good). If everything passes, it **survived**, which proves that this behavior isn't pinned down by any assertion.
4. Write tests until every mutant dies.

Around 2000 a run like this took him all night. With agents and modern hardware he describes it taking about 30 minutes, with the agent plugging every hole it finds. In his pipeline the "hardener" agent does this job and is merciless about it.

**This repo has a worked example.** The first time `tools/mutate.py` ran on [`example/shop`](../example/shop), two mutants survived: `frozen=True` changed to `frozen=False` on two dataclasses. Every test still passed, because no test checked that receipts and line items can't be edited after creation. Two small tests fixed it (see `test_line_item_is_immutable` and `test_receipts_cannot_be_altered`). Coverage was already 100%, so coverage alone could never have caught this.

### I09 · Agents don't feel boredom, which unlocks shelved tools

The general lesson is a selection rule: **look for good ideas that were abandoned only because they were tedious.** Agents are fast, don't care how boring the work is, and do what they're told. Both CRAP and mutation testing fit: sound ideas killed purely by labor cost.

Some candidates of my own (not from the episode): exhaustive property-based tests, keeping docs in sync with code, full dependency upgrades with changelog review, and characterization tests for legacy code.

---

## Picture it

```
 CRAP for a function with CC = 4
   coverage:  0%    25%    50%    75%    100%
   score:    20.0  10.75   6.0   4.25    4.0
                          ^ exactly at a threshold of 6 = pass (gate fails only if > 6)

 MUTATION TESTING
   original:   if age >= 18: ...
   mutant #1:  if age >  18: ...   tests pass? -> SURVIVED  (nobody tested age == 18)
   mutant #2:  if age <  18: ...   tests fail  -> killed
   mutant #3:  if age >= 19: ...   tests pass? -> SURVIVED  (same hole)
   fix: add `assert is_adult(18)` and `assert not is_adult(17)`  -> all killed
```

---

## Why it matters to you

- **Coverage lies; mutation testing doesn't (as much).** 100% coverage only means the lines ran. Mutation testing checks that your assertions would notice a change.
- **CRAP gives agents a precise repair target.** "This function scores 14: split it or test the untested branches" is something an agent can act on. "Write cleaner code" isn't.
- **Cheap to adopt.** You already produce coverage, and CRAP is a tiny calculation on top of it.

## Try it this week

```bash
pip install pytest coverage
make crap      # CRAP report for tools/ and example/shop (fails if any function > 6)
make mutate    # mutation-test example/shop (fails if any mutant survives)
```

Then break something on purpose and watch the gate catch it:

1. Delete `test_shipping_is_free_at_exactly_fifty_dollars` from `example/tests/test_pricing.py`.
2. Run `make mutate`. Two mutants survive: `5000 -> 5001` and `>= -> >` in `pricing.py`. Coverage is still 100%, because the line still runs. What's gone is the only test that checks the exact $50.00 boundary.
3. Restore the test (`git checkout example/tests/test_pricing.py`). Everything dies again.

(Deleting the bulk-discount-at-ten test *won't* produce survivors, because two other tests also use exactly ten items. Mutation testing measures your suite as a whole, not individual tests.)

For your own language: Java (`crap4java`, PIT), Go (`crap4go`, gremlins), JS/TS (`js-crap-score`, Stryker), Rust (`cargo-crap`, `cargo-mutants`), Python (this repo's tools, `mutmut`, `cosmic-ray`).

## Watch out

- **100% mutation score is usually impossible.** Some mutants don't change behavior at all (**equivalent mutants**), and research estimates them at roughly 4-39% of mutants. You need a way to excuse them *with a written reason*. In `tools/mutate.py` that's a `# mutate: skip -- <reason>` comment.
- **Mutation testing is expensive** (mutants × test-suite time). Scope it to changed code, use incremental modes, and set a budget (`--max-mutants`).
- **CRAP's exponents were chosen by debate, not data**, as the authors themselves said. It's a useful heuristic, not a law of nature.
- **Assertion-free tests can pump coverage**, which can make CRAP look good. Pair CRAP with mutation testing. That's exactly why the episode's pipeline has both a cleaner and a hardener.

## Check yourself

<details><summary>1. A function has CC = 3 and no tests. What is its CRAP score? Does it pass a threshold of 6?</summary>

3² × (1 − 0)³ + 3 = 9 + 3 = **12**. It fails: 12 > 6.
</details>

<details><summary>2. A function has CC = 7 and 100% coverage. Can it pass a threshold of 6?</summary>

No. At full coverage CRAP equals CC, which is 7, and 7 > 6. The only fix is to reduce complexity, for example by splitting the function.
</details>

<details><summary>3. Your tests cover 100% of lines but a mutant survives. What does that tell you?</summary>

The line ran during tests, but no assertion depended on its exact behavior. Coverage measures execution, mutation testing measures detection. Write a test that fails on that exact change.
</details>

<details><summary>4. Why were these tools shelved in the first place, and why does that matter now?</summary>

They were too tedious and slow for humans, which is a labor-cost problem rather than a flaw in the idea. Agents don't get bored, so the cost that killed them is gone. Look for other ideas shelved for the same reason.
</details>

---

Previous: [Chapter 2](02-rules-fade-gates-dont.md) · Next: [Chapter 4: The relay race](04-the-relay-race.md)
