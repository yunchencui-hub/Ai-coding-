# Chapter 6: Values, not rituals

> **In one breath:** Impose human *values* on agents (tested, clean, well-structured code) but not human *disciplines* (the exact rituals people use to get there). And thresholds may need to move: agents might handle more complexity per function than people can.

Insights: **I18 · I19**. Source concept: C17, C18.

---

## Explain it like I'm five

We want kids to have **clean teeth**. That's the value. To get there, we give kids a ritual: brush for two minutes, sing the song, top teeth then bottom teeth. The ritual exists because kids get bored, forget and rush.

Now imagine a robot that cleans teeth perfectly, but in its own order and without the song. Should we force it to sing? No. We should **check the teeth.** Keep the value and check the result. Let the ritual go if it was only there to help humans.

And the robot might be able to clean trickier teeth than a kid can, so the "this tooth is too hard to clean" line might sit in a different place for the robot.

---

## The grown-up version

### I18 · Values transfer, disciplines don't, thresholds move

This is the sharpest formulation in the conversation. Uncle Bob (paraphrased) thinks it's probably a mistake to impose a human *discipline* on an agent, but **not** a mistake to impose human *values*, though some thresholds may need to change.

Two concrete cases:

**1. TDD is a human discipline, so he doesn't enforce it on agents.**
This is notable coming from one of TDD's best-known advocates. He sees no sense in making an agent write one line of test, then one line of production code, back and forth. Agents naturally write a function and then its tests. He notes that this is closer to how John Ousterhout works (the two publicly debated TDD and function size in 2024-25), and since agents keep falling back to it, he accepts it. The **value** survives: everything is tested. The gates (coverage via CRAP, mutation testing) enforce the value without the ritual.

**2. CRAP thresholds move.**

| Who writes the code | His CRAP threshold |
|---|---|
| Humans | Keep it below ~4 |
| Agents | Set to 6, considering 8 |

His reasoning is that agents have a huge and perfectly accurate short-term memory, so they can hold more paths in mind than a human can. Treat that as **his working hypothesis**: I found no independent research confirming it. His own `crap4java` tool's README sets its failure line at 8.

### I19 · Agent debates generate hypotheses, not authority

He sometimes debates design questions with agents, such as what the CRAP threshold should be. He's explicit that you can't trust any debate you have with an agent, and he has them anyway. Use agent opinions to **generate ideas and surface arguments**, never as **evidence**. Agents are agreeable, persuadable, and confidently wrong in ways a measurement isn't.

---

## Picture it

```
              HUMANS                         AGENTS
 VALUE        tested, clean, structured  ==  tested, clean, structured   (same)
 DISCIPLINE   TDD red-green-refactor     !=  write fn, then its tests    (different ritual)
 THRESHOLD    CRAP <= ~4                 ->  CRAP <= 6 (maybe 8)         (moves)
 ENFORCED BY  habit, review, pairing     ->  deterministic gates         (different mechanism)
```

---

## Why it matters to you

- **Stop copying human process onto agents by default.** Ask of each practice: "Is this the value, or a ritual that helps humans reach the value?"
- **Measure outcomes, not process.** You can't watch an agent "do TDD" meaningfully, but you can measure coverage and mutation score.
- **Tune your thresholds with evidence.** Run your gates at 6 for a while, then 8, and watch the thrash rate and defect rate. Don't settle it by asking the agent.

## Try it this week

Make a three-column table for your team's practices:

| Practice | The value behind it | How a gate could check the value |
|---|---|---|
| TDD | Every behavior is tested | Coverage + mutation score |
| Small functions | Code is understandable and changeable | CRAP threshold |
| Code review | Defects and design flaws get caught | Gates + human architecture review + spot checks |
| "Clean architecture" | Dependencies point toward policy | Dependency fence |

For any practice where the right column is empty, either invent a gate or keep it as a human responsibility on purpose.

## Watch out

- **Some disciplines carry values you haven't named.** Code review also spreads knowledge across the team. If agents write the code and nobody reads it, where does that knowledge come from? (Chapter 8 tackles this.)
- **A looser threshold is an experiment, not a conclusion.** He's still deciding between 6 and 8 himself.
- **Don't swap "the agent agrees" for evidence.** That includes asking an agent whether this chapter is right.

## Check yourself

<details><summary>1. Distinguish a value from a discipline using TDD as the example.</summary>

Value: every behavior is covered by tests that would catch regressions. Discipline: the specific red-green-refactor micro-cycle humans use to get there. Uncle Bob enforces the value on agents (through gates) but not the discipline.
</details>

<details><summary>2. What CRAP thresholds does he use for humans vs agents, and why the difference?</summary>

Below ~4 for humans; 6 (maybe 8) for agents. He attributes the difference to agents' large, accurate short-term memory. That's his hypothesis, not established research.
</details>

<details><summary>3. You ask an agent "Should our threshold be 6 or 8?" and it argues convincingly for 8. Now what?</summary>

Treat it as a hypothesis worth testing. Run with 8 and measure thrash, defects and margin. An agent debate is not evidence.
</details>

---

Previous: [Chapter 5](05-rooms-with-doors.md) · Next: [Chapter 7: The one-dollar house](07-the-one-dollar-house.md)
