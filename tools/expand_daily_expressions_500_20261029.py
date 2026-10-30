"""Idempotent authoring import for a 500-card *private* daily-expression draft.

Reads original, locally authored sentences, not external licensed text. Maintains
all original 300 card IDs/records and all stored learning-progress keys.
No synthetic audio is presented as human recorded audio.
"""
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources/daily-expressions-200-additions-20261029.tsv'
DEST = ROOT / 'data/daily-expressions.json'
COUNTS = {'B1':150,'B2':210,'C1':140}
CATEGORIES = {'K':'connectors','C':'collocations','S':'conversation_starters'}
NOTES = {
  'connectors': 'Links ideas logically in spoken or written English; read both examples to notice the relationship.',
  'collocations': 'A natural word combination used for this action or idea; practice it as one meaningful unit.',
  'conversation_starters': 'Use this starter to introduce a thought, question or explanation; complete it naturally in context.',
}
# Refine generic guidance for common logical functions, without asserting
# certified corpus frequency or CEFR level.
RELATIONS = {
 'concession': 'even though;even if;despite;in spite of;nevertheless;notwithstanding;albeit;be that as it may;all the same;that said',
 'condition': 'as long as;unless;in case;provided that;in the event of;on the condition that;insofar as;to the extent that',
 'reason': 'because of;thanks to;for this reason;given that;in light of;in view of;on the grounds that;by virtue of;inasmuch as',
 'result': 'as a result;as a consequence;consequently;to that end;on that basis',
 'contrast': 'instead of;in contrast;on the other hand;as opposed to;by contrast;in comparison;in other respects',
 'similarity': 'in the same way;in a similar vein;by the same token;in this regard',
 'sequence': 'at first;after that;by the time;meanwhile;to begin with;in the meantime',
 'summary': 'to sum up;in short;for all practical purposes',
 'examples': 'for example;in particular;as illustrated by;more specifically',
 'additional': 'in addition to;at the same time;in conjunction with',
 'limits': 'for the purposes of;with the exception of;in the absence of;in keeping with;in relation to;with regard to;in terms of',
}
RELATION_NOTES={
 'concession':'Introduces a contrast or a result that remains true despite an obstacle.',
 'condition':'Sets a condition, limit or possible situation affecting the main statement.',
 'reason':'Explains a reason, cause or justification for an action or conclusion.',
 'result':'Links evidence or an action to its outcome, consequence or purpose.',
 'contrast':'Compares differences between two choices, observations or claims.',
 'similarity':'Shows how another example or argument follows a similar pattern.',
 'sequence':'Places actions or ideas in a clear time or presentation order.',
 'summary':'Summarizes a practical conclusion without repeating every detail.',
 'examples':'Adds a concrete illustration or highlights a specific example.',
 'additional':'Adds a related idea, comparison or simultaneous event.',
 'limits':'Limits a claim or clarifies which aspect, exception or context matters.',
}
LOOKUP={phrase.strip().lower():key for key,terms in RELATIONS.items() for phrase in terms.split(';')}

# Original cards are not modified. These existing cards are relevant both in
# everyday use and TOEFL-style argumentation, but no item is claimed to be
# statistically frequent on the TOEFL exam.
LEGACY_TOEFL_EXPRESSIONS={
 'That makes sense', 'That’s a good point','That\'s a good point',
 'To be honest','If you ask me','That being said','As far as I know',
 'If I\'m not mistaken','Speaking of which','That reminds me',
 'It depends','In the meantime','From my perspective',
 'The way I see it','In other words','To put it simply',
 'For the record','As a rule of thumb','Generally speaking',
 'For what it\'s worth','Correct me if I\'m wrong',
 'Just to clarify','Let me put it another way',
 'What I\'m trying to say is','It boils down to',
 'The bottom line is','There\'s more to it than that',
 'That doesn\'t necessarily follow','There\'s a case to be made for',
 'That remains to be seen','To put things into perspective',
 'Let\'s not lose sight of','It\'s not entirely clear-cut',
 'All things considered','On balance','To a certain extent',
 'Not to mention','Let alone','By and large',
 'For the most part','More often than not',
 'In the grand scheme of things','As it turns out',
}

def norm(value):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKC', value).lower())


