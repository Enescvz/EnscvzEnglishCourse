import json
import tempfile
import unittest
from pathlib import Path
from tools.audio_quality_gate import audit, ROOT

class AudioQualityGateTest(unittest.TestCase):
 def test_current_content_is_explicitly_unapproved(self):
  report=audit()
  self.assertEqual(report['recordings'],42)
  self.assertEqual(report['approved_for_natural_listening'],0)
  self.assertEqual(report['quarantined_synthetic_recordings'],42)
  self.assertEqual(report['status'],'BLOCKED')
  self.assertEqual(report['errors'],[])

 def test_approval_requires_evidence(self):
  with tempfile.TemporaryDirectory() as d:
   base=Path(d)
   (base/'data').mkdir()
   for fn in ('episodes.json','drills.json','audio-provenance.json'):
    (base/'data'/fn).write_bytes((ROOT/'data'/fn).read_bytes())
   doc=json.loads((base/'data/audio-provenance.json').read_text())
   first=next(iter(doc['recordings']))
   doc['recordings'][first]['quality']='approved'
   (base/'data/audio-provenance.json').write_text(json.dumps(doc))
   report=audit(base)
   self.assertIn('unverified_approval',[e['type'] for e in report['errors']])

 def test_manifest_covers_both_content_types(self):
  d=json.loads((ROOT/'data/audio-provenance.json').read_text())
  self.assertEqual(sum(k.startswith('episode:') for k in d['recordings']),18)
  self.assertEqual(sum(k.startswith('drill:') for k in d['recordings']),24)
  self.assertTrue(all(v['quality']=='unapproved_robotic' for v in d['recordings'].values()))

if __name__=='__main__': unittest.main()
