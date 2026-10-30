#!/usr/bin/env python3
"""Human-authored in-code conversation-first vocabulary batch; NOT independently reviewed.
No invented CEFR certification; levels remain imported source candidates.
"""
import json
from pathlib import Path
from promote_content_batch import process
ROOT=Path(__file__).resolve().parents[1]
# word|Turkish meaning|original English definition|context 1|context 2
ROWS='''
unfamiliar|tanıdık olmayan, yabancı|Not known to you because you have not seen or experienced it before.|This neighborhood feels unfamiliar after so many years away.|I'm unfamiliar with the rules, so could you explain them?
illustration|örnek çizim, görsel anlatım|A picture or example that makes an idea or story easier to understand.|The book has an illustration of every animal mentioned.|Let me give you an illustration of what I mean.
nerves|gerginlik, heyecan|Feelings of worry or tension before something challenging.|I had terrible nerves before meeting her parents.|Taking a few deep breaths helped calm my nerves.
moving|dokunaklı, duygulandırıcı|Causing strong feelings, especially sympathy or sadness.|His speech about his grandfather was deeply moving.|We watched a moving film about an unlikely friendship.
tender|şefkatli, nazik; hassas|Showing affection and care, or sensitive to touch.|She gave her son a tender hug before school.|The skin around my ankle is still tender after the fall.
stern|sert, ciddi, tavizsiz|Serious and strict, often in the way someone speaks or behaves.|Dad gave us a stern warning about driving too fast.|She looked stern, but she was actually very kind.
striking|çarpıcı, dikkat çekici|So unusual or impressive that it immediately attracts attention.|There's a striking view of the mountains from the porch.|I noticed a striking resemblance between the two sisters.
hastily|aceleyle, düşünmeden|Quickly and often without enough time to think carefully.|He hastily packed his bag and left for the airport.|I sent the message hastily and immediately regretted it.
intimate|samimi, yakın; özel|Very personal or close, particularly in a relationship or setting.|We had an intimate dinner with just a few close friends.|She shared some intimate details of her childhood.
midst|ortasında, tam içinde|The middle part of an activity, place, or period of time.|We're in the midst of planning our summer vacation.|The phone rang in the midst of our conversation.
manufacturing|imalat, üretim|The activity of making products, especially in large quantities.|The town has a long history of car manufacturing.|He works in manufacturing but wants to change careers.
migration|göç, yer değiştirme|The movement of people or animals from one area to another.|The documentary followed the annual migration of birds.|The family discussed migration after receiving a job offer abroad.
undoubtedly|şüphesiz, kuşkusuz|Used to say that something is certainly true or very likely.|She is undoubtedly the best cook in our family.|The delay was undoubtedly frustrating for everyone involved.
swift|hızlı, çabuk|Happening or moving in a very short amount of time.|The hotel staff took swift action when we complained.|We made a swift decision to take the earlier train.
margin|fark, marj; sayfa kenarı|The difference between two amounts, or the blank edge of a page.|We won the game by a very small margin.|She wrote a reminder in the margin of her notebook.
stake|riskte olan şey; pay, hisse|Something important that could be gained or lost in a situation.|There's a lot at stake if we miss the application deadline.|He has a personal stake in the success of the community center.
instinct|içgüdü, doğal sezgi|A natural feeling that guides how you react without deliberate thought.|My first instinct was to call my sister for advice.|Trust your instincts if a situation feels unsafe.
shipping|gönderim, kargo taşımacılığı|The process or cost of transporting goods to customers or places.|Shipping is free if your order is over fifty dollars.|The store sent me an update about the shipping delay.
skilled|becerikli, kalifiye|Having the training or ability needed to do something well.|She's a skilled photographer who works at local events.|Repairing that roof requires a skilled professional.
temporarily|geçici olarak|For a limited period of time rather than permanently.|We're temporarily staying with friends during the renovation.|The hiking trail is temporarily closed after heavy rain.
unconscious|baygın, bilinci kapalı|Not awake or aware of what is happening around you.|He was unconscious for a few moments after the accident.|The paramedics checked the unconscious passenger immediately.
idle|boşta, kullanılmayan; aylak|Not active, working, or being used at the present time.|The old playground has stood idle since last summer.|Try not to leave the car idling outside the house.
inspect|incelemek, kontrol etmek|To look at something carefully in order to check its condition.|Always inspect a used bicycle before you buy it.|The landlord came to inspect the damage after the leak.
suspicious|şüpheli, kuşkulu|Making you think something is wrong or someone may be dishonest.|I got a suspicious text asking for my bank password.|She became suspicious when the seller refused to answer.
supervision|gözetim, denetim|Watching or directing an activity to make sure it is done safely.|Children should swim only with adult supervision.|The trainees practiced under the supervision of an instructor.
subside|yatışmak, azalmak, dinmek|To become less intense or serious after a period of activity.|The rain finally began to subside before sunset.|Her anxiety subsided once she heard everyone was safe.
unwilling|isteksiz, razı olmayan|Not prepared or wanting to do what someone asks or suggests.|He was unwilling to drive in the heavy snow.|She seemed unwilling to talk about what had happened.
sincerity|samimiyet, içtenlik|The quality of genuinely meaning what you say or do.|I could hear the sincerity in her apology.|Her sincerity made it easier for everyone to trust her.
modest|mütevazı, ölçülü|Not acting as if you are better than others, or small in size.|He stayed modest despite winning the award.|We're planning a modest celebration with a few friends.
misleading|yanıltıcı, yanlış izlenim veren|Giving someone an idea that is not true or accurate.|The photo is misleading because the room is actually tiny.|Her brief answer gave a misleading impression of the problem.
unaware|habersiz, farkında olmayan|Not knowing that something exists or has happened.|I was unaware that the meeting had been moved.|She walked past, completely unaware that we were waving.
unreasonable|mantıksız, makul olmayan|Not fair or sensible in a particular situation.|It seems unreasonable to expect an answer at midnight.|The landlord made an unreasonable demand about the deposit.
troublesome|sorun çıkaran, zahmetli|Causing repeated problems or difficulty.|That old washing machine has become troublesome lately.|The most troublesome part of the trip was finding parking.
superb|mükemmel, harika|Extremely good in quality or skill.|The restaurant served a superb dinner last night.|She did a superb job organizing the surprise party.
trait|özellik, kişilik niteliği|A particular quality in someone's personality or character.|Patience is a trait I admire in good teachers.|His most noticeable trait is his sense of humor.
alienate|yabancılaştırmak, kendinden uzaklaştırmak|To make someone feel excluded or disconnected from other people.|His constant jokes began to alienate his new coworkers.|You can disagree without alienating your friends.
allege|iddia etmek, öne sürmek|To state that someone has done something wrong without proving it.|The neighbors allege that the noise continues after midnight.|The article alleged that the company had hidden the problem.
altruism|özgecilik, karşılık beklemeden iyilik|Concern for other people's well-being rather than personal gain.|Her volunteering comes from genuine altruism.|The rescue effort showed remarkable altruism in the community.
altruistic|özgeci, fedakâr|Caring about helping other people without expecting a reward.|An altruistic neighbor offered to buy groceries for everyone.|He made an altruistic decision to donate his prize money.
appalling|berbat, dehşet verici|Extremely bad or shocking in a way that causes strong disapproval.|The conditions in the temporary shelter were appalling.|I was shocked by the appalling customer service.
assertion|iddia, kesin ifade|A statement made confidently, even though it may need evidence.|His assertion that the road was safe surprised everyone.|She challenged the assertion that nobody wanted the change.
avid|hevesli, tutkulu|Very enthusiastic about an activity or interest.|My aunt is an avid reader of historical novels.|He's an avid runner who goes out before breakfast.
boast|övünmek, böbürlenmek|To talk with too much pride about what you have or have done.|He likes to boast about how quickly he finishes puzzles.|She never boasts about her achievements.
bribe|rüşvet vermek; rüşvet|To offer something valuable to make a person act dishonestly.|Someone tried to bribe the official to avoid a fine.|The officer refused the bribe and reported the incident.
bribery|rüşvetçilik, rüşvet verme|The act of offering or taking money to influence someone dishonestly.|The mayor faced serious allegations of bribery.|The organization introduced stricter rules against bribery.
candid|açık sözlü, samimi|Honest and direct about what you really think or feel.|Can I be candid with you about the new plan?|Her candid advice helped me avoid a costly mistake.
candidly|açıkça, dürüstçe|In an honest and straightforward way without hiding your opinion.|He spoke candidly about his fears before the trip.|Candidly, I don't think that restaurant is worth the price.
collaboration|iş birliği, ortak çalışma|Working together with others to create or achieve something.|The neighborhood festival was a collaboration between three groups.|Good collaboration made planning the trip much easier.
collaborative|iş birliğine dayanan, ortak|Involving people working together and sharing ideas or responsibilities.|We took a collaborative approach to planning the wedding.|She prefers a collaborative environment over constant competition.
commend|övmek, takdir etmek|To express approval or praise for someone's actions.|I want to commend the staff for handling the delay so calmly.|The teacher commended her for helping a classmate.
compliant|kurallara uyan, uyumlu|Following rules, requests, or standards that apply in a situation.|The renovated building is now compliant with fire regulations.|The company wants its packaging to be compliant with local rules.
comprise|oluşmak, kapsamak|To consist of the parts or people that make up a whole.|The hiking group comprises six adults and two children.|The meal comprises a starter, a main course, and dessert.
compulsion|karşı konulmaz dürtü, zorlantı|A very strong feeling that you must do something, even if you do not want to.|I felt a strange compulsion to check the door one more time.|He described a compulsion to keep every old receipt.
concur|aynı fikirde olmak, katılmak|To agree with another person's opinion or conclusion.|I concur with your suggestion to leave earlier.|Most of the committee members concurred with the decision.
confide|sır vermek, güvenerek anlatmak|To share private feelings or information with someone you trust.|She confided in me about her worries at home.|He found it easier to confide in his older brother.
conformity|uyum, kurallara uymak|Behavior that follows established rules or social expectations.|The school values creativity over strict conformity.|He felt pressure toward conformity when he started the new job.
conscientious|titiz, özenli, sorumluluk sahibi|Taking great care to do something properly and responsibly.|She's a conscientious driver who always checks her mirrors.|His conscientious preparation made the trip run smoothly.
conscientiously|titizlikle, özenle|In a careful and responsible way that shows attention to detail.|He conscientiously checked every item on the packing list.|She conscientiously followed the doctor's instructions.
conserve|tasarruf etmek, korumak|To save or protect a resource by using as little as necessary.|We try to conserve water during the summer.|Turn off the lights to conserve energy while you're away.
convoluted|karmaşık, dolambaçlı|Too complicated or difficult to follow or understand easily.|The directions were so convoluted that we got lost.|He gave a convoluted explanation for a simple mistake.
criteria|ölçütler, kriterler|The standards used to judge or choose between different options.|Location and price are our main criteria for an apartment.|What criteria did you use to choose this language course?
cynical|alaycı, insanlardan kuşkulanan|Believing that people are mostly motivated by selfish interests.|He became cynical after hearing too many empty promises.|Don't be so cynical about someone offering help.
cynically|alaycı biçimde, kuşkuyla|In a way that shows distrust of people's motives or sincerity.|She cynically assumed that the gift came with conditions.|He cynically joked that the apology was just for publicity.
cynicism|alaycılık, güvensizlik|A tendency to distrust people's sincerity or good intentions.|Years of disappointment had turned his hope into cynicism.|Her cynicism made it hard to accept genuine compliments.
confinement|kapalı yerde tutulma, kısıtlanma|Being kept within a limited space or prevented from moving freely.|After a week of confinement indoors, the kids needed fresh air.|The long confinement made the rescued animals nervous.
detest|nefret etmek, hiç sevmemek|To strongly dislike someone or something.|I detest being interrupted in the middle of a story.|She detests the sound of people chewing loudly.
disdain|küçümseme, hor görme|A strong feeling that someone or something is beneath your respect.|He looked at the cheap furniture with obvious disdain.|She spoke with disdain about people who took the bus.
divergent|birbirinden farklı, ayrışan|Developing in different directions or holding quite different views.|We had divergent opinions about where to go on vacation.|Their divergent plans made it hard to choose a date.
dither|kararsız kalmak, tereddüt etmek|To spend too much time hesitating over a decision.|Don't dither too long or the tickets will sell out.|I dithered between the blue jacket and the green one.
enviable|gıpta edilecek, imrenilecek|So good or desirable that other people wish they had it.|She has an enviable view of the ocean from her balcony.|His enviable work schedule leaves plenty of time for family.
exuberant|coşkulu, enerjik|Full of excitement, energy, or cheerful enthusiasm.|The children were exuberant after the school play.|Her exuberant greeting made everyone feel welcome.
exuberance|coşku, taşkın sevinç|Very lively, cheerful energy and enthusiasm.|The crowd's exuberance filled the street after the victory.|I love the exuberance of the neighborhood summer festival.
extortion|şantajla para alma, haraç|The illegal act of getting money through threats or force.|The business owner reported the attempted extortion to police.|They were arrested on suspicion of extortion.
flattery|yağcılık, aşırı övgü|Praise that is often exaggerated to gain someone's favor.|He tried flattery to persuade the teacher to extend the deadline.|I prefer honest feedback to empty flattery.
heighten|artırmak, yoğunlaştırmak|To make a feeling, quality, or situation stronger or more intense.|The unexpected silence heightened everyone's anxiety.|Warm lighting can heighten the cozy feeling of a room.
hypocrisy|ikiyüzlülük, riyakârlık|Behavior that contradicts the moral standards someone claims to have.|She accused him of hypocrisy for breaking his own rules.|People noticed the hypocrisy in his criticism of others.
hypocrite|ikiyüzlü kişi, riyakâr|Someone who criticizes behavior that they themselves also practice.|He called me a hypocrite for telling him not to be late.|Nobody likes being judged by a hypocrite.
hypocritical|ikiyüzlü, riyakâr|Claiming to have standards while behaving in ways that violate them.|It's hypocritical to complain about noise while playing loud music.|She admitted it was hypocritical to ignore her own advice.
impede|engellemek, zorlaştırmak|To slow down or block someone's progress or ability to act.|Heavy rain may impede traffic on the mountain road.|The cluttered hallway impeded our efforts to move the couch.
impediment|engel, güçlük|Something that makes it difficult to do or achieve something.|A lack of transportation was an impediment to attending classes.|His injury became a temporary impediment to hiking.
impersonal|kişisel olmayan, soğuk|Not showing warmth or individual attention toward someone.|The hotel felt efficient but strangely impersonal.|I don't like sending an impersonal message after a breakup.
impoverished|yoksullaşmış, çok fakir|Having very little money or the resources needed for basic living.|The charity provided meals to impoverished families.|She grew up in an impoverished rural community.
inclusion|dahil etme, kapsayıcılık|Making sure people are welcomed and able to participate.|The club wants to improve inclusion at its events.|Small acts of inclusion can help new neighbors feel welcome.
inclusive|kapsayıcı, herkesi içeren|Designed to welcome and include people with different needs.|They chose an inclusive activity that everyone could enjoy.|The event offered inclusive seating for people with disabilities.
individuality|bireysellik, kendine özgülük|The qualities that make a person different from everyone else.|Her unusual clothing reflects her individuality.|The school encourages students to express their individuality.
inexcusable|affedilemez, mazur görülemez|So bad or wrong that no acceptable excuse can justify it.|His rude behavior toward the waiter was inexcusable.|Leaving a child alone in that situation would be inexcusable.
inexplicable|açıklanamaz, anlaşılması zor|Very difficult or impossible to explain or understand.|There was an inexplicable noise coming from the attic.|His sudden change of mind seemed inexplicable to everyone.
inherently|doğası gereği, özünde|In a way that is a natural or essential part of something.|Traveling alone isn't inherently dangerous if you plan carefully.|A disagreement isn't inherently a sign of a bad relationship.
innovate|yenilik yapmak, yeni yöntem geliştirmek|To introduce a new idea or method that makes something better.|Small businesses often innovate to meet changing customer needs.|The bakery continues to innovate with new seasonal recipes.
insecure|güvensiz hisseden, kendinden emin olmayan|Feeling unsure of yourself, your abilities, or your relationships.|He felt insecure about his accent when speaking English.|She sometimes feels insecure in large social gatherings.
insightful|anlayışlı, isabetli gözlemler yapan|Showing a deep and accurate understanding of a situation.|That was an insightful question about the family's plans.|Her insightful comments helped us see the problem differently.
instinctive|içgüdüsel, sezgisel|Happening naturally without needing conscious thought.|Her instinctive reaction was to catch the falling glass.|He made an instinctive move to protect his younger brother.
insubordinate|itaatsiz, yetkiliye karşı gelen|Refusing to follow reasonable instructions from someone in authority.|The supervisor said his repeated refusals were insubordinate.|She was disciplined for insubordinate behavior at work.
integral|vazgeçilmez, ayrılmaz parça|Essential to the proper working or success of something.|Good communication is integral to a healthy relationship.|Music is an integral part of the family's celebrations.
intuition|sezgi, içgörü|An immediate feeling about something without conscious reasoning.|My intuition told me to take a different route home.|She trusted her intuition when choosing a roommate.
intuitive|sezgisel, kolay kavranır|Easy to understand or use without detailed explanation.|The ticket machine has a surprisingly intuitive interface.|His explanation was clear and intuitive for beginners.
intuitively|sezgisel olarak, içinden gelerek|By relying on a natural feeling rather than a detailed analysis.|She intuitively understood that he needed some space.|I intuitively reached for the familiar route to school.
irate|çok kızgın, öfkeli|Extremely angry about something that has happened.|An irate customer complained about the canceled flight.|Dad was irate when he discovered the broken window.
lapse|kısa süreli hata, aksama; geçersiz kalmak|A temporary failure in attention or a period when something stops being valid.|I had a lapse in concentration and missed the turn.|Don't let your travel insurance lapse before the trip.
legacy|miras, kalıcı iz|The lasting effect someone or something leaves behind.|Her kindness is the legacy her friends remember most.|The community garden is a legacy of years of volunteer work.
lethargic|halsiz, uyuşuk, enerjisiz|Feeling unusually tired and lacking energy or motivation.|I felt lethargic after staying up too late.|The dog seemed lethargic, so we called the vet.
lethargy|halsizlik, bitkinlik|A state of low energy and little interest in activity.|A few days of poor sleep left him struggling with lethargy.|She noticed a sense of lethargy after the long trip.
liaison|irtibat görevlisi, bağlantı kişisi|Someone who helps different people or groups communicate.|She acted as a liaison between the parents and the school.|Our neighborhood liaison helped resolve the parking issue.
likelihood|olasılık, ihtimal|How probable it is that something will happen.|The likelihood of rain increases after sunset.|What's the likelihood of getting tickets at the door?
ludicrous|saçma, gülünç derecede mantıksız|So unreasonable or ridiculous that it is hard to take seriously.|It's ludicrous to charge that much for a bottle of water.|His excuse for missing the flight sounded ludicrous.
malfunction|arızalanmak, bozulma|To stop working correctly, or a failure in a device or system.|The elevator began to malfunction during the storm.|A minor malfunction delayed the train by twenty minutes.
manipulation|manipülasyon, yönlendirme|Controlling someone's choices or feelings in an unfair or hidden way.|She recognized the emotional manipulation in his messages.|The documentary discussed manipulation through misleading advertisements.
methodical|sistemli, titiz, planlı|Working in an organized way by following a clear sequence.|He took a methodical approach to cleaning the garage.|Her methodical packing saved time at the airport.
mingle|kaynaşmak, insanlarla sohbet etmek|To move among people and talk casually in a social setting.|I tried to mingle with the other guests at the party.|The host encouraged everyone to mingle before dinner.
mutually|karşılıklı olarak, iki tarafça|In a way that is shared or agreed by both people or sides.|We mutually agreed to cancel the weekend trip.|The neighbors found a mutually acceptable solution.
negligent|ihmalkâr, dikkatsiz|Failing to take the care that a situation reasonably requires.|It was negligent to leave the gate open near the road.|The company was accused of negligent maintenance of the stairs.
negligible|ihmal edilebilir, çok küçük|So small or unimportant that it has little practical effect.|The difference in ticket prices is negligible.|The amount of sugar in the sauce is negligible.
niche|özel alan, dar ilgi alanı|A small or specialized market, role, or area of interest.|She found her niche teaching yoga to older adults.|That bookstore caters to a niche group of readers.
notable|dikkate değer, önemli|Especially worth noticing because it is unusual or important.|There was a notable improvement in his pronunciation.|One notable feature of the hotel is its rooftop garden.
oblige|mecbur bırakmak; iyilik yapmak|To make someone feel required to do something, or willingly help them.|I'd be happy to oblige if you need a ride home.|The new rule obliges drivers to carry proof of insurance.
occupational|meslekle ilgili, işle ilgili|Related to someone's job, working conditions, or profession.|The clinic offers occupational health checkups.|Occupational stress can affect sleep and mood.
oversee|denetlemek, gözetmek|To be responsible for watching and directing an activity or project.|My aunt will oversee the renovation while we're away.|She oversees the volunteers at the animal shelter.
perpetuate|sürdürmek, devam ettirmek|To make a belief, situation, or problem continue over time.|Repeating that rumor will only perpetuate the confusion.|Old habits can perpetuate problems in a friendship.
pertinent|ilgili, yerinde|Directly related and useful to the topic being discussed.|That's a pertinent question about the cost of the trip.|Please keep your comments pertinent to the main issue.
phenomenal|olağanüstü, inanılmaz derecede iyi|Unusually great or impressive in amount, quality, or success.|The singer gave a phenomenal performance last night.|The support from our neighbors has been phenomenal.
ploy|hile, taktik, kurnazca hamle|A clever and sometimes dishonest move used to gain an advantage.|The supposed discount was a ploy to attract customers.|He used a playful ploy to get the children to tidy up.
plummet|hızla düşmek, çakılmak|To fall very quickly and often by a large amount.|The temperature began to plummet after sunset.|My phone battery level plummeted during the video call.
plunge|dalmak, birden düşmek|To move suddenly downward or into something, often very quickly.|The kids plunged into the swimming pool after lunch.|Ticket sales plunged when the weather turned bad.
portray|canlandırmak, tasvir etmek|To show someone or something in a particular way through words or art.|The film portrays the family as warm and welcoming.|The article portrayed the neighborhood as dangerous.
portrayal|tasvir, canlandırma|The way a person or situation is represented in a story or image.|I liked her portrayal of the main character.|The show's portrayal of city life felt surprisingly realistic.
predecessor|selef, kendisinden önceki kişi|The person or thing that held a position before another.|The new manager thanked her predecessor for the support.|This phone is much lighter than its predecessor.
premise|temel varsayım, öncül|An idea that forms the starting point of an argument or plan.|The whole plan rests on the premise that the store stays open.|I disagree with the basic premise of that argument.
privileged|ayrıcalıklı, imtiyazlı|Having special benefits or opportunities that many others do not.|We feel privileged to live so close to the sea.|She grew up in a privileged neighborhood.
prohibitive|aşırı pahalı, engelleyici|So expensive or difficult that it prevents something from happening.|The cost of parking downtown is prohibitive.|For some families, the travel expenses are prohibitive.
proliferate|hızla çoğalmak, yayılmak|To increase or spread quickly in number.|Small coffee shops began to proliferate in the neighborhood.|Rumors proliferated after the unexpected announcement.
prolific|üretken, verimli|Producing a large amount of work, ideas, or results.|She's a prolific writer who publishes several books a year.|The garden was especially prolific this summer.
prospective|muhtemel, gelecekteki|Likely to become something or happen in the future.|The landlord showed the apartment to prospective tenants.|Prospective students can visit the school next Saturday.
provocative|kışkırtıcı, tartışma yaratan|Likely or intended to make people angry, interested, or ready to argue.|His provocative comment started a heated discussion.|The exhibition featured some provocative artwork.
provoke|kışkırtmak, bir tepki doğurmak|To cause a strong reaction or deliberately make someone angry.|The sudden price increase provoked complaints from customers.|Try not to provoke an argument over something so small.
rarity|nadirlik, ender görülen şey|Something unusual or not often found or experienced.|A quiet street like this is a rarity downtown.|Snow in this area is something of a rarity.
rediscover|yeniden keşfetmek, tekrar fark etmek|To find or enjoy something again after forgetting about it.|I rediscovered my love of painting during the holidays.|She rediscovered an old photo album while moving.
refurbish|yenilemek, elden geçirmek|To repair and improve something old so that it looks or works better.|We plan to refurbish the kitchen rather than replace it.|They refurbished the old library last year.
refurbishment|yenileme, tadilat|Work that repairs or improves an older building or object.|The hotel closed for refurbishment over the winter.|Our apartment's refurbishment took longer than expected.
relinquish|vazgeçmek, bırakmak|To give up something, especially control, possession, or a right.|She reluctantly relinquished her seat on the committee.|He agreed to relinquish control of the family business.
reminisce|eski günleri anmak|To talk pleasantly about things you remember from the past.|We spent the evening reminiscing about our school days.|My grandparents love to reminisce about their first home.
reminiscent|anımsatan, çağrıştıran|Making you remember someone or something from the past.|The smell of cinnamon was reminiscent of my childhood.|Her singing style is reminiscent of old jazz records.
repel|uzaklaştırmak, püskürtmek|To push something away or cause someone to feel strong dislike.|This spray helps repel mosquitoes on summer evenings.|His rude behavior repelled several potential customers.
resonate|yankı bulmak, güçlü etki bırakmak|To produce a strong emotional response or seem personally meaningful.|Her story resonated with everyone who had moved away from home.|The message about friendship really resonated with me.
respite|kısa mola, dinlenme fırsatı|A short period of rest or relief from something difficult.|The weekend gave us a welcome respite from the noise.|A quiet afternoon was a respite from the hectic week.
ruthless|acımasız, merhametsiz|Willing to hurt others or act without sympathy to achieve a goal.|The villain in the movie was completely ruthless.|She criticized the ruthless way the staff were treated.
'''.strip()

