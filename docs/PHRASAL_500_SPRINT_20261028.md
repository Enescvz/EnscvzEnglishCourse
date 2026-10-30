# American English Lab — 500 conversational phrasal drafts milestone

**28 October 2026 — private development checkpoint, DO NOT DEPLOY.**

## User-approved curriculum

- **General vocabulary:** 500 B2 + 500 C1 targets. **422** selected words have contextual lesson drafts, **451** focus targets have Turkish gloss-only drafts, and **127** focus targets have only source headwords. Still **578** general contextual drafts to author. No claim that this is a quantitatively validated American spoken-frequency top-1,000 list.
- **Phrasal verbs:** **500 distinct contextual lesson drafts out of 500 selected targets**, each containing a Turkish meaning, an original English definition, two distinct example sentences, a syntax note, and at least one meaning/sense record. **Zero** independent editorial approvals; CEFR-sense estimates are provisional.
- **Extra specialist material:** 284 accounting/finance entries; 852 distinct bilingual rapid cards outside the contextual general course. Rapid cards are not independently mastered lessons.

## What actually changed in this sprint

1. `tools/author_final_phrasal_focus_20261028.py` contains **70 original, source-grounded, conversational phrasal drafts**. The older focus list's bottom 70 included infrequent or basic verb+preposition expressions (e.g. *belly out*, *go to*, *look at*). A curated priority set replaced these; existing 430 authored cards were preserved without changing IDs. No external definitions or example sentences were copied from the CC BY-NC source.
2. `tools/build_fluency_focus.py` now selects these 70 last-mile phrases before the alphabetical and common-verb fallbacks. After promotion it reports exactly **500 `context_draft`** phrasals, **zero `headword_only`** phrasals and still **1,000 selected general word targets**.
3. `tools/complete_legacy_phrasal_examples_20261028.py` supplied **33 original second-sentence examples** missing from old phrasal lessons; none of the 500 phrasal lessons remains with fewer than two distinct examples. Source files and IDs were preserved. Both tools can be rerun with no duplicates.
4. `sources/phrasal-candidates.json` and `data/candidate-catalog.json` were refreshed. The original headword catalog contains **1,204** source expressions, 424 of which overlap teaching drafts; the remaining are unverified source candidates, **not** lesson content.
5. `sw.js` development cache version bumped. Tests were extended in `tests/test_final_phrasal_focus.py` and existing tests updated to the new legitimate **500-context** milestone without weakening the release gate.

## Verified tests, limitations, and release lock

- `npm run test:all`: **46 Node + 58 Python = 104/104 passed.**
- `python tools/audio_qa.py`: 42 bundled **synthetic**, not human, MP3 timing/container checks passed.
- `python tools/audit_examples.py`: 500 phrasal entries all have two examples; across **all** general + finance/accounting lessons **414 still need second examples** (182 general, 232 specialist). This is a structural audit only; no independent semantic review was performed.
- `AEL_STATIC_HARNESS=1 python tests/e2e_playwright.py` emitted `PASS desktop` and `PASS mobile` using **virtual-origin Chromium + simulated mobile viewport**. The runner timed out while shutting down; don't count it as a clean end-to-end process exit. **Real iPhone Safari/WebKit not tested**.
- `python tools/release_gate.py`: **expected nonzero result: LOCKED**. No editorial signoff, no US meaning/CEFR validation, no independently licensed human narration, and the general vocabulary, listening/podcast/reading/grammar quotas remain incomplete.

## Recommended next development sprint

Prioritize **182 existing contextual general words with only one example** before describing the entire general course as uniformly two-context; then convert **451 gloss-only** and **127 headword-only** focus vocabulary items into individually meaningful contextual drafts, preserving correct American senses and accurate CEFR evidence. Continue listening/speaking exercises linked to learned words. Do not fabricate native-speaker validation. Never upload incomplete code to GitHub or Google Drive, and never generate or present a publication ZIP. A separately labeled private development handoff archive is permissible.
