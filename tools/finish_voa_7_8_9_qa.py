#!/usr/bin/env python3
"""Regenerate non-speaking audit counters from current project data, no false approvals."""
import json
from collections import Counter
from pathlib import Path
root=Path(__file__).resolve().parents[1]
rfile=root/'qa/non-speaking-quality-report.json'
r=json.loads(rfile.read_text(encoding='utf8'))
a=json.loads((root/'data/authentic-listening.json').read_text(encoding='utf8'))
l=json.loads((root/'data/voa-source-quizzes.json').read_text(encoding='utf8'))
r.update({'integratedPublisherTranscripts':len(a),'publisherOnlyTranscriptsAndAudio':len(l),
          'originalVOAComprehensionQuestions':sum(len(x['questions']) for x in a+l),
          'publisherTranscriptTurnBoundQuestionEvidence':sum(bool(q.get('sourceEvidenceTurn') is not None) for x in a for q in x['questions']),
          'directAudioUrlUnavailableTranscriptLessons':sum(not bool(x.get('audioUrl')) for x in a),
          'externalMP3PlaybackVerifiedOnDevice':0,'bundledLicensedHumanMP3':0,
          'audioTranscriptTimestampVerified':0,'fullSemanticEditorialApproval':False,
          'iPhoneSafariQAApproved':False,'releaseApproved':False})
r['remainingTasks']=[
 f'Import and source-compare {len(l)} remaining publisher transcripts',
 'Verify Level 2 Lesson 7 publisher song/preposition appendix separately from spoken conversation',
 'Locate a verified independent audio source for Level 2 Lesson 8 (do not put a page URL in audio src)',
 'Independently verify online MP3 playback and legal reuse on physical devices',
 'Verify question meaning and answer evidence for previously source-linked quizzes',
 'Review speech-frequency CEFR and US semantics with language editor',
 'Replace or demote 42 robotic eSpeak MP3s for natural listening',
 'Test Safari, Android Chrome, offline fallback, and screen-reader interactions',
]
rfile.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
statusfile=root/'development-status.json'
s=json.loads(statusfile.read_text(encoding='utf8'))
s['readyForRelease']=False
s['verifiedHumanAudio']=0
s['gates']['At least 40 verified human-voice lessons with in-app transcript and quiz']=len(a)>=40 and False
s['gates']['Publisher-only listening lessons individually audio/transcript verified']=False
s['gates']['Human voice playback and source transcript alignment independently verified']=False
statusfile.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'inAppTranscripts':len(a),'publisherOnly':len(l),'questions':r['originalVOAComprehensionQuestions'],'evidencedQuestions':r['publisherTranscriptTurnBoundQuestionEvidence']},indent=2))
