"""Specific anti-regression tests for the authored daily-context content sprint."""
import json
import sys
import tempfile
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from author_daily_context_sprint_20261028 import make_rows
from promote_content_batch import validate_record
from reconcile_rapid_promotions import reconcile

class DailyContextSprint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=make_rows()
        cls.bank=json.loads((ROOT/'data/vocabulary.json').read_text())
        cls.archive=json.loads((ROOT/'data/archived-vocabulary.json').read_text()) if (ROOT/'data/archived-vocabulary.json').exists() else []
        cls.focus=json.loads((ROOT/'data/fluency-focus.json').read_text())
        cls.rapid=json.loads((ROOT/'data/rapid-vocabulary.json').read_text())
        cls.authorized={x['word']:x for x in json.loads((ROOT/'sources/general-production-queue.json').read_text())}

    def test_authored_batch_unique_and_context_rich(self):
        self.assertEqual(len(self.rows),178)
        self.assertEqual(len({x['word'] for x in self.rows}),178)
        catalog={x['word']:x['levelCandidate'] for x in json.loads((ROOT/'sources/b2-c1-offline-catalog.json').read_text())}
        bank={x['word']:x for x in self.bank if x['category']=='general'}
        historic={x['word']:x for x in self.archive}
        focused={x['word']:x for x in self.focus['vocabulary']}
        for row in self.rows:
            with self.subTest(word=row['word']):
                self.assertEqual(row['level'],catalog[row['word']])
                lesson=bank.get(row['word']) or historic[row['word']]
                self.assertEqual(row['level'],lesson['level'])
                if row['word'] in bank:
                    self.assertEqual(focused[row['word']]['status'],'context_draft')
                    self.assertEqual(focused[row['word']]['lessonId'],lesson['id'])
                else:
                    self.assertTrue(lesson.get('archivedFromFocus'))
                    self.assertNotIn(row['word'],focused)
                self.assertTrue(row['examples'][0]==row['example'])
                self.assertEqual(len(set(row['examples'])),2)
                self.assertTrue(all(len(s)>=25 and s.strip()[-1] in '.!?' for s in row['examples']))
                self.assertFalse(lesson.get('editorialStatus')=='approved')
                self.assertFalse(lesson.get('meaningReviewed',False))
                self.assertFalse(lesson.get('exampleReviewed',False))

    def test_no_duplicate_general_or_rapid_promotion(self):
        general=[x for x in self.bank if x['category']=='general']
        words={x['word'] for x in general}
        self.assertEqual(len(general),len(words))
        rapid_words={x['word'] for x in self.rapid}
        self.assertEqual(len(rapid_words),len(self.rapid))
        self.assertFalse(words.intersection(rapid_words))
        self.assertEqual(self.focus['meta']['generalBreakdown']['context_draft'],len(general))

    def test_gloss_history_is_not_converted_to_false_mastery(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'data').mkdir()
            for name in ['vocabulary.json','rapid-vocabulary.json']:
                (root/'data'/name).write_text((ROOT/'data'/name).read_text())
            before=(root/'data/vocabulary.json').read_bytes()
            result=reconcile(root)
            self.assertEqual(result['promotedOverlapRemoved'],0)
            self.assertFalse(result['fullMasteryGranted'])
            self.assertEqual((root/'data/vocabulary.json').read_bytes(),before)

    def test_source_stage_idempotence(self):
        source=ROOT/'sources/authored-20261028-daily-context-sprint.jsonl'
        lines=[json.loads(x) for x in source.read_text().splitlines()]
        self.assertEqual(len(lines),178)
        self.assertEqual(lines,self.rows)
        self.assertNotIn('editorialApproved',lines[0])

if __name__=='__main__':unittest.main()
