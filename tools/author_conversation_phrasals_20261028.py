#!/usr/bin/env python3
"""Original two-context conversational phrasal lesson batch. Never self-approve.

Meaning, syntax and context are authored educational drafts, requiring a
qualified editor for American-English usage, nuance, and CEFR before release.
"""
from pathlib import Path
import json
from promote_content_batch import process
ROOT=Path(__file__).resolve().parents[1]
# word | Turkish gloss | English definition | context one | context two | syntax
ROWS="""
catch up with|birinin haberlerini almak; yetişip sohbet etmek|To talk with someone you have not seen recently and exchange news.|I called my cousin to catch up with her after her trip.|We caught up with some old friends over coffee.|inseparable
set up|kurmak, ayarlamak|To arrange or establish something so it is ready to use.|Could you set up a meeting for Friday afternoon?|They set up a small table near the entrance.|separable
make up|uydurmak|To invent a story or excuse rather than tell the truth.|He made up an excuse for arriving late.|Please don't make up a story about what happened.|separable
fill in|doldurmak (form, bilgi)|To write the required information in the blank spaces of a document.|Please fill in your address before submitting the form.|She filled in the missing details on the application.|separable
show up|gelmek, ortaya çıkmak|To arrive at a place, especially when people are expecting you.|Only half the guests showed up for the picnic.|I was worried he wouldn't show up on time.|intransitive
come around|fikrini değiştirmek, ikna olmak|To change your opinion and begin to accept an idea.|She didn't like the plan at first, but she came around.|Give him a day to think; he may come around.|intransitive
pick up|gidip almak, birini arabayla almak|To collect someone or something from a particular place.|I'll pick you up outside the station at six.|Can you pick up the package on your way home?|separable
slow down|yavaşlamak, yavaşlatmak|To reduce speed or make something happen less quickly.|Slow down when you reach the narrow street.|The rain slowed down traffic on the highway.|separable
settle down|yerleşmek, sakin bir hayata geçmek|To establish a stable home or a calmer routine.|They want to settle down near their families.|After years of moving, she finally settled down.|intransitive
reach out|iletişime geçmek, yardım istemek|To contact someone in order to talk, ask for help, or offer support.|Don't hesitate to reach out if you need advice.|I reached out to a former classmate about the event.|intransitive
break up|ilişkiyi bitirmek, ayrılmak|To end a romantic relationship with another person.|They broke up after dating for three years.|She was upset when she and her boyfriend broke up.|intransitive
go on|devam etmek|To continue doing something or happening.|The music went on long after the sun went down.|Please go on; I want to hear the rest of the story.|intransitive
hold on|biraz beklemek|To wait briefly while someone checks or finishes something.|Hold on a second while I check the address.|Could you hold on until I find my keys?|intransitive
let down|hayal kırıklığına uğratmak|To disappoint someone by failing to do what they expected.|I promised to help and I don't want to let her down.|He felt that the team had let him down.|separable
pass out|bayılmak, bilincini kaybetmek|To lose consciousness for a short period of time.|She nearly passed out in the crowded room.|He passed out from the heat during the race.|intransitive
look out|dikkat etmek, tehlikeye karşı uyarmak|To be careful because there may be danger nearby.|Look out! There's a bike coming around the corner.|You need to look out when crossing this busy road.|intransitive
run out|tükenmek, bitmek|To become completely used up or no longer available.|Our supplies ran out before the storm ended.|The printer paper ran out during the meeting.|intransitive
drop off|birini bir yere bırakmak|To take someone or something to a place and leave them there.|Can you drop me off near the library?|She dropped off the kids at school before work.|separable
show off|gösteriş yapmak|To behave in a way that draws attention to your abilities or possessions.|He kept showing off his new watch at dinner.|She can play well without trying to show off.|intransitive
walk away|uzaklaşıp gitmek, çekip gitmek|To leave a place or situation, often to avoid an argument.|He decided to walk away before the discussion became heated.|Sometimes it's better to walk away from a bad deal.|intransitive
think over|iyice düşünmek|To consider something carefully before making a decision.|I'd like a day to think over your offer.|She thought the proposal over before answering.|separable
get around|bir yerde dolaşmak, ulaşım sağlamak|To travel from place to place within an area.|It's easy to get around the city by subway.|We rented bicycles to get around during our trip.|intransitive
keep on|devam etmek, sürdürmek|To continue doing something, especially despite difficulty.|Keep on practicing and the phrases will feel more natural.|He kept on talking even after the lights went out.|intransitive
come along|birine katılmak, beraber gitmek|To accompany someone who is going somewhere.|You're welcome to come along to the museum.|My sister came along when we went shopping.|intransitive
come to|kendine gelmek, bilinci yerine gelmek|To become conscious again after fainting.|She came to a few minutes after the accident.|When he came to, a nurse was sitting beside him.|intransitive
put on|giymek, takmak|To place clothing or an accessory on your body.|Put on a jacket; it's getting cold outside.|She put her glasses on to read the menu.|separable
keep up|hıza ayak uydurmak|To move or work fast enough to match others.|I had to walk quickly to keep up with the group.|The new student struggled to keep up in class.|intransitive
move in|yeni bir eve taşınmak|To begin living in a different house or apartment.|We're moving in next weekend if the paint is dry.|They moved in after the landlord gave them the keys.|intransitive
go out|dışarı çıkmak, sosyalleşmeye gitmek|To leave home to spend time socially.|We usually go out for dinner on Friday nights.|She didn't feel like going out after the long trip.|intransitive
look around|etrafına bakmak, gezinmek|To explore a place or examine what is available.|We looked around the neighborhood before choosing an apartment.|Feel free to look around the store while I get your order.|intransitive
run through|hızlıca gözden geçirmek|To review or practice something quickly from beginning to end.|Let's run through the schedule before everyone arrives.|She ran through her notes one last time before speaking.|separable
back out|verdiği karardan caymak|To decide not to do something you had previously agreed to do.|He backed out of the trip when his plans changed.|Please tell me now if you're going to back out.|intransitive
lay off|işten çıkarmak|To stop employing someone because the organization needs fewer workers.|The company laid off several employees after sales dropped.|She was laid off when the store closed.|separable
watch out|dikkat etmek, gözünü dört açmak|To stay alert to possible danger or trouble.|Watch out for the wet steps near the entrance.|You should watch out when crossing at that intersection.|intransitive
stand by|yanında olmak, desteklemek|To support someone through a difficult situation.|Her family stood by her during the trial.|I'll stand by you whatever you decide.|inseparable
give away|bedava vermek, bağışlamak|To give something to someone without asking for money.|We gave away our old furniture before moving.|She gives away clothes she no longer wears.|separable
bring on|neden olmak, tetiklemek|To cause an event or condition to begin.|Too much stress can bring on a headache.|The sudden change in temperature brought on the symptoms.|separable
give out|dağıtmak|To distribute something to several people.|The teacher gave out the worksheets at the start of class.|Volunteers gave out bottles of water at the finish line.|separable
make for|bir yere doğru yönelmek|To move toward a particular destination or location.|We made for the exit as soon as the show ended.|When the rain started, the hikers made for the cabin.|inseparable
turn over|ters çevirmek|To change the position of something so its other side faces up.|Turn over the paper when the timer starts.|He turned the card over to read the instructions.|separable
break in|zorla içeri girmek|To enter a building without permission, usually by force.|Someone tried to break in through the back window.|The alarm went off when a thief broke in.|intransitive
call out|seslenmek, yüksek sesle söylemek|To speak loudly so that someone can hear you.|She called out his name across the crowded platform.|He called out for help when he saw the smoke.|intransitive
cut out|kesip çıkarmak|To remove a shape or picture by cutting around it.|The kids cut out paper stars for the decorations.|She cut the coupon out of the newspaper.|separable
run away|kaçmak, uzaklaşmak|To leave quickly, often because of fear or danger.|The dog ran away when the gate was left open.|The children ran away from the sudden noise.|intransitive
run over|arabayla üzerinden geçmek|To hit and pass over something with a moving vehicle.|Be careful not to run over the bike near the driveway.|A delivery truck ran over the empty cardboard box.|separable
set off|yola çıkmak|To leave a place and begin a trip or journey.|We set off before sunrise to avoid the traffic.|They set off for the beach early on Saturday.|intransitive
work on|üzerinde çalışmak, geliştirmek|To spend time improving or completing a task.|I'm working on my English pronunciation this month.|They're working on a plan for the school festival.|inseparable
drop out|okulu veya programı bırakmak|To stop taking part in a school program or organized activity.|He dropped out of the course after two weeks.|She almost dropped out but decided to finish the program.|intransitive
fall out|tartışıp küsmek|To have an argument and stop being friendly with someone.|They fell out over a misunderstanding about the money.|I don't want to fall out with my best friend over this.|intransitive
act up|yaramazlık yapmak, düzgün çalışmamak|To behave badly or fail to work as expected.|My phone started acting up during the video call.|The kids tend to act up when they're overtired.|intransitive
back away|geri çekilmek|To move backward from someone or something, especially in fear.|She backed away when the dog began to growl.|He slowly backed away from the edge of the roof.|intransitive
barge in|izinsiz ve aniden içeri girmek|To enter a room or interrupt without being invited.|He barged in while we were discussing the surprise.|Please knock instead of barging in on our meeting.|intransitive
beat up|dövmek, hırpalamak|To physically attack and seriously hurt someone.|The police arrested the men who beat him up.|He was beaten up during an argument outside the club.|separable
blow off|birini veya işi önemsemeyip ekmek|To ignore an obligation or a person instead of following through.|He blew off our plans without even sending a message.|Don't blow off the appointment just because you're tired.|separable
black out|bayılmak, geçici olarak bilincini kaybetmek|To temporarily lose consciousness or the ability to remember events.|He blacked out for a few seconds after hitting his head.|She said she blacked out and couldn't remember the fall.|intransitive
blend in|ortama uyum sağlamak, dikkat çekmemek|To look or behave like the people around you.|She wore a simple coat to blend in with the crowd.|It took time to blend in at the new school.|intransitive
blurt out|ağzından kaçırmak, düşünmeden söylemek|To say something suddenly without thinking first.|He blurted out the surprise before anyone could stop him.|I accidentally blurted out the answer during the quiz.|separable
bottle up|duygularını içine atmak|To hide feelings rather than express them.|She tends to bottle up her frustration until she feels overwhelmed.|Try not to bottle up everything that's bothering you.|separable
burn out|çok çalışmaktan tükenmek|To become exhausted from prolonged stress or overwork.|He burned out after months of working every weekend.|You might burn out if you never take a break.|intransitive
bump into|tesadüfen karşılaşmak|To meet someone you know unexpectedly by chance.|I bumped into our old neighbor at the grocery store.|She bumped into a college friend on the train.|inseparable
calm down|sakinleşmek, sakinleştirmek|To become less upset or to help someone feel calmer.|Take a minute to calm down before you respond.|The teacher calmed the children down after the alarm.|separable
call up|telefonla aramak|To phone someone, often to have a conversation.|I called up my brother to ask how he was doing.|She called her friend up after hearing the good news.|separable
""".strip()

