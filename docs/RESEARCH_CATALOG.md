# B2/C1 and phrasal source explorer — DEVELOPMENT ONLY

Goal: browse the existing source inventory without falsely teaching unverified entries.

Build: `python3 tools/build_research_catalog.py`. The source data comes from `sources/b2-c1-offline-catalog.json` and `sources/phrasal-candidates.json`. The output `data/candidate-catalog.json` contains only headwords, declared source-level candidates, part-of-speech candidates, pronunciation candidates, and references to existing lesson IDs. **No external definitions are included.**

The source general headwords are editorially unreviewed. Phrasal verbs are mixed multiword phrases, not independently CEFR rated: `l: null` is intentional. All 4,851 rows stay quarantined (`RESEARCH_HEADWORDS_ONLY_NO_TEACHING_CREDIT`) and do not enter `quizBank`, the spaced repetition engine, practice counters, or `data/vocabulary.json` / `data/phrasals.json`.

The viewport renders 30 cards per page. Data is lazily loaded only after visiting `#catalog`, so students never download the research corpus during normal lessons. Service worker caches it only opportunistically after first use.

Source pointers: CEFR-J B2, Octanove C1/C2, tema4p `English_Phrasal_Verbs_in_Action_EN.txt` (CC BY-NC 4.0, noncommercial). The development output distributes only headwords and metadata; verify rights before public deployment. No Google Drive used.

To produce active learning cards in bulk, use `tools/promote_content_batch.py` with real definitions, Turkish glosses and authored natural contexts, appropriate level evidence, and human signoff; do not directly move the research catalog into live `data/`.
