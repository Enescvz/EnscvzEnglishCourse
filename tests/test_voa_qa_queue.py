"""Keep source-review queue honest and reproducible; don't invent MP3 passes."""
import csv, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('voa_queue',ROOT/'tools/audit_voa_completion_queue.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class CompletionAuditTests(unittest.TestCase):
 def test_audit_does_not_promote_source_only_lessons(self):
  tracked=[ROOT/'data/authentic-listening.json',ROOT/'data/voa-source-quizzes.json',ROOT/'data/voa-source-catalog.json']
  before=[p.read_bytes() for p in tracked]
  r=mod.audit()
  self.assertEqual([r[k] for k in ('totalVOASourceLessons','inAppTranscriptLessons','publisherPageOnlyLessons','totalOriginalQuestions','speakerAndTurnEvidenceChecked','pendingQuestionSourceEvidence')], [50,30,20,204,124,0])
  self.assertEqual([p.read_bytes() for p in tracked],before)
  self.assertEqual(r['publisherLinkedExcerptEvidenceChecked'],80)
  self.assertEqual(r['sourceEvidenceTotal'],204)
  self.assertFalse(r['readyForRelease'])
  self.assertFalse(r['offlineE2EPassed'])
  self.assertFalse(r['physicalIPhoneSafariPassed'])
  with (ROOT/'qa/voa-question-review-queue.csv').open(encoding='utf-8-sig',newline='') as f:
   records=list(csv.DictReader(f))
  self.assertEqual(len(records),0)
  self.assertTrue(all(row['verificationStatus']=='PENDING_SOURCE_TURN_REVIEW' for row in records))
  self.assertEqual(len(set((x['lessonId'],x['questionIndex']) for x in records)),0)
 def test_publisher_authored_only_credit_is_explicit(self):
  r=json.loads((ROOT/'qa/voa-source-coverage.json').read_text())
  self.assertEqual(r['localHumanAudioMP3Count'],0)
  self.assertEqual(r['sourceLicense'],'https://learningenglish.voanews.com/p/6861.html')
  self.assertEqual(len(r['remainingLessons']),20)
if __name__=='__main__':unittest.main()
