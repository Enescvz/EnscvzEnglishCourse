import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build_curriculum_batches',ROOT/'tools/build_curriculum_batches.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class BatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=mod.generate()
        cls.v=json.loads((ROOT/'sources/general-production-queue.json').read_text())
        cls.p=json.loads((ROOT/'sources/phrasal-production-queue.json').read_text())

    def test_full_review_queue_targets_not_teaching_counts(self):
        self.assertEqual(len(self.v),3500)
        self.assertEqual(len(self.p),600)
        self.assertEqual(self.report['newEditoriallyApprovedCards'],0)
        self.assertFalse(self.report['publicationAllowed'])

    def test_no_duplicate_headwords(self):
        self.assertEqual(len({x['word'].casefold() for x in self.v}),3500)
        self.assertEqual(len({x['word'].casefold() for x in self.p}),600)

    def test_existing_cards_retained(self):
        for x in [e for e in self.v if e['teachingCardExists']]:
            self.assertEqual(x['origin'],'existing-authored-card')
        self.assertEqual(sum(x['teachingCardExists'] for x in self.v),len([x for x in json.loads((ROOT/'data/vocabulary.json').read_text()) if x.get('category')=='general']))
        self.assertEqual(sum(x['teachingCardExists'] for x in self.p),len(json.loads((ROOT/'data/phrasals.json').read_text())))

    def test_unreviewed_phrasals_never_get_fake_cefr(self):
        for x in self.p:
            if not x['teachingCardExists']:
                self.assertIsNone(x['levelCandidate'])
                self.assertFalse(x['editorialApproved'])
                self.assertTrue(x['requiresSenseAndCEFRReview'])

    def test_only_source_level_candidates(self):
        self.assertTrue(all(x['levelCandidate'] in ('B2','C1') for x in self.v))
        self.assertTrue(any(not x['teachingCardExists'] for x in self.v))
        self.assertGreater(self.report['missingC1CandidateLevelsToReachMix'],0)

    def test_serialized_and_private_only(self):
        self.assertTrue((ROOT/'sources/general-production-queue.json').is_file())
        self.assertTrue((ROOT/'sources/phrasal-production-queue.json').is_file())
        gitignore=(ROOT/'.gitignore').read_text()
        self.assertIn('sources/',gitignore)

if __name__=='__main__':unittest.main()
