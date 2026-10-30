#!/usr/bin/env python3
"""Conservative, reproducible editorial improvement of the 1,000-word focus deck.

91 editorially selected, CEFR-J/Octanove-source-matched replacements with original
examples.  This is an editorial relevance pass, NOT a SUBTLEX/COCA frequency
ranking or CEFR sense approval. Archived cards retain their original IDs and
content, so existing localStorage review records are not deleted or regraded.

Run from any directory: python tools/curate_daily_spoken_curriculum.py
Check only: python tools/curate_daily_spoken_curriculum.py --check
"""
from __future__ import annotations
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'sources/daily-spoken-swap-20261028.tsv'
WORDS = ROOT / 'data/vocabulary.json'
FOCUS = ROOT / 'data/fluency-focus.json'
ARCHIVE = ROOT / 'data/archived-vocabulary.json'
REPORT = ROOT / 'qa/daily-spoken-curation-report.json'


def load(p):
    return json.loads(p.read_text(encoding='utf-8'))


def save(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def changes(root=ROOT):
    paths=[root/'sources/daily-spoken-swap-20261028.tsv',root/'sources/daily-spoken-swap-stage2-20261028.tsv']
    source={r['word']:r for r in load(root/'sources/b2-c1-offline-catalog.json')}
    records=[]; seen_from=set(); seen_to=set()
    for path in paths:
      with path.open(encoding='utf-8', newline='') as fp:
        for line,parts in enumerate(csv.reader(fp, delimiter='|'), 1):
            if len(parts)!=8:raise ValueError(f'row {line}: expected 8 pipe-delimited fields')
            level,old,new,tr,definition,ex1,ex2,reason=[p.strip() for p in parts]
            if level not in ('B2','C1'):raise ValueError(f'row {line}: bad level')
            if old==new or old in seen_from or new in seen_to:raise ValueError(f'row {line}: duplicate replacement')
            if source.get(new,{}).get('levelCandidate')!=level:raise ValueError(f'{new}: not sourced as {level} candidate')
            if len(tr)<3 or min(map(len,(definition,ex1,ex2,reason)))<8 or len(definition)<30:
                raise ValueError(f'{new}: incomplete meanings or examples')
            if ex1==ex2 or any(len(x)<25 or x[-1] not in '.!?' for x in (ex1,ex2)):
                raise ValueError(f'{new}: examples must be distinct full sentences')
            seen_from.add(old);seen_to.add(new)
            records.append(dict(level=level,old=old,new=new,tr=tr,definition=definition,examples=[ex1,ex2],reason=reason))
    if len(records)!=91 or Counter(x['level'] for x in records)!={'B2':55,'C1':36}:
        raise ValueError('Expected exactly 55 B2 + 36 C1 replacements')
    return records


def evaluate(root=ROOT, write=False):
    proposals=changes(root)
    vocab=load(root/'data/vocabulary.json')
    focus=load(root/'data/fluency-focus.json')
    a=root/'data/archived-vocabulary.json'
    archive=load(a) if a.exists() else []
    live={x['word']:x for x in vocab if x.get('category')=='general'}
    retired={x['word']:x for x in archive}
    original_focus={x['word']:x for x in focus['vocabulary']}
    origin_ids={x['id'] for x in vocab} | {x['id'] for x in archive}
    updates=[]; retired_rows=[]; new_rows=[]
    for r in proposals:
        old,new,level=r['old'],r['new'],r['level']
        if old in original_focus and new not in original_focus:
            if old not in live or live[old]['level']!=level or new in live:
                raise ValueError(f'{old}/{new}: unexpected state before replacement')
            record=live[old].copy()
            record['archivedFromFocus']=True
            record['archivedReason']='replaced in editorial daily-conversation priority shortlist'
            record['replacedBy']=new
            retired_rows.append(record)
            id_='g-'+new.replace(' ','-')
            if id_ in origin_ids:raise ValueError(f'{new}: ID collision')
            origin_ids.add(id_)
            replacement={'id':id_,'word':new,'tr':r['tr'],'definition':r['definition'],
                         'example':r['examples'][0], 'level':level,'category':'general',
                         'priority':record.get('priority',0),
                         'prompt':f'Use “{new}” in a situation from your own life.',
                         'examples':r['examples'], 'editorialStatus':'authored_unreviewed',
                         'meaningReviewed':False,'exampleReviewed':False,
                         'cefrSenseVerified':False,'spokenFrequencyVerified':False,
                         'selectionBasis':'editorial everyday-conversation usefulness, frequency unverified',
                         'cefrHeadwordSource':'CEFR-J/Octanove local source-candidate catalog',
                         'editorialContext':r['reason']}
            new_rows.append(replacement)
            updates.append(dict(old=old,new=new,level=level,reason=r['reason'],status='replaced'))
        elif new in original_focus and old not in original_focus:
            if new not in live or old not in retired or retired[old]['replacedBy']!=new:
                raise ValueError(f'{old}/{new}: mismatched previously applied replacement')
            updates.append(dict(old=old,new=new,level=level,reason=r['reason'],status='already_applied'))
        else:raise ValueError(f'{old}/{new}: cannot safely determine focus migration')
    if new_rows:
        remove={r['old'] for r in updates if r['status']=='replaced'}
        vocab=[x for x in vocab if x['word'] not in remove]+new_rows
        archive+=retired_rows
        old_to_new={x['old']:x['new'] for x in updates if x['status']=='replaced'}
        new_by_word={x['word']:x for x in new_rows}
        new_focus=[]
        for row in focus['vocabulary']:
            if row['word'] not in old_to_new:new_focus.append(row);continue
            w=old_to_new[row['word']];v=new_by_word[w]
            new_focus.append({'word':w,'level':v['level'],'status':'context_draft',
                              'editorialApproved':False,'selectionBasis':v['selectionBasis'],
                              'lessonId':v['id'],'cefrVerified':False,'spokenFrequencyVerified':False})
        focus['vocabulary']=new_focus
        focus['meta']['selectionPolicy']='Editorial daily-conversation relevance; 91 sourced replacements. Spoken US corpus ranking and sense-specific CEFR approval still pending.'
        focus['meta']['spokenFrequencyValidated']=False
        focus['meta']['editorialCurationRevision']='daily-spoken-swap-20261028'
    active=[x for x in vocab if x.get('category')=='general']
    selected=focus['vocabulary']
    if (len(active)!=1000 or Counter(x['level'] for x in active)!={'B2':500,'C1':500}
            or {x['word'] for x in active}!={x['word'] for x in selected}
            or len({x['id'] for x in active})!=1000):
        raise AssertionError('Focus invariants violated')
    if any(x.get('editorialStatus')=='approved' for x in active):
        raise AssertionError('Curation must not grant human approval')
    if len({x['word'] for x in archive})!=len(archive):raise AssertionError('Duplicate archived cards')
    report={'method':'sourced-headword, original draft examples, qualitative conversational editorial prioritization',
            'newReplacements':sum(x['status']=='replaced' for x in updates),
            'previouslyApplied':sum(x['status']=='already_applied' for x in updates),
            'reviewedReplacements':len(updates),'generalActive':len(active),'generalB2':500,'generalC1':500,
            'archiveEntries':len(archive),'corpusFrequencyVerified':0,'cefrSenseVerified':0,
            'humanEditoriallyApproved':0,'releaseAllowed':False,
            'learnerHistory':'Existing IDs kept in archive and localStorage remains untouched; no automatic mastery transfer to replacement IDs.',
            'replacements':updates}
    if write:
        if new_rows:
            save(root/'data/vocabulary.json',vocab)
            save(root/'data/fluency-focus.json',focus)
            save(a,archive)
        save(root/'qa/daily-spoken-curation-report.json',report)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    result=evaluate(write=not args.check)
    print(json.dumps({k:v for k,v in result.items() if k!='replacements'},ensure_ascii=False,indent=2))
