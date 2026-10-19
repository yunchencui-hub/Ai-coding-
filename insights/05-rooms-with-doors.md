# Chapter 5: Rooms with doors

> **In one breath:** Structure still matters, and for the same reason as with people: models understand compartmentalized code better. Ask the agents what the structure is, expect to be scared, design the modules yourself, and lock the design in with a dependency fence that a tool enforces.

Insights: **I13 · I14 · I15 · I16 · I17**. Source concepts: C12-C16. Hands-on: [`tools/fence.py`](../tools/fence.py), [`example/fence.toml`](../example/fence.toml).

---

## Explain it like I'm five

A good house has rooms, and each room has a job: you cook in the kitchen and sleep in the bedroom. Doors connect some rooms and not others. You can make a sandwich without knowing how the bathroom plumbing works.

A bad house is one giant room with the stove next to the bed and the bathtub in the hallway. Everyone (people *and* robots) gets confused about what goes where.

Now add **house rules**: "the kitchen opens to the dining room, never into the garage." Then post a guard at each door who checks every trip. That guard is the **dependency fence**.

Finally, think of a **TV remote**: a few simple buttons on the outside and lots of clever electronics inside. You use it without opening it. That's a **deep module**, and agents love them for the same reason you do.

---

## The grown-up version

### I13 · Interrogate the agents about structure, and expect to be scared

Uncle Bob's practice: ask the agents what the structure of the system is and how modules relate. He says the answers frightened him. Then he designs a module structure himself and gives the agents an implementation plan to get there.

He's tried to automate this design step and says it hasn't worked well so far. **Module design is still a human job** in his workflow.

### I14 · Have agents build your instruments

He had his agents build him an **architecture viewer**: a UML-style diagram of the modules and which way the dependencies run. He can click into a module to see its submodules and pull up the code. (His public repos include `uml-viewer`, which can overlay CRAP scores from `crap4clj`.)

The lesson generalizes: **agents are great at building the dashboards and tools you use to supervise agents.**

### I15 · The dependency fence

He describes another deterministic tool: a tight little specification file saying which module may depend on which and which way dependencies must flow. Agents can't violate it, because a checker runs at the end and fails the build.

When the fence fails, there are three standard repairs:

1. **Invert the dependency.** Make the low-level thing depend on the high-level one.
2. **Insert an interface.** Depend on an abstraction, not a concrete module.
3. **Split the module in half.** It was doing two jobs.

**In this repo:** [`example/fence.toml`](../example/fence.toml) says `checkout` may use `cart` and `pricing`, but **not** `storage`. Checkout still needs to load carts, so [`checkout.py`](../example/shop/checkout.py) declares a small `CartStore` interface and accepts any object that fits. That's repair #2 already applied. Run `make fence` to check it.

### I16 · Compartmentalization serves models like it serves humans

Uncle Bob's argument: well-partitioned code with disciplined interfaces is graspable by humans because we compartmentalize in our heads, and models do the same. Stuff a module with everything under the sun and the agent won't know what it's doing in there. It's the coffee/soap-opera problem from Chapter 4, at the scale of a module instead of a conversation.

### I17 · Deep modules are context economy

Matt Pocock brought in John Ousterhout's idea (*A Philosophy of Software Design*) that a **deep module** has a small, simple interface hiding a lot of implementation. He suggested this suits models well: they can read the interface and skip the implementation. Uncle Bob agreed. Agents pay attention to structure, and good structure lets them skip the code beneath, which he called both a danger and an advantage. It works as long as the code underneath is consistent. He added that agents also read **tests** to understand what a system does.

In context-window terms, a deep module is **cheap to load**: interface + doc comment + tests, without the internals.

---

## Picture it

```
 THE FENCE FOR example/shop          (arrows = "may import")

        +----------+
        | checkout |-------------+
        +----------+             |
          |      \               v
          |       \         +---------+
          |        +------->| pricing |
          v                 +---------+
     (CartStore                  |
      interface)                 v
          ^                 +---------+
          :  satisfies      |  cart   |  <- depends on nothing
     +---------+            +---------+
     | storage |------------------^
     +---------+

 checkout -> storage is FORBIDDEN. Checkout declares CartStore; storage happens to fit it.

 SHALLOW vs DEEP
   shallow:  [ big interface | tiny implementation ]     agent must read everything
   deep:     [ small iface ]
             [ ............. large hidden implementation ............. ]
             agent reads the iface + tests and moves on
```

---

## Why it matters to you

- **Structure is now a lever on agent performance**, not just maintainability. Messy boundaries mean confused agents and more thrash.
- **Architecture is enforceable.** A fence turns "please respect the layering" (a fading rule) into a failing build (a gate).
- **Your time is best spent here.** If agents write the code, the human's highest-leverage work is module boundaries and dependency direction.

## Try it this week

1. Ask your agent: *"Describe the module structure of this repo. Which modules depend on which? Where are the cycles?"* Compare the answer to what you believed.
2. Draw the dependency graph you *want*. Write it as a fence file. The format is in [`tools/fence.py`](../tools/fence.py).
3. Run the checker. Every violation is a design conversation: invert, interface, or split?
4. Add the fence to your gate command so no agent can merge a violation.
5. Ask an agent to build you a small viewer that renders the fence file and the actual imports as a diagram.

## Watch out

- **Deep modules have a danger side too,** which Uncle Bob flagged himself. If agents trust the interface and skip the implementation, an inconsistent implementation will mislead them. Mutation tests and contract tests keep interfaces honest.
- **A fence is only as good as its map.** If the map is wrong (modules carved along the wrong lines), enforcing it hard just makes the wrong structure rigid. Revisit it as the design evolves.
- **Don't let agents edit the fence to pass the gate.** Changing `fence.toml` is a *design* decision. Treat it like a code-owner-protected file.

## Check yourself

<details><summary>1. Your fence fails: module `billing` imports `email`, which isn't allowed. Name the three standard repairs.</summary>

Invert the dependency, insert an interface (for example, billing declares a `Notifier` interface that an email adapter implements), or split the module.
</details>

<details><summary>2. Why are deep modules especially good for agents?</summary>

The agent can understand and use them from the small interface (plus tests) without loading the large implementation. That saves context and attention.
</details>

<details><summary>3. In Uncle Bob's workflow, who designs the module structure: agents or humans?</summary>

Humans, for now. He interrogates the agents about the existing structure, designs the target structure himself, and gives them an implementation plan. His attempts to automate this haven't worked well yet.
</details>

---

Previous: [Chapter 4](04-the-relay-race.md) · Next: [Chapter 6: Values, not rituals](06-values-not-rituals.md)
