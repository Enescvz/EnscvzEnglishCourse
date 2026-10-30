#!/usr/bin/env python3
"""Create a source-grounded *online* listening pilot from VOA-published transcripts.

VOA Learning English says its original texts and MP3s may be reused with attribution.
Source: https://learningenglish.voanews.com/p/6861.html
Important: these are publisher-published transcripts; no unsupported ASR claim.
Audio is streamed from VOA and NOT bundled. Do not set offline=true.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def parse(text):
    rows = []
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        person, sep, words = line.partition(': ')
        if not sep or not person or not words:
            raise ValueError(f'Invalid VOA transcript turn: {line}')
        rows.append({'speaker':person.strip(), 'text':words.strip()})
    return rows

LESSONS=[
{
'id':'voa-level2-01-budget-cuts', 'title':'Budget Cuts — Office Rumors', 'level':'B1–B2', 'topic':'Work & Everyday Conversation', 'minutes':4.12,
'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson1/3960391.html',
'audioUrl':'https://voa-audio.voanews.eu/vle/2017/08/31/3bf697ff-3ef5-4d59-8dcd-52613e2e7e9d_hq.mp3?download=1',
'focus':['budget cuts','gossip','rumors','assignment','fire someone'],
'raw':'''Anna: Hum. Oh! “Important meeting. Everyone must come.” Well, back to work! And my boss has called a meeting. I wonder what it's about. Maybe we're all getting raises! Ooo, there's Jonathan! Maybe he knows.
Professor Bot: Hi! I'm Professor Bot! This video is all about work. People talk about jobs and things that happen at work. Your assignment is to find as many work words as you can. Don't worry, I'll help.
Anna: So, Jonathan, what do you think today's meeting is about? The email sounded important.
Jonathan: Well, I have heard people in the building talking about budget cuts.
Anna: Oh! Budget cuts? Wait, who has been talking about budget cuts?
Jonathan: Mark in Accounting.
Anna: Mark in Accounting? That's one person. That's not “people.”
Jonathan: I know, but Mark knows everything that goes on at The Studio.
Anna: That is true. But wait, look at us. We shouldn't gossip. That's how rumors start. We'll just go to the meeting and see what happens.
Jonathan: You're right. No more talk about budget cuts.
Amelia: Budget cuts? Oh no!
Amelia: I just heard Anna and Jonathan talking about budget cuts.
Kaveh: That must be what the meeting is about. When there are budget cuts, people lose their jobs.
Amelia: Not you. You're a good reporter.
Kaveh: And it's not you. You've done a great job as a videographer.
Amelia: I can't go back to being a detective. Criminals scare me!
Kaveh: And I can't go back to being a teacher! High school kids scare me!
Professor Bot: Did you hear any work words? They talked about a lot of jobs. You can make the name of a job by adding an ending to a verb! Kaveh reports, so, he's a reporter. Amelia used to detect, so she was a detective. If you teach, you're a teacher. And a videographer….uh, I think you understand. Back to the story.
Kaveh: Penelope, have you heard the news? Today's meeting is about budget cuts.
Penelope: That's awful! What should I do?
Kaveh: Update your résumé. I’ve already updated mine. I’ll see you at the meeting.
Ms. Weaver: Hello everyone! Quiet, please. Quiet, please!
Ms. Weaver: This meeting won’t take long. Then you can all leave.
Ms. Weaver: What is wrong with everyone? You look like I'm going to fire you. Ha-ha-ha-ha-ha! Seriously, what is wrong with everyone?
Anna: Excuse me, Ms. Weaver?
Ms. Weaver: Yes, Anna.
Anna: Well, everyone has been worrying about, you know … We’ve been worrying that you are going to fire us!
Ms. Weaver: I’m not going to fire any of you! No! The reason for this meeting is to tell you what a good job you’ve been doing and give out new assignments. Budget cuts have been happening. But only one person has lost their job -- Mark in Accounting? Now, let’s talk about those new assignments.
Professor Bot: Ms. Weaver's team is doing a good job! How did you do? Did you find all of the work words? Here's a list you can check.''',
'questions':[
 ('What were Anna and Jonathan initially worried about?', ['An office relocation','Budget cuts and possible job losses','A new staff party','A delayed delivery'],1,'The meeting is first misunderstood as a discussion of budget cuts.'),
 ('Who originally told Jonathan about the budget cuts?', ['Ms. Weaver','Kaveh','Mark in Accounting','Amelia'],2,'Jonathan says that Mark in Accounting is the source.'),
 ('What does Anna say can cause rumors to spread?', ['Gossiping','Working late','Changing jobs','Sending applications'],0,'Anna realizes that gossip can spread unverified stories.'),
 ('Why did Kaveh tell Penelope to update her résumé?', ['He wanted her to be promoted','He thought employees might lose their jobs','He was moving to a different country','He had a new job offer for her'],1,'He believed the budget cuts meant layoffs were possible.'),
 ('What was the real reason for the meeting?', ['A company closure','A pay reduction for everyone','To give praise and new assignments','To fire Anna'],2,'Ms. Weaver explains that the meeting is about good work and new assignments.'),
 ]
},
{
'id':'voa-level2-02-interview', 'title':'The Interview — Team Up and Find Out', 'level':'B1–B2', 'topic':'Phrasal Verbs & Social Skills', 'minutes':4.08,
'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-2/3960471.html',
'audioUrl':'https://voa-audio.voanews.eu/vle/2017/09/05/676d9800-cee0-4a59-9e79-b9378e0061ad_hq.mp3?download=1',
'focus':['give out','take on','team up','throw away','find out'],
'raw':'''Anna: Ms. Weaver is giving new assignments out. I am ready to take on anything she gives me. Well, except reporting traffic from a helicopter. Wish me luck.
Professor Bot: I wonder what Anna’s new assignment will be? Professor Bot here! While you are watching, look for phrasal, or two-word verbs. Some stay together, like “go back” and some can come apart, like “give [assignments] out.” Good luck, Anna!
Ms. Weaver: So, as I said at the meeting last week, I have new assignments for everyone at The Studio. Anna, you're good at asking questions. So, I want you to go back to hosting and reporting.
Anna: That sounds great.
Ms. Weaver: You're also a team player. So, I want you team up with someone ...
Anna: That sounds even better!
Ms. Weaver: ... someone who is very "different" from you.
Anna: That sounds ... what do you mean "different"?
Ms. Weaver: Well, you are very cheerful, you're a people person. I want you to team up with someone who ... isn't.
Anna: Ms. Weaver, I will find that person.
Mimi: Excuse me. Are you using this chair?
Pete: Yes.
Anna: Pete, hi! Thanks for meeting me.
Pete: Sure. But I don’t have lots of time, Anna. I’m busy looking for work.
Anna: Pete, you can tear these want ads up and throw them away! I have good news!
Pete: Anna, I was working on that crossword puzzle.
Anna: Oh. Sorry. Sorry. Pete, forget about the crossword puzzle. I have a job offer for you!
Pete: I'm listening.
Anna: My boss wants me to team up with someone to host a talk show. But the person must be different from me. So, I thought of you.
Pete: Different from you? What do you mean?
Anna: I'm sorry, Pete, I don't have time right now. Here's my boss's address. Your interview is tomorrow morning at 10 am.
Pete: But what do you mean “different”?
Anna: Just be yourself, Pete. Just be yourself.
Professor Bot: Did you find any two-word verbs? Here’s one example. Pete can throw the want ads away! Throw away is a two-word verb.
Ms. Weaver: Thanks for coming in, Pete.
Pete: Thanks for the opportunity, Ms. Weaver.
Ms. Weaver: I need to find out if you have the skills for this job. And I want you to be completely honest.
Pete: Okay.
Ms. Weaver: First, let's talk about your personal skills. Pete, are you a people person?
Pete: Well, okay, sometimes I think people talk too much.
Ms. Weaver: Pete, what work of yours are you most proud of?
Pete: Last year, I locked myself in a cabin and wrote a book. I didn't speak to anybody the entire time! It was the best two months of my life.
Ms. Weaver: Okay. I think I’ve heard enough.
Anna: Hey! Hey, Pete, how was the interview with Ms. Weaver?
Pete: Well, she said I was grumpy and not good with people.
Anna: And … ?
Pete: And, I got the job!
Anna: I knew it! Congratulations! Let's go celebrate.
Pete: Okay!
Professor Bot: Did you find more two-word verbs? Here is the list.''',
'questions':[
 ('What kind of colleague does Ms. Weaver want Anna to work with?', ['Someone very similar to Anna','Someone different from Anna','A reporter from another country','Someone who enjoys driving helicopters'],1,'Ms. Weaver wants a different personality for the new talk show.'),
 ('What does “team up with” mean in this conversation?', ['Compete against someone','Work together with someone','Interview someone in secret','Get promoted ahead of someone'],1,'The show would have two people working as a team.'),
 ('Why does Anna suggest Pete throw away the job ads?', ['She has a job opportunity for him','He has already retired','She lost his crossword puzzle','The newspaper is outdated'],0,'She tells Pete that she has an offer for him.'),
 ('Which personal trait worries Ms. Weaver during the interview?', ['Pete talks too much','Pete is uncomfortable with people','Pete refuses to write','Pete does not speak English'],1,'Pete describes avoiding people and preferring months alone.'),
 ('What happens to Pete at the end?', ['He rejects the position','He gets the job','He leaves the country','He starts teaching again'],1,'Despite being called grumpy, Pete says he got the job.'),
 ('In the interview, what does “find out” mean?', ['Discover or determine','Leave a building','Forget something','Work overtime'],0,'Ms. Weaver needs to discover whether Pete has the right skills.'),
 ]
},
{
'id':'voa-level2-10-peru', 'title':'Visit to Peru — Making Plans', 'level':'B1–B2', 'topic':'Travel & Social Plans', 'minutes':3.95,
'sourceUrl':'https://learningenglish.voanews.com/a/lets-learn-english-lesson-10-visit-to-peru/4079037.html',
'audioUrl':'https://voa-audio.voanews.eu/vle/2017/10/27/863aecf4-1d6a-4fe1-9789-5251ac1e0be1_hq.mp3?download=1',
'focus':['I wish I could','How’s it going?','check out','deadline','in person'],
'raw':'''Bruna: Hi, Anna!
Anna: Hi, Bruna! What’s up?
Bruna: I thought we could meet for lunch today.
Anna: I wish I could, but I can’t. I have to research Peru for a story.
Bruna: How’s it going?
Anna: Not so good. I’ve been reading about Peru and listening to Peruvian music. I really want to understand Peru. I hope it's enough.
Bruna: You should visit Peru.
Anna: I wish!
Bruna: You can!
Anna: Bruna, I don’t have the money or time to go to Peru. My deadline is tomorrow!
Bruna: No, I don’t mean to really go there. The museum where I work is having a Peruvian festival today! …. Anna? Anna? Anna, are you there?
Prof. Bot: Hello again! Professor Bot here. Today we will hear about wishes and hopes. Bruna asked Anna to go to lunch, but she answered, I wish I could, but I can’t. Listen for more hope and wish sentences.
Bruna: Hi, Anna!
Anna: Hi, Bruna! Thanks for telling me about this event.
Bruna: Sure! It's much better than staring at your computer. I hope it helps with your story.
Anna: I’m sure it will. So, what should we see first?
Bruna: Dance and music are very important to Peruvian culture, so let’s watch the dancers.
Anna: Great! Let’s go!
Bruna: There's this very special Peruvian dance called Marinera Norteña.
Anna: I love the Marinera Nortina… !
Bruna: Marinera Norteña.
Anna: Marinera Norten… ?
Bruna: No. Marinera Norteña.
Anna: I love the … marriage dance!
Anna: Bruna, I read about this dance. But it is much more romantic in person!
Bruna: The dancers are giving lessons after their performance. You should try it!
Anna: I’d love to. But I’m not ready to get married. I mean, one day I hope to meet the right guy. We’ll buy matching motorcycles and ride into the sunset -- the wind blowing through our hair!
Bruna: Anna, the dance just shows the courtship tradition. It doesn’t mean you will get married.
Anna: Oh. Well, I’ll try anyway.
Bruna: Don’t forget. This festival also shows Peruvian art!
Anna: I hope I have time to see everything!
Bruna: Anna, I wish I could join you. But I have some work to do.
Anna: Of course, of course. You go back to work. I’ll check out the art.
Bruna: Okay, I’m hoping to finish in about an hour. Let’s meet then.
Anna: Great. See you then!
Bruna: See ya!
Prof. Bot: Did you notice any sentences with hope or wish? Anna says, “One day I hope to meet the right guy.” That’s an example of using “hope” with an infinitive to talk about doing something in the future. Keep watching!
Anna: Oh, wow! I can make my own Peruvian art!
Bruna: Anna, how’s it going?
Anna: Hi, Bruna!
Bruna: You know you're in the kid's section, right?
Anna: I'm in the art making section.
Bruna: I see that. Your art is very nice. I wish I could do art like that.
Anna: Oh, this one’s not mine. This is mine.
Bruna: Wow! Really? That's really nice!
Anna: Thanks! And thanks for telling me about this festival. I learned so much about Peru. Ooh, we still have time!
Bruna: Time for what?
Anna: Time for Marinera Norteña!
Prof. Bot: Do you remember what Anna said? “I really want to understand Peru.” I hope you understand Peru a little better now, too. And I wish I could talk with you more about grammar, but that’s all the time we have today! Go to the website to learn more!''',
'questions':[
 ('Why does Anna initially refuse to meet for lunch?', ['She is sick','She has research to finish','She dislikes Peruvian food','She is traveling abroad'],1,'She says she has to research Peru for a story.'),
 ('What does Bruna mean when she says Anna can visit Peru?', ['Book a flight tomorrow','Attend a festival at the museum','Read an article online','Meet a Peruvian politician'],1,'Bruna refers to a museum festival rather than an international trip.'),
 ('Which activity does Bruna recommend at the festival?', ['Watch the dancers','Attend a basketball game','Visit an airport','Go shopping'],0,'Bruna suggests that they watch the traditional dance.'),
 ('Why does Anna mention getting married?', ['She is engaged to Bruna','She misunderstands what the dance means','She is interviewing a wedding planner','She forgot her deadline'],1,'She mistakenly thinks trying the dance implies marriage.'),
 ('What does Anna decide to check out while Bruna works?', ['The art','An old library','The subway','A job interview'],0,'Anna says she will check out the art.'),
 ]
}
]

def main():
    result=[]
    for item in LESSONS:
        item=dict(item)
        transcript=parse(item.pop('raw'))
        questions=[]
        for question,options,answer,explanation in item.pop('questions'):
            questions.append({'question':question,'options':options,'answer':answer,'explanation':explanation})
        item.update({
            'attribution':'Voice of America (VOA Learning English)',
            'sourceSeries':"Let's Learn English — Level 2",
            'sourceLicense':'VOA-original public domain, attribution requested; excludes third-party elements',
            'rightsUrl':'https://learningenglish.voanews.com/p/6861.html',
            'audioProvider':'VOA Learning English',
            'audioType':'human_dialogue_source',
            'audioAvailability':'external_online_stream_only',
            'offlineReady':False,
            'transcriptSource':'Publisher-provided VOA transcript',
            'transcriptVerifiedAgainstAudio':False,
            'timingVerified':False,
            'quality':'external_source_not_independently_audio_reviewed',
            'turns':transcript,
            'questions':questions,
        })
        result.append(item)
    output=ROOT/'data/authentic-listening.json'
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {len(result)} VOA lessons, {sum(len(x["questions"]) for x in result)} original comprehension questions, {sum(len(x["turns"]) for x in result)} transcript turns -> {output}')
if __name__=='__main__':main()
