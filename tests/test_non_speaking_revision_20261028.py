import json
import unittest
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
class NonSpeakingQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        def read(x):return json.loads((ROOT/'data'/f'{x}.json').read_text(encoding='utf-8'))
        cls.full=read('authentic-listening');cls.linked=read('voa-source-quizzes')
        cls.reading=read('readings');cls.grammar=read('grammar')
    def test_fifty_question_sets_with_twelve_transcripts(self):
        self.assertEqual(len(self.full),30)
        self.assertEqual(len(self.linked),20)
        self.assertEqual(sum(len(x['questions']) for x in self.full+self.linked),204)
    def test_new_publisher_transcript_answers_have_verifiable_evidence(self):
        x=next(x for x in self.full if x['id']=='voa-linked-2-03')
        self.assertEqual(len(x['turns']),25)
        self.assertFalse(x['offlineReady']);self.assertFalse(x['transcriptVerifiedAgainstAudio'])
        self.assertTrue(all(q['sourceEvidence'] and 'publisher Conversation' not in q['sourceEvidence'] for q in x['questions']))
        text=' '.join(t['text'].lower() for t in x['turns'])
        for detail in ('43 minutes','special','scooter','birds','point of view'):
            self.assertIn(detail,text)
    def test_new_two_transcripts_have_turn_bound_answer_evidence(self):
        for id_ in ('voa-linked-2-04','voa-linked-2-05','voa-linked-2-06'):
            lesson=next(x for x in self.full if x['id']==id_)
            self.assertGreaterEqual(len(lesson['turns']),20)
            self.assertFalse(lesson['transcriptVerifiedAgainstAudio'])
            self.assertFalse(lesson['offlineReady'])
            for q in lesson['questions']:
                turn=lesson['turns'][q['sourceEvidenceTurn']]
                self.assertEqual(q['sourceEvidenceSpeaker'],turn['speaker'])
                self.assertIn(q['sourceEvidence'],turn['text'])
    def test_transcript_lessons_require_listening_self_report(self):
        app=(ROOT/'js/app.js').read_text(encoding='utf-8')
        self.assertIn('authenticListenedConfirm',app)
        self.assertIn('if(!ui.authenticListened)',app)
        self.assertIn("assessmentType:'publisher-transcript-comprehension'",app)
        self.assertIn('audioPlaybackSelfReported:true,audioPlaybackVerified:false',app)
        self.assertIn('authenticEvidence(q)',app)
    def test_correct_options_do_not_follow_position_shortcut(self):
        reading=Counter(q['answer'] for x in self.reading for q in x['questions'])
        grammar=Counter(g['answerIndex'] for g in self.grammar)
        self.assertEqual(sum(reading.values()),150)
        self.assertLessEqual(max(reading.values())-min(reading.values()),1)
        self.assertEqual(dict(grammar),{0:5,1:5,2:5,3:5})
    def test_all_answer_keys_match_content(self):
        for x in self.reading:
            for q in x['questions']:
                self.assertIn(q['answer'],range(4))
                self.assertEqual(len(set(q['options'])),4)
        for g in self.grammar:
            self.assertEqual(g['answer'],g['options'][g['answerIndex']])
    def test_no_audio_claims_in_source_only_lessons(self):
        self.assertTrue(all(x['audioAvailability']=='publisher_external_only' and not x['audioBundled'] and not x['playerVerified'] for x in self.linked))
if __name__=='__main__':unittest.main()
