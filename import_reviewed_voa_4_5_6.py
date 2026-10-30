#!/usr/bin/env python3
"""Promote two VOA Level 2 publisher transcripts to in-app listening lessons.

Publisher originals from Voice of America, with sources linked below. Scripts were
checked against the publicly displayed 'Conversation' sections on 2026-10-28.
This does *not* assert audio playback, timing or independent editorial approval.
Idempotent: card and quiz IDs are preserved.
"""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'data/voa-source-catalog.json'
QUIZ=ROOT/'data/voa-source-quizzes.json'
AUTH=ROOT/'data/authentic-listening.json'

# Each line beginning with 'Speaker:' is a new turn; other lines continue that
# speaker's utterance. Text is from VOA's own course pages, not invented speech.
SOURCES={
 'voa-2-04':{
  'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-4-run-away-with-the-circus/4034187.html',
  'audioUrl':'https://voa-audio.voanews.eu/vle/2017/09/19/56dbc988-a70f-4417-8668-c3916f6b73e7_hq.mp3?download=1',
  'title':'Run Away With the Circus! — Agreeing and Disagreeing','minutes':5.02,
  'focus':['I completely disagree','I see your point','trapeze artist','athletic','back and forth'],
  'topic':'Agreeing, disagreeing and seeing both sides',
  'evidence':[
   'Pete: Circus? That’s not an art form.',
   'I think they’re athletes with interesting skills … and costumes.',
   'They are athletic. But they are called trapeze artists.',
   'No, but we can agree that these young people are amazing.',
  ],
  'transcript':'''Anna: Hello, I’m Anna …
Pete: … and I’m Pete. Welcome to “He Said,
Anna: … She Said”!
Pete: Because there are always two sides …
Anna: to every story!
Anna: Today’s show is about Circus Arts!
Pete: Circus? That’s not an art form.
Anna: Yes, it is.
Pete: No, it isn't.
Anna: Yes, it is.
Pete: No, it isn't.
Anna: Yes, it is!
Pete: No, it isn't.
Anna: Yes, it is!
Pete: No, it isn't.
Anna: Yes, it is!
Pete: No, it isn't.
Professor Bot: Oh dear. Anna and Pete do not agree about Circus Arts. But that's okay. Today’s lesson is about agreeing and disagreeing. Let’s listen to how Anna and Pete disagree or agree. Let’s hope these two can agree on something.
Anna: Today, let’s run away with the circus!
Recently, I went to a circus festival. There was a huge circus tent. And many different circus performers. It was a celebration of circus arts!
Pete: That looks fun, Anna. But I don’t think circus performers are artists. I think they’re athletes with interesting skills … and costumes.
Anna: Hmm, that is a very interesting point of view, Pete. And I completely disagree.
Pete: Anna, Michelangelo was an artist. Rembrandt was an artist. People who swing from ropes are not artists. I know it’s not easy to swing from a bar and catch someone by the hands. You have to be very athletic to do that.
Anna: That’s a good point, Pete. They are athletic. But they are called trapeze artists. Trapeze … ARTISTS.
Pete: I hear what you’re saying, Anna. I do. But where is the art? Look at these guys. They’re jugglers.
Anna: Yes, they are skilled in the art of juggling.
Pete: They have a special skill. But are they artists?
Anna: Yes!
Pete: No!
Pete: They're just throwing things back and forth.
Anna: Kind of like you and me, Pete. We’re going back and forth on this issue.
Pete: I don’t think we’ll ever agree on this one.
Anna: No, but we can agree that these young people are amazing.
Pete: Okay, yeah. We can agree on that. But, still, they are very athletic – flipping and throwing each other around.
Anna: Yes, I agree with you on that point.
Professor Bot: They did it! They agreed!! Anna says she agrees that the performers are athletic. "That’s a good point, Pete. They are athletic. I agree with you on that point." Now look for other ways they agree.
Pete: Anna? Anna!!
Anna: Sorry! Sorry! But he’s an artist too. He is telling a story with his sticks and his costume.
Pete: What story? What costume?
Anna: I see your point, Pete. I really do. But circus performers do more than physical tricks. Look! Look at these amazing performers!
Pete: I will admit -- I like their costumes.
Anna: You know, Pete. Let’s let the performers speak for themselves.
Anna: Kate and Piper tell stories while hanging upside down on a ring!
Pete: Was it hard to interview them upside down?
Anna: I interviewed them right side up, Pete. Kate says circus performing may be athletic but it’s not competitive. With most sports, you compete.
Kate: It’s an art form because like, other sports are competing. This is simply performing and having fun.
Pete: Okay, Kate made a really good point. In athletics, there is a lot of competition. But still …
Anna: Here’s Piper, Pete. Please pay attention, Pete.
Pete: But, I -
Anna: Shh.
Piper: Well, when you’re up in the air doing circus you have to perform. And so, we learn to embody characters, and to move fluidly and gracefully … in artistic ways.
Anna: And that …is why they are artists!
Pete: You’re right, Anna. Oh, you’re right. It’s just so beautiful.
Anna: I know. I know, Pete.
Professor Bot: Good job you two! I'm so glad that Anna and Pete finally agree! Pete said, "You’re right, Anna." I agree, too. Circus arts are beautiful. Remember the website!''',
 },
 'voa-2-05':{
  'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-5-greatest-vacation/4035571.html',
  'audioUrl':'https://voa-audio.voanews.eu/vle/2017/09/27/11289bfa-a821-47fb-905b-7b4174ae0c5e_hq.mp3?download=1',
  'title':'Greatest Vacation of All Time — Travel Choices','minutes':4.83,
  'focus':['getaway','priciest','afraid of heights','under the stars','scariest'],
  'topic':'Travel, preferences and making comparisons',
  'evidence':[
   'A beach is much better than here. I need a vacation!',
   'Anna: I’m afraid of high places.',
   'That’s why our Deep Sea Adventure is better for you!',
   'At night, you’ll sleep out under the stars.',
  ],
  'transcript':'''Anna: “Do you need a vacation?” Wow. That was the best vacation I have ever had … in my head. A beach is much better than here. I need a vacation!
Professor Bot: I hear you, Anna. I need a vacation too but not at the beach. Sand is not good for robots! When we compare things, we use special forms of adjectives. "Better" is a comparative adjective. That is used to compare two things. "Best" is a superlative adjective. It shows that one thing has more of ...something than ALL of the others. Try to find more of these adjectives. Look for ER or EST at the end.
Dan: NO! You can’t get your money back. I don’t care that it was your worst vacation ever!
Dan: Hello! Have a seat! Welcome to the World’s Best Vacation Travel Agency!
Anna: Thank you and congratulations!
Dan: For what?
Anna: For being the world’s best travel agency.
Dan: Right … thanks.
Dan: Trudy, hold my calls. I am going to sell our most expensive vacation.
Trudy: Sure thing, Boss.
Dan: The Mountain Getaway is good for you. It’s a little pricey. But think of it -- you, on top of a mountain for seven days!
Anna: I’m afraid of high places.
Dan: Of course you are. That’s why our Deep Sea Adventure is better for you! It is pricier than the Mountain Getaway. Just you and the animals of the sea!
Anna: Shark! Shark!
Dan: No, there are no sharks in your dream vacation! You need the Safari Camp Out! It is our priciest vacation. But I think it’s the best one for you. During the day, you’ll see elephants, giraffes and lions. At night, you’ll sleep out under the stars.
Anna: Look, I think this was a bad idea.
Dan: Sure, you can leave. But then you won’t see the latest vacation technology.
Professor Bot: Did you find all of those adjectives? Dan started with good - The mountain getaway; then he moved to better - The Deep Sea Adventure. And finally, he said the Safari Campout was the best vacation for Anna!
Anna: Exactly what is the “latest vacation technology” … exactly?
Dan: I’m happy you asked. Meet the Travel Max 2000!
Anna: Wow.
Dan: So, tell me, how do you like to travel?
Anna: Well, I like travel that is cozy and romantic but still exciting.
Dan: Great. Tell me more.
Anna: I like traveling in a plane but not in a helicopter! Planes are a little scary but helicopters are scarier! My favorite way of traveling is by train. Ships can be the scariest! Have you seen the movie “Titanic”? Oh, and no horses. But I will ride a camel. And no bike tours. Biking is THE slowest AND least romantic way to travel. Excuse me, but I think the Travel Max 2000 is on fire.
Dan: Yes, we’re both on fire! We really want to sell you the most ex-, I mean, best vacation ever!
Anna: No, I mean it’s really on fire!
Dan: You killed it. You killed the Travel Max 2000!
Anna: I am so sorry! Can I help you fix it?
Dan: No, no!
Anna: Don’t cry. I know what you need -- a vacation!
Anna: The Safari Campout looks fun. It is the priciest. But I think you deserve it.
Dan: No, no!
Professor Bot: Oh Anna. This is the smokiest lesson yet! There were a lot of comparatives and superlatives but … I can’t breathe. Just go to the website to learn the best ways to use them!''',
 },
}

