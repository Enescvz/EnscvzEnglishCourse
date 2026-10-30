"""Build 500 B2 + 500 C1 / 500 phrasal *focus targets*, not fake finished lessons.

Existing authored cards come first, then sourced bilingual glosses, then unglossed
headword candidates. Every target advertises its true content status. This is an
editorial shortlist, NOT a measured frequency ranking or CEFR certification.
Run offline: python tools/build_fluency_focus.py
"""
from __future__ import annotations
import json
import re
from pathlib import Path

try:
    # Weak written-English proxy for sorting tied source candidates, not spoken-US corpus frequency.
    from textblob.en import spelling as _spelling
except ImportError:
    _spelling = {}

def rough_written_frequency(word):
    return int(_spelling.get(word.lower(), 0))

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def key(word):
    return re.sub(r'\s+', ' ', word.strip().lower())


# Editorial priority examples: everyday decisions, relationships, plans, feelings,
# explanations and natural conversation. Source order otherwise wins.  The list is
# deliberately small so no unsubstantiated claim of quantitative word frequency.
B2_PRIORITY = '''overwhelmed acknowledge appreciate crucial outcome reluctant genuinely aware apparently
assume approach benefit concern challenge commitment cope convince deserve enable ensure
expectation flexible hesitate improve influence insight intention issue justify likelihood
manage opportunity outcome perspective predict preference priority recognize relevant reliable
require responsible significant solution struggle tendency urgent valuable available straightforward
handle affordable effective adequate compromise consequence concern consistent capability
alternative assumption assessment collaborate comfortable confidence conflict contribute
convenient considerate determine develop distract encourage engaging essential establish
evaluate evidence exaggerate exceed experience explain express figure focus fortunate
frustrated grateful hesitate highlight identify imply improve involve maintain meaningful
mention mutual negotiate obstacle perspective potential practical prevent promote propose
provide realistic reassure recommend recover reflect regret reject relationship reluctant
respond reveal schedule settle significant situation solution support supposed tolerate
transition understand unexpected unfamiliar unfortunately valuable wonder worthwhile'''.split()
C1_PRIORITY = '''alleviate compelling plausible scrutiny subtle resilient resilience profound profoundly
conscientious contemplate contemplate convey articulate articulate enhance reinforce undermine
substantially inevitable subsequently nevertheless nonetheless acknowledge remarkable
sophisticated coherent comprehensive persistent persist perceive perspective persuasive
persuasion insightful insightful insight discern skeptical skepticism meticulous
meticulously compelling clarify ambiguity ambiguous mitigate facilitate coherent
plausible contradiction conflict inconsistency constraint consensus collaborate
contemplate implication implications initiative incentive increasingly inevitable
intrinsic inherently implicit explicit credible credibility credible reassure
restoration sustainable sustainability versatile versatility resilience
proactive reluctant reluctantly profound viable viable potentially apparently
perpetuate concise elaborate tedious meticulous nuance subtlety substantial
prioritize compelling compelling contemplate detrimental invaluable skeptical
assertion assert decisive rational irrational empathetic empathy candid candidly
provoke resentment resentment adversity overcome mindful articulate'''.split()

# Important: raw Octanove C1 labels include many high-frequency beginner words
# ("man", "house", "behind") when a different *sense* is advanced. Selecting
# by spelling frequency alone without sense review is misleading. Prefer useful
# advanced headwords before any weak-frequency fallback. These are still targets
# awaiting a sense-level editorial review, NOT CEFR-certified entries.
C1_CONVERSATIONAL_CANDIDATES = """alienate allege altruism altruistic appalling assertion avid boast bribe bribery
candid candidly collaboration collaborative commend compliance compliant comprise
compulsion concur confide conformity conscientious conscientiously conserve
convoluted criteria cynical cynically cynicism degradation degrade degrading
confinement contradictory detest disdain dispensary divergent dither
elaboration enviable estimation extortion extravagance exuberant exuberance
fatality ferocious flattery fluctuate forceful fundamental
harass harassment heighten hypocrisy hypocrite hypocritical
impede impediment impersonal impoverished inclusion inclusive individuality
inexcusable inexplicable inherently innovate insecure insightful instinctive
insubordinate integral intuition intuitive intuitive intuitively irate
lapse legacy lethargic lethargy liaison likelihood ludicrous malfunction
manipulation marginally methodical mingle monotony mutually negligent
negligible neutralize niche notable numb oblige obscurely occupational
oversee perpetuate pertinent phenomenal physically plausible plausibly
ploy plummet plunge portray portrayal posture predecessor premise privileged
prohibitive proliferate prolific prospective provocative provoke psyche
rarity reclaim rediscover refurbish refurbishment relinquish reminisce reminiscent
repel resonate respite ruthless ruthlessness salvage sarcasm sarcastically
self-conscious self-worth sedentary shortlist smug somber spacious speculation
speculative stamina substantially subtly suffice sustainable sustainably
swap symptomatic tactful tactfully tantrum tedious tedium testament torment
tranquility unconventional unconvincing unwavering upheaval versatile voracious
wary wrangle wry""".split()

