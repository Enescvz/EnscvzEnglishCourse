#!/usr/bin/env python3
"""Build independently authored quizzes grounded in reviewed VOA Conversation pages.

Publisher audio/transcript stays on VOA's site. This is intentionally NOT
an imported audio/transcript lesson. Repeatable, no external network required.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'data/voa-source-catalog.json'
OUT=ROOT/'data/voa-source-quizzes.json'

# Each row: source catalog number, source-grounded question tuples.
# (question, correct option, incorrect options, explanation citing the actual source event)
ITEMS={
3:[
('Why are Anna and Pete meeting Kelly?', 'To get advice about a new show', 'To buy a new car','To plan a circus performance','To book a hotel','Kelly is the consultant for their new show.'),
('How late does Kelly say they are?','43 minutes','5 minutes','15 minutes','Two hours','Kelly says they arrived exactly 43 minutes late.'),
('What does Anna blame Pete for?','Stopping for special coffee','Missing the train','Forgetting the meeting room','Buying cinema tickets','Anna says Pete made a stop for coffee.'),
('According to Pete, what made their commute worse?','A scooter ride and a stop to feed birds','Heavy snowfall','A broken subway train','A flat tire','Pete describes the scooter and feeding birds as delays.'),
],
4:[
('What do Anna and Pete mainly disagree about?','Whether circus performers are artists','Whether the weather is good','Whether the tent is too small','Whether they should buy tickets','The discussion is about circus arts.'),
('How does Pete primarily view circus performers?','Athletes with impressive skills','Actors in a movie','Restaurant workers','Musicians in a band','Pete argues they are athletic rather than artistic.'),
('What example does Anna use to defend her point?','Trapeze artists','Fashion designers','Soccer referees','Travel agents','Anna calls attention to trapeze artists.'),
('What do both speakers finally acknowledge?','The performers are athletic and amazing','The show should be canceled','Art must be painted','Circus skills are easy','They agree on the performers’ athletic abilities.'),
],
5:[
('Where does Anna imagine taking a vacation at first?','On a beach','At a ski resort','On a cruise ship','At a busy office','Anna imagines relaxing at the beach.'),
('Why does Anna reject the mountain getaway?','She is afraid of heights','She dislikes swimming','She cannot drive','She has no passport','Anna tells Dan that she fears high places.'),
('What kind of holiday does Dan offer after the mountain trip?','A deep-sea adventure','A cooking workshop','A city bus tour','A family reunion','Dan moves on to the Deep Sea Adventure.'),
('Where would the Safari Camp Out guests sleep?','Outdoors under the stars','Inside an airplane','In a subway station','On a houseboat','Dan describes sleeping under the stars on safari.'),
],
6:[
('Why does Anna take Penelope on a tour?','Penelope is new to Washington, D.C.','Penelope is a tour guide','Anna needs to buy a car','Penelope is moving abroad tomorrow','Anna says her friend is new to town.'),
('What is special about the DC Ducks vehicle?','It travels on roads and in water','It can fly over buildings','It only runs on rails','It is pulled by horses','The vehicle is a boat with wheels.'),
('What did the amphibious vehicle originally help transport?','People and supplies during World War II','Only circus performers','Coal from a mine','Visitors to a museum','Penelope reads that it carried people and supplies in World War II.'),
('Which monument does Anna point out on their left?','The Washington Monument','The Statue of Liberty','The Golden Gate Bridge','Mount Rushmore','Anna identifies the Washington Monument on the left.'),
],
7:[
('What unusual mistake does the young guide mention?','A word carved incorrectly at the Lincoln Memorial','The wrong date on a train ticket','A missing car key','An incorrect restaurant menu','He points out an old carving mistake at the memorial.'),
('Which experience especially excites Anna during the river crossing?','Going under a bridge by boat','Riding a bicycle through a tunnel','Flying a helicopter','Walking across the bridge','Anna enjoys going underneath the bridge.'),
('Why were tunnels built beneath the U.S. Capitol, according to the guide?','To avoid walking outside in bad weather','To store museum paintings','To hide pirate treasure','To carry riverboats','The boy says lawmakers wanted shelter from bad weather.'),
('What is unusual about their sightseeing vehicle?','It both drives and sails','It is completely solar-powered','It flies','It is pulled by a train','Penelope is surprised it can drive out of the water.'),
],
8:[
('Why does Anna talk to Kelly at the start?','She wants advice about a recent project','She wants Kelly to repair a car','She needs a new passport','She is looking for a lost dog','Anna asks Kelly for advice about her project.'),
('What event was Anna assigned to cover?','A large barbecue food festival','A fashion show','A baseball game','A science convention','Kelly refers to Anna’s coverage of a barbecue festival.'),
('How do barbecue chefs treat their sauce recipes?','They often keep ingredients secret','They publish every recipe','They never use spices','They all use identical sauces','The chefs refuse to reveal their secret ingredients.'),
('Which combination is mentioned as common in barbecue sauce?','Tomato sauce, vinegar and spices','Chocolate, milk and rice','Tea, lemon and honey','Butter, sugar and flour','Anna lists tomato sauce, vinegar and spices.'),
],
9:[
('Where did Anna spend part of her weekend?','At the D.C. State Fair','At an airport','At a basketball tournament','At a concert hall','Anna tells Ashley she attended the state fair.'),
('What did Anna use as her unusual pet?','A pet rock','A goldfish','A pet lizard','A hamster','She entered a rock she had kept since childhood.'),
('Which contest did Anna win?','One-of-a-Kind Pet','Best Trained Dog','Fastest Runner','Best Costume Designer','Anna explains that her rock won the unusual pet competition.'),
('What is Ashley’s dog called?','Dublin','Romeo','Buster','Sherlock','Ashley introduces her dog as Dublin.'),
],
11:[
('What kind of weather event did Anna report on?','A blizzard','A tornado in Florida','A heat wave','A drought','Anna recalls reporting on a blizzard.'),
('Who did Anna recruit to help her report?','Pete','Dan','Bruna','Caroline','Anna says she volunteered Pete to help.'),
('Which supplies did Anna prepare for the storm?','Food, blankets and warm clothes','Swimming goggles and sunscreen','Paint and brushes','Movie tickets and popcorn','Anna carries emergency supplies for the snowstorm.'),
('What could Anna’s weather software display in real time?','Temperature, wind and snowfall','Airport ticket prices','Restaurant ratings','Traffic fines','She lists temperature, wind speed, wind direction and snowfall.'),
],
12:[
('What does Kaveh advise Anna to do when a bee comes near?','Ignore it so it flies away','Swat it immediately','Throw water at it','Catch it in a cup','Kaveh advises ignoring the bee rather than swatting it.'),
('What does Kaveh warn could happen if Anna swats the bee?','It might sting her','It will disappear instantly','It will become a butterfly','It will stop flying forever','He warns that swatting could provoke a sting.'),
('Who does Kaveh suggest Anna contact?','Caroline, a beekeeper and educator','A car mechanic','A television producer','A travel agent','Kaveh recommends his beekeeper friend Caroline.'),
('Roughly how many bees does Caroline say are in each hive?','30,000','300','3,000','300,000','Caroline says there are about thirty thousand bees per hive.'),
],
13:[
('What does Caroline use to help keep bees calm?','A smoker','A loud whistle','A flashlight','A vacuum cleaner','Caroline explains how smoke can calm the bees.'),
('What is one main role of the queen bee?','Laying eggs','Driving the bees to flowers','Making protective clothing','Guarding a car','Caroline identifies egg laying as the queen’s job.'),
('What do worker bees bring back to the hive?','Nectar and pollen','Leaves and stones','Salt and pepper','Seeds and wood','Worker bees gather nectar and pollen from flowers.'),
('How can Anna help support bees?','Plant flowers native to the area','Remove all flowers from gardens','Paint the hives black','Feed bees candy','Caroline recommends planting native flowers.'),
],
14:[
('What similarity does Pete share with his girlfriend?','Neither of them can whistle','They both play baseball professionally','They both hate movies','They both own boats','Pete mentions that neither partner can whistle.'),
('What does Anna invent to impress her friends?','An imaginary boyfriend','A new television channel','An exotic vacation','A pet shop','Anna pretends she has a boyfriend.'),
('What name does Anna give this invented boyfriend?','Buster Carter','Hank Weaver','Dublin Jones','Alaskan Albert','She improvises the name Buster Carter.'),
('What excuse does Anna give for not bringing him to dinner?','He is busy with a squirrel collection','He missed a flight','He cannot find his car','He is working at the fair','She claims he is occupied with a squirrel collection.'),
],
15:[
('What sport are Anna and Penelope doing together?','Speed walking','Swimming','Ice skating','Rock climbing','Both friends are speed walking.'),
('Since what time do they say they have been walking?','8 a.m.','Noon','6 p.m.','Midnight','Anna says they have been speed walking since 8 a.m.'),
('What kind of trainer does Penelope suggest hiring?','A personal trainer','A driving instructor','A singing teacher','A swimming coach','Penelope suggests professional training.'),
('What does Alaskan Albert call his unusual workout?','Call of the Wild Parkour','The Lazy River Walk','Weekend Yoga Club','The Office Stretch','He says he combined wilderness training and city exercise into parkour.'),
],
16:[
('What is Anna searching for at work?','Her lost key','A passport','A phone charger','A parking ticket','Anna tells Kaveh she lost her key.'),
('Where has the Lost & Found office moved?','To the basement near the elevators','To the cafeteria entrance','To the rooftop','Outside the building','Kaveh describes its new basement location.'),
('Why does Serenity misunderstand Anna’s request?','She thinks Anna needs a symbolic key to happiness','She believes Anna wants a new apartment','She thinks Anna is buying a car','She mistakes Anna for a reporter','Serenity treats the missing key as a personal happiness problem.'),
('What activity does Anna remember doing with her family as a child?','Singing','Rock climbing','Sailing','Cooking barbecue','Anna says she used to sing with her family.'),
],
17:[
('What new topic does Ms. Weaver assign to Anna and Pete?','The experiences of single parents','The history of cars','Weather forecasting','Barbecue festivals','The assignment is a show about raising children alone.'),
('What objects serve as practice babies?','Bags of flour','Toy robots','Water bottles','Basketballs','Ms. Weaver hands out bags of flour as babies.'),
('For how many days must they care for the flour babies?','Six days','Two days','Two weeks','One month','Ms. Weaver specifies the next six days.'),
('What is the promised reward for the better research?','An extra day of vacation','A new computer','A cash prize','A travel ticket','The best research receives an extra vacation day.'),
],
18:[
('Who presents a large research binder?','Pete','Kaveh','Bruna','Penelope','Pete hands Ms. Weaver a heavy binder.'),
('Why does Anna look so exhausted?','She cared for her flour baby around the clock','She took an overnight flight','She worked at a barbecue restaurant','She climbed a mountain','Anna says she fed the flour baby every three hours and barely slept.'),
('How did Anna accidentally set her flour baby on fire?','She used a microwave to dry it','She left it next to a campfire','She dropped it into a volcano','She put it in a hot car','She dried her wet flour baby in a microwave.'),
('Why does Ms. Weaver praise Anna despite the messy result?','Anna followed the care instructions','Anna wrote the longest report','Anna bought the biggest stroller','Anna arrived first','Ms. Weaver values Anna’s compliance with the instructions.'),
],
19:[
('What does Pete want during the movie?','A quiet theater experience','A longer commercial break','More popcorn flavors','A seat near the exit','Pete wants Anna and others to stay quiet.'),
('What language strategy does the lesson emphasize?','Polite indirect questions','Reported speech only','Future perfect tense','Conditional type two only','The professor discusses indirect questions as polite requests.'),
('What does Anna drink noisily?','A thick milkshake','Hot coffee','A glass of lemonade','A can of soup','Her loud milkshake drinking bothers Pete.'),
('What happens to Anna’s phone after it rings?','She drops it beneath a seat','She throws it outside','She lends it to Pete','She leaves it in a taxi','Anna drops the ringing phone and has to find it.'),
],
20:[
('Where are Anna and Penelope filming a story?','The Washington Car Show','A train station','A circus festival','A library','Their assignment is to cover the car show.'),
('What did Ms. Weaver ask them to do?','Show cars, interview people and have fun','Avoid talking to anyone','Only film one robot','Buy the most expensive car','Anna recalls the instructions from their boss.'),
('What does Anna do to entertain a robot?','She performs a robot dance','She sings a lullaby','She paints a portrait','She performs a magic trick','Anna dances in front of Hank the Robot.'),
('Who actually drives during the Jaguar test drive?','A stunt driver named Kurt','Anna alone','Ms. Weaver','Pete','The transcript identifies Kurt as the stunt driver.'),
],
}


def question(data,seed):
    ask,correct,wrong1,wrong2,wrong3,explanation=data
    # Rotate the correct choice to avoid position bias; all four remain unique.
    pos=seed%4
    others=iter((wrong1,wrong2,wrong3))
    options=[correct if i==pos else next(others) for i in range(4)]
    assert len(set(options))==4
    return {'question':ask,'options':options,'answer':pos,'explanation':explanation,'sourceEvidence':'VOA publisher Conversation transcript (see linked original)'}


def build():
    catalog=json.loads(CAT.read_text(encoding='utf-8'))
    by_id={x['id']:x for x in catalog}
    quizzes=[]
    for no,rows in ITEMS.items():
        source=by_id[f'voa-2-{no:02d}']
        assert not source['transcriptImported'],source['id']
        item={'id':f'voa-linked-2-{no:02d}', 'catalogId':source['id'],
              'title':source['title'],'level':'B1–B2','topic':source['topic'],
              'sourceUrl':source['sourceUrl'],'attribution':'VOA Learning English',
              'audioAvailability':'publisher_external_only','transcriptAvailability':'publisher_external_only',
              'audioBundled':False,'transcriptImported':False,'playerVerified':False,
              'questions':[question(row,no+i) for i,row in enumerate(rows)]}
        quizzes.append(item)
        source.update({'linkedQuizId':item['id'],'questionCount':len(item['questions']),
                       'integrationStatus':'source_linked_quiz',
                       'audioPlayback':'Open publisher page to hear; external playback not verified'})
    OUT.write_text(json.dumps(quizzes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    CAT.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'publisherTranscriptsCopied':0,'fullyImportedLessons':3,'linkedSourceQuizzes':len(quizzes),'newQuestions':sum(len(x['questions']) for x in quizzes),'totalQuizEnabled':len(quizzes)+3},indent=2))

if __name__=='__main__': build()
