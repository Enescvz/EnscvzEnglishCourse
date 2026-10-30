#!/usr/bin/env python3
"""Original contextual drafts for the 500-item fluency focus. Never approve automatically.

Rows contain original, purpose-written explanatory prose and contrasting everyday
examples. Level labels are provisional educational estimates, not CEFR certificates.
Re-running is safe: existing lessons are not duplicated.
"""
from pathlib import Path
import json
from promote_content_batch import process, ROOT

ROWS = r'''
check into|giriş yapmak; araştırmak|To register at a hotel or investigate a situation in more detail.|We need to check into the hotel before six tonight.|The manager promised to check into my complaint tomorrow.|inseparable
check off|listede işaretlemek|To mark an item as finished or completed on a list.|I checked off the groceries as I put them in the cart.|She checked every task off before going home.|separable
fill out|form doldurmak|To complete a form by writing the information it asks for.|Please fill out this form before your appointment.|He filled the application out on his phone last night.|separable
fill up|tamamen doldurmak|To make a container or space completely full of something.|Let's fill up the car before we leave town.|She filled her water bottle up at the airport.|separable
finish up|bitirip tamamlamak|To complete the last part of a task or activity.|I'll finish up this email and meet you downstairs.|They finished the cleaning up before the guests arrived.|separable
fit in|uyum sağlamak; vakit ayırmak|To feel accepted in a group or find room for an activity.|It took him a while to fit in at his new school.|Can we fit in a quick call before lunch today?|intransitive
keep off|uzak durmak; üzerine çıkmamak|To avoid touching or entering a surface or area.|Please keep off the grass while it is being repaired.|The doctor told him to keep weight off his injured ankle.|inseparable
keep out|içeri sokmamak; dışarıda tutmak|To prevent a person or thing from entering a place.|Close the window to keep the mosquitoes out tonight.|The fence keeps strangers out of the backyard.|separable
come about|meydana gelmek; gerçekleşmek|To happen or develop as the result of circumstances.|How did this sudden change in plans come about?|The agreement came about after several long meetings.|intransitive
come after|peşinden gelmek; hedef almak|To follow someone or try to find and catch them.|A little dog came after us as we left the park.|The reporter came after the company for an explanation.|inseparable
come by|elde etmek; uğramak|To obtain something or visit a place briefly.|Affordable apartments are hard to come by in this area.|Come by my place after work if you have time.|intransitive
come into|miras almak; sahip olmaya başlamak|To receive money or property, often through inheritance.|She came into some money after her aunt passed away.|He unexpectedly came into ownership of the family store.|inseparable
come on|hadi; başlamak; gelişmek|To begin happening or make progress, often used conversationally.|Come on, we're going to miss the train again.|I can feel a headache coming on after that long drive.|intransitive
come up to|yaklaşmak; yanına gelmek|To approach someone and stop near them, often to speak.|A stranger came up to me and asked for directions.|Two kids came up to our table to say hello.|inseparable
come upon|tesadüfen rastlamak|To discover or meet someone or something unexpectedly.|We came upon a quiet beach while exploring the coast.|She came upon an old photograph in the attic.|inseparable
make over|yeniden düzenlemek; dönüştürmek|To change the appearance or style of a person or place significantly.|They made over the old kitchen before moving in.|The designer made the small room over on a tight budget.|separable
put across|fikrini anlaşılır biçimde anlatmak|To communicate an idea successfully so that people understand it.|She put her main point across without raising her voice.|It's easier to put a complex idea across with an example.|separable
put in|yerleştirmek; zaman veya emek harcamak|To place something somewhere or spend time doing an activity.|He put in extra hours to prepare for the interview.|Please put the leftovers in the fridge after dinner.|separable
put under|baskı altına almak; zorlamak|To place someone in a difficult situation or under pressure.|The tight deadline put the whole team under pressure.|Unexpected bills put the family under serious financial strain.|separable
look away|bakışını başka yöne çevirmek|To turn your eyes away from something you are watching.|I had to look away during the frightening scene.|She looked away when she noticed the camera.|intransitive
look on|izlemek; seyirci kalmak|To watch an event without taking part in it.|Several people looked on as the firefighters arrived.|Her friends looked on while she opened the gift.|intransitive
look to|güvenmek; yardım beklemek|To depend on someone for help, guidance, or support.|New employees look to her for practical advice.|We look to our neighbors when we need help.|inseparable
get along|iyi geçinmek; anlaşmak|To have a friendly relationship with another person.|My sister and I get along much better now.|Do you get along with your new roommates?|intransitive
get at|ima etmek; kastetmek|To suggest something indirectly rather than say it plainly.|I'm not sure what you're getting at with that question.|What are you getting at when you say I changed?|inseparable
get onto|bir konuya geçmek; birine ulaşmak|To start talking about a subject or contact someone about it.|How did we get onto the subject of moving abroad?|I'll get onto the landlord about the broken heater.|inseparable
get to|bir yere ulaşmak; fırsat bulmak|To arrive at a place or have the chance to do something.|What time did you get to the station yesterday?|I finally got to meet her parents last weekend.|inseparable
go about|bir işe girişmek; yapmak|To start or carry out a task in a particular way.|How should I go about finding a new apartment?|She went about solving the problem one step at a time.|inseparable
go along|eşlik etmek; birlikte gitmek|To accompany someone or continue with an activity.|Can I go along when you visit the market?|He went along with his friends to the concert.|intransitive
go around|dolaşmak; yayılmak|To move from place to place or spread among people.|A stomach bug is going around the office this week.|Let's go around the block before heading home.|intransitive
go by|geçip gitmek; esas almak|To pass in time or follow a piece of information or rule.|The afternoon went by faster than I expected.|We usually go by the instructions on the package.|intransitive
go under|batmak; iflas etmek|To fail financially or stop operating as a business.|A lot of small restaurants went under that winter.|Without more customers, the shop could go under soon.|intransitive
go with|birlikte tercih etmek; uyum sağlamak|To choose one option or match well with another thing.|I think I'll go with the blue jacket today.|Those shoes go with almost everything you own.|inseparable
bring around|ikna etmek; fikrini değiştirmek|To persuade someone to accept an idea they first rejected.|We finally brought Dad around to our travel plans.|A good explanation might bring the team around.|separable
bring off|zor bir işi başarmak|To succeed in doing something difficult or unlikely.|They brought off a surprise party without anyone noticing.|She brought the difficult presentation off with confidence.|separable
hand out|dağıtmak|To give something to several people one by one.|The teacher handed out copies of the assignment.|Volunteers handed blankets out to people waiting outside.|separable
hand over|teslim etmek; devretmek|To give control or possession of something to another person.|Please hand over your keys before you move out.|He handed the project over to the new manager.|separable
hand down|nesilden nesile aktarmak|To pass something from an older generation to a younger one.|This recipe was handed down by my grandmother.|She handed the old watch down to her son.|separable
cheer up|neşelenmek; neşelendirmek|To become happier or help someone feel less sad.|A walk in the sunshine might cheer you up.|She cheered up when she heard the good news.|separable
chip in|katkıda bulunmak; para koymak|To contribute money, effort, or help to a shared task.|Everyone chipped in to buy a birthday present.|Can you chip in and help us clean the kitchen?|intransitive
chill out|rahatlamak; sakinleşmek|To relax and stop worrying or getting upset about something.|Let's chill out at home instead of going out.|He needs to chill out before discussing the problem.|intransitive
clean out|içini tamamen boşaltıp temizlemek|To remove unwanted things from the inside of a space.|I cleaned out my closet over the weekend.|We need to clean the old garage out before winter.|separable
clean up|temizlemek; toparlamak|To make a place or situation clean and orderly.|Could you clean up the kitchen after breakfast?|We cleaned the room up before our friends arrived.|separable
clear out|boşaltmak; çıkıp gitmek|To remove everything from a place or leave it completely.|We cleared out the basement to make room for storage.|The staff asked everyone to clear out after closing.|separable
clear up|açıklığa kavuşturmak; düzelmek|To make confusion disappear or become less cloudy or unpleasant.|Let me clear up the misunderstanding before we leave.|The weather cleared up just in time for the picnic.|separable
close down|kalıcı olarak kapatmak|To stop operating a business or place permanently.|The bakery closed down after thirty years on the corner.|They closed the old factory down last spring.|separable
close up|kapatmak; aralığı daraltmak|To shut a shop or bring the edges of something together.|We close up the store at nine on weekdays.|The gap in the fence closed up after the repairs.|intransitive
cool down|serinlemek; sakinleşmek|To become cooler or less angry after a heated situation.|Let's wait for the soup to cool down before eating.|He took a walk to cool down after the argument.|intransitive
cool off|serinlemek; duyguların yatışması|To become cooler or less emotionally intense.|We sat in the shade to cool off after our hike.|Their excitement cooled off when the price went up.|intransitive
cook up|uydurmak; hızla hazırlamak|To invent a plan or excuse, or prepare food with what is available.|They cooked up an excuse for missing the meeting.|I can cook up something simple with these vegetables.|separable
cover up|gizlemek; üzerini örtmek|To hide a mistake, fact, or wrongdoing from other people.|Don't try to cover up the mistake; just tell me.|The company covered the problem up for several months.|separable
cover for|birinin yerine bakmak; idare etmek|To do someone's duties temporarily or make an excuse for them.|Could you cover for me while I take a break?|She covered for her coworker during his vacation.|inseparable
count down|geri saymak|To say numbers in reverse order before an event happens.|The crowd counted down to midnight together.|Let's count down from ten before the game starts.|intransitive
crack down|sert önlem almak|To take stronger action to stop illegal or unwanted behavior.|The city is cracking down on unsafe driving.|The school cracked down on students arriving late.|intransitive
crack up|kahkahaya boğulmak|To suddenly begin laughing very hard at something funny.|We all cracked up when he told that story.|She cracks up every time she watches that video.|intransitive
cross off|listeden çizmek|To remove a name or task by drawing a line through it.|I crossed off the errands I'd already finished.|She crossed my name off the guest list by mistake.|separable
cut across|kestirmeden geçmek|To take a shorter route by moving across a place.|We cut across the park to reach the station.|She cut across the parking lot to save time.|inseparable
cut away|kesip çıkarmak|To remove part of something by cutting it away.|He cut away the damaged fabric before sewing the patch.|The gardener cut the dead branches away carefully.|separable
cut in|sözünü kesmek; araya girmek|To interrupt someone speaking or move suddenly in front of others.|Sorry to cut in, but I have one quick question.|A car cut in right ahead of us on the highway.|intransitive
cut up|küçük parçalara kesmek|To divide food or another material into smaller pieces with a knife.|Can you cut up the apples for the kids?|She cut the vegetables up while I cooked the rice.|separable
catch up|yetişmek; haberleşip sohbet etmek|To reach someone's level or share recent news after time apart.|Let's catch up over coffee this weekend.|I missed two classes and need to catch up.|intransitive
call in|telefon edip bildirmek; çağırmak|To phone a workplace or ask someone to come and help.|She called in sick because she had a fever.|We had to call in a plumber to fix the leak.|separable
cancel out|birbirini etkisiz hale getirmek|To have opposite effects so that neither has a final impact.|The extra fee canceled out the discount completely.|Their two small mistakes canceled each other out.|separable
drop behind|geride kalmak|To fall farther back than other people or a planned schedule.|I dropped behind during the last mile of the run.|The project dropped behind when we lost two workers.|intransitive
eat out|dışarıda yemek yemek|To have a meal at a restaurant instead of at home.|We usually eat out on Friday nights.|They decided to eat out after a long day at work.|intransitive
eat up|tamamını yemek|To eat all of the food that someone has given you.|Eat up your dinner before it gets cold.|The kids ate the sandwiches up after swimming.|separable
eat in|evde yemek yemek|To eat a meal at home rather than at a restaurant.|Let's eat in tonight and watch a movie.|We ate in all week to save some money.|intransitive
ease off|hafiflemek; azalmak|To gradually become less strong, severe, or frequent.|The rain finally eased off around lunchtime.|His back pain eased off after a few days of rest.|intransitive
even out|dengelemek; eşitlenmek|To make differences smaller or become more equal over time.|The workload should even out after the holiday season.|We spread the costs out to even out our monthly budget.|separable
fade away|yavaş yavaş kaybolmak|To gradually become weaker, less noticeable, or disappear.|The noise from the street faded away at night.|Her worries slowly faded away during the vacation.|intransitive
fall into|içine düşmek; alışkanlık edinmek|To enter a condition or gradually develop a habit without planning.|I fell into the habit of checking my phone too often.|The room fell into silence when she started speaking.|inseparable
fall off|düşmek; azalmak|To become detached and drop, or decrease in amount or quality.|A button fell off my jacket on the bus.|Sales often fall off after the holiday rush.|intransitive
fall over|düşüp devrilmek|To lose your balance and fall onto the ground.|Be careful not to fall over on the icy sidewalk.|A chair fell over when the dog ran past it.|intransitive
feel like|istemek; öyle hissetmek|To want to do something or have the impression that something is true.|I feel like staying home and cooking tonight.|It feels like we're finally making some progress.|inseparable
fend off|savmak; uzak tutmak|To defend against a threat or unwanted attention successfully.|She fended off several questions about her private life.|We used umbrellas to fend off the afternoon rain.|separable
fight off|yenmek; direnerek uzaklaştırmak|To resist or successfully overcome an illness or attack.|He's trying to fight off a cold before the trip.|The team fought off a late challenge and won.|separable
filter out|ayıklamak; elemek|To remove things that are not wanted or relevant from a larger group.|The app filters out messages from unknown senders.|I filtered the irrelevant search results out before reading.|separable
follow through|sonuna kadar götürmek|To complete a plan or promise after making a decision.|You need to follow through if you want real progress.|She made a promise and followed through the next day.|intransitive
fool around|boş boş oyalanmak; şakalaşmak|To waste time behaving playfully instead of working seriously.|Stop fooling around and help me with the boxes.|The kids fooled around in the backyard all afternoon.|intransitive
freak out|paniğe kapılmak; çok heyecanlanmak|To react with sudden intense fear, worry, or excitement.|Don't freak out; we still have plenty of time.|He freaked out when he couldn't find his passport.|intransitive
gear up|hazırlanmak|To prepare yourself or a group for a demanding activity.|We're gearing up for a busy holiday weekend.|The team geared up for the big presentation.|intransitive
give off|yaymak; koku veya ışık çıkarmak|To release or produce a smell, light, heat, or other effect.|The flowers give off a sweet smell in the evening.|That old heater gives off a lot of heat.|inseparable
hang around|oyalanmak; takılmak|To stay in a place without doing anything particular.|We hung around the cafe after lunch and talked.|He often hangs around the park with his friends.|intransitive
hang on|beklemek; tutunmak|To wait briefly or hold tightly to something.|Hang on a second; I need to grab my keys.|Hang on to the railing while you walk downstairs.|intransitive
hang up|telefonu kapatmak|To end a phone call by disconnecting.|She hung up before I could say goodbye.|Don't hang up yet; I have one more question.|intransitive
hold down|işi sürdürmek; bastırmak|To keep a job or physically prevent something from moving.|He managed to hold down two part-time jobs.|Hold the edge of the paper down while I tape it.|separable
hold in|duyguyu bastırmak|To stop yourself from expressing a feeling or reaction.|She tried to hold in her laughter during the speech.|I couldn't hold my tears in when I heard the news.|separable
hold onto|sıkı tutmak; saklamak|To keep something in your possession or grip despite difficulty.|Hold onto your ticket until the end of the trip.|She held onto the letters her grandfather had written.|inseparable
lie down|uzanmak|To put yourself in a flat resting position on a bed or floor.|I need to lie down for a few minutes after lunch.|He lay down on the couch and closed his eyes.|intransitive
line up|sıraya girmek; sıralamak|To stand in a row or arrange people or things in order.|People lined up outside the theater before the show.|We lined the chairs up along the wall.|separable
move over|kenara çekilmek; yer açmak|To change position so that another person can fit nearby.|Could you move over so I can sit beside you?|Everyone moved over to make room on the bench.|intransitive
pass away|vefat etmek|To die, often used instead of the more direct word die.|Her grandfather passed away peacefully last year.|We were sad to hear that our neighbor had passed away.|intransitive
pull over|aracı yol kenarına çekmek|To move a vehicle to the side of the road and stop.|Please pull over when you see a safe place to stop.|The officer asked the driver to pull over immediately.|intransitive
run across|tesadüfen karşılaşmak; rastlamak|To find something or meet someone unexpectedly.|I ran across an old classmate downtown yesterday.|She ran across a useful article while researching.|inseparable
set down|yere koymak; yazmak|To put something on a surface or record something in writing.|Set the bags down here while I open the door.|He set down a few thoughts in his notebook.|separable
shut down|kapatmak; çalışmayı durdurmak|To stop a machine, business, or service from operating.|The airport shut down briefly because of the storm.|Please shut the computer down before you leave.|separable
sign in|oturum açmak; giriş yapmak|To enter your details to access a system or register your arrival.|You need to sign in before you can see your messages.|We signed in at the front desk when we arrived.|intransitive
sign up|kayıt olmak|To register your name to join an activity, course, or service.|I signed up for a cooking class next month.|She signed up to volunteer at the community center.|intransitive
stay up|geç yatmak; uyanık kalmak|To remain awake later than usual or through the night.|We stayed up late talking after the wedding.|I shouldn't stay up so late before an early meeting.|intransitive
throw away|çöpe atmak|To get rid of something you no longer need or want.|Don't throw away the receipt until the return period ends.|She threw the empty boxes away after unpacking.|separable
throw out|dışarı atmak; çöpe atmak|To remove something by disposing of it or putting it outside.|We threw out the broken chair last weekend.|He threw the old food out before cleaning the fridge.|separable
throw up|kusmak|To bring food or liquid up from your stomach through your mouth.|He felt sick and threw up on the way home.|She nearly threw up after the rough boat ride.|intransitive
tidy up|toparlamak; düzenlemek|To make a room or area neat by putting things in place.|Let's tidy up the living room before the guests arrive.|She tidied her desk up before starting work.|separable
try on|giyip denemek|To put on clothing briefly to see whether it fits or looks good.|Can I try on this jacket in a smaller size?|She tried the shoes on before buying them.|separable
try out|deneyip test etmek|To use something experimentally to decide whether it works or suits you.|I want to try out the new exercise class tonight.|They tried the recipe out on their friends first.|separable
tune in|yayına bağlanmak; dinlemek|To listen to or watch a particular broadcast or program.|Tune in at eight to hear the live interview.|We tuned in to the radio show on our drive home.|intransitive
wake up|uyanmak; uyandırmak|To stop sleeping or cause someone else to stop sleeping.|I usually wake up before my alarm goes off.|Please wake me up if you leave early tomorrow.|separable
warm up|ısınmak; ısıtmak|To prepare your body for exercise or make something warmer.|Warm up before you start running to avoid injury.|She warmed the soup up for a quick dinner.|separable
wear out|eskimek; yormak|To become unusable through use or make someone extremely tired.|Walking all day really wore me out.|These shoes wear out quickly when I run in them.|separable
work off|sporla yakmak; çalışarak ödemek|To get rid of energy or a debt through physical activity or work.|I went for a walk to work off some nervous energy.|He worked off the debt by helping around the house.|separable
work up|cesaret veya duygu toplamak|To gradually develop an emotion, appetite, or enough courage to act.|She worked up the courage to ask for a raise.|The long hike helped us work up an appetite.|separable
write down|not almak; yazmak|To record information in writing so that you can remember it.|Write down the address so you don't forget it.|He wrote her number down on a piece of paper.|separable
write off|zarar yazmak; değersiz saymak|To record a loss financially or dismiss someone as having no chance.|They had to write off the cost of the damaged goods.|Don't write her off just because she's inexperienced.|separable
'''.strip()

