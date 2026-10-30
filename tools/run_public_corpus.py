#!/usr/bin/env python3
"""Run source-independent corpus tests in the public repository.

The full corpus test suite requires intentionally gitignored, rights-sensitive
reference material in sources/. This runner reports every excluded test, never
counts exclusions as passes, and fails on real failures in the remaining suite.
Run `npm run test:corpus` only from the complete private development archive.
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Only checks that require quarantined publisher/third-party or development
# reference source files are excluded. Entries are explicit so that newly
# introduced tests are *not* automatically excluded.
SOURCE_DEPENDENT_CLASSES = {
    "test_curriculum_batches.BatchTests",
    "test_daily_context_sprint_20261028.DailyContextSprint",
    "test_daily_spoken_curation.DailySpokenCurationTests",
    "test_final_focus_words_20261028.FinalFocusLessons",
    "test_final_phrasal_focus.FinalPhrasalFocusTests",
    "test_general_context_sprint_20261028.GeneralContextSprintTests",
    "test_reviewed_voa_13_14.SourceReviewed1314Tests",
    "test_reviewed_voa_15_18.Reviewed15To18",
    "test_useful_phrasal_batch.UsefulPhrasalBatchTests",
}

SOURCE_DEPENDENT_TESTS = {
    "test_candidate_pronunciation.PronunciationTest.test_enrichment_is_staging_only",
    "test_daily_expressions_500_20261029.DailyExpressions500ExtraTests.test_source_reproducible_and_editorially_pending",
    "test_import_offline_lexicon.OfflineImportTests.test_catalog_structure_and_level_labels",
    "test_import_offline_phrasals.OfflinePhrasalTests.test_1204_real_source_headwords_staged",
    "test_import_offline_phrasals.OfflinePhrasalTests.test_all_source_entries_protected_against_auto_approval",
    "test_rapid_deck.RapidDeckTests.test_upstream_json_only_import_can_run_without_tsv",
    "test_research_catalog.ResearchCatalogTests.test_real_generated_catalog_covers_source",
    "test_reviewed_voa_07_08_20261028.VOASevenEightTests.test_07_complete_page_conversation_with_turn_evidence",
    "test_reviewed_voa_20_21.VOATwentyTwentyOneTests.test_full_conversation_and_evidence_source_checked",
    "test_toefl_daily_core_20261028.TOEFLDailyCoreTests.test_generation_repeatable",
    "test_toefl_daily_core_20261028.TOEFLDailyCoreTests.test_original_core_prefix_and_existing_context_immutability",
    "test_voa_25_30_integrity.FourVOATranscripts.test_source_and_all_question_evidence_exact",
    "test_voa_reviewed_23_24.VOAReviewed2324Tests.test_imported_scripts_match_source_dialogue_and_have_grounded_questions",
}


def flatten(suite: unittest.TestSuite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from flatten(test)
        else:
            yield test


def is_source_dependent(test_id: str) -> bool:
    return (test_id in SOURCE_DEPENDENT_TESTS or
            any(test_id.startswith(c + ".") for c in SOURCE_DEPENDENT_CLASSES))


def main() -> int:
    os.chdir(ROOT)
    suite = unittest.defaultTestLoader.discover(str(TESTS), pattern="test_*.py", top_level_dir=str(TESTS))
    discovered = list(flatten(suite))
    selected, withheld = [], []
    for test in discovered:
        (withheld if is_source_dependent(test.id()) else selected).append(test if not is_source_dependent(test.id()) else test.id())
    # Explicitly visible exclusions; never equate an incomplete suite with full QA.
    print(f"PUBLIC CORPUS: {len(selected)} tests scheduled; {len(withheld)} source-bound tests NOT EXECUTED", flush=True)
    for name in withheld:
        print(f"  NOT EXECUTED (private sources): {name}", flush=True)

    summary = os.getenv("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(f"## Corpus test scope\n\n"
                    f"- Public-safe tests scheduled: **{len(selected)}**\n"
                    f"- Source-dependent tests **NOT EXECUTED**: **{len(withheld)}**\n"
                    "- Full private corpus audit: **not verified by this workflow**\n"
                    "- This green check is **not** permission to publish AEL.\n\n")
            f.write("<details><summary>Excluded source-dependent test IDs</summary>\n\n")
            for name in withheld:
                f.write(f"- `{name}`\n")
            f.write("\n</details>\n")

    if not selected:
        print("ERROR: No public-safe corpus tests discovered", file=sys.stderr)
        return 2
    result = unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite(selected))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
