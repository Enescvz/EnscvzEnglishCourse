#!/usr/bin/env python3
"""Validate authored JSONL vocabulary/phrasal lessons for safe batch promotion.

DRY RUN BY DEFAULT. `--apply` explicitly updates data/*.json, preserving existing
IDs, orders and progress. Does NOT grant editorial approval or pass release lock.
An origin in sources/*-production-queue.json is required for every imported word.
This protects students from source HEADWORD_ONLY records masquerading as cards.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SINGLE = re.compile(r"[a-z][a-z' -]{1,69}")
PV_SYNTAX = {'separable','inseparable','intransitive'}
REQUIRED = {'word','tr','definition','example','examples','level'}


def load(path):
    return json.loads(path.read_text(encoding='utf8'))


def read_jsonl(path):
    records=[]
    for line,raw in enumerate(path.read_text(encoding='utf8').splitlines(),1):
        if not raw.strip():continue
        try:obj=json.loads(raw)
        except json.JSONDecodeError as exc:raise ValueError(f'Line {line}: invalid JSON') from exc
        if not isinstance(obj,dict):raise ValueError(f'Line {line}: record must be object')
        records.append(obj)
    if not records:raise ValueError('No input records')
    return records


def validate_record(rec,kind,authorized):
    word=rec.get('word','').strip().lower()
    if not SINGLE.fullmatch(word):raise ValueError(f'{word}: invalid word form')
    if word not in authorized:raise ValueError(f'{word}: not present in the sourced production queue')
    if rec.get('level') not in ('B2','C1'):raise ValueError(f'{word}: B2/C1 source level required')
    for field in REQUIRED:
        if field not in rec:raise ValueError(f'{word}: missing {field}')
    if not isinstance(rec['tr'],str) or len(rec['tr'].strip())<2:raise ValueError(f'{word}: missing Turkish meaning')
    if not isinstance(rec['definition'],str) or len(rec['definition'].strip())<30:raise ValueError(f'{word}: insufficient English definition')
    if not isinstance(rec['example'],str) or len(rec['example'].strip())<25:raise ValueError(f'{word}: insufficient original example')
    ex=rec['examples']
    if not isinstance(ex,list) or len(ex)<2 or ex[0]!=rec['example'] or len(set(ex))!=len(ex) or any(not isinstance(e,str) or len(e)<25 for e in ex):
        raise ValueError(f'{word}: two distinct contextual examples required, first matching example')
    if rec.get('editorialStatus')=='approved':raise ValueError(f'{word}: automatic editorial approval forbidden')
    if kind=='phrasal':
        if rec.get('syntax') not in PV_SYNTAX:raise ValueError(f'{word}: phrasal syntax required')
        if not rec.get('register') or not rec.get('note'):raise ValueError(f'{word}: register and syntax note required')
        senses=rec.get('senses',[])
        if not senses or not all(isinstance(s,dict) and isinstance(s.get('tr'),str) and len(s.get('definition',''))>=30 and len(s.get('example',''))>=25 for s in senses):
            raise ValueError(f'{word}: every phrasal sense needs meaning, definition, example')
    return word


def process(path,kind,apply=False,root=ROOT):
    if kind not in ('general','phrasal'):raise ValueError('unknown content type')
    bank=root/'data'/('vocabulary.json' if kind=='general' else 'phrasals.json')
    queue=root/'sources'/('general-production-queue.json' if kind=='general' else 'phrasal-production-queue.json')
    authorized={x['word'].casefold():x for x in load(queue)}
    # The old phrasal-production-queue.json was built for a 600-item historical
    # target. The current user-approved 500-focus shortlist differs. Accept
    # additional focus headwords ONLY if they also appear in our provenance
    # catalog; never authorize arbitrary user-supplied or unsourced phrases.
    if kind=='phrasal' and (root/'data/fluency-focus.json').is_file() and (root/'sources/phrasal-candidates.json').is_file():
        focus={x['word'].casefold() for x in load(root/'data/fluency-focus.json')['phrasals']}
        for item in load(root/'sources/phrasal-candidates.json'):
            w=item['word'].casefold()
            if w in focus and w not in authorized:
                authorized[w]={'word':w,'levelCandidate':item.get('levelCandidate')}
    # The focused general shortlist can legitimately contain CEFR-J/Octanove
    # headwords outside the legacy 3,500-item production queue. Authorize ONLY
    # those independently present in the imported CEFR source with the exact
    # focus level. Never authorize an arbitrary free-form headword.
    if kind=='general' and (root/'data/fluency-focus.json').is_file() and (root/'sources/b2-c1-offline-catalog.json').is_file():
        focus={x['word'].casefold():x['level'] for x in load(root/'data/fluency-focus.json')['vocabulary']}
        for item in load(root/'sources/b2-c1-offline-catalog.json'):
            w=item['word'].casefold()
            if w in focus and w not in authorized and item.get('levelCandidate')==focus[w]:
                authorized[w]={'word':w,'levelCandidate':focus[w],'origin':'CEFR sourced offline catalog'}
    original=load(bank)
    existing={x['word'].casefold() for x in original if kind=='phrasal' or x.get('category')=='general'}
    input_records=read_jsonl(path)
    staged=[]; seen=set()
    for rec in input_records:
        w=validate_record(rec,kind,authorized)
        if w in seen:raise ValueError(f'{w}: duplicate input word')
        seen.add(w)
        if w in existing:raise ValueError(f'{w}: existing content must be updated in place, not duplicated')
        if kind=='general' and authorized[w].get('levelCandidate')!=rec['level']:
            raise ValueError(f'{w}: CEFR level disagrees with source, resolve before import')
        if kind=='phrasal' and authorized[w].get('levelCandidate') is None and not rec.get('levelEvidence'):
            raise ValueError(f'{w}: unknown CEFR level; levelEvidence required')
        obj={k:v for k,v in rec.items() if k not in ('id','editorialStatus','category','priority')}
        obj['id']=('g-' if kind=='general' else 'pv-')+re.sub(r'[^a-z0-9]+','-',w).strip('-')
        obj['word']=w
        obj['priority']=max((int(x.get('priority',0)) for x in original),default=0)+1+len(staged)
        obj['editorialStatus']='authored_unreviewed'
        if kind=='general':obj['category']='general'
        staged.append(obj)
    existing_ids={x['id'] for x in original}
    if any(x['id'] in existing_ids for x in staged):raise ValueError('ID collisions; resolve before import')
    report={'mode':'applied' if apply else 'dry-run','kind':kind,'sourceFile':str(path.name),
            'validatedNewCards':len(staged),'existingCardsUntouched':len(original),
            'editoriallyApprovedNewCards':0,'releaseReady':False}
    if apply:
        bank.write_text(json.dumps(original+staged,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return report


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',type=Path,required=True)
    ap.add_argument('--kind',choices=('general','phrasal'),required=True)
    ap.add_argument('--apply',action='store_true',help='Explicitly append after validation; never auto-approve')
    args=ap.parse_args()
    print(json.dumps(process(args.input,args.kind,args.apply),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
