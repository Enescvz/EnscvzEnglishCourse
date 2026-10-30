"""Additional non-publishing structural QA for 500 daily expressions."""
import json
import re
import unittest
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BANK=json.loads((ROOT/'data/daily-expressions.json').read_text(encoding='utf8'))
ADDED=BANK['cards'][300:]

class DailyExpressions500ExtraTests(unittest.TestCase):
 def test_500_target_and_new_category_mix(self):
  self.assertEqual(len(BANK['cards']),500)
  self.assertEqual(BANK['meta']['targetTotal'],500)
  self.assertEqual(Counter(x['level'] for x in BANK['cards']),{'B1':150,'B2':210,'C1':140})
  self.assertEqual(Counter(x['category'] for x in ADDED),{'connectors':80,'collocations':70,'conversation_starters':50})
 def test_source_reproducible_and_editorially_pending(self):
  lines=(ROOT/'sources/daily-expressions-200-additions-20261029.tsv').read_text(encoding='utf8').splitlines()
  self.assertEqual(len(lines),200)
  for item,line in zip(ADDED,lines):
   parts=line.split('|')
   self.assertEqual(len(parts),7)
   self.assertEqual(item['expression'],parts[2]);self.assertEqual(item['tr'],parts[3])
   self.assertEqual(item['examples'],parts[4:6])
   self.assertEqual(item['editorialStatus'],'authored_pending_independent_review')
   self.assertEqual(item['audioStatus'],'not_provided')
  self.assertFalse(BANK['meta']['independentEditorApproved'])
  self.assertEqual(BANK['meta']['approvedHumanVoiceCount'],0)
 def test_no_duplicate_ids_or_overlapping_existing_headwords(self):
  ids=[x['id'] for x in BANK['cards']];self.assertEqual(len(ids),len(set(ids)))
  norm=lambda x:re.sub('[^a-z0-9]','',x.lower())
  expressions=[norm(x['expression']) for x in BANK['cards']]
  self.assertEqual(len(expressions),len(set(expressions)))
  existing=[x['word'] for name in ('vocabulary','phrasals') for x in json.loads((ROOT/f'data/{name}.json').read_text())]
  self.assertFalse(set(expressions)&set(map(norm,existing)))
 def test_usage_tags_are_classification_not_exam_frequency_claim(self):
  legacy=BANK['meta']['legacyToeflDailyIds']
  self.assertEqual(len(legacy),len(set(legacy)))
  self.assertTrue(set(legacy)<=set(x['id'] for x in BANK['cards'][:300]))
  for x in ADDED:
   self.assertIn('daily',x['contexts'])
   self.assertTrue(set(x['contexts'])<=set(['daily','toefl']))
  self.assertIn('not measured exam frequency',BANK['meta']['description'])
if __name__=='__main__':unittest.main()
