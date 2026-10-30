import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from import_voa_level1_33_42 import parse_publisher_html,stage_one,IDS
class TestSourceImport(unittest.TestCase):
 def test_ten_target_identifiers_are_unique_and_l1(self):
  self.assertEqual(len(IDS),10)
  self.assertEqual(len(set(IDS)),10)
  self.assertEqual(IDS[0],'voa-1-33')
  self.assertEqual(IDS[-1],'voa-1-42')
 def test_import_requires_real_conversation_and_minimum_text(self):
  with self.assertRaises(ValueError):parse_publisher_html('<h2>Speaking</h2><p>Anna: Hi.</p>')
  with self.assertRaises(ValueError):parse_publisher_html('<h2>Conversation</h2><p>Anna: Hi.</p><h2>Quiz</h2>')
 def test_valid_fixture_is_staged_not_audio_approved(self):
  body=' '.join(['We are practicing a complete sentence with useful original context.']*3)
  html='<h2>Conversation</h2>'+''.join(f'<p>Anna: {body}</p>' for _ in range(12))+'<h2>Quiz</h2>'
  turns,warnings,dropped,audio=parse_publisher_html(html)
  self.assertEqual(len(turns),12);self.assertFalse(warnings)
  cat={'id':'voa-1-33','sourceUrl':'https://learningenglish.voanews.com/a/test'}
  li={'id':'voa-linked-1-33','title':'Test','level':'B1','topic':'test','sourceUrl':cat['sourceUrl'],
    'questions':[{'question':'What?','answer':0,'options':['a','b','c','d'],'sourceEvidence':'We are practicing'}]}
  lesson,report=stage_one(cat,li,html)
  self.assertEqual(lesson['questions'][0]['sourceEvidenceTurn'],0)
  self.assertFalse(report['independentHumanReviewed'])
  self.assertFalse(lesson['transcriptVerifiedAgainstAudio'])
  self.assertIsNone(lesson['audioUrl'])
  self.assertTrue(report['warnings'])
if __name__=='__main__':unittest.main()
