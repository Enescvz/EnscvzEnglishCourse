"""Verify new VOA turn-bound evidence, 204 questions, and no release overclaim."""
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('review07',ROOT/'tools/review_voa_07_08_20261028.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class VOASevenEightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.full=json.loads((ROOT/'data/authentic-listening.json').read_text('utf8'))
        cls.linked=json.loads((ROOT/'data/voa-source-quizzes.json').read_text('utf8'))
        cls.catalog=json.loads((ROOT/'data/voa-source-catalog.json').read_text('utf8'))
    def test_lessons_still_total_50_and_204_questions(self):
        self.assertEqual((len(self.full),len(self.linked)),(30,20))
        self.assertEqual(sum(len(x['questions']) for x in self.full+self.linked),204)
        self.assertEqual(len({x['id'] for x in self.full+self.linked}),50)
        self.assertTrue(all(not x.get('audioBundled',False) for x in self.full+self.linked))
    def test_07_complete_page_conversation_with_turn_evidence(self):
        l=next(x for x in self.full if x['id']=='voa-linked-2-07')
        self.assertEqual(l['sourceUrl'],m.SOURCE7)
        self.assertFalse(l['timingVerified'])
        self.assertFalse(l['transcriptVerifiedAgainstAudio'])
        self.assertFalse(l['offlineReady'])
        self.assertFalse(l.get('audioBundled',False))
        self.assertEqual(l['turns'],m.parse_reviewed_transcript(m.TRANSCRIPT.read_text('utf8')))
        self.assertGreaterEqual(len(l['turns']),35)
        for q in l['questions']:
            turn=l['turns'][q['sourceEvidenceTurn']]
            self.assertEqual(q['sourceEvidenceSpeaker'],turn['speaker'])
            self.assertIn(q['sourceEvidence'],turn['text'])
            self.assertFalse(l['transcriptVerifiedAgainstAudio'])
    def test_08_quoted_evidence_without_fake_turn_ids(self):
        l=next(x for x in self.full if x['id']=='voa-linked-2-08')
        self.assertEqual(l['sourceUrl'],m.SOURCE8)
        self.assertGreater(len(l['turns']), 10)
        self.assertEqual(len(l['questions']),4)
        for q,(speaker,quote) in zip(l['questions'],m.EVIDENCE8):
            self.assertEqual(q['sourceEvidenceSpeaker'],speaker)
            self.assertIn(quote,q['sourceEvidence'])
            turn=l['turns'][q['sourceEvidenceTurn']]
            self.assertEqual(turn['speaker'],speaker)
            self.assertIn(q['sourceEvidence'],turn['text'])
            self.assertFalse(l['transcriptVerifiedAgainstAudio'])
    def test_import_idempotent(self):
        paths=(m.AUTH,m.QUIZ,m.CAT)
        before=[p.read_bytes() for p in paths]
        m.run()
        self.assertEqual(before,[p.read_bytes() for p in paths])
    def test_malformed_or_mismatched_transcript_rejected(self):
        with self.assertRaises(ValueError):m.parse_reviewed_transcript('Anna: Hello')
        with self.assertRaises(ValueError):m.annotate([{'answer':0,'options':['a','b','c','d']}],m.EVIDENCE7)
    def test_release_locked_and_speaking_untouched_by_import_script(self):
        status=json.loads((ROOT/'development-status.json').read_text('utf8'))
        self.assertFalse(status['readyForRelease'])
        self.assertFalse(status['gates']['Browser E2E evidence desktop + iPhone WebKit'])
        script=(ROOT/'tools/review_voa_07_08_20261028.py').read_text('utf8')
        self.assertNotIn('data/speaking',script)
        self.assertNotIn('localStorage',script)

if __name__=='__main__':unittest.main()
