#!/usr/bin/env python3
"""Remove answer-position shortcuts from Reading and Grammar without changing correct content.

Deterministically assigns the correct option across A/B/C/D. Idempotent, keeps IDs,
explanations, and the right answer text intact. Does not certify semantic accuracy.
"""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def place_at(options,answer_idx,target_idx):
    if len(options)!=4 or answer_idx not in range(4) or target_idx not in range(4):
        raise ValueError('Invalid answer/options shape')
    correct=options[answer_idx]
    ordered=[o for i,o in enumerate(options) if i!=answer_idx]
    ordered.insert(target_idx,correct)
    if ordered[target_idx]!=correct or len(set(ordered))!=4:
        raise ValueError('Question options became ambiguous')
    return ordered

def rebalance():
    rpath=ROOT/'data/readings.json';gpath=ROOT/'data/grammar.json'
    readings=json.loads(rpath.read_text(encoding='utf-8'))
    grammar=json.loads(gpath.read_text(encoding='utf-8'))
    for li,lesson in enumerate(readings):
        for qi,q in enumerate(lesson['questions']):
            target=(li*len(lesson['questions'])+qi)%4
            q['options']=place_at(q['options'],q['answer'],target)
            q['answer']=target
    for i,g in enumerate(grammar):
        idx=g.get('answerIndex',0)
        if g['options'][idx]!=g['answer']:
            raise ValueError('Incorrect grammar key: '+g['id'])
        target=i%4
        g['options']=place_at(g['options'],idx,target)
        g['answerIndex']=target
    for p,obj in ((rpath,readings),(gpath,grammar)):
        p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {'readingOptions':dict(Counter(q['answer'] for e in readings for q in e['questions'])),
            'grammarOptions':dict(Counter(g['answerIndex'] for g in grammar))}
if __name__=='__main__':print(json.dumps(rebalance(),indent=2))
