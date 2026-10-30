#!/usr/bin/env python3
"""Manually source-checked VOA lesson 21-30 quiz additions.
Publisher pages were reviewed 2026-10-28. Only new questions/explanations are stored,
not publisher transcript or downloaded sound. Safe to re-run (stable IDs).
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAT=ROOT/'data/voa-source-catalog.json'
QUIZ=ROOT/'data/voa-source-quizzes.json'
# Question, correct answer, three clearly wrong alternatives, supporting explanation
BANK={
21:[
('What secret did Pete ask Anna to keep?','His upcoming birthday',['A new job offer','An office relocation','A planned wedding'],'Pete told Anna not to tell anyone about his upcoming birthday.'),
('Where does Ashley suggest finding a unique gift?','Tanglewood Works',['The airport gift shop','The museum café','A supermarket'],'Ashley recommends Tanglewood Works when Anna asks about a unique present.'),
('Why does Anna decide to buy a gift anyway?','She wants to celebrate Pete despite his attitude',['Pete explicitly asks for a gift','The boss orders a party','Ashley offers to pay'],'Anna says she does not care that Pete seems to dislike presents and fun.'),
('What unusual birthday surprise does Anna suggest?','Renting a clown',['Hiring a tour guide','Going fishing','Booking a cooking class'],'Anna says she might rent Pete a clown; Ashley jokes Pete would never speak to her again.')],
22:[
('Which item does Anna bring to the upcycling class?','A broken toy',['An antique watch','A brand-new guitar','A glass vase'],'Sue examines Anna’s broken toy along with other discarded objects.'),
('What does Anna imagine her objects are doing?','Talking to her',['Growing larger','Predicting the weather','Playing recorded music'],'Anna describes the net, helmet and toy as speaking to her.'),
('How does Sue describe most of Anna’s collected objects?','Garbage rather than treasure',['Rare antiques','Unopened gifts','Expensive art supplies'],'Sue says these particular objects are garbage, even though some trash can be reused.'),
('What should Anna bring to the following class?','A clean shoe box',['An old suitcase','A bicycle helmet','A bag of birdseed'],'Sue asks Anna to bring a clean shoe box for the next craft lesson.')],
23:[
('Whom is Anna scheduled to interview?','The musician Emma G',['Her sister in Chicago','A famous scientist','A basketball coach'],'Ms. Weaver assigns Anna an interview with musician Emma G.'),
('What gift does Anna show Emma G during the interview?','A scrapbook video with edited photos',['A concert ticket','A homemade cake','A signed book'],'Anna says she inserted herself into photos of Emma G and assembled a video scrapbook.'),
('Where will Emma G perform in early June?','Austin, Texas',['Miami, Florida','Denver, Colorado','Seattle, Washington'],'Emma G describes several performances in Austin in early June.'),
('What will Emma G be doing in Chicago in mid-July?','Teaching at a music camp',['Working in a hospital','Attending a robotics exhibition','Filming a cooking show'],'Emma G says she will teach at a music camp in Chicago in mid-July.')],
24:[
('Where does Anna plan to go that evening?','A superhero convention',['A job interview','A theater audition','An animal shelter'],'Anna says she is going to the large superhero convention that night.'),
('What kind of superhero origin does the young man prefer?','Being born with superpowers',['Learning powers at school','Finding an ancient map','Winning a science competition'],'The young man says he would rather be born a superhero.'),
('What unexpectedly happens to Anna?','She is struck by lightning',['She falls into a pool','She loses her train ticket','She breaks her phone'],'After the conversation, Anna is struck by lightning and believes she has powers.'),
('What does “you’d better” mainly express in this lesson?','Strong, informal advice',['A completed past action','An impossible wish','A polite request for permission'],'The grammar explanation treats “had better” as strong, informal advice.')],
25:[
('Which power does Lightning Bolt Lady initially fail to demonstrate?','Walking through walls',['Learning a new language','Reading a newspaper','Playing the piano'],'The announcer describes several failed powers, including an attempt to walk through walls.'),
('What unusual form of speed does she discover?','Super-speed walking',['Supersonic swimming','Fast flying','Instant teleportation'],'After reading about lightning, she tries fast walking and calls it a power.'),
('What happens when she tries to charge a stranger’s phone?','The phone turns to ashes',['The phone gets a new screen','The phone starts playing music','The phone becomes waterproof'],'The lightning destroys the phone; she compensates the woman with money.'),
('Which tense does the announcer explain?','Past perfect continuous',['Present perfect simple','Future passive','Second conditional'],'The presenter explains past perfect continuous using had been plus an -ing verb.')],
26:[
('What claim in the article interests Anna?','Someone in the world may look exactly like you',['Everyone has the same job','People never change their appearance','Photos are always misleading'],'Anna reads an article claiming that each person may have a look-alike.'),
('Who says he met a woman who looks like Anna?','Pete',['Jonathan','Ms. Weaver','Ashley'],'Pete tells Anna he encountered a woman at work who resembles her.'),
('What kind of job does Pete think the look-alike has?','Career consultant',['Train conductor','Veterinarian','Restaurant manager'],'Pete thinks the woman he met works as a career consultant.'),
('How does Anna first respond to Pete’s negative opinion of the woman?','She says they should give the newcomer a chance',['She cancels her plans','She immediately calls the police','She decides to move away'],'Anna suggests the woman may just be new and deserves a chance.')],
27:[
('Why does Anna refuse Ms. Weaver’s dinner invitation?','She already plans to visit a friend’s houseboat',['She is ill','She has an exam','She dislikes seafood'],'Anna explains that she already has plans to visit her friend’s houseboat.'),
('Who offers to give Anna a tour of the houseboat?','Phoenix',['Professor Bot','Pete','Jonathan'],'Fanny asks her son Phoenix to show Anna around the houseboat.'),
('What did the houseboat family have to do when moving from a three-story home?','Downsize their possessions',['Build a larger garage','Hire a gardener','Buy a second car'],'Phoenix explains that they downsized significantly after moving from a three-story house.'),
('Why can’t Phoenix stop the houseboat from rocking?','It is floating on water',['The engine is broken','Someone is jumping on it','The boat has no windows'],'Phoenix points out that a floating houseboat naturally moves with the water.')],
28:[
('What event are Kelly and Anna taking part in?','A city bird count',['A marathon','A cooking competition','A music festival'],'They have joined the Great City Bird Count and are supposed to record birds.'),
('What does Anna put on her map instead of birds?','Ten ice cream trucks',['Fire stations','Taxi stands','Bookshops'],'Anna has located ten ice cream trucks in an area of five blocks.'),
('What does Kelly expect Anna to complete?','The official bird-watching form',['A job application','A health questionnaire','A hotel reservation'],'Kelly reminds Anna to record her bird observations on the official form.'),
('Why does Anna suspect the suited man is a spy?','He leaves a briefcase at an ice cream truck',['He talks to a bird','He loses his wallet','He buys a train ticket'],'Anna invents a spy story after seeing the suited man leave his briefcase.')],
29:[
('What new responsibility has Ms. Weaver given Anna?','Fire safety monitor',['Travel coordinator','Sports coach','Office accountant'],'Anna says Ms. Weaver named her the workplace fire safety monitor.'),
('How often should the fire alarm be tested according to the firefighters?','Every month',['Every five years','Only after a fire','Once a decade'],'The firefighters advise testing the alarm monthly and checking its batteries.'),
('During a fire, which route should you use rather than an elevator?','The stairs',['A freight elevator','A storage tunnel','A window ledge'],'The firefighters clearly advise using the stairs rather than an elevator.'),
('Why do the firefighters tell Anna to stay low?','Air near the ground is clearer beneath rising smoke',['It keeps clothing clean','It makes the alarm louder','It protects against rain'],'Because smoke rises, the air closer to the floor may be clearer.')],
30:[
('Why does Anna mistakenly think she is dying?','She overhears a nurse talking about someone else’s test',['She gets a parking ticket','She loses her luggage','She receives a wrong email'],'Anna hears the nurse say someone will not make it, but the call is about a student.'),
('What does the nurse actually mean by “not going to make it”?','A student might not graduate',['Anna will miss a flight','A dog is sick','A concert is canceled'],'The nurse was talking about a science student who might not graduate.'),
('What kind of job would Ashley love to do?','Train dogs',['Fly airplanes','Teach mathematics','Repair computers'],'Ashley says she would like to be a dog trainer and has taught Dublin tricks.'),
('What competition would Jonathan like to win?','A world karaoke contest',['A swimming race','An art exhibition','A spelling bee'],'Jonathan tells Anna that winning the World Karaoke Contest is on his bucket list.')]
}

BANK1={
33:[
('Which sport does Anna want to explain?','Baseball',['Basketball','Ice hockey','Tennis'],'Anna uses the baseball field to explain America’s sport to children.'),
('Who helps Anna travel to the correct location?','MINDY',['Marsha','Pete','Dr. Jill'],'MINDY is the computer that finally sends Anna to a baseball field.'),
('What three basic items does Anna say are needed for baseball?','A bat, a ball and a glove',['A net, a racket and a shuttlecock','A helmet, skates and a stick','A rope, a whistle and a flag'],'Anna lists a bat, ball and glove as the basic equipment.'),
('How many innings are in the baseball game Anna describes?','Nine',['Three','Five','Twelve'],'Anna says the game normally has nine innings.')],
34:[
('Why does Anna ask Genie for help?','She needs a Halloween costume',['She missed her train','Her car has broken down','She needs a flight ticket'],'Anna is unsure whether to attend a Halloween party because she has no costume.'),
('What kind of costume does Genie first suggest?','A genie',['A pirate','A pilot','A firefighter'],'Genie initially suggests that Anna dress as a genie.'),
('What subject is Rebecca studying in college?','Journalism',['Medicine','Engineering','Architecture'],'Rebecca tells Anna she is a college junior who studies journalism.'),
('Which costume does Anna finally choose?','A rock star',['A magician','A baseball player','A nurse'],'Genie gives Anna a rock-star costume after the mind-reading idea becomes stressful.')],
35:[
('Who is responsible for doing the shopping?','Anna',['Marsha','Jonathan','Pete'],'Anna explains that Marsha is cooking while Anna shops for ingredients.'),
('Why is Marsha unhappy with the groceries?','Anna bought items from the breakfast list',['The shop closed early','All the food had expired','Anna forgot her wallet'],'Marsha discovers Anna took the breakfast list, not the dinner list.'),
('Where had Marsha intended to leave the correct dinner list?','On the refrigerator',['Inside the oven','At the bus stop','On her desk at work'],'Marsha says the dinner shopping list was on the refrigerator, although it fell to the floor.'),
('How soon are their guests expected to arrive?','In thirty minutes',['In three hours','The next morning','In five minutes'],'Marsha says their guests are due in thirty minutes.')],
36:[
('Where did Anna put the flour?','Inside the refrigerator',['On the balcony','Under the bed','Inside the oven'],'Anna misinterprets the instruction to keep flour in a cool, dry place.'),
('Where did Anna store the eggs?','In a cabinet under the sink',['In the freezer','On top of the television','In the closet'],'Anna says she placed the eggs in a cabinet under the sink.'),
('What meal does Anna make from the available ingredients?','Peanut-butter-banana pancakes',['Spaghetti and meatballs','Vegetable soup','Grilled salmon'],'Anna adapts her plan and makes her favorite peanut-butter-banana pancakes.'),
('How does Marsha react after tasting the meal?','She admits it tastes good',['She refuses to eat it','She immediately orders pizza','She throws it away'],'Marsha initially objects to breakfast for dinner but then likes the taste.')],
37:[
('What lost item does Anna return to Phil?','A travel bag',['A bicycle','A camera tripod','A passport wallet'],'Anna finds a bag and eventually gives it back to Phil.'),
('Where is Phil visiting from?','A small town in the countryside',['Another continent','A nearby island','A ship at sea'],'Phil says he comes from a small town and feels lost in Washington, D.C.'),
('Why does Anna prefer living in the city?','It has culture, entertainment and more job options',['It has no traffic','It has fewer buildings','It is always quieter'],'Anna values city museums, restaurants, theater, music and job opportunities.'),
('What does Anna suggest to make city people friendlier?','Say hello to more people',['Write complaints to the mayor','Move everyone to the countryside','Avoid meeting strangers'],'Anna and Phil decide to greet others in hopes that greetings spread.')]
}

BANK1.update({
38:[
('Who comes to Washington to visit Anna?','Penelope, a friend from her hometown',['Her college professor','A cousin from Texas','A former boss'],'Penelope is Anna’s old friend visiting from their shared hometown.'),
('How do Anna and Marsha handle their apartment rent?','They split it',['Anna pays all of it','Their employer pays it','They pay no rent'],'Anna tells Penelope that she and her roommate share the rent.'),
('Which children’s program does Anna work on?','The Time Traveling Treehouse',['The Ocean Detectives','The Daily Market','The Music News'],'Anna tells Penelope that she makes a children’s program called The Time Traveling Treehouse.'),
('Why does Penelope remember a treehouse?','They played in one together as children',['She designed a museum treehouse','She lost a book there','Her brother moved into one'],'Penelope remembers playing in the old treehouse behind her family’s home with Anna.')],
39:[
('What problem does Anna hope the advertised product will solve?','Untidy hair in windy weather',['A broken washing machine','A cold apartment','Loud traffic'],'Anna complains that the wind makes her hair untidy.'),
('Who promotes the Hair Be Good product?','Pete',['Penelope','Ms. Weaver','Jonathan'],'Pete appears in an advertisement for Hair Be Good.'),
('How much does one can of Hair Be Good cost?','Ten dollars',['Fifty dollars','Two dollars','One hundred dollars'],'The advertisement says one can of the product costs ten dollars.'),
('Why does Anna become angry with Pete?','The product makes her hair look worse',['He loses her luggage','He cancels their lunch','He forgets her birthday'],'Anna trusts the advertisement, but Amelia says the resulting hairstyle looks bad.')],
40:[
('Why does Anna visit the theater director?','To audition for a stage role',['To buy concert tickets','To repair the lighting','To interview a scientist'],'Anna’s New Year resolution is to act on stage, so she attends an audition.'),
('What does the director ask Anna to change about her first line?','Speak louder and more seriously',['Whisper more quietly','Sing the words','Speak in another language'],'The director says Anna is too soft and asks her to speak louder and more seriously.'),
('What timing mistake does Anna make during the final scene?','First too late, then too early',['She never says a word','She skips the audition','She reads a different play'],'Anna speaks too late on her first attempt and too early on the next.'),
('Which part does Anna eventually receive?','A tree',['The narrator','A princess','A firefighter'],'The director gives Anna a costume and she appears as a tree in the production.')],
41:[
('Why is Anna nervous at the start of the story?','Her boss is reviewing her work',['She has lost her phone','She is taking a driving test','She is late for a wedding'],'Anna says she is on her way to an annual work review.'),
('What is wrong with Ms. Weaver’s first chart?','It is upside down',['It shows the wrong television station','It has no labels','It is from another year'],'Anna notices the audience chart is upside down, reversing its apparent trend.'),
('What does Ms. Weaver want Anna to improve?','The size of the show’s audience',['The office parking','The building’s heating','The sports schedule'],'Ms. Weaver says the audience is big but not big enough and wants it to grow.'),
('What kind of pictures appear on Ms. Weaver’s motivational posters?','Cats',['Ocean waves','Old airplanes','Mountains'],'The motivational posters repeatedly feature cats.')],
42:[
('What is Anna doing when she first hears someone calling for help?','Leaving work to get lunch',['Driving to the airport','Shopping for groceries','Taking a school exam'],'Anna says she had left work to buy lunch when she heard the cries.'),
('What are the robbers trying to take?','A woman’s bag',['A bicycle','A car','A suitcase of books'],'The robbers grab the woman’s bag while she tries to resist with her umbrella.'),
('Why are the robbers removed from the bus?','They have not paid the fare',['They are traveling with a pet','They are on the wrong route','They are asleep'],'Anna explains that they were kicked off the bus because they did not pay.'),
('How does Anna say her arm is hurt?','Someone steps on it while she is on the ground',['She burns it while cooking','She hits it on a train door','She falls from a ladder'],'Anna explains that a passerby stepped on her arm while she was lying on the ground.')]
})

BANK1.update({
43:[
('Why can Anna not use the Metro to teach her class?','She has lost her wallet and Metro card',['The station is closed','She missed the last train','The lesson was canceled'],'Anna loses the wallet that contains her Metro card, credit card and money.'),
('Why can Marsha not come downtown to help?','She has a major presentation in one hour',['She is away on vacation','She is studying for an exam','She has no telephone'],'Marsha explains that she is busy preparing for a presentation.'),
('Why can Jonathan not lend Anna money?','He is at the airport with his mother',['He has lost his own wallet','He is fixing a car','He is giving a concert'],'Jonathan is at the airport; his mother’s flight is leaving soon.'),
('What prevents Ashley from coming to meet Anna?','She is babysitting',['She is in a dentist appointment','She is running a marathon','She is buying a new house'],'Ashley tells Anna that she is taking care of her niece.')],
44:[
('What two kinds of food does Anna argue with herself about?','Healthy food and junk food',['Fish and chicken','Breakfast and lunch','Tea and coffee'],'Anna describes two competing impulses: healthy foods and junk food.'),
('Which store does Ashley suggest Anna visit?','The Giant supermarket',['A pharmacy','An electronics store','A bookstore'],'Ashley directs Anna to the Giant supermarket to buy food.'),
('Which dessert does the junk-food side of Anna particularly want?','Ice cream',['Fruit salad','Plain yogurt','A baked potato'],'The character called Junky repeatedly argues in favor of ice cream.'),
('What healthy food does the other side prefer in the frozen aisle?','Frozen peas',['Chocolate cake','Donuts','Potato chips'],'Healthy suggests frozen peas while Junky wants ice cream.')],
45:[
('Who goes on a road trip with Anna?','Her roommate Marsha',['Pete','Her school teacher','A television producer'],'Anna explains that she and Marsha are on vacation at the same time.'),
('Which New York City landmark does Anna want to see?','The Statue of Liberty',['The Golden Gate Bridge','The Space Needle','Mount Rushmore'],'Anna includes the Statue of Liberty in her plans for New York City.'),
('Which natural landmark does Marsha want to visit?','The Grand Canyon',['Niagara Falls in Canada','Mount Fuji','The River Thames'],'Marsha explicitly adds the Grand Canyon to their desired stops.'),
('What does Anna want to see at an unusual roadside stop?','The world’s largest rocking chair',['A giant snow globe','An old rocket launch pad','A famous dinosaur skeleton'],'Anna’s additional roadside list includes the world’s largest rocking chair.')],
46:[
('What occasion does Anna almost forget?','Marsha’s birthday',['Her graduation','A holiday parade','A business conference'],'Marsha reminds Anna about the birthday celebration at 7 p.m.'),
('Why does Anna decide to make a gift?','She does not receive her paycheck until the following week',['The shops are closed for a month','Marsha requested no presents','Anna has a free woodworking class'],'Anna needs a low-cost gift because her paycheck is due next week.'),
('Which office supply does Anna borrow from Amelia?','A stapler',['A desk lamp','A computer monitor','A printer'],'Amelia lends Anna her favorite stapler and asks for its return.'),
('What birthday gift does Anna finally make?','A hat made from office supplies',['A photo album','A knitted sweater','A painted bicycle'],'Anna combines borrowed office supplies into a hat for Marsha.')],
47:[
('What is Pete trying to fix at the start?','His car',['His kitchen sink','A bicycle tire','An office computer'],'Pete is working on his car when Anna meets him.'),
('Which engine parts has Pete mistakenly removed?','Spark plugs',['Seat belts','Windshield wipers','Floor mats'],'Pete incorrectly believes there are extra spark plugs in his engine.'),
('How many lessons are in the repair course Pete is taking?','Four hundred and fifty',['Ten','Twenty','One hundred'],'Pete has watched ten lessons, but the complete course has 450.'),
('How did Anna learn to repair cars?','She learned from a master as a teenager',['She learned in one afternoon','She studied only a pamphlet','She watched a short advertisement'],'Anna says she fixed cars when she was a teenager and learned from a master.')]
})

BANK1.update({
48:[
('Where has Jean just arrived from?','Boston',['San Francisco','Dallas','Chicago'],'Jean tells Anna she has just flown in from Boston.'),
('What kind of museum does Jean want to visit?','An unusual one',['Only a sports museum','Only a museum about cars','No museum at all'],'Jean asks Anna for an interesting, unusual museum recommendation.'),
('Which place does Anna recommend for outdoor sculptures?','The Sculpture Garden',['The National Zoo','A baseball park','An airport terminal'],'Anna recommends visiting the Sculpture Garden.'),
('Which local attraction has Anna surprisingly never visited?','The zoo',['The library','The train station','The Botanic Gardens'],'Although Anna has lived in D.C. for over a year, she has never visited the zoo.')],
49:[
('Which museum does Anna visit for her assignment?','The International Spy Museum',['A natural history museum','A train museum','A medical museum'],'Anna visits the International Spy Museum to gather information for a show.'),
('What code name does Anna give herself?','Agent Flamingo',['Agent Sparrow','Agent Panther','Agent Tiger'],'Anna identifies herself as Agent Flamingo during the mission.'),
('Why does Anna find the air duct difficult?','It is dark and cramped',['It is full of water','She forgot her shoes','It is too brightly lit'],'Anna is afraid of small, dark spaces but crawls through an air duct.'),
('What new skill does Anna try after using the air duct?','Cracking a code',['Playing the violin','Cooking soup','Repairing a car'],'Ms. Weaver then asks whether Anna has ever cracked a code.')],
50:[
('Which university does Anna visit when she returns to school?','Georgetown University',['Stanford University','Boston University','Columbia University'],'Anna introduces the campus of Georgetown University in Washington, D.C.'),
('How long have the students been waiting for their professor?','About ten minutes',['Two hours','All day','About forty minutes'],'Taylor says the class has waited about ten minutes.'),
('Why is Anna nervous about returning to school?','She has been working for several years',['She has lost her passport','She dislikes the campus','She forgot her tuition payment'],'Anna explains that after several years of work, going back to school is nerve-racking.'),
('What word does Anna confuse with “draft”?','Giraffe',['Graph','Drift','Graft'],'Anna says she thought the professor had asked students to bring a giraffe rather than a draft.')],
51:[
('What race does Ashley say she will run that weekend?','Her first marathon',['A bicycle race','A relay swim','A car rally'],'Ashley says she will run her first marathon that weekend.'),
('How long has Anna been training when Ashley asks?','About an hour',['Six months','Two years','One week'],'Anna admits she only started training earlier that day, about an hour ago.'),
('Why is Anna not allowed to run the race she found?','It is a children’s event',['She has lost her shoes','The race has been canceled','Her registration was sent to the wrong city'],'The organizer explains that the race is for children, not adults.'),
('What helpful goal does Anna adopt at the end?','Helping raise money for sick children',['Setting a world record','Winning a professional medal','Opening a sports store'],'Anna decides to help the charity event that raises money for sick children.')],
52:[
('What kind of role did Anna play in Kelly’s stage show?','A tree',['A police detective','A race driver','A scientist'],'Kelly remembers Anna as Tree Number 15 in The Woods Are Alive.'),
('How many movies will Anna act in?','Three',['One','Five','Ten'],'Anna announces plans to perform in three films.'),
('Which movie genre is not among Anna’s three upcoming films?','Historical documentary',['Science fiction','Romantic comedy','Action'],'Anna lists science fiction, romantic comedy and action films, not a documentary.'),
('Does Anna plan to move permanently to Hollywood?','No, she wants to return to Washington, D.C.',['Yes, immediately','Yes, after the first movie','She plans to move to Boston instead'],'Anna says she will make the movies and return to her home in Washington, D.C.')]
})

def make():
 cat=json.loads(CAT.read_text(encoding='utf8')); quiz=json.loads(QUIZ.read_text(encoding='utf8'))
 byid={x['id']:x for x in cat}; found={q['catalogId']:q for q in quiz}; made=0
 for level,lesson_number,questions in [(2,n,q) for n,q in BANK.items()]+[(1,n,q) for n,q in BANK1.items()]:
  catalog_id=f'voa-{level}-{lesson_number:02d}'; item=byid[catalog_id]
  if catalog_id in found or item.get('transcriptImported'):continue
  rows=[]
  for j,(question,correct,wrong,explanation) in enumerate(questions):
   # Stable rotation of answer slot to prevent answer-position shortcut.
   slot=(j+lesson_number)%4
   options=wrong.copy();options.insert(slot,correct)
   rows.append({'question':question,'options':options,'answer':slot,'explanation':explanation,
                'sourceEvidence':'VOA publisher Conversation transcript (see linked original)'})
  entry={'id':f'voa-linked-{level}-{lesson_number:02d}','catalogId':catalog_id,
         'title':item['title'],'level':item['learnerDifficulty'],'topic':item['topic'],
         'sourceUrl':item['sourceUrl'],'attribution':'VOA Learning English',
         'audioAvailability':'publisher_external_only','transcriptAvailability':'publisher_external_only',
         'audioBundled':False,'transcriptImported':False,'playerVerified':False,
         'questions':rows,'sourceReview':'Publisher Conversation reviewed 2026-10-28; answers checked against dialogue'}
  quiz.append(entry)
  item.update({'integrationStatus':'source_linked_quiz','linkedQuizId':entry['id'],
               'questionCount':len(rows),'sourcePageReviewed':'2026-10-28'})
  made+=1
 QUIZ.write_text(json.dumps(quiz,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 CAT.write_text(json.dumps(cat,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 return {'created':made,'sourceLinkedQuizzes':len(quiz),'totalQuestionCount':sum(len(q['questions']) for q in quiz)}
if __name__=='__main__':print(json.dumps(make(),indent=2))
