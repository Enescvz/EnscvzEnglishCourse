#!/usr/bin/env python3
"""Hand-authored conversational phrasal lesson drafts, never auto-approved.

The shortlist excludes low-value candidates previously used to pad the 500 target.
Definitions/examples are original; phrase membership derives from locally stored
source candidate catalog, whose CEFR labels are unverified.
"""
import json
from pathlib import Path
from promote_content_batch import ROOT, process

# word | Turkish gloss | concise original sense | everyday example A | example B | syntax
ROWS = r'''
blow out|üfleyerek söndürmek|To put out a flame by blowing air toward it.|She blew out the candles before opening her presents.|Please blow the match out before throwing it away.|separable
blow over|yatışmak; geçip gitmek|To become less serious or disappear after a short period.|The disagreement will probably blow over by tomorrow.|We stayed home until the storm had blown over.|intransitive
boil down|özünde şu anlama gelmek|To have one main point after unnecessary details are removed.|The whole argument boils down to a lack of trust.|Our decision boils down to how much time we have.|intransitive
boil over|taşmak; kontrolden çıkmak|To overflow while boiling or become suddenly very emotional.|The milk boiled over while I answered the phone.|Their frustration finally boiled over during the meeting.|intransitive
book up|rezervasyonlarla dolmak|To fill all available places through advance reservations.|The small hotel books up quickly during the summer.|Restaurants near the stadium were booked up for Friday.|intransitive
boss around|emir yağdırmak; buyurgan davranmak|To tell someone what to do in an annoying, controlling way.|My older brother used to boss me around as a kid.|Stop bossing everyone around and help with the work.|separable
breathe in|nefes almak; içeri çekmek|To draw air into your lungs through your nose or mouth.|Breathe in slowly before you start speaking again.|She breathed the fresh mountain air in deeply.|separable
breathe out|nefes vermek|To release air from your lungs through your mouth or nose.|Breathe out gently and let your shoulders relax.|He breathed out slowly when he heard the good news.|intransitive
brush up|bilgiyi tazelemek; tekrar etmek|To improve a skill that you have not practiced recently.|I need to brush up on my English before the trip.|She's brushing up her Spanish for a family visit.|separable
bump up|artırmak; yükseltmek|To increase an amount, price, or level, often unexpectedly.|The airline bumped up the ticket price overnight.|We bumped our daily step goal up to eight thousand.|separable
bundle up|kalın giyinmek; sarıp sarmalamak|To dress warmly or wrap something in several layers.|Bundle up before you go outside; it's freezing.|She bundled the baby up in a warm blanket.|separable
burn down|yanıp kül olmak; tamamen yakmak|To be destroyed by fire or destroy a building with fire.|The empty house burned down during the wildfire.|A kitchen accident almost burned their apartment down.|separable
burn off|sporla enerji yakmak; yok olmak|To use up energy through activity or disappear through heat.|Let's take a walk and burn off some energy.|The morning fog burned off before we reached the lake.|separable
burst out|birden patlamak; aniden başlamak|To suddenly begin laughing, crying, or speaking emotionally.|Everyone burst out laughing at his unexpected joke.|She burst out crying when she saw the old photograph.|intransitive
camp out|kamp yaparak gecelemek|To sleep outside in a tent or temporary shelter.|We camped out beside the lake last weekend.|The kids want to camp out in the backyard tonight.|intransitive
care for|bakımını üstlenmek; ilgilenmek|To look after someone who needs help or attention.|He cares for his grandfather after work every day.|A neighbor cared for our cat while we were away.|inseparable
cave in|baskıya boyun eğmek; içeri çökmek|To give in under pressure or collapse toward the inside.|I didn't want dessert, but I finally caved in.|The old roof caved in after the heavy snowfall.|intransitive
charge up|şarj etmek; enerji doldurmak|To put electrical energy into a battery or device.|Charge up your phone before we leave the house.|I charged my headphones up during breakfast.|separable
chase after|peşinden koşmak; kovalamak|To run after someone or something to catch or reach it.|The dog chased after the ball across the yard.|She ran outside to chase after the departing bus.|inseparable
chew over|uzun uzun düşünmek; değerlendirmek|To think carefully about an idea before making a decision.|Let me chew over your suggestion until tomorrow.|We chewed the offer over during dinner last night.|separable
choke up|duygulanıp konuşamamak|To become unable to speak normally because of strong emotion.|He choked up while thanking his parents on stage.|I always choke up when I watch that family video.|intransitive
chop up|küçük parçalara doğramak|To cut something into several smaller pieces.|Could you chop up the onions for the soup?|She chopped the vegetables up before starting dinner.|separable
clam up|susup içine kapanmak|To suddenly stop talking, especially from fear or shyness.|He clammed up when I asked about the argument.|She usually clams up around people she doesn't know.|intransitive
clear away|ortadan kaldırmak; toplamak|To remove things from an area so that it becomes clear.|Let's clear away the dishes after everyone finishes.|They cleared the toys away before the guests arrived.|separable
climb up|yukarı tırmanmak|To move upward using your legs and sometimes your hands.|We climbed up the hill before it got too hot.|The child climbed up onto the chair to see outside.|intransitive
clock in|işe giriş kaydı yapmak|To record the time when you begin a work shift.|I clocked in five minutes before my shift began.|The staff clock in using a card near the entrance.|intransitive
clog up|tıkamak; engellemek|To block a pipe, road, or passage so that nothing moves easily.|Hair can clog up the shower drain over time.|Traffic clogged the streets up after the concert.|separable
clue in|bilgilendirmek; olan biteni anlatmak|To tell someone important facts they do not yet know.|Could you clue me in on what happened yesterday?|She clued the new teammate in before the meeting.|separable
cop out|sorumluluktan kaçmak|To avoid doing something difficult by making an excuse.|Don't cop out just because the task looks hard.|He copped out of helping us at the last minute.|intransitive
cough up|istemeyerek para vermek|To pay money unwillingly, often under pressure.|We had to cough up extra cash for the repairs.|He finally coughed up the money he owed her.|separable
crank up|sesini veya gücünü artırmak|To increase the power, volume, or intensity of something.|Could you crank up the heat? I'm freezing.|They cranked the music up when the party started.|separable
curl up|kıvrılıp uzanmak; büzülmek|To sit or lie with your body bent into a small, comfortable shape.|I curled up on the couch with a good book.|The cat curled up beside the heater and fell asleep.|intransitive
dig in|iştahla yemeye başlamak; girişmek|To start eating enthusiastically or begin a task with energy.|Dinner is ready, everyone; let's dig in!|Once we agreed on a plan, the team dug in.|intransitive
dig into|derinlemesine incelemek; araştırmak|To examine information or a subject in greater detail.|I want to dig into the numbers before deciding.|The journalist dug into the story for several weeks.|inseparable
dig out|bulup çıkarmak; kazıp kurtarmak|To find and take something out of a hidden or crowded place.|I dug out my old winter coat from the closet.|She dug the photos out to show her friends.|separable
dig up|araştırıp bulmak; kazıp çıkarmak|To uncover information or find something that was hidden.|He dug up an old email that explained the problem.|The kids dug up a few coins in the garden.|separable
doze off|uyuklamak; dalıp gitmek|To fall asleep for a short time without planning to.|I dozed off during the long train ride home.|He nearly dozed off while watching the late movie.|intransitive
drag on|gereğinden uzun sürmek|To continue for an annoyingly long period of time.|The meeting dragged on well past lunchtime.|Their argument dragged on for the whole evening.|intransitive
dream up|hayal edip ortaya atmak|To invent a new idea, often one that seems unusual.|The kids dreamed up a game for the rainy afternoon.|She dreamed up a clever way to save space at home.|separable
dress up|şık giyinmek; kostüm giymek|To wear special clothes for an occasion or appearance.|We dressed up for my cousin's wedding last night.|The children dressed up as astronauts for the party.|intransitive
drift off|uykuya dalmak; düşüncelere kaymak|To gradually fall asleep or stop paying attention.|I drifted off while listening to the rain outside.|She drifted off halfway through the documentary.|intransitive
factor in|hesaba katmak|To include a particular detail when calculating or deciding something.|Remember to factor in the cost of parking.|We factored the extra travel time in before leaving.|separable
finish off|son kısmını tamamlamak; bitirmek|To complete the last part of a task or use the last amount.|I'll finish off the report after my morning coffee.|We finished the leftover cake off after dinner.|separable
fire up|çalıştırmak; heyecanlandırmak|To start a machine or make someone feel more enthusiastic.|Fire up the grill while I prepare the vegetables.|The coach fired the players up before the game.|separable
flare up|aniden şiddetlenmek; alevlenmek|To suddenly become more intense, especially anger or pain.|His knee pain flared up after the long hike.|An argument flared up over the seating arrangement.|intransitive
flip out|çılgına dönmek; aşırı tepki vermek|To become extremely upset, excited, or surprised very suddenly.|My mom flipped out when she saw the broken window.|Don't flip out; we can still fix the mistake.|intransitive
fold up|katlamak; kapatıp toplamak|To bend something so it takes up less space.|Please fold up the chairs after the event.|He folded the map up and put it in his backpack.|separable
freshen up|üstünü başını düzeltmek; tazelenmek|To wash or tidy yourself quickly so you feel more comfortable.|I need to freshen up before we go to dinner.|She freshened up after the flight and changed clothes.|intransitive
gather up|toplayıp bir araya getirmek|To collect several items and bring them together.|Gather up your things; we're leaving in ten minutes.|He gathered the papers up from the kitchen table.|separable
glance over|şöyle bir gözden geçirmek|To read or look at something quickly without studying it closely.|Could you glance over this message before I send it?|She glanced over the menu and ordered soup.|inseparable
gloss over|üstünü örtmek; geçiştirmek|To avoid discussing an unpleasant or important detail.|He glossed over the problem during his presentation.|We shouldn't gloss over the cost of changing plans.|inseparable
grow up|büyümek; yetişkin olmak|To develop from a child into an adult over time.|I grew up in a small town near the mountains.|She wants to be a doctor when she grows up.|intransitive
hang in|dayanmak; pes etmemek|To keep trying when a situation feels difficult.|Hang in there; the first week is always tough.|She hung in through months of difficult treatment.|intransitive
hash out|konuşup çözüme bağlamak|To discuss a disagreement or plan until the details are settled.|Let's hash out the details over coffee tomorrow.|They hashed the problem out before the guests arrived.|separable
heat up|ısıtmak; ısınmak|To make food or a place warmer, or become warmer.|I'll heat up some leftovers for lunch today.|She heated the soup up on the stove.|separable
help out|yardım etmek; el atmak|To give practical assistance when someone needs it.|Can you help out with the dishes after dinner?|My neighbor helped me out when my car broke down.|intransitive
hook up|bağlamak; bağlantı kurmak|To connect devices or equipment so they can work together.|Can you hook up the printer to my laptop?|We hooked the speakers up before the guests arrived.|separable
jot down|çabucak not almak|To write a short note quickly so you remember something.|I'll jot down the address before I forget it.|She jotted his phone number down on a receipt.|separable
kick in|devreye girmek; etkisini göstermeye başlamak|To begin working or having an effect after a delay.|The pain medicine kicked in after half an hour.|My energy finally kicked in after the morning walk.|intransitive
kick out|kovmak; dışarı atmak|To force someone to leave a place or group.|The landlord kicked the noisy tenants out.|He was kicked out of the game for arguing.|separable
knock over|devirip düşürmek|To hit something accidentally and cause it to fall.|Be careful not to knock over your glass of water.|The dog knocked the flower vase over with its tail.|separable
leave behind|geride bırakmak; unutmak|To go away without taking someone or something with you.|I accidentally left my umbrella behind at the cafe.|We left the old furniture behind when we moved.|separable
let in|içeri almak; içeri girmesine izin vermek|To open an entrance so someone or something can enter.|Could you let the delivery person in, please?|She opened the curtains to let the sunlight in.|separable
let out|dışarı çıkarmak; serbest bırakmak|To allow a person, animal, or thing to leave a place.|Don't forget to let the dog out before bed.|The teacher let the students out five minutes early.|separable
light up|aydınlatmak; yüzü gülmek|To become bright or cause something to shine with light.|Her face lit up when she saw her friends.|The string lights lit the whole patio up at night.|separable
log in|hesaba giriş yapmak|To enter a digital account using a username or other credentials.|I can't log in because I forgot my password.|She logged in to check her flight details.|intransitive
log off|hesaptan çıkış yapmak|To end an authenticated session in an app or computer.|Remember to log off before using a shared computer.|He logged off after finishing his online class.|intransitive
loosen up|gevşemek; rahatlamak|To become less tense or less formal around others.|I always loosen up after talking for a few minutes.|A short stretch can help your shoulders loosen up.|intransitive
mess up|batırmak; hata yapmak|To make a mistake or spoil an arrangement or plan.|I messed up the reservation date by accident.|Don't worry if you mess up while speaking English.|separable
mix up|karıştırmak; birbirine karıştırmak|To mistake one thing for another or combine things unintentionally.|I always mix up their names when I'm nervous.|She mixed the two appointments up and arrived late.|separable
'''.strip()

