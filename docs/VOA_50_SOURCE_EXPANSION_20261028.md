# VOA 50 — authentic American English listening expansion (28 October 2026)

## What is actually done

**50 real VOA Learning English course URLs were inspected via the official series indexes:**
30 *Let’s Learn English Level 2* lessons and 20 later *Level 1* lessons (numbers 33–52).
The app now has a filterable, searchable, paginated list of those 50 publisher-linked sources.
They contain human-spoken scripted American English and a publisher-supplied conversation transcript on the official lesson pages.

**Only 3 of those 50 have full transcripts and 16 original multiple-choice questions imported into the application.**
The other 47 entries are source links for the learner to listen to on VOA and read the publisher transcript. The 47 are NOT represented as complete interactive lessons.

| Dimension | Confirmed current state |
|---|---:|
| Official VOA lesson pages | 50 |
| Intermediate Level 2 | 30 |
| Level 1 later-course warm-ups | 20 |
| Full in-app transcripts + original quizzes | 3 |
| Publisher-hosted sources still to import | 47 |
| Quizzes attached to the 47 source-only items | 0 |
| Downloaded original human MP3 | 0 |
| Independent device audio playback proof | None |

## Source and licence

- Official Level 2 index: https://learningenglish.voanews.com/p/6765.html
- Official Level 1 index: https://learningenglish.voanews.com/p/5644.html
- VOA reuse terms: https://learningenglish.voanews.com/p/6861.html
- Individual source URLs: `qa/voa-50-source-links.csv` and `data/voa-source-catalog.json`.
- VOA-produced Learning English text and MP3 are generally public domain, VOA attribution required. Some individual pages include third-party music/images/other material which are **not** automatically included in this permission (e.g. Level 1 Lesson 45 includes a song quotation). Only external links are provided for unreviewed lessons; importing and redistributing any audio requires a source-level rights audit.

## Status and honest limitations

- Level 2 is called *intermediate* by the publisher; the app's B1–B2 approximate tag is pedagogical only, **not** an official CEFR label.
- The 20 Level 1 lessons are tagged *easy practice* rather than claiming to be B2/C1. They should remain optional warm-ups for a B1 learner.
- Scripted instructional dialogue is clear human speech, but does not replace unscripted conversations with natural overlap, reduction, background noise or fast exchanges.
- No new MP3 has been downloaded. Third-party streaming and in-browser playback were **not tested in a real iPhone Safari device**.
- The 47 future transcripts, questions, explanations, timing and listening QA remain outstanding. No automatic question is generated from a title or a source synopsis.
- The 42 old synthetic audio files remain separate and are not mislabeled as natural human speech.

## Bulk import mechanism

`python tools/stage_voa_transcripts.py` prints a dry-run; `python tools/stage_voa_transcripts.py --fetch` attempts to download the other 47 official HTML pages and extract speaker-labelled text plus candidate MP3 URLs **into a review-only staging file**. Network is not available in this execution environment, so the real extraction was **not run**. Parser tests on synthetic HTML fixtures passed. No staging data automatically counts as verified transcript or question.

## Next quality stages

1. Download and validate complete transcripts from 47 official sources in an internet-enabled environment, checking especially dialogues without a direct MP3 and third-party music.
2. Review speaker turns, verify audio matching, build **original** 4–6 comprehension questions per lesson with traceable answer evidence.
3. Integrate approved quizzes into `data/authentic-listening.json` and migrate source entries from source-only to interactive one by one.
4. Test audio loading, mobile iOS Safari, pause/seek, transcript hide/reveal, scoring, progress and accessibility.
5. Complement scripted VOA dialogue with permission-cleared unscripted American speech. Keep release locked until all existing QA criteria are met.

**Not a release artifact. No Google Drive or GitHub publication.**
