#!/usr/bin/env python3
"""Add US-style CMU pronunciation *candidate metadata* to staged headwords.

CMUdict transcriptions are lexical ARPAbet approximations and do not certify
speaker audio, connected-speech rules, stress-in-context, or CEFR levels.
No finished lesson cards are generated or approved. Requires local cmudict.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'sources' / 'b2-c1-offline-catalog.json'
PHS = ROOT / 'sources' / 'phrasal-candidates.json'
REPORT = ROOT / 'qa' / 'pronunciation-candidate-report.json'


def normalize_pronunciation(pronunciations):
    return ' '.join(pronunciations[0]) if pronunciations else None


def enrich():
    try:
        import cmudict
    except ImportError as exc:
        raise RuntimeError('cmudict dependency is unavailable in this Python environment') from exc
    dic = cmudict.dict()
    words = json.loads(CATALOG.read_text(encoding='utf-8'))
    phrasals = json.loads(PHS.read_text(encoding='utf-8'))
    word_hits = 0
    phrase_hits = 0
    missing = []
    for rec in words:
        pron = normalize_pronunciation(dic.get(rec['word']))
        if pron:
            rec['americanPronunciationCandidateARPAbet'] = pron
            rec['pronunciationSource'] = 'CMU Pronouncing Dictionary'
            rec['usPronunciationChecked'] = False  # lexical transcription, not editor sign-off
            word_hits += 1
        else:
            missing.append(rec['word'])
    # Word-by-word is *not* a native recording or connected-speech transcription.
    for rec in phrasals:
        terms = rec['word'].split()
        pronunciations = [normalize_pronunciation(dic.get(t)) for t in terms]
        if all(pronunciations):
            rec['isolatedComponentARPAbetCandidate'] = ' | '.join(pronunciations)
            rec['componentPronunciationSource'] = 'CMU Pronouncing Dictionary'
            phrase_hits += 1
    CATALOG.write_text(json.dumps(words,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    PHS.write_text(json.dumps(phrasals,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report={
        'source':'CMU Pronouncing Dictionary via cmudict package',
        'generalHeadwords':len(words),
        'generalWithLexicalPronunciationCandidate':word_hits,
        'generalMissingLexicalPronunciation':len(words)-word_hits,
        'phrasalHeadwords':len(phrasals),
        'phrasalsWithEachComponentCandidate':phrase_hits,
        'sourcePronunciationReviewComplete':False,
        'bundledHumanAudioCreated':0,
        'newApprovedTeachingCards':0,
        'remainingWordExamples':missing[:25],
        'sourceChecksum':hashlib.sha256(str(len(dic)).encode()).hexdigest(),
        'releaseReady':False,
    }
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__ == '__main__':enrich()
