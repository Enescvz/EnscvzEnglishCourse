#!/usr/bin/env python3
"""Offline automated checks. Does NOT assess semantic accuracy, idiomaticity, dialect or CEFR level.
Writes a machine-readable editorial queue; never marks a card reviewed.
"""
from pathlib import Path
from collections import Counter
import json,re
ROOT=Path(__file__).resolve().parents[1]
vocab=json.loads((ROOT/'data/vocabulary.json').read_text())
phrasals=json.loads((ROOT/'data/phrasals.json').read_text())
items=vocab+phrasals
placeholder=re.compile(r'^(The investor considered|The finance department documented|The investment analyst discussed)\b',re.I)
issues=[]
for card in items:
 examples=card.get('examples') or []
 if not examples:issues.append({'id':card['id'],'reason':'no_context_example'})
 if len(examples)<2:issues.append({'id':card['id'],'reason':'needs_second_distinct_example'})
 if len(set(examples))!=len(examples):issues.append({'id':card['id'],'reason':'duplicate_example'})
 if examples and card.get('example')!=examples[0]:issues.append({'id':card['id'],'reason':'primary_mismatch'})
 for i,text in enumerate(examples):
  if len(text)<20 or not text.endswith(('.', '?', '!')):
   issues.append({'id':card['id'],'reason':'malformed_example','index':i})
  if placeholder.search(text):issues.append({'id':card['id'],'reason':'boilerplate','index':i})
  if '<' in text or '>' in text:issues.append({'id':card['id'],'reason':'html_safety_review','index':i})
 if card.get('editorialStatus')!='authored_unreviewed':issues.append({'id':card['id'],'reason':'review_status_misrepresentation'})
report={
 'manualSemanticVerification':'not_performed',
 'automaticStructuralChecksOnly':True,
 'counts':{'vocabulary':len(vocab),'phrasals':len(phrasals),'general':sum(v['category']=='general' for v in vocab),'specialist':sum(v['category']!='general' for v in vocab),'entriesWithAtLeastOneExample':sum(bool(v.get('examples')) for v in items),'entriesWithAtLeastTwoExamples':sum(len(v.get('examples',[]))>=2 for v in items),'totalDistinctContextSentences':sum(len(set(v.get('examples',[]))) for v in items)},
 'issueBreakdown':dict(Counter(x['reason'] for x in issues)),
 'issues':issues,
}
folder=ROOT/'qa';folder.mkdir(exist_ok=True)
(folder/'example_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='issues'},ensure_ascii=False,indent=2))
