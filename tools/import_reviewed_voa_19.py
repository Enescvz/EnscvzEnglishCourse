"""Review-gated VOA19 importer; preserves existing linked ID and answer history."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sources/voa-reviewed-lesson-19-20261028.txt'
AUDIO='https://voa-audio.voanews.eu/vle/2018/02/08/aa7b1559-adea-4534-8d4f-649785319a21_hq.mp3?download=1'
def load(name):return json.loads((ROOT/'data'/name).read_text())
def save(name,d): (ROOT/'data'/name).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def import_reviewed():
    catalog=load('voa-source-catalog.json');interactive=load('authentic-listening.json');linked=load('voa-source-quizzes.json')
    item=next(x for x in catalog if x['id']=='voa-2-19')
    if any(x['id']=='voa-linked-2-19' for x in interactive):return False
    x=next(x for x in linked if x['id']=='voa-linked-2-19')
    assert item['sourceUrl']==x['sourceUrl']
    turns=[]
    for line in SOURCE.read_text().splitlines():
        if not line or line.startswith('#'):continue
        speaker,text=line.split('|',1)
        assert speaker and text
        turns.append({'speaker':speaker,'text':text,'kind':'stage_direction' if speaker=='Stage direction' else 'speech'})
    assert len(turns)>=60 and any(x['speaker']=='Security guard' for x in turns)
    for q in x['questions']:
        needle=q['sourceEvidence'].casefold().strip()
        matches=[(i,t) for i,t in enumerate(turns) if needle in t['text'].casefold()]
        assert len(matches)==1,(needle,len(matches))
        i,t=matches[0]
        assert q['sourceEvidenceKind']==t['kind'],(q['question'],q['sourceEvidenceKind'],t['kind'])
        q['sourceEvidenceTurn']=i
        q['sourceEvidenceSpeaker']=t['speaker']
        q['sourceEvidenceKind']=t['kind']
        q['sourceReviewStatus']='publisher_page_turn_reviewed_not_audio_verified'
    interactive.append({'id':x['id'],'title':'Movie Night — Polite Questions', 'level':x['level'], 'topic':x['topic'],
        'minutes':4.78,'focus':['indirect questions','would you mind','movie theater','shush','milkshake'],'sourceUrl':x['sourceUrl'],'audioUrl':AUDIO,'attribution':'VOA Learning English — Lesson 19',
        'sourceSeries':"Let's Learn English — Level 2",'sourceLicense':'VOA original public domain; attributed; excludes third-party material',
        'rightsUrl':'https://learningenglish.voanews.com/p/6861.html', 'audioProvider':'VOA Learning English',
        'audioType':'human_dialogue_source','audioAvailability':'external_online_stream_only',
        'audioBundled':False,'offlineReady':False, 'transcriptSource':'VOA publisher Conversation page',
        'transcriptVerifiedAgainstAudio':False,'timingVerified':False,'quality':'external_source_not_independently_audio_reviewed',
        'turns':turns,'questions':x['questions']})
    linked=[y for y in linked if y['id']!=x['id']]
    item.update(interactiveLessonId=x['id'],integrationStatus='interactive_transcript_quiz',transcriptImported=True,
        linkedQuizId=None,audioPlayback='VOA MP3 linked; playback unverified',sourcePageReviewed='2026-10-28')
    save('authentic-listening.json',interactive);save('voa-source-quizzes.json',linked);save('voa-source-catalog.json',catalog)
    return True
if __name__=='__main__':print(json.dumps({'imported':import_reviewed()}))
