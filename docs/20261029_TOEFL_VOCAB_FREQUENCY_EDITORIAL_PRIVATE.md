# TOEFL + Daily — 475 Card Frequency and Editorial Evidence Check

**PRIVATE DEVELOPMENT / DO NOT DEPLOY — 29 October 2026.** Current 400 vocabulary + 75 phrasal verb *existing card IDs* and shared learning history are preserved. Speaking and audio were not edited.

## 1. What was verifiably checked

- **400 word and 75 phrasal IDs:** resolved, unique; all have a Turkish gloss, English definition and two distinct contextual examples. Automated structural and rough morphology audit performed and reproducible by `python3 tools/audit_toefl_475_source_quality.py`. These checks alone cannot verify accurate translation, natural English, correct usage sense, pronunciation, or TOEFL exam occurrence.
- **Coxhead AWL:** cross-checked **all 10 sublists (570 headwords)** against an openly published AWL headword table; **168 of 400** study words matched AWL headwords directly (**83 are in sublists 1–3**). The remaining **232** have no exact AWL headword match, but may be related word-family forms or high-frequency general English. Not having a direct headword match is *not evidence of uselessness*. AWL is for general academic texts, NOT official TOEFL exam frequency or an exact exam item list.
- **PHaVE / COCA:** cross-checked the published top **150** most frequent phrasal verb *forms*: **38 of 75** were on it. The other **37** are not disproved as useful in university, student life or TOEFL. PHaVE frequency is for expression forms across registers; *individual taught senses may have different frequencies*. Not an ETS rank.
- **Targeted editorial corrections:** 12 card definitions/examples/grammar notes were corrected for sense/example alignment and duplication. Cambridge Dictionary was consulted for `back up` and `take off` senses; rewritten example sentences are original AEL copy. Corrections are logged in `qa/toefl-editorial-corrections-20261029.json` with old/new values.
- **No invented scores:** no COCA per-million frequency, no 400-word frequency ordering, no claim of official TOEFL most-used word list. No redistribution of full corpus or proprietary dictionary definitions.

## 2. Verified sources

1. [Coxhead Academic Word List](https://www.wgtn.ac.nz/lals/resources/academicwordlist/information) and [AWL published table](https://www.eapfoundation.com/vocab/academic/awllists/index.php). AWL sublists are grouped by academic corpus frequency.
2. [PHaVE university teaching notes](https://globalaffairs.ucdavis.edu/iae/graduate/language-tips/high-frequency-phrasal-verbs), [PHaVE published frequency-rank appendix](https://afa4be34-0fda-46d9-8e64-5adf13d4216b.filesusr.com/ugd/5f2482_dd3f49d53f484b33b904bf7606641e1b.pdf). COCA-based general-language evidence, not ETS frequency.
3. [AVL academic corpus methodology](https://academic.oup.com/applij/article-abstract/35/3/305/146569) (methodology reviewed only; AEL cards were NOT individually AVL-ranked).
4. [Cambridge take off](https://dictionary.cambridge.org/dictionary/english/take-off) and [Cambridge back up](https://dictionary.cambridge.org/dictionary/english/back-up) (usage sense checks; definitions not copied).

## 3. Still open and blocking human signoff

- Full 400-word independent, sense-level native-US-English editorial approval (grammar, register, Turkish translations, collocations, example authenticity, academic relevance) **NOT DONE**; current targeted copy fixes are AI-assisted, not an independent qualified human editor.
- Individual COCA/AVL corpus ranks for every card, US spoken frequency and TOEFL exam occurrence are **not available in this audit**. Only AWL direct-headword matching and PHaVE top-150 expression matching were completed; word-family inflections and corpus-specific frequency need further research.
- Complete source licensing and original upstream reuse rights, actual Safari, speech playback and offline QA are separate release blockers.
- Do not mark `editorialSignoffComplete=true`, `frequencyAuditComplete=true`, `licensesChecked=true` or `readyForRelease=true` from this audit.

## 4. Reproduction

`python3 tools/audit_toefl_475_source_quality.py`, `npm test`, `python3 -m unittest discover -s tests -p 'test_*.py'`, `npm run release:check` (must remain **LOCKED**, exit nonzero). See generated `qa/toefl-475-frequency-and-editorial-audit-20261029.json` and CSV for item-level evidence/classifications.
