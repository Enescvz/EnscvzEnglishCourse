import unittest, json, re
from pathlib import Path
P=Path(__file__).resolve().parents[1]
DATA=json.loads((P/'data/daily-expressions.json').read_text())
class DailyExpressions300Tests(unittest.TestCase):
 def test_counts(self):
  by={level:[x for x in DATA['cards'] if x['level']==level] for level in ['B1','B2','C1']}
  self.assertEqual({k:len(v) for k,v in by.items()},{'B1':150,'B2':210,'C1':140})
  self.assertEqual(DATA['meta']['targetTotal'],500)
 def test_stable_ids(self):
  ids=[x['id'] for x in DATA['cards']]
  self.assertEqual(len(set(ids)),500)
  for level,total in [('b1',150),('b2',210),('c1',140)]:
   self.assertEqual([x['id'] for x in DATA['cards'] if x['level'].lower()==level],[f'ex-{level}-{i:03}' for i in range(1,total+1)])
 def test_unique_text_and_nonempty_context(self):
  normalized=[re.sub('[^a-z0-9]','',x['expression'].lower()) for x in DATA['cards']]
  self.assertEqual(len(set(normalized)),500)
  for x in DATA['cards']:
   with self.subTest(x=x['id']):
    self.assertGreaterEqual(len(x['tr']),4)
    self.assertGreaterEqual(len(x['usageNote']),20)
    self.assertEqual(len(x['examples']),2)
    self.assertNotEqual(*[a.lower() for a in x['examples']])
    self.assertEqual([r['speaker'] for r in x['dialogue']],['A','B'])
    self.assertTrue(all(len(r['text'])>6 for r in x['dialogue']))
 def test_claims_stay_pending(self):
  self.assertFalse(DATA['meta']['independentEditorApproved'])
  self.assertEqual(DATA['meta']['approvedHumanVoiceCount'],0)
  for x in DATA['cards']:
   self.assertEqual(x['editorialStatus'],'authored_pending_independent_review')
   self.assertEqual(x['audioStatus'],'not_provided')
 def test_legacy_b1_unmodified(self):
  self.assertEqual(DATA['cards'][0]['expression'],'Keep you warm')
  self.assertEqual(DATA['cards'][99]['expression'],'I owe you one')
 def test_status_matches_content(self):
  d=json.loads((P/'development-status.json').read_text())['dailyExpressions']
  self.assertEqual(d['authored'],len(DATA['cards']))
  self.assertEqual(d['authoredByLevel'],{'B1':150,'B2':210,'C1':140})
if __name__=='__main__':unittest.main()
