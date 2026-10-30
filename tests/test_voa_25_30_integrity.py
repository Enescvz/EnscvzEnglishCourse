"""VOA 25–30 new transcripts: publisher evidence, stable IDs and release lock."""
import importlib.util
import json
import unittest
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('voa2528',ROOT/'tools/import_voa_reviewed_25_30.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
class FourVOATranscripts(unittest.TestCase):
 def test_source_and_all_question_evidence_exact(self):
  full={x['id']:x for x in read('data/authentic-listening.json')}
  original=read('sources/voa-25-30-original-quiz-ids.json')
  catalog={x['id']:x for x in read('data/voa-source-catalog.json')}
  for number,meta in module.SOURCES.items():
   key=f'voa-linked-2-{number:02d}'
   with self.subTest(number=number):
    item=full[key]
    self.assertEqual(item['turns'],module.parse_transcript(number))
    self.assertEqual(item['sourceUrl'],meta['page'])
    self.assertEqual(item['audioUrl'],meta['audio'])
    self.assertEqual(urlsplit(item['audioUrl']).hostname,'voa-audio.voanews.eu')
    self.assertEqual([{'question':q['question'],'options':q['options'],'answer':q['answer']} for q in item['questions']], original[key])
    self.assertTrue(catalog[f'voa-2-{number:02d}']['transcriptImported'])
    self.assertFalse(item['audioBundled'])
    self.assertFalse(item['offlineReady'])
    self.assertFalse(item['transcriptVerifiedAgainstAudio'])
    self.assertFalse(item['timingVerified'])
    for q in item['questions']:
     turn=item['turns'][q['sourceEvidenceTurn']]
     self.assertEqual(turn['speaker'],q['sourceEvidenceSpeaker'])
     self.assertIn(q['sourceEvidence'].casefold(),turn['text'].casefold())
     self.assertEqual(turn['kind'],q['sourceEvidenceKind'])
 def test_all_counts_and_idempotent_import(self):
  paths=[ROOT/x for x in ('data/authentic-listening.json','data/voa-source-quizzes.json','data/voa-source-catalog.json','development-status.json')]
  before=[p.read_bytes() for p in paths]
  self.assertEqual(module.apply(),0)
  self.assertEqual([p.read_bytes() for p in paths],before)
  full=read('data/authentic-listening.json');linked=read('data/voa-source-quizzes.json');status=read('development-status.json')
  self.assertEqual((len(full),len(linked)),(30,20))
  self.assertEqual(len({x['id'] for x in full+linked}),50)
  self.assertEqual(sum(len(x['questions']) for x in full+linked),204)
  self.assertEqual(status['voaTranscriptTurnEvidenceQuestions'],124)
  self.assertEqual(status['voaPublisherExcerptEvidenceQuestions'],80)
  self.assertFalse(status['readyForRelease'])
  self.assertEqual(status['voaAudioPlaybackVerifiedOnPhysicalIphone'],0)
 def test_third_party_song_lyrics_are_not_republished(self):
  item=next(x for x in read('data/authentic-listening.json') if x['id']=='voa-linked-2-30')
  self.assertTrue(item['transcriptRightsExclusion'])
  text=' '.join(t['text'] for t in item['turns']).casefold()
  self.assertIn('third-party song lyrics omitted',text)
  self.assertNotIn('you can reach for the stars',text)
 def test_stage_direction_never_mislabeled_spoken(self):
  full=read('data/authentic-listening.json')
  item=next(x for x in full if x['id']=='voa-linked-2-25')
  q=item['questions'][2]
  self.assertEqual(q['sourceEvidenceKind'],'stage_direction')
  self.assertEqual(item['turns'][q['sourceEvidenceTurn']]['kind'],'stage_direction')
if __name__=='__main__':unittest.main()
