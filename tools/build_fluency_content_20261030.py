"""Original, independently unreviewed content for private AEL fluency pilot."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# 12 real-life situations with 3 independently authored decisions and feedback.
scenarios=[
('hotel','Hotel check-in','Hotel','Good evening. Do you have a reservation?',[
 ('Say you booked a room for tonight.','Yes, I have a reservation for tonight.','Yes, I am having a reserve tonight.','I reserve for last night.','The present simple describes an existing booking.'),
 ('Ask when breakfast starts.','What time does breakfast start?','What time breakfast starts?','When the breakfast will starting?','Use does before the subject in a present simple question.'),
 ('Ask politely if you may leave luggage after checkout.','Could I leave my luggage here after checking out?','Can I leaving my luggage here tomorrow?','Could leave I my bag?','Could I + base verb is a polite request.')]),
('cafe','At the café','Cafe','Hi! Are you ready to order?',[
 ('Order a latte politely.','Could I have a latte, please?','Give me latte right now.','I am have a latte.','Could I have ... is a natural polite request.'),
 ('Ask whether oat milk is available.','Do you have oat milk?','You have oat milk?','Are there oat milk?','Do you have ... asks if the shop offers something.'),
 ('Ask for the check.','Could we have the check, please?','Please give the account.','Can we receiving the bill?','Check is common US English in a restaurant.')]),
('airport','At the airport','Travel','May I see your boarding pass?',[
 ('Explain that your pass is on your phone.','It is on my phone.','It is in my telephone inside.','I have it in phone me.','On my phone is an idiomatic location phrase.'),
 ('Ask where your gate is.','Could you tell me where my gate is?','Could you tell me where is my gate?','Tell me where my gate?','Indirect questions keep normal subject–verb order.'),
 ('Ask whether the flight is delayed.','Is the flight delayed?','Does the flight delayed?','Is delayed the flight?','Be + subject + adjective/past participle.')]),
('directions','Finding your way','City','Excuse me, are you looking for something?',[
 ('Ask how to get to the subway.','How can I get to the subway station?','How I can get to subway?','How getting to the subway?','Use can before the subject.'),
 ('Ask how long the walk takes.','How long does it take to walk there?','How long it take to walk?','How much time it taking for walk?','How long does it take ... is common for duration.'),
 ('Check that you understood the directions.','So I turn left at the next street, right?','So I will left from next street?','I am taking left, no?','A confirmation question can check understanding.')]),
('neighbors','Meeting a neighbor','Social','Hi, I just moved into this building.',[
 ('Welcome your neighbor.','Welcome to the building!','Welcome in this building!','I will welcoming you.','Welcome to + place.'),
 ('Ask how they like the neighborhood.','How do you like the neighborhood so far?','How you like neighborhood?','Are you liking the area until now?','How do you like ... so far? is a natural question.'),
 ('Offer to help if they need anything.','Let me know if you need anything.','Tell to me if you need something.','You should needing me.','Let me know if ... is a natural offer.')]),
('appointment','Rescheduling an appointment','Daily life','Hello, how can I help you today?',[
 ('Say you need to change your appointment.','I need to reschedule my appointment.','I need change appointment me.','I am need to switch an appoint.','Reschedule is natural for changing a booked time.'),
 ('Ask about available times on Friday.','Do you have any openings on Friday?','You having free hours Friday?','Has you an opening Friday?','Any openings asks about appointment availability.'),
 ('Thank the person for accommodating you.','Thanks for being flexible.','Thanks because flexible you.','Thanking for your flexibility being.','Thanks for + noun or -ing form.')]),
('shopping','Returning an item','Shopping','Hello, what can I do for you?',[
 ('Explain that the item does not work.','I bought this yesterday, but it does not work.','I buy this yesterday and not working.','It did not worked yesterday.','Use bought for a past purchase and does not work for current status.'),
 ('Ask about the return policy.','What is your return policy?','What your return politics?','Which is return police?','Return policy is the store rule about returns.'),
 ('Ask whether you can exchange it.','Could I exchange it for another one?','Can I changing it for other?','Could exchange I this?','Could I + base verb; exchange for another item.')]),
('friend','Making weekend plans','Friends','Do you have plans this weekend?',[
 ('Say you are free on Saturday.','I am free on Saturday afternoon.','I am free in Saturday afternoon.','I will free by Saturday.','On + day; in + part of day without a named day.'),
 ('Suggest trying a new place.','Why don’t we try that new restaurant?','Why we don’t try new restaurant?','Why no try to restaurant?','Why don’t we + base verb suggests a plan.'),
 ('Ask what time works best.','What time works best for you?','What time to you is best working?','How time works good you?','What time works best for you? is natural.')]),
('smalltalk','Starting a conversation','Social','That is a nice book. What are you reading?',[
 ('Say what kind of book it is.','It is a mystery novel.','It is mystery book novel.','That has mystery novel.','It is + a + singular countable noun.'),
 ('Ask what books the other person likes.','What kind of books do you enjoy?','What kind books you enjoy?','What you enjoys reading books?','What kind of + plural noun; do you + base verb.'),
 ('Ask for a recommendation.','Could you recommend something similar?','Do you recommendation same thing?','Would you recommend me similar?','Recommend + object is natural here.')]),
('delivery','Calling customer support','Services','Thanks for calling. What seems to be the problem?',[
 ('Explain the package has not arrived.','My package has not arrived yet.','My package did not arrived yet.','My package no arrived already.','Present perfect is natural when it has not arrived up to now.'),
 ('Ask when it will arrive.','Do you know when it will arrive?','Do you know when will it arrive?','When it will arrive you know?','Use statement word order inside indirect questions.'),
 ('Ask for a tracking number.','Could you give me the tracking number?','Could you giving tracking numbers?','Give tracking I number.','Could you + base verb.')]),
('health','At the pharmacy','Daily life','Hello. What are you looking for?',[
 ('Ask where the sunscreen is.','Where can I find sunscreen?','Where I can find the sunscreen?','Where finding sunscreen me?','Where can I + base verb.'),
 ('Ask about the price.','How much does this cost?','How much this costs?','How many cost this?','How much + does + singular subject + base verb.'),
 ('Ask if there is a smaller size.','Do you have a smaller size?','Has you smaller size?','Are you have little size?','Do you have ... is a common shopping question.')]),
('school','Asking a classmate','Study','Hi! Did you understand today’s lesson?',[
 ('Admit that you missed one part.','I understood most of it, but I missed the last part.','I understanded all but missed last.','I am missing the last part yesterday.','Past tense: understood, missed.'),
 ('Ask for an explanation.','Could you explain that part again?','Can you explanation that piece?','Could you explaining that?','Explain is a verb: could you explain ...'),
 ('Ask to study together.','Would you like to study together tomorrow?','Would you liking study together?','You like study together tomorrow?','Would you like to + base verb.')])]
scenario_rows=[]
for sid,title,topic,opening,turns in scenarios:
 steps=[]
 for i,(task,good,bad1,bad2,explanation) in enumerate(turns):
  # fixed shuffled answer positions, preserving authored distractors
  variants=[good,bad1,bad2]; shift=(i+len(sid))%3
  options=variants[shift:]+variants[:shift]
  steps.append({'id':f'rl-{sid}-{i+1}','task':task,'reply':('Thanks. Let me check.' if i==0 else 'That makes sense.' if i==1 else 'Absolutely. Have a great day!'),'options':options,'correct':options.index(good),'explanation':explanation})
 scenario_rows.append({'id':'rl-'+sid,'title':title,'topic':topic,'opening':opening,'steps':steps,'editorApproved':False})
# Original short prompts that do not require Turkish-to-English translation.
think_situations=[
('decline','Politely decline a dinner invitation and give one reason.','Thanks for inviting me, but I already have plans that evening.','polite refusal'),
('clarify','You did not understand a direction. Ask for clarification.','Could you explain which street I should turn onto?','clarifying questions'),
('followup','A friend is starting a new course. Ask a thoughtful follow-up question.','What made you choose that course?','follow-up question'),
('opinion','Give your opinion about working from home, with one reason.','I think working from home can be helpful because it saves commuting time.','supporting opinions'),
('compare','Compare taking the train with driving for a weekend trip.','The train is often more relaxing, whereas driving gives you more flexibility.','comparison'),
('apologize','Apologize for being late and explain briefly.','I am sorry I am late. The bus was delayed.','apology'),
('reschedule','Ask to move a meeting to next Monday.','Would it be possible to move our meeting to next Monday?','polite request'),
('hypothetical','Ask what someone would do if they had a free month.','What would you do if you had a whole month off?','hypothetical question'),
('contrast','Say that something was expensive but worth buying.','Although it was expensive, I think it was worth buying.','contrast'),
('reason','Explain why you decided to learn a new skill.','I decided to learn a new skill because I want to challenge myself.','giving reasons'),
('detail','Ask someone for details about their weekend plans.','What are you planning to do on Saturday afternoon?','detail questions'),
('uncertainty','Say you are not certain, then suggest how to check.','I am not sure, but we could check the official website.','expressing uncertainty'),
('recommend','Recommend a quiet place to read.','I would recommend the library because it is usually peaceful.','recommendation'),
('agree','Agree with a proposal and add a benefit.','That sounds reasonable, and it could also save us time.','agreement'),
('disagree','Disagree politely with an idea and explain why.','I see your point, but I think we need more information.','polite disagreement'),
('condition','Say that you will join a trip if the weather is good.','I will join you as long as the weather is good.','conditional'),
('request','Ask a classmate to send you the notes.','Could you send me your notes when you have a moment?','request'),
('check','Check whether you understood someone correctly.','Do you mean that we should arrive before nine?','confirmation'),
('preference','Explain why you prefer studying in the morning.','I prefer studying in the morning because I can concentrate better.','preferences'),
('past','Tell someone about a small unexpected event yesterday.','Yesterday I missed my bus, so I walked to the station.','past narration'),
('future','Describe a plan for learning English next month.','Next month I am going to practice listening every morning.','future plans'),
('questiontag','Use a question tag to check a plan.','We are meeting at seven, aren’t we?','question tag'),
('indirect','Ask politely where the nearest pharmacy is.','Could you tell me where the nearest pharmacy is?','indirect question'),
('suggest','Suggest an alternative when a restaurant is full.','We could try the café across the street instead.','suggestions'),
]
think=[{'id':'think-'+k,'task':p,'modelAnswer':m,'focus':f,'editorApproved':False} for k,p,m,f in think_situations]
writing=[
('email','Write a polite email to reschedule a meeting.','Explain the conflict, suggest two possible times, and end politely.',90,180),
('complaint','Write to customer service about a delayed order.','Give the order context, explain the issue, and request a specific solution.',90,180),
('opinion','Should students have homework every day?','Give an opinion, two reasons, one example, and a conclusion.',120,220),
('reflection','Describe something you learned from a mistake.','Describe what happened, the result, and what you would do differently.',110,200),
('compare','Compare online and face-to-face courses.','Compare their advantages and disadvantages and explain your preference.',130,230),
('invitation','Invite a friend to an event.','Include when, where, why it could be fun, and how to respond.',70,130),
('discussion','Does technology always save time?','Consider at least one counterargument before your conclusion.',130,230),
('review','Write a short review of a café you visited.','Describe atmosphere, service, value, and whether you recommend it.',100,180),
('proposal','Suggest an improvement to a local park.','Describe a problem, propose a solution, and explain a benefit.',120,220),
('travel','Explain how you would plan a three-day city trip.','Include priorities, transport options, and a backup plan.',120,220),
('apology','Write an email apologizing for missing a deadline.','Take responsibility, explain briefly, and suggest a concrete next step.',100,180),
('story','Tell a story about meeting someone unexpectedly.','Include background, a turning point, and an ending.',130,230)
]
writing=[{'id':'write-'+k,'title':t,'instructions':desc,'minWords':mn,'maxWords':mx,'editorApproved':False} for k,t,desc,mn,mx in writing]
result={'meta':{'version':1,'language':'en-US','independentEditorApproved':False,'license':'Original authored pilot prompts; VOA human-source streams and publisher transcripts are not bundled here.','audioBundled':False,'autoEssayScoring':False,'speakingModuleChanged':False},'realLife':scenario_rows,'thinking':think,'writing':writing}
(ROOT/'data/fluency-studio.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(len(scenario_rows),'scenarios',sum(len(x['steps']) for x in scenario_rows),'decisions',len(think),'thinking prompts',len(writing),'writing prompts')
