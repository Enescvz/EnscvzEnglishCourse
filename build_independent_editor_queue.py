#!/usr/bin/env python3
"""Make reproducible human-review queue. Never fabricates editorial approval."""
import csv
import json
import re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'qa'/'20261030-editor-review'
OUT.mkdir(parents=True,exist_ok=True)
vocab=json.loads((ROOT/'data/vocabulary.json').read_text(encoding='utf-8')) + json.loads((ROOT/'data/toefl-academic.json').read_text(encoding='utf-8'))
phrasals=json.loads((ROOT/'data/phrasals.json').read_text(encoding='utf-8'))
expressions=json.loads((ROOT/'data/daily-expressions.json').read_text(encoding='utf-8'))['cards']
toe=json.loads((ROOT/'data/toefl-core.json').read_text(encoding='utf-8'))
words=set(toe['wordLessonIds']);pvs=set(toe['phrasalLessonIds'])
rows=[]
for kind,collection in [('vocabulary',vocab),('phrasal',phrasals),('expression',expressions)]:
  for item in collection:
    if kind=='vocabulary' and item.get('id') not in words:continue
    if kind=='phrasal' and item.get('id') not in pvs:continue
    if kind=='expression' and not item.get('id'):continue
    term=item.get('expression') or item.get('word','')
    examples=item.get('examples') or ([item['example']] if item.get('example') else [])
    meanings=item.get('tr') or ''
    flags=[]
    if not term.strip():flags.append('empty_term')
    if not meanings.strip():flags.append('empty_translation')
    if not item.get('definition') and not item.get('usageNote'):flags.append('no_usage_note')
    if len(examples)!=2 or len({re.sub(r'\s+',' ',x.strip().casefold()) for x in examples})!=2:flags.append('needs_two_distinct_examples')
    if len(examples)==2 and any(len(x.strip().split())<3 for x in examples):flags.append('short_example')
    if any('lorem ipsum' in x.casefold() for x in examples):flags.append('placeholder_text')
    if kind=='expression' and len(item.get('dialogue') or [])<2:flags.append('missing_two_speaker_dialogue')
    rows.append({'kind':kind,'id':item['id'],'term':term,'level':item.get('level',''),
      'meaning':meanings,'example1':examples[0] if examples else '',
      'example2':examples[1] if len(examples)>1 else '',
      'automaticFlags':';'.join(flags),'humanTranslationApproved':'',
      'humanUsageApproved':'','humanLevelApproved':'','reviewer':'','reviewDate':'','reviewNotes':''})
expected=400+75+500
assert len(rows)==expected, (len(rows),expected)
with (OUT/'review-queue.csv').open('w',newline='',encoding='utf-8-sig') as f:
 writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
counts=Counter(r['automaticFlags'] for r in rows if r['automaticFlags'])
summary={'scope':'400 TOEFL words, 75 TOEFL phrasals, 500 daily expressions',
         'machineChecked':len(rows),'independentHumanApproval':False,
         'humanReviewCompleted':0,'automaticFlagged':sum(counts.values()),
         'flags':dict(counts),
         'notes':'Automatic consistency audit is not editorial signoff; no user progress or original card IDs changed.'}
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Full-curriculum secondary audit for non-TOEFL general/finance and other cards;
# 975-card priority queue above remains intact and preserves its stable IDs.
whole=[]
for kind,collection in [('vocabulary',vocab),('phrasal',phrasals),('expression',expressions)]:
  for item in collection:
    key=item.get('id');term=item.get('expression') or item.get('word','')
    examples=item.get('examples') or ([item['example']] if item.get('example') else [])
    whole.append({'kind':kind,'id':key,'term':term,'level':item.get('level',''),
      'translation':item.get('tr',''), 'example1':examples[0] if examples else '',
      'example2':examples[1] if len(examples)>1 else '',
      'humanMeaningApproved':'', 'humanUsageApproved':'', 'humanExamplesApproved':'',
      'reviewer':'','date':'','notes':''})
assert len(whole)==len(vocab)+len(phrasals)+len(expressions)
assert len({(x['kind'],x['id']) for x in whole})==len(whole)
with (OUT/'full-curriculum-review-queue.csv').open('w',newline='',encoding='utf-8-sig') as f:
  writer=csv.DictWriter(f,fieldnames=list(whole[0]));writer.writeheader();writer.writerows(whole)
summary['fullCurriculumAuditQueueItems']=len(whole)
(OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
