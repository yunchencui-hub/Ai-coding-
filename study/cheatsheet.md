# Cheat sheet: Uncle Bob on software fundamentals in the age of AI

**The whole episode in one sentence:** let agents write the code, but build a cage of deterministic checks and good structure around them, because the fundamentals that make code manageable for humans make it manageable for models.

## The 28 insights in one line each

**1 · Fast hands, slow hands**
- **I01** Agents are fast at code, you're slow: give them the code and take the scaffolding.
- **I02** Mess compounds for agents too; past a point they thrash and give up.
- **I03** Score yourself on the margin: agents + gates must beat a human (he reports 2-5x).

**2 · Rules fade, gates don't**
- **I04** Long prompt rules become "guidelines" (lost in the middle). Keep the prompt tiny.
- **I05** Gate loop: change the code until the tool says OK.
- **I06** Agents read everything; humans read nothing agents write. Long for agents, short for humans.

**3 · Boring tools come back**
- **I07** CRAP = CC² × (1 − cov)³ + CC. Fully tested gives CRAP = CC.
- **I08** Mutation testing: inject tiny bugs; every mutant must make a test fail.
- **I09** Revive ideas that died only of tedium. Agents don't get bored.

**4 · The relay race**
- **I10** Specifier → Coder → Cleaner (CRAP) → Hardener (mutation) → QA (script).
- **I11** Agents are born, do one task, and die. Fresh context, parallel coders, slow startup.
- **I12** Sessions have momentum; reset the context to reset the trajectory.

**5 · Rooms with doors**
- **I13** Ask agents about the structure, get scared, design the modules yourself.
- **I14** Have agents build your instruments (an architecture viewer).
- **I15** Dependency fence: a spec file plus a checker. Repairs: invert, interface, split.
- **I16** Compartments help models like they help humans.
- **I17** Deep modules mean agents read the interface and tests, not the internals.

**6 · Values, not rituals**
- **I18** Impose values (tested, clean), not disciplines (strict TDD). Thresholds move: CRAP ~4 for humans, 6-8 for agents.
- **I19** Debating with agents gives you hypotheses, not evidence.

**7 · The one-dollar house**
- **I20** Big up-front agent specs = waterfall again. Beautiful plans fall apart.
- **I21** Small batches: a story or two, then look at the architecture.
- **I22** Change costs about $1 now, so fiddle until it's right instead of over-planning.
- **I23** Specs are ephemeral; the working result is the spec.
- **I24** Point, don't download: agents study an exemplar and build your version.

**8 · The general and the sergeant**
- **I25** Agents are tactical sergeants; humans are strategic generals.
- **I26** Learning path: code by hand ~1 year, then be a "human subagent" under the gates, then run agents.
- **I27** Spotting thrash takes having struggled. Read the old books.
- **I28** Fundamentals survive every abstraction jump. Thrown-away rules come back.

## Numbers worth remembering

| Thing | Value |
|---|---|
| CRAP threshold for human code (his) | below ~4 |
| CRAP threshold for agent code (his) | 6, maybe 8 |
| Classic CRAP "crappy" line (Savoia & Evans) | 30 |
| CC 2, untested | CRAP 6 |
| CC 5, untested | CRAP 30 |
| Agent startup cost he cites | ~10-15 s |
| Mutation run, ~2000 vs now (his account) | overnight vs ~30 min |
| Margin he reports | ~2x-5x |
| Equivalent mutants (research) | ~4-39% of mutants |

## The loop, drawn

```
 story -> [specifier] -> [coder] -> [cleaner: CRAP] -> [hardener: mutation] -> [QA script]
              each seat: fresh agent, one job, must pass its gate, then exits
 every 1-2 stories: human reviews architecture (fence, viewer, CRAP report)
```

## This repo's gates

```bash
make crap     # fails if any function's CRAP > 6
make mutate   # fails if any mutant survives
make fence    # fails if a module imports something it isn't allowed to
make check    # all of the above, plus tests and generated-file freshness
```
