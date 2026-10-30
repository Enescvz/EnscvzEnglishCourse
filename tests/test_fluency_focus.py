"""Focused learning targets are deterministic and never conflate headwords with lessons."""
import json
import pathlib
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]

class FocusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.focus=json.loads((ROOT/'data/fluency-focus.json').read_text(encoding='utf8'))
        cls.vocab=json.loads((ROOT/'data/vocabulary.json').read_text(encoding='utf8'))
        cls.phrasals=json.loads((ROOT/'data/phrasals.json').read_text(encoding='utf8'))

    def test_exact_targets_and_disjoint_levels(self):
        v=self.focus['vocabulary']; p=self.focus['phrasals']
        self.assertEqual(len(v),1000);self.assertEqual(len(p),500)
        self.assertEqual(len({x['word'].lower() for x in v}),1000)
        self.assertEqual(len({x['word'].lower() for x in p}),500)
        self.assertEqual(sum(x['level']=='B2' for x in v),500)
        self.assertEqual(sum(x['level']=='C1' for x in v),500)
        self.assertTrue(all(not x['editorialApproved'] for x in v+p))

    def test_context_entries_are_real_content_ids(self):
        gen={x['id']:x for x in self.vocab if x['category']=='general'}
        phrasals={x['id']:x for x in self.phrasals}
        for row in self.focus['vocabulary']:
            if row['status']=='context_draft':
                self.assertEqual(row['word'],gen[row['lessonId']]['word'].lower())
            elif row['status']=='gloss_draft':self.assertTrue(row.get('rapidId'))
            else:self.assertEqual(row['status'],'headword_only')
        for row in self.focus['phrasals']:
            if row['status']=='context_draft':self.assertEqual(row['word'],phrasals[row['lessonId']]['word'].lower())
            else:self.assertEqual(row['status'],'headword_only')

    def test_c1_source_sense_false_positives_are_not_promoted_to_c1_targets(self):
        c1={x['word'] for x in self.focus['vocabulary'] if x['level']=='C1'}
        self.assertFalse({'man','house','behind'}.intersection(c1))

    def test_locked_until_complete_and_editorial_review(self):
        self.assertFalse(self.focus['meta']['publishable'])
        self.assertEqual(self.focus['meta']['generalBreakdown']['context_draft'],sum(x['status']=='context_draft' for x in self.focus['vocabulary']))
        self.assertEqual(self.focus['meta']['generalBreakdown']['context_draft'],1000)
        self.assertEqual(self.focus['meta']['generalBreakdown']['gloss_draft'],0)
        self.assertEqual(self.focus['meta']['phrasalBreakdown']['context_draft'],sum(x['status']=='context_draft' for x in self.focus['phrasals']))
        self.assertEqual(self.focus['meta']['phrasalBreakdown']['context_draft'],500)
        self.assertTrue(all(not x['editorialApproved'] for x in self.focus['phrasals']))
        self.assertTrue(all(x.get('editorialStatus') != 'approved' for x in self.phrasals))

if __name__=='__main__':unittest.main()
