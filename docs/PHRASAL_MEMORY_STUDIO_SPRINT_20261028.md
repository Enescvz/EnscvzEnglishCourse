# American English Lab — Contextual Phrasals & Memory Studio Sprint

Date: 2026-10-28. **PRIVATE DEVELOPMENT ONLY — DO NOT DEPLOY.**

## Verified advancement

- **112 original new contextual phrasal-verb lesson drafts** created with the batch authoring tool `tools/author_useful_phrasals_20261028.py`. Every entry has a Turkish sense, English explanation, two distinct original example sentences and a grammatical usage note. Re-running the tool does not duplicate entries. All `editorialStatus` fields remain `authored_unreviewed`.
- Focused contextual phrasal lessons **318 → 430 / 500**, with **70** source headwords remaining to be turned into contextual lessons. The source's CEFR categorization and frequency are **not independently verified**. Source headword license and provenance remain in `CONTENT_LICENSE.md`.
- Focused general word contextual drafts remain **422 / 1,000**: 500 B2 + 500 C1 user-selected targets. Specialist Accounting & Finance remains **284**. Separate bilingual-only rapid cards remain **852**.
- The Memory Coach now has a responsive **five-stage visual progress rail** (connect, listen, recall, understand context, use) with accessible current-step and progress semantics. Current step is never marked completed prematurely. FSRS algorithm and existing progress format remain unchanged.
- Service worker revision changed to `ael-dev-20261028-context-phrase-3` so the new data and UI can be refreshed in offline caches.

## Verification performed

- `npm run test:all`: **46 Node + 54 Python = 100 tests passed**.
- `python tools/audio_qa.py`: **42 synthetic MP3 container/timeline checks passed**. These are not licensed human recordings.
- `python tools/audit_examples.py`: JSON example check passed; **447 legacy lesson cards across all categories still need an independent second example**.
- `python tools/release_gate.py`: expected non-zero; **release remains LOCKED**. Manual American-English semantic / CEFR review and real iPhone Safari/WebKit acceptance still missing.
- `npm run qa:sandbox`: **desktop passed** but the full run **timed out after desktop**. Therefore the current change has **no confirmed mobile E2E pass**. A virtual Chromium viewport is never a physical iPhone test.

## Pending next steps

1. Review new 112 contextual phrasal lessons for meaning, American naturalness, grammar/syntax and which sense is taught. Do not auto-certify B2 levels.
2. Curate **70 remaining high-utility phrasal targets** carefully: avoid treating generic prepositional combinations (e.g. `go to`, `look at`) and rare entries as equally valuable everyday phrasal verbs. Candidate list is in `data/fluency-focus.json`.
3. Contextualize **578** focus words. Fix the 447 legacy short-example records, then expand audio/podcasts/listening and human-recording licensing.
4. Repeat mobile WebKit and desktop tests; maintain release lock. No Google Drive and **no GitHub deployment**.

No claim of fully completed application or C1 guarantee. A source headword is never an approved teaching card.