# Additional practical combinations to consider BEFORE falling back to the
# historical alphabetic source order. Headword presence is verified below.
PHRASAL_CONVERSATION_CANDIDATES = [p.strip() for p in """check into,check off,fill out,fill up,finish up,fit in,get down,get in,get off,get on,get out,get together,get up,get away,keep away,keep off,keep out,come about,come after,come away,come by,come into,come on,come up to,come upon,make for,make over,make out,put across,put in,put under,put back,put down,put out,put up,turn over,turn in,turn back,turn into,look at,look away,look on,look to,look over,look through,get about,get along,get at,get onto,get to,go about,go along,go around,go by,go past,go under,go with,go back,go away,bring around,bring off,bring on,hand in,hand out,hand over,hand down,hand back,check in,check out,cheer up,chip in,chill out,clean out,clean up,clear out,clear up,close down,close up,cool down,cool off,cook up,cover up,cover for,count down,crack down,crack up,cross off,cut across,cut away,cut in,cut up,catch up,call back,call in,call out,call up,calm down,cancel out,come around,come along,cut down,drop away,drop behind,drop down,drop out,eat out,eat up,eat in,ease off,end up,even out,fade away,fall down,fall in,fall into,fall off,fall over,feel for,feel like,fend off,fight off,filter out,follow through,fool around,force out,freak out,gear up,get by,get through,get over,give away,give off,give out,give in,give back,hang around,hang on,hang out,hang up,head back,head out,hold back,hold down,hold in,hold onto,hold over,join in,keep on,kick off,lay off,leave out,lie down,line up,link up,look around,look back,look out,move around,move over,move up,move in,move out,pass away,pass out,pass up,pay back,pick at,pick out,point out,pull away,pull off,pull out,pull over,pull through,put aside,roll out,run across,run around,run away,run down,run for,run off,run on,run over,run up,run through,set down,set off,set out,set aside,settle down,settle for,show around,show off,show up,shut down,shut off,sign in,sign up,slow down,sort out,speak up,stand by,stand out,start over,stay up,step down,step up,stick around,stick to,stop by,take after,take apart,take away,take back,take down,take in,take off,take on,take out,take over,take up,talk over,talk into,talk out of,think over,throw away,throw out,throw up,tidy up,try on,try out,tune in,turn away,turn down,wake up,walk away,warm up,watch out,wear out,work on,work off,work out,work up,wrap up,write down,write off,zone out""".split(',') if p.strip()]

# Source sense labels can be advanced for a beginner-level headword. These
# words cannot be taught as C1 merely because one source marks them C1.
BASIC_C1_FALSE_POSITIVES = set("""man house voice behind condition till trying removed ground nature tone
firm rich drive lodge bald battery burst class hanging jersey stretching grounds pace
perfect angle frost wing signal brief desert signal goose pupil chart engineer drill
calf clock glass board green""".split())

