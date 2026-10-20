# Sources, provenance and confidence

This file explains where every claim in this repository comes from and how much weight it can bear. Please read it before you quote anything from here.

## The episode

| | |
|---|---|
| **Title** | LIVE: Uncle Bob on Software Fundamentals in the Age of AI |
| **URL** | https://www.youtube.com/live/zcLPGC-tvgk |
| **Host** | Matt Pocock |
| **Guest** | Robert C. Martin ("Uncle Bob") |
| **Date** | Wednesday, 19 August 2026 (livestream) |
| **Length** | about 57 minutes |
| **Format** | Two-person video conversation; no slides or screen shares reported |

## How this repository was built, and its limits

**I could not watch the video directly.** The environment that produced this repository had no network access to YouTube. Instead, the insights were reconstructed from secondary sources and cross-checked against each other:

1. **The primary secondary source** is a community analysis of the episode built from the video's own auto-captions: the *Concept Ledger* and *Extraction* notes in [Island-Dev-Crew/uncle-bob-skills](https://github.com/Island-Dev-Crew/uncle-bob-skills) (`docs/01-CONCEPT-LEDGER.md`, `docs/00-EXTRACTION.md`). It breaks the conversation into 28 numbered concepts (**C1-C28**), each backed by a short quote from the auto-captions. The `C` numbers in this repo refer to that ledger, so you can trace any insight back to its quote there.
2. **Independent corroboration** came from search-engine summaries of other write-ups of the same episode, which agree on the core claims: the five-role agent pipeline (specifier, coder, cleaner, hardener, QA), reviving CRAP and mutation testing as agent-run gates, deterministic gates over prompt steering, and "values, not disciplines":
   - besthub.dev, *Uncle Bob's AI Coding Pipeline: 5-Agent Gauntlet & Architecture Governance* (26 Aug 2026)
   - sozai.app transcript summary: https://sozai.app/transcript/uncle-bob-software-fundamentals-ai/
   - howardism.dev articles on Robert C. Martin and reviving impractical quality tools
   - daily.dev listing: https://daily.dev/posts/live-uncle-bob-on-software-fundamentals-in-the-age-of-ai-tb2uozdzr
   - Matt Pocock's announcement posts on X ("If your code sucks, your agent will too...")
3. **Primary artifacts I checked directly:** the READMEs of Uncle Bob's public repositories [`unclebob/crap4java`](https://github.com/unclebob/crap4java), [`unclebob/crap4go`](https://github.com/unclebob/crap4go), [`unclebob/crap4clj`](https://github.com/unclebob/crap4clj) and [`unclebob/swarm-forge`](https://github.com/unclebob/swarm-forge). They exist, implement the CRAP formula quoted in Chapter 3, and (for swarm-forge) describe two-, four- and six-role agent packs.

What this means for you:

- The **ideas and their attribution** are well supported: several independent sources agree.
- The **exact wording** of the short quotes comes from auto-captions as recorded by the community ledger. Auto-captions garble words: the ledger notes, for example, "claw.md" for CLAUDE.md, "Dex Hardy" for Dex Horthy and "crap" for C.R.A.P. Treat the quotes as close to verbatim, not as certified transcripts.
- **Speaker attribution** (who said what) follows the ledger's reading of a two-voice conversation and is occasionally a judgment call.
- If precision matters (for a talk, an article, a decision), **watch the relevant part of the video yourself.** The ledger's concept numbers make each claim easy to find.

## Confidence labels used in `data/insights.json`

| Label | Meaning |
|---|---|
| `episode` | Said in the episode, per the sources above. This is the speaker's view, not established fact. |
| `episode+verified` | Said in the episode, and the factual part was checked independently (see below) |
| `episode+anecdotal` | Said in the episode, but it's the speaker's personal experience or hypothesis (numbers, rationales), with no independent evidence found |

## Factual claims checked independently

| Claim | Status | Reference |
|---|---|---|
| CRAP formula `CC² × (1 − cov)³ + CC`, created by Alberto Savoia & Bob Evans, 2007 | Verified | Savoia, "Pardon My French, But This Code Is C.R.A.P." (Artima, 2007); `unclebob/crap4*` READMEs |
| Uncle Bob publishes CRAP tools and an agent orchestrator | Verified | `unclebob/crap4java`, `crap4go`, `crap4clj`, `swarm-forge` |
| "Lost in the middle": LLMs use the start and end of long contexts better than the middle | Verified | Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*, TACL 2024 |
| "Smart zone / dumb zone" framing is Dex Horthy's (HumanLayer) | Verified per the community research notes; the caption reads "Dex Hardy" | Horthy, *12-Factor Agents*; Pragmatic Engineer interview |
| Mutation testing dates to Lipton (1971) and DeMillo, Lipton & Sayward (1978) | Verified | DeMillo, Lipton & Sayward, "Hints on Test Data Selection", *IEEE Computer*, 1978 |
| A 100% mutation score is generally unreachable because of equivalent mutants | Verified (research consensus) | Budd & Angluin (1982) on undecidability; empirical studies estimate roughly 4-39% equivalent mutants |
| Deep modules, tactical vs strategic programming | Verified as Ousterhout's concepts | John Ousterhout, *A Philosophy of Software Design* |
| Ousterhout and Martin publicly debated TDD, comments and function size | Verified | github.com/johnousterhout/aposd-vs-clean-code (2024-25) |
| *Clean Code*, 2nd edition, exists (2025) | Verified | Pearson / InformIT listing |
| "Agents have a huge, perfectly accurate short-term memory" (his reason for a looser CRAP threshold) | **Not verified**: his working hypothesis | none found |
| Productivity margin of roughly 2x-5x | **Not verified**: his personal experience | none found |
| "Software is the most complicated thing humans have attempted" attributed to Dijkstra | **Not verified as a verbatim Dijkstra quote**; he hedged it himself | nearest: Dijkstra, *The Humble Programmer* (EWD340) |

## Copyright and fair use

The conversation belongs to Robert C. Martin and Matt Pocock. This repository does **not** contain a transcript. It contains original explanations, a few short attributed phrases for commentary, and links to the sources. The tools in `tools/` are independent implementations of published ideas (the CRAP formula, mutation testing, dependency rules), not copies of anyone's code.
