"""VOA human-audio pilot must be source-attributed, honest about online playback,
and have grounded answer keys without guessing transcript timestamps."""
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]

class VOAPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lessons=json.loads((ROOT/'data/authentic-listening.json').read_text(encoding='utf8'))
        cls.app=(ROOT/'js/app.js').read_text(encoding='utf8')
        cls.sw=(ROOT/'sw.js').read_text(encoding='utf8')

    def test_twelve_unique_authentic_lessons_with_published_transcripts(self):
        self.assertEqual(len(self.lessons),30)
        self.assertEqual(len({x['id'] for x in self.lessons}),30)
        self.assertGreaterEqual(sum(len(x['turns']) for x in self.lessons),135)
        for l in self.lessons:
            with self.subTest(l['id']):
                self.assertTrue(l['sourceUrl'].startswith('https://learningenglish.voanews.com/a/'))
                if l['audioUrl']:
                    self.assertEqual(urlparse(l['audioUrl']).hostname,'voa-audio.voanews.eu')
                else:
                    self.assertEqual(l['id'],'voa-linked-2-08')
                self.assertIn('VOA',l['attribution'])
                self.assertIn('public domain',l['sourceLicense'].replace('-',' '))
                self.assertEqual(l['audioType'],'human_dialogue_source')
                self.assertTrue('VOA' in l['transcriptSource'])
                self.assertFalse(l['transcriptVerifiedAgainstAudio'])
                self.assertFalse(l['timingVerified'])
                self.assertFalse(l['offlineReady'])
                self.assertEqual(l['audioAvailability'],'external_online_stream_only' if l['audioUrl'] else 'publisher_page_only')
                self.assertGreaterEqual(len(l['turns']),20)
                self.assertTrue(all(t['speaker'] and len(t['text'])>=2 for t in l['turns']))

    def test_original_quiz_questions_are_complete(self):
        self.assertEqual(sum(len(x['questions']) for x in self.lessons),124)
        for lesson in self.lessons:
            for q in lesson['questions']:
                with self.subTest(lesson=lesson['id'],question=q['question']):
                    self.assertTrue(q['question'].endswith('?'))
                    self.assertGreaterEqual(len(q['options']),4)
                    self.assertEqual(len(q['options']),len(set(q['options'])))
                    self.assertIn(q['answer'],range(len(q['options'])))
                    self.assertGreaterEqual(len(q['explanation']),30)

    def test_not_misrepresented_as_local_audio_or_timed_transcript(self):
        self.assertIn('ONLINE MP3 · HUMAN',self.app)
        self.assertIn('İnternet bağlantısı olmadan çalışmaz',self.app)
        self.assertIn('Saniye bazında ses eşleşmesi henüz doğrulanmadı',self.app)
        self.assertIn('Önce transkript kapalıyken dinle',self.app)
        self.assertIn("'./data/authentic-listening.json'",self.sw)
        self.assertNotIn('voa-level2-02-interview.mp3',self.sw)

    def test_original_synthetic_records_not_replaced(self):
        legacy=json.loads((ROOT/'data/episodes.json').read_text(encoding='utf8'))
        self.assertEqual(len(legacy),18)
        self.assertTrue(all(x['audio'].startswith('assets/audio/') for x in legacy))

if __name__=='__main__':unittest.main()
