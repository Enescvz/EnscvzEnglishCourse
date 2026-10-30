"""Offline provenance and integrity checks for the high-utility phrasal draft batch."""
import json
import pathlib
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from author_useful_phrasals_20261028 import make
from promote_content_batch import validate_record

class UsefulPhrasalBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch=make()
        cls.bank=json.loads((ROOT/'data/phrasals.json').read_text(encoding='utf8'))
        cls.focus=json.loads((ROOT/'data/fluency-focus.json').read_text(encoding='utf8'))
        cls.provenance={x['word'] for x in json.loads((ROOT/'sources/phrasal-candidates.json').read_text(encoding='utf8'))}

    def test_all_authored_phrases_exist_in_traceable_source(self):
        self.assertEqual(len(self.batch),112)
        self.assertTrue(all(x['word'] in self.provenance for x in self.batch))

    def test_all_context_examples_are_two_distinct_original_complete_sentences(self):
        for row in self.batch:
            with self.subTest(word=row['word']):
                self.assertEqual(validate_record(row,'phrasal',set(self.provenance)),row['word'])
                self.assertNotEqual(row['examples'][0],row['examples'][1])
                self.assertGreaterEqual(len(row['examples'][0].split()),6)
                self.assertGreaterEqual(len(row['examples'][1].split()),6)

    def test_each_batch_phrase_has_one_unapproved_lesson_not_duplicates(self):
        by_word={}
        for lesson in self.bank:by_word.setdefault(lesson['word'],[]).append(lesson)
        for row in self.batch:
            with self.subTest(word=row['word']):
                self.assertEqual(len(by_word.get(row['word'],[])),1)
                self.assertNotEqual(by_word[row['word']][0].get('editorialStatus'),'approved')

    def test_focus_labels_new_drafts_without_falsely_approving_them(self):
        focus={x['word']:x for x in self.focus['phrasals']}
        for row in self.batch:
            with self.subTest(word=row['word']):
                self.assertEqual(focus[row['word']]['status'],'context_draft')
                self.assertFalse(focus[row['word']]['editorialApproved'])
        self.assertEqual(self.focus['meta']['phrasalBreakdown']['context_draft'],len(self.bank))

if __name__=='__main__':unittest.main()
