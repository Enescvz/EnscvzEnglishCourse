import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SentenceSkillCorpusTests(unittest.TestCase):
 def setUp(self):self.data=json.loads((ROOT/'data/sentence-skills.json').read_text())
 def test_counts(self):
  lessons=self.data['lessons'];self.assertEqual(len(lessons),34)
  self.assertEqual(sum(len(x['exercises']) for x in lessons),340)
  self.assertEqual({x:len([l for l in lessons if l['area']==x]) for x in ('question','preposition','connector','sentence')},{'question':12,'preposition':10,'connector':8,'sentence':4})
 def test_editor_and_id_integrity(self):
  ids=[];answers=[]
  for lesson in self.data['lessons']:
   for ex in lesson['exercises']:
    ids.append(ex['id']);answers.append(ex['modelAnswer'].casefold())
    self.assertFalse(ex['independentEditorApproved'])
  self.assertEqual(len(ids),len(set(ids)));self.assertEqual(len(answers),len(set(answers)))
  self.assertFalse(self.data['meta']['independentEditorApproved'])
 def test_cache_and_non_speaking_integration(self):
  sw=(ROOT/'sw.js').read_text();self.assertIn("'./data/sentence-skills.json'",sw);self.assertIn("'./js/sentence-skills.js'",sw)
  self.assertIn("['sentenceSkills'",(ROOT/'js/app.js').read_text())
if __name__=='__main__':unittest.main()
