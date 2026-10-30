"""Source-reviewed VOA-original transcript importer (NOT audio QA). Safe, idempotent, preserves IDs."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
URLS={20:'https://voa-audio.voanews.eu/vle/2018/02/15/8b42c321-07ea-4eb1-a1f9-e7cc6019606e_hq.mp3?download=1',
      21:'https://voa-audio.voanews.eu/vle/2018/03/06/fabffd67-3af1-480c-925c-0b87e11fe82b_hq.mp3?download=1'}
def read(name):return json.loads((ROOT/'data'/name).read_text())
def write(name,data):(ROOT/'data'/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def source_turns(n):
    src=ROOT/'sources'/f'voa-reviewed-lesson-{n}-20261029.txt'
    turns=[]
    for line in src.read_text().splitlines():
        if not line or line.startswith('#'):continue
        speaker,phrase=line.split('|',1)
        assert speaker and phrase
        turns.append({'speaker':speaker,'text':phrase,'kind':'stage_direction' if speaker=='Stage direction' else 'speech'})
    assert len(turns)>40
    return turns

def integrate():
    interactive=read('authentic-listening.json');linked=read('voa-source-quizzes.json');catalog=read('voa-source-catalog.json')
    changed=[]
    for n in (20,21):
        lid=f'voa-linked-2-{n}';catalog_id=f'voa-2-{n}'
        if any(x['id']==lid for x in interactive):continue
        x=next(x for x in linked if x['id']==lid)
        c=next(x for x in catalog if x['id']==catalog_id)
        assert x['sourceUrl']==c['sourceUrl']
        turns=source_turns(n)
        for q in x['questions']:
            speaker=q['sourceEvidenceSpeaker'];kind=q['sourceEvidenceKind'];phrase=q['sourceEvidence'].casefold()
            found=[(i,t) for i,t in enumerate(turns) if t['speaker']==speaker and t['kind']==kind and phrase in t['text'].casefold()]
            assert len(found)==1,(lid,q['question'],found)
            i,t=found[0];q['sourceEvidenceTurn']=i;q['sourceEvidenceSpeaker']=t['speaker']
            q['sourceReviewStatus']='publisher_page_turn_reviewed_not_audio_verified'
        interactive.append({'id':lid,'title':x['title'],'level':x['level'],'topic':x['topic'],
          'minutes':4.68 if n==20 else 4.1,'sourceUrl':x['sourceUrl'],'audioUrl':URLS[n],
          'attribution':f'VOA Learning English — Lesson {n}', 'sourceSeries':"Let's Learn English — Level 2",
          'sourceLicense':'VOA original public domain; attributed; excludes third-party material',
          'rightsUrl':'https://learningenglish.voanews.com/p/6861.html',
          'audioProvider':'VOA Learning English', 'audioType':'human_dialogue_source',
          'audioAvailability':'external_online_stream_only','audioBundled':False,'offlineReady':False,
          'transcriptSource':'VOA publisher Conversation page','transcriptVerifiedAgainstAudio':False,'timingVerified':False,
          'quality':'external_source_not_independently_audio_reviewed','turns':turns,'questions':x['questions']})
        linked=[q for q in linked if q['id']!=lid]
        c.update(interactiveLessonId=lid,integrationStatus='interactive_transcript_quiz',transcriptImported=True,
          linkedQuizId=None,audioPlayback='VOA MP3 linked; playback unverified',sourcePageReviewed='2026-10-29')
        changed.append(lid)
    if changed:
        write('authentic-listening.json',interactive);write('voa-source-quizzes.json',linked);write('voa-source-catalog.json',catalog)
    return changed
if __name__=='__main__':print(json.dumps({'newlyIntegrated':integrate()}))
