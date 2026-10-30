"""No fabricated corpus frequency or editorial approval."""
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit_core',ROOT/'tools/audit_toefl_core_editorial.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
class CorpusAudit(unittest.TestCase):
 def test_review_queue_retains_475_existing_ids_and_explicit_approval_gaps(self):
  result=a.audit()
  self.assertEqual(result['reviewScope'],475)
  self.assertEqual(result['resolvableExistingIDs'],475)
  self.assertFalse(result['corpusUSFrequencyMeasured'])
  self.assertFalse(result['TOEFLFrequencyMeasured'])
  self.assertEqual(result['humanEditorApproved'],0)
  self.assertFalse(result['releaseApproved'])
  import csv
  with (ROOT/result['reviewQueue']).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),475)
  self.assertEqual(len({x['id'] for x in rows}),475)
  self.assertTrue(all(x['independentEditorApproval']=='PENDING' for x in rows))
if __name__=='__main__':unittest.main()
