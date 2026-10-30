import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('import_offline_phrasals',
    Path(__file__).resolve().parents[1] / 'tools/import_offline_phrasals.py')
imp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(imp)

class OfflinePhrasalTests(unittest.TestCase):
    def test_decode_known_prefix_sequences(self):
        self.assertEqual(imp.decode_headwords('0back down|5off|5up'),
                         ['back down','back off','back up'])

    def test_duplicate_or_unsorted_input_rejected(self):
        with self.assertRaises(ValueError):
            imp.decode_headwords('0back down|0abide by')
        with self.assertRaises(ValueError):
            imp.decode_headwords('0back down|az')

    def test_1204_real_source_headwords_staged(self):
        report = imp.stage()
        self.assertEqual(report['sourceHeadwords'],1204)
        self.assertEqual(report['distinctSourceHeadwords'],1204)
        self.assertGreater(report['newHeadwordCandidates'],600)
        self.assertFalse(report['releaseReady'])
        self.assertEqual(report['newVerifiedTeachingCards'],0)

    def test_all_source_entries_protected_against_auto_approval(self):
        import json
        catalog=json.loads(imp.OUTPUT.read_text(encoding='utf8'))
        self.assertTrue(all(r['notSuitableForPublication'] for r in catalog))
        self.assertTrue(all(r['levelCandidate'] is None for r in catalog))
        self.assertIn('figure out',{p['word'] for p in catalog})
        self.assertIn('back down',{p['word'] for p in catalog})

if __name__ == '__main__': unittest.main()
