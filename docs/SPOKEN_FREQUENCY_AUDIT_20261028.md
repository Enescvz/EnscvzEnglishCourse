# 28 October 2026 — Daily spoken English suitability check (preliminary)

## The key finding

The target list has **1,000 general word entries (500 B2 / 500 C1) and 500 phrasal entries**, and full-context draft cards exist for all. **This does not establish that every item is frequent in spoken American English.** The project metadata explicitly warns the shortlist is editorial, *not a spoken-frequency ranking*.

An initial transparent rule-based/manual editorial flag pass marked **58 general** and **13 phrasal** entries needing priority review. This is a *minimum illustrative shortlist*, **not the number of statistically rare words**. No entry currently has validated US spoken frequency rank or sense-specific editorial approval.

Examples to reconsider: C1 *unmusically, pendulous, repertory, concerto, verandah, fiendishly*; B2 *typhoid, mutton, unto, monastery*; phrasals such as *get up, wake up* are useful but may already be known to a B1 learner, so test for novelty. Compare with higher-utility words such as *acknowledge, reluctant, overwhelmed, straightforward, figure out, bring up, turn out*.

## Approval gates for replacing / admitting target cards

1. Check **US spoken-language or US TV/movie subtitle frequencies** and record corpus, date, lemma and word sense, not just CEFR headword.
2. Prioritize **real conversations, podcast/listening comprehension, requests, disagreements, emotions, plans, explaining causes and opinions**. Include common phrases and collocations.
3. Test **B1 novelty** before forcing 500 B2 + 500 C1. CEFR labels do not imply a rank in spoken frequency. A rarer C1 word cannot outrank a very useful B2 collocation just to fill quotas.
4. Manually verify **American senses, multiword syntax, examples and pronunciation**. Do not mark as editorially approved without real review.
5. Replace weak items **without erasing user progress**: keep a mapping from old card ID to archived/supplemental entry; preserve the review history and show new priority separately.
6. Do **not** use purchased/restricted corpora as distributed app assets without appropriate permission. Keep only rank/flags where licensing permits.

## Project status and artifacts

- `qa/spoken-priority-review.csv`: one row per target, explicit unverified-frequency status, initial qualitative review flags.
- `qa/spoken-priority-report.json`: totals and methodological caveat.
- `tools/audit_conversational_priority.py`: repeatable preliminary flag generator.
- Both 1,000 general and 500 phrasals **remain drafts** pending quality review. Publication remains locked. No selection is silently replaced by this audit.

**Primary external methodology references:** COCA / its spoken and TV/movies genres (english-corpora.org), wordfreq (pypi.org/project/wordfreq) combining subtitle and other domains, English Vocabulary Profile / Cambridge sense-level guidance. Frequency numbers are not yet imported, so none are claimed.
