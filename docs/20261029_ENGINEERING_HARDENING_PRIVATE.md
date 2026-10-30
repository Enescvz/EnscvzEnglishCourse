# American English Lab — 29 October 2026 engineering hardening (PRIVATE)

**Release remains LOCKED.** This sprint improves engineering safeguards but does **not** claim 9/10 release readiness, Apple Safari/iPhone approval, ETS-aligned scoring, independent content approval or verified human audio playback.

## Implemented and tested

1. **Non-destructive learning-backup import:** `js/progress-safety.js` validates the backup format, conservatively merges existing and imported progress by original card/lesson ID, preserves the newer FSRS review state (`last` timestamp), avoids duplicate imported event history while retaining multiple identical local records, never erases current unknown legacy fields, and refuses malformed/prototype-polluting payloads. Settings now explicitly say imports **merge**, rather than overwrite. `js/app.js` writes to browser storage before changing live in-memory progress; import failures leave the existing state untouched. **Important:** this does not replace external/exported backups or guarantee Safari storage permanence.
2. **Offline Safari robustness:** service-worker revision bumped to `ael-dev-20261029-engineering-hardening-v2`, newly added JS included in the required offline cache. The Settings panel displays available browser-storage estimates and warns that Safari may evict content and progress. Existing repair and cache-status mechanism remains. No human-voice VOA audio is mislabeled as offline; synthetic eSpeak files remain unapproved.
3. **Lesson 22 official VOA original conversation:** level 2 `Trash to Treasure, Part 2` complete publisher conversation added under the **existing** lesson ID `voa-linked-2-22`. All four existing question IDs/options/answers preserved, with source speaker/turn evidence. Official publisher MP3 is **linked only** and has **not** been played/quality-checked or bundled. Third-party song lyrics and agency material were not included.
4. **Repeatable QA:** 87 JS tests and 171 Python tests pass. A targeted Chromium virtual-browser test passes desktop and mobile for the existing memory coach and for JSON import. Independent structural release audit checks VOA 50/204 and TOEFL 400/75/50/20 invariants and flags outstanding work instead of substituting green checks for human approval.
5. **Real offline boundary test:** real localhost Chromium/Service Worker execution was attempted, but `net::ERR_BLOCKED_BY_ADMINISTRATOR` prevented the test. This is a **blocked** test, not a pass. WebKit binary and physical iPhone are unavailable in this environment.

## Latest verified scope

| Capability | Verified evidence | Remaining restriction |
|---|---|---|
| VOA lessons | 22 in-app full source conversations; 28 external pages; 204 questions preserve source evidence | 28 transcripts still not in app, source-to-audio timing not independently verified |
| TOEFL + Daily | 400 selected words and 75 selected phrasals; 50 original Reading questions, 20 Writing tasks, 8 transcript-only Listening scenarios | No independent editor, no authentic TOEFL listening sound on 8 scripts, no ETS calibrated adaptive score |
| Memory coach | 1,550 context card pool, FSRS review code regression passes, backup merge tested | No seven- or thirty-day learning outcome study |
| iPhone Safari offline | code and SW simulated tests pass; storage health visible | No physical iOS test, no HTTP browser end-to-end confirmation |
| Speech | **unchanged** | Untested existing module — outside scope |

## Pending 9/10 blockers

- Real iPhone Safari: install, airplane mode, offline reload, persistent progress and cache-eviction scenarios.
- Publisher-human audio: physical playback, source/license per recording and transcript timing QA; 0 bundled approved human MP3, 42 unapproved synthetic MP3.
- 28 remaining full VOA conversations, third-party rights filtering.
- Independent native-language US English editor signoff, especially all 475 TOEFL-highlighted items and example/distractor quality.
- ETS-level adaptive/exam calibration unavailable; AEL tests must remain explicitly unofficial.
- Longitudinal user learning measurement and full WebKit smoke.

## Source references

- ETS 2026 test content: https://www.ets.org/toefl/test-takers/ibt/about/content.html?version=after-jan-2026
- VOA public-domain and exceptions: https://learningenglish.voanews.com/p/6861.html
- Lesson 22 publisher Conversation: https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-22/4283017.html

All changes are private development only. No GitHub, Google Drive, publication or Speaking changes.