def make():
 out=[]
 for lineno,line in enumerate(ROWS.splitlines(),1):
  parts=[s.strip() for s in line.split('|')]
  if len(parts)!=6:raise ValueError(f'bad row {lineno}: {parts}')
  word,tr,definition,first,second,syntax=parts
  if syntax not in {'separable','inseparable','intransitive'}:raise ValueError(word)
  note={'separable':'The object may go between verb and particle; pronoun objects usually do.',
        'inseparable':'Keep the particle or preposition attached to the verb before its object.',
        'intransitive':'No direct object is required in the sense illustrated here.'}[syntax]
  out.append({'word':word,'level':'B2','tr':tr,'definition':definition,'example':first,
              'examples':[first,second], 'syntax':syntax,'register':'neutral',
              'note':note,'levelEvidence':'Provisional educational estimate; source does not certify CEFR.',
              'levelStatus':'editorial_estimate_unverified','senses':[{'tr':tr,'definition':definition,'example':first}]})
 return out

if __name__=='__main__':
 file=ROOT/'sources/authored-20261028-conversational-phrasals.jsonl'
 file.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in make()),encoding='utf8')
 existing={x['word'].casefold() for x in json.loads((ROOT/'data/phrasals.json').read_text())}
 missing=[row for row in make() if row['word'].casefold() not in existing]
 if missing:
  pending=ROOT/'sources/.pending-20261028-phrasal.jsonl'
  try:
   pending.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in missing),encoding='utf8')
   result=process(pending,'phrasal',apply=True)
  finally: pending.unlink(missing_ok=True)
 else: result={'mode':'already_applied','validatedNewCards':0,'releaseReady':False}
 print(json.dumps(result,ensure_ascii=False))
