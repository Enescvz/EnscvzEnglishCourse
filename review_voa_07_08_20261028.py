#!/usr/bin/env python3
"""Publisher-page reviewed Lesson 7 and evidence-only Lesson 8; not audio-approved.

One-time, idempotent, fail-closed upgrade. Never regenerates IDs, resets history,
changes Speaking or treats publisher text review as MP3 playback evidence.
"""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'data/voa-source-catalog.json'
AUTH=ROOT/'data/authentic-listening.json'
QUIZ=ROOT/'data/voa-source-quizzes.json'
TRANSCRIPT=ROOT/'sources/voa-reviewed-lesson-07-20261028.txt'
SOURCE7='https://learningenglish.voanews.com/a/lesson-7-tip-your-tour-guide/4064769.html'
SOURCE8='https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-8-best-barbecue/4073994.html'
MP3_7='https://voa-audio.voanews.eu/vle/2017/10/17/45e008c5-648b-4275-ad2d-d3b058d199a6_hq.mp3?download=1'
# Reviewed on original VOA Conversation pages. Quotes intentionally short enough
# to locate the correct speaker turn, not automatically inferred from an answer.
EVIDENCE7=(
    ('Boy','the word “FUTURE” was carved wrong! They carved “EUTURE”!'),
    ('Anna','I love riding under a bridge in a boat!'),
    ('Boy','The lawmakers did not want to walk around outside in bad weather.'),
    ('Penelope','I still can’t believe this thing drives and sails!'),
)
EVIDENCE8=(
    ('Anna','I’d like to get your advice on my latest project.'),
    ('Kelly','you were sent to cover a big food festival that has all kinds of barbecue.'),
    ('Anna','Most ingredients are kept secret!'),
    ('Anna','Most sauces are made with a tomato sauce, vinegar, and spices.'),
)

def parse_reviewed_transcript(text):
    turns=[]
    for line in text.splitlines():
        if not line.strip():continue
        m=re.fullmatch(r'([A-Za-z][A-Za-z .&]{0,35}): (.+)',line)
        if not m:raise ValueError('Unlabelled or malformed transcript turn: '+line[:100])
        turns.append({'speaker':m[1],'text':m[2]})
    if len(turns)<35:raise ValueError('Transcript shorter than 35 verified turns')
    return turns

def annotate(questions,evidence,turns=None):
    if len(questions)!=len(evidence):raise ValueError('Evidence count must match questions')
    for q,(speaker,quote) in zip(questions,evidence):
        if not 0<=q['answer']<len(q['options']):raise ValueError('Bad answer index')
        # Never bind speaker and quote to an invented transcript turn.
        if turns is not None:
            hits=[i for i,t in enumerate(turns) if t['speaker']==speaker and quote in t['text']]
            if len(hits)!=1:raise ValueError(f'Expected one exact speaker quote: {speaker}: {quote}')
            q['sourceEvidenceTurn']=hits[0]
        q['sourceEvidenceSpeaker']=speaker
        q['sourceEvidence']=quote
        q['sourceEvidenceReview']='publisher-page-text-compared-not-audio'
    return questions

