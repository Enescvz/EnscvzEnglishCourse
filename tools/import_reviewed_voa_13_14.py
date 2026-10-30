#!/usr/bin/env python3
"""Import checked public-domain VOA Conversation sections, level 2 lessons 13–14.

Audio URL is a publisher-provided external MP3 URL, NOT playback verification.
Keep original lesson IDs, questions and historical learner storage keys intact.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUTH=ROOT/'data/authentic-listening.json'
LINKED=ROOT/'data/voa-source-quizzes.json'
CAT=ROOT/'data/voa-source-catalog.json'
RIGHTS='https://learningenglish.voanews.com/p/6861.html'

SOURCES={
 'voa-2-13':{
  'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-13-save-the-bees/4145716.html',
  'audioUrl':'https://voa-audio.voanews.eu/vle/2017/12/01/104a6627-290a-4472-911e-3bb9349f44f7_hq.mp3?download=1',
  'title':'Save the Bees! — Keeping Bees Safe','minutes':3.85,
  'topic':'Environment, beekeeping and conditional sentences',
  'focus':['smoker','queen bee','worker bee','nectar','native flowers'],
  'evidence':[
   ('Caroline','If I use a smoker, the bees will stay calm.'),
   ('Caroline','The queen bee lays the eggs.'),
   ('Caroline','The worker bees collect nectar and pollen'),
   ('Caroline','You can plant native flowers that bees like.'),
  ],
  'turns':[
   ('Prof. Bot', 'We are back with Anna and Caroline and the bees. Last time, Anna was afraid. (Anna: I\'m not afraid of bees!) But Caroline is helping her to stay safe. Look at sentences that start with "If" to find more conditional sentences. Remember, Type 1 conditionals use the present tense and "will," and Type 2 use the past tense and "would." Now, let\'s find out what happens with Anna and the bees.'),
   ('Caroline', 'I have a feeling that your fear of bees will be gone soon. There are things beekeepers do to protect ourselves. For example, we wear protective clothing. This is a beekeeper’s veil, suit and gloves. There are other things we can do, too. If I use a smoker, the bees will stay calm.'),
   ('Anna', 'Let’s use smoke … lots of smoke.'),
   ('Caroline', 'Okay, Anna, that’s enough smoke. Another thing you can do is stay calm. Okay. When I lift the frame, you will see the bees.'),
   ('Anna', 'I’m ready. Let\'s do this thing!'),
   ('Caroline', 'Okay, let\'s put on our protective clothing.'),
   ('Caroline', 'I will carefully take out a frame. This is where the bees live. There are worker bees, drone bees and the queen bee. The bees have different jobs. The queen bee lays the eggs. The worker bees collect nectar and pollen from flowers and bring it back to the hive. Then they make honey! Now, you hold the frame. There are the bees.'),
   ('Anna', 'There are so many! And they are so busy! Now I know why we say, “busy as a bee!”'),
   ('Caroline', 'Good job, Anna.'),
   ('Anna', 'Caroline, bees are beautiful and important. If I wanted to help the bees, what would I do?'),
   ('Caroline', 'Great question. You can plant native flowers that bees like. Here’s a book to help you know which ones to plant.'),
   ('Anna', 'It’s a beautiful book. And look, it tells you which bees like which types of flowers.'),
   ('Caroline', 'It also tells you how the flowers affect the flavor of the honey.'),
   ('Anna', 'Flowers make a big difference to bees. If they don’t eat, they won’t live.'),
   ('Caroline', 'Buying local honey also helps the bees. If you want to help bees, do those two things.'),
   ('Prof. Bot', 'I learned a lot about bees. Hey, if I worked with bees, I would not need protective clothing! Guess what? That was a Type 2 conditional. And I heard a Type 1 conditional, too. (Anna: If they don’t eat, they won’t live.)'),
   ('Anna', 'Thanks for the book, Caroline, and the bee puppet and for teaching me about bees. Look … I’m not scared.'),
   ('Caroline', 'Good job, Anna. If you ever want to see the bees again, I’ll be here! You have my business card. I\'ll let you see yourself out.'),
   ('Anna', 'Thanks! Bye! I will plant tons of flowers!'),
   ('Bees', 'Thanks, Anna. (bees spell out the words)'),
   ('Anna', 'Sure thing, bees! Oh, and I\'m sorry about hitting that hive when I was a little girl.'),
   ('Bees', 'We love you, Anna. (bees make a heart sign.)'),
   ('Anna', 'Take care, bees! (to herself) Which way is the Metro?'),
   ('Bees', 'That way. (they draw an arrow)'),
   ('Anna', 'Thanks!'),
   ('Prof. Bot', 'So, if I you want to learn more about bees, visit your local beekeeper like Anna did. Maybe you can try some local honey, too. Now it’s your turn. Practice making conditional sentences. If you practice, you will become better at them. That\'s type 1!'),
  ],
 },
 'voa-2-14':{
  'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-14-made-for-each-other/4159000.html',
  'audioUrl':'https://voa-audio.voanews.eu/vle/2017/12/12/e2fe076d-3fa7-495a-83ea-9d4d4cba9fad_hq.mp3?download=1',
  'title':'Made for Each Other — Similarities and Relationships','minutes':4.60,
  'topic':'Relationships, connectors and agreement',
  'focus':['have in common','made for each other','either','so do I','squirrel collection'],
  'evidence':[
   ('Pete','She can’t whistle and I can’t either.'),
   ('Pete','You know, she made all that up.'),
   ('Anna','It’s just Buster Carter, Ashley.'),
   ('Anna','squirrel collection. Bye, guys! Gotta go!'),
  ],
  'turns':[
   ('Anna','Hello! What are you guys looking at?'),
   ('Pete','I’m showing Ashley pictures of my girlfriend. We have so much in common -- even small things. She can’t whistle and I can’t either.'),
   ('Ashley','(to Pete) And here’s a picture of my boyfriend. (sighs)'),
   ('Ashley','My family is big and so is his. I don’t like ball sports and he doesn’t either! (sighs) We are made for each other ...'),
   ('Pete','… and so are we. (sighs)'),
   ('Anna','Uh… you have found perfect partners … and so have I!'),
   ('Professor Bot','Pete and Ashley are talking about people they love. They are putting two ideas together with connectors. Let’s start with these two sentences: She can’t whistle. Pete can’t whistle. How do you put them together? Pete says, "She can’t whistle and I can’t either." You can see we just add the conjunction “either” and take away the verb “whistle.” And Ashley says: "I don’t like ball sports and he doesn’t either!" Keep looking for connectors!'),
   ('Ashley','You met someone, Anna? That’s great! What’s his name?'),
   ('Anna','His name? His name is uh… (stalling, looks around, sees a bus) Bus … ter. (stalling, looks around, sees a car) Car … ter.'),
   ('Ashley','(says it like Anna did) Bus...ter Car...ter?'),
   ('Anna','It’s just Buster Carter, Ashley. I like him and he likes me. We’re a great couple.'),
   ('Ashley','Hey, let’s all get dinner tonight, together. You can bring Buster.'),
   ('Pete','(laughing) Yeah, I can’t wait to meet him.'),
   ('Anna','Thanks, Ashley, but he’s really busy tonight with his uh, (looks around, sees squirrel) squirrel collection. Bye, guys! Gotta go!'),
   ('Ashley','Squirrel collection?'),
   ('Pete','You know, she made all that up.'),
   ('Ashley','That’s so sad. She needs to meet someone. Hey, do you know anyone who she might...'),
   ('Pete','No.'),
   ('Anna','(to herself) Anna, Anna, you lied! You lied! Now, they think you have a boyfriend - with a squirrel collection. Here, squirrel. (throws food) Well, you need to tell them the truth. You don’t have a boyfriend.'),
   ('Man','Excuse me, is this seat taken?'),
   ('Anna','Ashley, Pete, I need to talk to you. This morning, I lied.'),
   ('Pete','Let me guess. There’s no Buster Carter. What a surprise!'),
   ('Anna','I’m sorry. But later I really did meet someone and we have a lot in common! He’s good at flying kites and so am I. He likes to read comics and so do I. I can play the ukulele and so can he.'),
   ('Ashley','He sounds perfect for you, Anna. Can he come tonight?'),
   ('Anna','That’s the sad part. You see, he just got a job as a spy, and tonight he leaves on assignment.'),
   ('Pete','Of course he does.'),
   ('Anna','But that\'s okay, because now I know that there is someone out there made for me. (looks at the time) Oh, it’s late! I have to see him off at the train station. Bye, you guys!'),
   ('Ashley','Bye Anna! Oh dear, she’s worse than we thought.'),
   ('Pete','She’s lost her mind.'),
   ('Ashley','What should we do?'),
   ('Pete','(happy, excited) Let’s tell her!'),
   ('Ashley','No, Pete. Mr. Right may not be real but he makes her really happy.'),
   ('Professor Bot','Did you find any other connectors? Notice how the words are in a different order in the part after “so.” "I am" becomes "am I" and "he can" becomes "can he." "He’s good at flying kites and so am I. I can play the ukulele and so can he."'),
  ],
 },
}


def run():
    auth=json.loads(AUTH.read_text(encoding='utf-8'))
    linked=json.loads(LINKED.read_text(encoding='utf-8'))
    catalog=json.loads(CAT.read_text(encoding='utf-8'))
    original_ids={x['id'] for x in auth+linked}
    original_quiz_ids=[(x['id'],[q['question'] for q in x['questions']]) for x in auth+linked]
    for cid,src in SOURCES.items():
        cat=next(x for x in catalog if x['id']==cid)
        if cat['sourceUrl']!=src['sourceUrl']:raise ValueError('Source mismatch '+cid)
        existing=next((x for x in auth if x['id']=='voa-linked-'+cid.split('-',1)[-1]),None)
        old=next((x for x in linked if x['catalogId']==cid),None)
        if existing is not None:
            if old is not None:raise ValueError('Duplicate integrated and linked lesson '+cid)
            continue
        if not old:raise ValueError('Expected publisher-linked quiz '+cid)
        if len(src['turns'])<20 or len(old['questions'])!=4:raise ValueError('Incomplete lesson '+cid)
        turns=[{'speaker':speaker,'text':text} for speaker,text in src['turns']]
        for question,(speaker,quote) in zip(old['questions'],src['evidence']):
            matches=[i for i,t in enumerate(turns) if t['speaker']==speaker and quote in t['text']]
            if len(matches)!=1:raise ValueError('Evidence absent or ambiguous '+cid+' '+quote)
            if not 0<=question['answer']<len(question['options']):raise ValueError('Invalid answer '+cid)
            question.update({'sourceEvidence':quote,'sourceEvidenceTurn':matches[0],
                             'sourceEvidenceSpeaker':speaker})
        auth.append({'id':old['id'],'title':src['title'],'level':old['level'],
            'topic':src['topic'],'minutes':src['minutes'],'sourceUrl':src['sourceUrl'],
            'audioUrl':src['audioUrl'],'focus':src['focus'],'attribution':'VOA Learning English',
            'sourceSeries':"Let's Learn English — Level 2",
            'sourceLicense':'VOA original public-domain materials; attributed; excludes third parties',
            'rightsUrl':RIGHTS,'audioProvider':'VOA Learning English',
            'audioType':'human_dialogue_source','audioAvailability':'external_online_stream_only',
            'offlineReady':False,'transcriptSource':'Publisher-provided VOA Conversation section',
            'transcriptVerifiedAgainstAudio':False,'timingVerified':False,
            'quality':'publisher_transcript_checked_audio_playback_unverified',
            'transcriptReviewedOn':'2026-10-28','turns':turns,'questions':old['questions']})
        linked=[x for x in linked if x['catalogId']!=cid]
        cat.update({'integrationStatus':'interactive_transcript_quiz','interactiveLessonId':old['id'],
                    'transcriptImported':True,'questionCount':len(old['questions']),
                    'audioBundled':False,'audioPlayback':'VOA MP3 direct link (unverified)',
                    'sourcePageReviewed':'2026-10-28'})
        cat.pop('linkedQuizId',None)
    if {x['id'] for x in auth+linked}!=original_ids:raise ValueError('Lesson IDs changed')
    if len(auth)+len(linked)!=50 or len(auth)<14:raise ValueError('Lesson count wrong')
    if sum(len(x['questions']) for x in auth+linked)!=204:raise ValueError('Quiz count changed')
    if sorted((x['id'],[q['question'] for q in x['questions']]) for x in auth+linked)!=sorted(original_quiz_ids):
        raise ValueError('Quiz texts changed')
    for path,content in [(AUTH,auth),(LINKED,linked),(CAT,catalog)]:
        path.write_text(json.dumps(content,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return {'integrated':len(auth),'linked':len(linked),'questions':204,
            'evidence':sum('sourceEvidenceTurn' in q for l in auth for q in l['questions']),
            'audioVerifiedOnIphone':False,'releaseApproved':False}

if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
