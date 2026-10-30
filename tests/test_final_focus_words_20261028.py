"""Ensure all 238 draft lessons are sourced, unique, and never auto-approved."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from author_final_focus_words_20261028 import make_rows
from promote_content_batch import validate_record

class FinalFocusLessons(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=make_rows()
        cls.lessons={x['word']:x for x in json.loads((ROOT/'data/vocabulary.json').read_text()) if x['category']=='general'}
        cls.archive={x['word']:x for x in json.loads((ROOT/'data/archived-vocabulary.json').read_text())} if (ROOT/'data/archived-vocabulary.json').exists() else {}
        cls.focus=json.loads((ROOT/'data/fluency-focus.json').read_text())
        cls.catalog={x['word']:x for x in json.loads((ROOT/'sources/b2-c1-offline-catalog.json').read_text())}

    def test_full_focus_reaches_1000_without_claiming_approval(self):
        v=self.focus['vocabulary']
        self.assertEqual(len(v),1000)
        self.assertEqual(sum(x['level']=='B2' for x in v),500)
        self.assertEqual(sum(x['level']=='C1' for x in v),500)
        self.assertEqual(sum(x['status']=='context_draft' for x in v),1000)
        self.assertFalse(any(x['editorialApproved'] for x in v))
        self.assertFalse(self.focus['meta']['publishable'])

    def test_last_238_are_two_distinct_original_contexts(self):
        self.assertEqual(len(self.rows),238)
        self.assertEqual(len({x['word'] for x in self.rows}),238)
        for row in self.rows:
            with self.subTest(word=row['word']):
                lesson=self.lessons.get(row['word']) or self.archive[row['word']]
                self.assertEqual(row['level'],self.catalog[row['word']]['levelCandidate'])
                self.assertEqual(row['level'],lesson['level'])
                self.assertEqual(row['examples'],lesson['examples'])
                self.assertEqual(lesson['editorialStatus'],'authored_unreviewed')
                self.assertFalse(lesson['meaningReviewed'])
                self.assertFalse(lesson['exampleReviewed'])
                self.assertEqual(len(set(lesson['examples'])),2)
                self.assertTrue(all(x.endswith(('.', '!', '?')) and len(x)>=25 for x in lesson['examples']))

    def test_import_idempotence_and_provenance(self):
        data=json.loads((ROOT/'data/vocabulary.json').read_text())
        full=[x for x in data if x['category']=='general']
        self.assertEqual(len(full),len({x['word'] for x in full}))
        focused={x['word'] for x in self.focus['vocabulary']}
        self.assertEqual(focused,set(self.lessons))
        rapid=json.loads((ROOT/'data/rapid-vocabulary.json').read_text())
        self.assertFalse(focused.intersection(x['word'] for x in rapid))
        self.assertEqual(len(rapid),399)
        source=[json.loads(s) for s in (ROOT/'sources/authored-20261028-final-focus-238.jsonl').read_text().splitlines()]
        self.assertEqual(source,self.rows)

if __name__=='__main__':unittest.main()
