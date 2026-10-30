import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('rapid_gloss_import',ROOT/'tools/rapid_gloss_import.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class RapidDeckTests(unittest.TestCase):
    def test_imported_glosses_are_distinct_and_unreviewed(self):
        cards=json.loads((ROOT/'data/rapid-vocabulary.json').read_text(encoding='utf-8'))
        taught={x['word'].casefold() for x in json.loads((ROOT/'data/vocabulary.json').read_text()) if x.get('category')=='general'}
        words=[x['word'].casefold() for x in cards]
        self.assertGreater(len(cards),0)  # Number decreases as quick cards become contextual lessons
        self.assertEqual(len(words),len(set(words)))
        self.assertFalse(taught.intersection(words))
        for c in cards:
            self.assertIn(c['level'],('B2','C1'))
            self.assertEqual(c['teachingDepth'],'gloss_only')
            self.assertFalse(c['meaningReviewed'])
            self.assertFalse(c['exampleReviewed'])
            self.assertTrue(c['tr'].strip())
            self.assertEqual(c['editorialStatus'],'unreviewed')
    def test_upstream_json_only_import_can_run_without_tsv(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'C1.json'
            path.write_text(json.dumps({'words':[{'w':'abound','tr':'bol olmak'}]}),encoding='utf8')
            source=Path(tmp)/'not-present.tsv'
            result=mod.main(source,apply=False,upstream=[path])
            self.assertEqual(result['sourceRows'],1)
            self.assertEqual(result['newRapidCards'],1)
            self.assertFalse(result['releaseReady'])
    def test_pwa_includes_rapid_module_and_cards(self):
        js=(ROOT/'sw.js').read_text()
        self.assertIn("'./js/rapid.js'",js)
        self.assertIn("'./data/rapid-vocabulary.json'",js)
if __name__=='__main__':unittest.main()
