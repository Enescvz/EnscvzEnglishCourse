"""VOA-original transcript proof; audio/device QA remains unverified."""
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('review20',ROOT/'tools/import_reviewed_voa_20_21.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def read(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
class VOATwentyTwentyOneTests(unittest.TestCase):
 def test_full_conversation_and_evidence_source_checked(self):
  arr=read('data/authentic-listening.json')
  for n in (20,21):
   x=next(x for x in arr if x['id']==f'voa-linked-2-{n}')
   self.assertEqual(x['turns'],m.source_turns(n))
   self.assertGreater(len(x['turns']),40)
   self.assertTrue(x['audioUrl'].startswith('https://voa-audio.voanews.eu/'))
   self.assertFalse(x['audioBundled']);self.assertFalse(x['offlineReady'])
   self.assertFalse(x['timingVerified']);self.assertFalse(x['transcriptVerifiedAgainstAudio'])
   for q in x['questions']:
    t=x['turns'][q['sourceEvidenceTurn']]
    self.assertEqual((t['speaker'],t['kind']),(q['sourceEvidenceSpeaker'],q['sourceEvidenceKind']))
    self.assertIn(q['sourceEvidence'].casefold(),t['text'].casefold())
 def test_question_identity_and_all_50_lesson_ids_preserved(self):
  full=read('data/authentic-listening.json');linked=read('data/voa-source-quizzes.json')
  self.assertEqual((len(full),len(linked)),(30,20))
  self.assertEqual(len({x['id'] for x in full+linked}),50)
  self.assertEqual(sum(len(x['questions']) for x in full+linked),204)
 def test_import_idempotence_and_release_lock(self):
  files=[ROOT/'data'/f for f in ('authentic-listening.json','voa-source-catalog.json','voa-source-quizzes.json')]
  before=[p.read_bytes() for p in files]
  self.assertEqual(m.integrate(),[])
  self.assertEqual(before,[p.read_bytes() for p in files])
  status=read('development-status.json')
  self.assertFalse(status['readyForRelease'])
  self.assertFalse(status['gates']['Browser E2E evidence desktop + iPhone WebKit'])
if __name__=='__main__':unittest.main()