PHRASAL_PRIORITY = '''figure out,come across,come up with,bring up,put off,look forward to,get along with,
catch up with,run into,turn down,turn out,work out,deal with,go through,find out,
point out,carry on,give up,set up,break down,look into,look after,make up,
get over,come down with,put up with,sort out,look up,cut down on,fill in,
show up,call off,carry out,back up,keep up with,run out of,come around,
get by,bring about,hang out,take over,step up,turn up,pick up,slow down,
check out,drop by,take up,go over,put together,look back on,move on,
cut off,come up,go ahead,make up for,settle down,reach out,break up,
get through,go on,take off,turn around,hold on,let down,pass out,
find out,look out,follow up,stick to,run out,drop off,stand out,
show off,speak up,walk away,head out,think over,rule out,fall apart,
get around,hold back,keep on,come along,bring back,catch on,join in,
miss out,turn in,check in,come back,put away,deal with,step down,
get together,hold up,make out,get rid of,look down on,get away with,
get used to,stand for,look up to,look out for,come to,go off,
put on,get on,turn on,turn off,pay off,keep up,break into,fall behind,
start over,move in,move out,carry out,break out,bring in,go out,
look around,settle for,make do with,run through,take on,walk through,
back out,break even,come through,lay off,get ahead,bring down,check up on,
watch out,put aside,set aside,hold off,cut back,go along with,stand by'''.replace('\n', '').split(',')


def candidates_with_status(authored, quick, candidate, n, level, excluded=None):
    chosen = {}
    def add(word, status, item=None, why=''):
        word = key(word)
        if not word or word in chosen or word in (excluded or set()) or len(chosen) >= n:
            return
        row = {
            'word': word, 'level': level, 'status': status,
            'editorialApproved': False, 'selectionBasis': why,
        }
        if item and status == 'context_draft':
            row['lessonId'] = item['id']
        elif item and status == 'gloss_draft':
            row['rapidId'] = item['id']
        chosen[word] = row

    auth = {key(x['word']): x for x in authored if x.get('level') == level and x.get('category') == 'general'}
    gloss = {key(x['word']): x for x in quick if x['level'] == level}
    pending = {key(x['word']): x for x in candidate if x.get('levelCandidate') == level}
    priority = B2_PRIORITY if level == 'B2' else C1_PRIORITY
    for w in priority:
        w=key(w)
        if w in auth: add(w,'context_draft',auth[w], 'editorial useful-in-conversation shortlist')
        elif w in gloss: add(w,'gloss_draft',gloss[w], 'editorial useful-in-conversation shortlist')
        # Do not put definition-free words at the front of an immediately teachable deck.
    for x in authored:
        if x.get('category')=='general' and x.get('level')==level:
            add(x['word'],'context_draft',x,'existing authored priority, not frequency measurement')
    eligible_quick=[x for x in quick if x['level']==level]
    for x in sorted(eligible_quick,key=lambda o:-rough_written_frequency(o['word'])):
        add(x['word'],'gloss_draft',x,'bilingual draft; weak written-English frequency tie-break only')
    eligible_candidates=[x for x in candidate if x.get('levelCandidate')==level and re.fullmatch(r'[a-z]+(?:-[a-z]+)*', x['word'])]
    if level=='C1':
        for w in C1_CONVERSATIONAL_CANDIDATES:
            if w in pending and w not in BASIC_C1_FALSE_POSITIVES:
                add(w,'headword_only',None,'advanced-sense conversational editorial priority; meaning review pending')
    for x in sorted(eligible_candidates,key=lambda o:-rough_written_frequency(o['word'])):
        if level=='C1' and x['word'] in BASIC_C1_FALSE_POSITIVES:continue
        add(x['word'],'headword_only',None,'CEFR source headword; weak written frequency tie-break only, no meaning')
    if len(chosen)!=n:
        raise ValueError(f'{level}: only {len(chosen)}/{n} targets')
    return list(chosen.values())


