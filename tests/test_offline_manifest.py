import re,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OfflineManifestTests(unittest.TestCase):
    def test_robotic_audio_never_cached_or_shipped(self):
        src=(ROOT/'sw.js').read_text()
        m=re.search(r'const AUDIO=(\[[^\n]*\]);',src)
        self.assertIsNotNone(m)
        self.assertEqual(json.loads(m.group(1)),[])
        items=json.loads((ROOT/'data/episodes.json').read_text())+json.loads((ROOT/'data/drills.json').read_text())
        self.assertEqual(len(items),42)
        self.assertTrue(all(not (ROOT/row['audio']).exists() for row in items))
    def test_catalog_script_precached(self):
        self.assertIn("'./js/catalog.js'",(ROOT/'sw.js').read_text())
if __name__=='__main__':unittest.main()
