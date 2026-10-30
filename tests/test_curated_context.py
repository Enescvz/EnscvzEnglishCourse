"""Independent checks on original context additions; no claim of semantic review."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from curated_context_batch import parse,GENERAL,PHRASALS

class CuratedContextTests(unittest.TestCase):
 def test_150_original_sentences_present_and_distinct(self):
  total=0
  for name,records in [('vocabulary',GENERAL),('phrasals',PHRASALS)]:
   data={x['word']:x for x in json.loads((ROOT/'data'/f'{name}.json').read_text())}
   entries=parse(records)
   self.assertEqual(len(entries),75)
   for word,sentence in entries.items():
    self.assertIn(word,data)
    self.assertIn(sentence,data[word]['examples'])
    self.assertNotEqual(sentence,data[word]['example'])
    self.assertEqual(data[word]['examples'].count(sentence),1)
    self.assertGreaterEqual(len(data[word]['examples']),2)
    total+=1
  self.assertEqual(total,150)
 def test_original_sentences_not_copy_pasted(self):
  all_sentences=list(parse(GENERAL).values())+list(parse(PHRASALS).values())
  self.assertEqual(len(set(all_sentences)),150)
  self.assertTrue(all(len(s.split())>=8 for s in all_sentences))
  self.assertTrue(all(s[-1] in '.!?' for s in all_sentences))

if __name__=='__main__':unittest.main()
