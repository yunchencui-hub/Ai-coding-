# Chapter 8: The general and the sergeant

> **In one breath:** Agents are excellent tacticians and poor strategists, so the human job is strategy. But you can only supervise work you understand, so the next generation still needs to learn to code: first by hand, then as an "agent" under the same gates, then running agents. And the old fundamentals keep coming back, because they're about organizing complexity, which models need too.

Insights: **I25 · I26 · I27 · I28**. Source concepts: C25-C28.

---

## Explain it like I'm five

In an army, the **sergeant** knows how to get the squad across the river: who carries what, where to step. The **general** decides *which* river to cross, and whether to cross at all. Agents are amazing sergeants and terrible generals.

To become a good general, though, you need to have waded a few rivers yourself. A swimming coach can tell a swimmer who is *playing* from one who is *drowning*, because the coach has struggled in the water. Someone who's never swum can't tell the difference.

And every time a new tool arrives, people panic that the old rules are dead. Then, a year later, they're picking the old rules up off the floor, dusting them off, and remembering why they needed them.

---

## The grown-up version

### I25 · Tactical vs strategic: agents took the sergeant's job

Matt Pocock raised Ousterhout's distinction between **tactical** programming (get this feature working now) and **strategic** programming (invest in design so the whole system stays easy to change). Uncle Bob agreed with the sergeant/general framing: agents are really good at tactics and really bad at strategy. Both reached for their copies of Ousterhout's book during this part of the conversation.

### I26 · Human as subagent: the education gauntlet

How should a new engineer learn when agents write the code? Uncle Bob's proposed path:

1. **Write code yourself for about a year**, so you know what the agents are dealing with.
2. **At a company, be treated as an agent.** The lead engineer gives you the same kinds of tasks the agents get and runs you through the same deterministic tools. You spend several months being, in his words, horribly unproductive while learning a huge amount.
3. **Then you may be trusted to run an agent yourself**, under supervision at first.

Underneath that he describes a learning ladder: binary, assembly language, a language like C, a higher-level language like Python, and finally strategically running an agent under supervision. His argument for the low rungs: if all you ever do is write Java, you live in a fantasy world. You don't know what's really happening under the abstraction.

Matt Pocock added a hopeful note: agents compress feedback loops. Strategic mistakes that used to take nine months to show up can now show up fast enough to learn from. His half-joke: become the agent, and have the agent delegate to you.

### I27 · Recognizing thrash is the key diagnostic skill

How did Uncle Bob know the agents were failing when he first used them seriously? He watched them **thrash**, and he recognized the struggle because he had been through it himself. A novice would come in and not recognize it.

His cure for the novice: **read the old books.** He names Tom DeMarco, Ed Yourdon and *The Pragmatic Programmer*, and suggests filtering out the dated parts. Those books were written in the 70s and 80s, when these lessons were first learned.

### I28 · Fundamentals persist up every abstraction rung

His closing argument: software may be the most complex thing humans attempt. (He attributed a version of that line to Dijkstra; I couldn't verify the exact quote.) The fundamentals are how we organize that complexity into something that can be understood, not just by humans but by models, which are modeled on humans.

History rhymes. Binary to assembly, assembly to compilers, compilers to models: every step brought the same panic that the old rules were dead. His warning, roughly: **the rules you throw away now are the ones you'll be picking up off the floor in a year, remembering why you needed them.** He closed by holding up the second edition of *Clean Code* (2025).

---

## Picture it

```
 WHO DOES WHAT
   strategic (the general):  which problem? which modules? which direction?  -> HUMAN
   tactical  (the sergeant): implement, test, refactor, harden               -> AGENTS

 THE EDUCATION GAUNTLET
   [learn the stack: binary -> assembly -> C -> Python]
          |
   [~1 year writing code by hand]
          |
   [months as a "human subagent": same tasks, same gates as the agents]
          |
   [run an agent under supervision]
          |
   [run agents strategically]

 THE ABSTRACTION LADDER (same panic at every rung; fundamentals survive)
   binary -> assembly -> compilers -> high-level languages -> models
```

---

## Why it matters to you

- **Your durable value is judgment:** choosing problems, shaping modules, spotting thrash, deciding direction.
- **Diagnosis needs experience.** If you've never written the kind of code your agents write, you can't tell productive work from flailing. Keep your hands in.
- **Fundamentals are the operating manual for agents.** Coupling, cohesion, information hiding and testing aren't legacy concerns. They're how you make a codebase agent-friendly (Chapters 2 and 5).

## Try it this week

1. **Thrash spotting:** watch an agent session on a hard task without intervening. Note the moments it loops, reverts itself, or "fixes" one test by breaking another. What structural problem was underneath?
2. **Be the subagent:** take one ticket your agents usually get, do it by hand, and run it through `make check`. How did the gates feel from the inside?
3. **Old books:** pick one, such as *The Pragmatic Programmer*, DeMarco's *Structured Analysis*, Yourdon & Constantine's *Structured Design*, Parnas's 1972 paper on decomposing systems into modules, or Brooks's *The Mythical Man-Month*. Read one chapter and ask: "How does this apply to agents?"

## Watch out

- **The gauntlet is a proposal, not a proven program.** Nobody has run this apprenticeship at scale yet. It's a thoughtful hypothesis from an experienced practitioner.
- **"Learn assembly first" is contested.** Plenty of strong engineers never wrote assembly. The underlying point (understand at least one layer below your abstraction) is broadly accepted; the specific ladder is his preference.
- **Strategy isn't safe forever.** Agents' strategic ability may improve. The episode describes the state of things in mid-2026.

## Check yourself

<details><summary>1. In the sergeant/general framing, which role do agents play and which do humans keep?</summary>

Agents are the sergeants: tactical execution. Humans are the generals: strategic choices about direction, structure and trade-offs.
</details>

<details><summary>2. Describe the "human as subagent" stage and why it exists.</summary>

A junior engineer receives the same tasks agents get and goes through the same deterministic gates, under a lead. It builds the hands-on understanding needed later to supervise agents and to recognize their thrash.
</details>

<details><summary>3. Why can an experienced engineer spot agent thrash that a novice misses?</summary>

They've been through the same struggle themselves, so they recognize the pattern: looping, breaking one thing while fixing another, spinning on tangled code.
</details>

<details><summary>4. Why do fundamentals still matter if models write the code?</summary>

Fundamentals organize complexity into understandable pieces, and models, being modeled on humans, benefit from the same organization. Every abstraction jump has triggered a "the old rules are dead" panic, and the rules came back.
</details>

---

Previous: [Chapter 7](07-the-one-dollar-house.md) · Back to the [index](README.md)
