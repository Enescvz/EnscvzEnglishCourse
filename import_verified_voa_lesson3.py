#!/usr/bin/env python3
"""Import VOA Level 2 Lesson 3's publisher transcript into the local transcript UI.

The MP3 remains an external VOA URL. Nothing is described as bundled or
independently synchronized/verified. Idempotent; reuses existing quiz questions.

VOA source: https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-3/4027340.html
Source text manually compared against publisher's Conversation section on 2026-10-28.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'data/voa-source-catalog.json'
QUIZ=ROOT/'data/voa-source-quizzes.json'
AUTH=ROOT/'data/authentic-listening.json'
SOURCE='https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-3/4027340.html'
AUDIO='https://voa-audio.voanews.eu/vle/2017/09/15/078ffce1-f691-4e1e-811e-058154119d2d_hq.mp3?download=1'
# Speaker turns from VOA's public-domain Conversation section, not machine-generated audio captions.
TRANSCRIPT=[
('Anna',"Today, Pete and I are meeting with a consultant who will help us with our new show. Yesterday, Pete had promised to meet me here at 8:00 am. but he did not come on time."),
('Prof Bot',"Uh-oh. It’s bad to be late for a business meeting. But while we wait for Pete, let’s talk about a new verb tense -- past perfect! You know the past tense, right? Like, 'Pete promised to meet me here at 8:00 a.m.' Past perfect is a little different. When we talk about two things in the past, we can use the past perfect for the first event. Put 'had' before the past participle. 'Pete had promised he would meet Anna.' Here's your assignment: find sentences with the past perfect tense. Remember, look for 'had!'"),
('Kelly',"You two are late -- exactly 43 minutes late! What happened?"),
('Anna',"He had to get his 'special' coffee -- SPECIAL coffee!"),
('Pete',"She had to feed her birds -- HER birds!"),
('Kelly',"Okay, I can see already that you need my help. You can’t both talk at the same time. You have to take turns. Alright, Anna, you go first."),
('Anna',"Sure. Kelly, see, Pete and I live in the same building. So, we decided to meet at 8:00 a.m. - 8:00 a.m. to come to work together. I had waited 15 minutes when Pete arrived!"),
('Anna',"After Pete had wasted time waiting for coffee, we were late. I left you a message."),
('Kelly',"Hum. I didn’t get that message."),
('Anna',"Oh. Sorry."),
('Kelly',"Pete?"),
('Prof Bot',"Anna left a message. That’s the right thing to do. Did you find some examples of the past perfect sentences? I did. Anna said, 'After Pete had wasted time waiting for coffee, we were late.' Look at that coffee! It looks more like dessert! Okay, keep watching for past perfect!"),
('Pete',"Yeah, that’s not why we’re late. This is why we’re late: I had arrived on time at 8:00 a.m. but didn’t see Anna. She was standing behind a tree. I think she was hugging it. I always walk to work. But she said that would take too long and that a scooter would be much faster. It was awful. I hated it. And it added too much time to our commute!"),
('Pete',"Then Anna stopped by a pond to feed the birds. She had named them after characters from books and yelled the names out loud … Romeo! Juliet! Sherlock! By the time she had fed all the birds, we were late."),
('Kelly',"This is what I think. You two see the same event very differently. Does this happen often with you two?"),
('Pete',"Yes."),('Anna',"No."),('Pete',"No."),('Anna',"Yes."),
('Kelly',"Okay. This is good. This is good! It’s good to see things differently. I have an idea: we will call the show 'He Said, She Said.' For every story, you tell a different point of view."),
('Anna',"That is a great idea, Kelly! Pete, we are different. That’s why I thought of you for this job!"),
('Kelly',"I think you two understand perfectly."),
('Anna',"Let’s get to work!"),
('Kelly',"She named the birds? Really?"),('Pete',"Yeah…"),
]

def run():
 catalog=json.loads(CAT.read_text(encoding='utf-8'))
 quizzes=json.loads(QUIZ.read_text(encoding='utf-8'))
 lessons=json.loads(AUTH.read_text(encoding='utf-8'))
 source=next(x for x in catalog if x['id']=='voa-2-03')
 if source['sourceUrl']!=SOURCE:raise ValueError('Source URL mismatch; no import')
 linked=next((x for x in quizzes if x['catalogId']=='voa-2-03'),None)
 old=next((x for x in lessons if x['id'] in ('voa-level2-03-he-said-she-said','voa-linked-2-03')),None)
 if not linked and not old:raise ValueError('Must find a verified linked quiz before promoting to transcript lesson')
 questions=linked['questions'] if linked else old['questions']
 if len(questions)!=4:raise ValueError('Unexpected quiz size')
 # Source evidence is a verifiable assertion, not just a generic 'reviewed' tag.
 evidence=[
  "Anna says, 'meeting with a consultant who will help us with our new show'",
  "Kelly asks, 'You two are late -- exactly 43 minutes late!'",
  "Anna says, 'He had to get his special coffee'",
  "Pete describes the scooter commute and says Anna fed the birds",
 ]
 for q,e in zip(questions,evidence):q['sourceEvidence']=e
 lesson={
  'id':'voa-linked-2-03','title':'He Said – She Said — Different Perspectives',
  'level':'B1–B2','topic':'Work, point of view & disagreements','minutes':4.92,
  'sourceUrl':SOURCE,'audioUrl':AUDIO,
  'focus':['point of view','take turns','commute','past perfect','on time'],
  'attribution':'VOA Learning English','sourceSeries':"Let's Learn English — Level 2",
  'sourceLicense':'VOA-produced public domain educational material (third-party elements excluded)',
  'rightsUrl':'https://learningenglish.voanews.com/p/6861.html',
  'audioProvider':'VOA Learning English','audioType':'human_dialogue_source',
  'audioAvailability':'external_online_stream_only','offlineReady':False,
  'transcriptSource':'Publisher-provided VOA Conversation section',
  'transcriptVerifiedAgainstAudio':False,'timingVerified':False,
  'quality':'source_transcript_checked_audio_playback_unverified',
  'transcriptReviewedOn':'2026-10-28','turns':[{'speaker':s,'text':t} for s,t in TRANSCRIPT],
  'questions':questions,
 }
 lessons=[x for x in lessons if x['id'] not in ('voa-level2-03-he-said-she-said',lesson['id'])]+[lesson]
 quizzes=[x for x in quizzes if x['catalogId']!='voa-2-03']
 source.update({'integrationStatus':'interactive_transcript_quiz','interactiveLessonId':lesson['id'],
  'questionCount':len(questions),'transcriptImported':True,'audioPlayback':'VOA MP3 linked; playback unverified',
  'audioBundled':False,'sourcePageReviewed':'2026-10-28'})
 source.pop('linkedQuizId',None)
 for p,obj in [(AUTH,lessons),(QUIZ,quizzes),(CAT,catalog)]:p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return {'fullTranscriptLessons':len(lessons),'sourceLinkedOnly':len(quizzes),'totalQuizLessons':len(lessons)+len(quizzes),
  'newTranscriptTurns':len(TRANSCRIPT),'bundledHumanAudio':0}
if __name__=='__main__':print(json.dumps(run(),indent=2))
