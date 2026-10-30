#!/usr/bin/env python3
"""Hard release lock: NEVER describe a development snapshot as publishable.
Usage: python tools/release_gate.py. Nonzero exit means NO ZIP RELEASE / NO GITHUB PAGES DEPLOY.
"""
from pathlib import Path
import json, sys, hashlib
from audio_quality_gate import audit as audit_listening_audio
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/'data'/f'{name}.json').read_text(encoding='utf-8'))
vocab=read('vocabulary');phrasals=read('phrasals');episodes=read('episodes');drills=read('drills');readings=read('readings');grammar=read('grammar')
finance=[x for x in vocab if x.get('category') in ('finance','accounting')]
general=[x for x in vocab if x.get('category')=='general']
audio=list((ROOT/'assets/audio').glob('*.mp3'))
qualified_human=[]
for ep in episodes:
 if ep.get('audioType')!='human_recording':continue
 if not all(ep.get(field) for field in ('sourceUrl','sourceLicense','attribution','audio')):continue
 location=ROOT/ep['audio']
 if location.is_file() and location.stat().st_size>10000:
  qualified_human.append(ep)
audio_quality=audit_listening_audio()
authentic=read('authentic-listening')
linked_voa=read('voa-source-quizzes')
focus=read('fluency-focus')
focus_words=focus['vocabulary'];focus_phrasals=focus['phrasals']
by_id={x['id']:x for x in general}
phrasals_by_id={x['id']:x for x in phrasals}
def completed_focus(targets, available):
    return [available[x['lessonId']] for x in targets if x.get('status')=='context_draft' and x.get('lessonId') in available]
ready_words=completed_focus(focus_words,by_id)
ready_phrasals=completed_focus(focus_phrasals,phrasals_by_id)
criteria={
 'Focus shortlist: 500 B2 + 500 C1 distinct': len(focus_words)==1000 and len({x['word'] for x in focus_words})==1000 and sum(x['level']=='B2' for x in focus_words)==500 and sum(x['level']=='C1' for x in focus_words)==500,
 'Focus shortlist: 500 distinct phrasals': len(focus_phrasals)==500 and len({x['word'] for x in focus_phrasals})==500,
 '1,000 focused general context lessons completed': len(ready_words)==1000,
 '500 focused phrasal context lessons completed': len(ready_phrasals)==500,
 '1,000 focused general lessons editorially approved': len(ready_words)==1000 and all(x.get('editorialStatus')=='approved' for x in ready_words),
 '500 focused phrasal lessons editorially approved': len(ready_phrasals)==500 and all(x.get('editorialStatus')=='approved' for x in ready_phrasals),
 'Accounting/Finance extras >=200':len(finance)>=200,
 '200 finance/accounting entries individually approved':sum(x.get('editorialStatus')=='approved' for x in finance)>=200,
 'Phrasal verbs have real English definitions':all(len(p.get('definition',''))>24 and not p['definition'].startswith(p['word']+':') for p in phrasals),
 'Focus targets US-English and CEFR meaning validated':len(ready_words)==1000 and len(ready_phrasals)==500 and all(x.get('editorialStatus')=='approved' for x in ready_words+ready_phrasals),
 'All vocabulary cards have original semantic fields':all(v.get('tr') and len(v.get('definition',''))>=25 and len(v.get('example',''))>=25 for v in vocab),
 'At least two different context examples for every focused lesson':len(ready_words)==1000 and len(ready_phrasals)==500 and all(len(x.get('examples',[]))>=2 and len(set(x['examples']))==len(x['examples']) and x['examples'][0]==x['example'] for x in ready_words+ready_phrasals),
 'Minimum 50 original podcast lessons (legacy requirement)':len(episodes)>=50,
 'At least 40 verified human-voice lessons with in-app transcript and quiz':sum(bool(x.get('turns') and x.get('questions') and x.get('sourceUrl')) for x in authentic)>=40,
 'Publisher-only listening lessons individually audio/transcript verified':len(linked_voa)==0,
 'Human voice playback and source transcript alignment independently verified':len(authentic)>=40 and all(x.get('transcriptVerifiedAgainstAudio') and x.get('timingVerified') for x in authentic),
 'Minimum 60 listening drills':len(drills)>=60,
 'TOEFL core independently reviewed for US-English and exam relevance':(ROOT/'qa/toefl-core-signoff.json').is_file() and json.loads((ROOT/'qa/toefl-core-signoff.json').read_text()).get('approved') is True,
 'Minimum 30 reading lessons':len(readings)>=30,
 'Minimum 20 grammar lessons':len(grammar)>=20,
 'At least 10 licensed, attributed, bundled human recordings':len(qualified_human)>=10,
 'No unapproved synthetic podcasts included in build':not any((ROOT/ep['audio']).is_file() for ep in episodes),
 'Every listening recording licensed, timing-reviewed and approved for natural speech':audio_quality['status']=='READY',
 'Manual US-English editorial verification recorded':(ROOT/'qa/american_editorial_signoff.json').is_file(),
 'Browser E2E evidence desktop + iPhone WebKit':(ROOT/'qa/browser_e2e_report.json').is_file(),
}
# Require machine-readable QA to actually contain proven passes, not merely a file.
qa=ROOT/'qa/browser_e2e_report.json'
if qa.is_file():
 try:
  report=json.loads(qa.read_text());criteria['Browser E2E evidence desktop + iPhone WebKit']=all(report.get(k)== 'passed' for k in ('chromium_desktop','webkit_iphone'))
 except Exception:criteria['Browser E2E evidence desktop + iPhone WebKit']=False
