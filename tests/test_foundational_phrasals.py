"""Foundation-first phrasals must not inflate verified B2 learning."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class FoundationalPhrasalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.focus=json.loads((ROOT/'data/fluency-focus.json').read_text())
        cls.lessons=json.loads((ROOT/'data/phrasals.json').read_text())
    def test_foundation_count_and_ids_preserved(self):
        focus={x['word']:x for x in self.focus['phrasals']}
        lessons={x['word']:x for x in self.lessons}
        self.assertEqual(len(focus),500)
        self.assertEqual(len(lessons),500)
        flagged={w for w,x in focus.items() if x.get('placementCheckFirst')}
        self.assertEqual(len(flagged),13)
        for w in flagged:
            self.assertEqual(focus[w]['level'],'B1')
            self.assertEqual(lessons[w]['level'],'B1')
            self.assertEqual(focus[w]['lessonId'],lessons[w]['id'])
            self.assertFalse(focus[w]['cefrVerified'])
            self.assertFalse(focus[w]['editorialApproved'])
        self.assertEqual(self.focus['meta']['foundationalPhrasalsPlacementFirst'],13)
    def test_other_phrasal_levels_untouched(self):
        self.assertEqual(sum(x.get('placementCheckFirst') is not True for x in self.focus['phrasals']),487)
        self.assertFalse(self.focus['meta']['publishable'])

if __name__=='__main__':unittest.main()
