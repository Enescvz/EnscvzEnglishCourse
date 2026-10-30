# American English Lab — VOA Listening transcript and assessment QA (28 October 2026)

## Verified project counts

- **50** unique official VOA source pages, all with in-app question sets; **204** original comprehension questions in total.
- **7** full publisher *Conversation* transcripts structured as speaker turns and displayed inside the application; **43** remaining recordings still link to the publisher for their audio and transcript.
- **268** total in-app transcript speaker turns across the 7 lessons; **32** questions in transcript lessons and **172** source-linked questions.
- Three newly integrated transcripts: `voa-2-04` (54 turns), `voa-2-05` (34 turns), `voa-2-06` (37 turns). Existing four transcript lessons and existing user-facing quiz IDs retained.
- **12** questions (in these three new transcripts) now include quote, speaker, and transcript-turn index for source-bound answer evidence.
- **30** Reading lessons (150 questions), **20** Grammar lessons unchanged; **1,000** focused vocabulary and **500** focused phrasal-verb learning-card drafts unchanged.

## Source pages and audio provenance

These are publisher-original, scripted **human-spoken** VOA Level 2 lessons. Conversation text was compared with the corresponding official pages. MP3 URLs are copied from each page's 128 kbps direct-link listing. A direct link does **not** establish actual-device playback or reliable downloading.

1. [Run Away With the Circus!](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-4-run-away-with-the-circus/4034187.html)
2. [Greatest Vacation of All Time](https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-5-greatest-vacation/4035571.html)
3. [Will It Float?](https://learningenglish.voanews.com/a/lesson-6-will-it-float/4064553.html)

All imported transcripts are **publisher-text checked**, but **NOT independently aligned with the audio** and **NOT timestamp synchronized**. Third-party inclusions require separate license review. This is not a certification of spelling, CEFR appropriateness, or independent language-editing quality.

## Learning accuracy and progress history

- Both listening pathways now require a user's explicit **I listened** confirmation before saving a completed listening quiz; there is no automatic verification of audio playback.
- `audioPlaybackSelfReported: true` and `audioPlaybackVerified: false` are stored explicitly. Older completions lacking self-report are labelled as unverified, not silently upgraded.
- After answering the 12 source-evidenced questions, users can see the supporting speaker turn in feedback. Raw answers/score alone must not be confused with verified listening fluency or CEFR level.
- Importer `tools/import_reviewed_voa_4_5_6.py` is idempotent, preserving lesson IDs and authored answer selections.

## QA, limitations and next work

- **49 JavaScript + 113 Python = 162 automated tests passed** on the latest development snapshot.
- Targeted virtual-origin Chromium UI passed for desktop (1280×850) and mobile viewport (390×844), including question evidence and self-report gates. **Not iPhone WebKit evidence.**
- Release check deliberately reports **LOCKED**: editorial approval, real-device audio testing, offline audio, and other quality gates remain incomplete.
- 43 publisher transcripts still need full import and answer-by-answer source verification; 172 source-linked question answers still only have generic publisher transcript references.
- External MP3 playback verified on physical device: **0**. Bundled licensed human MP3: **0**. Independently verified source-to-audio timing: **0**.
- 42 legacy **eSpeak** MP3s remain labelled as synthetic, not natural voices. Speaking was out of scope and untouched. No Google Drive or GitHub upload; no release package.
