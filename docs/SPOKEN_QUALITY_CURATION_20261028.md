# American English Lab — Daily Conversation Quality Pass
**2026-10-28 | INTERNAL DEV RECORD — NOT A RELEASE APPROVAL**

## Purpose
Prioritize highly useful American English for B1→advanced listening and speaking, rather than inflate a vocabulary count with rare topic-specific words, archaic forms, or A1/A2 words already likely familiar.

## What was changed (verified in code)
- **91 focus-word replacements:** 55 B2 and 36 C1, with sourced headword-level candidate labels, original draft English definitions, Turkish glosses, two different context sentences, and editorial rationale.
- **1,000 focus words maintained:** 500 B2 + 500 C1, without new duplicate IDs. No change to 284 optional finance cards.
- **91 original cards archived in `data/archived-vocabulary.json`:** preserve their original IDs and text, **not** deleted or remapped as learned. Active mastery ignores inactive IDs; local learner history is left untouched.
- **2 quick-card collisions reconciled:** 399 independent rapid cards remain; focus words are not double-counted in quick-card mode.
- **500 phrasal verbs retained:** 13 widely used foundational phrases (get up, wake up, turn on, etc.) annotated **B1 editorial/placement-first, not an independently verified CEFR level**. Remaining **487** retain provisional B2/C1 study labels. Prior user progress is preserved.
- `tools/build_fluency_focus.py` guards against overwriting editorially curated selections with old automatic lists. `tools/build_research_catalog.py` regenerated research-candidate lesson links.
- Data + test scripts are idempotent and fail closed for headwords not present in the existing licensed/attributed candidate sources.

## Example swaps
| Low-priority selection archived | Newly prioritized example | Why (qualitative) |
|---|---|---|
| humbug | doubt | Uncertainty in conversation |
| southward | struggle | Everyday problems |
| homeward | relief | Describing emotions |
| unmusically | superficial | Evaluating explanations |
| repertory | accustomed | Habits and adjustment |
| concerto | traumatic | Describing experiences |
| typhoid | approach | Discussing methods |
| pendulous | retention | Study and information |

Full 91-row rationale and copy: `sources/daily-spoken-swap-20261028.tsv` and `sources/daily-spoken-swap-stage2-20261028.tsv`. Current mapping: `qa/daily-spoken-curation-report.json`.

## Critical limitations and next editorial criteria
**No American conversational-frequency ranks were retrieved or verified in this pass.** The additions are editorially prioritized for usefulness, not demonstrated to be top-frequency words. In particular, a word's CEFR headword list is **not** evidence that the particular sense/example is at the same level or frequent. The 0 remaining general risk flags reflect only the initial *small* handcrafted concern list, not full screening clearance. All 1,000 word frequencies and 500 phrasal expression frequencies require verification.

Research targets for a future authorized/licensed comparison:
- SUBTLEX-US: https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus — US subtitle frequency and contextual diversity; word-form and lemma caveats.
- COCA (Spoken and TV/Movies): https://www.english-corpora.org/coca/help/texts.asp — spoken vs scripted conversational evidence and sense-aware comparisons.
- Phrasal verb **multiword expression** counts must not be inferred from component-word counts.
- Add CEFR *sense-level*, en-US naturalness, semantic accuracy and human editorial approval; exclude very basic already-known items through an initial placement diagnostic.
- Before selecting replacements, score: US conversational frequency; practical daily scenario reach; listening recognition; active speaking utility; B1 learner novelty; natural American examples; diversity/coverage. Do not promote merely because category says C1.

## QA results and release status
- **125/125 automated tests**: 46 JS + 79 Python.
- Focus totals/duplicates and archives verified, no approval flags automatically granted.
- `python tools/release_gate.py`: **EXIT 1 / LOCKED**. Human editorial review, source license audit, richer listening content, desktop/iPhone WebKit E2E and other release requirements remain unfinished.
- No Google Drive, GitHub upload, public ZIP, or deployment performed.
