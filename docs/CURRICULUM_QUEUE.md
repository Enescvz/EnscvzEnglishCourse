# Private authoring pipeline — B2/C1 and phrasal verbs

**NOT FOR GITHUB PAGES RELEASE. No student-facing card automatically created.**

## Selected private review queues

Run from repository root:

```bash
npm run curriculum:review-queues
```

Outputs (source-only, private):

- `sources/general-production-queue.json`: **3,500 UNIQUE headwords**, including all **281** existing authored general cards and **3,219** source-only candidates.
- `sources/phrasal-production-queue.json`: **600 UNIQUE expressions**, including all **199** existing authored phrasal cards and **401** additional source-only candidates without verified CEFR assignments.
- `qa/curriculum-queue-report.json`: audited counts, B2/C1 split, levels lacking evidence, disclaimer/status.

Current target-level candidates: B2 **2,393**, C1 **1,107**. The originally suggested C1=1,500 distribution is **393 candidate levels short**. These are source-level *claims*, not manual sense-level certification. In particular the 401 new phrasal items **must not receive a guessed B2 or C1 label**. Word selection is an editorial production order, NOT a validated American spoken-frequency ranking.

## Promotion of individually authored batches (all-or-nothing)

Human-authored JSONL, one JSON object per line, may be validated without writing:

```bash
python3 tools/promote_content_batch.py --input my-authored-words.jsonl --kind general
python3 tools/promote_content_batch.py --input my-authored-phrasals.jsonl --kind phrasal
```

Add `--apply` only after validation and reviewing the content to append records in `data/*.json`. Entries require: source-listed headword, B2/C1 level, English definition, Turkish meaning, original example + a different second example. Phrasal verbs also require syntax, register, a grammatical note, contextualized sense(s), and source-level evidence when they were unlevelled candidates. Existing records are never overwritten; reimported names are rejected. Newly added lessons are always `editorialStatus: authored_unreviewed`, never `approved`.

`--apply` is **not** an editorial signoff; it does not unlock the release. Written definitions/US semantic usage cannot be automatically verified solely by structural tests. A future license-compliant source of meanings/examples is still required for the remaining authored cards. The source-only headword lists **are not** copied into the deployed `data/*.json` without semantic completion.

Privacy: no Google Drive, no third-party user account, no GitHub write. The `sources/` directory is gitignored and included only in private development transfer archives.