SOURCES['voa-2-06']={
 'sourceUrl':'https://learningenglish.voanews.com/a/lesson-6-will-it-float/4064553.html',
 'audioUrl':'https://voa-audio.voanews.eu/vle/2017/10/10/4814fa95-feaa-447a-a081-499d11b1d5f3_hq.mp3?download=1',
 'title':'Will It Float? — Touring Washington, DC',
 'minutes':4.73,
 'topic':'Travel directions, landmarks and place prepositions',
 'focus':['take a tour','get aboard','along the river','on the left','give a tip'],
 'evidence':[
  'You are new to town. And a tour is the best way to see more of the city!',
  'We will ride on the road and then sail on the water!',
  'created during World War II to carry people and supplies',
  'the Washington Monument is on the left!',
 ],
 'transcript':'''Penelope: Anna, thanks for taking me on a tour of D.C. today.
Anna: Sure thing, Penelope. You are new to town. And a tour is the best way to see more of the city!
Penelope: So, which tour are we taking – the one that goes through the city on a bus? Or the one that goes along the river in a boat?
Anna: Both!
Penelope: What? Anna, this isn’t going to be one of those trips, is it?
Anna: No. Follow me.
Professor Bot: In this lesson, you are going to hear lots of prepositions! What’s a preposition, you ask? It’s a word that shows relationships between things. Anna says they are going on a tour through the city and along the river. Through and along are both prepositions. Watch for more!
Anna: Well, Penelope, there’s our ride!
Penelope: What is it?
Anna: It’s the famous DC Ducks -- the boat with wheels! We will ride on the road and then sail on the water!
Penelope: Who thinks of these things?
Anna: I don't know. But I’m glad they do! Let’s get aboard, Sailor!
Penelope: (looking at a brochure about the boat) Hey, did you know that this bus … um, boat was created during World War II to carry people and supplies?
Anna: Wow. You know, a tour is so much more interesting with Fun Facts, like that one.
Penelope: I agree. I love Fun Facts!
Boy: Did I hear you say you love Fun Facts?
Anna & Penelope: Yeah.
Boy: Well, I have tons of Fun Facts for this tour!
Anna & Penelope: Great!
Anna: Penelope, where are his parents?
Penelope: Maybe - maybe he’s the Captain’s son and he helps his dad on tours!
Anna: Oh yeah! It would be so awesome to ride around the city in a boat all day with your dad!
Penelope: This is amazing, Anna. There are so many beautiful buildings along this road!
Anna: Hey, the Washington Monument is on the left!
Professor Bot: I have a Fun Fact too! Did you know that the Washington Monument was damaged in an earthquake? Whoa. Did you feel that?! I heard: "around the city in a boat," "along this road" and "on the left." All of these are prepositions showing place. Let's watch for more places and prepositions!
Penelope: Look, Anna, we’re across from the White House!
Anna: Penelope, the only thing between us and the President is the street … and a park … and a security gate .... and police officers … with guns.
Boy: Excuse me, do you want to know a Fun Fact about the White House?
Anna & Penelope: Yes!
Boy: Inside the White House there is a swimming pool, a movie theater and 32 bathrooms!
Penelope: Thirty-two bathrooms! That’s a lot of bathrooms!
Boy: I’d be happy with two. I live in a house with my mom, four sisters, two aunts and only one bathroom!
Penelope: Oh my! You know, Anna, we should give him a tip!
Anna: Of course! It is polite to tip your tour guide! Luckily, I have lots of dollar bills!
Penelope: That was a great Fun Fact! Here you go!
Boy: Thank you! I can tell you Fun Facts all day!
Professor Bot: Did you hear any more prepositions of place? I heard "between us and the president" “inside the White House” and "in a house." And did you hear that the Duck Boat can go on the river? I don't believe it. Join us next time to find out which preposition we will use: The boat went ON the river or The boat went INTO the river?''',
}

