#!/usr/bin/env python3
"""Create a small browser-visible *research* catalog, never teaching cards.

All source headwords are quarantined. No invented meanings or CEFR tags for
phrasal verbs; approved learning cards continue to reside in data/*.json.
"""
from pathlib import Path
from collections import Counter
import json

ROOT=Path(__file__).resolve().parents[1]

def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))

def compile_catalog(vocab, phrasals, lessons, pv_lessons):
    existing={(x['category'],x['word'].casefold()):x['id'] for x in lessons}
    existing_pv={x['word'].casefold():x['id'] for x in pv_lessons}
    entries=[];seen=set()
    for v in vocab:
        word=v['word'].strip().lower(); key=('vocabulary',word)
        if key in seen:raise ValueError(f'duplicate {key}')
        seen.add(key)
        level=v.get('levelCandidate')
        if level not in ('B2','C1'):raise ValueError(f'invalid vocab level {word}: {level}')
        entries.append({'w':word,'t':'v','l':level,'levels':v.get('candidateLevels',[level]),
            'pos':v.get('partsOfSpeech',[]),'arp':v.get('americanPronunciationCandidateARPAbet',''),
            'lesson':existing.get(('general',word),''), 's':'CEFR-J' if level=='B2' else 'Octanove'})
    for v in phrasals:
        word=v['word'].strip().lower();key=('phrasal',word)
        if key in seen:raise ValueError(f'duplicate {key}')
        seen.add(key)
        # Source contains many combinations which are not strictly phrasal verbs.
        entries.append({'w':word,'t':'p','l':None,'levels':[],
            'arp':v.get('americanPronunciationCandidateARPAbet',''),
            'lesson':existing_pv.get(word,''),'s':'tema4p'})
    entries.sort(key=lambda x:(x['t'],x['w']))
    return entries

def main():
    entries=compile_catalog(read('sources/b2-c1-offline-catalog.json'),read('sources/phrasal-candidates.json'),read('data/vocabulary.json'),read('data/phrasals.json'))
    stats={'total':len(entries),'vocabulary':sum(x['t']=='v' for x in entries),'phrasal':sum(x['t']=='p' for x in entries),
        'lessonOverlaps':sum(bool(x['lesson']) for x in entries),'unreviewed':len(entries),
        'status':'RESEARCH_HEADWORDS_ONLY_NO_TEACHING_CREDIT', 'version':1}
    (ROOT/'data/candidate-catalog.json').write_text(json.dumps({'meta':stats,'entries':entries},ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    (ROOT/'qa/candidate-catalog-build.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=False,indent=2))
    return stats
if __name__=='__main__':main()
