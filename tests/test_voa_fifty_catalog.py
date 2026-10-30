"""VOA 50-source catalog must not overstate readiness or pretend files are local."""
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]

class VOA50CatalogTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.catalog=json.loads((ROOT/'data/voa-source-catalog.json').read_text(encoding='utf8'))
  cls.ready=json.loads((ROOT/'data/authentic-listening.json').read_text(encoding='utf8'))
  cls.linked=json.loads((ROOT/'data/voa-source-quizzes.json').read_text(encoding='utf8'))
  cls.app=(ROOT/'js/app.js').read_text(encoding='utf8')
  cls.sw=(ROOT/'sw.js').read_text(encoding='utf8')

 def test_exactly_fifty_unique_official_voa_pages(self):
  self.assertEqual(len(self.catalog),50)
  self.assertEqual(len({x['sourceUrl'] for x in self.catalog}),50)
  self.assertEqual(len({x['id'] for x in self.catalog}),50)
  for x in self.catalog:
   self.assertEqual(urlparse(x['sourceUrl']).hostname,'learningenglish.voanews.com')
   self.assertTrue(x['sourceUrl'].startswith('https://learningenglish.voanews.com/a/'))
   self.assertTrue(x['title'] and x['topic'])
   self.assertEqual(x['sourcePublisher'],'VOA Learning English')
   self.assertEqual(x['audioBundled'],False)
   self.assertEqual(x['speakingType'],'human_spoken_scripted_dialogue')

 def test_thirty_intermediate_twenty_warmups(self):
  self.assertEqual(sum(x['levelGroup']=='Level 2' for x in self.catalog),30)
  self.assertEqual(sum(x['levelGroup']=='Level 1' for x in self.catalog),20)
  self.assertTrue(all(x['educationalRole']=='optional_listening_warmup' for x in self.catalog if x['levelGroup']=='Level 1'))

 def test_twelve_transcripts_and_thirtyeight_linked_quizzes(self):
  ready={x['id']:x for x in self.ready}
  linked={x['id']:x for x in self.linked}
  self.assertEqual(len(ready),30)
  self.assertEqual(len(linked),20)
  self.assertEqual(sum(x['transcriptImported'] for x in self.catalog),30)
  self.assertEqual(sum(x['integrationStatus']=='source_linked_quiz' for x in self.catalog),20)
  self.assertEqual(sum(x['integrationStatus']=='publisher_source_only' for x in self.catalog),0)
  for x in self.catalog:
   if x['transcriptImported']:
    self.assertIn(x['interactiveLessonId'],ready)
    self.assertEqual(x['sourceUrl'],ready[x['interactiveLessonId']]['sourceUrl'])
    self.assertEqual(x['questionCount'],len(ready[x['interactiveLessonId']]['questions']))
   elif x.get('linkedQuizId'):
    self.assertIsNone(x['interactiveLessonId'])
    self.assertIn(x['linkedQuizId'],linked)
    self.assertEqual(x['sourceUrl'],linked[x['linkedQuizId']]['sourceUrl'])
    self.assertEqual(x['questionCount'],len(linked[x['linkedQuizId']]['questions']))
    self.assertFalse(linked[x['linkedQuizId']]['transcriptImported'])
    self.assertFalse(linked[x['linkedQuizId']]['audioBundled'])
   else:
    self.assertIsNone(x['interactiveLessonId'])
    self.assertEqual(x['questionCount'],0)

 def test_progress_cannot_be_faked_by_catalog(self):
  self.assertIn('50 ücretsiz VOA kaynağı',self.app)  # Source library; not a fabricated playback count
  self.assertIn('Uygulama soruları henüz hazırlanmadı',self.app)
  self.assertIn("voaCatalog:'voa-source-catalog'",(ROOT/'js/content-loader.js').read_text(encoding='utf-8'))
  self.assertIn("'./data/voa-source-catalog.json'",self.sw)
  self.assertNotIn('publisher_source_only',json.dumps(self.catalog))
  self.assertNotIn('50 yeni podcast',self.app)

if __name__=='__main__':unittest.main()