SYNTAX_NOTE = {
    'separable': 'A direct object can follow the whole phrase or appear between verb and particle; pronouns usually go between.',
    'inseparable': 'Keep the particle/preposition together with the verb before its object in this sense.',
    'intransitive': 'This use does not require a direct object; a following prepositional phrase is possible.',
}

def make():
    items=[]
    for idx,line in enumerate(ROWS.splitlines(),1):
        parts=[p.strip() for p in line.split('|')]
        if len(parts)!=6: raise ValueError(f'Row {idx}: needs six fields: {parts!r}')
        word,tr,definition,first,second,syntax=parts
        if syntax not in SYNTAX_NOTE:raise ValueError(f'Row {idx}: invalid syntax')
        items.append({'word':word,'tr':tr,'definition':definition,'example':first,'examples':[first,second],
                      'level':'B2','syntax':syntax,'note':SYNTAX_NOTE[syntax], 'register':'neutral',
                      'levelEvidence':'Provisional pedagogical estimate only; the phrase source does not certify CEFR.',
                      'levelStatus':'editorial_estimate_unverified',
                      'senses':[{'tr':tr,'definition':definition,'example':first}]})
    if len({x['word'] for x in items})!=len(items):raise ValueError('Duplicate phrase in authored batch')
    return items

def main():
    items=make()
    out=ROOT/'sources/authored-20261028-useful-phrasals.jsonl'
    out.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in items),encoding='utf8')
    existing={x['word'].casefold() for x in json.loads((ROOT/'data/phrasals.json').read_text(encoding='utf8'))}
    staged=[x for x in items if x['word'].casefold() not in existing]
    pending=ROOT/'sources/.pending-20261028-useful-phrasals.jsonl'
    try:
        if staged:
            pending.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in staged),encoding='utf8')
            report=process(pending,'phrasal',apply=True)
        else:report={'mode':'already_applied','validatedNewCards':0,'releaseReady':False}
    finally: pending.unlink(missing_ok=True)
    print(json.dumps({'authored':len(items),'new':len(staged),'result':report},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
