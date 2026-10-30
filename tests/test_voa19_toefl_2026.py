"""Regression: original card/progress IDs and 2026 new content integrity."""
import json,hashlib,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
class VOA19TOEFL2026Tests(unittest.TestCase):
 def test_all_fifty_ids_and_original_question_answers_unchanged(self):
  baseline=read('qa/voa204-question-identity-baseline-from-previous-backup.json')['lessonQuestionHashes']
  all_lessons=read('data/authentic-listening.json')+read('data/voa-source-quizzes.json')
  self.assertEqual(set(baseline),{x['id'] for x in all_lessons})
  for lesson in all_lessons:
   original=json.dumps([[q['question'],q['options'],q['answer']] for q in lesson['questions']],ensure_ascii=False,sort_keys=True)
   self.assertEqual(hashlib.sha256(original.encode()).hexdigest(),baseline[lesson['id']],lesson['id'])
  self.assertEqual(sum(len(l['questions']) for l in all_lessons),204)
 def test_voa19_publisher_turns_and_scene_evidence_have_clear_disclaimer(self):
  l=next(x for x in read('data/authentic-listening.json') if x['id']=='voa-linked-2-19')
  self.assertGreaterEqual(len(l['turns']),60)
  self.assertTrue(l['audioUrl'].startswith('https://voa-audio.voanews.eu/'))
  self.assertFalse(l['offlineReady']);self.assertFalse(l['transcriptVerifiedAgainstAudio']);self.assertFalse(l['timingVerified'])
  self.assertEqual(len(l['questions']),4)
  for q in l['questions']:
   turn=l['turns'][q['sourceEvidenceTurn']]
   self.assertIn(q['sourceEvidence'].lower(),turn['text'].lower())
   self.assertEqual(q['sourceEvidenceSpeaker'],turn['speaker'])
  self.assertEqual([q.get('sourceEvidenceKind') for q in l['questions']],['speech','speech','speech','stage_direction'])
  app=(ROOT/'js/app.js').read_text(encoding='utf-8')
  self.assertIn('sahne yönergesi (sesli replik değil)',app)
  self.assertIn('seslendirilmiş olduğu doğrulanmadı',app)
 def test_import_twice_is_safe_and_same_progress_id(self):
  import sys
  sys.path.insert(0,str(ROOT/'tools'))
  from import_reviewed_voa_19 import import_reviewed
  paths=[ROOT/'data'/p for p in ('authentic-listening.json','voa-source-quizzes.json','voa-source-catalog.json')]
  before=[p.read_bytes() for p in paths]
  self.assertFalse(import_reviewed())
  self.assertEqual(before,[p.read_bytes() for p in paths])
  lesson=next(l for l in read('data/authentic-listening.json') if l['id']=='voa-linked-2-19')
  self.assertEqual(lesson['id'],'voa-linked-2-19')
 def test_toefl_2026_categories_distinct_and_not_official_scored(self):
  r=read('data/toefl-reading-practice.json');w=read('data/toefl-writing-practice.json')
  self.assertEqual({x['type'] for x in r},{'complete_words','daily_life','academic_passage'})
  self.assertEqual({x['kind'] for x in w},{'build_sentence','write_email','academic_discussion'})
  self.assertEqual((len(r),len(w)),(18,28))
  self.assertEqual(len({x['id'] for x in r+w}),46)
  self.assertTrue(all(x['id'].startswith('tr26-') for x in r))
  self.assertTrue(all(x['id'].startswith('tw26-') for x in w))
  s=(ROOT/'js/app.js').read_text();self.assertIn('ETS resmî soruları veya gerçek sınav simülasyonu değildir.',s)
  self.assertIn('Başarı puanı üretilmez.',s)
 def test_offline_app_shell_manifest_contains_all_new_files_but_not_remote_voa_mp3(self):
  sw=(ROOT/'sw.js').read_text()
  core=re.search(r'const CORE=\[(.*?)\];',sw,re.S)
  self.assertIsNotNone(core)
  paths=re.findall(r"'\./([^']+)'",core.group(1))
  self.assertTrue(all((ROOT/path).is_file() for path in paths if path not in ('','./')))
  for p in ['js/toefl-writing.js','data/toefl-writing-practice.json','data/toefl-reading-practice.json']:
   self.assertIn(p,paths)
  self.assertNotIn('voa-audio.voanews.eu',core.group(1))
  report=read('qa/real-offline-chromium-report.json')
  self.assertNotEqual(report['status'],'PASS_CHROMIUM_ONLY')
if __name__=='__main__':unittest.main()
