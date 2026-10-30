# VOA Level 2 Lessons 13–14 — Publisher Conversation review (28 October 2026)

**Private development only; DO NOT DEPLOY. Speaking unchanged.**

## Actual implementation

- Official VOA Conversation sections imported for [Lesson 13: Save the Bees!](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-13-save-the-bees/4145716.html) and [Lesson 14: Made for Each Other](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-14-made-for-each-other/4159000.html). Publisher wordings were compared with the two published pages, not independently with audio. Non-spoken directions and typography are not timed captions. Original publisher typo in Lesson 13 closing line retained; not editorially corrected.
- Lesson 13: 26 conversation speaker turns, four source-evidenced quiz answers (smoker; egg-laying queen; nectar/pollen; native flowers).
- Lesson 14: 33 conversation speaker turns, four source-evidenced quiz answers (whistling; invented boyfriend; name; squirrel collection). The invented-boyfriend question is supported by dialogue describing an invented claim; this is a meaning-level conclusion, not a single verbatim explicit answer.
- Both original `voa-linked-2-13`/`voa-linked-2-14` IDs and question texts, options, answer indices, and order are unchanged; corresponding linked entries moved into the app-transcript collection with speaker/turn evidence indices. Frozen baseline in `sources/voa-linked-13-14-original-quiz-20261028.json` checks this.
- Publisher-listed 128 kbps MP3 links are online only; they are **not** downloaded, rehosted, replay-tested or audio-aligned. Source metadata explicitly sets `offlineReady=false`, `timingVerified=false`, `transcriptVerifiedAgainstAudio=false`. The listening self-report gate remains unchanged.
- New measured totals: 50 source IDs, 204 questions; **14** complete in-app publisher transcripts (60 of the 204 questions with source-turn evidence); **36** linked-only quizzes (144 remaining questions without turn-bound evidence).
- Importer `python3 tools/import_reviewed_voa_13_14.py` is idempotent and checks IDs/question count. Source and license: [VOA Request Our Content](https://learningenglish.voanews.com/p/6861.html); VOA-original educational text/MP3 may be reused with credit; third-party material excluded. No local MP3 bundled.

## QA and unresolved matters

- First baseline: Node 50 + Python 126 passed. After import and test expansion: Node 51 + Python 130 passed. Latest verified state is recorded in `qa/non-speaking-quality-report.json`.
- Virtual Chromium desktop and mobile assertions passed, but the process closure was not captured as a clean test-run exit; this is not release evidence.
- A genuine Chromium offline test was attempted against a local HTTP server and blocked by the sandbox (`net::ERR_BLOCKED_BY_ADMINISTRATOR`). **Offline QA NOT passed.** Browser automation can be rerun in an environment with localhost access using `python3 tests/e2e_offline_chromium.py`.
- A real iPhone Safari/WebKit and actual external MP3 playback on device remain untested, as do voice/transcript synchronization, source-level editorial signoff and US spoken-frequency evaluation.
- Next priority: 36 publisher-only transcripts, 144 linked questions; no fabricated audio verifications or editor signoffs; keep release gate LOCKED, no GitHub/Google Drive.