SYNTAX_NOTE={
'separable':'An object can follow the particle or go between verb and particle; object pronouns normally go between.',
'inseparable':'Keep the particle or preposition next to the verb before its object for this meaning.',
'intransitive':'No direct object is required for this meaning; a following prepositional phrase may be used.'}


def make():
    out=[]
    for line_number, line in enumerate(ROWS.splitlines(),1):
        fields=[p.strip() for p in line.split('|')]
        if len(fields)!=6:raise ValueError(f'line {line_number} has {len(fields)} fields')
        word,tr,definition,e1,e2,syntax=fields
        if syntax not in SYNTAX_NOTE:raise ValueError(f'{word}: invalid syntax')
        out.append({'word':word,'tr':tr,'definition':definition,'example':e1,'examples':[e1,e2],
            'level':'B2','syntax':syntax,'note':SYNTAX_NOTE[syntax], 'register':'neutral',
            'levelEvidence':'Provisional level estimate only; source does not certify CEFR for this phrasal sense.',
            'levelStatus':'editorial_estimate_unverified', 'senses':[{'tr':tr,'definition':definition,'example':e1}]})
    if len(out)!=70 or len({x['word'] for x in out})!=70:raise ValueError(f'Expected 70 unique rows, found {len(out)}')
    return out


def main():
    rows=make()
    names={x['word'] for x in rows}
    source={x['word'] for x in json.loads((ROOT/'sources/phrasal-candidates.json').read_text(encoding='utf8'))}
    if names-source:raise ValueError(f'No source evidence for {names-source}')
    authored={x['word']:x for x in json.loads((ROOT/'data/phrasals.json').read_text(encoding='utf8'))}
    for item in rows:
        if item['word'] in authored:
            old=authored[item['word']]
            if any(old.get(field)!=item[field] for field in ('definition','tr','example')):
                raise ValueError(f'Existing authored content differs: {item["word"]}')
    out=ROOT/'sources/authored-20261028-final-conversational-phrasals.jsonl'
    out.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf8')
    # Precondition: build_fluency_focus.py includes these source headwords before
    # older low-value candidates, but no status is forged or editorially approved.
    selected={x['word'] for x in json.loads((ROOT/'data/fluency-focus.json').read_text(encoding='utf8'))['phrasals']}
    if not names<=selected:raise ValueError(f'Rebuild focus first; missing {names-selected}')
    remaining=[row for row in rows if row['word'] not in authored]
    pending=ROOT/'sources/.pending-20261028-final-phrasals.jsonl'
    try:
        if remaining:
            pending.write_text(''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in remaining),encoding='utf8')
            report=process(pending,'phrasal',apply=True)
        else:
            report={'mode':'already_applied','validatedNewCards':0,'releaseReady':False}
    finally:
        pending.unlink(missing_ok=True)
    print(json.dumps({'authored':len(rows),'new':len(remaining),'result':report},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
