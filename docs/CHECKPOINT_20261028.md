# American English Lab — Private development checkpoint (2026-10-28)

**NO DEPLOY. NO GOOGLE DRIVE. Not a release.**

## Restored source state and limitations

The mounted full-project ZIP available in this session was dated before the latest claimed
979 general contextual lessons / 600 phrasal lessons snapshot. The latest fully authored
snapshot was NOT available as a full backup. We restored the last available complete
129-file project archive, then re-applied its original, existing authored batch from
`tools/author_batch_20261027.py` (+71 general, +57 phrasal). We did not reproduce
missing later lessons or falsely count their existence.

## Current *on-disk*, verified inventory

- 352 contextual B2/C1 general lessons (not editorially signed off).
- 284 finance/accounting contextual lessons, counted separately.
- 256 contextual phrasal-verb lessons (CEFR estimates not independently validated).
- 905 **additional** bilingual rapid-study cards (791 B2; 114 C1), no overlap with contextual general lessons.
- 1,257 distinct accessible general words when counting rapid and contextual *separately*; only 352 have full semantic fields.
- 18 original synthetic podcast MP3 lessons, 24 synthetic listening drills, 8 reading texts, 10 grammar lessons, 42 total local MP3 files.
- 3,647 vocabulary source candidates and 1,204 phrasal source candidates; NOT verified lessons.

## This iteration

- Rebuilt the complete runnable project from the latest available complete private ZIP and the newer local rapid data file.
- Added `js/rapid.js`: bilingual filtering, duplicate suppression, 10-minute retry / increasing-day recall schedule; never confuses rapid recognition with full mastery.
- Added a `rapid` route to `js/app.js`, separately saved progress, US-English device TTS, EN→TR / TR→EN study, B2/C1 and review-status filters, search and pagination, JSON backup/restore compatibility.
- Linked rapid-only words from the separate source catalog, without falsely labelling them complete lessons.
- Updated PWA cache (`sw.js`) for new module/data and all 42 existing audio recordings.
- Fixed `tools/rapid_gloss_import.py` to accept whole locally downloaded upstream B2/C1 JSON files without requiring an initial TSV file.
- Rebuilt the research catalog against restored contextual lessons.
- Removed outdated hard-coded counts from snapshot-fragile tests and added rapid tests.

## Tests and blockers

- `npm run test:all`: **36 Node + 46 Python tests passed**.
- `npm run qa:audio`: 42 synthetic MP3s file/timeline checks passed (not human speech).
- Simulated Chromium desktop passed; full combined desktop/mobile harness run timed out after desktop, so latest mobile E2E is **not confirmed**. Real iPhone Safari not tested.
- `npm run release:check`: nonzero; `readyForRelease:false` as intended.
- No editorial sign-off, no licensed human recordings; upstream bilingual translation redistribution rights need verification. Keep everything private.

## Reproducing a safe development session

```
cd american-english-lab
npm run test:all
npm run qa:audio
npm run release:check   # expected failure / release lock
python3 tools/rapid_gloss_import.py --upstream-json path/to/B2.json --upstream-json path/to/C1.json
```

Do not run the last command without first obtaining the source files and confirming
appropriate reuse rights. The importer replaces rapid cards with a deduplicated set
and does **not** alter authored semantic lessons.

## Next steps

1. Recover a *newer full project source* if user supplies it; reconcile, do not silently overwrite user progress.
2. Bulk ingest the remaining B2/C1 bilingual entries using upstream JSON with licensing diligence. Maintain source-level status, no inflated contextual lesson counts.
3. Expand contextual semantics, listening and reading, then real WebKit and human-voice licensed recordings.
4. Never publish or connect Google Drive.
