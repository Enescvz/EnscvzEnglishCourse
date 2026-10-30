import json, unittest, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('source22',ROOT/'tools/import_reviewed_voa_22.py')
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)
def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
class VOALesson22Tests(unittest.TestCase):
 def test_publisher_conversation_and_exact_turn_evidence(self):
  full=read('data/authentic-listening.json');linked=read('data/voa-source-quizzes.json')
  item=next(x for x in full if x['id']=='voa-linked-2-22')
  expected=[{'speaker':s,'text':t,'kind':'stage_direction' if s=='Stage direction' else 'speech'} for s,t in source.turns]
  self.assertEqual(item['turns'],expected)
  self.assertEqual(len(item['questions']),4)
  for q in item['questions']:
   evidence=item['turns'][q['sourceEvidenceTurn']]
   self.assertEqual(evidence['speaker'],q['sourceEvidenceSpeaker'])
   self.assertEqual(evidence['kind'],q['sourceEvidenceKind'])
   self.assertIn(q['sourceEvidence'].casefold(),evidence['text'].casefold())
  self.assertEqual((len(full),len(linked)),(30,20))
  self.assertEqual(sum(len(x['questions']) for x in full+linked),204)
 def test_no_false_audio_or_speaking_approval(self):
  x=next(x for x in read('data/authentic-listening.json') if x['id']=='voa-linked-2-22')
  self.assertEqual(x['sourceUrl'],source.source)
  self.assertEqual(x['audioUrl'],source.audio)
  self.assertFalse(x['transcriptVerifiedAgainstAudio'])
  self.assertFalse(x['timingVerified'])
  self.assertFalse(x['audioBundled'])
  self.assertFalse(x['offlineReady'])
  self.assertFalse(read('development-status.json')['readyForRelease'])
 def test_import_is_idempotent(self):
  p=[ROOT/'data'/n for n in ['authentic-listening.json','voa-source-quizzes.json','voa-source-catalog.json']]
  before=[x.read_bytes() for x in p]
  self.assertFalse(source.apply())
  self.assertEqual([x.read_bytes() for x in p],before)
if __name__=='__main__':unittest.main()
