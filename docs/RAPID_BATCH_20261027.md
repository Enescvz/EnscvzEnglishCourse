# Rapid Bilingual Card Batch — 2026-10-27

## Verified local counts

| Inventory | Count | Meaning |
|---|---:|---|
| Full-semantic-field general words | 979 | Definitions and an example, not editorially approved |
| Specialist Accounting/Finance | 284 | Separate lessons, unreviewed |
| Unique full-field phrasal verbs | 600 | CEFR labels include editorial estimates, not source-certified |
| NEW rapid bilingual gloss-only cards | **905** | **791 B2 + 114 C1**, not duplicated in full general cards |
| General words accessible in a learning interface | **1,884** | 979 full + 905 rapid; distinct tiers |
| Source-only B2/C1 inventory | 3,647 | Candidate level classification; NOT 3,647 complete cards |
| Source phrasal candidates | 1,204 | Not all valid or CEFR-verified |

## What changed

- `tools/rapid_gloss_import.py` bulk imports bilingual B2/C1 pairs from local TSV and optionally whole upstream JSON files. Validates source membership and ensures no duplicated teaching entry.
- `data/rapid-vocabulary.json` has 905 distinct entries. Explicit `teachingDepth=gloss_only`, `editorialStatus=unreviewed`. No fake definitions or invented context sentences.
- `js/rapid.js` supports level filtering, bilingual searches, and simple self-assessed recall review.
- `js/app.js` adds a Rapid Deck route reachable via home discovery card and sidebar, with en-US device TTS and local review progress. JSON backup includes this progress.
- `sw.js` precaches the new module and rapid JSON for offline study.
- Automated tests cover import validity, uniqueness, source labels, overlap exclusion, filters, UI, simulated desktop/mobile browser paths and offline manifest.

## Publishing lock

The added rapid records do not count toward the 3,500 approved contextual general lessons nor the mandatory editorial signoff. No GitHub deployment, no release ZIP, no Google Drive. The upstream translation licensing requires a separate redistribution check. The simulated-browser test is not real iPhone WebKit proof.

## Fast continuation

The remaining headwords can be imported in one batch as soon as the publicly distributed `B2.json` and `C1.json` bilingual lexicon files are placed locally, using `--upstream-json` twice. The local corpus is already staged for headword/CEFR matching. The target 3,500 fully contextual lessons still requires source-grounded English definitions, two accurate original examples and editorial verification.
