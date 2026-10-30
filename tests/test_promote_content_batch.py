from importlib.util import module_from_spec,spec_from_file_location
import json
import tempfile
import unittest
from pathlib import Path

MOD=Path(__file__).resolve().parents[1]/'tools/promote_content_batch.py'
spec=spec_from_file_location('promote_content_batch',MOD)
m=module_from_spec(spec);spec.loader.exec_module(m)

def sample(kind='general'):
    d=dict(word='alleviate' if kind=='general' else 'account for',level='C1' if kind=='general' else 'B2',
           tr='hafifletmek' if kind=='general' else 'açıklamak',
           definition='To make an unpleasant condition feel less severe than it did before.',
           example='The city introduced new measures to alleviate overcrowding at the station.',
           examples=['The city introduced new measures to alleviate overcrowding at the station.',
                     'Regular breaks can alleviate pressure during long, demanding projects.'])
    if kind=='phrasal':d.update(syntax='inseparable',register='neutral',note='Object follows the full phrase.',
                                levelEvidence='Editorial review of an appropriate advanced sense',
                                senses=[dict(tr='açıklamak',definition=d['definition'],example=d['example'])])
    return d

class TestPromotion(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        (self.root/'data').mkdir();(self.root/'sources').mkdir()
        (self.root/'data/vocabulary.json').write_text('[]')
        (self.root/'data/phrasals.json').write_text('[]')
        (self.root/'sources/general-production-queue.json').write_text('[{"word":"alleviate","levelCandidate":"C1"}]')
        (self.root/'sources/phrasal-production-queue.json').write_text('[{"word":"account for","levelCandidate":null}]')
        self.input=self.root/'batch.jsonl'
    def tearDown(self):self.tmp.cleanup()
    def put(self,record):self.input.write_text(json.dumps(record)+'\n')
    def test_dry_run_does_not_touch_students_data(self):
        self.put(sample());out=m.process(self.input,'general',root=self.root)
        self.assertEqual(out['validatedNewCards'],1)
        self.assertEqual(json.loads((self.root/'data/vocabulary.json').read_text()),[])
    def test_apply_preserves_status_unreviewed(self):
        self.put(sample());m.process(self.input,'general',apply=True,root=self.root)
        data=json.loads((self.root/'data/vocabulary.json').read_text())
        self.assertEqual(data[0]['id'],'g-alleviate')
        self.assertEqual(data[0]['editorialStatus'],'authored_unreviewed')
    def test_existing_record_is_not_duplicated(self):
        self.put(sample());m.process(self.input,'general',apply=True,root=self.root)
        with self.assertRaisesRegex(ValueError,'existing content'):
            m.process(self.input,'general',apply=True,root=self.root)
    def test_level_conflicts_stop_import(self):
        x=sample();x['level']='B2';self.put(x)
        with self.assertRaisesRegex(ValueError,'CEFR level disagrees'):
            m.process(self.input,'general',root=self.root)
    def test_phrasal_needs_provenance(self):
        x=sample('phrasal');x.pop('levelEvidence');self.put(x)
        with self.assertRaisesRegex(ValueError,'levelEvidence'):
            m.process(self.input,'phrasal',root=self.root)
    def test_syntax_and_meaning_needed(self):
        x=sample('phrasal');x['senses']=[];self.put(x)
        with self.assertRaisesRegex(ValueError,'phrasal sense'):
            m.process(self.input,'phrasal',root=self.root)
    def test_reject_auto_editorial_approval(self):
        x=sample();x['editorialStatus']='approved';self.put(x)
        with self.assertRaisesRegex(ValueError,'automatic editorial approval'):
            m.process(self.input,'general',root=self.root)

if __name__=='__main__':unittest.main()
