"""Evidence integrity and release honesty for official VOA Lessons 11 and 12."""
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reviewed1112',ROOT/'tools/import_reviewed_voa_11_12.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PublisherTurnEvidenceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  read=lambda name:json.loads((ROOT/'data'/name).read_text(encoding='utf8'))
  cls.auth=read('authentic-listening.json')
  cls.linked=read('voa-source-quizzes.json')
  cls.cat=read('voa-source-catalog.json')

 def test_turn_evidence_is_exact_and_unambiguous(self):
  for cid,src in mod.SOURCES.items():
   lesson=next(x for x in self.auth if x['id']=='voa-linked-'+cid.split('-',1)[-1])
   with self.subTest(cid=cid):
    turns=mod.parse_turns(src['transcript'])
    self.assertEqual(lesson['turns'],turns)
    self.assertGreaterEqual(len(turns),30)
    self.assertEqual(lesson['sourceUrl'],src['sourceUrl'])
    self.assertEqual(len(lesson['questions']),4)
    self.assertTrue(lesson['audioUrl'].startswith('https://voa-audio.voanews.eu/'))
    self.assertFalse(lesson['timingVerified'])
    self.assertFalse(lesson['transcriptVerifiedAgainstAudio'])
    self.assertFalse(lesson['offlineReady'])
    for q,(speaker,phrase) in zip(lesson['questions'],src['evidence']):
     idx=q['sourceEvidenceTurn']
     self.assertEqual(q['sourceEvidenceSpeaker'],speaker)
     self.assertIn(phrase,turns[idx]['text'])
     self.assertEqual(turns[idx]['speaker'],speaker)
     self.assertEqual(len([t for t in turns if t['speaker']==speaker and phrase in t['text']]),1)
     self.assertEqual(q['sourceEvidence'],phrase)

 def test_preserved_quiz_ids_and_corrected_answer(self):
  ids={x['id'] for x in self.auth+self.linked}
  self.assertEqual(len(ids),50)
  self.assertIn('voa-linked-2-11',ids)
  self.assertIn('voa-linked-2-12',ids)
  self.assertEqual(sum(len(x['questions']) for x in self.auth+self.linked),204)
  self.assertEqual(len(self.auth),30)
  self.assertEqual(len(self.linked),20)
  for cid in mod.SOURCES:
   c=next(x for x in self.cat if x['id']==cid)
   self.assertTrue(c['transcriptImported'])
   self.assertEqual(c['interactiveLessonId'],'voa-linked-'+cid.split('-',1)[-1])
  lesson=next(x for x in self.auth if x['id']=='voa-linked-2-11')
  q=lesson['questions'][2]
  self.assertEqual(q['options'][q['answer']],'Food, a blanket, and warm clothing')

 def test_idempotent_import_and_release_honesty(self):
  before=[(p,p.read_bytes()) for p in (mod.AUTH,mod.LINKED,mod.CAT)]
  result=mod.run()
  self.assertEqual(result['speakerTurnEvidence'],124)
  self.assertFalse(result['releaseApproved'])
  self.assertFalse(result['iphoneAudioPlaybackVerified'])
  self.assertTrue(all(p.read_bytes()==b for p,b in before))
  report=json.loads((ROOT/'qa/non-speaking-quality-report.json').read_text())
  self.assertEqual(report['integratedPublisherTranscripts'],19)
  self.assertEqual(report['publisherTranscriptTurnBoundQuestionEvidence'],80)
  self.assertEqual(report['externalMP3PlaybackVerifiedOnDevice'],0)
  self.assertFalse(report['releaseApproved'])
  status=json.loads((ROOT/'development-status.json').read_text())
  self.assertEqual(status['voaPublisherSources'],50)
  self.assertEqual(status['voaIntegratedPublisherTranscripts'],30)
  self.assertEqual(status['voaPublisherOnlyQuizzes'],20)
  self.assertEqual(status['voaQuizQuestionCount'],204)
  self.assertEqual(status['voaSpeakerTurnEvidenceQuestions'],121)
  self.assertEqual(status['voaAudioPlaybackVerifiedOnPhysicalIphone'],0)
  self.assertFalse(status['readyForRelease'])

if __name__=='__main__':unittest.main()
