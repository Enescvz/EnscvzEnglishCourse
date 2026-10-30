#!/usr/bin/env python3
"""Private structural pre-use QA. Never authorizes publication or substitutes iPhone/WebKit QA."""
import json,re,collections,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
load=lambda f:json.loads((ROOT/'data'/f'{f}.json').read_text(encoding='utf-8'))
readings=load('toefl-reading-practice');writings=load('toefl-writing-practice')
core=load('toefl-core');vocab=load('vocabulary');academic=load('toefl-academic');phrasals=load('phrasals')
voa=load('authentic-listening');linked=load('voa-source-quizzes');status=json.loads((ROOT/'development-status.json').read_text())
questions=[(r,q) for r in readings for q in r['questions']]
all_voa=[*voa,*linked]
voa_questions=[q for d in all_voa for q in d['questions']]
core_sw=(ROOT/'sw.js').read_text(encoding='utf-8').split('const CORE=[',1)[1].split('];',1)[0]
sw_refs=re.findall(r"'\.(/[^']*)'",core_sw)
word_ids=[*core['wordLessonIds']];phrasal_ids=[*core['phrasalLessonIds']]
check={
 '400_toefl_word_ids_unique':len(word_ids)==400 and len(set(word_ids))==400,
 '75_toefl_phrasal_ids_unique':len(phrasal_ids)==75 and len(set(phrasal_ids))==75,
 'all_toefl_word_ids_resolve':set(word_ids).issubset({x['id'] for x in [*vocab,*academic]}),
 'all_toefl_phrasal_ids_resolve':set(phrasal_ids).issubset({x['id'] for x in phrasals}),
 'reading_50_answer_keys_valid':len(questions)==50 and all(len(q['options'])==4 and len(set(x.casefold().strip() for x in q['options']))==4 and type(q['answer']) is int and q['answer'] in range(4) for _,q in questions),
 'reading_3_task_types':{r['type'] for r in readings}=={'complete_words','daily_life','academic_passage'},
 'writing_28_original_tasks':len(writings)==28 and len({x['id'] for x in writings})==28,
 'writing_task_bank_supports_10_1_1':sum(x['kind']=='build_sentence' for x in writings)>=10 and sum(x['kind']=='write_email' for x in writings)>=1 and sum(x['kind']=='academic_discussion' for x in writings)>=1,
 '50_voa_lessons':len(all_voa)==50,
 '204_voa_questions':len(voa_questions)==204,
 'voa_all_question_keys_valid':all(type(q.get('answer')) is int and q['answer'] in range(len(q.get('options',[]))) for q in voa_questions),
 'offline_core_files_exist':all(entry=='/' or (ROOT/entry.removeprefix('/')).is_file() for entry in sw_refs),
 'release_lock_engaged':status.get('readyForRelease') is False,
 'human_mp3_not_misrepresented':status.get('verifiedHumanAudio')==0,
}
report={
 'audit':'PRIVATE PERSONAL USE PREFLIGHT / NOT RELEASE APPROVAL','date':'2026-10-29',
 'structuralChecks':check,'passed':sum(check.values()),'failed':[k for k,v in check.items() if not v],
 'actualCounts':{
  'toeflCoreWordIds':len(word_ids),'toeflCorePhrasalIds':len(phrasal_ids),
  'readingTasks':len(readings),'readingQuestions':len(questions),
  'sourceReadingAnswerIndexCount':dict(sorted(collections.Counter(q['answer'] for _,q in questions).items())),
  'newSessionReadingAnswerPosition':'balanced by v2 presentation, legacy sessions remain original',
  'writingTaskBank':len(writings),'voaInAppTranscripts':len(voa),
  'voaPublisherLinked':len(linked),'voaQuestions':len(voa_questions),'offlineCoreFiles':len(sw_refs),
  'verifiedBundledHumanMP3':status.get('verifiedHumanAudio'), 'syntheticMP3':status.get('bundledSyntheticAudio')},
 'testedOutsideThisScript':['npm test','Python unittest','example audit','audio quality gate','virtual Chromium desktop/mobile'],
 'mustNotBeClaimedPassed':['physical iPhone Safari','real HTTP browser offline WebKit','external audio playback and transcript alignment','independent native English editorial review','ETS calibrated scoring','official adaptive TOEFL'],
 'useDecision':'Windows local HTTP personal pilot conditionally suitable; iPhone Safari offline not signed off; release locked'
}
out=ROOT/'qa/final-personal-use-preflight-20261029.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':report['passed'],'total':len(check),'failed':report['failed']},ensure_ascii=False))
if report['failed']:raise SystemExit(1)
