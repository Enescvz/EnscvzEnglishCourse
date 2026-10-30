# Conversion progress — 27 October 2026

**Development-only: do not deploy to GitHub Pages.** Counts below are measured directly from the project JSON data.

## Actual learning lessons

- **459** general B2/C1 learning cards (goal 3,500; 3041 still needed).
- **284** separate accounting/finance cards (goal 200; numeric target achieved, editorial validation pending).
- **329** unique phrasal-verb learning cards (goal 600; 271 still needed).
- This conversion adds **71** general cards and **57** phrasal verb cards to the previous snapshot, a total of 128 meaningful cards.
- Each of those new cards includes an original English definition, Turkish meaning, two distinct contextual English example sentences, and a review exercise entry. Phrasal verbs include grammatical structure notes and at least one sense.
- Source-only entries do **not** count as lessons.

## Source-only research candidates

- 3647 general sourced headwords, 1204 phrasal-verb sourced headwords (candidate reference catalogs, not verified teaching lessons).
- 548 source entries currently link to an authored learning card. The number is not an editorial-approval count.
- Phrasal-verb source does not supply CEFR classifications; authored B2 levels are provisional editorial estimates, not source-certified.
- An exact 2,000 B2 / 1,500 C1 split cannot currently be claimed from these sources; do not change source labels to inflate numbers.

## QA and release blockers

- Need to fill definition/meaning/context gaps elsewhere in the old deck: 447 older entries fail the strict two-example gate.
- Other gaps: licensed human voice recordings, podcasts, listening drills, reading and grammar coverage, independent editorial review, actual iPhone WebKit E2E.
- Release gate `readyForRelease`: **false**. Leave the publication lock active.

## Reproduction and incremental authoring

```bash
python3 tools/author_batch_20261027.py  # idempotent: skips already existing cards
python3 tools/build_curriculum_batches.py
python3 tools/build_research_catalog.py
npm run test:all
npm run qa:audio
npm run release:check # must fail until every release gate is proven
```
