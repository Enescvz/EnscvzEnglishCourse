# VOA L2 lessons 19–30 — 12-lesson publisher-source evidence batch

**PRIVATE DEVELOPMENT · DO NOT DEPLOY · Speaking unchanged · 28 Oct 2026**

## Scope and outcomes

A single batch of **12 official VOA Level 2 Conversation pages (Lessons 19–30)** was reviewed against the AEL-created multiple-choice questions. Four short publisher-source excerpts per lesson were saved, totaling **48 question-level source checks**. Each check records the speaker or explicit nonspoken stage direction, excerpt, official source URL and a *web-extraction line hint*; the hint is not a stable publisher paragraph number or sound time index. Answers/options, question counts, and lesson IDs were not changed. The app displays the source excerpt and direct VOA link when the student answers the question.

**Honest coverage:** 18 in-app full transcripts + 32 external source-linked pages (unchanged). 76 in-app speaker+turn-indexed checks + 48 new publisher page excerpt checks = **124/204** source-evidenced answers; **80 remain**. These are separate evidence levels; the 48 new excerpts must NOT be counted as 48 in-app speaker/turn verified questions or as transcripts imported. The original 204 questions are project-authored, not VOA exam-question copies. New excerpt references are manually reviewed, not independently source-crawled and machine-verified.

Official sources: 

| Level 2 | Source | Level 2 | Source |
|---|---|---|---|
| 19 | [Movie Night](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-19/4242927.html) | 25 | [Only Human](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-25/4322773.html) |
| 20 | [The Test Drive](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-20/4254704.html) | 26 | [Look-alikes](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-26/4350607.html) |
| 21 | [Trash to Treasure 1](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-21/4273059.html) | 27 | [Fish out of Water](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-27/4374632.html) |
| 22 | [Trash to Treasure 2](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-22/4283017.html) | 28 | [For the Birds](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-28/4396849.html) |
| 23 | [Rock Star](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-23/4287922.html) | 29 | [Where There's Smoke](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-29/4423736.html) |
| 24 | [I Feel Super](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-24/4307612.html) | 30 | [Dream a Little Dream](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-30/4465315.html) |

## Rights and evidence limits

[VOA's usage policy](https://learningenglish.voanews.com/p/6861.html) permits reuse of original VOA Learning English content with attribution. It does *not* cover material from third parties. Lesson 23 contains third-party commercial song lyrics; Lesson 30 includes song text. Neither was copied or bundled. In Lessons 19, 20, and 25, one question each is based on a written stage direction: **not spoken dialogue**, and explicitly labeled in the UI. These three can support *reading* verification but require independent audio-level check before any spoken-listening evidence claim.

No licensed local human-voice MP3s were created, and no real remote audio payload/playback, timestamp sync, iPhone Safari, low bandwidth, or offline test was certified. The publisher's audio is still opened on their website for these 12 entries. No score is marked as a verified listening session without the user's own checkbox, and that checkbox is explicitly a self-report, not technical playback validation.

## Engineering checks

- Before changes: **51 JS + 136 Python** tests passed.
- After changes: **51 JS + 141 Python** tests passed.
- Virtual Chromium (desktop 1280×850 + mobile 390×844) linked-lesson UI checks passed: proof snippet shown, stage direction labeled, VOA link accessible, no progress recorded without listening self-report, self-reported completion stores `audioPlaybackVerified:false`.
- Existing card and VOA IDs and all original question texts/options/answer indices preserved, verified by SHA-256 baseline from incoming backup.
- Source review data: `qa/source-reviews/voa-l2-19-30-evidence-20261028.json`; remaining 80-question action list: `qa/voa-question-review-queue.csv`.
- Release gate remains intentionally **LOCKED**. Next work: 20 Level 1 question-review sets, 32 full transcripts, human/audio/offline and TOEFL editorial QA.
