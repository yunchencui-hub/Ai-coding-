# Interleaved quiz

Questions are deliberately **shuffled across chapters**. Mixing topics is harder than drilling one chapter at a time, and it's what makes knowledge stick and transfer. Answer each one out loud or on paper *before* opening the answer. Score yourself honestly; the goal is to find gaps.

Suggested schedule: take it once after reading all chapters, again 3 days later, again 2 weeks later.

---

**Q1.** You inherit a 600-line `CLAUDE.md`. Agents follow the first few rules and ignore most of the rest. Using the episode's ideas, what do you do?

<details><summary>Answer</summary>

Trim it to a minimal priority zone (identity, intent, the few rules that must shape generation), and convert every checkable rule into a gate the agent must pass (tests, CRAP, fence, linters). Rules in the middle of long contexts fade (lost in the middle); gates don't. (I04, I05)
</details>

**Q2.** Compute the CRAP score: CC = 4, coverage = 50%. Does it pass a threshold of 6?

<details><summary>Answer</summary>

4² × (0.5)³ + 4 = 16 × 0.125 + 4 = **6.0**. It passes: the gate fails only when the score is *above* 6. (I07)
</details>

**Q3.** A junior engineer asks how to become someone who can run agents well. What path does Uncle Bob propose?

<details><summary>Answer</summary>

Write code by hand for about a year. Then, at a company, be treated as an agent: receive agent-style tasks and pass the same deterministic gates, for months, while being "unproductive but learning". Then run an agent under supervision. Underneath sits the ladder from binary and assembly through C and Python to agents. (I26)
</details>

**Q4.** True or false: "Since agents write the code, the CRAP threshold should be the same as for humans."

<details><summary>Answer</summary>

False, per Uncle Bob. Values stay the same but thresholds can move: about 4 for humans, 6 (maybe 8) for agents, on the hypothesis that agents have a larger, accurate short-term memory. That hypothesis isn't independently verified. (I18)
</details>

**Q5.** Your agent has been going in circles for 40 minutes: it fixes test A, which breaks test B, and fixing B breaks A again. Name two things the episode suggests are going on, and what to do.

<details><summary>Answer</summary>

(1) **Thrash from mess**: the code is tangled enough that the agent can't cope (I02). (2) **Trajectory**: the session is stuck on its early approach (I12). Stop the session; look at the structure (fence violations, high-CRAP functions) and fix or redesign it (I13, I15); then restart with a fresh context and a narrower task (I11). Recognizing this pattern quickly is the skill from I27.
</details>

**Q6.** What does a surviving mutant prove that a coverage report can't?

<details><summary>Answer</summary>

That a specific change to the code goes unnoticed by every test: the behavior isn't pinned down by any assertion, even if the line was executed (covered). (I08)
</details>

**Q7.** Your PM wants a 40-page spec written before any agent starts. What's Uncle Bob's view, and what does he do instead?

<details><summary>Answer</summary>

It's the waterfall temptation again: agent plans look gorgeous but fall apart in execution because nobody can anticipate everything (I20). Instead, do a story or two, look at the result and the architecture, adjust, continue (I21). With change costs near $1, iterating beats over-planning (I22). Caveat: plan more where change is genuinely expensive.
</details>

**Q8.** Order these seats and match each to its gate: Hardener, QA, Specifier, Cleaner, Coder. Gates: CRAP, executable QA script, mutation testing, Gherkin + QA procedure, unit + acceptance tests green.

<details><summary>Answer</summary>

Specifier (Gherkin + QA procedure) → Coder (unit + acceptance tests green) → Cleaner (CRAP) → Hardener (mutation testing) → QA (executable QA script). (I10)
</details>

**Q9.** The fence says `orders` may not import `email`, but orders must send confirmation emails. Fix it without changing the fence.

<details><summary>Answer</summary>

**Insert an interface**: `orders` declares a small `Notifier` interface and receives an implementation from outside; the email module provides one. (Alternatives: invert the dependency, or split a module that's doing two jobs.) See `example/shop/checkout.py`, which does exactly this with `CartStore`. (I15)
</details>

**Q10.** Why might deep modules be *risky* for agents, not just helpful?

<details><summary>Answer</summary>

Agents may trust the interface and never read the implementation. If the implementation is inconsistent with the interface, they'll be misled. Uncle Bob called it "both a danger and an advantage". Tests that pin the interface's behavior reduce the risk. (I17)
</details>

**Q11.** Give one example of a practice "shelved only because it was tedious" that agents could revive, besides CRAP and mutation testing.

<details><summary>Answer</summary>

Any sound answer works, for example: exhaustive property-based testing, characterization tests for legacy code, keeping docs in sync with code, full dependency upgrades with changelog review, or formal checks of small critical functions. The selection rule is that the idea was good and only its labor cost killed it. (I09)
</details>

**Q12.** You asked an agent whether your architecture is good and it said yes, enthusiastically. How much should that move you?

<details><summary>Answer</summary>

Very little. Agent debates are hypothesis generators, not authority (I19). Check with deterministic evidence instead: the fence, CRAP report, an architecture viewer (I14), and your own strategic judgment (I25).
</details>

**Q13.** Explain the "$1 house" to a non-engineer in two sentences.

<details><summary>Answer</summary>

If every change to your house cost one dollar and took a second, you wouldn't pay an architect to plan it perfectly up front; you'd move things around until it looked right. AI agents have made changing software nearly that cheap, so heavy up-front planning stops paying for itself. (I22)
</details>

**Q14.** What's the scoreboard that tells you whether your gates are worth it?

<details><summary>Answer</summary>

The productivity margin: human time for a task divided by agents-plus-gates time. Keep it above 1. Uncle Bob reports 2-5x; measure your own. (I03)
</details>

**Q15.** Why do fundamentals matter *more*, not less, with AI, according to the episode?

<details><summary>Answer</summary>

Fundamentals organize complexity into understandable pieces, and models, being modeled on humans, need that organization too. Mess degrades agents (I02), compartments help them (I16), and every abstraction jump brought "the old rules are dead" panic before the rules came back (I28).
</details>

**Q16.** (Critical thinking) Name two things CRAP + mutation + fence gates would *not* catch.

<details><summary>Answer</summary>

Any two of: security vulnerabilities, performance regressions, poor UX or wrong product decisions, data/migration problems, privacy or compliance issues, mechanically split functions that lower CC without improving design. See [critical-lens.md](critical-lens.md).
</details>

**Q17.** Hands-on: in this repo, which single test can you delete to make `make mutate` report survivors, and why does deleting `test_bulk_discount_starts_at_exactly_ten_items` *not* do it?

<details><summary>Answer</summary>

Delete `test_shipping_is_free_at_exactly_fifty_dollars`: then `5000 -> 5001` and `>= -> >` survive, because nothing else tests exactly $50.00. The bulk-discount test isn't the only one using exactly 10 items (the rounding test and a checkout test do too), so those mutants still die. Mutation testing judges the suite as a whole. (I08, Chapter 3)
</details>

---

**Scoring:** 15-17 means you've internalized it, so move on to the [playbook](../playbook/README.md). 10-14: re-read the chapters behind the misses and retake the quiz in 3 days. Below 10: start with the [cheat sheet](cheatsheet.md) and the flashcards, then retry.
