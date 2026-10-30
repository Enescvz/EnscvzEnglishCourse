#!/usr/bin/env python3
"""Source-reviewed VOA Level 2 lessons 11–12 (private development only).

Exact Conversation text reviewed against VOA publisher HTML views 2026-10-28.
Does not claim device playback, audio alignment, offline readiness, or editorial QA.
Idempotent; stable quiz and lesson IDs are retained without changing learning records.
"""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AUTH=ROOT/'data/authentic-listening.json'
LINKED=ROOT/'data/voa-source-quizzes.json'
CAT=ROOT/'data/voa-source-catalog.json'

SOURCES={
 'voa-2-11': {
  'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-11-the-big-snow/4102755.html',
  'audioUrl':'https://voa-audio.voanews.eu/vle/2017/11/21/0117495a-4165-48c3-8972-61491413ad7a_hq.mp3?download=1',
  'title':'The Big Snow — Weather and Emergencies',
  'minutes':4.45,
  'topic':'Weather reports, emergency supplies, past and present perfect',
  'focus':['blizzard','weather forecast','emergency supplies','wind speed','run out of'],
  'evidence':[
   ('Anna','I’ve reported on a blizzard.'),
   ('Anna','I volunteered Pete to help me.'),
   ('Anna','my supplies – food, a blanket; warm clothing.'),
   ('Anna','It will give us the temperature, wind speed, wind direction and amount of snowfall … in real time!'),
  ],
  'transcript':'''Kelly: Hi, Anna. Why do you have all this weather stuff?
Anna: I love weather.
Kelly: Me too! Weather is so important.
Anna: It is. It affects people’s lives!
Kelly: Have you ever reported on a big weather event?
Anna: I have. I’ve reported on a blizzard.
Kelly: Do mean the one last weekend?
Anna: Yes! I had been waiting for that blizzard for years. When it came, I was ready.
Prof. Bot: Welcome to our most perfect lesson! Why is it perfect? Today we are reviewing the present perfect and past perfect verb tenses. These show that an action is completed. Kelly uses the present perfect when she says,
Kelly: Have you ever reported on a big weather event?
Prof. Bot: Anna uses the past perfect when she says,
Anna: I had been waiting for that blizzard for years.
Prof. Bot: Listen for "have" or "had" and the past participle to find more sentences with the perfect tense. I'll color those words to help you.
Anna: I have wanted to report on a big weather event my whole life.
Kelly: Who hasn’t? Did you report all weekend ... by yourself?
Anna: No, no. I volunteered Pete to help me.
Pete: Why am I here on a Saturday? Why are you carrying things? Why? Why?
Anna: Pete, these are my supplies – food, a blanket; warm clothing. Where are your supplies?
Anna: Pete, Pete, Pete. This could be the “blizzard of the century.”
Pete: It’ll be fine.
Kelly: How else had you prepared?
Anna: Well, I had just bought the latest weather forecasting software. So, I brought it!
Kelly: Do you mean The Weather Genie Pro?
Anna: You know it. Pete thought it was pretty great too.
Pete: Do you have any games on that thing?
Anna: Yes! I have the best weather survival game. Boom!~~ ~~
Pete: Sounds fun.
Anna: It is. But right now, Pete, this computer is a work tool. It will give us the temperature, wind speed, wind direction and amount of snowfall … in real time! Boom, boom!
Pete: I can’t wait.
Anna: Pete, we need a name for this blizzard.
Pete: No, we don’t.
Anna: All the great storms have names.
Pete: No, they don’t.
Anna: I know -- “The Big Snow!”
Pete: I am not saying “The Big Snow.”
Pete: Welcome to “The Big Snow.”
Kelly: The Big Snow broke all kinds of records, didn’t it?
Anna: Yes it did. And every time a record was broken, we celebrated!
Anna: So far, in Washington, D.C. 29 inches of snow has fallen. That, my dear listeners, is a record! (Honks horn)
Anna: We just broke the wind speed record! (Honks horn)
Anna: Snow has been falling for 30 hours straight! That’s another record! (Honks horn. Pete comes into room and breaks the horn.)
Kelly: By Saturday night, stores and restaurants had closed. Did you bring enough food?
Anna: I thought I had brought enough food. But I ran out.
Anna: Hey, Pete, where is my bag of popcorn?
Pete: Maybe you ate it already.
Anna: No, I didn’t.
Pete: I haven't seen it. (Pete has popcorn in his beard. Anna tries to hit him.)
Anna: We had reported together for 48 hours straight!
Kelly: Wow. That must have been a great team-building exercise for you and Pete.
Anna: Yeah. You - you could say that.
Prof. Bot: I hope you found all the sentences with perfect tenses. Learn more on our website!'''
 },
 'voa-2-12': {
  'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-12-run-bees/4139015.html',
  'audioUrl':'https://voa-audio.voanews.eu/vle/2017/11/28/260c25bd-1773-42d0-8b8a-54924d27427c_hq.mp3?download=1',
  'title':'Run! Bees! — Bees and Conditionals',
  'minutes':4.3,
  'topic':'Nature, beekeeping and conditional sentences',
  'focus':['beekeeper','swat','sting','beehive','stay calm'],
  'evidence':[
   ('Kaveh','if you ignore it, it will fly away.'),
   ('Kaveh','if you swat it, it might sting you.'),
   ('Kaveh','you should call my friend, Caroline.'),
   ('Caroline','About thirty thousand (30,000) in each.'),
  ],
  'transcript':'''Anna: Wow. Did you know that bees are dying?
Kaveh: That is bad news. If all the bees died, there would be no food. Bees are very important.
Anna: Yes, they are. Speaking of bees, one of our little friends is here now.
Kaveh: You know, Anna, if you ignore it, it will fly away. But if you swat it, it might sting you.
Anna: I’ll ignore it. I can ignore it. See, I’m ignoring it. (she is swatting at the bee)
Kaveh: Anna, are you afraid of bees?
Anna: What makes you say that?
Kaveh: Anna, you should call my friend, Caroline. She is a beekeeper and a bee educator. If you talk to her, she’ll probably help you get over your fear of bees.
Anna: I am not afraid of bees.
Kaveh: Here’s her card.
Anna: Ahhh!
Prof. Bot: In this lesson, you can learn about conditionals. They have "if" and "will" or "would." There are two kinds of conditional sentences in this lesson. Type 1 conditionals have a real event, and a result that probably will happen. Chances are good. Here is the pattern: If +present tense verb ... will + future tense verb. Kaveh uses this when he says: "If you ignore it, it will fly away." Type 2 conditionals have a possible event and a result that may or may not happen. We don't know. Here is the pattern: If + past tense verb ...would + infinitive verb. Kaveh uses this pattern when he says, "If all the bees died, there would be no food." Look for the "if" in a sentence to find more conditionals in today's lesson. I'll color them, too!
Anna: I think I'm at the wrong address. This does not look like a place where bees are kept. ​(knocks on door)
Anna: Oh, sorry to bother you. I’m looking for beekeeper Caroline. I’m here to take her “Learn to Love Bees!” class.
Caroline: You’re in the right place! I’m Caroline!
Anna: Oh, nice to meet you! Um, Caroline, I thought this class used real bees and real hives.
Caroline: It does! If you look in my backyard, you will see my bees! I’m a home beekeeper!
Anna: What? You live with bees? That is really amazing! And at the same time really scary.
Caroline: It’s not scary. If you come, I’ll show you.
Anna: Caroline, how many bees are in that hive?
Caroline: About thirty thousand (30,000) in each.
Anna: What? That's amazing! But, aren’t you afraid that they are gonna come out and kill you?
Caroline: No, not at all, Anna. Even my children help me. Tell me, why are you afraid of bees?
Anna: I don't know. Well, when I was a little girl my mom ran out of honey. And I really wanted honey for my pancakes. So, I climbed high into a tree and hit a beehive with a stick … several times. Then I reached inside with my bare hands to pull the honey out. That’s when I got stung … a lot.
Anna: Caroline, if you hit a beehive with a stick and reach inside, you might get stung.
Caroline: No, Anna. If you do those things, you will get stung.
Anna: Yes. I did.
Caroline: And you know that it was your fault you got stung, don’t you?
Anna: Yes. I did.
Caroline: Bees know your feelings. And if you stay calm, the bees will be calm. If you're nervous, the bees will be nervous. And if bees are nervous, they may sting. So, please be calm.
Anna: I will be calm. I am calm. Okay, I'm ready. I'm ready
Caroline: Great. Let’s get our equipment on.
Anna: Wait! Wait! I’m not ready! I'm nervous! Give me a minute to be calm.
Prof. Bot: Are you ready for one more conditional sentence? If you are not afraid, you will join us next time to learn more about bees!'''
 }
}