def build():
    data=json.loads(DEST.read_text(encoding='utf8'))
    old=data['cards']
    assert len(old) in (300,500),len(old)
    rows=[]
    for lineno,line in enumerate(SOURCE.read_text(encoding='utf8').splitlines(),1):
        if not line.strip():continue
        parts=line.split('|')
        if len(parts)!=7:
            raise ValueError(f'line {lineno}: expected 7 fields; received {len(parts)}')
        key,level,expr,tr,ex1,ex2,question=(x.strip() for x in parts)
        rows.append((key,level,expr,tr,ex1,ex2,question))
    assert len(rows)==200
    assert Counter(r[0] for r in rows)=={'K':80,'C':70,'S':50}
    assert Counter(r[1] for r in rows)=={'B1':50,'B2':90,'C1':60}
    prior_counts=Counter(x['level'] for x in old[:300]);assert prior_counts=={'B1':100,'B2':120,'C1':80}
    vocabulary=json.loads((ROOT/'data/vocabulary.json').read_text())
    phrasals=json.loads((ROOT/'data/phrasals.json').read_text())
    seen={norm(x['expression']) for x in old[:300]}
    forbidden={norm(x['word']) for x in vocabulary+phrasals}
    expected=[]
    for key,level,expr,tr,ex1,ex2,question in rows:
        normalized=norm(expr)
        if normalized in seen or normalized in forbidden:
            raise ValueError('duplicate or existing lexicon item: '+expr)
        seen.add(normalized)
        idx=prior_counts[level]+1;prior_counts[level]+=1
        identifier=f'ex-{level.lower()}-{idx:03}'
        note=RELATION_NOTES.get(LOOKUP.get(expr.lower()),NOTES[CATEGORIES[key]]) if key=='K' else NOTES[CATEGORIES[key]]
        if key=='C':
            note=f"Use '{expr}' as a natural word partnership in speaking or writing; notice the surrounding words."
        elif key=='S':
            note=f"Start with '{expr}' to express a complete thought or introduce a question naturally."
        # The dialogue uses a context-matched question followed by a full
        # natural example. A few examples have question form and are overridden.
        answer=ex1
        if expr=='Give someone a hand':answer=ex2
        if expr=='Keep an eye on':answer="Sure, I'll keep an eye on your bag."
        if expr=='Do you happen to know':answer="I asked, 'Do you happen to know when the store opens?'"
        if expr=='Could you do me a favor?':answer="Of course. What do you need?"
        if expr=="I'd appreciate it if":answer="I'd appreciate it if you sent the file today."
        if expr=="I'd be interested to know":answer="I'd be interested to know how you reached that result."
        if expr=='Make a recommendation':answer=ex1
        contexts=['daily']
        if key=='K' and expr not in {'At first','After that','As usual','In the end'} or key=='C' and level in ('B2','C1') or key=='S' and level in ('B2','C1'):
            contexts.append('toefl')
        expected.append({
          'id':identifier,'level':level,'expression':expr,'tr':tr,
          'usageNote':note,'examples':[ex1,ex2],
          'dialogue':[{'speaker':'A','text':question},{'speaker':'B','text':answer}],
          'category':CATEGORIES[key],'contexts':contexts,
          'audioStatus':'not_provided',
          'editorialStatus':'authored_pending_independent_review',
        })
    if len(old)==300:
        data['cards'].extend(expected)
    else:
        if old[300:]!=expected:
            raise ValueError('Existing 500-card content differs; refusing overwrite')
    data['meta'].update({
        'title':'Everyday American English Expressions — 500',
        'targetTotal':500,
        'targetByLevel':COUNTS,
        'authoringStage':'B1-B2-C1-500-authored-pending-independent-review',
        'approvedHumanVoiceCount':0,
        'independentEditorApproved':False,
        'legacyToeflDailyIds':[x['id'] for x in old[:300] if x['expression'] in LEGACY_TOEFL_EXPRESSIONS],
        'categoryCounts':{'connectors':80,'collocations':70,'conversation_starters':50},
        'description':'500 originally authored expressions. TOEFL + Daily denotes potential study usefulness only, not measured exam frequency or externally verified CEFR. Human audio and independent review pending.',
    })
    assert Counter(x['level'] for x in data['cards'])==COUNTS
    assert len(set(x['id'] for x in data['cards']))==500
    DEST.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Done:',len(data['cards']),COUNTS,'new category counts:',Counter(x['category'] for x in expected), 'legacy TOEFL + Daily IDs:',len(data['meta']['legacyToeflDailyIds']))

if __name__=='__main__':build()
