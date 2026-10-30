#!/usr/bin/env python3
"""Create complete, deterministic private content-production queues.

This does not translate words or invent B2/C1 levels for phrasal verbs. Existing
unreviewed teaching cards retain their data and status; source-only entries are
explicitly marked NOT ready for students, publication and mastery counts.
"""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TARGET_VOCAB = 3500
TARGET_PHRASALS = 600
COMMON_PHRASAL_ROOTS = (
    'get', 'take', 'go', 'come', 'put', 'make', 'look', 'turn', 'bring',
    'give', 'set', 'run', 'break', 'hold', 'keep', 'carry', 'work',
    'cut', 'pick', 'call', 'pull', 'stand', 'drop', 'fall', 'move',
    'pass', 'point', 'back', 'check', 'figure', 'find', 'catch',
)
COMMON_PARTICLES = (
    'up', 'out', 'off', 'on', 'down', 'in', 'over', 'away', 'back',
    'through', 'into', 'with', 'for', 'to', 'after', 'across',
)


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def write_json(path, data):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def phrase_score(record):
    word = record['word']
    parts = word.split()
    root = parts[0]
    particle = parts[-1]
    return (
        0 if root in COMMON_PHRASAL_ROOTS else 1,
        COMMON_PHRASAL_ROOTS.index(root) if root in COMMON_PHRASAL_ROOTS else 100,
        0 if particle in COMMON_PARTICLES else 1,
        0 if len(parts) <= 3 else 1,
        word,
    )


def generate():
    existing_words = [e for e in read_json('data/vocabulary.json') if e['category'] == 'general']
    existing_pv = read_json('data/phrasals.json')
    candidates = read_json('sources/b2-c1-offline-catalog.json')
    pv_candidates = read_json('sources/phrasal-candidates.json')
    assert len({x['word'].casefold() for x in existing_words}) == len(existing_words)
    assert len({x['word'].casefold() for x in existing_pv}) == len(existing_pv)
    have_words = {x['word'].casefold() for x in existing_words}
    have_phrases = {x['word'].casefold() for x in existing_pv}

    # Existing authored cards cannot be silently displaced by imported headwords.
    words = [dict(word=x['word'],levelCandidate=x['level'],origin='existing-authored-card',
                  contentStatus=x.get('editorialStatus', 'authored_unreviewed'),
                  teachingCardExists=True,editorialApproved=x.get('editorialStatus')=='approved',
                  activeCardId=x['id']) for x in existing_words]
    extras = [x for x in candidates if x['word'].casefold() not in have_words]
    # No real usage-frequency data is available: do not claim this is a corpus rank.
    # Prioritize C1 words for review because C1 source coverage is below target.
    extras.sort(key=lambda x: (x['levelCandidate'] != 'C1',
                               0 if x.get('americanPronunciationCandidateARPAbet') else 1,
                               x['word']))
    words.extend(dict(word=x['word'],levelCandidate=x['levelCandidate'],
                      candidateLevels=x['candidateLevels'],origin=x['source'],
                      partOfSpeech=x.get('partsOfSpeech',[]),
                      usPronunciationCandidate=x.get('americanPronunciationCandidateARPAbet'),
                      contentStatus='HEADWORD_ONLY',teachingCardExists=False,
                      editorialApproved=False,requiresSemanticAuthoring=True)
                 for x in extras[:TARGET_VOCAB-len(words)])

    phrasals = [dict(word=x['word'],levelCandidate=x['level'],origin='existing-authored-card',
                     contentStatus=x.get('editorialStatus','authored_unreviewed'),
                     teachingCardExists=True,editorialApproved=x.get('editorialStatus')=='approved',
                     activeCardId=x['id']) for x in existing_pv]
    pending = [x for x in pv_candidates if x['word'].casefold() not in have_phrases]
    pending.sort(key=phrase_score)
    phrasals.extend(dict(word=x['word'],levelCandidate=None,origin=x['source'],
                         sourceLicense=x.get('sourceLicense'),
                         pronunciationCandidate=x.get('isolatedComponentARPAbetCandidate'),
                         contentStatus='HEADWORD_ONLY',teachingCardExists=False,
                         editorialApproved=False,requiresSenseAndCEFRReview=True)
                    for x in pending[:TARGET_PHRASALS-len(phrasals)])

    assert len(words)==TARGET_VOCAB
    assert len(phrasals)==TARGET_PHRASALS
    assert len({x['word'].casefold() for x in words})==TARGET_VOCAB
    assert len({x['word'].casefold() for x in phrasals})==TARGET_PHRASALS
    assert all(x['levelCandidate'] is None for x in phrasals if not x['teachingCardExists'])
    assert all(not x['editorialApproved'] for x in words+phrasals if not x['teachingCardExists'])

    word_levels = dict(Counter(x['levelCandidate'] for x in words))
    report = dict(
        targetVocabulary=TARGET_VOCAB,
        targetUniquePhrasalVerbs=TARGET_PHRASALS,
        generalSelected= len(words),phrasalSelected=len(phrasals),
        generalExistingAuthored=sum(e['teachingCardExists'] for e in words),
        phrasalExistingAuthored=sum(e['teachingCardExists'] for e in phrasals),
        generalSourceOnly=sum(not e['teachingCardExists'] for e in words),
        phrasalSourceOnly=sum(not e['teachingCardExists'] for e in phrasals),
        generalLevelCandidates=word_levels,
        requestedC1Count=1500,sourceLimitedC1Candidates=word_levels.get('C1',0),
        missingC1CandidateLevelsToReachMix=max(0,1500-word_levels.get('C1',0)),
        newEditoriallyApprovedCards=0,publicationAllowed=False,
        phrasalCEFRMissing=sum(x['levelCandidate'] is None for x in phrasals),
        orderingWarning='Heuristic production review order; not measured spoken-US frequency.',
        semanticWarning='The source-only entries are NOT lessons and cannot be used in flashcard or exam mode.',
        licensingWarning='External phrasal headword source is CC BY-NC 4.0; no source glosses copied.'
    )
    write_json('sources/general-production-queue.json',words)
    write_json('sources/phrasal-production-queue.json',phrasals)
    write_json('qa/curriculum-queue-report.json',report)
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report


if __name__=='__main__':
    generate()
