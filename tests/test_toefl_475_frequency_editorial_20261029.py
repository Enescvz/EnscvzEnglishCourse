import json,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(path):return json.loads((R/path).read_text())
class TOEFLFrequencyEditorialAudit(unittest.TestCase):
 def test_reference_check_covers_unchanged_ids(self):
  c=read('data/toefl-core.json');a=read('qa/toefl-475-frequency-and-editorial-audit-20261029.json')
  rows=a['rows'];self.assertEqual(len(rows),475)
  self.assertEqual([r['id'] for r in rows],[*c['wordLessonIds'],*c['phrasalLessonIds']])
  self.assertEqual(len(set(r['id'] for r in rows)),475)
 def test_no_fake_ets_or_human_approval(self):
  a=read('qa/toefl-475-frequency-and-editorial-audit-20261029.json');c=read('data/toefl-core.json')
  self.assertFalse(a['officialTOEFLFrequencyClaim']);self.assertFalse(a['independentEditorialSignoff'])
  self.assertEqual(a['summary']['ETSExamFrequencyRanked'],0)
  self.assertEqual(a['summary']['humanEditorApproved'],0)
  self.assertIs(c['meta']['editorialSignoffComplete'],False)
 def test_reference_evidence_not_overinterpreted(self):
  a=read('qa/toefl-475-frequency-and-editorial-audit-20261029.json')
  self.assertEqual(a['summary']['referenceMembershipCounts']['AWL_headword_match'],168)
  self.assertEqual(a['summary']['referenceMembershipCounts']['PHaVE_top_150'],38)
  self.assertFalse(a['releaseReady'])
  self.assertEqual(len(a['flags']),0)
 def test_corrections_are_sense_consistent(self):
  ph={p['id']:p for p in read('data/phrasals.json')}; acad={p['id']:p for p in read('data/toefl-academic.json')}
  corr=read('qa/toefl-editorial-corrections-20261029.json')
  self.assertEqual(corr['fixCount'],12)
  self.assertEqual(len({r['id'] for r in corr['corrections']}),12)
  self.assertIn('popular',ph['pv-take-off']['definition'])
  self.assertIn('podcast',ph['pv-take-off']['examples'][1])
  self.assertIn('claim',ph['pv-back-up']['examples'][0]);self.assertIn('conclusion',ph['pv-back-up']['examples'][1])
  self.assertEqual(ph['pv-step-up']['syntax'],'separable')
  self.assertIn('noun',acad['toefl-benefit']['definition'])
  self.assertIn('verb',acad['toefl-finance']['definition'])
  self.assertEqual(len(ph['pv-break-down']['examples']),2)
  self.assertFalse(corr['approvedByHumanEditor'])
if __name__=='__main__':unittest.main()
