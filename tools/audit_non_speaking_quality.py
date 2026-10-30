#!/usr/bin/env python3
"""Honest readiness report for Listening, Reading and Grammar. Speaking excluded.

Passing structured checks does not certify natural audio, CEFR levels or editorial quality.
"""
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(name):
    return json.loads((ROOT/'data'/f'{name}.json').read_text(encoding='utf-8'))

def audit():
    catalog,full,linked=read('voa-source-catalog'),read('authentic-listening'),read('voa-source-quizzes')
    reading,grammar=read('readings'),read('grammar')
    all_quizzes=full+linked
    assert len(catalog)==50 and len(all_quizzes)==50
    assert len({x['sourceUrl'] for x in catalog})==50
    assert len({x['id'] for x in all_quizzes})==50
    assert len({x['id'] for x in reading})==30
    assert len({x['id'] for x in grammar})==20
    assert all(x['audioAvailability']=='external_online_stream_only' and not x['offlineReady'] for x in full)
    assert all(not x['audioBundled'] and not x['transcriptImported'] for x in linked)
    assert all(not x.get('transcriptVerifiedAgainstAudio') and not x.get('timingVerified') for x in full)
    # Questions with publisher-turn citations must point to the actual quoted turn.
    evidence_count=0
    for lesson in full:
        turns=lesson['turns']
        for q in lesson['questions']:
            if 'sourceEvidenceTurn' not in q:
                continue
            index=q['sourceEvidenceTurn']
            assert isinstance(index,int) and 0<=index<len(turns)
            turn=turns[index]
            assert turn['speaker']==q['sourceEvidenceSpeaker']
            assert q['sourceEvidence'] in turn['text']
            evidence_count+=1
    assert evidence_count>=12
    app=(ROOT/'js/app.js').read_text(encoding='utf-8')
    assert 'if(!ui.authenticListened)' in app and 'if(!ui.linkedListened)' in app
    reading_keys=Counter(q['answer'] for x in reading for q in x['questions'])
    grammar_keys=Counter(x.get('answerIndex',0) for x in grammar)
    assert max(reading_keys.values())-min(reading_keys.values())<=1
    assert set(grammar_keys.values())=={5}
    sources_mapped={x['id'] for x in catalog}
    assert {x['catalogId'] for x in linked}<=sources_mapped
    for c in catalog:
        if c.get('transcriptImported'):
            assert any(x['id']==c['interactiveLessonId'] for x in full)
        else:
            assert any(x['id']==c['linkedQuizId'] for x in linked)
    report={
        'scope':'Non-speaking educational quality (development snapshot)',
        'humanVoicedPublisherSources':len(catalog),
        'quizEnabledSourceLessons':len(all_quizzes),
        'integratedPublisherTranscripts':len(full),
        'publisherOnlyTranscriptsAndAudio':len(linked),
        'originalVOAComprehensionQuestions':sum(len(x['questions']) for x in all_quizzes),
        'publisherTranscriptTurnBoundQuestionEvidence':evidence_count,
        'bothListeningFlowsRequireUserSelfReport':True,
        'externalMP3PlaybackVerifiedOnDevice':0,
        'bundledLicensedHumanMP3':0,
        'audioTranscriptTimestampVerified':0,
        'originalReadingLessons':len(reading),
        'readingQuestions':sum(len(x['questions']) for x in reading),
        'grammarLessons':len(grammar),
        'readingCorrectOptionDistribution':dict(sorted(reading_keys.items())),
        'grammarCorrectOptionDistribution':dict(sorted(grammar_keys.items())),
        'fullSemanticEditorialApproval':False,
        'phoneticAndCEFRReviewApproved':False,
        'iPhoneSafariQAApproved':False,
        'sourceLinkedQuizzesRequireListeningSelfReport':True,
        'remainingTasks':[f'Import and manually compare {len(linked)} remaining publisher transcripts',
                          'Independently verify online MP3 playback and legal reuse/attribution on actual device',
                          'Review question answer evidence and CEFR labels with language editor',
                          'Replace or demote 42 robotic eSpeak MP3s for natural listening',
                          'Test Safari, Android Chrome, offline fallback and screen-reader interactions'],
        'releaseApproved':False,
    }
    out=ROOT/'qa/non-speaking-quality-report.json'
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report
if __name__=='__main__':print(json.dumps(audit(),ensure_ascii=False,indent=2))
