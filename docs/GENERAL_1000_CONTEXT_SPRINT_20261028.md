# American English Lab — 1,000 context-draft general vocabulary milestone

**28 October 2026 — PRIVATE DEVELOPMENT ONLY, NOT RELEASE READY.**

## Actual changes in this sprint

- Added **238** general vocabulary draft lessons to `data/vocabulary.json`: **183 B2 + 55 C1** selected from the already-existing focused 1,000-word list. The previous checkpoint contained 762 drafts.
- Each of these 238 cards now has a source-based Turkish gloss, an English description, **two independently written distinct contextual example sentences**, and an own-sentence prompt. The examples are original project copy, **not quotations from external dictionaries**.
- The source English/Turkish bilingual glosses were already staged locally, and all 238 headwords are present in the existing CEFR source candidate catalog. **This proves the headwords were sourced, not that any particular definition/sense is officially graded B2/C1.**
- Removed 238 display duplicates from `data/rapid-vocabulary.json` (639 -> **401**), without rewriting localStorage or upgrading recognition scores into productive-speaking mastery.
- Regenerated `data/fluency-focus.json`: **500 B2 + 500 C1, all 1,000 at `context_draft`**, and **500 phrasal verbs at `context_draft`**. `editorialApproved` and per-card review flags remain false.
- Created `tools/author_final_focus_words_20261028.py` (source guards + idempotent application) and `tests/test_final_focus_words_20261028.py`, and bumped the service-worker cache revision.
- A separately recorded `qa/daily-use-selection-review-20261028.json` flags unusual, archaic, region-specific and low-conversation-value items for replacement consideration. The 1,000 list is **not yet demonstrably the 1,000 most useful words in spoken American English**.

## Checks

- `npm run test:all`: **46 Node tests + 72 Python tests = 118 passed**.
- Re-running the new authoring script returned `validatedNewCards: 0` (`already_applied`) — no duplicate cards.
- `python tools/audit_examples.py`: **1,000 general and 500 phrasal cards with two distinct examples**. **232 finance/accounting terms still require a second example**.
- `python tools/release_gate.py`: exit 1, **LOCKED**. Editorial verification, licensed human audio, more podcast/drill/reading/grammar content, and actual WebKit/iPhone test evidence are not complete.
- No GitHub or Google Drive usage, no site deployment or publication artifact.

## Real content numbers

| Category | Count |
|---|---:|
| Focused B2 context drafts | 500 |
| Focused C1 context drafts | 500 |
| Focused phrasal context drafts | 500 |
| Extra finance/accounting terms | 284 |
| Non-focused bilingual rapid vocabulary | 401 |
| Podcasts | 18 |
| Listening drills | 24 |
| Readings | 8 |
| Grammar lessons | 10 |
| Bundled synthetic audio | 42 |
| Licensed, credited human recordings | 0 |

## Editorial and app-quality limitations

1. The C1 source includes unusual adverbs and specialist words (e.g. **unmusically, fiendishly, raunchily**) and nonstandard or regional spelling (e.g. **verandah, mark-up**). These are **not endorsed as daily-essential**. Replace or demote after human/corpus review without erasing student history.
2. Sentence structure and sound naturalness still need independent American English native/professional editorial review. Automated structural checks do **not** demonstrate natural usage in actual speech.
3. TTS listening drills are useful for decoding individual words but do not substitute for human spoken connected-speech training.
4. Actual iPhone Safari, desktop browser E2E and release-license checks remain necessary.

**Next steps:** improve the 1,000-word selection for real daily-use frequency and US orthography; fill 232 second examples in Finance; expand genuinely natural Listening and Speaking practice; obtain real device/browser evidence; do not publish until every release gate passes.
