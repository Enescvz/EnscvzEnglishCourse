#!/usr/bin/env python3
"""Reproducible editorial triage, not a claim of corpus frequency or human review."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data';QA=ROOT/'qa'
def load(name):return json.loads((DATA/name).read_text(encoding='utf-8'))
def audit():
 core=load('toefl-core.json');words=load('vocabulary.json')+load('toefl-academic.json');phrasals=load('phrasals.json')
 by_id={x['id']:x for x in words+phrasals}
 assert len(by_id)==len(words)+len(phrasals),'Duplicate card IDs in curriculum'
 assert (len(core['wordLessonIds']),len(core['phrasalLessonIds']))==(400,75)
 ids=core['wordLessonIds']+core['phrasalLessonIds']
 assert len(set(ids))==475,'Duplicate TOEFL focus ID'
 assert all(x in by_id for x in ids),'Unresolvable existing card ID'
 review=[];less_than_two=[];nonempty_def=0
 for kind,arr in [('word',core['wordLessonIds']),('phrasal',core['phrasalLessonIds'])]:
  for itemid in arr:
   x=by_id[itemid];examples=[s for s in x.get('examples',[]) if isinstance(s,str) and s.strip()]
   if len(examples)<2:less_than_two.append(itemid)
   definition=bool(x.get('definition','').strip())
   nonempty_def+=definition
   review.append({'id':itemid,'kind':kind,'headword':x['word'],'levelCandidate':x.get('level',''),
     'currentEditorialStatus':x.get('editorialStatus','unknown'),
     'englishDefinitionAvailable':definition,'originalExamples':len(examples),
     'spokenUSFrequencyRank':'NOT_MEASURED','TOEFLExamFrequencyRank':'NOT_AVAILABLE',
     'senseAndRegisterReview':'PENDING_HUMAN','independentEditorApproval':'PENDING',
     'sourceLicenseReview':'PENDING_PER_ITEM','recommendedAction':'Check US spoken and academic senses, examples and register without replacing card ID'})
 QA.mkdir(exist_ok=True)
 columns=list(review[0]);withopen=QA/'toefl-475-independent-review-queue.csv'
 with withopen.open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(review)
 result={'audit':'metadata_and_internal_structural_audit_only','reviewScope':475,
  'words':400,'phrasalVerbs':75,'resolvableExistingIDs':475,'englishDefinitionsPresent':nonempty_def,
  'cardsWithFewerThanTwoExamples':less_than_two,
  'corpusUSFrequencyMeasured':False,'TOEFLFrequencyMeasured':False,'humanEditorApproved':0,
  'reviewQueue':'qa/toefl-475-independent-review-queue.csv','releaseApproved':False}
 (QA/'toefl-core-editorial-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))
