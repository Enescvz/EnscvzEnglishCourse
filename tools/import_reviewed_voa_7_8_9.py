#!/usr/bin/env python3
"""Import VOA original publisher Conversation transcripts for Level 2 lessons 7–9.

The lesson-8 VOA page does not expose a direct Conversation MP3 URL in the
available public page view: never forge one. It is marked publisher-page-only.
Text checked against the VOALearningEnglish publisher pages, 2026-10-28;
source-page transcription is NOT an independent audio alignment review.
All quiz IDs and answer choices remain unchanged. Re-running is idempotent.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUTH = ROOT / 'data/authentic-listening.json'
LINKED = ROOT / 'data/voa-source-quizzes.json'
CAT = ROOT / 'data/voa-source-catalog.json'

SOURCES = {
 'voa-2-07': {
  'sourceUrl':'https://learningenglish.voanews.com/a/lesson-7-tip-your-tour-guide/4064769.html',
  'audioUrl':'https://voa-audio.voanews.eu/vle/2017/10/17/45e008c5-648b-4275-ad2d-d3b058d199a6_hq.mp3?download=1',
  'title':'Tip Your Tour Guide — A River Tour', 'minutes':3.95,
  'publisherAppendix':{'label':'VOA publisher preposition word list (not audio-aligned)',
    'items':['since','at','through','aboard','behind','to','about','by','near','across','for','of','ahead','from','on','around','in','until','over','like','with']},
  'topic':'Travel, landmarks and prepositions of place',
  'focus':['carved in stone','on your left','under a bridge','in the river','come up'],
  'evidence':[
   ('Boy','On a wall inside the memorial, the word “FUTURE” was carved wrong! They carved “EUTURE”!'),
   ('Anna','But I love riding under a bridge in a boat!'),
   ('Boy','The lawmakers did not want to walk around outside in bad weather.'),
   ('Penelope','I still can’t believe this thing drives and sails!'),
  ],
  'transcript':'''Professor Bot: Welcome back! Anna and Penelope are taking a tour with DC Ducks. In this lesson, we are looking for prepositions. Listen for in, on, at, under and over - some important prepositions of place.
Anna: Penelope, the Lincoln Memorial is coming up on your left!
Boy: You’re going to love my Lincoln Memorial Fun Fact!
Anna: Oh, please tell us!
Boy: On a wall inside the memorial, the word “FUTURE” was carved wrong! They carved “EUTURE”!
Anna: Well, we all make mistakes.
Boy: Yeah, but this mistake was carved in stone!
Anna: You’re right. That is pretty bad. Here’s another dollar!
Penelope: More fun facts, please! (Crossing the river) I love riding over bridges! The water looks so pretty from here!
Anna: Penelope, this is amazing! A minute ago, we were riding along the river, and now we’re riding in the river! Awesome.
Penelope: Hey, we’re passing by the Pentagon on our right!
Anna: Penelope, you love riding over the water on a bridge. But I love riding under a bridge in a boat!
Penelope: Anna, look! An airplane is flying right over our heads!
Anna: Wow! This is the closest I’ve ever been to an airplane in flight. Well, I’ve been inside a flying airplane. But not outside of an airplane as it flies over my head!
Penelope: And now we’re driving out of the water. I still can’t believe this thing drives and sails!
Anna: I know. It’s amazing.
Boy: After we ride along these railroad tracks, you’ll see my favorite part of the tour! The U.S. Treasury where they make money!
Professor Bot: That young man is making a lot of money, too. Did you hear these prepositions? On your left, on our right, in the river, over bridges, over our heads, over my head, on a bridge. As you watch more, look for 'inside' and 'outside.'
Penelope: Look, the U.S. Capitol is coming up!
Boy: I have a great Fun Fact about the U.S. Capitol.
Penelope: What is it?
Boy: There are tunnels under the Capitol. They connect the Capitol and office buildings of lawmakers.
Anna: I bet they built them years ago for secret reasons!
Boy: No. The lawmakers did not want to walk around outside in bad weather.
Anna: Oh.
Penelope: We’re back at Union Station!
Boy: Do you want to know a creepy Fun Fact about Union Station? (he points to Union Station)
Penelope: The creepier the better!
Boy: Many years ago, inside Union Station, there was a funeral home!
Anna: A funeral home?! You mean, for dead people?!
Boy: Do you know another kind of funeral home?
Anna: No!
Boy: Well, I’ve gotta run!
Anna: Thanks for giving us the great tour!
Anna: Captain, that was awesome! And your son is a great tour guide!
Captain: What son?
Anna: Him.
Captain: I’ve never seen that boy in my life! See ya, ladies!
Professor Bot: I learned many new Fun Facts in this lesson. Did you learn about prepositions? Here’s a list of all the prepositions used in this lesson. Wow! That’s a lot! I know, let’s not read them. Let’s sing them! Hit it, boys! Take it away singers!''',
 },
 'voa-2-08': {
  'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-8-best-barbecue/4073994.html',
  'audioUrl':None,
  'title':'The Best Barbecue — Food & Opinions', 'minutes':5.0,
  'topic':'Food festivals, opinions and the passive voice',
  'focus':['get your advice','cover a festival','kept secret','loyal to','feel strongly about'],
  'evidence':[
   ('Anna','I’d like to get your advice on my latest project.'),
   ('Kelly','I heard you were sent to cover a big food festival that has all kinds of barbecue.'),
   ('Anna','Most ingredients are kept secret!'),
   ('Anna','Most sauces are made with a tomato sauce, vinegar, and spices.'),
  ],
  'transcript':'''Anna: Thanks for meeting me.
Kelly: Sure.
Anna: I’d like to get your advice on my latest project.
Kelly: Of course. I heard you were sent to cover a big food festival that has all kinds of barbecue. So, how did it go?
Anna: Well, things started out great! But then, well, maybe you should watch it yourself.
Prof. Bot: Hi English learners! Your lesson today is about my favorite food -- barbecue! Your assignment is to find passive sentences. What are those, you might ask? In passive sentences the subject receives the action! For example, “Anna was sent to cover a food festival.” Passive sentences have a form of the BE verb + the past participle of the main verb. This lesson is LOADED with passive sentences. Hey! That’s a passive sentence, too! Okay, now, it’s Barbecue Time!
Anna: Today, a Barbecue Battle is being held in Washington, D.C. This festival, which is known as one of the biggest food festivals in the United States, brings together barbecue lovers from all over the country! Barbecue is meat that is cooked over an open fire or on a grill. Chicken, pork and beef are all common meats to grill on a barbecue! No matter which meat you like to barbecue, the sauce is very important. Sauces are taken very seriously by chefs. Most ingredients are kept secret! So, can you tell us what is in your barbecue sauce?
Chef 1: No, I can’t tell you.
Anna: So, tell us, what is the secret ingredient in your barbecue sauce?
Chef 2: (says nothing.)
Anna: Sauces are made by the barbecue chefs themselves. Most sauces are made with a tomato sauce, vinegar, and spices.
Prof. Bot: How many passive sentences did you find? Here is one I found: Today, a Barbecue Battle is being held on the National Mall in Washington, D.C. Now you try. Turn this sentence from active to passive. Professor Bot loves Barbecue! Barbecue is loved by Prof. Bot. Good job! And yes, I do.
Anna: There are some areas of the U.S. that are known for their tasty barbecue. The states of Texas, North and South Carolina and the cities of Memphis and Kansas City are known as the Barbecue Belt. People who are loyal to barbecue are really loyal to their favorite barbecue. That is why this festival is called a battle! Let’s ask a couple of people which barbecue is best.
Person 1: Texas, of course!
Person 2: Carolina barbecue is the very best.
Person 3: Kansas City!
Person 4: Memphis style!
Person 3: Kansas City!
Person 5: Texas!
Person 3: Kansas!
Person 5: Texas!
Person 3: Kansas!
Person 5: Texas!
Person 3: I say Kansas.
Person 5: Texas!
Person 3: She keeps saying Texas, I say Kansas.
Anna: This is Anna Matteo reporting.
Anna: Kelly, people feel so strongly about barbecue. Unbelievable! So, what do you think of my project?
Kelly: This is what I think. There is no way that Texas has the best barbecue. I am from Kansas City and we have THE best barbecue in the whole country. My mother and father owned a barbecue restaurant, which was really famous! So, I know barbecue! Anna, I know barbecue! I know barbecue! I know barbecue!
Prof Bot: Oh my. Kelly knows a lot about barbecue! And you know more about passive sentences! Be sure you go to the website to learn even more! Ah! Now, if you'll excuse me .. I'm hungry''',
 },
 'voa-2-09': {
  'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-9-pets-are-family-too/4074883.html',
  'audioUrl':'https://voa-audio.voanews.eu/vle/2017/10/25/268efe48-7ad7-48da-8d13-89846a1f681a_hq.mp3?download=1',
  'title':'Pets Are Family, Too! — Pets and Responsibilities', 'minutes':4.43,
  'topic':'Pets, family, responsibility and tag questions',
  'focus':['state fair','pet rock','one of a kind','big responsibility','take care of'],
  'evidence':[
   ('Anna','I went to the D.C. State Fair.'),
   ('Anna','the closest thing I have is my pet rock.'),
   ('Anna','“One-of-Kind Pet” contest. And I won!'),
   ('Ashley','This is Dublin.'),
  ],
  'transcript':'''Anna: Hi Ashley!
Ashley: Hey, Anna! How was your weekend?
Anna: It was great! I went to the D.C. State Fair.
Ashley: I would have gone, but I was busy. How was it?
Anna: It was awesome! I won first place in a pet contest!
Ashley: But, you don’t have a pet, do you?
Anna: Yes and no. What do you mean by “pet”?
Prof. Bot: A pet is an animal that lives with you. People love their pets. "Ashley said, you don’t have a pet, do you? She used a tag question, a small question at the end of a sentence. Let's look for more of them!
Anna: Look, a pet! Who’s this cute little dog?
Ashley: Oh, right. You haven’t met my dog, have you? This is Dublin.
Anna: Hi, Dublin! Nice to meet you. He’s so cute!
Ashley: Thanks! So, tell me about the state fair.
Anna: Oh, there were the usual things -- fair food, cute babies, music. But there must have been a dozen different contests! And some were pretty strange.
Anna: There was a contest to see who could spit a watermelon seed the farthest. You should have seen all the people who wanted to spit a watermelon seed! And, it was pretty fun to watch. But Ashley, the pet contests were the best. There was a pet parade. Lots of people walked with their dogs.
Ashley: That sounds so fun. But Anna, tell me, how did you win a pet contest without a pet?
Anna: Okay, the closest thing I have is my pet rock.
Anna: I know it’s silly, but I’ve had it since I was a little girl. So, for a joke, I brought it to the fair. But then I was invited to enter the “One-of-Kind Pet” contest. And I won! (holds up first place ribbon)
Ashley: Anna, only you could have won a pet contest with a pet rock. I should have brought Dublin. He would’ve won a contest!
Anna: It’s not very easy to win one of these. (shows her the blue ribbon) Does he have a costume?
Anna: They had a costume contest. You should have seen this little girl. She and her dog wore matching princess costumes!
Ashley: Dublin doesn’t wear costumes.
Anna: Does he know any tricks?
Ashley: Come this way. Now, watch this. (Dublin chases a toy)
Anna: You caught it, Dublin! And you killed it! Good dog! Ashley, he could have won the Best Catch contest! Aw, good boy! Ashley, pets are fun, aren’t they?
Ashley: Yes. And they become part of your family. (she drinks from her Dublin mug)
Anna: Ashley, I think I want a dog. No. I know I want a dog!
Ashley: It’s a big responsibility. You may want to spend time with a dog first.
Anna: That is a great idea. But where can I find a dog?
Ashley: You know, Anna, I have some shopping to do. Do you want to watch Dublin for a couple of hours?
Anna: Yes! I would! I will take very good care of him!
Ashley: I know you will. Here’s his leash.
Anna: Thank you.
Ashley: (to Dublin) Okay, I'll miss you!
Anna: Aw. I don’t want you to be lonely. Here, Rocky can stay with you. (puts pet rock on wall)
Ashley: Anna, I really don’t need … Okay. Thanks, Anna.
Anna: Sure. Bye, Ashley. (to Dublin) Come on, Dublin! Bye, Rocky!
Ashley: Bye!
Prof. Bot: Anna’s rock is cute, isn’t it? Oh, there is another tag question! You found some more, didn’t you? You haven’t met my dog, have you? Go to the VOA Learning English website to learn more.''',
 },
}


def parse_turns(text):
    turns=[]
    for line in text.splitlines():
        m=re.match(r'^([^:]{2,45}):\s*(.*)$',line.strip())
        if not m or not m.group(2):
            raise ValueError('Unstructured/empty transcript line: '+line)
        turns.append({'speaker':m.group(1),'text':m.group(2)})
    return turns


def run():
    full=json.loads(AUTH.read_text(encoding='utf-8'))
    linked=json.loads(LINKED.read_text(encoding='utf-8'))
    catalog=json.loads(CAT.read_text(encoding='utf-8'))
    for cid,source in SOURCES.items():
        cat=next(x for x in catalog if x['id']==cid)
        if cat['sourceUrl']!=source['sourceUrl']:
            raise ValueError('Publisher source URL mismatch: '+cid)
        lesson_id='voa-linked-'+cid.split('-',1)[-1]
        old=next((x for x in linked if x['catalogId']==cid),None)
        if old is None:
            existing=next((x for x in full if x['id']==lesson_id),None)
            if not existing:raise ValueError('Quiz ID disappeared: '+lesson_id)
            if source.get('publisherAppendix') and not existing.get('publisherAppendix'):
                existing['publisherAppendix']=source['publisherAppendix']
            continue
        if len(old['questions'])!=4 or len(source['evidence'])!=4:
            raise ValueError('Unexpected quiz length: '+cid)
        turns=parse_turns(source['transcript'])
        if len(turns)<25:raise ValueError('Incomplete publisher Conversation: '+cid)
        # Attach exact source evidence to each pre-existing question without rewriting IDs/answers.
        for q,(speaker,evidence) in zip(old['questions'],source['evidence']):
            matches=[(i,t) for i,t in enumerate(turns) if speaker==t['speaker'] and evidence in t['text']]
            if len(matches)!=1:raise ValueError('Evidence must uniquely match transcript: '+cid+' '+evidence)
            q['sourceEvidence']=evidence
            q['sourceEvidenceTurn']=matches[0][0]
            q['sourceEvidenceSpeaker']=speaker
            if not (0<=q['answer']<len(q['options'])):raise ValueError('Answer index invalid')
        has_audio=bool(source['audioUrl'])
        full.append({
            'id':old['id'],'title':source['title'],'level':old['level'],
            'topic':source['topic'],'minutes':source['minutes'],
            'sourceUrl':source['sourceUrl'],'audioUrl':source['audioUrl'],
            'focus':source['focus'],'attribution':'VOA Learning English',
            'sourceSeries':"Let's Learn English — Level 2",
            'sourceLicense':'VOA original public domain educational material; third-party content excluded',
            'rightsUrl':cat['rightsUrl'],'audioProvider':'VOA Learning English',
            'audioType':'human_dialogue_source',
            'audioAvailability':'external_online_stream_only' if has_audio else 'publisher_page_only',
            'offlineReady':False,'transcriptSource':'Publisher-provided VOA Conversation section',
            'transcriptVerifiedAgainstAudio':False,'timingVerified':False,
            'quality':'publisher_transcript_checked_audio_playback_unverified',
            'transcriptReviewedOn':'2026-10-28','turns':turns,
            **({'publisherAppendix':source['publisherAppendix']} if source.get('publisherAppendix') else {}),
            'questions':old['questions'],
        })
        linked=[x for x in linked if x['catalogId']!=cid]
        cat.update({
            'integrationStatus':'interactive_transcript_quiz',
            'interactiveLessonId':old['id'],'transcriptImported':True,
            'questionCount':4,'audioBundled':False,
            'audioPlayback':'VOA MP3 direct link (unverified)' if has_audio else 'Publisher page link only (no verified MP3 URL)',
            'sourcePageReviewed':'2026-10-28',
        })
        cat.pop('linkedQuizId',None)
    all_ids=[x['id'] for x in full+linked]
    if len(all_ids)!=len(set(all_ids)) or len(all_ids)!=50:
        raise ValueError('Lost or duplicate quiz identity')
    if sum(len(x['questions']) for x in full+linked)!=204:
        raise ValueError('Quiz data lost')
    for path,records in [(AUTH,full),(LINKED,linked),(CAT,catalog)]:
        path.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return {'transcriptsInApp':len(full),'linkedQuizOnly':len(linked),'questionCount':sum(len(x['questions']) for x in full+linked),'turnEvidenceAdded':12,'publisherPageOnlyAudio':['voa-2-08'],'devicePlaybackVerified':False,'releaseApproved':False}

if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
