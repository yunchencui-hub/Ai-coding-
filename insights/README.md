# The insights, chapter by chapter

28 insights in 8 chapters. Each chapter follows the same shape so your brain knows where to look:

1. **In one breath:** the whole chapter in two sentences
2. **Explain it like I'm five:** an everyday analogy
3. **The grown-up version:** what was actually said, attributed
4. **Picture it:** a diagram
5. **Why it matters to you**
6. **Try it this week:** something to do, often with this repo's tools
7. **Watch out:** limits, edge cases, counterpoints
8. **Check yourself:** questions with hidden answers (answer before you peek)

| # | Chapter | The big idea | Insights |
|---|---|---|---|
| 1 | [Fast hands, slow hands](01-fast-hands-slow-hands.md) | Agents own the code; you own everything around it | I01-I03 |
| 2 | [Rules fade, gates don't](02-rules-fade-gates-dont.md) | Short prompts + deterministic checks beat long rule files | I04-I06 |
| 3 | [Boring tools come back](03-boring-tools-come-back.md) | CRAP and mutation testing are practical now that agents do the tedium | I07-I09 |
| 4 | [The relay race](04-the-relay-race.md) | Specialist agents in fresh contexts: specifier → coder → cleaner → hardener → QA | I10-I12 |
| 5 | [Rooms with doors](05-rooms-with-doors.md) | Structure helps models like it helps people; enforce it with a fence | I13-I17 |
| 6 | [Values, not rituals](06-values-not-rituals.md) | Keep the values (tested, clean), drop human-only rituals (strict TDD), move thresholds | I18-I19 |
| 7 | [The one-dollar house](07-the-one-dollar-house.md) | Cheap change kills big up-front plans; iterate in small batches | I20-I24 |
| 8 | [The general and the sergeant](08-the-general-and-the-sergeant.md) | Agents do tactics, humans do strategy; learn the fundamentals to supervise | I25-I28 |

## How the ideas connect

```
                 Agents are fast, humans are slow (1)
                               |
          so humans leave the code loop... but mess compounds (1)
                               |
             so quality must be enforced without human reading
                               |
          +--------------------+---------------------+
          |                                          |
  prompts fade (2)                       gates don't fade (2)
  keep them tiny                                     |
                         +-----------------+---------+-----------+
                         |                 |                     |
                  CRAP + mutation    dependency fence      relay of fresh
                  revived (3)        + module design (5)   specialists (4)
                         |                 |                     |
                         +--------+--------+---------------------+
                                  |
            values stay, rituals go, thresholds move (6)
                                  |
             change is cheap -> small batches, not big specs (7)
                                  |
     humans own strategy; they learn it by first doing the tactics (8)
```

**One-sentence version of the whole episode:** *Let agents write the code, but build a cage of deterministic checks and good structure around them, because the fundamentals that made code manageable for humans are exactly what make it manageable for models.*

Next: try the [quiz](../study/quiz.md), import the [flashcards](../study/flashcards.csv), or put it into practice with the [playbook](../playbook/README.md).
