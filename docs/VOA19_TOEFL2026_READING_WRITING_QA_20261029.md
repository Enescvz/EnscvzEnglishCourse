# AEL — VOA19 + TOEFL 2026 Reading/Writing, private QA checkpoint (29 October 2026)

**PRIVATE DEVELOPMENT — DO NOT DEPLOY. Speaking is strictly out of scope.**

## Reviewed, implemented changes

1. Reused existing VOA Level 2 Lesson 19 ID `voa-linked-2-19` and moved that lesson from the publisher-linked list to the in-app publisher transcript list without creating a new progress ID. Imported the VOA-published *Conversation* transcript, preserving speakers and clearly labeling stage directions. The 4 original questions and answer indices were preserved. Evidence is linked to 3 spoken turns and 1 stage direction, not 4 spoken turns. Official online MP3 URL is a reference only, **not** a verified playable recording. No MP3 was downloaded or bundled. Reviewed source: https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-19/4226815.html. Rights overview: https://learningenglish.voanews.com/p/6861.html; any third-party items must be excluded or licensed independently.
2. Added 6 **original, unofficial** 2026 TOEFL-style Reading exercises: 2 Complete the Words, 2 Read in Daily Life, 2 Read an Academic Passage (14 questions). Existing original Reading courses remain unchanged: 30 lessons / 150 questions. The new exercises use existing progress storage with distinct `tr26-` IDs.
3. Added 9 **original, unofficial** 2026 TOEFL-style Writing exercises: 3 Build a Sentence, 3 Write an Email, 3 Write for an Academic Discussion. Stored as separate `toefl:` task keys in existing local writing progress. Only Build a Sentence checks against a prepared exact reference; free writing receives no automatic language-quality score or fabricated ETS score. All responses can be saved and retained via the app's existing export mechanism.
4. Added source-evidence UI labeling that differentiates publisher speech from printed stage directions. Added service-worker app-shell paths for Reading/Writing scripts and data (offline cache *configuration only*).
5. Kept all 50 original VOA lesson IDs, 204 original quiz question/option/answer identities, 400/75 TOEFL shared core, 1,000 general word and 500 phrasal drafts, and all existing progress keys.

## Measured current state

| Measure | Value | Qualification |
| --- | ---: | --- |
| In-app publisher VOA transcripts | 19 / 50 | Official text checked; **not** transcript-vs-playback validated |
| Publisher-linked, no full in-app transcript | 31 / 50 | Publisher pages contain transcripts and audio links |
| VOA source-text-evidenced questions | 204 / 204 | 79 spoken in-app turn + 1 scene direction + 124 short publisher excerpt |
| New reading practice tasks | 6 | 14 new, author-created questions; no official ETS source |
| New writing practice tasks | 9 | 3 categories, 3 tasks each; no score claims |
| Existing Reading / Grammar | 30 / 20 lessons | Existing 150 Reading questions preserved |
| Existing TOEFL shared vocabulary | 400 words + 75 phrasals | Editorial/frequency review pending |
| Local licensed human-voice MP3 | 0 | Existing 42 synthetic eSpeak items remain unapproved |
| Actual iPhone Safari/audio playback QA | 0 | No physical device access |

## QA evidence, including limitations

- Automated suite: **55 JS + 158 Python = 213 passing**. Includes old ID/answer fingerprint regression, VOA19 source-turn checks, importer idempotence, unofficial content type/ID tests and service worker path checks.
- Targeted virtual Chromium desktop/mobile UI smoke: passed; report at `qa/toefl-2026-browser-smoke.json`. **This is virtual asset interception, not a real HTTP or offline pass and not Apple WebKit.** An older full-browser runner produced desktop/mobile PASS assertions but did not exit cleanly, so this is *not* a complete clean E2E.
- Real local HTTP + Chromium offline E2E: **BLOCKED/FAILED** by `net::ERR_BLOCKED_BY_ADMINISTRATOR` on `127.0.0.1` in the execution environment. Report at `qa/real-offline-chromium-report.json`. Merely adding items to the service worker precache does **not** validate offline behavior.
- Real iPhone Safari, remote VOA MP3 playback, text/audio timeline alignment, non-native accent and phonetic review: **NOT TESTED**.
- Manual American-English language-editor approval, TOEFL exam frequency ranking and Listening/Reading/Writing curricular approval: **NOT SIGNED OFF**.
- Release gate: **LOCKED**. The existing gate continues to reject release; do not run deployment, GitHub upload, Google Drive transfer or a public-release ZIP.

## Next strictly required work

1. Source-review and integrate full publisher transcripts for the remaining 31 VOA lessons, excluding third-party copyright material. Do not confuse source excerpts on 204 questions with 50 complete transcripts.
2. Use a permitted physical iPhone Safari/device to test playback controls, network failures, transcripts, quiz listening self-report, screenreader and browser storage. Do not mark as passed without device evidence.
3. Run real-origin HTTPS/offline E2E on a usable network. Verify service-worker caches, cold/return visits, airplane-mode app shell, graceful remote audio failures and preserved progress.
4. Independently edit vocabulary, phrasal, reading, writing and claimed TOEFL relevance. 2026 formats were consulted, not official ETS question banks.
5. Preserve Speaking, ID mapping and learning history; re-run all tests and keep LOCKED until gates have evidence.
