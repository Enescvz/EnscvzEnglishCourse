"""Unit tests for the B2/C1 bulk-import quarantine, independent of network."""
import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from bulk_curriculum import word_candidates,phrasal_candidates,report_and_save,english_form,rejected_us

class BulkCurriculumTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.dir=Path(self.tmp.name)
 def tearDown(self):self.tmp.cleanup()
 def file(self,name,data,lines=False):
  p=self.dir/name
  if lines:p.write_text('\n'.join(json.dumps(x) for x in data)+'\n',encoding='utf8')
  else:p.write_text(json.dumps(data),encoding='utf8')
  return p
 def test_level_dedup_us_and_existing(self):
  b2=self.file('B2.json',{'level':'B2','words':[{'w':'acknowledge','tr':'kabul etmek','pos':['verb']},{'w':'colour','tr':'renk'},{'w':'insight','tr':'içgörü'},{'w':'hello','tr':'merhaba'}]})
  c1=self.file('C1.json',{'level':'C1','words':[{'w':'insight','tr':'içgörü'},{'w':'contemplate','tr':'düşünmek'}]})
  vocab,rejected=word_candidates(b2,c1,existing=[{'word':'hello'}])
  self.assertEqual({v['word'] for v in vocab},{'acknowledge','insight','contemplate'})
  self.assertEqual(rejected['british_only'],1)
  self.assertEqual(rejected['already_in_curriculum'],1)
  self.assertIn('C1',next(x for x in vocab if x['word']=='insight')['levelDisagreement'])
  self.assertTrue(all(x['editorialStatus']=='candidate_unreviewed' for x in vocab))
 def test_ambiguous_senses_dont_guess_tr_mapping(self):
  b2=self.file('B2.json',{'level':'B2','words':[{'w':'conduct','tr':'yönetmek','pos':['verb']}]})
  bw=self.file('words.jsonl',[{'word':'conduct','part_of_speech':'verb','description':'To carry something out','word_level':'B2','area_variant':'common'}],True)
  meanings=self.file('meaning.jsonl',[{'word':'conduct','part_of_speech':'verb','definition':'To manage an activity','examples':['They conduct interviews.'],'sort_order':1},{'word':'conduct','part_of_speech':'verb','definition':'To transfer heat or electricity','examples':['Copper conducts electricity.'],'sort_order':2}],True)
  vocab,_=word_candidates(b2,None,bw,meanings)
  self.assertEqual(vocab[0]['definitionCandidate'],'')
  self.assertEqual(len(vocab[0]['senseCandidates']),2)
 def test_source_requires_actual_phrasal_senses_and_rejects_b1_and_uk(self):
  phrasals=self.file('phrasals.jsonl',[{'word':'carry','phrasal_variants':['carry out','carry on','carry over','carry up']}],True)
  records=[{'word':'carry out','part_of_speech':'verb','verb___is_phrasal':True,'word_level':'B2','area_variant':'american','verb___phrasal_object_pattern':'separable'},
           {'word':'carry on','part_of_speech':'verb','verb___is_phrasal':True,'word_level':'B1','verb___phrasal_object_pattern':'inseparable'},
           {'word':'carry over','part_of_speech':'verb','verb___is_phrasal':True,'word_level':'C1','area_variant':'british','verb___phrasal_object_pattern':'inseparable'},
           {'word':'carry up','part_of_speech':'verb','verb___is_phrasal':True,'word_level':'B2','verb___phrasal_object_pattern':'separable'}]
  words=self.file('bloom.jsonl',records,True)
  meanings=self.file('meaning.jsonl',[{'word':'carry out','part_of_speech':'verb','meaning_level':'B2','definition':'To complete a task after planning it carefully.','examples':['They carried out the plan.']},{'word':'carry up','part_of_speech':'verb','meaning_level':'B2','definition':'something','examples':['No suitable entry']}],True)
  pv,rejected=phrasal_candidates(words,meanings,phrasals,[])
  self.assertEqual([x['word'] for x in pv],['carry out'])
  self.assertEqual(pv[0]['syntaxCandidate'],'separable')
  self.assertEqual(pv[0]['trCandidate'],'')
  self.assertEqual(rejected['out_of_level'],1)
  self.assertEqual(rejected['regional_filter'],1)
 def test_frequency_ranks_ahead_of_alphabetic_and_missing_rank(self):
  b2=self.file('B2.json',{'level':'B2','words':[{'w':'zest','tr':'coşku'},{'w':'abrupt','tr':'ani'},{'w':'acknowledge','tr':'kabul etmek'}]})
  freq=self.file('rank.json',{'words':[{'w':'zest','rank':120},{'w':'abrupt','rank':1500}]})
  vocab,_=word_candidates(b2,None,frequency=freq)
  self.assertEqual([v['word'] for v in vocab],['zest','abrupt','acknowledge'])
  self.assertIsNone(vocab[2]['frequencyRank'])
 def test_only_appropriate_forms(self):
  self.assertFalse(english_form('a/b'))
  self.assertFalse(english_form('take off'))
  self.assertTrue(english_form('take off',True))
  self.assertTrue(rejected_us('colour'))
 def test_rejects_wrong_schema(self):
  path=self.file('bad.json',{'level':'B1','words':[]})
  with self.assertRaises(ValueError):word_candidates(path,None)
if __name__=='__main__':unittest.main()
