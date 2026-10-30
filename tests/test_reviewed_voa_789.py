"""Publisher transcripts, evidence and audio honesty for new lessons 7–9."""
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reviewed789',ROOT/'tools/import_reviewed_voa_7_8_9.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class Reviewed789Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  def read(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf8'))
  cls.ready=read('authentic-listening.json');cls.linked=read('voa-source-quizzes.json');cls.catalog=read('voa-source-catalog.json')

 def test_source_turns_match_all_evidence_and_keep_ids(self):
  for cid,source in mod.SOURCES.items():
   with self.subTest(cid=cid):
    lesson=next(x for x in self.ready if x['id']=='voa-linked-'+cid.split('-',1)[-1])
    cat=next(x for x in self.catalog if x['id']==cid)
    self.assertEqual(lesson['sourceUrl'],source['sourceUrl'])
    self.assertGreaterEqual(len(lesson['turns']),25)
    self.assertEqual(len(lesson['questions']),4)
    self.assertEqual(cat['interactiveLessonId'],lesson['id'])
    self.assertTrue(cat['transcriptImported'])
    self.assertNotIn(lesson['id'],{x['id'] for x in self.linked})
    for q,(speaker,evidence) in zip(lesson['questions'],source['evidence']):
     self.assertIn(q['answer'],range(4))
     turn=lesson['turns'][q['sourceEvidenceTurn']]
     self.assertEqual(turn['speaker'],speaker)
     self.assertEqual(q['sourceEvidenceSpeaker'],speaker)
     self.assertIn(evidence,turn['text'])
     self.assertEqual(q['sourceEvidence'],evidence)

 def test_direct_audio_must_be_real_url_or_fallback(self):
  byid={x['id']:x for x in self.ready}
  self.assertIsNone(byid['voa-linked-2-08']['audioUrl'])
  self.assertEqual(byid['voa-linked-2-08']['audioAvailability'],'publisher_page_only')
  for cid in ['07','09']:
   x=byid[f'voa-linked-2-{cid}']
   self.assertTrue(x['audioUrl'].startswith('https://voa-audio.voanews.eu/'))
  app=(ROOT/'js/app.js').read_text(encoding='utf8')
  self.assertIn('doğrulanmış doğrudan MP3 bağlantısı bulunamadı',app)
  self.assertIn("x.audioUrl?'ONLINE MP3 · HUMAN':'VOA SAYFASINDA DİNLE'",app)
  self.assertIn('authenticListenedConfirm',app)

 def test_never_assert_human_audio_playback_or_readiness(self):
  all_lessons=self.ready+self.linked
  self.assertEqual(len(all_lessons),50)
  self.assertEqual(len({x['id'] for x in all_lessons}),50)
  self.assertEqual(sum(len(x['questions']) for x in all_lessons),204)
  for x in self.ready:
   self.assertFalse(x.get('offlineReady',False))
   self.assertFalse(x.get('transcriptVerifiedAgainstAudio',False))
   self.assertFalse(x.get('timingVerified',False))
  report=json.loads((ROOT/'qa/non-speaking-quality-report.json').read_text(encoding='utf8'))
  pets=next(x for x in self.ready if x['id']=='voa-linked-2-09')
  self.assertEqual(pets['questions'][2]['options'][pets['questions'][2]['answer']],'One-of-Kind Pet')
  self.assertEqual(report['integratedPublisherTranscripts'],19)
  self.assertEqual(report['publisherTranscriptTurnBoundQuestionEvidence'],80)
  self.assertEqual(report['externalMP3PlaybackVerifiedOnDevice'],0)
  self.assertFalse(report['releaseApproved'])

if __name__=='__main__':unittest.main()

class BackfilledSourceEvidenceTests(unittest.TestCase):
 def test_every_in_app_question_has_turn_bound_publisher_script_evidence(self):
  ready=json.loads((ROOT/'data/authentic-listening.json').read_text(encoding='utf8'))
  for lesson in ready:
   for q in lesson['questions']:
    with self.subTest(lesson=lesson['id'],question=q['question']):
     self.assertIn('sourceEvidenceTurn',q)
     turn=lesson['turns'][q['sourceEvidenceTurn']]
     self.assertEqual(q['sourceEvidenceSpeaker'],turn['speaker'])
     self.assertIn(q['sourceEvidence'],turn['text'])
     for extra in q.get('sourceEvidenceAdditional',[]):
      t=lesson['turns'][extra['turn']]
      self.assertEqual(extra['speaker'],t['speaker'])
      self.assertIn(extra['text'],t['text'])
 def test_older_lesson_identity_and_extra_evidence(self):
  ready=json.loads((ROOT/'data/authentic-listening.json').read_text(encoding='utf8'))
  lesson=next(x for x in ready if x['id']=='voa-linked-2-03')
  self.assertEqual(len(lesson['questions']),4)
  self.assertEqual(len(lesson['questions'][3]['sourceEvidenceAdditional']),1)
  self.assertIn('Kaynak:',(ROOT/'js/app.js').read_text(encoding='utf8'))
