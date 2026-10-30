#!/usr/bin/env python3
"""Mark high-utility, foundational phrases for placement before advanced study.

This is an editorial study-priority tag, not a validated CEFR or corpus rating.
Retains all card IDs, definitions, examples, and history.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
FOUNDATIONAL={
    'get up','look for','go out','go away','go down','come in','come on',
    'get in','get out','take out','turn on','turn off','wake up',
}

def apply(write=True):
    focus_path=ROOT/'data/fluency-focus.json'
    lessons_path=ROOT/'data/phrasals.json'
    focus=json.loads(focus_path.read_text(encoding='utf-8'))
    lessons=json.loads(lessons_path.read_text(encoding='utf-8'))
    selected={item['word'] for item in focus['phrasals']}
    if not FOUNDATIONAL <= selected:
        raise AssertionError(f'Placement phrases missing: {FOUNDATIONAL-selected}')
    linked={item['word']:item for item in lessons}
    for item in focus['phrasals']:
        word=item['word']
        if word in FOUNDATIONAL:
            item.update({
                'placementCheckFirst':True,
                'priorityLane':'foundational-high-utility-check',
                'level':'B1',
                'cefrVerified':False,
                'levelBasis':'editorial foundational estimate; requires sense-level validation',
                'editorialApproved':False,
            })
            if word not in linked:raise AssertionError(f'No lesson for {word}')
            linked[word].update({
                'placementCheckFirst':True,
                'priorityLane':'foundational-high-utility-check',
                'level':'B1',
                'cefrVerified':False,
                'levelBasis':'editorial foundational estimate; requires sense-level validation',
            })
    focus['meta']['foundationalPhrasalsPlacementFirst']=len(FOUNDATIONAL)
    focus['meta']['advancedPhrasalPriority']=len(focus['phrasals'])-len(FOUNDATIONAL)
    focus['meta']['foundationalPhasing']='Common foundational phrases retained for placement-first review, rather than being misrepresented as verified B2 content.'
    if write:
        focus_path.write_text(json.dumps(focus,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        lessons_path.write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {'placementFirst':len(FOUNDATIONAL),'advancedPhrasalPriority':len(focus['phrasals'])-len(FOUNDATIONAL),'phrasalTotal':len(focus['phrasals'])}

if __name__=='__main__':print(json.dumps(apply(),indent=2))
