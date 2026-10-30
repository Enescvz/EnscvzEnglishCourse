#!/usr/bin/env python3
"""Promote the remaining 238 sourced B2/C1 gloss cards to context-lesson drafts.

The examples in sources/authored-20261028-final-*.txt are newly written
for this project, not source-dictionary example quotations. English definitions
and usage patterns await independent US-English editorial review. Source CEFR
levels are *candidates* and not verified CEFR sense certificates.

Idempotent. Never modifies learner history or confers editorial approval.
"""
from __future__ import annotations
import json
from pathlib import Path
from promote_content_batch import process

ROOT=Path(__file__).resolve().parents[1]
SOURCES=[ROOT/'sources/authored-20261028-final-b2-part1.txt',
         ROOT/'sources/authored-20261028-final-b2-part2.txt',
         ROOT/'sources/authored-20261028-final-c1.txt']


def make_rows(root=ROOT, sources=None):
    sources=sources or SOURCES
    focus=json.loads((root/'data/fluency-focus.json').read_text(encoding='utf8'))
    focused={x['word']:x for x in focus['vocabulary']}
    # Preserve validation of historical source batches when a low-value headword was retired.
    archived=root/'data/archived-vocabulary.json'
    if archived.exists():
        focused.update({x['word']:x for x in json.loads(archived.read_text())})
    rapid={x['word']:x for x in json.loads((root/'data/rapid-vocabulary.json').read_text(encoding='utf8'))}
    authored={x['word']:x for x in json.loads((root/'data/vocabulary.json').read_text(encoding='utf8')) if x.get('category')=='general'}
    if archived.exists():
        authored.update({x['word']:x for x in json.loads(archived.read_text())})
    catalog={x['word']:x for x in json.loads((root/'sources/b2-c1-offline-catalog.json').read_text(encoding='utf8'))}
    rows=[];seen=set()
    for path in sources:
        level='C1' if path.name.endswith('-c1.txt') else 'B2'
        for line,raw in enumerate(path.read_text(encoding='utf8').splitlines(),1):
            parts=[s.strip() for s in raw.split('|')]
            if len(parts)!=4:raise ValueError(f'{path.name}:{line}: expected four fields, got {len(parts)}')
            word,definition,example1,example2=parts
            if word in seen:raise ValueError(f'duplicate in source: {word}')
            seen.add(word)
            if word not in focused or focused[word]['level']!=level:
                raise ValueError(f'{word}: not in the focused {level} curriculum')
            if word not in rapid and word not in authored:
                raise ValueError(f'{word}: neither a bilingual gloss nor a promoted lesson')
            source_card=rapid.get(word) or authored.get(word)
            if source_card['level']!=level:
                raise ValueError(f'{word}: level differs from the sourced gloss / authored lesson')
            if word not in catalog or catalog[word]['levelCandidate']!=level:
                raise ValueError(f'{word}: missing corresponding CEFR source candidate')
            if len(definition)<30 or len(example1)<25 or len(example2)<25 or example1==example2:
                raise ValueError(f'{word}: empty, short, or duplicate contexts')
            if not all(s.rstrip(chr(34) + chr(39) + '”’')[-1] in '.!?' for s in (example1,example2)):
                raise ValueError(f'{word}: example needs sentence punctuation')
            rows.append(dict(word=word,level=level,tr=source_card['tr'],definition=definition,
                example=example1,examples=[example1,example2],
                levelStatus='source_candidate_unreviewed',meaningReviewed=False,exampleReviewed=False,
                prompt=f'Use “{word}” in a situation from your own life.'))
    if len(rows)!=238 or sum(x['level']=='B2' for x in rows)!=183 or sum(x['level']=='C1' for x in rows)!=55:
        raise ValueError('Final batch must have exactly 183 B2 and 55 C1 distinct sourced entries')
    return rows


def apply():
    rows=make_rows()
    target=ROOT/'sources/authored-20261028-final-focus-238.jsonl'
    target.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf8')
    current={x['word'] for x in json.loads((ROOT/'data/vocabulary.json').read_text()) if x.get('category')=='general'}
    pending=[r for r in rows if r['word'] not in current]
    if pending:
        temp=ROOT/'sources/.final-focus-238-pending.jsonl'
        temp.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in pending),encoding='utf8')
        try:out=process(temp,'general',apply=True)
        finally:temp.unlink(missing_ok=True)
    else:out={'validatedNewCards':0,'mode':'already_applied'}
    print(json.dumps(dict(authored=len(rows),new=len(pending),imported=out),ensure_ascii=False))

if __name__=='__main__':apply()
