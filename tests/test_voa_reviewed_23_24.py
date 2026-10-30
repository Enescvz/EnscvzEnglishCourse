"""Contract for VOA publisher-dialogue import without false audio or copyright approvals."""
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
modfile=ROOT/'tools/import_voa_reviewed_23_24.py'
spec=importlib.util.spec_from_file_location('voa2324',modfile)
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def read(name):return json.loads((ROOT/name).read_text(encoding='utf8'))
class VOAReviewed2324Tests(unittest.TestCase):
 def test_imported_scripts_match_source_dialogue_and_have_grounded_questions(self):
  full=read('data/authentic-listening.json')
  linked=read('data/voa-source-quizzes.json')
  cat={x['id']:x for x in read('data/voa-source-catalog.json')}
  for number,meta in mod.SOURCES.items():
   with self.subTest(lesson=number):
    key=f'voa-linked-2-{number:02d}'
    l=next(x for x in full if x['id']==key)
    self.assertEqual(l['turns'],mod.load_turns(meta['file']))
    self.assertEqual(l['sourceUrl'],meta['sourceUrl'])
    self.assertEqual(l['audioUrl'],meta['audioUrl'])
    self.assertEqual(len(l['questions']),4)
    self.assertFalse(l['offlineReady'])
    self.assertFalse(l['audioBundled'])
    self.assertFalse(l['transcriptVerifiedAgainstAudio'])
    self.assertFalse(l['timingVerified'])
    self.assertEqual(cat[f'voa-2-{number:02d}']['interactiveLessonId'],key)
    self.assertTrue(cat[f'voa-2-{number:02d}']['transcriptImported'])
    self.assertFalse(any(x['id']==key for x in linked))
    for q in l['questions']:
     ix=q['sourceEvidenceTurn']
     turn=l['turns'][ix]
     self.assertEqual(turn['speaker'],q['sourceEvidenceSpeaker'])
     self.assertIn(q['sourceEvidence'].casefold(),turn['text'].casefold())
     self.assertNotEqual(q['answer'],None)
  self.assertEqual(len(full),30)
  self.assertEqual(len(linked),20)
  self.assertEqual(len({x['id'] for x in full+linked}),50)
  self.assertEqual(sum(len(x['questions']) for x in full+linked),204)

 def test_licensed_song_exclusion_is_explicit(self):
  l=next(x for x in read('data/authentic-listening.json') if x['id']=='voa-linked-2-23')
  self.assertTrue(l['transcriptRightsExclusion'])
  self.assertIn('exclusions',l['transcriptScope'])
  text=' '.join(t['text'] for t in l['turns']).casefold()
  self.assertIn('third-party song lyrics omitted',text)
  self.assertNotIn('every breath you take',text)
  self.assertNotIn('every move you make',text)
  self.assertIn('transcriptRightsExclusion',(ROOT/'js/app.js').read_text())

 def test_import_does_not_rewrite_any_id_or_mark_release_ready(self):
  before=[p.read_bytes() for p in [ROOT/'data/authentic-listening.json',ROOT/'data/voa-source-quizzes.json',ROOT/'data/voa-source-catalog.json',ROOT/'development-status.json']]
  self.assertEqual(mod.apply(),0)
  after=[p.read_bytes() for p in [ROOT/'data/authentic-listening.json',ROOT/'data/voa-source-quizzes.json',ROOT/'data/voa-source-catalog.json',ROOT/'development-status.json']]
  self.assertEqual(before,after)
  status=read('development-status.json')
  self.assertFalse(status['readyForRelease'])
  self.assertEqual(status['voaAudioPlaybackVerifiedOnPhysicalIphone'],0)
  self.assertEqual(status['voaIntegratedPublisherTranscripts'],30)
  self.assertEqual(status['voaPublisherOnlyQuizzes'],20)
  self.assertEqual(status['voaTranscriptTurnEvidenceQuestions'],124)
  self.assertEqual(status['voaPublisherExcerptEvidenceQuestions'],80)

if __name__=='__main__':unittest.main()
