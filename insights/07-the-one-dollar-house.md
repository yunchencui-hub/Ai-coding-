# Chapter 7: The one-dollar house

> **In one breath:** When change is nearly free, giant up-front plans lose their point, because they're the old waterfall temptation in new clothes. Work in small batches, look at the result, adjust. The finished system is the real specification. And to specify a tool, point your agents at a good example rather than writing a long description.

Insights: **I20 · I21 · I22 · I23 · I24**. Source concepts: C19-C23.

---

## Explain it like I'm five

You're building a Lego house. If every brick cost $1,000 and took a week to place, you'd draw careful blueprints first. Mistakes would be expensive.

Now imagine every change costs **one dollar** and takes a second. Would you spend a month on blueprints? No. You'd build a bit, look at it, move the door, add a window, look again. The house itself shows you what you want.

Also, when you want a treehouse like your friend's, you don't write a 20-page description. You **point**: "Like that one, but for my tree, and with a rope ladder."

---

## The grown-up version

### I20 · Heavy up-front specs are the 1970s temptation, replayed

Uncle Bob sees an old pattern returning: the urge to specify, specify, specify, then hand everything to the agent. In the 70s the same urge gave us the **waterfall** process.

He was trying exactly this the week of the conversation and says it keeps going wrong. You write a big plan, the agents start, and partway through you discover they can't follow it because the plan didn't anticipate everything. They charge off in a bad direction, and you have to stop, back up and rewrite the plan. He also notes that agents *love* writing plans. The plans look beautiful and fall apart at the end.

On **spec-driven development** (a popular 2025-26 approach), his impression is that it probably won't work. This is one of the clearest points where the conversation pushes back on current fashion.

### I21 · Agile small batches, for agents

His alternative: let the agents do a story or two, look at the architecture, maybe intervene by hand, then a few more stories. He admits we may never escape that manual "organize the structure" step at the end of each batch, though he's trying.

### I22 · The $1 house: when change is cheap, plan less

His thought experiment: if every change to a house cost $1, nobody would pay an architect for a perfect up-front design. You'd fiddle until it looked right. He argues that agents have pushed the cost of code changes about as close to zero as we'll ever get, so the case for expensive up-front planning collapses.

### I23 · Specs are ephemeral; the end result is the specification

In his workflow the specs (stories, Gherkin, plans) are **ephemeral**: used, then gone. He points out that source code used to be the final specification, the one thing humans wrote and kept, and that role no longer exists in the same way. Instead of writing a spec that defines what he wants, he looks at the end result and treats *that* as the specification.

Matt Pocock asked whether *persistence* is what separates spec-driven development from this, meaning spec-driven development keeps the spec around. Uncle Bob's answer: his specs don't persist.

### I24 · Point, don't download

He has published his CRAP tools, mutation tester and agent harness, and his advice is surprising: **don't download them.** He wrote them for himself. Instead, point your agents at them, have the agents study them, and build your own version. He sees this as a far better way to specify the *essence* of a tool and customize it to your situation.

**This repo follows that advice.** The Python tools in [`tools/`](../tools/) were written independently from the published formulas and descriptions, not ported from his code, and they're single-file and dependency-free so your agent can read one and build its own.

---

## Picture it

```
 WATERFALL (expensive change)            ONE-DOLLAR HOUSE (cheap change)
 spec spec spec spec spec                story -> build -> LOOK
            |                                 ^              |
            v                                 |   adjust     |
          build build build                   +--------------+
            |                            every 1-2 stories: human reviews architecture
            v
        "it doesn't match"               spec = the thing you can see working

 POINT, DON'T DOWNLOAD
   "Here is tools/crap.py. Study it. Build one for our TypeScript monorepo
    that reads istanbul JSON, gates at 6, and checks only changed files."
```

---

## Why it matters to you

- **Beware the beautiful agent plan.** A plan that looks thorough isn't proof that the agents can execute it. Prefer a thin slice that works.
- **Small batches are a structural safety valve.** Reviewing architecture every story or two catches drift while it's cheap to fix.
- **Exemplars beat descriptions.** One good example file teaches an agent more than pages of requirements.

## Try it this week

1. Next feature: instead of a big plan, write **one** story. Let the agent build it through your gates. Look at the result, then write the next story.
2. After every one or two stories, spend 10 minutes on the architecture: run `make fence`, look at the CRAP report, ask the agent to describe the structure.
3. Pick one tool from this repo. Point your agent at it and ask it to build the equivalent for your stack. Compare the two.

## Watch out

- **"No big plan" is not "no thinking".** The human still owns strategy, module boundaries and what to build. The batch is small; the intent isn't vague.
- **Not every domain has $1 changes.** Database migrations, public APIs, hardware, regulated systems and anything with external users carry real change costs. Plan more where change is expensive.
- **Ephemeral specs can cost you the "why".** If specs vanish, record important decisions somewhere durable (ADRs, commit messages), or the reasoning goes with them.
- **This is one practitioner's view on spec-driven development.** Teams report success with spec-first workflows too. Test it in your context; both views are hypotheses.

## Check yourself

<details><summary>1. Why does Uncle Bob compare heavy agent specs to waterfall?</summary>

Both rest on the idea that you can specify everything up front. In practice the agents hit cases the plan didn't anticipate, go off course, and force you to back up and re-plan, just as waterfall projects discovered problems late.
</details>

<details><summary>2. What is the "$1 house" argument in one sentence?</summary>

When every change is nearly free, the expensive up-front design that exists to avoid costly changes stops paying for itself, so you iterate instead.
</details>

<details><summary>3. He published his tools. What does he tell you to do with them, and why?</summary>

Don't download them. Point your agents at them so they can study them and build versions tailored to you. An exemplar specifies the essence of a tool better than a description.
</details>

---

Previous: [Chapter 6](06-values-not-rituals.md) · Next: [Chapter 8: The general and the sergeant](08-the-general-and-the-sergeant.md)
