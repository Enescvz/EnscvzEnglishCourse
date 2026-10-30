# American English Lab — 29 October 2026 private gap reduction

**Development snapshot only. DO NOT DEPLOY. Speaking code untouched.**

## Grounding

* Original baseline: `AEL_PRIVATE_DEV_BACKUP_20261029_TOEFL2026_INTEGRATED_PREP_QA_DO_NOT_DEPLOY.zip`.
* ETS 2026 test task names and indicative sections: https://www.ets.org/toefl/test-takers/ibt/about/content.html?version=after-jan-2026 . Original practice, **not** ETS questions, calibrated adaptive test or official TOEFL score. Public TOEFL section time/length is not equivalent to this corpus.
* VOA rights: https://learningenglish.voanews.com/p/6861.html . Only VOA-original dialogue content is used, with source attribution. Third-party material excluded.

## Actual changes in this sprint

1. **VOA L2 Lessons 20–21:** The Test Drive and Trash to Treasure Part 1 entire publisher Conversation dialogue with speaker/stage turn indexing and online published MP3 URLs. Source files in `sources/voa-reviewed-lesson-20-20261029.txt` and `...21...`. Exact, idempotent importer: `tools/import_reviewed_voa_20_21.py`. Two source pages inspected; four old quiz questions each re-anchored to exact in-app turns. Full-transcript coverage **21/50**; linked-only **29/50**. All **204/204** questions have text provenance: **88 in-app turn** (86 spoken + 2 stage), **116 publisher-page excerpt**. Stage direction evidence is not an audible spoken utterance. No audio-download, remote playback, or synchronization certification.
2. **Non-ETS Reading diagnostic:** 34 existing original questions, all three Reading task categories, 30-minute practice timer, five questions/page to avoid creating a huge mobile DOM. Existing 9-question/12-minute mini remains available. The new test is not a true full TOEFL or multistage/adaptive simulation; item bank is far too small and questions repeat. All feedback is local correctness (no score conversion).
3. **Reading session continuity:** Unfinished practice stored under new optional `toeflActiveReading` property in the existing `ael-progress` object, with question identities, local answers and original wall-clock start time. Closing the practice screen retains the unfinished timer. Resume revalidates question IDs against authored content; finishing clears only the active session and keeps prior attempt history. Reload during an active attempt also reconstructs the session. No old card IDs or history deleted.
4. **Personal feedback:** Reading subcategory observation counts / accuracy and concrete weak-category recommendations use completed Reading attempts only. Writing revisions use observable word, sentence and paragraph metrics and task-specific manual editing prompts. No automatic grammar, semantic, pronunciation or ETS-score claims.
5. **Validation:** New automated tests cover all diagnostic questions, malformed answer keys, offline service-worker shell and range-response simulation, preserved VOA IDs and source-anchored questions, explicit approval flags and 475-card editorial queue. The 475 focus cards have definitions and >=2 context examples, but this does **not** constitute US frequency ranking or human editorial approval.
6. **QA honesty:** Virtual Chromium desktop and mobile-view QA passed. Real localhost HTTP offline/browser QA was **blocked by administrator policy** (`ERR_BLOCKED_BY_ADMINISTRATOR`). Simulated worker cache tests passed; they are not a replacement for actual offline Safari. Remote MP3 playback, true offline listening, and physical iPhone Safari not tested. All 42 legacy synthetic eSpeak MP3s remain unapproved.

## Explicitly incomplete / next required actions

| Blocker | Now | To approve |
|---|---|---|
| Full VOA transcripts | 21/50 | Manually compare the 29 remaining publisher Conversation texts, stage directions and third-party exclusions; import only after exact evidence check |
| Source-text question evidence | 204/204 | Independent audit for answer quality and distractor validity is still advisable; evidence is not audio alignment |
| Listening quality / offline sound | 0 local approved human MP3 | Obtain lawful VOA originals, check actual decoder/browser playback, timing alignment, US speech intelligibility and license rights per asset |
| TOEFL Listening task simulations | 8 text-only studies | License/generate verified naturally spoken recordings before recording any *listening* success |
| TOEFL full-length adaptive + 1–6 scoring | Not available | Human-reviewed sufficiently large original test bank, psychometric calibration, proper four-skill administration; do not pretend ETS scoring |
| Writing automatic quality grading | Structural observations only | Human rubrics/rater evaluation or validated system; no score extrapolation before that |
| Speaking | Not touched | Do not modify unless the user explicitly revokes the speaking freeze |
| Editorial core frequency | 0/475 independently reviewed | Review `qa/toefl-475-independent-review-queue.csv` with a qualified en-US editor and licensed corpora; document senses, register, actual frequency by source |
| Physical Safari / real offline | Not tested | Check on actual iPhone: install as PWA, go offline, restart, restore user progress, stream VOA while connected, confirm audio and transcript, record screenshots/results |
| Release gates | LOCKED | No deployment, GitHub upload, Google Drive, public ZIP, false passing flags |

## Reproducible checks

```sh
npm run test:all
python tools/audit_voa_completion_queue.py
python tools/audit_toefl_core_editorial.py
python tests/toefl_prep_browser_smoke.py      # virtual Chromium only
python tests/real_offline_chromium.py        # expected BLOCKED in this environment
python tools/release_gate.py               # expected nonzero LOCKED
```

All generated ZIPs named `PRIVATE_DEV_BACKUP_...DO_NOT_DEPLOY` are *source backups*, not release packages. No external storage or hosting action was undertaken.

**Final retest note:** The automated 230-test suite passed again. A further virtual Chromium rerun after documenting the results timed out without an exit result; the earlier targeted desktop/mobile run passed. This last rerun is **not** counted as a second pass.