def records():
    data=[]
    for n,line in enumerate(ROWS.splitlines(),1):
        a=[x.strip() for x in line.split('|')]
        if len(a)!=5:raise ValueError(f'line {n} has {len(a)} fields: {line[:55]}')
        word,tr,definition,one,two=a
        data.append({'word':word,'tr':tr,'definition':definition,'example':one,'examples':[one,two],
                     'prompt':f'Explain or use “{word}” in a real-life sentence.'})
    return data

def run():
    focus={x['word']:x['level'] for x in json.loads((ROOT/'data/fluency-focus.json').read_text())['vocabulary']}
    source={x['word']:x['levelCandidate'] for x in json.loads((ROOT/'sources/general-production-queue.json').read_text())}
    source.update({x['word']:x['levelCandidate'] for x in json.loads((ROOT/'sources/b2-c1-offline-catalog.json').read_text()) if x['word'] not in source})
    known={x['word'] for x in json.loads((ROOT/'data/vocabulary.json').read_text()) if x.get('category')=='general'}
    rows=records()
    for row in rows:
        w=row['word']
        if w not in focus or w not in source or focus[w]!=source[w]:raise ValueError(f'{w} level or selection disagreement: {focus.get(w)},{source.get(w)}')
        row['level']=focus[w]
        row['levelStatus']='source_candidate_unreviewed'
    if len({r['word'] for r in rows})!=len(rows):raise ValueError('duplicate source words')
    pending=[r for r in rows if r['word'] not in known]
    path=ROOT/'sources'/'authored-20261028-fluency-general.jsonl'
    path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf8')
    if pending:
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf8',suffix='.jsonl',delete=False) as f:
            tmp=Path(f.name)
            f.write(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in pending))
        try:
            result=process(tmp,'general',apply=True)
        finally:
            tmp.unlink(missing_ok=True)
    else:result={'validatedNewCards':0,'mode':'already_applied','releaseReady':False}
    print(json.dumps({'authoredSourceCards':len(rows),'selectedB2':sum(r['level']=='B2' for r in rows),'selectedC1':sum(r['level']=='C1' for r in rows),'import':result},ensure_ascii=False))

if __name__=='__main__':run()
