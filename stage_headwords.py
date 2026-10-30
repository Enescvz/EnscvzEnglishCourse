#!/usr/bin/env python3
"""Decode compact, original CEFR-J B2 and Octanove C1 word indexes.
No invented definitions are generated and no staged entries are exposed as lessons.
"""
import json, re, pathlib
from collections import Counter
ROOT=pathlib.Path(__file__).resolve().parents[1]
SRC=ROOT/'sources'

def decode(data):
    arr=[];prev=''
    for token in data.strip().split('|'):
        m=re.fullmatch(r'([0-9a-z])([a-z\x27-]+)',token)
        if not m: raise ValueError(f'Bad delta token {token[:30]}')
        n=int(m[1],36);v=prev[:n]+m[2]
        if not re.fullmatch("[a-z][a-z'-]*",v):raise ValueError(v)
        if arr and v<=arr[-1]:raise ValueError('unsorted '+v+' after '+arr[-1])
        arr.append(v);prev=v
    return arr

def main():
    rows=[];totals=Counter()
    for lev in ('B2','C1'):
        f=SRC/f'{lev.lower()}-delta.txt'
        words=decode(f.read_text(encoding='utf8'))
        totals[lev]=len(words)
        for w in words:
            rows.append({'word':w,'levelCandidate':lev,'source': 'CEFR-J Wordlist Version 1.5 (Tono Laboratory, TUFS)' if lev=='B2' else 'Octanove Vocabulary Profile C1/C2 1.0', 'status':'levelled_headword_only', 'language':'en-US'})
    existing=json.loads((ROOT/'data/vocabulary.json').read_text())
    seen={r['word'].lower() for r in existing if r.get('category')=='general'}
    unique={}
    for r in rows:
        w=r['word']
        if w not in unique:unique[w]=r
        elif unique[w]['levelCandidate']!=r['levelCandidate']:
            unique[w]['levelDisagreement']=['B2','C1']
    staged=[v for k,v in unique.items() if k not in seen]
    (SRC/'b2-c1-candidates.json').write_text(json.dumps(staged,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    report={'B2_raw':totals['B2'],'C1_raw':totals['C1'],'sourceUnique':len(unique),'existingGeneral':len(seen),'newHeadwordCandidates':len(staged),'reviewStatus':'NOT_REVIEWED_NOT_TEACHABLE','sourceUrls':['https://github.com/openlanguageprofiles/olp-en-cefrj/blob/master/cefrj-vocabulary-profile-1.5.csv','https://github.com/openlanguageprofiles/olp-en-cefrj/blob/master/octanove-vocabulary-profile-c1c2-1.0.csv']}
    (ROOT/'qa/headword-staging-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
