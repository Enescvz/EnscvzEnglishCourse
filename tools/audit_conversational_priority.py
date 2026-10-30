"""Preliminary manual-risk screening only; NOT a corpus-frequency ranking.

All unverified items remain blocked from claims of high spoken frequency.
Use US spoken corpus data and human sense-level review before approvals.
"""
from pathlib import Path
import csv
import json
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
FOCUS=ROOT/'data'/'fluency-focus.json'
QA=ROOT/'qa'

# Initial red flags are qualitative editorial examples, NOT a frequency threshold.
REVIEW = {
  'low_priority_niche_topic': set('typhoid mutton hemp monastery transfusion telescope nobility legislature legislative malaria'.split()) |
    set('concerto repertory pendulous fissure wizened folktale carpenter radiator playwright'.split()),
  'low_priority_rare_form_or_register': set('unto lest homeward southward thickly thirdly irresistibly temperate humbug malady'.split()) |
    set('unmusically somberly fiendishly irately docilely raunchily magnetically demographically primitively synthetically monotonously remorselessly insubordinately bureaucratically acoustically fanatically benignly primitively verandah'.split()),
  'likely_known_foundational_or_too_general': set('later known learning lower means master tail jaw loan throat hook tub tunnel'.split()),
}
# Correct multiword list (split as phrases, not individual tokens).
REVIEW['likely_known_foundational_or_too_general'] = set('later known learning lower means master tail jaw loan throat hook tub tunnel'.split()) | {
    'get up','look for','go out','go away','go down','come in','come on','get in','get out','take out','turn on','turn off','wake up'
}
REVIEW['low_priority_niche_topic'].discard('playwright')


def run():
    f=json.loads(FOCUS.read_text(encoding='utf-8'))
    rows=[]
    for kind,items in [('general',f['vocabulary']),('phrasal',f['phrasals'])]:
        for entry in items:
            word=entry['word'].strip().lower()
            reasons=[reason for reason,words in REVIEW.items() if word in words]
            rows.append({
                'kind':kind,'headword':word,'existing_level':entry.get('level',''),
                'spoken_frequency_verified':'NO',
                'spoken_rank':'', 'spoken_corpus':'',
                'editorial_priority_review':'REVIEW' if reasons else 'PENDING',
                'review_reason':'; '.join(reasons),
                'note':'Manual candidate flag only; no US spoken-frequency percentile or frequency assertion'
            })
    QA.mkdir(exist_ok=True)
    dest=QA/'spoken-priority-review.csv'
    with dest.open('w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle, fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    counts=Counter(r['kind'] for r in rows)
    flagged=Counter(r['kind'] for r in rows if r['editorial_priority_review']=='REVIEW')
    report={
        'review_method':'manual editorial red-flag screening, not corpus scoring',
        'screened_total':len(rows), 'screened_by_kind':dict(counts),
        'preliminary_review_flags':{k:flagged.get(k,0) for k in ('general','phrasal')},
        'spoken_frequency_verified':0,
        'high_frequency_confirmed':0,
        'recommended_next_step':'Compare sense-level items to licensed COCA spoken / US TV subtitle frequency data; compare everyday contexts, then replace low-value candidates before approving the 1000+500 focus selection.',
        'criteria':['US spoken frequency','listening comprehension utility','active speaking utility','daily scenario coverage','learner B1 novelty','US sense/phrase naturalness'],
        'disclaimer':'Unflagged items are not verified as frequent. Flagged entries are not proven rare; they require priority review.'
    }
    (QA/'spoken-priority-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':run()
