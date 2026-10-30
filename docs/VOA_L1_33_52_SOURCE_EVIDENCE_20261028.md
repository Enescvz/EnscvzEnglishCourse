# American English Lab — VOA L1 Lessons 33–52: 80 question evidence sprint

**Date:** 2026-10-28 · **Status:** private development only / NOT APPROVED FOR RELEASE.

## What was actually changed

- Continued from the private VOA L2 Lessons 19–30 backup, not a new project.
- Opened and reviewed each **official VOA Learning English Level 1 Conversation page** for lessons 33–52. Source URLs are in `data/voa-source-quizzes.json` and in the 80-item evidence record.
- Added **80** distinct originally authored question evidence citations: short literal publisher excerpt, speaker, page URL, inspection-line locator and review status. No fabricated local transcript turn index was introduced for external-only lessons. 3 editorial clarification caveats flag nuanced contexts (L40, L42, L52).
- Final text-source audit: **204 of 204 questions have evidence**: **76** on imported transcript turns; **128** from 32 publisher-linked lessons. No unreviewed question remains in that *source-text-only* queue.
- Kept **18** fully imported transcripts and **32** external-only. Did **not** import 20 complete transcripts or download 20 voice recordings in this sprint.
- Restored compatibility of historical Level 2 Lessons 7–8 tests/importer with latest data so previous lessons cannot be demoted, and fixed the no-pending-rows empty CSV audit bug.
- Added UI after-answer contextual notes without changing a single question, option, answer index, card ID or progress key.
- Excluded Level 1 Lesson 45 *This Land Is Your Land* (Woody Guthrie) third-party song lyrics from imported source evidence. The publisher's own dialogue is the cited source. Separate third-party rights review remains necessary for any later full-transcript import.

## Grounding and attribution

Official publisher content reviewed: VOA Learning English, *Let's Learn English* Level 1 lessons 33–52, at the specific `sourceUrl` values in the JSON. Official usage policy: https://learningenglish.voanews.com/p/6861.html (VOA-original text and audio public domain with credit; news-agency/third-party material excluded). Quiz questions are independently authored and are **not** copies of the VOA quizzes.

**Important limitations:** A line locator comes from the web-rendered published Conversation page on this date; it is **not** a stable paragraph ID, phoneme interval, verified audio segment or in-app full transcript turn. Source evidence supports answer text only. For the 20 new lessons, the source quotation was compared with the relevant question and the answer, but there is no external independent editor signoff or complete distractor accuracy certification. *Lesson 42 nuance:* Anna describes a person stepping on her arm while the ending reveals a vending machine incident; the question intentionally asks what she says, and the answer feedback warns of the story twist. *Lesson 52 nuance:* the omitted genre is inferred from an exhaustive same-line listing.

## Tests and blocks

New tests: `tests/test_reviewed_voa_l1_33_52.py`, existing Python QA queue regressions, historical 07–08 importer safe no-op. JavaScript and Python test suite must pass after changes. Virtual Chromium desktop/mobile UI QA checks source links, source evidence visibility and listening self-report gate; no physical iPhone Safari. Local HTTP offline smoke remains **blocked by environment `net::ERR_BLOCKED_BY_ADMINISTRATOR`**, not approved. Publisher MP3 playback, transcript-to-audio alignment and human editorial approval are **not verified**. Forty-two local eSpeak recordings remain synthetic and unapproved as natural speech. The release gate remains **LOCKED**.

## Next scoped work

Import 32 remaining source Conversation transcripts in checked batches, excluding songs/third-party material; test legitimate MP3 playback on a physical iPhone and real offline behavior; finish independent corpus-frequency and lesson-editorial review and non-Speaking TOEFL Reading/Writing content. Preserve all existing IDs, user progress and release lock. Do not touch Speaking, use Google Drive/GitHub or produce deployment artifacts.
