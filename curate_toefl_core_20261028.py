#!/usr/bin/env python3
"""Private AEL TOEFL + daily English core. ID-preserving and idempotent.

This is an editorial starter shortlist, NOT an ETS frequency ranking or CEFR signoff.
AWL Sublist 1 headwords guide the academic slice; all glosses and examples
are authored for AEL, never copied from dictionaries or third-party lessons.
"""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
AWL_1=('analyze approach area assess assume authority available benefit concept consist '
'constitute context contract create data define derive distribute economy environment establish '
'estimate evident export factor finance formula function identify income indicate individual '
'interpret involve issue labor legal legislate major method occur percent period policy principle '
'proceed process require research respond role section sector significant similar source specific '
'structure theory vary').split()
# A mixed spoken/academic slice: these already have two authored examples in AEL.
# Does NOT claim objective TOEFL examination frequency.
PHRASAL_PRIORITY=('figure out|carry out|find out|point out|set up|come up with|deal with|'
'look into|go over|bring up|work out|turn out|account for|put forward|break down|'
'break through|come across|get across|look up|keep up|keep up with|make up for|'
'rule out|sum up|back up|come down to|come up|go through|put off|take on|'
'take over|stand for|reach out to|fill in|turn in|check out|drop out|'
'sign up|catch up|move on|run into|phase out|draw on|bring about|step up|'
'carry on|sort out|set out|fall behind|pick up').split('|')

