#!/usr/bin/env python3
"""Import public-domain VOA-original Lesson 22 (no external audio copied)."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source='https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-22/4283017.html'
audio='https://voa-audio.voanews.eu/vle/2018/03/06/0fd0e840-fff7-4d90-aaeb-eba188526184_hq.mp3?download=1'
# Transcribed from the publisher's Conversation section, speaker-by-speaker;
# no commercially licensed song lyrics, external news, or other third-party passages.
turns=[
('Sue','Welcome to class, Anna. I can’t wait to see your trash!'),
('Sue','Oh, okay. Alright, it’s a -- it’s a net with a … oh, it’s got a hole in it. Tell me about that.'),
('Anna','This net said to me, “Anna, I used to catch stuff. I don’t anymore. So, use me, Anna.” That’s what it said. It said, “Use me, Anna.”'),
('Sue','Okay. So...it’s a plastic helmet.'),
('Anna','This plastic helmet said, “Anna. Hey, Anna, find me a head.”'),
('Sue','Okay, um...and a broken toy.'),
('Anna','This broken toy … this broken toy said to me – it said, “Anna, help me find fun.” “Help me, Anna” is what it said.'),
('Sue','Anna, this stuff is not saying anything to you or me or anyone. It’s what we like to call in the business … garbage.'),
('Anna','But you said to bring in trash.'),
('Sue',"Sometimes trash is treasure. Sometimes it's just trash."),
('Sue','Anna, don’t worry. Next week, I could teach you decoupage.'),
('Anna','Decoupage. Decoupage. That’s fun to say.'),
('Sue','All you need to bring is a clean shoe box. A box that held shoes.'),
('Anna','I got it. I got it! See you next week!'),
('Prof. Bot','Ut oh. It looks like Anna doesn’t know the difference between treasure and trash. She thinks those things are telling her something!'),
('Prof. Bot','The words tell and say have similar meanings. But we use them in different ways.'),
('Prof Bot','Tell means “to inform or instruct someone with words” and is almost always followed by an indirect object. For example, Sue says, “Tell me about that.”'),
('Prof. Bot','The word me is the indirect object and tells us who is being told.'),
('Prof. Bot','Say means “to express something with words” and focuses more on the words used. For example, Anna says, “That’s what it said. It said, ‘Use me, Anna.’”'),
('Prof. Bot','Listen for when Anna and Sue use tell and say.'),
('Sue','Anna, welcome to Decoupage class. Decoupage is just gluing pretty pictures onto stuff.'),
('Stage direction','(Sue gets a phone call.)'),
('Sue','Anna, I’ve got to talk to this person. I’ll be right back. Don’t start without me.'),
('Anna','Got it.'),
('Stage direction','(Sue leaves to take her phone call. Anna gets glue everywhere. She becomes covered with glue and paper.)'),
('Anna','Okay. I can fix this.'),
('Sue','Anna, what happened? I told you to wait for me!'),
('Anna','Actually, you told me not to start without you, which I didn’t. Your glue is really sticky.'),
('Sue',"Next week, let’s try lamp making. There’s – there’s no glue. Here's a flier."),
('Anna','Thanks. See you next week.'),
('Sue','Anna, you did really well this week. I think lamp making might be your thing!'),
('Anna','Thanks, Sue. I did everything you told me to do.'),
('Sue','Remember: I said to read the instructions really carefully. Where are those instructions?'),
('Anna','Let’s just plug it in!'),
('Stage direction','(Anna plugs in the lamp and, suddenly, the city loses electricity.)'),
('Anna','So, what class will you be teaching next week?'),
('Prof. Bot','Too bad Anna didn’t follow instructions! Visit our website for more on tell and say!')]
def apply():
 a=ROOT/'data/authentic-listening.json';b=ROOT/'data/voa-source-quizzes.json';c=ROOT/'data/voa-source-catalog.json';d=ROOT/'development-status.json'
 full=json.loads(a.read_text());linked=json.loads(b.read_text());catalog=json.loads(c.read_text());status=json.loads(d.read_text())
 id='voa-linked-2-22'
 if any(x['id']==id for x in full):return False
 entry=next(x for x in linked if x['id']==id)
 x={'id':id,'title':entry['title'],'level':entry['level'],'topic':entry['topic'],'minutes':4.78,
    'sourceUrl':source,'audioUrl':audio,'attribution':'VOA Learning English — Lesson 22',
    'sourceSeries':"Let's Learn English — Level 2",'sourceLicense':'VOA original public domain; attributed; third-party works excluded',
    'rightsUrl':'https://learningenglish.voanews.com/p/6861.html','audioProvider':'VOA Learning English',
    'audioType':'human_dialogue_source','audioAvailability':'external_online_stream_only','audioBundled':False,
    'offlineReady':False,'transcriptSource':'VOA publisher Conversation page','transcriptVerifiedAgainstAudio':False,
    'timingVerified':False,'quality':'external_source_not_independently_audio_reviewed',
    'turns':[{'speaker':s,'text':t,'kind':'stage_direction' if s=='Stage direction' else 'speech'} for s,t in turns],
    'questions':entry['questions']}
 for q in x['questions']:
  matches=[i for i,t in enumerate(x['turns']) if t['speaker']==q['sourceEvidenceSpeaker'] and q['sourceEvidence'].casefold() in t['text'].casefold()]
  if len(matches)!=1:raise ValueError(f'Cannot uniquely prove question evidence: {q["question"]}: {matches}')
  q['sourceEvidenceTurn']=matches[0]
  q['sourceReviewStatus']='publisher_page_turn_reviewed_not_audio_verified'
 full.append(x)
 linked=[i for i in linked if i['id']!=id]
 item=next(z for z in catalog if z['id']=='voa-2-22')
 item.update({'integrationStatus':'interactive_transcript_quiz','interactiveLessonId':id,'audioPlayback':'VOA MP3 linked; playback unverified',
              'transcriptImported':True,'audioBundled':False,'sourcePageReviewed':'2026-10-29','linkedQuizId':None})
 status['voaIntegratedPublisherTranscripts']=len(full)
 status['voaPublisherOnlyQuizzes']=len(linked)
 status['voaSpeakerTurnEvidenceQuestions']=sum('sourceEvidenceTurn' in q and q.get('sourceEvidenceKind')!='stage_direction' for z in full for q in z['questions'])
 status['voaStageDirectionTurnEvidenceQuestions']=sum('sourceEvidenceTurn' in q and q.get('sourceEvidenceKind')=='stage_direction' for z in full for q in z['questions'])
 status['voaTranscriptTurnEvidenceQuestions']=sum('sourceEvidenceTurn' in q for z in full for q in z['questions'])
 status['voaPublisherExcerptEvidenceQuestions']=sum('sourceEvidence' in q and 'sourceEvidenceTurn' not in q for z in linked for q in z['questions'])
 assert len(full)+len(linked)==50 and sum(len(z['questions']) for z in full+linked)==204
 for p,data in [(a,full),(b,linked),(c,catalog),(d,status)]:p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 return True
if __name__=='__main__':print('added' if apply() else 'unchanged')