def parse_turns(txt):
 turns=[]
 for raw in txt.splitlines():
  row=raw.strip()
  if not row:continue
  m=re.match(r'^([A-Za-z][A-Za-z &.]{0,35}):\s*(.+)$',row)
  if m:
   turns.append({'speaker':m.group(1),'text':m.group(2)})
  elif turns:
   turns[-1]['text']+=' '+row
  else:raise ValueError('Orphan transcript line')
 return turns

def run():
 catalog=json.loads(CAT.read_text(encoding='utf-8'))
 linked=json.loads(QUIZ.read_text(encoding='utf-8'))
 lessons=json.loads(AUTH.read_text(encoding='utf-8'))
 for cid,entry in SOURCES.items():
  cat=next(x for x in catalog if x['id']==cid)
  if cat['sourceUrl']!=entry['sourceUrl']:raise ValueError('Publisher URL changed for '+cid)
  old_quiz=next((x for x in linked if x['catalogId']==cid),None)
  if not old_quiz: # Idempotency: already promoted.
   old=next((x for x in lessons if x['id']=='voa-linked-'+cid.split('-',1)[-1]),None)
   if not old:raise ValueError('No quiz to promote for '+cid)
   continue
  questions=old_quiz['questions']
  if len(questions)!=len(entry['evidence']):raise ValueError('Question/evidence mismatch')
  turns=parse_turns(entry['transcript'])
  if len(turns)<20:raise ValueError('Too short to qualify as a full transcript')
  normalized=' '.join((t['speaker']+': '+t['text']) for t in turns)
  for q,evidence in zip(questions,entry['evidence']):
   evidence_text=evidence.split(': ',1)[1] if re.match(r'^[A-Za-z ]+: ',evidence) else evidence
   hit=next(((i,t) for i,t in enumerate(turns) if evidence_text in t['text']),None)
   if hit is None:raise ValueError('Evidence not in any single transcript turn: '+evidence)
   if not (0<=q['answer']<len(q['options'])):raise ValueError('Invalid answer index')
   q['sourceEvidence']=evidence_text
   q['sourceEvidenceTurn']=hit[0]
   q['sourceEvidenceSpeaker']=hit[1]['speaker']
  item={
   'id':old_quiz['id'],'title':entry['title'],
   'level':old_quiz['level'],'topic':entry['topic'],'minutes':entry['minutes'],
   'sourceUrl':entry['sourceUrl'],'audioUrl':entry['audioUrl'],
   'focus':entry['focus'],'attribution':'VOA Learning English',
   'sourceSeries':"Let's Learn English — Level 2",
   'sourceLicense':'VOA original public domain educational material; third-party content excluded',
   'rightsUrl':cat['rightsUrl'],
   'audioProvider':'VOA Learning English','audioType':'human_dialogue_source',
   'audioAvailability':'external_online_stream_only','offlineReady':False,
   'transcriptSource':'Publisher-provided VOA Conversation section',
   'transcriptVerifiedAgainstAudio':False,'timingVerified':False,
   'quality':'publisher_transcript_checked_audio_playback_unverified',
   'transcriptReviewedOn':'2026-10-28','turns':turns,'questions':questions,
  }
  lessons.append(item)
  linked=[x for x in linked if x['catalogId']!=cid]
  cat.update({'integrationStatus':'interactive_transcript_quiz',
              'interactiveLessonId':old_quiz['id'],'transcriptImported':True,
              'questionCount':len(questions),'audioBundled':False,
              'audioPlayback':'VOA MP3 linked; playback unverified',
              'sourcePageReviewed':'2026-10-28'})
  cat.pop('linkedQuizId',None)
 # Fail if duplicates before writing.
 ids=[x['id'] for x in lessons]+[x['id'] for x in linked]
 if len(ids)!=len(set(ids)):raise ValueError('Duplicate lesson ID')
 for path,payload in ((AUTH,lessons),(QUIZ,linked),(CAT,catalog)):
  path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 return {'transcriptsInApp':len(lessons),'publisherLinkedOnly':len(linked),
         'questionSets':len(lessons)+len(linked),
         'allQuestions':sum(len(x['questions']) for x in lessons+linked),
         'externalAudioPlaybackVerified':0,'releaseApproved':False}

if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
