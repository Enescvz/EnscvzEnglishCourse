#!/usr/bin/env python3
"""Drop quick-only display duplicates when an authored full lesson now exists.

This does not touch student localStorage, exported progress or browser histories.
Rapid IDs remain addressable in exported progress; they are not silently
translated into context mastery (recognition is not productive proficiency).
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def reconcile(root=ROOT):
    vocab=json.loads((root/'data/vocabulary.json').read_text(encoding='utf8'))
    quick_path=root/'data/rapid-vocabulary.json'
    quick=json.loads(quick_path.read_text(encoding='utf8'))
    authored={x['word'].casefold() for x in vocab if x['category']=='general'}
    # Archived focus swaps must not reappear as new priority cards. Archived
    # source lessons and existing localStorage review records remain intact.
    archived_path=root/'data/archived-vocabulary.json'
    if archived_path.exists():
        authored.update(x['word'].casefold() for x in json.loads(archived_path.read_text(encoding='utf8')))
    keep=[x for x in quick if x['word'].casefold() not in authored]
    removed=[x for x in quick if x['word'].casefold() in authored]
    if removed:
        quick_path.write_text(json.dumps(keep,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8')
    return {'originalRapidCards':len(quick),'promotedOverlapRemoved':len(removed),
        'rapidRemaining':len(keep),'progressStorageChanged':False,
        'priorRapidIdsRemainInLocalProgress':True,'fullMasteryGranted':False}

if __name__=='__main__':
    result=reconcile()
    path=ROOT/'qa/rapid-promotion-reconcile.json'
    path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result,ensure_ascii=False))
