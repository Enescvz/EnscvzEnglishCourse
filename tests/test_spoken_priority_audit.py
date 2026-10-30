import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class SpokenPriorityAuditTest(unittest.TestCase):
    def test_audit_does_not_claim_frequency(self):
        subprocess.run([sys.executable,str(ROOT/'tools'/'audit_conversational_priority.py')],capture_output=True,check=True)
        report=json.loads((ROOT/'qa'/'spoken-priority-report.json').read_text())
        self.assertEqual(report['screened_total'],1500)
        self.assertEqual(report['spoken_frequency_verified'],0)
        self.assertEqual(report['preliminary_review_flags']['general'],0)
        self.assertGreater(report['preliminary_review_flags']['phrasal'],5)
        csv=(ROOT/'qa'/'spoken-priority-review.csv').read_text()
        self.assertNotIn('unmusically',csv)
        archive=json.loads((ROOT/'data/archived-vocabulary.json').read_text())
        self.assertIn('unmusically',{x['word'] for x in archive})
        self.assertNotIn('pendulous',csv)
        self.assertIn('wake up',csv)

if __name__ == '__main__':unittest.main()
