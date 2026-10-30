# American English Lab — Conversation & Retention Sprint (2026-10-28)

**Private work in progress — not ready for publication, Google Drive or GitHub.**

## Target and verified scope

The user-approved learning target is **500 B2 + 500 C1 everyday-use vocabulary headwords, plus 500 useful phrasal verbs**. These are target counts, not certified CEFR frequency rankings, nor a promise of perfect fluency. Accounting & Finance (284) remains a separate optional category.

| Category | Earlier | Current | Change | Still missing |
|---|---:|---:|---:|---:|
| Focused vocabulary contextual drafts | 352 | **422** | **+70** | 578 |
| Focused phrasal contextual drafts | 256 | **318** | **+62** | 182 |
| Rapid-only bilingual cards, distinct from contextual lessons | 905 | **852** | **-53 overlap removals** | N/A |
| Focused vocabulary gloss-only targets | 504 | **451** | **-53 promoted** | 451 |
| Focused vocabulary headword-only targets | 144 | **127** | **-17 promoted** | 127 |
| Focused phrasal headword-only targets | 244 | **182** | **-62 promoted** | 182 |

**B2/C1 focus breakdown:** B2: 150 contextual, 350 gloss-only; C1: 272 contextual, 101 gloss-only, 127 headword-only. These are educational source labels, subject to independent sense-level verification. A level assigned to a phrase by our authors is a provisional estimate, not CEFR certification. The 852 rapid cards are bilingual recognition drafts, not full contextual lessons.

### Newly drafted content

- `sources/authored-20261028-conversational-words.jsonl`: **70 original** English explanations, Turkish meanings, and two deliberately distinct English examples. No copyrighted dictionary example text has been copied as new teaching copy.
- `sources/authored-20261028-conversational-phrasals.jsonl`: **62 original** phrasal explanations, Turkish meanings, two examples, grammatical structure notes and meaning-use sense records.
- Applied with `tools/promote_content_batch.py` to `data/vocabulary.json` and `data/phrasals.json`, preserving existing IDs and active records. New records have `editorialStatus: authored_unreviewed`; **no one marked them editorially approved**. The two batch scripts are repeat-safe: rerunning reports no new items without creating duplicates.
- Changed the historical phrasal production-queue validator to accept *current-focus* candidates only when each phrase also exists in the source-provenance catalog. Arbitrary items remain disallowed.
- The legacy CEFR source selected beginner headwords such as `man`, `house`, or `behind` when a rare advanced sense was intended. The C1 **headword-only** shortlist now first prioritizes genuinely useful-looking advanced candidates and excludes these obviously basic headwords. The selected items still require individual meaning and CEFR review. A parallel curated phrasal priority list reduces alphabetic source-order noise. Neither is a quantified spoken-American frequency ranking.

### Memory Coach improvements

The five-stage practice loop now runs:

1. **Personal mnemonic:** review meaning and two original contexts, save a personal story or visual cue.
2. **Auditory discrimination:** hear the expression using an available **device en-US TTS voice**, and transcribe it. Pressing check before an utterance actually **starts** cannot grant listening credit. Users without this voice can explicitly skip; no listening credit is given.
3. **Active recall:** retrieve the exact English term from its Turkish meaning with no answer revealed until grading.
4. **Context recognition:** read a *second* English context and choose the correct Turkish sense from **four distinct alternatives**; the answer remains hidden until a choice is made. This is a recognition task, not a claim of productive speaking mastery.
5. **Sentence generation:** write an original sentence and self-evaluate. Since the app does not have an automatic grammar/meaning judge, this is stored as **self-reported production only**.

FSRS-5 is used for reviewing; a `good` grade now requires a successful listened-and-written trial, typed recall, context answer, and self-confirmed sentence. Incorrect recall is graded `again`; listening/context errors and untestable stages constrain the grade to `hard`. Success in context is logged as observed `modeSuccess.context`; user-reviewed sentence production never masquerades as verified productive mastery.

Audio caveat: device TTS is synthetic and may be unavailable or less natural than real recordings. A `speechSynthesis.onstart` event confirms playback began, not that the learner actually heard audio; genuine listening QA still requires human recordings and device testing.

### Quality checks performed

- `npm run test:all`: **45 Node tests + 50 Python tests passed**.
- `npm run qa:sandbox`: synthetic-origin Chromium **desktop + mobile-viewport** UI flow passed with mocked storage, **not real iPhone/WebKit and not release evidence**.
- `python tools/audit_examples.py`: JSON/structural checks passed; **447 existing records** across the *entire* lesson bank still need a second independent example. Manual semantic verification has **not** been performed.
- `python tools/audio_qa.py`: all **42 synthetic MP3** container/timing checks passed; this is not transcript-to-human-speech validation.
- `python tools/release_gate.py`: expected **nonzero exit**, **LOCKED**, including incomplete lessons, human audio, expert signoff and true desktop/iPhone E2E.
- Service worker cache bumped to `ael-dev-20261028-fluency-memory-2`; offline manifest includes the current JSON and 42 bundled MP3s.

### Next editorial work

Prioritize 451 bilingual gloss targets and 127 C1 candidate words for real original examples and exact sense verification. Author 182 remaining phrasal entries with meanings and syntax, ensuring natural US usage and avoiding the automatic inference that all source strings are true phrasal verbs. Target short real-life listening dialogues and shadowing, then qualified English review. **Do not upload to GitHub or Google Drive or distribute a release ZIP until all real release gates pass.**
