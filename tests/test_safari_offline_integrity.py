import unittest,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SafariOfflineIntegrityTests(unittest.TestCase):
 def test_all_core_scripts_and_runtime_json_available_for_offline_boot(self):
  sw=(ROOT/'sw.js').read_text()
  m=re.search(r'const CORE=(\[[^\n]*\]);',sw)
  self.assertIsNotNone(m)
  import ast
  core=set(ast.literal_eval(m.group(1)))
  required={
   './','./index.html','./styles.css','./manifest.webmanifest','./js/offline.js','./data/candidate-catalog.json',
   *{'./js/'+file.name for file in (ROOT/'js').glob('*.js')},
   *{'./data/'+file for file in ('vocabulary.json','phrasals.json','episodes.json','drills.json','grammar.json','readings.json','authentic-listening.json','toefl-reading-practice.json','toefl-writing-practice.json','toefl-listening-practice.json','voa-source-catalog.json','voa-source-quizzes.json','rapid-vocabulary.json','fluency-focus.json','toefl-academic.json','toefl-core.json')}
  }
  self.assertTrue(required.issubset(core),sorted(required-core))
  self.assertTrue(all((ROOT/path.removeprefix('./')).is_file() or path=='./' for path in core))
 def test_safari_offline_status_cannot_claim_real_safari_qa(self):
  offline=(ROOT/'js/offline.js').read_text()
  self.assertIn('iPhone Safari testi ayrıca gerekli',offline)
  self.assertIn('result.ready?',offline)
  self.assertIn('İçerikleri indir / doğrula',offline)
  sw=(ROOT/'sw.js').read_text()
  self.assertIn('AEL_CACHE_REPAIR',sw)
  self.assertNotIn('await cache.addAll(AUDIO);',sw)
if __name__=='__main__':unittest.main()
