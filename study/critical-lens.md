# Critical lens: agreements, tensions and counterpoints

Understanding an argument includes knowing where it's strong, where it's contested, and what it leaves out. This page separates three things that are easy to blur:

1. **Where the two speakers agree** (from the episode)
2. **Where the conversation pushes against itself or against current fashion** (from the episode)
3. **Counterpoints and gaps** (from outside the episode: my analysis and published research, labeled as such)

---

## 1. Where Matt Pocock and Uncle Bob agree

| Topic | Who proposed it | The other's response |
|---|---|---|
| Deep modules are good for models (I17) | Pocock, via Ousterhout | Bob: agrees, adding that it's "both a danger and an advantage" |
| Agents are tactical, not strategic (I25) | Pocock, via Ousterhout | Bob: agrees; both pull out their copies of Ousterhout's book |
| Sessions have trajectory; clear the context to reset (I12) | Pocock | Bob: agrees and adds the coffee/soap-opera parable |
| Long steering degrades (smart zone / dumb zone) (I04) | Bob (lost in the middle) | Pocock: connects it to Dex Horthy's framing |
| Agents read what they're given; humans don't read agent output (I06) | Pocock | Bob: adds the mirror half |
| Feedback loops for learning strategy are faster now (I26) | Pocock | Bob's apprenticeship model rests on the same idea |

The overall picture is a **host who brings modern agent-engineering vocabulary** (Ousterhout, Horthy, trajectory) and a **guest who maps it onto fifty years of practice**. They agree more than they disagree.

## 2. Tensions inside the conversation

These are the most interesting places to think hard.

**a) The TDD champion doesn't impose TDD on agents (I18).**
Uncle Bob is one of TDD's best-known advocates, and he publicly debated Ousterhout on it in 2024-25. Here he lets agents write code first and tests after, which is closer to Ousterhout's style. His reconciliation is that TDD is a human discipline serving a value (everything tested), and gates enforce the value. *Question to sit with:* was TDD ever only about test coverage, or also about design pressure (writing the test first shapes the interface)? If it's the latter, what gives agents that pressure? His candidates would be the CRAP gate and the fence.

**b) "Don't read the code" vs "you must have written code to supervise" (I01 vs I26-I27).**
He aims to never read agent code, yet his ability to spot thrash comes from decades of reading and writing code. His apprenticeship model is his answer to this tension: he wants humans to build that experience deliberately, under the gates. It's still an open question whether that produces the same depth of judgment.

**c) Spec-driven development (I20, I23).**
Pocock raises spec-driven development, a popular approach in 2025-26. Uncle Bob is skeptical: he expects heavy specs to repeat waterfall, and his own specs are ephemeral. This is the episode's clearest disagreement with current fashion. Note that it's a prediction, and teams do report success with spec-first agent workflows.

**d) Automating architecture.**
Bob says the human still designs module structure (I13) and that his attempts to automate it haven't worked (I21). The whole system depends on a step that doesn't yet scale beyond the human.

## 3. Counterpoints and gaps (outside the episode)

These are **my analysis, informed by published research**, not claims made in the episode.

**Gates measure what's measurable.** CRAP, mutation testing and a dependency fence say nothing about:
- **security** (injection, auth bypass, secrets): you need SAST, dependency scanning and threat modeling;
- **performance**: you need benchmarks and budgets;
- **UX and product fit**: the QA seat covers flows, not whether users want it;
- **data correctness at scale**, migrations, privacy compliance.

A "never read the code" stance should be scoped to what your gates cover. For high-stakes paths, human review still pays for itself.

**Metric gaming is the classic failure of metric gates.** Agents optimize what you measure (Goodhart's law). Known holes:
- assertion-free tests inflate coverage and so lower CRAP (mutation testing plugs this, which is why both gates matter);
- splitting functions mechanically lowers CC without improving design (Ousterhout's "shallow modules" warning);
- agents may write tests that pin the *current* behavior, bugs included.

**100% mutation score is generally unreachable.** Equivalent mutants (changes that don't alter behavior) are undecidable to detect in general, and studies estimate them at roughly 4-39% of mutants. A "merciless" hardener needs a documented way to excuse them, or it will either loop forever or "kill" them with absurd tests. (`tools/mutate.py` uses a `# mutate: skip -- <reason>` comment.)

**CRAP's exponents were set by discussion, not calibration.** Its authors said so. It's a good heuristic for "complex and untested", not a precise risk measure. It's also blind to coupling between functions.

**Several numbers are one person's experience.** The 2x-5x margin, the 30-minute mutation runs and the "perfect short-term memory" rationale come from one expert on his own (often Clojure) projects. They're plausible and worth testing, not established.

**The relay has coordination costs.** Brooks's law ("adding manpower to a late project makes it later") has an agent analogue: more agents means more handoffs. Bob acknowledges the overhead; small tasks may not justify five seats.

**Who tests the tester?** If gates are the only check, the gates themselves must be correct. A buggy CRAP tool or a fence with a wrong map silently waves bad code through. (That's why this repository tests its tools, and the tools pass their own gates.)

**Team and legacy context.** The episode reflects a solo expert's workflow. In teams, the fence file and thresholds become shared agreements. On legacy codebases, an immediate hard gate can block all work, so ratchets (no function may get worse) are the usual on-ramp.

## Open questions worth tracking

1. Can module design (the strategic step) be automated, or will it stay human?
2. What's the right CRAP threshold for agent-written code: 6, 8, or something that depends on the model?
3. Does the "human subagent" apprenticeship produce engineers with strong judgment?
4. Do ephemeral specs lose institutional memory ("why is it like this?") over years?
5. As models improve, which of today's gates become unnecessary, and which become *more* important?
