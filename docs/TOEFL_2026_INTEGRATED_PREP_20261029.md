# TOEFL 2026 + Daily English — integrated private development sprint

**DO NOT DEPLOY.** Existing ZIP was opened; tests were run before changes. No Google Drive, GitHub, release or deployment.

## Official format reference

ETS 2026 test structure: <https://www.ets.org/toefl/test-takers/ibt/about/content.html?version=after-jan-2026>. Reading: Complete the Words, Read in Daily Life, Read an Academic Passage. Listening: Listen and Choose a Response, Conversation, Announcement, Academic Talk. Writing: Build a Sentence, Write an Email, Academic Discussion. The actual TOEFL also includes Speaking; **not modified by this sprint**.

## Features implemented

- Added 6 original Reading tasks (+20 questions) to existing 6: **12 tasks, 34 questions**. Original IDs unchanged.
- Added 9 original Writing tasks to existing 9: **18 tasks**. Original drafts remain under `P.writing['toefl:'+task.id]`.
- Added 8 original **transcript study** listening scenarios (+14 questions), covering four official categories. **NO RECORDED AUDIO**, do not claim Listening completion or improvement from text-only exercises. Prefer source-linked real VOA for audio, still not independently device-verified.
- Added `TOEFL + Daily` navigation and home entry point; joint core 400 words/75 phrasals remains linked to existing IDs and FSRS/memory records.
- Original 9-item/12-minute Reading mini test with all three task categories, concealed answer/explanation until submission, auto-submit on time expiry, wall-clock timer, attempt history in `P.toeflAttempts` and weakest observed Reading skill advice. **No ETS calibration, adaptive algorithm, 1–6 score prediction or full mock claim.**
- Writing feedback is *non-evaluative*: word count, exact answer for Build a Sentence; structural suggestions for email/discussion. No automated grammar accuracy, reasoning correctness or essay grading. A manual language editor is still required.
- PWA core cache updated to include the two new assets. **This is not an actual offline test.** Remote VOA MP3 cannot be assumed cached or licensed to bundle.

## Verification and known gaps

See `qa/toefl-2026-integrated-prep-report.json` and `qa/toefl-prep-browser-smoke.json` for exact scope. Automated tests and virtual Chromium are **not** physical Safari, audio playback, source/auditory transcript match, genuine offline origin or editorial signoff.

The remaining 31 VOA full transcriptions, 42 synthetic/robotic legacy MP3 review, licensed/verified human Listening audio, formal adaptive mock and score calibration are pending. Speaking unchanged. Release gate **LOCKED**.
