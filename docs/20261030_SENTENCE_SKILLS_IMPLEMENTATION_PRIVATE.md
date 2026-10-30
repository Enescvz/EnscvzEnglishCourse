# AEL Sentence Skills — 2026-10-30 (PRIVATE / DO NOT DEPLOY)

## Scope and delivery

Added **34 authored lessons** and **340 distinct reference sentences** to the existing American English Lab offline-first static app. No new vocabulary, phrasal, daily-expression or audio lessons were added.

| New module | Lessons | Exercises |
|---|---:|---:|
| Question Builder | 12 | 120 |
| Preposition Lab | 10 | 100 |
| Connector Lab | 8 | 80 |
| Sentence Builder | 4 | 40 |

Each lesson contains ten staged exercises: **2 tap-to-order tasks, 4 contextual cloze tasks, 2 free productions, 2 contextual transfers**. The final four prompts have manually authored Turkish scenarios tied to the English model responses, not only a generic "write something" instruction. Exercises contain a rule, a common error and a model answer.

## Access and architecture

- Navigation: **Soru & Cümle Atölyesi**; homepage shortcut and discovery card.
- Separate skill decks and learner progression under `P.skillCards` and `P.skillHistory` (stable `sk-*` task keys). Existing `cards`, `phrasals`, `expressions`, `memoryCues`, `writing`, `events` etc. are not overwritten.
- Review scheduler reuses `engine.reviewItem()` / FSRS-5 math; due skill cards are reached through the skills page and linked from Smart Review. This is **not an independently calibrated retention model**.
- Input feedback: token reordering and cloze answers are checked against a normalized single reference response. An unmatched response is **not** necessarily ungrammatical: the user can explicitly switch to self-assessment for a valid alternative. Free text has **no automated grammar or semantic grading** and must be self-assessed.
- Save safety: skill grading uses a single prospective-progress write. If `localStorage.setItem` throws, memory state stays unchanged and the UI does not claim the record was saved.
- Backup export includes `skillCards` and `skillHistory`; existing additive import/merge handles both without deleting older keys, with newer timestamp wins for reviewed tasks.
- Long-term observations: 7–14 and 30–45 day reference-match windows, only if a learner genuinely returns. No estimated memory retention is stated as measured fact.
- Service Worker caches `sentence-skills.json` and `sentence-skills.js`; cache version incremented. Content texts and UI can be available without internet once the offline cache installs successfully; this **does not** establish real iPhone Safari functionality.

## Content and fidelity policy

- Authored reference sentences are exercises, not licensed copies of third-party courses.
- `independentEditorApproved=false`; editorial, regional US usage and edge-case review still required.
- `audio=null`; no synthetic recording was introduced and no human audio was invented.
- No publishing, GitHub push, deployment, release zip or Speaking changes. Existing Speaking region SHA-256 prefix matches original: `984556e8e67108cf`.
- TOEFL mock exams and examination modes are unchanged.

## QA performed (2026-10-30)

- `npm test`: **121/121** Node tests passed (includes 8 new curriculum/safety tests).
- `npm run test:corpus`: **197/197** Python tests passed (includes 3 new data/integration tests).
- `python3 tests/e2e_sentence_skills_virtual.py`: simulated-origin Chromium desktop **PASS**, simulated 390px mobile viewport **PASS**. Covered navigation, order, answer comparison, self-assessed production, local mock storage. This **is not genuine iOS/Safari E2E evidence**.
- `release:check`: remains **blocked**, as intended.

## Open quality gates before public use

1. Independent review of all authored examples and targeted Turkish scenarios; evaluate acceptable grammatical alternatives in a pilot.
2. Real iPhone Safari test: install, offline restart, cache migration, localStorage durability and JSON restore.
3. Real user learning outcome study with 7-day and 30-day follow-up; validate retention thresholds and task utility.
4. Core AEL gates still outstanding: verified human-voice Listening, missing VOA transcripts and TOEFL writing assessment fidelity.
5. The production/transfer tasks currently use **manual self-rating**. Do not advertise them as automatically AI graded.

## Run locally

```bash
cd american-english-lab
python3 -m http.server 8080
# open http://localhost:8080/#/sentenceSkills
npm test
npm run test:corpus
```

**Important:** This ZIP is a private development backup, not a public release candidate.
