import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pronunciation',ROOT/'tools/enrich_candidate_pronunciation.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class PronunciationTest(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(mod.normalize_pronunciation([['F','IH1','G','ER0']]),'F IH1 G ER0')
        self.assertIsNone(mod.normalize_pronunciation([]))

    def test_enrichment_is_staging_only(self):
        report=mod.enrich()
        self.assertGreater(report['generalWithLexicalPronunciationCandidate'],3000)
        self.assertGreater(report['phrasalsWithEachComponentCandidate'],1000)
        self.assertEqual(report['newApprovedTeachingCards'],0)
        self.assertFalse(report['releaseReady'])
        vocab=json.loads(mod.CATALOG.read_text(encoding='utf-8'))
        self.assertFalse(any(v.get('usPronunciationChecked') for v in vocab))

if __name__=='__main__':unittest.main()
