"""Publisher transcript imports must preserve quiz identity and evidence provenance."""
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reviewed',ROOT/'tools/import_reviewed_voa_4_5_6.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ReviewedVOAImportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full=json.loads((ROOT/'data/authentic-listening.json').read_text(encoding='utf-8'))
        cls.linked=json.loads((ROOT/'data/voa-source-quizzes.json').read_text(encoding='utf-8'))
        cls.catalog=json.loads((ROOT/'data/voa-source-catalog.json').read_text(encoding='utf-8'))

    def test_three_source_verified_imports_keep_ids_and_original_quiz_counts(self):
        self.assertEqual(len(module.SOURCES),3)
        for cid,source in module.SOURCES.items():
            with self.subTest(cid=cid):
                lesson=next(x for x in self.full if x['id']=='voa-linked-'+cid.split('-',1)[-1])
                self.assertEqual(lesson['sourceUrl'],source['sourceUrl'])
                self.assertEqual(len(lesson['questions']),4)
                self.assertGreaterEqual(len(lesson['turns']),20)
                self.assertFalse(lesson['transcriptVerifiedAgainstAudio'])
                self.assertFalse(lesson['timingVerified'])
                self.assertFalse(lesson['offlineReady'])
                self.assertNotIn(lesson['id'],{x['id'] for x in self.linked})
                self.assertTrue(next(x for x in self.catalog if x['id']==cid)['transcriptImported'])

    def test_each_answer_contains_concrete_turn_evidence(self):
        for cid in module.SOURCES:
            lesson=next(x for x in self.full if x['id']=='voa-linked-'+cid.split('-',1)[-1])
            for q in lesson['questions']:
                i=q['sourceEvidenceTurn']
                self.assertLess(i,len(lesson['turns']))
                self.assertEqual(lesson['turns'][i]['speaker'],q['sourceEvidenceSpeaker'])
                self.assertIn(q['sourceEvidence'],lesson['turns'][i]['text'])
                self.assertNotIn('see linked original',q['sourceEvidence'])

    def test_all_fifty_question_sets_have_unique_id_and_natural_audio_not_copied(self):
        data=self.full+self.linked
        self.assertEqual(len(data),50)
        self.assertEqual(len({x['id'] for x in data}),50)
        self.assertEqual(sum(len(x['questions']) for x in data),204)
        self.assertTrue(all(not x.get('audioBundled',False) for x in data))

if __name__=='__main__':unittest.main()
