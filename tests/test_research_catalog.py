import json
import unittest
from pathlib import Path
from tools.build_research_catalog import compile_catalog
ROOT=Path(__file__).resolve().parents[1]
class ResearchCatalogTests(unittest.TestCase):
    def test_fails_on_duplicate_headword(self):
        with self.assertRaisesRegex(ValueError,'duplicate'):
            compile_catalog([{'word':'reliable','levelCandidate':'B2'},{'word':'Reliable','levelCandidate':'B2'}],[],[],[])
    def test_phrasals_are_not_fake_levelled(self):
        rows=compile_catalog([{'word':'credible','levelCandidate':'C1'}],[{'word':'look up','levelCandidate':'B2'}],[],[])
        pv=next(r for r in rows if r['t']=='p')
        self.assertIsNone(pv['l']);self.assertEqual(pv['levels'],[])
    def test_real_generated_catalog_covers_source(self):
        catalog=json.loads((ROOT/'data/candidate-catalog.json').read_text(encoding='utf-8'))
        words=catalog['entries'];vocab=json.loads((ROOT/'sources/b2-c1-offline-catalog.json').read_text(encoding='utf-8'))
        verbs=json.loads((ROOT/'sources/phrasal-candidates.json').read_text(encoding='utf-8'))
        self.assertEqual(len(words),len(vocab)+len(verbs))
        self.assertEqual(len({(x['t'],x['w']) for x in words}),len(words))
        self.assertTrue(all(not x['l'] for x in words if x['t']=='p'))
        self.assertTrue(all(x['l'] in ('B2','C1') for x in words if x['t']=='v'))
        self.assertEqual(catalog['meta']['unreviewed'],len(words))
if __name__=='__main__':unittest.main()