def compile_core(root=ROOT):
    vocab=json.loads((root/'data/vocabulary.json').read_text(encoding='utf-8'))
    phrasals=json.loads((root/'data/phrasals.json').read_text(encoding='utf-8'))
    by_word={x['word'].lower():x for x in vocab}
    by_phrase={x['word'].lower():x for x in phrasals}
    existing_ids={x['id'] for x in vocab+phrasals}
    extra=[]
    for line in (root/'sources/toefl-awl1-extra-20261028.tsv').read_text(encoding='utf-8').splitlines():
        if not line.strip():continue
        word,tr,definition,example1,example2=line.split('|')
        assert word not in by_word, 'duplicate existing card: '+word
        assert len(definition)>=25 and len(example1)>=25 and len(example2)>=25
        assert len({example1,example2})==2 and example1[-1] in '.!?' and example2[-1] in '.!?'
        assert re.search(r'\b'+re.escape(word)+r'(?:s|d|ed|ing)?\b',example1,re.I), 'missing example headword: '+word
        item={
            'id':'toefl-'+word,'word':word,'tr':tr,
            'definition':definition,'example':example1,'examples':[example1,example2],
            'level':'B2', # placement suggestion, not individually verified CEFR
            'category':'toeflAcademic','priority':0,
            'prompt':f'Use “{word}” in a daily and in an academic sentence.',
            'editorialStatus':'authored_unreviewed',
            'sourceList':'AWL sublist 1 (US headword normalized)',
            'frequencyStatus':'AWL broad academic frequency; not verified TOEFL exam frequency',
        }
        assert item['id'] not in existing_ids, 'ID collision: '+item['id']
        extra.append(item)
    assert len(extra)==50 and set(AWL_1)=={x['word'] for x in extra}|{w for w in AWL_1 if w in by_word}
    by_extra={x['word']:x for x in extra}
    reuse_words=(root/'sources/toefl-curated-reuse-20261028.txt').read_text(encoding='utf-8').split()
    assert len(reuse_words)==len(set(reuse_words))
    reuse=[w for w in reuse_words if w not in AWL_1]
    assert len(reuse)>=140
    reuse=reuse[:140]
    assert all(w in by_word for w in reuse)
    assert len(PHRASAL_PRIORITY)==50 and len(set(PHRASAL_PRIORITY))==50
    assert all(w in by_phrase for w in PHRASAL_PRIORITY)
    word_lessons=[(by_word.get(w) or by_extra[w])['id'] for w in AWL_1]
    word_lessons += [by_word[w]['id'] for w in reuse]
    phrasal_lessons=[by_phrase[w]['id'] for w in PHRASAL_PRIORITY]
    assert len(word_lessons)==len(set(word_lessons))==200
    assert len(phrasal_lessons)==len(set(phrasal_lessons))==50
    # Preserve the previous 200/50 in their exact order. Never recreate their IDs,
    # split their learning records or silently add a duplicate sense as a new card.
    previous=json.loads((root/'sources/toefl-core-original-200-50-20261028.json').read_text(encoding='utf8'))
    assert word_lessons==previous['wordLessonIds']
    assert phrasal_lessons==previous['phrasalLessonIds']
    def load_unique_lines(name, size):
        entries=[x.strip() for x in (root/'sources'/name).read_text(encoding='utf8').splitlines()
                 if x.strip() and not x.lstrip().startswith('#')]
        assert len(entries)==size and len(set(entries))==size, f'invalid editorial shortlist {name}'
        return entries
    extend_words=load_unique_lines('toefl-curated-extension-20261028.txt',200)
    extend_phrasals=load_unique_lines('toefl-phrasal-extension-20261028.txt',25)
    assert all(w in by_word and by_word[w].get('category')=='general' for w in extend_words), 'unknown/non-general word'
    assert all(w in by_phrase for w in extend_phrasals), 'unknown phrasal'
    additional_word_ids=[by_word[w]['id'] for w in extend_words]
    additional_phrasal_ids=[by_phrase[w]['id'] for w in extend_phrasals]
    assert set(additional_word_ids).isdisjoint(word_lessons), 'duplicate word in previous core'
    assert set(additional_phrasal_ids).isdisjoint(phrasal_lessons), 'duplicate phrasal in previous core'
    for w in extend_words:
        item=by_word[w]
        examples=item.get('examples',[])
        assert len(examples)==2 and len(set(examples))==2 and examples[0]==item.get('example'), f'weak context {w}'
        assert item.get('tr') and len(item.get('definition',''))>=25, f'missing definition {w}'
        assert item.get('editorialStatus')!='approved', f'unexpected approval {w}'
    for w in extend_phrasals:
        item=by_phrase[w]
        examples=item.get('examples',[])
        assert len(examples)>=2 and len(set(examples))>=2 and examples[0]==item.get('example'), f'weak phrasal context {w}'
    word_lessons.extend(additional_word_ids)
    phrasal_lessons.extend(additional_phrasal_ids)
    assert len(word_lessons)==len(set(word_lessons))==400
    assert len(phrasal_lessons)==len(set(phrasal_lessons))==75
    catalog={
      'meta':{'version':2,'date':'2026-10-28','name':'TOEFL + Daily English Core',
        'studyTarget':{'words':400,'phrasals':75,'dailyWords':10,'dailyPhrasals':3},
        'newAcademicLessonCount':len(extra),
        'reusedGeneralLessonCount':350,
        'reusedPhrasalLessonCount':75,
        'officialTOEFLFrequencyRanking':False,
        'editorialSignoffComplete':False, 'frequencyAuditComplete':False,
        'licensesChecked':False,
        'basis':['AWL sublist 1 (60 word families, US spellings)', 'AEL curated academic/daily extension (200 previously authored general lessons)', '25 additional previously authored phrasal lessons', '2026 ETS updated exam overview'],
        'sources':['https://www.eapfoundation.com/vocab/academic/awllists/index.php',
                   'https://www.english-corpora.org/coca/avl.asp',
                   'https://www.eu.ets.org/toefl/test-takers/ibt/upcoming-updates-jan-2026.html'],
        'disclaimer':'Curated study priorities, not an official ETS / empirically ranked TOEFL word list; frequency, sense-level and licensing approval pending.'},
      'wordLessonIds':word_lessons,'phrasalLessonIds':phrasal_lessons
    }
    report={'checkedDate':'2026-10-28','status':'PRIVATE_DEV_QA_ONLY',
       'coreWords':len(word_lessons),'corePhrasals':len(phrasal_lessons),
       'newAcademicLessons':len(extra),'reusedGeneralLessons':len(word_lessons)-len(extra),
       'reusedPhrasals':len(phrasal_lessons),'existingFocusIDsModified':0,
       'learnedProgressModified':False,'sourceProvenance':'AWL1 + manually selected prior AEL cards; neither official TOEFL nor quantified COCA rankings',
       'headwordAndOriginalContextAutomatedReview':True,'automatedReviewScope':'ID integrity, card category, two non-identical context strings, basic definition presence; no semantic endorsement',
       'humanEditorialApproved':False,
       'audioVerifiedOnIphone':False,'licenseNote':'No third-party lexical examples or commercial AVL lists were copied in this sprint; 200 added words and 25 phrasals are existing AEL cards. Existing data provenance and full redistribution clearance remain pending. TOEFL is not ETS-endorsed.',
       'speakingModified':False,'releaseAllowed':False,
       'priorCoreWordsPreserved':200,'priorCorePhrasalsPreserved':50,
       'additionalExistingWordIDs':200,'additionalExistingPhrasalIDs':25,
       'independentFrequencyAuditComplete':False,'physicalSafariVerified':False,
       'offlineVerified':False}
    return extra,catalog,report

def main():
    extra,catalog,report=compile_core()
    for relative,obj in [
       ('data/toefl-academic.json',extra),('data/toefl-core.json',catalog),
       ('qa/toefl-core-report.json',report)]:
       p=ROOT/relative;p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(f'TOEFL + Daily shared deck: {len(catalog["wordLessonIds"])} words, {len(catalog["phrasalLessonIds"])} phrasals, {len(extra)} fresh academic lessons')

if __name__=='__main__':main()
