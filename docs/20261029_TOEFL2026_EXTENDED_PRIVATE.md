# AEL — TOEFL 2026 Extended Private Development / 29 Oct 2026

**PRIVATE DEV ONLY — DO NOT DEPLOY OR UPLOAD TO GITHUB. Release gate LOCKED.**

## Verified additions

- Expanded existing original Reading collection from 12 tasks / 34 questions to **18 tasks / 50 questions** (16 newly authored questions). Three current ETS Reading task categories are represented, but items are **AEL-authored multiple-choice approximations, not ETS adaptive items**. A 30-minute timed practice uses the full 50 question set; previous 34-question unfinished sessions can still be resumed against retained IDs.
- Expanded existing original Writing from 18 to **20 tasks**, including 8 Build a Sentence tasks. Added a **12-task, 23-minute practice** (8 sentences, 2 emails, 2 discussions), with autosaved local drafts, resuming an interrupted session, wall-clock timeout, and feedback only after submission. **This mix is an AEL rehearsal, not an ETS item allocation.** Sentence reference matching is not an essay score; open tasks receive structural observations only.
- Added links from TOEFL study center to official ETS sample and ETS TestReady/preparation, which open independently with internet. ETS-owned assessment is not embedded, copied or automatically scored as AEL progress.
- Updated service-worker core manifest version to include the newly imported Writing practice module, maintaining offline bundle integrity.
- Explicitly verified unchanged original vocabulary, phrasals, TOEFL 400/75 card ID selection, VOA 50/204 content, Speaking function and related sources.

## Tested

- `npm test`: **76/76 PASS**.
- `python3 -m unittest discover -s tests -p 'test_*.py'`: **164/164 PASS**.
- Focused Chromium virtual-asset smoke: **desktop and mobile PASS**.
- Prior broad Chromium suite: **TIMEOUT** in this environment, *not counted as pass*.
- `python tools/release_gate.py`: **LOCKED** (expected, nonzero exit).

## Open and not misrepresented

- No ETS-linked, calibrated 1–6 score or true multistage adaptive algorithm. 50 AEL Reading questions do **not** constitute an official full-length practice test.
- No real, verified, licensed human audio for 8 TOEFL script-only Listening scenarios; those cannot be counted as Listening performance. For official sample audio, use ETS external resource.
- Writing AI/human content assessment and original task allocation calibration absent; structural checklist does not establish grammar, meaning or exam score.
- No physical iPhone Safari/WebKit end-to-end or live-origin offline verification; virtual Chromium UI isn't equivalent.
- Independent English language/editorial review pending for all modified and prior items, plus 400/75 selected cards.
- 31 VOA in-app transcripts still pending (separate Listening content backlog).
- Speaking untouched by request, therefore its TOEFL readiness not evaluated.

## Next verification before release

1. Obtain rights-cleared natural recordings and check all four Listening task types on a physical iPhone.
2. Run an independent US-English editorial review using `qa/toefl-2026-extended-editorial-queue.csv`.
3. Test on a physical iPhone Safari using HTTPS install plus airplane mode; inspect cache readiness and draft persistence.
4. Use ETS official practice to benchmark skill, not AEL's uncalibrated percentages.

Source: https://www.ets.org/toefl/test-takers/ibt/about/content.html?version=after-jan-2026
