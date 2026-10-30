"""VOA 19–30 source excerpt QA, separate from imported transcript turns/audio QA."""
import copy,hashlib,importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('voa_excerpt_review',ROOT/'tools/review_voa_publisher_questions_19_30.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class PublisherLinkedEvidenceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.linked=json.loads((ROOT/'data/voa-source-quizzes.json').read_text())
  cls.full=json.loads((ROOT/'data/authentic-listening.json').read_text())
  cls.catalog=json.loads((ROOT/'data/voa-source-catalog.json').read_text())
  cls.proof=json.loads((ROOT/'qa/source-reviews/voa-l2-19-30-evidence-20261028.json').read_text())
 def test_twelve_lessons_48_question_key_evidence(self):
  reviewed=[x for x in self.linked+self.full if x['id'].startswith('voa-linked-2-') and 19<=int(x['id'][-2:])<=30]
  self.assertEqual(len(reviewed),12)
  self.assertEqual({int(x['id'][-2:]) for x in reviewed},set(range(19,31)))
  self.assertEqual(len(self.proof['reviews']),48)
  review_by={(x['lessonId'],x['questionIndex']):x for x in self.proof['reviews']}
  for lesson in reviewed:
   self.assertTrue(lesson['sourceUrl'].startswith('https://learningenglish.voanews.com/a/'))
   if lesson in self.linked:
    self.assertEqual(lesson['transcriptAvailability'],'publisher_external_only')
    self.assertFalse(lesson['transcriptImported'])
    self.assertFalse(lesson['playerVerified'])
   else:
    self.assertFalse(lesson['transcriptVerifiedAgainstAudio'])
    self.assertFalse(lesson['offlineReady'])
   self.assertFalse(lesson['audioBundled'])
   for i,q in enumerate(lesson['questions']):
    proof=review_by[(lesson['id'],i)]
    self.assertEqual(q['sourceEvidence'],proof['literalExcerpt'])
    self.assertEqual(q['sourceEvidenceSpeaker'],proof['speakerOrStage'])
    self.assertEqual(q['sourceEvidenceKind'],proof['evidenceKind'])
    self.assertEqual(q['sourceEvidencePublisherLine'],proof['webReviewLine'])
    self.assertEqual(q['sourceEvidencePublisherUrl'],proof['sourceUrl'])
    if lesson in self.linked:self.assertNotIn('sourceEvidenceTurn',q)
    else:self.assertIn('sourceEvidenceTurn',q)
    self.assertLessEqual(len(q['sourceEvidence'].split()),12)
 def test_stage_directions_are_never_spoken_claims(self):
  stages=[r for r in self.proof['reviews'] if r['evidenceKind']=='stage_direction']
  self.assertEqual({(r['lessonId'],r['questionIndex']) for r in stages},
    {('voa-linked-2-19',3),('voa-linked-2-20',3),('voa-linked-2-25',2)})
  self.assertTrue(all(r['speakerOrStage']=='Stage direction' for r in stages))
 def test_provenance_locks_and_third_party_lyrics_excluded(self):
  self.assertIn('Lesson 23 commercial song lyrics',self.proof['thirdPartyCopyrightExclusion'])
  self.assertFalse(self.proof['notAudioVerified'] is False)
  self.assertTrue(self.proof['notFullTranscripts'])
  self.assertEqual(sum(len(x['questions']) for x in self.linked+self.full),204)
  self.assertEqual(len(self.full)+len(self.linked),50)
  a=(ROOT/'js/app.js').read_text()
  self.assertIn('function linkedEvidence(q)',a)
  self.assertIn('Kaynak kontrolü:',a)
  self.assertIn('Ses eşleşmesi doğrulanmadı.',a)
 def test_existing_quiz_questions_choices_and_answers_preserved(self):
  frozen=json.loads((ROOT/'qa/source-reviews/voa-l2-19-30-question-identity-baseline.json').read_text())
  for x in self.linked:
   if x['id'] not in frozen:continue
   self.assertEqual([hashlib.sha256(json.dumps([q['question'],q['options'],q['answer']],ensure_ascii=False,sort_keys=True).encode()).hexdigest() for q in x['questions']],frozen[x['id']])
 def test_review_import_idempotent_on_copy(self):
  with tempfile.TemporaryDirectory() as d:
   d=Path(d);q=d/'q.json';c=d/'c.json';p=d/'proof.json'
   q.write_text(json.dumps(self.linked,ensure_ascii=False));c.write_text(json.dumps(self.catalog,ensure_ascii=False))
   old=(mod.DATA,mod.CATALOG,mod.PROOF)
   try:
    mod.DATA,mod.CATALOG,mod.PROOF=q,c,p
    self.assertEqual(mod.run()['reviewedLinkedQuestions'],48)
    a=q.read_bytes();b=c.read_bytes();z=p.read_bytes()
    mod.run()
    self.assertEqual((a,b,z),(q.read_bytes(),c.read_bytes(),p.read_bytes()))
   finally:
    mod.DATA,mod.CATALOG,mod.PROOF=old
if __name__=='__main__':unittest.main()