def build():
    # Original candidate builder must never silently revert a curated curriculum.
    existing=ROOT/'data/fluency-focus.json'
    if existing.exists() and read('data/fluency-focus.json').get('meta',{}).get('editorialCurationRevision'):
        raise RuntimeError('Protected daily-spoken curriculum: do not regenerate the old frequency-unverified shortlist. Use npm run curriculum:focus for verification.')
    vocab=read('data/vocabulary.json'); rapid=read('data/rapid-vocabulary.json')
    general=read('sources/b2-c1-offline-catalog.json')
    phrases=read('data/phrasals.json'); pc=read('sources/phrasal-candidates.json')
    b2 = candidates_with_status(vocab,rapid,general,500,'B2')
    c1 = candidates_with_status(vocab,rapid,general,500,'C1', {key(x['word']) for x in b2})
    words = b2 + c1
    selected=[]; seen=set()
    authored={key(x['word']):x for x in phrases}
    candidates={key(x['word']):x for x in pc}
    def add(w, reason):
        w=key(w)
        if not w or w in seen or len(selected)>=500:return
        isAuth=w in authored
        if not isAuth and w not in candidates:return
        seen.add(w)
        selected.append({'word':w,'level':authored[w]['level'] if isAuth else None,
          'status':'context_draft' if isAuth else 'headword_only',
          'lessonId': authored[w]['id'] if isAuth else None,
          'editorialApproved':False,'selectionBasis':reason,
          'cefrVerified':False})
    for w in PHRASAL_PRIORITY: add(w,'editorial conversational shortlist')
    for x in phrases:add(x['word'],'existing authored priority, not frequency measurement')
    # Hand-curated last-mile set: everyday US conversation; replaces rare/invalid filler.
    for w in ['blow out', 'blow over', 'boil down', 'boil over', 'book up', 'boss around', 'breathe in', 'breathe out', 'brush up', 'bump up', 'bundle up', 'burn down', 'burn off', 'burst out', 'camp out', 'care for', 'cave in', 'charge up', 'chase after', 'chew over', 'choke up', 'chop up', 'clam up', 'clear away', 'climb up', 'clock in', 'clog up', 'clue in', 'cop out', 'cough up', 'crank up', 'curl up', 'dig in', 'dig into', 'dig out', 'dig up', 'doze off', 'drag on', 'dream up', 'dress up', 'drift off', 'factor in', 'finish off', 'fire up', 'flare up', 'flip out', 'fold up', 'freshen up', 'gather up', 'glance over', 'gloss over', 'grow up', 'hang in', 'hash out', 'heat up', 'help out', 'hook up', 'jot down', 'kick in', 'kick out', 'knock over', 'leave behind', 'let in', 'let out', 'light up', 'log in', 'log off', 'loosen up', 'mess up', 'mix up']:
        add(w,'editorial everyday-conversation priority, source verified; CEFR sense review pending')
    for w in PHRASAL_CONVERSATION_CANDIDATES:
        add(w,'conversational editorial priority, CEFR/sense not yet verified')
    core_verbs={'get':10,'go':10,'come':10,'take':9,'put':9,'look':9,'turn':8,'bring':8,'make':8,'give':8,'pick':7,'set':7,'run':7,'keep':7,'work':7,'find':7,'hold':7,'break':7,'cut':7,'call':7,'drop':6,'show':6,'fall':6,'check':6,'move':6}
    for x in sorted(pc,key=lambda x:(-core_verbs.get(x['word'].split()[0],0),len(x['word'].split()),x['word'])):
        add(x['word'],'candidate; common-verb heuristic, frequency not verified')
    if len(selected)!=500:raise ValueError('Not enough phrasal candidates')
    assert len({key(x['word']) for x in words}) == 1000
    assert len({key(x['word']) for x in selected}) == 500
    totals=lambda xs: {name:sum(x['status']==name for x in xs) for name in ('context_draft','gloss_draft','headword_only')}
    doc={'meta':{'description':'Focus TARGETS. Headword-only/gloss entries are not full lessons; no externally verified corpus frequency rank.',
                'vocabularyTarget':1000,'b2Target':500,'c1Target':500,'phrasalTarget':500,
                'generalBreakdown':totals(words),'phrasalBreakdown':totals(selected),
                'selectionPolicy':'Conversation-use editorial priorities + existing authored cards + bilingual source + screened advanced-sense C1 candidates, then fallback; not a spoken-frequency ranking. Requires US-English sense/level review.',
                'publishable':False},'vocabulary':words,'phrasals':selected}
    out=ROOT/'data/fluency-focus.json';out.write_text(json.dumps(doc,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps(doc['meta'],ensure_ascii=False,indent=2));return doc

if __name__=='__main__':build()
