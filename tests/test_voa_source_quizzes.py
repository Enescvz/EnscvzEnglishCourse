"""Contract tests for questions created from VOA-published conversation scripts."""
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
class LinkedVOAQuestionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.quizzes=json.loads((ROOT/'data/voa-source-quizzes.json').read_text(encoding='utf-8'))
  cls.catalog=json.loads((ROOT/'data/voa-source-catalog.json').read_text(encoding='utf-8'))
  cls.imported=json.loads((ROOT/'data/authentic-listening.json').read_text(encoding='utf-8'))
  cls.app=(ROOT/'js/app.js').read_text(encoding='utf-8')
 def test_remaining_source_linked_lessons(self):
  self.assertEqual(len(self.quizzes),20)
  self.assertEqual(len({q['id'] for q in self.quizzes}),20)
  for q in self.quizzes:
   self.assertEqual(urlparse(q['sourceUrl']).hostname,'learningenglish.voanews.com')
   self.assertFalse(q['audioBundled'])
   self.assertFalse(q['transcriptImported'])
   self.assertFalse(q['playerVerified'])
   self.assertEqual(q['audioAvailability'],'publisher_external_only')
   self.assertEqual(q['transcriptAvailability'],'publisher_external_only')
 def test_all_linked_quiz_answers_are_structurally_valid(self):
  self.assertEqual(sum(len(q['questions']) for q in self.quizzes),80)
  for q in self.quizzes:
   self.assertEqual(len(q['questions']),4)
   for question in q['questions']:
    self.assertTrue(question['question'].endswith('?'))
    self.assertEqual(len(question['options']),4)
    self.assertEqual(len(set(question['options'])),4)
    self.assertIn(question['answer'],range(4))
    self.assertGreaterEqual(len(question['explanation']),25)
    if q.get('questionEvidenceOnly'):
     self.assertEqual(question['sourceEvidencePublisherUrl'],q['sourceUrl'])
     self.assertIn(question['sourceEvidenceKind'],('speech','stage_direction'))
     self.assertFalse(question.get('sourceEvidenceTurn'))
    else:
     self.assertEqual(question['sourceEvidence'],'VOA publisher Conversation transcript (see linked original)')
 def test_catalog_links_are_lossless_and_existing_three_remain(self):
  by_id={x['id']:x for x in self.catalog}
  for q in self.quizzes:
   x=by_id[q['catalogId']]
   self.assertEqual(x['linkedQuizId'],q['id'])
   self.assertEqual(x['sourceUrl'],q['sourceUrl'])
   self.assertEqual(x['questionCount'],len(q['questions']))
   self.assertFalse(x['audioBundled'])
  self.assertEqual(len(self.imported),30)
  self.assertEqual(sum(len(x['questions']) for x in self.imported),124)
 def test_player_is_not_invented_for_publisher_only_quizzes(self):
  self.assertIn('VOA sayfasında metni gizleyerek dinle',self.app)
  self.assertIn('linkedQuizOpen',self.app)
  self.assertIn('linkedQuizFinish',self.app)
  self.assertIn("voaLinkedQuizzes:'voa-source-quizzes'",(ROOT/'js/content-loader.js').read_text(encoding='utf-8'))
  self.assertIn('audioPlaybackSelfReported:true',self.app)
  self.assertIn('voaListenedConfirm',self.app)
  self.assertIn('if(!ui.linkedListened)',self.app)
  self.assertIn('audioPlaybackVerified:false',self.app)
 def test_import_is_deterministic(self):
  # Re-running generation must not duplicate catalog entries/quiz IDs.
  self.assertEqual(len({x['catalogId'] for x in self.quizzes}),len(self.quizzes))
  self.assertEqual(len({x['sourceUrl'] for x in self.quizzes}),len(self.quizzes))
if __name__=='__main__': unittest.main()
