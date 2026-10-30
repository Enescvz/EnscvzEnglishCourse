# Real Voices — VOA Listening Pilot (28 October 2026)

## Deliverable in this development snapshot

Three directly sourced Voice of America (VOA Learning English) Level 2 dialogue lessons, **118 publisher-transcript speaker turns** and **16 new project-authored multiple-choice questions**. Existing eSpeak recordings are unchanged and are **not** endorsed as natural listening practice.

| ID | Lesson | Duration shown by VOA | Project questions | Original source |
|---|---|---:|---:|---|
| voa-level2-01-budget-cuts | Budget Cuts | 4:07 | 5 | https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson1/3960391.html |
| voa-level2-02-interview | The Interview | 4:05 | 6 | https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-2/3960471.html |
| voa-level2-10-peru | Visit to Peru | 3:57 | 5 | https://learningenglish.voanews.com/a/lets-learn-english-lesson-10-visit-to-peru/4079037.html |

**Important terminology:** Transcripts were **retrieved from the publisher's public-domain lesson pages** and structured by speaker, not auto-transcribed via ASR. They have not yet been acoustically checked or timestamp-aligned against the MP3. In particular, the lessons include scripted teaching segments from “Professor Bot”; they are human-spoken instructional dialogue, **not spontaneous unscripted interviews**.

## Rights / provenance

VOA states that original *VOA Learning English* texts and MP3s are public-domain for educational/commercial reuse with credit to `learningenglish.voanews.com`: https://learningenglish.voanews.com/p/6861.html . The corresponding VOA pages identify VOA as the audio source. Third-party news-agency audio, photos, illustrations and videos are **excluded** unless separately licensed.

**Alternative:** ELLLO https://elllo.org/ offers more natural, often spontaneous real-speaker conversation with transcripts and quizzes, but its audio is available for personal/educational classroom use with noncommercial restrictions. ELLLO content is **not** bundled in this pilot. Official policy: https://elllo.org/about/index.htm and https://www.elllo.org/english/Mixers/?D=A .

## Playback truth

- The JSON contains direct VOA audio MP3 URLs and source lesson pages.
- **All three recordings currently stream online; none was downloaded or bundled in this working environment.** The container has no public DNS; direct download failed.
- The source links were surfaced by the VOA audio player. Actual playback and synchronization remain unverified in a user's browser.
- The transcript is static and hidden before first listening; no invented timecodes or inaccurate segment seeking.
- Questions have four options and an authored explanation. Score goes into local browser progress (`authenticLessons`) and exportable JSON backup.
- No transcript-derived speech-recognition accuracy, native-speaker certification, CEFR qualification or human editorial signoff is claimed.
- To **optionally** fetch and bundle the original VOA MP3s when Internet access is available, run `python tools/download_voa_audio.py --download`. Successful downloads are SHA256 logged and only genuinely downloaded files are marked local/offline. Use `python tools/download_voa_audio.py` for a safe dry run. This has **not** been executed successfully here.

## Testing / release

- JavaScript syntax checked (`node --check js/app.js`).
- JSON/transcript/question/provenance/offline truth covered by `tests/test_voa_pilot.py`.
- Existing rapid deck showed 415 overlaps with completed lessons and 91 overlaps with archived lessons; reconciliation removed **506 duplicate quick-card display records**. Local student history and completed lesson cards were not modified. Remaining rapid quick cards: 399.
- `tools/rapid_gloss_import.py` fixed a preexisting JSON-only import test failure.
- Playwright desktop/mobile run attempted but Chromium navigation is blocked by the environment (`ERR_BLOCKED_BY_ADMINISTRATOR`); do **not** report a successful browser run.
- **Release gate must remain locked.** The three VOA sources do not substitute for previous requirements (licensed bundled human audio QA, editor signoff and verified iPhone WebKit E2E).

## Expansion policy

Before adding any new source audio: verify source ownership, reuse terms, stable MP3 URL, publisher transcript, speaker origin and educational suitability. Prefer naturally spoken en-US. Generate original comprehension, inference, vocabulary and focused dictation tasks **from the actual transcript**; validate answers and avoid fabricating timestamps. Introduce gradually less scripted listening after learner gains comprehension confidence. Never publish an incomplete bundle.
