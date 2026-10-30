"""Regression checks for 20 new linked VOA Level 1 source-grounded quizzes."""
import hashlib, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('voa_l1',ROOT/'tools/review_voa_l1_33_52_evidence_20261028.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def load(p):return json.loads(p.read_text('utf8'))

class VOAL1EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.linked=load(ROOT/'data/voa-source-quizzes.json')
        cls.auth=load(ROOT/'data/authentic-listening.json')
        cls.proofs=load(mod.REPORT)
        cls.cat=load(mod.CAT)

    def test_all_20_lessons_and_80_unique_source_proofs(self):
        self.assertEqual(self.proofs['countLessons'],20)
        self.assertEqual(len(self.proofs['reviews']),80)
        self.assertEqual(len(self.auth),30)
        self.assertEqual(len(self.linked),20)
        self.assertEqual(sum(len(x['questions']) for x in self.auth+self.linked),204)
        ids={(p['lessonId'],p['questionIndex']) for p in self.proofs['reviews']}
        self.assertEqual(len(ids),80)
        self.assertEqual({int(x[0][-2:]) for x in ids},set(range(33,53)))

    def test_proofs_match_visible_question_metadata_and_do_not_invent_turns(self):
        by_id={x['id']:x for x in self.linked}
        for p in self.proofs['reviews']:
            l=by_id[p['lessonId']]; q=l['questions'][p['questionIndex']]
            self.assertEqual(l['sourceUrl'],p['sourceUrl'])
            self.assertEqual(q['sourceEvidence'],p['literalExcerpt'])
            self.assertEqual(q['sourceEvidenceSpeaker'],p['speaker'])
            self.assertEqual(q['sourceEvidencePublisherLine'],p['publisherWebLine'])
            self.assertEqual(q['sourceEvidenceKind'],'speech')
            self.assertEqual(q['sourceReviewStatus'],'publisher_page_excerpt_reviewed_not_audio_verified')
            self.assertNotIn('sourceEvidenceTurn',q)
            self.assertFalse(l['transcriptImported'])
            self.assertFalse(l['audioBundled'])
            self.assertFalse(l['playerVerified'])
            self.assertTrue(0<=q['answer']<4)

    def test_coverage_is_source_evidence_only_not_audio_approval(self):
        coverage=load(ROOT/'qa/voa-source-coverage.json')
        self.assertEqual((coverage['sourceEvidenceTotal'],coverage['pendingQuestionSourceEvidence']),(204,0))
        self.assertEqual((coverage['speakerAndTurnEvidenceChecked'],coverage['publisherLinkedExcerptEvidenceChecked']),(124,80))
        self.assertEqual(coverage['unverifiedRemotePlaybackCount'],50)
        self.assertFalse(coverage['physicalIPhoneSafariPassed'])
        self.assertFalse(coverage['offlineE2EPassed'])
        self.assertFalse(coverage['releaseApproved'])

    def test_third_party_music_and_ambiguous_answers_not_overclaimed(self):
        self.assertTrue(any('Woody Guthrie' in x for x in self.proofs['thirdPartyExcluded']))
        by_key={(r['lessonId'],r['questionIndex']):r for r in self.proofs['reviews']}
        self.assertIn('vending-machine',by_key['voa-linked-1-42',3]['note'])
        self.assertIn('same publisher line',by_key['voa-linked-1-52',2]['note'])
        self.assertIn('otomat',next(x for x in self.linked if x['id']=='voa-linked-1-42')['questions'][3]['sourceEvidenceCaveat'])
        self.assertIn('sourceEvidenceCaveat', (ROOT/'js/app.js').read_text())

    def test_import_is_idempotent_in_temporary_files(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d); q=d/'linked.json'; c=d/'catalog.json'; r=d/'proof.json'
            q.write_text(json.dumps(self.linked,ensure_ascii=False));c.write_text(json.dumps(self.cat,ensure_ascii=False))
            old=(mod.QUIZ,mod.CAT,mod.REPORT)
            try:
                mod.QUIZ,mod.CAT,mod.REPORT=q,c,r
                mod.run()
                before=(q.read_bytes(),c.read_bytes(),r.read_bytes())
                mod.run()
                self.assertEqual(before,(q.read_bytes(),c.read_bytes(),r.read_bytes()))
            finally:mod.QUIZ,mod.CAT,mod.REPORT=old

    def test_speaking_and_release_do_not_change(self):
        status=load(ROOT/'development-status.json')
        self.assertFalse(status['readyForRelease'])
        self.assertEqual(status['voaPublisherExcerptEvidenceQuestions'],80)
        self.assertEqual(status['voaQuestionsAwaitingSourceEvidence'],0)
        importer=(ROOT/'tools/review_voa_l1_33_52_evidence_20261028.py').read_text()
        self.assertNotIn('js/speaking',importer)
        self.assertNotIn('data/speaking',importer)
        self.assertNotIn('localStorage',importer)

if __name__=='__main__':unittest.main()
