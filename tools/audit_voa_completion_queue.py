#!/usr/bin/env python3
"""Strict VOA provenance audit + actionable publisher-review queue, non-Speaking.

This script distinguishes verified in-app transcript turns from publisher excerpt
evidence on linked pages; it never claims remote audio playback or changes IDs.
"""
import csv,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; QA=ROOT/'qa'
def load(p):return json.loads(p.read_text(encoding='utf8'))
def audit():
    full=load(DATA/'authentic-listening.json'); linked=load(DATA/'voa-source-quizzes.json'); catalog=load(DATA/'voa-source-catalog.json')
    rows=[]; errors=[]
    ids=[x['id'] for x in full+linked];urls=[x['sourceUrl'] for x in catalog]
    if (len(full)+len(linked),len(catalog),len(set(ids)),len(set(urls)))!=(50,50,50,50):errors.append('catalog or lesson ID cardinality differs from 50')
    cat_by_url={c['sourceUrl']:c for c in catalog}; counts=Counter(); total=0
    for item in full+linked:
        imported=item in full
        if item['sourceUrl'] not in cat_by_url:errors.append('source URL missing: '+item['id'])
        if imported:
            if item.get('audioAvailability') not in ('external_online_stream_only','publisher_page_only'):errors.append('Bad audio availability: '+item['id'])
            if item.get('transcriptVerifiedAgainstAudio') or item.get('timingVerified') or item.get('offlineReady'):errors.append('Unproven audio flags: '+item['id'])
        else:
            if item.get('transcriptImported') or item.get('audioBundled') or item.get('playerVerified'):errors.append('Falsely approved linked lesson: '+item['id'])
        for ix,q in enumerate(item['questions']):
            total+=1
            if q.get('answer') not in range(len(q.get('options',[]))) or len(q.get('options',[]))!=4:errors.append(f'Invalid key {item["id"]} {ix}')
            complete=imported and all(k in q for k in ('sourceEvidenceTurn','sourceEvidenceSpeaker','sourceEvidence'))
            if complete:
                turns=item.get('turns') or []
                t=q['sourceEvidenceTurn']
                if type(t) is not int or t not in range(len(turns)):errors.append(f'Invalid source turn {item["id"]} {ix}')
                elif turns[t]['speaker']!=q['sourceEvidenceSpeaker'] or q['sourceEvidence'] not in turns[t]['text']:errors.append(f'No exact evidence {item["id"]} {ix}')
                else:
                    counts['turnVerified']+=1
                    if q.get('sourceEvidenceKind')=='stage_direction':counts['stageDirectionTurn']+=1
                    else:counts['spokenTurn']+=1
            elif (not imported and all(k in q for k in ('sourceEvidencePublisherLine','sourceEvidenceSpeaker','sourceEvidence','sourceEvidenceKind','sourceEvidencePublisherUrl'))):
                if q['sourceEvidenceKind'] not in ('speech','stage_direction') or q['sourceEvidencePublisherUrl'] != item['sourceUrl'] or not q['sourceEvidence'] or q['sourceEvidencePublisherLine']<100:
                    errors.append(f'Bad linked excerpt proof {item["id"]} {ix}')
                elif q['sourceEvidenceKind']=='stage_direction' and q['sourceEvidenceSpeaker']!='Stage direction':
                    errors.append(f'Stage direction mislabeled as spoken audio {item["id"]} {ix}')
                elif q.get('sourceEvidenceTurn') is not None:
                    errors.append(f'No in-app transcript turn for source-linked {item["id"]} {ix}')
                else:
                    counts['linkedExcerptVerified']+=1
            else:
                counts['pending']+=1
                rows.append({'lessonId':item['id'],'catalogId':item.get('catalogId') or cat_by_url[item['sourceUrl']]['id'],
                    'publisherURL':item['sourceUrl'],'questionIndex':ix+1,
                    'question':q['question'],'selectedAnswer':q['options'][q['answer']],
                    'verificationStatus':'PENDING_SOURCE_TURN_REVIEW',
                    'nextAction':'Compare official Conversation speaker+turn; check answer and distractors',
                    'audioPlaybackVerified':False})
    if total!=204 or counts['turnVerified']+counts['linkedExcerptVerified']+counts['pending']!=204:errors.append('204-question invariant violated')
    if errors:raise ValueError('VOA QA validation failed: '+'; '.join(errors[:8]))
    QA.mkdir(exist_ok=True)
    with (QA/'voa-question-review-queue.csv').open('w',newline='',encoding='utf-8-sig') as f:
        columns=['lessonId','catalogId','publisherURL','questionIndex','question','selectedAnswer',
                 'verificationStatus','nextAction','audioPlaybackVerified']
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
    report={
        'scope':'Source/text evidence only; not listening playback or editorial signoff',
        'totalVOASourceLessons':len(catalog),'inAppTranscriptLessons':len(full),'publisherPageOnlyLessons':len(linked),
        'totalOriginalQuestions':total,'speakerAndTurnEvidenceChecked':counts['turnVerified'],
        'publisherLinkedExcerptEvidenceChecked':counts['linkedExcerptVerified'],
        'spokenTurnEvidenceChecked':counts['spokenTurn'],
        'stageDirectionTurnEvidenceChecked':counts['stageDirectionTurn'],
        'sourceEvidenceTotal':counts['turnVerified']+counts['linkedExcerptVerified'],
        'pendingQuestionSourceEvidence':counts['pending'],
        'unverifiedRemotePlaybackCount':len(full)+len(linked),
        'localHumanAudioMP3Count':0,'physicalIPhoneSafariPassed':False,'offlineE2EPassed':False,
        'sourceLicense':'https://learningenglish.voanews.com/p/6861.html',
        'remainingLessons':[{'id':x['id'],'sourceUrl':x['sourceUrl'],'pendingQuestions':sum(not ('sourceEvidencePublisherLine' in q) for q in x['questions']), 'needsFullTranscript':True} for x in linked],
        'releaseApproved':False,'readyForRelease':False,
        'nextStep':'Source excerpt inspection queue is empty; remaining full transcripts still publisher-only, and audio/third-party permissions require separate checks.'
    }
    (QA/'voa-source-coverage.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    return report
if __name__=='__main__':
    result=audit()
    print(json.dumps({k:v for k,v in result.items() if k!='remainingLessons'},indent=2))