def parse_turns(text):
    turns=[]
    for line in text.splitlines():
        m=re.fullmatch(r'([^:]{2,45}):\s*(.+)',line.strip())
        if not m:raise ValueError('Unstructured VOA transcript: '+line[:80])
        turns.append({'speaker':m.group(1).strip(),'text':m.group(2).strip()})
    return turns

def run():
    auth=json.loads(AUTH.read_text(encoding='utf-8'))
    linked=json.loads(LINKED.read_text(encoding='utf-8'))
    catalog=json.loads(CAT.read_text(encoding='utf-8'))
    for cid, source in SOURCES.items():
        cat=next(x for x in catalog if x['id']==cid)
        if cat['sourceUrl']!=source['sourceUrl']:
            raise ValueError('Source URL mismatch: '+cid)
        old=next((x for x in linked if x['catalogId']==cid),None)
        lesson_id='voa-linked-'+cid.split('-',1)[-1]
        if old is None:
            existing=next((x for x in auth if x['id']==lesson_id),None)
            if not existing:raise ValueError('Original quiz ID missing: '+cid)
            continue
        turns=parse_turns(source['transcript'])
        if len(turns)<30 or len(old['questions'])!=4 or len(source['evidence'])!=4:
            raise ValueError('Transcript/quiz incomplete: '+cid)
        for q,(speaker,phrase) in zip(old['questions'],source['evidence']):
            matches=[i for i,t in enumerate(turns) if t['speaker']==speaker and phrase in t['text']]
            if len(matches)!=1:raise ValueError('Evidence not unambiguous: '+cid+' '+phrase)
            if not (0<=q['answer']<len(q['options'])):raise ValueError('Answer index invalid')
            q['sourceEvidence'],q['sourceEvidenceTurn'],q['sourceEvidenceSpeaker']=phrase,matches[0],speaker
        if cid=='voa-2-11':
            q=old['questions'][2]
            if q['options'][q['answer']]=='Food, blankets and warm clothes':
                q['options'][q['answer']]='Food, a blanket, and warm clothing'
                q['explanation']='Anna explicitly says she packed food, a blanket and warm clothing.'
        auth.append({
            'id':old['id'],'title':source['title'],'level':old['level'],'topic':source['topic'],
            'minutes':source['minutes'],'sourceUrl':source['sourceUrl'],'audioUrl':source['audioUrl'],
            'focus':source['focus'],'attribution':'VOA Learning English',
            'sourceSeries':"Let's Learn English — Level 2",
            'sourceLicense':'VOA original public domain material with VOA attribution; third-party content excluded',
            'rightsUrl':cat['rightsUrl'],'audioProvider':'VOA Learning English',
            'audioType':'human_dialogue_source','audioAvailability':'external_online_stream_only',
            'offlineReady':False,'transcriptSource':'Publisher-provided VOA Conversation section',
            'transcriptVerifiedAgainstAudio':False,'timingVerified':False,
            'quality':'publisher_transcript_checked_audio_playback_unverified',
            'transcriptReviewedOn':'2026-10-28','turns':turns,'questions':old['questions']
        })
        linked=[x for x in linked if x['catalogId']!=cid]
        cat.update({'integrationStatus':'interactive_transcript_quiz',
                    'interactiveLessonId':old['id'],'transcriptImported':True,
                    'questionCount':len(old['questions']),'audioBundled':False,
                    'audioPlayback':'VOA MP3 direct link (unverified)',
                    'sourcePageReviewed':'2026-10-28'})
        cat.pop('linkedQuizId',None)
    if len(auth)+len(linked)!=50 or len({x['id'] for x in auth+linked})!=50:
        raise ValueError('Duplicate or missing lesson IDs')
    if sum(len(x['questions']) for x in auth+linked)!=204:
        raise ValueError('Original quiz bank count changed')
    for path,records in [(AUTH,auth),(LINKED,linked),(CAT,catalog)]:
        path.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return {'full':len(auth),'sourceLinked':len(linked),'questions':204,
            'speakerTurnEvidence':sum('sourceEvidenceTurn' in q for l in auth for q in l['questions']),
            'iphoneAudioPlaybackVerified':False,'releaseApproved':False}

if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,indent=2))
