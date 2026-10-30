"""Tests for original CEFR files and bulk phrase stage parser."""
import importlib.util,tempfile,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('fast_source_import',Path(__file__).resolve().parents[1]/'tools/fast_source_import.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
class ImportTests(unittest.TestCase):
 def test_b2_and_us_filter(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'b.csv';p.write_text('headword,pos,CEFR\ncolour,noun,B2\naccountant,noun,B2\nhello,interjection,A1\nmerit,noun,C1\n')
   rows=mod.rows_from_csv(p,'B2');self.assertEqual([r['word'] for r in rows],['accountant'])
 def test_phrasal_and_first_definition(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'p.txt';p.write_text('come across - find unexpectedly\ncome across - create an impression\nlook (something) up - find info\naccount for - explain\n')
   rows=mod.parse_phrasals(p);self.assertEqual(len(rows),2);self.assertEqual(rows['come across'],'find unexpectedly')
if __name__=='__main__':unittest.main()
