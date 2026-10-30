# AEL — TOEFL-only 2026 Format Alignment · Private Development · 29 Oct 2026

**Private, NOT FOR DEPLOYMENT.** This sprint intentionally did not modify Speaking, VOA/Listening lessons, grammar, general reading, vocabulary, phrasal verb decks or FSRS logic. No Google Drive, GitHub, publication or release artifact.

## ETS reference and limits

- TOEFL iBT (after 21 Jan 2026): Reading approx. **50 items / 30 min**, Writing **12 items / 23 min**; task categories: Reading `Complete the Words`, `Read in Daily Life`, `Read an Academic Passage`, Writing `Build a Sentence`, `Write an Email`, `Write for an Academic Discussion`.
- ETS test specification Writing mix: **10 sentence building + 1 email + 1 academic discussion**. Sources:
  - https://www.ets.org/toefl/test-takers/ibt/about/content.html?version=after-jan-2026
  - https://www.eu.ets.org/pdfs/toefl/toefl-ibt-test-specifications-2026.pdf
- AEL questions are newly authored; no ETS-owned questions, score conversion, calibrated item-response model, or verified official feedback.

## Implemented

1. **Writing:** expanded from 20 to **28 original tasks**: 16 sentence-building, 6 emails, 6 discussions. Added 8 new, individually authored sentence-building exercises with exact reference answers and token bags. Retained old question IDs, task order and drafts. New timed Writing sessions use **10+1+1** over 23 minutes. Existing unfinished *version-1* **8+2+2** sessions remain recoverable, and old practice history still displays correct historical denominator; new sessions are version-2. No artificial grammar/meaning/ETS score is generated.
2. **Reading:** 50-item/30-min existing diagnostic and nine-item mini remain intact. Additionally added **16 typed word-completion items** using already authored `complete_words` question IDs, stems and reference keys. Their answer options are **not** displayed prior to typing; input is checked only after submission, with contextual explanation. Their learning records are distinctly labeled `original_typed_word_completion` and are not mixed into timed Reading weakness estimates. This is a dedicated vocabulary-in-context practice, **not** an official item or an assertion that the original multiple-choice diagnostic is form-equivalent to ETS.
3. **Offline cache:** cache version incremented to deliver the changed TOEFL source code, without introducing remote audio/recordings or changing any non-TOEFL feature.

## Verification and honest gaps

- Regression: **94 JavaScript + 180 Python = 274/274 pass**.
- Focused virtual-routed Chromium: **desktop and mobile pass** for typed completion and new Writing session/mix/draft persistence. Existing broader TOEFL Writing/Reading virtual Chromium: pass. A virtual test cannot verify actual browser-origin reload, Safari/WebKit, or real network-offline behavior.
- `release_gate.py` returns **LOCKED** as expected.
- Formal ETS adaptive algorithm, calibrated 1–6 scoring and subjective essay feedback remain **not available**; editorial signoff by an independent qualified human remains **pending**. TOEFL Listening intentionally unchanged, and Speaking untouched.
- Tests are synthetic/offline-safe; user-perceived language-learning gains are not measured in a longitudinal trial.

## Further TOEFL-only work

- Commission qualified US-English review of all TOEFL Reading/Writing tasks and distractors.
- Increase original graded Reading form bank before using repeated questions for diagnostic inference.
- Obtain legitimate scoring/assessment benchmark for open-ended writing; until then stay with explicit structure-only feedback.
- Benchmark against ETS TestReady without representing original AEL percentage as an ETS band.