qa=ROOT/'qa/american_editorial_signoff.json'
if qa.is_file():
 try:
  report=json.loads(qa.read_text());criteria['Manual US-English editorial verification recorded']=report.get('completed') is True and report.get('general_reviewed',0)>=1000 and report.get('b2_reviewed',0)>=500 and report.get('c1_reviewed',0)>=500 and report.get('phrasals_reviewed',0)>=500
 except Exception:criteria['Manual US-English editorial verification recorded']=False
status={
 'readyForRelease':all(criteria.values()),
 'general':len(general),'financeAccounting':len(finance),'phrasalVerbs':len(phrasals),
 'podcasts':len(episodes),'listeningDrills':len(drills),'readings':len(readings),'grammarLessons':len(grammar),
 'bundledSyntheticAudio':len(audio),'verifiedHumanAudio':len(qualified_human),
 'focusVocabularyTargets':len(focus_words),'focusPhrasalTargets':len(focus_phrasals),
 'focusContextWords':len(ready_words),'focusContextPhrasals':len(ready_phrasals),
 'glossOnly':len(read('rapid-vocabulary')),
 'toeflCoreWords':len(read('toefl-core')['wordLessonIds']),
 'toeflCorePhrasals':len(read('toefl-core')['phrasalLessonIds']),
 'toeflNewAcademicWords':len(read('toefl-academic')),
 # Recompute measured VOA QA counters on every release-gate invocation;
 # never let a stale README or manually updated status imply extra reviewed work.
 'voaPublisherSources':len(authentic)+len(linked_voa),
 'voaIntegratedPublisherTranscripts':len(authentic),
 'voaPublisherOnlyQuizzes':len(linked_voa),
 'voaQuizQuestionCount':sum(len(x['questions']) for x in authentic+linked_voa),
 'voaSpeakerTurnEvidenceQuestions':sum('sourceEvidenceTurn' in q and q.get('sourceEvidenceKind')!='stage_direction' for l in authentic for q in l['questions']),
 'voaStageDirectionTurnEvidenceQuestions':sum('sourceEvidenceTurn' in q and q.get('sourceEvidenceKind')=='stage_direction' for l in authentic for q in l['questions']),
 'voaTranscriptTurnEvidenceQuestions':sum('sourceEvidenceTurn' in q for l in authentic for q in l['questions']),
 'voaPublisherExcerptEvidenceQuestions':sum(
     all(k in q for k in ('sourceEvidencePublisherLine','sourceEvidencePublisherUrl','sourceEvidenceSpeaker','sourceEvidenceKind'))
     for l in linked_voa for q in l['questions']),
 'voaQuestionsAwaitingSourceEvidence':sum(
     not (('sourceEvidenceTurn' in q) if l in authentic else
          all(k in q for k in ('sourceEvidencePublisherLine','sourceEvidencePublisherUrl','sourceEvidenceSpeaker','sourceEvidenceKind')))
     for l in authentic + linked_voa for q in l['questions']),
 'voaAudioPlaybackVerifiedOnPhysicalIphone':0,
 'listeningNaturalApproved':audio_quality['approved_for_natural_listening'],
 'listeningNaturalPending':audio_quality['not_approved_for_natural_listening'],
 'gates':criteria,
}
# Recompute separate daily-expression counters from the actual teaching data, not
# from a stale snapshot. Preserve the release-lock's existing critical checks.
expressions_file=ROOT/'data/daily-expressions.json'
if expressions_file.is_file():
 bank=json.loads(expressions_file.read_text(encoding='utf-8'))
 cards=bank.get('cards',[])
 status['dailyExpressions']={
  'targetTotal':bank.get('meta',{}).get('targetTotal',500),
  'targetByLevel':bank.get('meta',{}).get('targetByLevel',{'B1':150,'B2':210,'C1':140}),
  'authored':len(cards),
  'authoredByLevel':{level:sum(x.get('level')==level for x in cards) for level in ('B1','B2','C1')},
  'independentEditorApproved':bank.get('meta',{}).get('independentEditorApproved') is True,
  'verifiedHumanAudio':sum(x.get('audioStatus')=='verified_human_recording' for x in cards),
  'fsrsLearningScope':'separate_expressions_map',
  'offlineAssetPrecachedInServiceWorker':"'./data/daily-expressions.json'" in (ROOT/'sw.js').read_text(encoding='utf-8'),
  'physicalSafariOfflineTested':False,
 }
(ROOT/'development-status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name,ok in criteria.items(): print(('PASS ' if ok else 'BLOCK')+name)
print('Release ready:',status['readyForRelease'])
if not status['readyForRelease']:
 print('LOCKED: do not generate a publication ZIP, upload to GitHub, or enable GitHub Pages.')
 sys.exit(1)
