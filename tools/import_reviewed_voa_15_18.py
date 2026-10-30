#!/usr/bin/env python3
"""Publisher-page reviewed VOA L2 15-18, preserving quiz IDs and learner progress.

Source: original VOA Learning English Conversation, public domain with VOA credit.
Not verified against real audio or a physical iPhone. Run idempotently.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
RIGHTS='https://learningenglish.voanews.com/p/6861.html'

# Each numbered dialogue line is one publisher speaker turn. Narration inside an
# already identified Professor Bot turn is preserved. Silent stage directions are
# omitted (the in-app view is the *spoken* Conversation transcript).
RAW={
15: '''Anna|Penelope, even though we both love speed walking, could we slow down a bit?
Penelope|No way! I think because I’m walking with you, I’m walking faster.
Anna|Come on, Penelope. Let's take a break. We've been speed walking since 8 a.m.! You're so competitive! You even wore your medals!
Penelope|You brought your trophies! You’re out of shape. When we were little girls, we could speed walk all day! (pulls ahead)
Anna|(chases her) Hey, wait for me! Hey, you know the speed walking rules! If both feet leave the ground, it’s running! You ran!
Prof. Bot|Anna and Penelope are doing something they both love - speed walking! They are also using adverb clauses. Adverb clauses tell us when, why, how, where and under what conditions. For example, "since 8 a.m." tells us when. Adverb clauses are dependent clauses and need an independent clause to make a complete sentence. Words like before, after, when, because, since, if and even though can signal an adverb clause. Keep watching for more adverb clauses!
Penelope|Whew! That was great!
Anna|(Anna catches up) Wow, Penelope, you’re still really fast! Since I’ve been working in an office, my speed walking has been much slower.
Penelope|You are slower, Anna. Maybe you should hire a personal trainer.
Anna|That will be great. As long as the trainer understands speed walking.
Penelope|(hands her a business card) Try this company. After you fill out an online application, they will match you to the perfect trainer.
Anna|As soon as I get home tonight, I’ll do it! Thanks.
Anna|Are you my trainer?
Alaskan Albert|If you’re Anna, then I’m your trainer -- Alaskan Albert. Because I’m from Alaskan wilderness, I’m skilled in all outdoor activities of the wild.
Anna|That’s great but what about speed walking?
Alaskan Albert|Speed walking? That's funny! Since I’ve been living in the city, I’ve combined wilderness training with a city workout. I call it “Call of the Wild Parkour!” (He howls like a wolf.)
Anna|Okay … but seriously, when do we speed walk?
Alaskan Albert|Your application did not say how funny you are!
Anna|No. But it did say that I'm a speed walker! Did you read it? Forget it. We'll have to cancel.
Alaskan Albert|Why?
Anna|We can't train today because it's too cold and too windy.
Alaskan Albert|No way! No pain, no gain! When you exercise in really cold weather, you feel alive!
Anna|Really? Because right now I just feel cold.
Alaskan Albert|You're so funny. But seriously, after our training, you will be ready for any extreme physical challenge. Let's get started!
Alaskan Albert|Anna, even though you’re trying really hard, you’re really bad at Call of the Wild Parkour. (he howls)
Anna|I'm bad at Call of the Wild Parkour because I don’t want to do Call of the Wild Parkour! (she howls) I am a speed walker. It’s what I do. It’s part of who I am.
Alaskan Albert|Why didn’t you say something?
Anna|I did. Several times! You thought I was joking.
Alaskan Albert|Now I understand. Anna, I can help you., if you follow my advice, I'll put the speed back in your speed walk.
Alaskan Albert|Go, Anna, go!
Prof. Bot|For more about adverb clauses, visit our website!''',
16: '''Anna|Hi, Kaveh! Let’s go to lunch!
Kaveh|Ooh, I know a great place. When I first started working here, I would go every day!
Anna|Great. Oh, no.
Kaveh|What’s wrong?
Anna|I lost my key! I just had it this morning.
Kaveh|You should check the Lost & Found office.
Anna|Great idea. Where is it?
Kaveh|Oh, it used to be across from the cafeteria. But now it’s down in the basement next to the elevators. It’s really hard to find.
Anna|The Lost & Found is hard to find. That’s funny.
Kaveh|It is.
Professor Bot|I hope Anna can find the Lost & Found office! Used to and would describe something that happened repeatedly in the past. Kaveh uses would when he says, “When I first started working here, I would go every day! There are two differences between used to and would. Number 1: We use would only when we say the time period first. Number 2: For verbs like be, think, feel, see and understand, we can only use used to. Kaveh says, "It used to be across from the cafeteria." Keep listening for more!
Serenity|Come in! I am Serenity.
Anna|Hi, Serenity. I’m Anna!
Serenity|Please, sit down. How can I help you?
Anna|I lost something very important.
Serenity|Shh. I already know. You need help.
Anna|Yes. I need help finding the key …
Serenity|Shh. You need to find the key – the key that will give you happiness.
Anna|Yes. Finding this key will make me very happy.
Serenity|First, Anna, let me tell you a little bit about myself.
Anna|Okay.
Serenity|I used to be a very important person with a very important job. I made a lot of money -- I mean a lot.
Anna|Wow. Good for you!
Serenity|No! No, it was bad for me. I lost the most important thing – the key! You’ve lost it too, haven’t you, Anna? Haven’t you?
Anna|I guess. So, how does this work? Do I have to fill out a form or something?
Serenity|No. No forms. Just answer this one question: As a child, what did you use to do to feel happy?
Anna|When I was little, I used to sing all the time with my family. Those were good times.
Serenity|Singing is so joyful! I used to sing. But now that I’ve started my business, I’ve just been too busy. Too busy! Anna, why don’t you sing again?
Anna|I sing everywhere! I sing in the office. I sing on the metro. I sing in the elevators. I sing on the escalators. I sing in the bathroom. Serenity! Serenity! I really need to find my key. Yeah!
Serenity|Yes, we need to find the key … the key to happiness.
Anna|No, no. I just need to find the key to my apartment.
Serenity|I used to know. But now I don't! Do you, Anna?
Anna|I don’t know. I think I left it in the ladies’ room. You know, this isn’t the Lost & Found, is it?
Serenity|It could be the Lost & Found. I’m lost! And I used to find joy for people! I used to find joy!
Anna|You know, this is a bad time for you. I’ll find the Lost & Found myself. Bye, thanks.
Serenity|I used to find joy. I used to find joy! I used to find joy!
Anna|Ah, I found my key!
Serenity|I used to find joy!
Pofessor Bot|Oh no. Serenity lost her joy. But at least Anna found her key! Check out our website for more!''',
17: '''Ms. Weaver|Anna, Pete, I have a new assignment for you -- a show on single parents! What is it like for a mother or a father to raise a child by herself or himself?
Anna|We can interview single parents. They can share their experiences themselves.
Ms. Weaver|Yes, but you need to experience parenthood yourselves.
Anna|Ourselves?
Peter|Yeah, how do we do that? We’re not parents.
Ms. Weaver|I asked myself the same question. I said, "Caty, how are they gonna do that?" Then an idea came to me. I will give you the babies!
Professor Bot|You may be asking yourself the same thing that I’m asking myself: what is Ms. Weaver talking about!? I am sure we will find out shortly. This lesson teaches reflexive pronouns. Reflexive pronouns refer back to the subject of a sentence or clause. We use them when the subject and the object are the same person or thing. For example, Ms. Weaver says, “I asked myself the same question.” “I” is the subject and “myself” refers back to it. Here, she would not use the pronoun “me.” You need to use the reflexive pronoun “myself.” Reflexive pronouns are easy to find: they end in “self” or “selves.” I have a feeling we are going to see a lot of reflexive pronouns. Listen for them!
Ms. Weaver|Here are your babies!
Pete|Those are bags of flour.
Ms. Weaver|No, Pete, for the next six days, this is your baby. Here are your instructions. Do not leave your babies alone. A baby cannot take care of itself. And you two must do everything by yourselves. We will meet next Friday. Oh, and the person who does the best research will get an extra day of vacation. Help yourself to a baby.
Anna|Pete, look, my baby is organic and whole grain. Your baby is ordinary.
Anna|(to Pete) Monster! (to Caty) This is a great idea, Ms. Weaver!
Pete|This is a terrible idea.
Anna|Speak for yourself, Pete! We need to throw ourselves into the research! I’m starting right now!
Pete|Hey Anna, you forgot your baby!
Anna|Come to mama!
Anna|Good girl! Good girl!
Professor Bot|Singular reflexive pronouns end in “self.” Plural ones end in “selves.” Anna says, “We need to throw ourselves into the research!” The subject “we” is plural. So, we must use the plural reflexive pronoun “ourselves.”
Anna|This is hard! I hope Pete is not doing well. I really need that vacation day!
Professor Bot|We will all see how Pete is doing in the next episode. We’ll also learn when not to use reflexive pronouns.''',
18: '''Professor Bot|In Part 1 of this two-part lesson, Ms. Weaver gave Anna and Pete an assignment. Ms. Weaver instructed them to do everything by themselves. “Themselves” is a reflexive pronoun. In today’s lesson, Ms. Weaver will look at Pete’s and Anna’s research. First, let’s see Pete’s experiment.
Ms. Weaver|Okay, Pete, let me see your research first.
Ms. Weaver|That’s a heavy binder. And you and your Baby look great.
Pete|Thanks, Ms. Weaver. We feel great!
Ms. Weaver|Anna. Anna, you’re next. Anna? Anna wake up!
Anna|I'm here, Baby! I’m here! I’m here! Here's your bottle.
Ms. Weaver|Anna, you and your baby look awful. What happened?
Anna|Well, I took her everywhere. Everywhere. And I fed her every three hours. So, I haven’t slept since … what day is it?
Ms. Weaver|It’s Friday. What happened there?
Anna|Oh, that. Oh, that. I was making myself a salad and had a little accident with a knife. I put my flour baby in front of me. And then I accidentally stabbed it. But I gave it First Aid!
Ms. Weaver|Is that a burn?
Anna|Yes. Yes it is. While I was making myself dinner, I put Baby next to me. I accidentally knocked her into the sink. So I put her in the microwave to dry. That’s when she caught fire.
Professor Bot|Okay. So, we use a reflexive pronoun when it refers to the subject of a sentence or clause. But we DON’T use a reflexive pronoun with prepositions of place. Anna uses examples of both in one sentence: While I was making myself dinner, I put Baby next to me. We use a reflexive pronoun in the first part of the sentence. “Myself” refers to the subject “I.” But in the second part of the sentence, we don’t use a reflexive pronoun in the prepositional phrase. We use the pronoun “me.” Why? “next to” is a preposition of place.
Ms. Weaver|Anna, Anna, you should be very proud of yourself.
Pete|Proud? She stabbed and burned her baby!! And she only did one page of research…and it’s covered in milk. Ew.
Ms. Weaver|Yes, Pete. But she followed instructions.
Pete|Hey, I did ...
Ms. Weaver|Please, Pete. Anna, I think your baby has lost some weight. Is there something else you want to share?
Anna|Yes. I’d like to share … these! I made them myself this morning.
Pete|You baked your baby? You should be ashamed of yourself!
Anna|I baked them at the end of the experiment, Pete. At that point, this was just a bag of flour.
Pete|It was always just a bag of flour!!
Ms. Weaver|Pete, will you listen to yourself?! You sound crazy.
Pete|I sound crazy! This whole experiment was crazy!! She was the one who carried around and fed it and ...
Pete|Mmm. That is good.
Professor Bot|So, what have we learned? We’ve learned when to use reflexive pronouns and when not to. Go to our website for more information! You can practice using reflexive pronouns in our comments section.'''
}
META={
 15:('Before and After — Speed Walking','Fitness, adverb clauses and personal training',4.15,'2018/01/04/99ceaa2e-fb25-43a8-8731-0a7f23901d65','Anna|we both love speed walking','Anna|since 8 a.m.','Penelope|hire a personal trainer','Alaskan Albert|I call it “Call of the Wild Parkour!”'),
 16:('Find Your Joy! — Lost and Found','Lost belongings and used to/would',4.68,'2018/01/10/95f0ce1f-6cfd-44e4-b83a-e225d7cb0224','Anna|I lost my key!','Kaveh|down in the basement next to the elevators','Serenity|the key that will give you happiness','Anna|used to sing all the time with my family'),
 17:('Flour Baby, Part 1 — A New Assignment','Parenthood, reflexive pronouns and responsibility',3.97,'2018/01/24/4f5af081-e654-4912-9f5d-24cd3fa5170a','Ms. Weaver|a show on single parents','Pete|Those are bags of flour.','Ms. Weaver|for the next six days','Ms. Weaver|an extra day of vacation'),
 18:('Flour Baby, Part 2 — Research Results','Parenting experiment, accidents and reflexive pronouns',4.3,'2018/01/31/16d806b3-f878-4eff-bd6e-1857ec1241e0','Ms. Weaver|That’s a heavy binder.','Anna|I fed her every three hours','Anna|I put her in the microwave to dry.','Ms. Weaver|But she followed instructions.')
}

def read(name):return json.loads((DATA/name).read_text(encoding='utf-8'))
def save(name,obj):(DATA/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def run():
    auth=read('authentic-listening.json'); linked=read('voa-source-quizzes.json'); catalog=read('voa-source-catalog.json')
    oldids={x['id'] for x in auth+linked}; originals={x['id']:json.dumps(x['questions'],ensure_ascii=False) for x in auth+linked}
    for n in (15,16,17,18):
        cid=f'voa-2-{n:02d}'; lid=f'voa-linked-2-{n:02d}'
        cat=next(x for x in catalog if x['id']==cid)
        if any(x['id']==lid for x in auth): continue
        old=next((x for x in linked if x['id']==lid),None)
        if old is None:raise ValueError(f'Lost old quiz {lid}')
        turns=[{'speaker':a,'text':b} for a,b in (line.split('|',1) for line in RAW[n].splitlines())]
        title,topic,minutes,mp3,*excerpts=META[n]
        if len(turns)<15:raise ValueError('Too few source turns '+lid)
        if len(excerpts)!=len(old['questions']):raise ValueError('Question count changed '+lid)
        for q,ev in zip(old['questions'],excerpts):
            speaker,quote=ev.split('|',1)
            found=[i for i,t in enumerate(turns) if t['speaker']==speaker and quote in t['text']]
            if len(found)!=1:raise ValueError(f'Ambiguous/missing speaker/quote {lid}: {ev}: {found}')
            if not 0<=q['answer']<len(q['options']):raise ValueError('Invalid answer')
            q.update(sourceEvidence=quote,sourceEvidenceTurn=found[0],sourceEvidenceSpeaker=speaker)
        auth.append({'id':lid,'title':title,'level':old['level'],'topic':topic,'minutes':minutes,
            'sourceUrl':cat['sourceUrl'],
            'audioUrl':f'https://voa-audio.voanews.eu/vle/{mp3}_hq.mp3?download=1',
            'focus':['publisher dialogue','listening comprehension','American English'],
            'attribution':'VOA Learning English','sourceSeries':"Let's Learn English — Level 2",
            'sourceLicense':'VOA original public domain with attribution; third-party content excluded',
            'rightsUrl':RIGHTS,'audioProvider':'VOA Learning English','audioType':'human_dialogue_source',
            'audioAvailability':'external_online_stream_only','offlineReady':False,
            'transcriptSource':'VOA official page — Conversation spoken-turn transcript; silent directions omitted',
            'transcriptVerifiedAgainstAudio':False,'timingVerified':False,
            'quality':'publisher_spoken_text_reviewed_audio_playback_unverified',
            'transcriptReviewedOn':'2026-10-28','turns':turns,'questions':old['questions']})
        linked=[x for x in linked if x['id']!=lid]
        cat.update({'integrationStatus':'interactive_transcript_quiz','interactiveLessonId':lid,
            'transcriptImported':True,'questionCount':len(old['questions']),
            'audioBundled':False,'audioPlayback':'VOA online MP3 link (not verified)',
            'sourcePageReviewed':'2026-10-28'})
        cat.pop('linkedQuizId',None)
    if {x['id'] for x in auth+linked}!=oldids or len(auth)+len(linked)!=50:raise AssertionError('Changed lesson ID set')
    if len(auth)<18 or len(linked)>32:raise AssertionError('Missing previously imported lessons')
    if sum(len(x['questions']) for x in auth+linked)!=204:raise AssertionError('Question total changed')
    for x in auth+linked:
        if x['id'] not in originals:raise AssertionError('Lesson missing')
        if x['id'] not in [f'voa-linked-2-{n:02d}' for n in META] and json.dumps(x['questions'],ensure_ascii=False)!=originals[x['id']]:raise AssertionError('Unrelated quiz changed')
    for fn,data in [('authentic-listening.json',auth),('voa-source-quizzes.json',linked),('voa-source-catalog.json',catalog)]:save(fn,data)
    return {'integrated':len(auth),'linked':len(linked),'questions':204,'evidence':sum('sourceEvidenceTurn' in q for x in auth for q in x['questions'])}
if __name__=='__main__':print(json.dumps(run(),indent=2))