def run():
    cat=json.loads(CAT.read_text('utf8'))
    auth=json.loads(AUTH.read_text('utf8'))
    linked=json.loads(QUIZ.read_text('utf8'))
    # Later development snapshots already promoted lesson 8 to the full
    # transcript deck. This historical import must be a no-op in that case:
    # never demote a lesson or overwrite newer source-turn evidence.
    if all(any(x['id'] == f'voa-linked-2-{n:02d}' for x in auth) for n in (7, 8)):
        if any(x['catalogId'] in ('voa-2-07', 'voa-2-08') for x in linked):
            raise ValueError('Duplicate promoted lesson in linked deck')
        if len(auth) + len(linked) != 50 or sum(len(x['questions']) for x in auth + linked) != 204:
            raise ValueError('Unexpected count drift after earlier promotions')
        return {'imported': len(auth), 'publisherOnly': len(linked),
                'alreadyPromoted': (7, 8), 'releaseApproved': False}
    by_cat={x['id']:x for x in cat}
    for cid,url in (('voa-2-07',SOURCE7),('voa-2-08',SOURCE8)):
        if by_cat[cid]['sourceUrl']!=url:raise ValueError(cid+' source URL mismatch')
    lesson7id='voa-linked-2-07'
    lesson7=next((x for x in auth if x['id']==lesson7id),None)
    pending7=next((x for x in linked if x['catalogId']=='voa-2-07'),None)
    turns=parse_reviewed_transcript(TRANSCRIPT.read_text('utf8'))
    if pending7 is not None:
        annotate(pending7['questions'],EVIDENCE7,turns)
        lesson7={
            'id':pending7['id'],'title':pending7['title'],'level':pending7['level'],
            'topic':pending7['topic'],'minutes':3.95,'sourceUrl':SOURCE7,
            'audioUrl':MP3_7,'focus':['on the left','under a bridge','inside','outside','tip your guide'],
            'attribution':'VOA Learning English','sourceSeries':"Let's Learn English — Level 2",
            'sourceLicense':'VOA-original public domain; third-party segments not cleared',
            'rightsUrl':by_cat['voa-2-07']['rightsUrl'],
            'audioProvider':'VOA Learning English','audioType':'human_dialogue_source',
            'audioAvailability':'external_online_stream_only','offlineReady':False,
            'audioBundled':False,'transcriptSource':'Publisher-provided VOA Conversation section',
            'transcriptVerifiedAgainstAudio':False,'timingVerified':False,
            'quality':'publisher_transcript_checked_audio_playback_unverified',
            'transcriptReviewedOn':'2026-10-28','turns':turns,
            'transcriptReviewNote':'VOA Conversation speakers and lines manually compared; non-spoken pedagogical preposition table not transcribed as speech.',
            'questions':pending7['questions']}
        auth.append(lesson7)
        linked=[q for q in linked if q['catalogId']!='voa-2-07']
        by_cat['voa-2-07'].update({'integrationStatus':'interactive_transcript_quiz',
            'interactiveLessonId':lesson7id,'transcriptImported':True,'questionCount':4,
            'audioBundled':False,'audioPlayback':'VOA MP3 linked; playback unverified',
            'sourcePageReviewed':'2026-10-28'})
        by_cat['voa-2-07'].pop('linkedQuizId',None)
    else:
        if lesson7 is None or lesson7['turns']!=turns:raise ValueError('Lesson 7 previously imported but source does not match')
        annotate(lesson7['questions'],EVIDENCE7,turns)

    lesson8=next(q for q in linked if q['catalogId']=='voa-2-08')
    annotate(lesson8['questions'],EVIDENCE8)
    lesson8['sourceReview']='All four answers compared with original VOA Conversation on 2026-10-28; transcript/audio still publisher-only'
    lesson8['questionEvidenceReviewedOn']='2026-10-28'
    by_cat['voa-2-08']['sourcePageReviewed']='2026-10-28'

    if len(cat)!=50 or len(auth)+len(linked)!=50 or sum(len(x['questions']) for x in auth+linked)!=204:
        raise ValueError('Unexpected count drift')
    ids=[x['id'] for x in auth+linked]
    if len(set(ids))!=50:raise ValueError('Lesson IDs not unique')
    for p,value in ((AUTH,auth),(QUIZ,linked),(CAT,cat)):
        p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n','utf8')
    return {'imported':len(auth),'publisherOnly':len(linked),'questionEvidenceCount':sum('sourceEvidenceSpeaker' in q and q.get('sourceEvidence')!='VOA publisher Conversation transcript (see linked original)' for l in auth+linked for q in l['questions']),'releaseApproved':False}

if __name__=='__main__':print(json.dumps(run(),indent=2))
