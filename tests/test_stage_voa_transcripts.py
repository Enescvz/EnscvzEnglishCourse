"""VOA transcript extraction stays review-only and fails safely."""
import unittest
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from stage_voa_transcripts import extract_transcript,extract_mp3_urls, retrieve_page

class VOATranscriptParserTests(unittest.TestCase):
 def test_speakers_before_quiz_and_continuation(self):
  h='<html><h2>Conversation</h2><p>Anna: Hello there.</p><p>Pete: Nice to see you.</p><p>Anna: I have news.</p><p>It is very exciting.</p><p>Pete: Tell me.</p><p>Anna: Later today.</p><h2>Listening Quiz</h2><p>Professor: Should never appear.</p></html>'
  turns=extract_transcript(h)
  self.assertEqual(len(turns),5)
  self.assertIn('exciting',turns[2]['text'])
  self.assertNotIn('Professor',str(turns))
 def test_no_fake_transcript(self):
  self.assertEqual(extract_transcript('<h2>Conversation</h2><p>One random line</p>'),[])
 def test_audio_urls_deduplicated_official_host_only(self):
  h='https://voa-audio.voanews.eu/vle/2020/01/01/aaa_hq.mp3?download=1 https://voa-audio.voanews.eu/vle/2020/01/01/aaa_hq.mp3?download=1'
  self.assertEqual(len(extract_mp3_urls(h)),1)
 def test_no_unsafe_hosts(self):
  with self.assertRaises(ValueError):retrieve_page('https://example.com/')
if __name__=='__main__':unittest.main()
