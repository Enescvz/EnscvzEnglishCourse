"""Create reproducible human-review queues from staged candidate catalogs.

This does not promote candidates into approved lessons.
"""
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'sources'
QA = ROOT / 'qa'


def normalized(word):
    return re.sub(r'\s+', ' ', str(word).strip().lower())


def triage(vocabulary, phrasals):
    review = []
    seen = set()
    for kind, entries in [('vocabulary', vocabulary), ('phrasal', phrasals)]:
        for row in entries:
            word = normalized(row.get('word', ''))
            if not word or (kind, word) in seen:
                continue
            seen.add((kind, word))
            flags = []
            if '/' in word:
                flags.append('VARIANT_OR_ALTERNATIVE_SPELLING')
            if not re.fullmatch(r"[a-z][a-z' -]*", word):
                flags.append('NON_STANDARD_HEADWORD_FORMAT')
            if kind == 'phrasal' and len(word.split()) < 2:
                flags.append('NOT_MULTIWORD')
            if kind == 'phrasal' and not row.get('levelCandidate'):
                flags.append('NO_SOURCE_CEFR_LEVEL')
            if row.get('alreadyTaught'):
                flags.append('OVERLAPS_EXISTING_LESSON')
            if not row.get('americanUsageVerified', False) and kind == 'phrasal':
                flags.append('US_USAGE_NOT_VERIFIED')
            if not row.get('usPronunciationChecked', False) and kind == 'vocabulary':
                flags.append('US_PRONUNCIATION_NOT_VERIFIED')
            priority = 0 if row.get('alreadyTaught') else 1
            review.append({'type': kind, 'headword': word, 'sourceLevel': row.get('levelCandidate') or '',
                           'priorityGroup': priority, 'reviewFlags': '|'.join(flags),
                           'publicationStatus': 'NOT_APPROVED'})
    review.sort(key=lambda x: (x['priorityGroup'], x['type'], x['headword']))
    return review


def main():
    vocab = json.loads((SOURCES / 'b2-c1-offline-catalog.json').read_text(encoding='utf-8'))
    phrasals = json.loads((SOURCES / 'phrasal-candidates.json').read_text(encoding='utf-8'))
    queue = triage(vocab, phrasals)
    QA.mkdir(exist_ok=True)
    with (QA / 'candidate-review-queue.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['type', 'headword', 'sourceLevel', 'priorityGroup', 'reviewFlags', 'publicationStatus'])
        writer.writeheader()
        writer.writerows(queue)
    report = {'uniqueCandidates': len(queue), 'byType': dict(Counter(r['type'] for r in queue)),
              'reviewFlagCounts': dict(Counter(flag for r in queue for flag in r['reviewFlags'].split('|') if flag)),
              'approvedForRelease': 0,
              'note': 'Review queue only; no candidate automatically promoted to a validated lesson.'}
    (QA / 'candidate-triage-report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
