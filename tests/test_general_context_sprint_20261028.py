"""Regression checks for authentic, sourced October 28 general-context upgrades."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from author_fluency_general_20261028 import records
from author_remaining_focus_headwords_20261028 import make as remaining_focus_records
from complete_general_second_examples_20261028 import SECOND, apply
from promote_content_batch import process, validate_record

class GeneralContextSprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=records()
        cls.vocab=json.loads((ROOT/'data/vocabulary.json').read_text())
        cls.rapid=json.loads((ROOT/'data/rapid-vocabulary.json').read_text())
        cls.focus=json.loads((ROOT/'data/fluency-focus.json').read_text())
        cls.source={x['word']:x['levelCandidate'] for x in json.loads((ROOT/'sources/b2-c1-offline-catalog.json').read_text())}

    def test_145_new_individually_authored_contexts_and_source_levels(self):
        self.assertEqual(len(self.rows),145)
        self.assertEqual(len({x['word'] for x in self.rows}),145)
        selected={x['word']:x['level'] for x in self.focus['vocabulary']}
        for row in self.rows:
            with self.subTest(word=row['word']):
                self.assertIn(row['word'],selected)
                self.assertEqual(self.source[row['word']],selected[row['word']])
                self.assertEqual(len(row['examples']),2)
                self.assertEqual(len(set(row['examples'])),2)
                self.assertGreaterEqual(len(row['definition']),30)
                for example in row['examples']:
                    self.assertGreaterEqual(len(example),25)
                self.assertNotEqual(row.get('editorialStatus'),'approved')

    def test_all_existing_general_have_two_distinct_examples(self):
        general=[x for x in self.vocab if x.get('category')=='general']
        self.assertGreaterEqual(len(general),584)
        self.assertEqual(len({x['id'] for x in general}),len(general))
        self.assertTrue(all(len(x.get('examples',[]))>=2 and
                            len(set(x['examples']))>=2 and
                            x['examples'][0]==x['example'] for x in general))
        self.assertEqual(len([x for x in SECOND.splitlines() if x.strip()]),182)

    def test_rapid_cards_do_not_duplicate_context_lessons(self):
        full={x['word'] for x in self.vocab if x.get('category')=='general'}
        rapid={x['word'] for x in self.rapid}
        self.assertFalse(full & rapid)
        self.assertGreater(len(self.rapid),0)

    def test_focus_status_matches_actual_lessons(self):
        full={x['word']:x for x in self.vocab if x.get('category')=='general'}
        for x in self.focus['vocabulary']:
            if x['status']=='context_draft':
                self.assertIn(x['word'],full)
                self.assertEqual(x['lessonId'],full[x['word']]['id'])
                self.assertNotEqual(full[x['word']].get('editorialStatus'),'approved')
        self.assertEqual(self.focus['meta']['generalBreakdown'],{'context_draft':len(full),'gloss_draft':1000-len(full),'headword_only':0})
        self.assertFalse(self.focus['meta']['publishable'])

    def test_last_seventeen_source_headwords_are_context_drafts(self):
        rows=remaining_focus_records()
        self.assertEqual(len(rows),17)
        focus={x['word']:x for x in self.focus['vocabulary']}
        by_word={x['word']:x for x in self.vocab if x.get('category')=='general'}
        for row in rows:
            with self.subTest(word=row['word']):
                self.assertEqual(self.source[row['word']],'C1')
                self.assertEqual(focus[row['word']]['status'],'context_draft')
                self.assertEqual(len(set(by_word[row['word']]['examples'])),2)
                self.assertNotEqual(by_word[row['word']].get('editorialStatus'),'approved')

    def test_source_catalog_cannot_be_bypassed_by_arbitrary_headword(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for sub in ('data','sources'): (root/sub).mkdir()
            for rel in ('data/vocabulary.json','sources/general-production-queue.json','data/fluency-focus.json','sources/b2-c1-offline-catalog.json'):
                (root/rel).write_text((ROOT/rel).read_text())
            bogus={'word':'inventedimaginaryword','level':'C1','tr':'uydurma','definition':'An invented English definition that sounds plausible.',
                   'example':'This invented word does not really exist in English.',
                   'examples':['This invented word does not really exist in English.','No learner should be taught a fabricated expression.']}
            path=root/'fake.jsonl'
            path.write_text(json.dumps(bogus)+'\n')
            with self.assertRaisesRegex(ValueError,'not present in the sourced production queue'):
                process(path,'general',apply=False,root=root)

    def test_handwritten_second_sentence_updater_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'data').mkdir()
            file=root/'data/vocabulary.json'
            file.write_text((ROOT/'data/vocabulary.json').read_text())
            before=file.read_bytes()
            result=apply(root)
            self.assertEqual(result['fixed'],0)
            self.assertEqual(file.read_bytes(),before)

if __name__=='__main__': unittest.main()
