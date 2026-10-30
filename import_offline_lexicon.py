#!/usr/bin/env python3
"""Build an en-US B2/C1 candidate headword catalog from local public datasets.

No API, Google Drive, remote account, or publish operation. Source entries are
NOT presented as finished vocabulary lessons and do NOT unlock release gates.
"""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILES = {"B2": ROOT / "sources" / "cefr_b2.csv", "C1": ROOT / "sources" / "octanove_c1.csv"}
SOURCE_NAMES = {"B2": "CEFR-J Wordlist Version 1.5", "C1": "Octanove Vocabulary Profile C1/C2 1.0"}
# Terms that are markedly UK-specific, unsuitable as general American-English cards.
UK_EXCLUSIVE = {"aubergine", "whilst", "amongst", "tyre", "nought", "lavatory", "caravan", "mum", "glacis"}
FLAG_SENSITIVE = {"gook", "gypsy"}
SPACES = re.compile(r"\s+")
VALID = re.compile(r"[a-z][a-z' -]*")


def americanize(head):
    """Resolve dual US/UK spellings only; never invent an unrelated synonym."""
    head = SPACES.sub(" ", head.lower().strip())
    if '/' in head:
        parts = [s.strip() for s in head.split('/')]
        if len(parts) != 2 or not all(VALID.fullmatch(s) for s in parts):
            return None, 'ambiguous_variant'
        # The source writes US first in these spellings, except archaeologist.
        head = parts[0]
    if not VALID.fullmatch(head):
        return None, 'invalid_headword'
    if head in UK_EXCLUSIVE:
        return None, 'uk_specific'
    if head in FLAG_SENSITIVE:
        return None, 'requires_sensitivity_review'
    return head, None


def read_source(level):
    path = SOURCE_FILES[level]
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        rd = csv.DictReader(f)
        assert {'headword','pos','CEFR'}.issubset(rd.fieldnames or []), path
        rows = [r for r in rd if r['CEFR'] == level]
    return rows


def build():
    for file in SOURCE_FILES.values():
        if not file.exists() or file.stat().st_size < 1000:
            raise FileNotFoundError(f'Missing or empty local source: {file}')
    index = {}
    stats = Counter()
    excluded = []
    for level in ('B2', 'C1'):
        rows = read_source(level)
        stats[f'{level}_source_rows'] = len(rows)
        for row in rows:
            raw = row['headword'].strip()
            word,reason = americanize(raw)
            if reason:
                excluded.append({'raw':raw,'level':level,'reason':reason})
                stats['excluded_'+reason] += 1
                continue
            key = word.casefold()
            if key in index:
                x = index[key]
                if level not in x['candidateLevels']:
                    x['candidateLevels'].append(level)
                    stats['cross_level_disagreements'] += 1
                if row['pos'].strip() and row['pos'].strip() not in x['partsOfSpeech']:
                    x['partsOfSpeech'].append(row['pos'].strip())
                continue
            index[key] = {'word':word,'candidateLevels':[level],
                'levelCandidate':level, 'partsOfSpeech':[row['pos'].strip()] if row['pos'].strip() else [],
                'source': SOURCE_NAMES[level], 'status':'HEADWORD_CANDIDATE_ONLY',
                'phoneticVariant':'en-US','usPronunciationChecked':False,
                'meaningReviewed':False, 'examplesReviewed':False}
    existing = json.loads((ROOT/'data/vocabulary.json').read_text(encoding='utf-8'))
    have = {v['word'].casefold() for v in existing if v.get('category')=='general'}
    for k in index:
        index[k]['alreadyTaught'] = k in have
    values = sorted(index.values(),key=lambda e:(e['levelCandidate']!='B2',e['word']))
    out = ROOT/'sources'/'b2-c1-offline-catalog.json'
    out.write_text(json.dumps(values,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    qa = ROOT/'qa';qa.mkdir(exist_ok=True)
    (qa/'excluded-headwords.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report = dict(stats)
    report.update({'catalog_unique_headwords':len(index),
        'already_taught_overlap':len(index.keys() & have),
        'new_candidate_headwords':len(index.keys() - have),
        'unreviewed_candidate_headwords':len(index),
        'new_verified_teaching_cards':0,
        'american_semantic_review':'NOT_COMPLETE',
        'publication_allowed':False,
        'source_checksums':{x:hashlib.sha256(p.read_bytes()).hexdigest() for x,p in SOURCE_FILES.items()}})
    (qa/'offline-catalog-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__ == '__main__':build()
