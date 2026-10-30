"""Reviewed VOA conversation excerpts and old-card preservation, private QA."""
import importlib.util
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('voa1314',ROOT/'tools/import_reviewed_voa_13_14.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))

class SourceReviewed1314Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.auth=read('data/authentic-listening.json')
  cls.linked=read('data/voa-source-quizzes.json')
  cls.catalog=read('data/voa-source-catalog.json')
  cls.original=read('sources/voa-linked-13-14-original-quiz-20261028.json')

 def test_evidence_is_at_exact_publisher_turn(self):
  for cid,source in mod.SOURCES.items():
   lesson=next(x for x in self.auth if x['id']=='voa-linked-'+cid.split('-',1)[-1])
   with self.subTest(cid=cid):
    self.assertEqual(lesson['turns'],[{'speaker':a,'text':b} for a,b in source['turns']])
    self.assertEqual(lesson['sourceUrl'],source['sourceUrl'])
    self.assertGreater(len(lesson['turns']),20)
    self.assertEqual(len(lesson['questions']),4)
    for q,(speaker,quote) in zip(lesson['questions'],source['evidence']):
     t=lesson['turns'][q['sourceEvidenceTurn']]
     self.assertEqual((t['speaker'],q['sourceEvidenceSpeaker']),(speaker,speaker))
     self.assertIn(quote,t['text'])
     self.assertEqual(q['sourceEvidence'],quote)
     self.assertEqual(sum(s==speaker and quote in txt for s,txt in source['turns']),1)

 def test_unchanged_question_ids_text_answers_and_original_order(self):
  for lesson_id, original_questions in self.original.items():
   lesson=next(x for x in self.auth if x['id']==lesson_id)
   self.assertEqual([[q['question'],q['options'],q['answer']] for q in lesson['questions']],original_questions)
  self.assertEqual(len({x['id'] for x in self.auth+self.linked}),50)
  self.assertEqual(sum(len(x['questions']) for x in self.auth+self.linked),204)
  self.assertEqual(len(self.auth),30)
  self.assertEqual(len(self.linked),20)
  self.assertEqual(sum('sourceEvidenceTurn' in q for l in self.auth for q in l['questions']),124)

 def test_publisher_audio_is_online_only_and_not_verified(self):
  for id_ in ('voa-linked-2-13','voa-linked-2-14'):
   x=next(x for x in self.auth if x['id']==id_)
   self.assertEqual(urlparse(x['audioUrl']).hostname,'voa-audio.voanews.eu')
   self.assertEqual(x['audioAvailability'],'external_online_stream_only')
   self.assertFalse(x['offlineReady'])
   self.assertFalse(x['timingVerified'])
   self.assertFalse(x['transcriptVerifiedAgainstAudio'])
   self.assertIn('VOA',x['attribution'])
  report=read('qa/non-speaking-quality-report.json')
  status=read('development-status.json')
  self.assertEqual(report['integratedPublisherTranscripts'],19)
  self.assertEqual(report['publisherOnlyTranscriptsAndAudio'],31)
  self.assertEqual(report['publisherTranscriptTurnBoundQuestionEvidence'],80)
  self.assertFalse(report['iPhoneSafariQAApproved'])
  self.assertFalse(report['releaseApproved'])
  self.assertEqual(status['voaSpeakerTurnEvidenceQuestions'],121)
  self.assertEqual(status['voaAudioPlaybackVerifiedOnPhysicalIphone'],0)
  self.assertFalse(status['readyForRelease'])

 def test_importer_does_not_duplicate_or_rekey(self):
  paths=(mod.AUTH,mod.LINKED,mod.CAT)
  before=[p.read_bytes() for p in paths]
  result=mod.run()
  self.assertEqual(result['integrated'],30)
  self.assertEqual(result['evidence'],124)
  self.assertTrue(all(p.read_bytes()==bytes_ for p,bytes_ in zip(paths,before)))

if __name__=='__main__':unittest.main()
