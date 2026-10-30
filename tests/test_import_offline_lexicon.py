import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('import_offline_lexicon', ROOT / 'tools' / 'import_offline_lexicon.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class OfflineImportTests(unittest.TestCase):
    def test_us_spellings(self):
        self.assertEqual(module.americanize('organize/organise')[0], 'organize')
        self.assertEqual(module.americanize('color/colour')[0], 'color')
        self.assertEqual(module.americanize(' harbor/harbour ')[0], 'harbor')

    def test_reject_uk_only_or_sensitive(self):
        self.assertEqual(module.americanize('aubergine')[1], 'uk_specific')
        self.assertEqual(module.americanize('gook')[1], 'requires_sensitivity_review')

    def test_reject_malformed_slash_form(self):
        self.assertEqual(module.americanize('a/b/c')[1], 'ambiguous_variant')

    def test_catalog_structure_and_level_labels(self):
        rows = json.loads((ROOT/'sources/b2-c1-offline-catalog.json').read_text(encoding='utf-8'))
        keys = [r['word'].casefold() for r in rows]
        self.assertEqual(len(keys),len(set(keys)))
        self.assertGreaterEqual(len(keys),3500)
        self.assertTrue(all(set(r['candidateLevels']) <= {'B2','C1'} for r in rows))
        self.assertTrue(all(r['status']=='HEADWORD_CANDIDATE_ONLY' for r in rows))
        self.assertTrue(all(r['meaningReviewed'] is False for r in rows))

    def test_release_stays_locked(self):
        result = json.loads((ROOT/'qa/offline-catalog-report.json').read_text(encoding='utf-8'))
        self.assertFalse(result['publication_allowed'])
        self.assertEqual(result['new_verified_teaching_cards'],0)

if __name__=='__main__':unittest.main()
