# TOEFL + Daily English — 400/75 content expansion (private, 2026-10-28)

## Scope

- Previously shared set: **200 vocabulary + 50 phrasals**. Both ordered ID lists remain byte-for-byte prefixes of the new set, with no re-keying of learner storage.
- Extension: **200 existing general word cards + 25 existing phrasal lessons** (all reference old `data/vocabulary.json` or `data/phrasals.json` IDs; do not duplicate lessons).
- Final shared catalogue: **400 word IDs (50 original AEL TOEFL academic drafts + 350 existing AEL general cards), 75 phrasal IDs (all existing AEL cards)**.
- Goal: blended everyday American English and current TOEFL daily/campus/academic language. Vocabulary priorities cover evidence, inference, cause/effect, study, student life and conversational interactions. This is a qualitative shortlist; no official ETS word-frequency ranking or corpus frequency statistics are claimed.
- Learner pacing: 10 new words and 3 new phrasals per day -> at least 40 days to encounter the 400 words once; spaced retrieval continues afterward. Do not claim fluency or TOEFL score guarantees.

## Provenance and licensing

- Card glosses/examples in this extension are **existing project authored drafts** (no new lexicographic corpus copied). AWL research: https://www.wgtn.ac.nz/lals/resources/academicwordlist/information . COCA AVL research: https://www.english-corpora.org/coca/avl.asp , with licensing restrictions on redistribution. Updated ETS content overview: https://www.ets.org/content/ets-org/language-master/in/home/toefl/institutions/ibt/about/content-structure.html .
- Word/phrase frequency ranking, independent American English semantic/editorial validation, original upstream reuse rights, pronunciation and real iPhone/offline QA remain **unverified**. This is not an ETS-affiliated course. `licensesChecked=false`, no release approval.

## Rebuild and invariant checks

- `python3 tools/curate_toefl_core_20261028.py`: deterministic generator; refuses duplicates or attempts to change the old 200/50 prefix; checks that extension cards belong to general vocabulary and possess 2 distinct examples, and that phrasal entries are extant.
- `sources/toefl-core-original-200-50-20261028.json`: frozen historic prefix for strict no-history-loss validation.
- `sources/toefl-curated-extension-20261028.txt`: 200 manually chosen shared general cards (not frequency-certified).
- `sources/toefl-phrasal-extension-20261028.txt`: 25 manually chosen existing phrasal cards.
- The Vocabulary and Phrasal UI reads the counts dynamically; prior lesson storage remains mapped to same IDs. `sw.js` cache name bumped to avoid stale catalogue JSON.

## QA limitations

- JavaScript/Python checks cover code paths, ID sets, learning UI and structural content. Passing these does **not** establish CEFR, linguistic precision, audio playback, reading/writing improvements, full TOEFL coverage, WebKit on actual iPhone, or reliable offline support.
- Speaking is not edited or altered. Existing 50 VOA sources, 12 embedded conversation transcripts, 204 questions, and 52 transcript-evidenced quiz questions are untouched.
- Not deployed, no publication ZIP, no Google Drive/GitHub operations. Release gate remains LOCKED.
