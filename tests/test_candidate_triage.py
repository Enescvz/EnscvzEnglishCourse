import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('triage_candidates', ROOT / 'tools' / 'triage_candidates.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CandidateTriageTests(unittest.TestCase):
    def test_deduplication_and_publication_gate(self):
        rows = module.triage([{'word': '  Analyze  ', 'levelCandidate': 'B2'}, {'word': 'analyze'}],
                             [{'word': 'look up', 'levelCandidate': None}])
        self.assertEqual(len(rows), 2)
        self.assertTrue(all(r['publicationStatus'] == 'NOT_APPROVED' for r in rows))
        self.assertIn('NO_SOURCE_CEFR_LEVEL', next(r for r in rows if r['type'] == 'phrasal')['reviewFlags'])

    def test_suspicious_variant(self):
        rows = module.triage([{'word': 'analyse/analyze'}], [])
        self.assertIn('VARIANT_OR_ALTERNATIVE_SPELLING', rows[0]['reviewFlags'])
