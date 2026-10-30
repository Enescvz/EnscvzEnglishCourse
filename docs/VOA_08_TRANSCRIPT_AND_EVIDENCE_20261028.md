# VOA 8th in-app transcript — partial source-verified development update (2026-10-28)

**PRIVATE DEVELOPMENT — DO NOT DEPLOY. Speaking unchanged.** This is an
incremental update to the VOA7 QA backup, not an independent language-editor
approval or a verified audio playback report.

## Publisher pages reviewed

- VOA Level 2 Lesson 7, **Tip Your Tour Guide**:
  https://learningenglish.voanews.com/a/lesson-7-tip-your-tour-guide/4064769.html
  — Conversation speaker lines compared with the publisher text. Review file:
  `sources/voa-reviewed-lesson-07-20261028.txt`. Original lesson/quiz ID
  `voa-linked-2-07` retained. The lesson uses VOA's published 128-kbps MP3 URL,
  but no device could actually play and verify this MP3 here. The final
  unlabelled teaching preposition table is not presented as spoken dialogue.
- VOA Level 2 Lesson 8, **The Best Barbecue**:
  https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-8-best-barbecue/4073994.html
  — Four answers compared with the official publisher Conversation; short,
  speaker-attributed excerpts attached. **Not imported**: the page did not
  provide a confirmed direct MP3 link for this workflow, so the user still
  opens it on the publisher site. No fake transcript turn indices.

VOA-original Learning English texts and MP3s are identified as public domain
with attribution, excluding third-party material:
https://learningenglish.voanews.com/p/6861.html
No third-party sound recording or external media has been copied. No new MP3
is bundled. Publisher transcript text and human-voice audio *alignment* is
unverified; no iPhone Safari or physical playback testing was performed.

## Changes and repeatability

- `tools/review_voa_07_08_20261028.py` is an idempotent source-evidence import.
  It refuses lost or duplicate lesson IDs, missing labels, shifted source URLs,
  invalid answer indices and missing exact quotes; rerun changes nothing.
- 7 → **8** publisher transcripts in-app, 43 → **42** linked-only sources.
  50 source pages and 204 original questions unchanged. 7th lesson adds
  **4** replik-indexed evidence annotations; 8th lesson adds **4** checked
  quotations without pretending those transcript turns exist locally.
- Source-bound questions: **16** local turn-indexed; **4** additional
  publisher-only quoted evidence; **184** other questions still lack
  exact speaker/quote grounding. Do not infer that the other answer keys have
  undergone this same level of revalidation.
- All old card IDs, learning records' schemas, vocabulary/phrasals, Reading,
  Grammar and local synthetic audio remain unmodified. User completion still
  requires a self-report and stores `audioPlaybackVerified:false`.
- `tools/stage_voa_transcripts.py` now accepts mixed speaker labels such as
  `Person 3` and `Anna & Penelope` while keeping extracted transcripts
  unapproved in staging. The container network could not connect to VOA;
  the 42 remaining published transcripts were **not fetched**.
- Run `npm run test:all` and `AEL_STATIC_HARNESS=1 python3 tests/e2e_non_speaking_sprint.py`.
  Virtual Chromium does not establish real-device WebKit or remote audio QA.

## Unfinished publication blockers

Import and publisher-compare the remaining **42** transcripts, attach
source-turn evidence to the remaining **184** questions, validate any disputed
answers, do physical iPhone Safari MP3 checks, independently verify natural
voice content and offline behavior, complete semantic/US-spoken frequency
review with appropriate data licenses. Release gate must remain **LOCKED**;
never upload or publish until the project is complete.

## Latest test record

`npm run test:all`: 49/49 JavaScript and 121/121 Python passed.
Targeted virtual-origin Chromium desktop (1280×850) and mobile (390×844):
passed. `python tools/release_gate.py` intentionally exits nonzero, LOCKED.
A separate whole-audio quality command was started but the final aggregate
command timed out before it completed: **do not record an audio-quality PASS**.
See `qa/voa08-dev-verification-20261028.json` for exact measured scope.
