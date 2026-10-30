#!/usr/bin/env python3
"""Import a properly attributed bilingual CEFR vocabulary glossary into FAST study cards.

Never fabricates definitions or examples. Unlike authored lessons, gloss-only cards
only support quick EN↔TR recall and en-US device TTS. Unreviewed, not release ready.
"""
import argparse, csv, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sources/rapid-bilingual-glosses.tsv'
OUT=ROOT/'data/rapid-vocabulary.json'
REPORT=ROOT/'qa/rapid-import-report.json'


def compile_cards(rows, catalog, existing):
    candidates={x['word'].casefold():x for x in catalog}
    taught={x['word'].casefold() for x in existing if x.get('category')=='general'}
    cards=[]; seen=set(); problems=[]; overlaps=0
    for idx,row in enumerate(rows,2):
        word=row.get('word','').strip().casefold()
        tr=row.get('tr','').strip()
        if not re.fullmatch(r"[a-z][a-z' -]{1,69}",word):
            problems.append(f'row {idx}: invalid English headword')
            continue
        if word not in candidates:
            problems.append(f'row {idx}: not in B2/C1 source: {word}')
            continue
        if word in seen:
            problems.append(f'row {idx}: repeated word: {word}')
            continue
        seen.add(word)
        if len(tr)<2 or '|' in tr or '<' in tr or '>' in tr:
            problems.append(f'row {idx}: invalid Turkish gloss: {word}')
            continue
        if word in taught:
            overlaps+=1
            continue
        origin=candidates[word]
        cards.append({'id':'rapid-'+re.sub(r"[^a-z0-9]+",'-',word).strip('-'),
            'word':word,'tr':tr,'level':origin['levelCandidate'],
            'pos':origin.get('partsOfSpeech',[]),
            'origin':'EnglishPractice bilingual B2/C1 glosses crosschecked against CEFR-J/Octanove headword list',
            'source':'https://github.com/recepyagmur/EnglishPractice',
            'teachingDepth':'gloss_only','editorialStatus':'unreviewed',
            'meaningReviewed':False,'exampleReviewed':False})
    if problems: raise ValueError('Import rejected: '+str(problems[:12]))
    return cards, overlaps


def read_bilingual_json(paths):
    """A downloaded EnglishPractice B2.json/C1.json can be consumed wholesale.

    Source origin is recorded and never counts as editorial review. Any source
    level conflicts are resolved from our independently imported CEFR catalog.
    """
    extras=[]
    for path in paths:
        obj=json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(obj,dict) or not isinstance(obj.get('words'),list):
            raise ValueError(f'Invalid upstream bilingual format: {path}')
        for item in obj['words']:
            if isinstance(item,dict):
                extras.append({'word':str(item.get('w','')), 'tr':str(item.get('tr',''))})
    return extras


def main(src=SOURCE, apply=True, upstream=()):
    if not src.exists() and not upstream: raise FileNotFoundError(src)
    rows=[]
    if src.exists():
        with src.open(encoding='utf-8',newline='') as f:
            reader=csv.DictReader(f,delimiter='\t')
            if reader.fieldnames!=['word','tr']:
                raise ValueError('Expected tab-separated header word\ttr')
            rows=list(reader)
    rows.extend(read_bilingual_json(upstream))
    # A local hand-reviewed correction takes priority over the bulk source gloss.
    seen=set();unique=[]
    for row in rows:
        key=row["word"].strip().casefold()
        if key not in seen:
            unique.append(row);seen.add(key)
    rows=unique
    catalog=json.loads((ROOT/'sources/b2-c1-offline-catalog.json').read_text())
    existing=json.loads((ROOT/'data/vocabulary.json').read_text())
    cards,overlaps=compile_cards(rows,catalog,existing)
    result={'sourceRows':len(rows),'newRapidCards':len(cards),
        'overlapWithFullLessons':overlaps,'levels':{k:sum(x['level']==k for x in cards) for k in ['B2','C1']},
        'fullTeachingCardsAdded':0,'editorialApproved':0,'releaseReady':False}
    if apply:
        OUT.write_text(json.dumps(cards,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
        REPORT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=SOURCE);p.add_argument('--upstream-json',type=Path,action='append',default=[],help='Downloaded bilingual EnglishPractice B2/C1 JSON file; repeat for each level');p.add_argument('--dry-run',action='store_true');a=p.parse_args()
    print(json.dumps(main(a.input,not a.dry_run,a.upstream_json),ensure_ascii=False,indent=2))
