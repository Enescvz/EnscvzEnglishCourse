# American English Lab — 30 Oct 2026 engineering QA (private; DO NOT DEPLOY)

## Actual changes

- Retention observation: time-stamped same-card reviews are grouped into 7- and 30-day windows; missing subsequent reviews are not counted as successes; no control-group claim or proficiency estimate.
- TOEFL Writing: a **two-human-reviewer comparison protocol** (four explicitly scored dimensions) flags large disagreements and never emits an ETS score. This is a protocol, not a functioning AI essay grader.
- Safari: an in-app local airplane-mode test wizard creates an identifying marker, requires a reload, checks local data/Service Worker and records a **self-reported** device outcome; this is not independent physical iPhone QA.
- Automated lexical consistency audit: 975 cards (400 TOEFL words, 75 TOEFL phrasal verbs, 500 daily expressions) checked for missing fields, duplicate examples, and placeholders. Output `qa/20261030-editor-review/review-queue.csv`. **Zero automated flags is not human/editorial approval.** The `validate_editor_signoff.py` gate stays BLOCKED until every row is actually reviewed.
- VOA Level 1 Lesson 33–42: source importer built, tested with synthetic fixtures and publisher pages manually located. **No new full transcript imported in this runtime**: publisher HTML fetch failed in container, which cannot network directly; source review has NOT occurred for all ten complete texts. Public-source importer is in `tools/import_voa_level1_33_42.py`; see staging README. Source list remains 50 lessons/204 questions, imported 30, publisher-only 20.
- Removed a stale browser test assumption that robotically voiced Listening would create a play history. Modern smoke test checks real 25-question exam history instead.

## Limitations / non-negotiable gates

- Physical iPhone Safari and real offline storage: **not performed**; self-report wizard is not external QA.
- Human source/audio alignment and direct MP3 playback: **not performed**, no newly bundled audio.
- Independent US-English language editor: **not signed off**.
- 7–30-day actual learner study with measured delayed recall: **not performed**, observational feature awaiting data.
- TOEFL score mapping, multi-stage calibration and independent essay grading: **not available**; ETS's 1–6 score is never inferred from this practice.
- Speaking code and microphone flow untouched; old card IDs, saved progress format and audio exclusions retained.
- No GitHub upload, no Google Drive usage, no public deploy, no release ZIP. This is strictly a private development backup.

## How to use safely

1. Open using a secure HTTPS origin or `localhost`, not `file://`.
2. Check offline cache at Settings; save a JSON progress backup before any device experiment.
3. On physical iPhone add to Home Screen, disconnect network, force close/reopen; use the self-test control and document outcome. Do not call it independently passed.
4. Continue normal vocabulary and TOEFL practice without expecting official ETS band scores.
5. **Do not unlock public publishing** until all release-gate blockers have real evidence.

## Suggested delayed-recall validation protocol (not yet performed)

- Recruit willing learners with consent and stable study access, record starting English level without inferring health traits.
- Compare randomly allocated, difficulty-matched card sets using active recall + spaced repetition against a defined control learning schedule.
- Measure time on task and the same delayed-response format at **7 and 30 days**; predefine how missed follow-ups are counted; show raw observed and missing denominators.
- Do not claim "N% faster" or use a 1–6 TOEFL conversion until an independent study and ETS-aligned validation exist.
- The in-app Analytics displays descriptive 7/30 day *observed follow-ups only* and explicitly labels this limitation.

## ETS 2026 scope

Official 2026 ETS test contains Reading, Listening, Writing and Speaking; Reading/Listening use a multi-stage adaptive structure and reported scores are 1–6. AEL's original Reading and Writing practice is **not** calibrated to this operational scale. Human dual-rater comparison is a training protocol and returns `officialTOEFLScore: null` under all circumstances.

Sources: https://www.ets.org/toefl/test-takers/ibt/scores/understand-scores.html ; https://www.ets.org/newsroom/toefl-transformation-announcement.html
