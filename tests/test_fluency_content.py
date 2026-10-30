import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestFluency(unittest.TestCase):
 def setUp(self):self.data=json.loads((ROOT/'data/fluency-studio.json').read_text());self.app=(ROOT/'js/app.js').read_text();self.sw=(ROOT/'sw.js').read_text()
 def test_authored_counts_and_editor_gates(self):
  d=self.data
  self.assertEqual((len(d['realLife']),sum(len(x['steps']) for x in d['realLife']),len(d['thinking']),len(d['writing'])),(12,36,24,12))
  self.assertFalse(d['meta']['independentEditorApproved']);self.assertFalse(d['meta']['audioBundled']);self.assertFalse(d['meta']['autoEssayScoring'])
 def test_new_navigation_offline_backup_integration(self):
  self.assertIn("['fluencyStudio'",self.app);self.assertIn('fluencyPage(',self.app)
  self.assertIn("'./data/fluency-studio.json'",self.sw);self.assertIn("'./js/fluency-ui.js'",self.sw)
  store=(ROOT/'js/progress-safety.js').read_text()
  for key in ('fluencyCards','fluencyHistory','fluencyDrafts'):self.assertIn(key,store)
 def test_no_new_voice_assets(self):
  self.assertFalse(any((ROOT/'assets').glob('*.mp3')))
  self.assertFalse(any((ROOT/'assets').glob('*.wav')))
if __name__=='__main__':unittest.main()
