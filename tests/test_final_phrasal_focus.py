"""500-target milestone: content integrity without fake CEFR or editorial approval."""
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from author_final_phrasal_focus_20261028 import make
from promote_content_batch import validate_record

class FinalPhrasalFocusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=make()
        cls.phrasals=json.loads((ROOT/'data/phrasals.json').read_text(encoding='utf8'))
        cls.focus=json.loads((ROOT/'data/fluency-focus.json').read_text(encoding='utf8'))
        cls.candidates={x['word'] for x in json.loads((ROOT/'sources/phrasal-candidates.json').read_text(encoding='utf8'))}

    def test_seventy_source_grounded_original_drafts(self):
        self.assertEqual(len(self.rows),70)
        self.assertEqual(len({x['word'] for x in self.rows}),70)
        for row in self.rows:
            with self.subTest(row=row['word']):
                self.assertEqual(validate_record(row,'phrasal',self.candidates),row['word'])
                self.assertNotEqual(row['examples'][0],row['examples'][1])
                self.assertEqual(row['levelStatus'],'editorial_estimate_unverified')

    def test_all_five_hundred_are_real_lessons_with_unique_ids(self):
        self.assertEqual(len(self.phrasals),500)
        by_word={x['word']:x for x in self.phrasals}
        self.assertEqual(len(by_word),500)
        self.assertEqual(len({x['id'] for x in self.phrasals}),500)
        self.assertEqual(len(self.focus['phrasals']),500)
        for row in self.focus['phrasals']:
            lesson=by_word[row['word']]
            self.assertEqual(row['status'],'context_draft')
            self.assertEqual(row['lessonId'],lesson['id'])
            self.assertEqual(len(lesson['examples']),2)
            self.assertTrue(lesson.get('definition'))
            self.assertNotEqual(lesson.get('editorialStatus'),'approved')
            self.assertFalse(row['editorialApproved'])

    def test_low_value_padded_phrases_not_in_focus(self):
        words={x['word'] for x in self.focus['phrasals']}
        self.assertTrue({'brush up','jot down','log in','mess up','boil down'}.issubset(words))
        self.assertFalse({'belly out','go to','come near','look at','beat out'}.intersection(words))

    def test_no_pretend_human_review_or_accurate_cefr_verification(self):
        for row in self.rows:
            self.assertNotIn('approved',row)
            self.assertIn('Provisional',row['levelEvidence'])
        self.assertFalse(self.focus['meta']['publishable'])

if __name__=='__main__':unittest.main()
