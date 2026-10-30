# Fluency Memory Sprint — 28 October 2026 (development only)

## Revised target agreed with user

- **500 B2 + 500 C1** distinct useful general English headwords.
- **500** distinct everyday phrasal verb targets.
- Finance/accounting remains **optional extra**, not counted toward the 1,000.
- Improve comprehension and spontaneous speaking, not merely recognition of glosses.
- Content must use American English and be presented with truthful level/quality metadata.
- **Never publish, upload to GitHub, or create an alleged release ZIP while incomplete. No Google Drive.**

## Focus catalog is not the finished curriculum

`data/fluency-focus.json` is a deterministic, disjoint target list. It contains:

| Target group | Target headwords | Context drafts | Gloss-only drafts | Headword only |
|---|---:|---:|---:|---:|
| B2 + C1 general | 1000 | 352 | 504 | 144 |
| Phrasal verbs | 500 | 256 | 0 | 244 |

General-level split is **500 B2 / 500 C1**. Level assignments of the existing authored cards are not independently verified; phrasal candidates without reviewed CEFR keep `level:null`. Focus shortlist is an editorial heuristic, **not** a validated ranking of American spoken frequency. A small handwritten conversational-use shortlist is used first; existing authored lessons follow; bilingual drafts are ordered by a **weak written-English frequency proxy** when `textblob` is installed, and unglossed candidates fill the remaining places. Technical availability never implies content accuracy or license clearance.

`tools/build_fluency_focus.py` rebuilds the focus list offline. The old 3,500/600 production-queue files are **historical** and no longer define the user's requested target. They remain archived for provenance and must not be injected as current focus goals.

## Memory Coach — working app module

`js/memory.js` and the `/memory` app route implement a short active-memory practice loop across existing contextual lessons:

1. **Build a cue:** inspect an English definition, Turkish gloss, one or two existing examples, and optionally write a personal association/story; cue persists in `progress.memoryCues`.
2. **Listen without text:** browser `en-US` synthesized voice reads the item; type what you hear (exact-normalized check), or skip if your device has no `en-US` voice; never count a skipped listening trial as successful.
3. **Retrieve from Turkish:** type the full English expression without a visible answer; optional personal cue; answer reveal scores a miss rather than a success.
4. **Produce:** write your own different sentence, then self-assess; interface explicitly explains that semantic/grammar correctness cannot be auto-verified.
5. **Spaced review:** one FSRS-5 review per completed item; due cards scheduled ahead of new material. Only observed listening and typed recall are recorded as such; self-reported sentence production uses a **separate** property, never the verified production mastery field.

Progress shares existing vocabulary/phrasal FSRS records and JSON export/import. 10-item sessions allow B2, C1, or phrasal scope. A finished lesson is selected only if the ID is present with an English definition, Turkish gloss and example; **gloss-only and headword-only candidates are not silently upgraded**. TTS is device-dependent, not a licensed native-speaker recording. No persistent cloud account or external audio processing is required for this coach.

## Automated evidence

- Node unit + UI contract tests: **43 passed**.
- Python corpus tests: **49 passed**.
- Static Chromium sandbox harness: **desktop flow passed**; full combined desktop+mobile run **timed out after desktop**, so mobile and real Safari/WebKit remain **unverified**.
- `python tools/release_gate.py` remains **nonzero / locked**. Release gates now target full and editorially approved 1,000 / 500, plus pre-existing listening, audio, QA requirements.

## Research basis (method selection, not a performance guarantee)

- Kim et al. (2022), *The Effects of Spaced Practice on Second Language Learning: A Meta-Analysis*, *Language Learning*. https://doi.org/10.1111/lang.12479
- Karatas et al. (2025 print / 2021 online), *Improving second language vocabulary learning and retention by leveraging memory enhancement techniques*, *Language Teaching Research*. https://doi.org/10.1177/13621688211053525
- Rice & Tokowicz (2020), *A Review of Laboratory Studies of Adult Second Language Vocabulary Training*, *Studies in Second Language Acquisition*. https://doi.org/10.1017/S0272263119000500
- Oxford Learner's Dictionaries, explanation of selecting advanced B2-C1 headwords by frequency and learner relevance. https://www.oxfordlearnersdictionaries.com/about/wordlists/oxford3000-5000.html

Evidence supports retrieval and spacing; it does not establish that a set of 1,500 expressions guarantees C1 fluency or permanent retention. Accuracy and frequency selection need independent editorial/source verification. Personal mnemonic cues help engage memory but do not magically remove forgetting.

## Remaining critical tasks

- Upgrade **504** gloss-only words to genuine teaching cards with independently checked meaning, natural examples, and comprehension activities; author **144** headword-only items in the 500/500 target split.
- Fully author **244** phrasal candidate expressions with valid senses, syntax, and examples; verify everyday American use and CEFR level, and replace less relevant candidates when necessary.
- Review all 352/256 contextual drafts with qualified human editorial approval; add second independent contexts where missing.
- Expand original natural-speech listening + production exercises, perform genuine WebKit/iPhone test, and resolve the audio, editorial and license gates before publication.
