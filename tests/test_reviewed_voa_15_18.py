"""Exact source turn verification and legacy ID safety for reviewed 15–18."""
import importlib.util
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('voa1518',ROOT/'tools/import_reviewed_voa_15_18.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def load(path):return json.loads((ROOT/path).read_text(encoding='utf8'))

class Reviewed15To18(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.auth=load('data/authentic-listening.json')
  cls.linked=load('data/voa-source-quizzes.json')
  cls.catalog=load('data/voa-source-catalog.json')
  cls.source_snapshot=load('sources/voa-linked-15-18-original-quiz-20261028.json')
 def test_exact_source_speaker_and_excerpt_and_old_questions(self):
  for n in (15,16,17,18):
   id_=f'voa-linked-2-{n:02d}'
   x=next(y for y in self.auth if y['id']==id_)
   self.assertEqual([{'speaker':a,'text':b} for a,b in (line.split('|',1) for line in mod.RAW[n].splitlines())],x['turns'])
   self.assertEqual([[q['question'],q['options'],q['answer']] for q in x['questions']],self.source_snapshot[id_])
   for q,ev in zip(x['questions'],mod.META[n][4:]):
    speaker,quote=ev.split('|',1)
    matches=[i for i,t in enumerate(x['turns']) if t['speaker']==speaker and quote in t['text']]
    self.assertEqual(matches,[q['sourceEvidenceTurn']],f'{id_}: {quote}')
    self.assertEqual((q['sourceEvidenceSpeaker'],q['sourceEvidence']),(speaker,quote))
    self.assertEqual(len(q['options']),4)
    self.assertTrue(0<=q['answer']<4)
 def test_all_fifty_ids_and_publisher_sources_are_preserved(self):
  catalog={x['id']:x for x in self.catalog}
  self.assertEqual((len(self.auth),len(self.linked)),(30,20))
  self.assertEqual(len({x['id'] for x in self.auth+self.linked}),50)
  self.assertEqual(sum(len(x['questions']) for x in self.auth+self.linked),204)
  self.assertEqual(sum('sourceEvidenceTurn' in q for x in self.auth for q in x['questions']),124)
  for n in (15,16,17,18):
   x=next(x for x in self.auth if x['id']==f'voa-linked-2-{n:02d}')
   c=catalog[f'voa-2-{n:02d}']
   self.assertEqual(c['sourceUrl'],x['sourceUrl'])
   self.assertEqual(c['interactiveLessonId'],x['id'])
   self.assertEqual(urlparse(x['audioUrl']).hostname,'voa-audio.voanews.eu')
   self.assertFalse(x['offlineReady'])
   self.assertFalse(x['timingVerified'])
   self.assertFalse(x['transcriptVerifiedAgainstAudio'])
   self.assertIn('public domain',x['sourceLicense'])
 def test_import_rerun_is_byte_idempotent(self):
  targets=[mod.DATA/x for x in ('authentic-listening.json','voa-source-quizzes.json','voa-source-catalog.json')]
  saved=[p.read_bytes() for p in targets]
  self.assertEqual(mod.run(),{'integrated':30,'linked':20,'questions':204,'evidence':124})
  self.assertEqual([p.read_bytes() for p in targets],saved)
 def test_qa_report_has_no_false_real_device_or_editor_approval(self):
  r=load('qa/non-speaking-quality-report.json')
  status=load('development-status.json')
  self.assertEqual(r['integratedPublisherTranscripts'],19)
  self.assertEqual(r['publisherOnlyTranscriptsAndAudio'],31)
  self.assertEqual(r['publisherTranscriptTurnBoundQuestionEvidence'],80)
  self.assertFalse(r['voaLesson15To18DirectMP3PlaybackVerified'])
  self.assertEqual(r['externalMP3PlaybackVerifiedOnDevice'],0)
  self.assertFalse(r['iPhoneSafariQAApproved'])
  self.assertFalse(r['fullSemanticEditorialApproval'])
  self.assertFalse(r['releaseApproved'])
  self.assertEqual(status['voaIntegratedPublisherTranscripts'],30)
  self.assertEqual(status['voaSpeakerTurnEvidenceQuestions'],121)
  self.assertFalse(status['readyForRelease'])

if __name__=='__main__':unittest.main()
