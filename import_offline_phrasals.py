#!/usr/bin/env python3
"""Stage public-source English phrasal-verb *headwords* without any external accounts.

The local prefix-coded corpus contains headwords extracted from the public
English_Phrasal_Verbs_in_Action_EN.txt resource (tema4p/english-vocabulary,
CC BY-NC 4.0). These are candidates, not CEFR-assessed vocabulary lessons.
No copyrighted definition text is included in this local subset.
The complete headword source was read through the GitHub public-file connector;
container networking to raw.githubusercontent.com is blocked. Import is fully
offline and does not interact with Drive, GitHub writes, or any user account.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENCODED = ROOT / 'sources/phrasal-en-delta.txt'
OUTPUT = ROOT / 'sources/phrasal-candidates.json'
REPORT = ROOT / 'qa/phrasal-source-report.json'
SOURCE_URL = ('https://github.com/tema4p/english-vocabulary/blob/main/content/'
              'phrasal-verbs/English_Phrasal_Verbs_in_Action_EN.txt')
EXPECTED_COUNT = 1204
ALLOW = re.compile(r"[a-z]+(?:[ '\-][a-z]+)+")


def decode_headwords(raw: str) -> list[str]:
    previous = ''
    result = []
    for i, token in enumerate(raw.strip().split('|'), start=1):
        if len(token) < 2 or not token[0].isalnum():
            raise ValueError(f'Invalid delta item at index {i}')
        shared = int(token[0], 36)
        if shared > len(previous):
            raise ValueError(f'Invalid prefix length at index {i}')
        value = previous[:shared] + token[1:]
        if result and value <= result[-1]:
            raise ValueError(f'Duplicate or unsorted phrase at index {i}: {value}')
        if not ALLOW.fullmatch(value):
            raise ValueError(f'Not a multiword verbal expression at index {i}: {value}')
        result.append(value)
        previous = value
    return result


def stage() -> dict:
    raw = ENCODED.read_text(encoding='utf8')
    phrases = decode_headwords(raw)
    if len(phrases) != EXPECTED_COUNT:
        raise ValueError(f'Phrasal headword source incomplete: {len(phrases)}/{EXPECTED_COUNT}')
    existing = json.loads((ROOT/'data/phrasals.json').read_text(encoding='utf8'))
    taught = {p['word'].casefold() for p in existing}
    records = [{
        'word': phrase,
        'partOfSpeech': 'phrasal verb or multiword verb (candidate)',
        'source': 'tema4p/english-vocabulary (English_Phrasal_Verbs_in_Action_EN)',
        'sourceUrl': SOURCE_URL,
        'sourceLicense': 'CC BY-NC 4.0 (noncommercial use only)',
        'status': 'HEADWORD_CANDIDATE_ONLY',
        'alreadyTaught': phrase in taught,
        'levelCandidate': None,
        'americanUsageVerified': False,
        'definitionReviewed': False,
        'examplesReviewed': False,
        'notSuitableForPublication': True,
    } for phrase in phrases]
    OUTPUT.write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    report = {
        'sourceHeadwords': len(phrases),
        'distinctSourceHeadwords': len(set(phrases)),
        'currentPhrasalLearningCards': len(existing),
        'sourceOverlapsLearningCards': len(set(phrases) & taught),
        'newHeadwordCandidates': len(set(phrases) - taught),
        'candidatesWithB2C1VerifiedLevel': 0,
        'newVerifiedTeachingCards': 0,
        'releaseReady': False,
        'sourceUrl': SOURCE_URL,
        'license': 'CC BY-NC 4.0 (noncommercial use only)',
        'sourceFormat': 'prefix-delta, headwords only, no English/Turkish definitions',
        'sourceSha256': hashlib.sha256(raw.encode('utf8')).hexdigest(),
        'warning': 'All source CEFR levels and senses unverified; this cannot satisfy the 500 independently approved focus phrasals release gate.'
    }
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == '__main__':
    stage()
