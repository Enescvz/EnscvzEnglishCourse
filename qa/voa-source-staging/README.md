# VOA Level 1 Lessons 33–42 — source import staging

**Status: NOT IMPORTED.** The private build retains **30 in-app transcripts and 20 publisher-only transcripts** until source pages are downloaded and individually checked. This folder is a work queue, not proof that ten transcripts have been completed.

The ten publisher URLs already exist in `data/voa-source-catalog.json`. The script `tools/import_voa_level1_33_42.py` retrieves the publisher **Conversation** section and tries to read its MP3 link. It requires a source-specific review of all turns, third-party music/lyrics and quiz evidence.

On a Windows computer with an internet connection:

```powershell
py -m pip install beautifulsoup4
py tools/import_voa_level1_33_42.py --fetch
```

Inspect all ten JSON transcripts, `source-review.json` warnings and publisher sources. **Only after independently comparing the entire text** and resolving all warnings:

```powershell
py tools/import_voa_level1_33_42.py --fetch --apply --confirmed-publisher-comparison
py -m unittest discover -s tests -p "test_*.py"
```

The command refuses an incomplete or evidence-mismatched page. This does not grant iPhone Safari/audio-sync or human-editor approvals. The publisher may change page markup and require parser maintenance.

VOA source policy: https://learningenglish.voanews.com/p/6861.html — VOA original materials generally public domain with attribution, third-party material excluded.
