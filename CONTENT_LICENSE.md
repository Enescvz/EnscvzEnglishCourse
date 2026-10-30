# Educational text content license

Original example sentences, dialogue scripts, podcast transcripts, reading passages,
Turkish glosses and lesson explanations in this repository are licensed under
Creative Commons Attribution 4.0 International (CC BY 4.0).

https://creativecommons.org/licenses/by/4.0/

This does not license the Oxford / Cambridge / Merriam-Webster / VOA material
linked as references. Linked external works remain under their own conditions.

Sound recordings bundled under `assets/audio/` were synthesized by the project
authoring workflow using eSpeak and are clearly marked as synthesized, not human voice.

## Optional bulk curriculum staging (NOT distributed as vetted lessons)

The importer at `tools/bulk_curriculum.py` supports external **B2/C1 candidate** sources:

- CEFR-J (B2) and Octanove (C1) as repackaged by [EnglishPractice](https://github.com/recepyagmur/EnglishPractice). **Different rights apply:** the CEFR-J Wordlist v1.5 (Tono Laboratory, TUFS) permits research/commercial use with proper citation; it is **not automatically CC BY-SA**. The Octanove C1/C2 profile is CC BY-SA 4.0. Its repository's MIT *code* license does not supersede either data license.
- [Vocab Bloom Hub English 0.2.0](https://huggingface.co/datasets/Fristail27/vocab-bloom-hub-en), CC BY 4.0. **AI-generated, not human-verified.** Keep clear visible AI-generated notices and attribution with any redistributed derived content; independent review is mandatory for language teaching.

These are development references, NOT an assertion that they are included, downloaded, independently verified, or endorsed by the original producers. The import script only writes quarantined candidate JSON and audit metadata. Original repo learning content retains the CC BY 4.0 license above; imported data must retain its own upstream conditions and attribution.

## Rapid bilingual glossary (development-only)

`data/rapid-vocabulary.json` is derived from locally transcribed bilingual
headwords/glosses in the public `recepyagmur/EnglishPractice` B2/C1 lexicon,
cross-matched against the project's CEFR-J/Octanove source-level candidates.
Repo: https://github.com/recepyagmur/EnglishPractice (source code MIT LICENSE).
Permission for upstream translations and underlying vocabulary sources should
be verified independently. **Do not treat the parent repository's MIT code
license as proof all third-party wordlist and translation rights are MIT.**
They remain strictly unreviewed quick study aids pending clearance.

## TOEFL + Daily English shared starter (private development)

`data/toefl-academic.json` contains 50 original English definitions, Turkish glosses, and two authored sentences per word. AWL Sublist 1 headwords were selected with attribution to [EAPFoundation](https://www.eapfoundation.com/vocab/academic/awllists/index.php), whose educational non-commercial reuse conditions require attribution; no proprietary example passages or dictionary definitions are copied. This is neither an ETS word list nor an ETS-endorsed course. Third-party frequency rankings require separate rights verification before any commercial redistribution. US lexical and exam relevance editorial QA pending.

## 28 Oct 2026 — TOEFL + Daily 400/75 extension (private only)

The additional 200 general words and 25 phrasals reference pre-existing AEL lesson IDs;
this change does **not** copy any third-party ETS, COCA, AVL or dictionary content.
Academic Word List and AVL links are background methodology references, **not** proof
of exact TOEFL examination frequency. The AVL download page restricts commercial use
and rehosting; no AVL tables have been downloaded or redistributed by this sprint.
Upstream provenance of older AEL cards still needs independent review before release.
No ETS affiliation or endorsement is implied. The package remains development-only.

## 28 October 2026 — VOA Level 2 lessons 19–30 excerpt-evidence review (private only)

12 official VOA Lesson 19–30 *Conversation* pages were checked for 48 short
answer-evidence excerpts. Publisher URL and HTML-text line hints are stored with
original learner quiz IDs; these are not time-aligned audio transcript turns.
Three answer facts appear in text *stage directions* rather than spoken audio;
UI explicitly marks them as such. Publisher-written original VOA Learning
English dialogue is reusable with credit per <https://learningenglish.voanews.com/p/6861.html>.
The original Lesson 23 page also embeds third-party commercial song lyrics;
Lesson 30 also displays a song segment. Those lyrics were **not** copied,
licensed, or included in this data. Third-party audio rights remain unresolved
for any future downloaded audio. No new MP3 files, no offline license claim,
no physical iPhone/online playback verification or editorial signoff.

## 29 October 2026 — VOA19 and original 2026 TOEFL-style tasks

VOA Level 2 Lesson 19 Conversation is reproduced in the private development
archive with prominent VOA attribution and publisher URL. Speech and bracketed
stage directions are labeled separately; no third-party commercial-song lyrics
were imported. VOA's own works are available for credited use under its published
terms: https://learningenglish.voanews.com/p/6861.html. The remote publisher MP3
link is not a downloaded, licensed-for-bundling audio asset and has not been
tested on a device. No third-party rights are presumed.

The 6 new Reading tasks, 14 authored questions and 9 Writing practice tasks are
original AEL educational practice, **not** ETS practice questions, actual TOEFL
forms or ETS-endorsed materials. The 2026 test categories are described on ETS
public guidance but any release still requires editorial and rights review.

## 29 October 2026 — Original TOEFL-style integrated practice (private only)

Six Reading exercises and twenty comprehension questions, nine Writing tasks,
and eight script-only Listening scenarios with fourteen comprehension questions
were newly authored for the AEL project. No ETS copyrighted test questions or
recorded audio were copied. ETS public task categories are used for descriptive
compatibility; the app is not endorsed or officially scored by ETS. The new
Listening scripts have **no verified audio** and must never be described as
a real Listening test or as having approved human voices. Original content
still requires independent editorial review before any release.

## 2026-10-29 — VOA publisher-dialogue import and third-party exclusions

Voice of America Learning English explicitly permits reprinting its own produced text and MP3 material for educational/commercial use with attribution: https://learningenglish.voanews.com/p/6861.html . This does NOT license third-party songs, lyrics or externally licensed media: https://learningenglish.voanews.com/p/6021.html .

Level 2 Lessons 23 and 24 include attributed publisher Conversation text; Lesson 23 omits third-party lyrics and is **not** a word-for-word transcript of the entire audio recording. Remote publisher MP3 URLs are linked, not bundled, and not verified as playable or offline-ready on a physical iPhone.
