# Chapter 1: Fast hands, slow hands

> **In one breath:** Agents write code much faster than you do, so stop competing with them at typing. Your job moves to everything *around* the code: the checks, the structure, the judgment. But mess still slows agents down, so the checks are not optional.

Insights: **I01 · I02 · I03**. Source concepts: C1, C2, C5 (see [SOURCES.md](../SOURCES.md)).

---

## Explain it like I'm five

Imagine a kitchen with a robot cook. The robot chops, stirs and fries ten times faster than the head chef. If the chef keeps grabbing the knife to "help", the whole kitchen goes at the chef's speed. So the smart chef puts the knife down.

But the robot is messy. It leaves peelings on the floor and dirty pans on every burner. After a while the kitchen gets so cluttered that even the robot starts dropping things, burning food and going in circles. So the chef's new job is to:

- write the recipe card (what to cook),
- set up the taste test (did it come out right?),
- put up a cleaning checklist (no dish leaves until the station is clean).

These checks slow the robot down a little. That's fine, as long as **robot + checks is still faster than the chef cooking alone.**

---

## The grown-up version

### I01 · Get the human out of the code loop

Uncle Bob (Robert C. Martin) describes the moment he started using coding agents seriously: they were fast, and having to read and fix their code made *him* the bottleneck. His conclusion, in his words: *"They are fast with code. I am slow with code."* So he hands the code to the agents and works on the scaffolding around it, aiming for a setup where he does not have to read the code at all.

Not reading the code does not mean not checking it. He swaps line-by-line review for other evidence: quality scores (CRAP, Chapter 3), spot checks, and test batteries the agents can't wriggle past.

### I02 · Mess compounds, for agents too

Messy code doesn't just look bad. It makes the next change harder, and that is as true for agents as for people. Uncle Bob saw agents get stuck in loops where fixing one thing broke another, spin without progress, and in one case say outright that they couldn't cope with the code any more. The level of mess that breaks an agent may differ from the level that breaks a human, but the cliff is real.

So "the agent wrote it, who cares what it looks like?" is a trap. Code quality is now a **performance input for your agents**, not just a courtesy to future humans.

### I03 · The productivity margin is the scoreboard

Every check you add slows the agents down. Add enough and they become slower than a human, at which point, as he puts it, you've lost the game. The quantity to watch is the **margin**: how much faster agents-plus-gates are than a competent human doing the same work.

He reports a margin of roughly **2x to 5x** with his full set of gates. For one story: a single unchecked agent pass takes minutes but gives questionable quality, his full multi-agent pipeline takes about an hour, and a human would take about half a day. Treat those numbers as his personal experience on his own projects, not a benchmark.

---

## Picture it

```
            BEFORE                                   AFTER
  +------------------------+          +---------------------------------+
  | human writes code      |          | agents write code (fast)        |
  | human reviews code     |  ---->   |   |                             |
  | human fixes code       |          |   v                             |
  | (everything at human   |          | gates check it (deterministic)  |
  |  speed)                |          |   |  fail -> agents fix, retry  |
  +------------------------+          |   v                             |
                                      | human: structure, judgment,     |
                                      |        spot checks, strategy    |
                                      +---------------------------------+

  margin = (human time for the task) / (agents + gates time)
           keep it > 1, or the gates have eaten your speed-up
```

---

## Why it matters to you

- **Your bottleneck moves.** If you review every line an agent writes, you've capped your throughput at your reading speed. That's the slow path the episode warns about.
- **Quality turns into speed.** A clean codebase is cheaper for agents to work in, so cleaning up is an investment in agent throughput, not overhead.
- **You need a number, not a feeling.** "Agents feel faster" isn't a margin. Time a few real tasks both ways.

## Try it this week

1. Pick one small feature. Time yourself doing it by hand (or estimate honestly).
2. Do it again with an agent and *your current* checks. Time it, including the time you spend reviewing and fixing.
3. Divide. That's your margin. Write it down and track it as you add gates in later chapters.
4. Watch the agent on a messy file and on a clean one. Do you see the "fix one, break another" thrash on the messy one?

## Watch out

- **"Don't read the code" is the end state, not step one.** Uncle Bob earned it by building gates first, and he still spot-checks. Skip the gates and you aren't delegating, you're just not looking.
- **Some code deserves human eyes anyway:** security boundaries, money movement, data deletion, anything regulated. The episode is about general application code. Use judgment.
- **The 2x-5x figure is anecdotal.** It's one expert's report. Your margin depends on your domain, your gates and your agents.

## Check yourself

Try to answer before opening each one.

<details><summary>1. Why is reviewing every line of agent output a problem, if you want speed?</summary>

Because then the whole system moves at human reading speed. The agents' speed advantage disappears into your review queue. The fix is to replace most reading with checks that run automatically.
</details>

<details><summary>2. "The agent wrote it, so code quality doesn't matter." What does the episode say?</summary>

Mess compounds for agents just like for humans. Past some level they thrash: they loop, break things while fixing others, and even give up. Clean code keeps agents productive.
</details>

<details><summary>3. You add five new quality checks, and now a feature takes your agents longer than it would take you. Who won?</summary>

Nobody. You've lost the game. The productivity margin (human time divided by agents-plus-gates time) has to stay above 1. Gates are worth it only while that's true.
</details>

---

Next: [Chapter 2: Rules fade, gates don't](02-rules-fade-gates-dont.md)
