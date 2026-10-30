"""Check expansion batches without pretending to certify CEFR or semantic correctness."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from expand_phrasals_v2 import parse as new_phrasals
from expand_listening import EPISODES,DRILLS

class ExpansionTests(unittest.TestCase):
 def test_curated_phrasals_have_unique_senses_and_two_examples(self):
  authored=new_phrasals()
  current={p['word']:p for p in json.loads((ROOT/'data/phrasals.json').read_text(encoding='utf8'))}
  self.assertEqual(len(authored),65)
  self.assertEqual(len({x['word'] for x in authored}),len(authored))
  added=0
  for p in authored:
   self.assertIn(p['word'],current)
   live=current[p['word']]
   self.assertEqual(live['editorialStatus'],'authored_unreviewed')
   if live['definition']==p['definition']:
    added+=1
    self.assertEqual(live['tr'],p['tr'])
    self.assertTrue(len(live.get('examples',[]))>=2)
   else:
    # An existing, independently authored entry has a different taught sense.
    self.assertGreater(len(live['definition']),25)
  self.assertEqual(added,60)

 def test_new_podcasts_and_drills_are_real_distinct_scripts(self):
  episodes={x['id']:x for x in json.loads((ROOT/'data/episodes.json').read_text())}
  drills={x['id']:x for x in json.loads((ROOT/'data/drills.json').read_text())}
  self.assertEqual(len({x['id'] for x in EPISODES}),6)
  self.assertEqual(len({x[0] for x in DRILLS}),12)
  for author in EPISODES:
   live=episodes[author['id']]
   self.assertEqual(len(live['turns']),10)
   self.assertEqual(len(live['questions']),3)
   self.assertEqual(len(live['turns']),len(live['timings']))
   self.assertEqual(live['audioType'],'synthetic')
   self.assertEqual(live['editorialStatus'],'authored_unreviewed')
   self.assertFalse((ROOT/live['audio']).exists(),'Unapproved robotic audio must not ship')
  for slug,*_ in DRILLS:
   live=drills[slug]
   self.assertEqual(live['audioType'],'synthetic')
   self.assertFalse((ROOT/live['audio']).exists(),'Unapproved robotic audio must not ship')

if __name__=='__main__':unittest.main()
