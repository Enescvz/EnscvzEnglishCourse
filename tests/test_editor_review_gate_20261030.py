import json,subprocess,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestIndependentEditorGate(unittest.TestCase):
 def test_queue_is_complete_but_not_signed_off(self):
  meta=json.loads((ROOT/'qa/20261030-editor-review/summary.json').read_text())
  self.assertEqual(meta['machineChecked'],975)
  self.assertFalse(meta['independentHumanApproval'])
  result=subprocess.run([sys.executable,str(ROOT/'tools/validate_editor_signoff.py')],capture_output=True,text=True)
  self.assertNotEqual(result.returncode,0)
  self.assertIn('BLOCK',result.stderr+result.stdout)
if __name__=='__main__':unittest.main()
