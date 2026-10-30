"""Regression safety net for original, text-grounded daily-English reading/grammar."""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class QualityReadingGrammarTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.readings=json.loads((ROOT/'data/readings.json').read_text(encoding='utf8'))
  cls.grammar=json.loads((ROOT/'data/grammar.json').read_text(encoding='utf8'))

 def test_thirty_unique_readings_with_source_specific_choices(self):
  self.assertEqual(len(self.readings),30)
  self.assertEqual(len({x['id'] for x in self.readings}),30)
  for x in self.readings:
   self.assertGreaterEqual(len(x['body'].split()),90,x['id'])
   self.assertIn(x['level'],('B2','C1'))
   self.assertEqual(len(x['questions']),5)
   for q in x['questions']:
    self.assertIn(q['answer'],range(4))
    self.assertEqual(len(q['options']),4)
    self.assertEqual(len(set(q['options'])),4)
    self.assertGreaterEqual(len(q['explanation']),25)
    self.assertNotIn('A completely unrelated technical requirement',q['options'])
    self.assertNotIn('The passage does not provide that explanation',q['options'])
    self.assertTrue(q['question'].strip().endswith('?'))

 def test_twenty_unique_grammar_items(self):
  self.assertEqual(len(self.grammar),20)
  self.assertEqual(len({x['id'] for x in self.grammar}),20)
  for x in self.grammar:
   self.assertIn(x['level'],('B2','C1'))
   self.assertEqual(len(x['options']),4)
   self.assertEqual(len(set(x['options'])),4)
   self.assertIn(x.get('answerIndex',0),range(4))
   self.assertEqual(x['answer'],x['options'][x.get('answerIndex',0)])
   self.assertTrue(x['example'] and x['question'] and x['explanation'])

 def test_new_lessons_are_tied_to_everyday_topics(self):
  ids={x['id'] for x in self.readings}
  self.assertTrue({'the-last-minute-change','the-rent-discussion','the-subscription-trap','an-imperfect-apology','the-faulty-metric'}.issubset(ids))
  grammar_ids={x['id'] for x in self.grammar}
  self.assertTrue({'reported-questions','used-to-and-be-used-to','future-perfect','wish-past-perfect-regret'}.issubset(grammar_ids))

 def test_no_word_for_word_repeated_new_passages(self):
  bodies=[x['body'].strip().lower() for x in self.readings]
  self.assertEqual(len(set(bodies)),len(bodies))
  self.assertEqual(len({q['question'] for x in self.readings for q in x['questions']}),150)

if __name__=='__main__':unittest.main()
