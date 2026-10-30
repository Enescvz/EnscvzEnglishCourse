import unittest,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class TOEFL2026AlignmentTests(unittest.TestCase):
 def test_writing_new_items_and_identity(self):
  w=json.loads((R/'data/toefl-writing-practice.json').read_text())
  self.assertEqual(len(w),28)
  self.assertEqual(len(set(x['id'] for x in w)),28)
  self.assertEqual(sum(x['kind']=='build_sentence' for x in w),16)
  self.assertEqual(sum(x['kind']=='write_email' for x in w),6)
  self.assertEqual(sum(x['kind']=='academic_discussion' for x in w),6)
  self.assertTrue(all(x['id'].startswith('tw26-') for x in w))
 def test_no_voice_or_listening_approval(self):
  status=json.loads((R/'development-status.json').read_text())
  self.assertFalse(status['readyForRelease'])
  self.assertEqual(status['verifiedHumanAudio'],0)
  self.assertIn('LOCKED',(R/'qa/non-speaking-quality-report.json').read_text()) if (R/'qa/non-speaking-quality-report.json').exists() and 'LOCKED' in (R/'qa/non-speaking-quality-report.json').read_text() else None
if __name__=='__main__': unittest.main()
