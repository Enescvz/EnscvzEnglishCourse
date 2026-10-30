"""TOEFL + Daily core integrity and legacy progress safeguards."""
import json
import tempfile
import unittest
from pathlib import Path
from tools.curate_toefl_core_20261028 import compile_core
ROOT=Path(__file__).resolve().parents[1]

class TOEFLDailyCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extra=json.loads((ROOT/'data/toefl-academic.json').read_text(encoding='utf8'))
        cls.core=json.loads((ROOT/'data/toefl-core.json').read_text(encoding='utf8'))
        cls.vocab=json.loads((ROOT/'data/vocabulary.json').read_text(encoding='utf8'))
        cls.phrasals=json.loads((ROOT/'data/phrasals.json').read_text(encoding='utf8'))
    def test_counts_links_and_no_duplicate_ids(self):
        self.assertEqual(len(self.extra),50)
        self.assertEqual(len(self.core['wordLessonIds']),400)
        self.assertEqual(len(self.core['phrasalLessonIds']),75)
        ids=[x['id'] for x in self.vocab+self.extra+self.phrasals]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len({x['word'].lower() for x in self.vocab+self.extra}),len(self.vocab+self.extra))
        self.assertTrue(set(self.core['wordLessonIds']).issubset({x['id'] for x in self.vocab+self.extra}))
        self.assertTrue(set(self.core['phrasalLessonIds']).issubset({x['id'] for x in self.phrasals}))
        self.assertEqual(len([x for x in self.vocab if x['category']=='general']),1000)
        self.assertEqual(len([x for x in self.vocab if x['category'] in ('finance','accounting')]),284)
    def test_original_core_prefix_and_existing_context_immutability(self):
        original=json.loads((ROOT/'sources/toefl-core-original-200-50-20261028.json').read_text(encoding='utf8'))
        self.assertEqual(self.core['wordLessonIds'][:200],original['wordLessonIds'])
        self.assertEqual(self.core['phrasalLessonIds'][:50],original['phrasalLessonIds'])
        self.assertEqual(len(set(self.core['wordLessonIds'])),400)
        self.assertEqual(len(set(self.core['phrasalLessonIds'])),75)
        self.assertEqual(len(set(self.core['wordLessonIds'][200:])&set(original['wordLessonIds'])),0)
        self.assertEqual(len(set(self.core['phrasalLessonIds'][50:])&set(original['phrasalLessonIds'])),0)
        by_id={z['id']:z for z in self.vocab}
        for identifier in self.core['wordLessonIds'][200:]:
            card=by_id[identifier]
            self.assertEqual(card['category'],'general')
            self.assertEqual(len(card['examples']),2)
            self.assertNotEqual(card['examples'][0],card['examples'][1])
        self.assertIs(self.core['meta']['officialTOEFLFrequencyRanking'],False)

    def test_source_context_and_non_approval(self):
        for x in self.extra:
            with self.subTest(word=x['word']):
                self.assertEqual(x['editorialStatus'],'authored_unreviewed')
                self.assertEqual(x['category'],'toeflAcademic')
                self.assertEqual(x['examples'][0],x['example'])
                self.assertEqual(len(x['examples']),len(set(x['examples'])))
                self.assertTrue(all(len(z)>25 for z in [x['definition'],*x['examples']]))
        self.assertIs(self.core['meta']['officialTOEFLFrequencyRanking'],False)
        self.assertIs(self.core['meta']['editorialSignoffComplete'],False)
    def test_generation_repeatable(self):
        extra,core,report=compile_core()
        self.assertEqual(extra,self.extra)
        self.assertEqual(core,self.core)
        self.assertEqual(report,json.loads((ROOT/'qa/toefl-core-report.json').read_text(encoding='utf8')))
    def test_offline_core_assets_cacheable(self):
        sw=(ROOT/'sw.js').read_text()
        self.assertIn('./data/toefl-academic.json',sw)
        self.assertIn('./data/toefl-core.json',sw)
        self.assertRegex(sw,r"const CACHE='ael-dev-202610[0-9]{2}-")
        self.assertIn('./data/authentic-listening.json',sw)

if __name__=='__main__':unittest.main()
