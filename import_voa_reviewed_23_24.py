#!/usr/bin/env python3
"""Import publisher VOA-original scripts for L2 lessons 23 and 24, excluding third-party lyrics.

Prepared from the official VOA Learning English Conversation pages, and linked back
for independent review. Never claims physical audio playback verification.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    23: {
        'file':'sources/voa-reviewed-publisher/level2-23.txt',
        'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-23/4287922.html',
        'audioUrl':'https://voa-audio.voanews.eu/vle/2018/03/15/b53a7e2c-2dd1-4623-b4d0-92efba982191_hq.mp3?download=1',
        'minutes':4.9,
        'exclusion':'The Police song and the guest musician\'s song lyrics are excluded; original VOA dialogue retained.',
    },
    24: {
        'file':'sources/voa-reviewed-publisher/level2-24.txt',
        'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-24/4307612.html',
        'audioUrl':'https://voa-audio.voanews.eu/vle/2018/03/23/f1f4841a-c2cb-4ee3-9cbe-2a132ffb5c8e_hq.mp3?download=1',
        'minutes':4.8,
        'exclusion':None,
    }
}
RIGHTS='https://learningenglish.voanews.com/p/6861.html'

def load_turns(file):
    turns=[]
    for n,line in enumerate((ROOT/file).read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        if '|' not in line:raise ValueError(f'Invalid transcript line {file}:{n}')
        speaker,text=(x.strip() for x in line.split('|',1))
        if not speaker or not text:raise ValueError(f'Empty transcript line {file}:{n}')
        if 'every breath you take' in text.casefold() or 'every move you make' in text.casefold():
            raise ValueError('Third-party song lyrics must not be republished')
        turns.append({'speaker':speaker,'text':text,'kind':'stage_direction' if speaker=='Stage direction' else 'speech'})
    if len(turns)<35: raise ValueError(f'Script too short to mark imported {file}')
    return turns

def apply():
    paths={k:ROOT/k for k in ['data/authentic-listening.json','data/voa-source-quizzes.json','data/voa-source-catalog.json','development-status.json']}
    full=json.loads(paths['data/authentic-listening.json'].read_text());linked=json.loads(paths['data/voa-source-quizzes.json'].read_text())
    catalog=json.loads(paths['data/voa-source-catalog.json'].read_text());status=json.loads(paths['development-status.json'].read_text())
    done=0
    for number,meta in SOURCES.items():
        lesson_id=f'voa-linked-2-{number:02d}'
        if any(x['id']==lesson_id for x in full):continue
        quiz=next((x for x in linked if x['id']==lesson_id),None)
        if quiz is None:raise ValueError(f'Missing quiz {lesson_id}')
        if quiz['sourceUrl']!=meta['sourceUrl']:raise ValueError(f'Official URL mismatch for {lesson_id}')
        turns=load_turns(meta['file'])
        entry={
            'id':lesson_id, 'title':quiz['title'], 'level':quiz['level'],'topic':quiz['topic'],
            'minutes':meta['minutes'], 'sourceUrl':meta['sourceUrl'],'audioUrl':meta['audioUrl'],
            'attribution':'VOA Learning English — publisher Conversation', 'sourceSeries':"Let's Learn English — Level 2",
            'sourceLicense':'VOA-original dialogue public domain with attribution; third-party works excluded',
            'rightsUrl':RIGHTS, 'audioProvider':'VOA Learning English','audioType':'human_dialogue_source',
            'audioAvailability':'external_online_stream_only', 'audioBundled':False, 'offlineReady':False,
            'transcriptSource':'VOA publisher Conversation page (manually compared; excludes rights-restricted third-party material)',
            'transcriptImported':True, 'transcriptVerifiedAgainstAudio':False, 'timingVerified':False,
            'quality':'external_source_not_independently_audio_reviewed', 'turns':turns,
            'questions':quiz['questions'],
            'transcriptScope':'published_VOA_original_dialogue_with_exclusions' if meta['exclusion'] else 'published_VOA_original_dialogue',
            'transcriptRightsExclusion':meta['exclusion'],
        }
        for q in entry['questions']:
            evidence=q.get('sourceEvidence','')
            speaker=q.get('sourceEvidenceSpeaker','')
            hits=[i for i,t in enumerate(turns) if t['speaker'].casefold()==speaker.casefold() and evidence.casefold() in t['text'].casefold()]
            if len(hits)!=1:
                raise ValueError(f'Cannot uniquely verify {lesson_id}: {q["question"]} ({hits})')
            q['sourceEvidenceTurn']=hits[0]
            q['sourceReviewStatus']='publisher_page_turn_reviewed_not_audio_verified'
        item=next(x for x in catalog if x['id']==quiz['catalogId'])
        item.update({'integrationStatus':'interactive_transcript_quiz','interactiveLessonId':lesson_id,
                     'transcriptImported':True,'linkedQuizId':None,'audioBundled':False,
                     'audioPlayback':'VOA MP3 linked; playback unverified','sourcePageReviewed':'2026-10-29',
                     'transcriptRightsExclusion':meta['exclusion']})
        full.append(entry)
        linked=[x for x in linked if x['id']!=lesson_id]
        done+=1
    if done:
        assert len(full)+len(linked)==50
        assert sum(len(x['questions']) for x in full+linked)==204
        status.update({
          'voaIntegratedPublisherTranscripts':len(full),
          'voaPublisherOnlyQuizzes':len(linked),
          'voaSpeakerTurnEvidenceQuestions':sum('sourceEvidenceTurn' in q and q.get('sourceEvidenceKind')!='stage_direction' for x in full for q in x['questions']),
          'voaStageDirectionTurnEvidenceQuestions':sum('sourceEvidenceTurn' in q and q.get('sourceEvidenceKind')=='stage_direction' for x in full for q in x['questions']),
          'voaTranscriptTurnEvidenceQuestions':sum('sourceEvidenceTurn' in q for x in full for q in x['questions']),
          'voaPublisherExcerptEvidenceQuestions':sum('sourceEvidence' in q and 'sourceEvidenceTurn' not in q for x in linked for q in x['questions'])
        })
        for key,value in [('data/authentic-listening.json',full),('data/voa-source-quizzes.json',linked),('data/voa-source-catalog.json',catalog),('development-status.json',status)]:
            paths[key].write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return done

if __name__=='__main__': print(f'Imported {apply()} VOA lesson(s)')
