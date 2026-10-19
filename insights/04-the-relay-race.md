# Chapter 4: The relay race

> **In one breath:** Don't have one agent do everything in one long session. Run a relay of specialists (specifier, coder, cleaner, hardener, QA), each starting with a fresh context, doing one job, and handing off. A long session drifts in whatever direction it started.

Insights: **I10 · I11 · I12**. Source concepts: C9, C10, C11. Templates: [`playbook/roles/`](../playbook/roles/).

---

## Explain it like I'm five

A relay race has four runners. Each runs one leg as hard as they can and hands the baton on. Nobody runs the whole race, because by the end they'd be exhausted and slow.

Agents get "tired" too, in their own way. Their memory (the context window) fills up with everything that happened earlier, and the important bits get lost in the clutter. So each runner starts fresh, does one leg, and passes a clean baton (the finished work plus a short note).

There's a second problem. Imagine you and a friend are chatting about coffee, and someone walks by loudly describing a soap opera. Suddenly every coffee joke turns into a soap-opera joke. You can't un-hear it. That's what happens to an agent when one session gets steered somewhere: everything afterward follows that path. The only reliable fix is a fresh conversation.

---

## The grown-up version

### I10 · The five-seat relay

Uncle Bob's pipeline, in his description:

| Seat | Job | Its gate (what "done" means) |
|---|---|---|
| **1. Specifier** | Turns a human-written story into a **Gherkin** acceptance test (given / when / then) and a **QA procedure** written from a human user's point of view: "you are a person operating this system through the UI; prove it works." | Spec + QA procedure exist and are reviewable by a human |
| **2. Coder** | Writes unit tests and the code that implements the story, and makes the Gherkin pass | Tests + acceptance tests green |
| **3. Cleaner** | Runs CRAP analysis and general code review, and cleans up the mess the coder made (he expects there to be one) | CRAP under threshold, tests still green |
| **4. Hardener** | Runs mutation testing mercilessly and closes every hole; full coverage | No surviving mutants (minus documented equivalents) |
| **5. QA** | Turns the written QA procedure into an executable script that drives the system and gives a deterministic result | QA script passes |

He's candid about the cost: the handoffs add a lot of communication overhead. Even so, he reports the whole relay is still well ahead of a human (Chapter 1's margin).

Uncle Bob's public orchestrator, `unclebob/swarm-forge`, ships packs of roles along these lines: a two-role coder→cleaner pack, a four-role pack, and a six-role pack covering specification, implementation, cleanup, architecture, hardening and QA. Each agent works in its own git worktree, and work moves between them through committed handoffs.

### I11 · Born, do the task, die

Each agent is created for one task, does it, and exits, so the next one starts with a clean context. That keeps each context small and inside the high-attention zone (Chapter 2), and the lost-in-the-middle problem mostly goes away.

Trade-offs he names:

- **Cost:** startup is slow. An agent can take 10-15 seconds just to start, and then it has to rebuild its understanding of the codebase.
- **Benefit:** parallelism. Several coders can run at once on one laptop.

### I12 · A context window has momentum

Matt Pocock's observation: steer an agent one way early in a session and everything after follows that **trajectory**. The only way to clear it is to clear the context. Uncle Bob agreed and offered the coffee/soap-opera parable. The model can't separate the relevant thread from the noise that got mixed in.

Practical upshot: when an agent goes off the rails, **don't argue with it in the same session.** Fix the instructions and start a fresh one.

---

## Picture it

```
 human story
     |
     v
 [1 SPECIFIER] --Gherkin + QA procedure--> [2 CODER] --code + tests-->
                                                                     |
     +---------------------------------------------------------------+
     v
 [3 CLEANER: CRAP] --clean code--> [4 HARDENER: mutation] --hardened-->
                                                                     |
     +---------------------------------------------------------------+
     v
 [5 QA: executable script] --pass--> human looks at architecture, then next story

 each [box] = fresh agent: born -> does one job -> passes its gate -> dies
```

---

## Why it matters to you

- **Specialization beats one do-everything prompt.** Each role prompt is short and focused, so it stays in the smart zone.
- **Separation of duties catches errors.** The cleaner doesn't feel attached to the coder's mess, and the hardener assumes the tests are weak.
- **Fresh context is a debugging tool.** A drifting session costs more to rescue than to restart.

## Try it this week

1. Start with the two-seat version: **coder → cleaner**. Use [`playbook/roles/coder.md`](../playbook/roles/coder.md) and [`playbook/roles/cleaner.md`](../playbook/roles/cleaner.md).
2. Run each as a *separate* agent session. Pass work between them through git commits, not a shared chat.
3. When that works, add the **hardener** ([`hardener.md`](../playbook/roles/hardener.md)) with `make mutate` as its gate.
4. Finally, add the **specifier** and **QA** seats. See [`example/features/checkout.feature`](../example/features/checkout.feature) for a Gherkin spec that this repo actually executes as a test.

## Watch out

- **Overhead is real.** For a one-line fix, five agents is silly. Scale the relay to the risk of the change.
- **Handoff notes are a new failure point.** If the coder's note is vague, the cleaner starts confused. Keep handoffs structured: what changed, which gates pass, what's left.
- **Parallel coders need boundaries.** Two agents editing the same module will collide. The module structure in Chapter 5 is what makes parallelism safe.
- **"Fresh" doesn't mean "uninformed".** Each agent still needs the right short context: its role, the story, the gates. It just shouldn't carry yesterday's chatter.

## Check yourself

<details><summary>1. Name the five seats in order and the main gate for each.</summary>

Specifier (Gherkin + QA procedure), Coder (unit + acceptance tests green), Cleaner (CRAP), Hardener (mutation testing), QA (executable QA script passes).
</details>

<details><summary>2. Why not run all five roles in one long session?</summary>

The context fills up and gets lost in the middle, and early steering creates a trajectory that pollutes later work. Fresh, single-task agents keep context small and clean.
</details>

<details><summary>3. An agent has been steered into a bad approach. Should you keep correcting it in the same session?</summary>

Usually not. The trajectory persists, so it's better to fix the instructions and start a fresh session.
</details>

<details><summary>4. What's the cost of the born-do-die approach?</summary>

Startup time (seconds per agent, plus rebuilding its understanding of the codebase) and communication overhead between seats. He reports the relay is still much faster than a human.
</details>

---

Previous: [Chapter 3](03-boring-tools-come-back.md) · Next: [Chapter 5: Rooms with doors](05-rooms-with-doors.md)
