"""No-loss daily-spoken curriculum swaps and release-safety checks."""
import json
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from curate_daily_spoken_curriculum import changes,evaluate


class DailySpokenCurationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.replacements=changes()
        cls.words=json.loads((ROOT/'data/vocabulary.json').read_text())
        cls.focus=json.loads((ROOT/'data/fluency-focus.json').read_text())
        cls.archive=json.loads((ROOT/'data/archived-vocabulary.json').read_text())
        cls.rapid=json.loads((ROOT/'data/rapid-vocabulary.json').read_text())
        cls.catalog={x['word']:x for x in json.loads((ROOT/'sources/b2-c1-offline-catalog.json').read_text())}

    def test_replacements_are_sourced_and_full_context_drafts(self):
        active={x['word']:x for x in self.words if x['category']=='general'}
        previous={x['word']:x for x in self.archive}
        focus={x['word']:x for x in self.focus['vocabulary']}
        self.assertEqual(Counter(x['level'] for x in self.replacements),{'B2':55,'C1':36})
        self.assertEqual(len(self.archive),91)
        for item in self.replacements:
            with self.subTest(replacement=item['new']):
                self.assertNotIn(item['old'],active)
                self.assertNotIn(item['old'],focus)
                self.assertIn(item['old'],previous)
                self.assertTrue(previous[item['old']]['archivedFromFocus'])
                self.assertEqual(previous[item['old']]['replacedBy'],item['new'])
                self.assertEqual(previous[item['old']]['id'],'g-'+item['old'])
                self.assertEqual(self.catalog[item['new']]['levelCandidate'],item['level'])
                lesson=active[item['new']]
                self.assertEqual(lesson['tr'],item['tr'])
                self.assertEqual(lesson['level'],item['level'])
                self.assertEqual(lesson['examples'],item['examples'])
                self.assertEqual(len(set(lesson['examples'])),2)
                self.assertEqual(lesson['editorialStatus'],'authored_unreviewed')
                self.assertFalse(lesson['meaningReviewed'])
                self.assertFalse(lesson['spokenFrequencyVerified'])
                self.assertFalse(focus[item['new']]['editorialApproved'])
                self.assertEqual(focus[item['new']]['lessonId'],lesson['id'])

    def test_no_collision_no_rapid_duplicates_and_unchanged_total(self):
        active=[x for x in self.words if x['category']=='general']
        self.assertEqual(len(active),1000)
        self.assertEqual(Counter(x['level'] for x in active),{'B2':500,'C1':500})
        self.assertEqual(len(set(x['word'] for x in active)),1000)
        self.assertEqual(len(set(x['id'] for x in active)),1000)
        self.assertEqual({x['word'] for x in active},{x['word'] for x in self.focus['vocabulary']})
        self.assertFalse({x['word'] for x in active}&{x['word'] for x in self.rapid})
        self.assertEqual(len(self.rapid),399)

    def test_idempotent_and_never_grants_approval(self):
        report=evaluate(write=False)
        self.assertEqual(report['newReplacements'],0)
        self.assertEqual(report['previouslyApplied'],91)
        self.assertFalse(report['releaseAllowed'])
        self.assertEqual(report['corpusFrequencyVerified'],0)
        self.assertEqual(report['humanEditoriallyApproved'],0)
        self.assertFalse(self.focus['meta']['publishable'])

    def test_unrecognized_candidate_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'sources').mkdir()
            path=root/'sources/daily-spoken-swap-20261028.tsv'
            path.write_text((ROOT/'sources/daily-spoken-swap-20261028.tsv').read_text().replace('|doubt|','|unverifiedfantasy|',1))
            (root/'sources/daily-spoken-swap-stage2-20261028.tsv').write_text((ROOT/'sources/daily-spoken-swap-stage2-20261028.tsv').read_text())
            (root/'sources/b2-c1-offline-catalog.json').write_bytes((ROOT/'sources/b2-c1-offline-catalog.json').read_bytes())
            with self.assertRaisesRegex(ValueError,'not sourced'):
                changes(root)

if __name__=='__main__':unittest.main()
