#!/usr/bin/env python3
"""Hand-authored, conversational US-English vocabulary draft sprint.

Each record has an independently written definition and two meaningful different
situations. It uses an existing sourced focus headword, never grants editorial
approval, and keeps existing lesson IDs and SRS history intact.
"""
from __future__ import annotations
import json
from pathlib import Path
from promote_content_batch import process

ROOT = Path(__file__).resolve().parents[1]
ROWS = '''
submit|sunmak, teslim etmek|To formally give a document or request for consideration.|You have until Friday to submit your application.|I submitted the insurance claim online last night.
haste|acele, telaş|Excessive speed that can lead to careless decisions.|In her haste to leave, she forgot her wallet.|There's no need for haste; the train won't leave for an hour.
toll|geçiş ücreti; ağır bedel|A charge for using a road, or a harmful effect over time.|We paid the bridge toll with a credit card.|Working without enough sleep took a toll on his health.
uncommon|alışılmadık, ender|Not often seen, heard, or experienced.|It's uncommon to see snow here in April.|That name is uncommon, but it's easy to remember.
spare|yedek; ayırmak, zaman bulmak|Extra and available, or to give time or resources to something.|Do you have a spare phone charger I could borrow?|Can you spare ten minutes to help me carry these boxes?
impressed|etkilenmiş, hayran kalmış|Feeling admiration because something is unusually good.|I was impressed by how calmly she handled the delay.|My parents were impressed with the food at your restaurant.
improved|geliştirilmiş, iyileştirilmiş|Made better than an earlier version or state.|The improved bus service makes commuting easier.|His pronunciation improved after he practiced every evening.
invisible|görünmez|Unable to be seen, even though it is there.|The stain was almost invisible in the dim light.|The small scratch is invisible unless you look closely.
irresistible|karşı konulmaz, dayanılmaz|So appealing that it is difficult to refuse or ignore.|The smell of freshly baked bread was irresistible.|She found the offer of a free weekend trip irresistible.
institution|kurum, kuruluş|An established organization serving a public, educational, or social purpose.|She applied for a scholarship at a respected institution.|The museum is an important cultural institution in the city.
stiff|sert; tutulmuş|Hard to bend or move, sometimes because of muscle pain.|My shoulders feel stiff after that long flight.|These new shoes are stiff, so I need to break them in.
initial|ilk, başlangıçtaki|Happening at the beginning of a process or situation.|My initial reaction was to say no.|The initial estimate was lower than the final repair bill.
inquire|sormak, bilgi almak|To ask for information, especially in a polite or formal way.|I called the hotel to inquire about late checkout.|You can inquire at the front desk about lost luggage.
insult|hakaret etmek; hakaret|A rude remark or action that shows disrespect.|I didn't mean to insult you with that joke.|She took his comment about her cooking as an insult.
landing|iniş; sahanlık|The act of arriving on the ground from the air, or a flat area by stairs.|The pilot announced that our landing would be delayed.|Leave the box on the landing outside the apartment.
manufacture|üretmek, imal etmek|To make products, usually in large numbers using machinery.|The company manufactures bicycles in Ohio.|These kitchen appliances are manufactured locally.
muddy|çamurlu, bulanık|Covered with mud or made unclear by dirt or confusion.|The children came home with muddy shoes.|The path was so muddy that we turned around.
sob|hıçkırarak ağlamak|To cry with loud, uneven breaths.|She started to sob when she heard the sad news.|I could hear someone sobbing in the next room.
toxic|zehirli; zarar verici|Containing poison or causing serious harm, physically or socially.|Keep toxic cleaning chemicals away from children.|He decided to leave a toxic friendship behind.
soaked|sırılsıklam, tamamen ıslanmış|Completely wet from rain, water, or another liquid.|We got soaked walking home without umbrellas.|My socks were soaked after I stepped in the puddle.
strictly|kesinlikle; sıkı biçimde|Exactly or firmly, with little room for exceptions.|The apartment is strictly nonsmoking.|Strictly speaking, the concert starts at eight, not seven.
successive|art arda gelen|Following one another without interruption.|It rained for three successive days.|The store raised prices in two successive months.
tenderly|şefkatle, nazikçe|In a gentle, loving, or careful manner.|She tenderly wrapped the baby in a blanket.|He held the injured bird tenderly in his hands.
tutor|özel öğretmen; özel ders vermek|A person who teaches someone individually or in a small group.|I hired a tutor to help me improve my pronunciation.|Her tutor explained the grammar rule in simpler terms.
ironically|ironik biçimde|In a way that is unexpected or opposite to what one might expect.|Ironically, the weather improved as soon as we canceled the picnic.|He bought a new umbrella but ironically left it at home.
skillful|becerikli, usta|Showing a high degree of ability or careful technique.|She's a skillful cook who can make anything taste good.|The dentist's skillful work made the procedure much easier.
thrill|heyecan, büyük coşku|A strong feeling of excitement or pleasure.|It was a thrill to see the ocean for the first time.|She gets a thrill from trying new activities.
ultimate|nihai, en son, en önemli|Final or most important after everything else is considered.|Our ultimate goal is to buy a small house near the beach.|The ultimate decision belongs to the person paying for the trip.
impatiently|sabırsızca|In a way that shows frustration about waiting.|The children waited impatiently for the movie to start.|He tapped his foot impatiently in the long line.
mobility|hareketlilik, hareket kabiliyeti|The ability to move easily or travel from one place to another.|Regular stretching can improve your mobility.|The new ramp makes the building easier to use for people with limited mobility.
sparkling|ışıltılı; gazlı|Shining with small flashes of light, or containing fizzy bubbles.|She ordered sparkling water instead of soda.|The lake looked sparkling in the morning sunlight.
unchanged|değişmemiş, aynı kalan|Remaining exactly the same as it was before.|The train schedule has remained unchanged for months.|Despite the repairs, the apartment's layout is unchanged.
humiliating|küçük düşürücü, utandırıcı|Making someone feel deeply embarrassed or ashamed.|Forgetting her name in front of everyone was humiliating.|He described the public criticism as a humiliating experience.
irritating|sinir bozucu, rahatsız edici|Causing mild anger, discomfort, or frustration.|That dripping faucet makes an irritating noise.|It's irritating when someone interrupts every sentence.
lawn|çimenlik, bahçe çimi|An area of short grass around a house or park.|We had lunch on the lawn behind the house.|He mows the front lawn every Saturday morning.
suppress|bastırmak, engellemek|To prevent a feeling, action, or information from being expressed or spreading.|I tried to suppress a laugh during the serious meeting.|She couldn't suppress her excitement about the surprise.
hint|ipucu, ima|A small piece of information that helps someone understand or guess something.|Can you give me a hint about the birthday present?|There was a hint of sadness in her voice.
intent|niyet; kararlı|A plan or purpose behind an action, or very focused attention.|I had no intent to upset anyone with my remark.|She was intent on finishing the book before bedtime.
momentary|anlık, çok kısa süren|Lasting for only a very short time.|There was a momentary pause before everyone applauded.|A momentary distraction made him miss the turn.
uneven|düzensiz, engebeli; eşit olmayan|Not smooth, level, or equal from one part to another.|Be careful walking on the uneven sidewalk.|The cake baked unevenly because the oven was too hot.
humiliation|aşağılanma, küçük düşürülme|A strong feeling of shame caused by being treated disrespectfully.|He felt deep humiliation after being mocked in public.|Nobody deserves the humiliation of being shouted at in a store.
ignorant|cahil; habersiz|Not knowing important facts about a subject or situation.|I was ignorant of the parking restrictions in that area.|He apologized for making an ignorant comment.
mask|maske; örtmek|A covering worn over the face, or something used to hide a feeling.|She wore a mask while sanding the old furniture.|He tried to mask his disappointment with a smile.
technical|teknik, uzmanlık gerektiren|Related to specialized skills, equipment, or practical details.|We had a technical problem with the ticket machine.|Could you explain that without using technical terms?
imprisonment|hapis, tutukluluk|The state of being kept in prison as a punishment.|The judge sentenced him to two years of imprisonment.|The documentary follows a family affected by wrongful imprisonment.
interpretation|yorum, anlamlandırma|A particular understanding or explanation of something.|My interpretation of her message was completely wrong.|There are several possible interpretations of that ending.
loosely|gevşekçe, kabaca|In a way that is not tight, exact, or strictly controlled.|Tie the scarf loosely around your neck.|The movie is loosely based on a real story.
modification|değişiklik, uyarlama|A small change made to improve or adapt something.|We made a modification to the travel schedule.|The chair needs a minor modification to fit under the desk.
temptation|ayartı; dayanılmaz istek|A strong desire to do something that might not be wise.|I resisted the temptation to check my phone during dinner.|The smell of cookies was too much temptation for the kids.
threaten|tehdit etmek; tehdit oluşturmak|To warn that you may cause harm, or to put something at risk.|Don't threaten to quit every time you disagree.|Dark clouds threatened to ruin our picnic.
unsatisfactory|yetersiz, tatmin edici olmayan|Not good enough to meet reasonable expectations.|The hotel's response to our complaint was unsatisfactory.|She returned the shoes because the quality was unsatisfactory.
infect|bulaştırmak, enfekte etmek|To pass a disease or harmful microorganism to someone or something.|Stay home if you're sick so you don't infect others.|A small cut can become infected if it isn't kept clean.
leisurely|acele etmeden, rahatça|Done slowly and without being hurried.|We enjoyed a leisurely breakfast on Sunday.|They took a leisurely walk along the waterfront.
sketch|taslak, eskiz; kabaca çizmek|A quick drawing or a rough outline of an idea.|She drew a sketch of the garden layout.|Can you sketch what the new kitchen might look like?
snap|birden kırılmak, çıtlamak; terslemek|To break or react suddenly with a sharp sound or movement.|The thin branch snapped under his foot.|I snapped at my brother because I was exhausted.
hospitality|misafirperverlik, konukseverlik|Friendly and generous treatment of guests or visitors.|Their hospitality made us feel at home immediately.|She thanked her neighbors for their warm hospitality.
identification|kimlik tespiti; kimlik belgesi|The process or document used to establish who someone is.|Please bring photo identification to the appointment.|The identification of the missing bag took an hour.
impose|dayatmak; uygulamak|To force a rule, cost, or decision to be accepted.|The city plans to impose a fine for illegal parking.|I don't want to impose my opinions on anyone.
indebted|borçlu; minnettar|Owing money or feeling deeply grateful to someone.|I'm indebted to my sister for helping with the move.|After the repairs, the family was heavily indebted.
luxurious|lüks, çok konforlu|Very comfortable, beautiful, or expensive beyond ordinary needs.|The hotel room felt luxurious after our long journey.|She bought a luxurious blanket for the winter.
mortgage|konut kredisi, ipotek|A loan used to buy property, usually repaid over many years.|Our mortgage payment increased after the rate changed.|They're saving for a down payment before applying for a mortgage.
multiply|çoğalmak; çarpmak|To increase in number, or calculate a number using multiplication.|The weeds multiply quickly after heavy rain.|Multiply the price by three to find the total cost.
neat|düzenli, temiz; hoş|Tidy and well organized, or pleasantly impressive.|His room is always neat and organized.|That's a neat trick for folding a fitted sheet.
nervously|gergin şekilde, endişeyle|In a way that shows worry or fear about what may happen.|She laughed nervously before the interview began.|He checked the time nervously as the train was delayed.
transmission|iletim; araç şanzımanı|The process of sending something, or the system that transfers power in a vehicle.|The car's transmission needs to be checked.|The radio transmission stopped during the storm.
underground|yer altında; gizli|Beneath the ground, or operating secretly outside normal systems.|The subway runs underground through the city center.|There's an underground parking garage beneath the mall.
unlimited|sınırsız|Not restricted in amount, number, or time.|The monthly plan includes unlimited calls.|The museum pass offers unlimited visits for one year.
unrest|huzursuzluk, toplumsal kargaşa|A period of public disorder or widespread dissatisfaction.|The city canceled the festival because of civil unrest.|The news reported unrest after the sudden policy change.
unsuitable|uygun olmayan, elverişsiz|Not right or safe for a particular purpose.|These shoes are unsuitable for hiking in the rain.|The movie is unsuitable for very young children.
upright|dik, dikey; dürüst|Standing or sitting straight, or behaving honestly.|Keep the glass upright so it doesn't spill.|She sat upright when the doctor entered the room.
harmless|zararsız, tehlikesiz|Unable or unlikely to cause harm.|Don't worry, that little spider is harmless.|It was meant as a harmless joke, not an insult.
humane|insancıl, merhametli|Showing kindness and concern for people or animals.|The shelter is known for its humane treatment of animals.|They searched for a more humane solution to the problem.
imitation|taklit, sahte benzer|A copy of something, usually less valuable than the original.|The bag was a cheap imitation of a designer brand.|Her imitation of the actor's voice made us laugh.
inherit|miras almak; kalıtımla edinmek|To receive property or characteristics from earlier generations.|She inherited her grandfather's old guitar.|He seems to have inherited his mother's sense of humor.
intrusion|izinsiz giriş, müdahale|An unwanted entry into a place or a private situation.|The alarm warned us of an intrusion into the building.|I hope my question doesn't feel like an intrusion.
literally|kelimenin tam anlamıyla|In the exact, nonfigurative sense of a word or statement.|The path was literally covered in ice.|When I said the store was empty, I meant literally nobody was there.
mastery|ustalık, tam hâkimiyet|A very high level of knowledge or skill in something.|Her mastery of the piano was clear from the first song.|It takes years of practice to develop mastery of a language.
media|medya; iletişim araçları|The channels through which news, entertainment, or messages reach people.|The local media covered the festival all weekend.|We try to limit our social media use before bed.
spark|kıvılcım; tetiklemek|A tiny flash of fire, or something that starts a feeling or event.|A spark from the fireplace landed on the rug.|The conversation sparked an idea for our next trip.
suburb|banliyö, şehir dışı yerleşim|A residential area outside the center of a city.|They moved to a quiet suburb when their daughter was born.|The last bus to our suburb leaves at midnight.
supplement|ek, takviye etmek|Something added to make an existing thing more complete.|She uses podcasts to supplement her English lessons.|The brochure is a supplement to the online guide.
testimony|tanıklık, ifade|A formal statement given as evidence, especially in court.|The witness gave testimony about the accident.|Her testimony helped explain what happened that night.
tiresome|yorucu, bıktırıcı|Annoying or boring because it requires too much patience.|The repeated delays made the trip tiresome.|It became tiresome to answer the same question every day.
utility|fayda; elektrik, su, gaz hizmeti|A useful service such as water or electricity, or the practical value of something.|The rent doesn't include utility bills.|We discovered the utility of keeping a spare key outside.
heritage|miras, kültürel geçmiş|Traditions, buildings, and history passed from earlier generations.|The town is proud of its musical heritage.|She wants her children to understand their cultural heritage.
hospitable|misafirperver, konuksever|Friendly and welcoming toward guests or strangers.|Everyone in the village was remarkably hospitable.|Our hosts were hospitable despite our late arrival.
imperative|çok önemli, zorunlu|Extremely important or necessary in a particular situation.|It's imperative that we leave early to catch the flight.|Clear directions are imperative when someone is driving in a new city.
inexperienced|deneyimsiz, tecrübesiz|Having little practical knowledge because of limited experience.|He's an inexperienced driver, so give him extra space.|I felt inexperienced the first time I traveled alone.
influential|etkili, nüfuzlu|Having the power to shape how other people think or act.|Her aunt was an influential teacher in the neighborhood.|That documentary had an influential role in changing my opinion.
mature|olgun; olgunlaşmak|Able to behave responsibly, or fully developed.|She handled the disagreement in a mature way.|The trees take many years to mature.
merge|birleştirmek, birleşmek|To join two or more things into one.|The two lines of traffic merge after the bridge.|We decided to merge our travel plans into one trip.
narrowly|kıl payı, çok az farkla|By only a small amount or with little room to spare.|We narrowly missed the last train home.|She narrowly won the race by half a second.
shift|vardiya; değişim|A period of work or a noticeable change in position or opinion.|My sister works the night shift at the hospital.|There has been a shift in how people shop for groceries.
straighten|düzeltmek, doğrultmak|To make something straight, tidy, or correctly positioned.|Could you straighten the picture on the wall?|She tried to straighten her hair before the party.
strive|çabalamak, gayret etmek|To work hard toward a goal that matters to you.|We strive to make every guest feel welcome.|She continues to strive for better pronunciation.
supervise|denetlemek, gözetmek|To watch over work or an activity and ensure it is done correctly.|An adult must supervise children near the pool.|The manager supervised the repairs in the lobby.
suspend|askıya almak; geçici durdurmak|To temporarily stop an activity or service.|The school decided to suspend classes during the storm.|The account was suspended after several failed sign-in attempts.
thrilling|heyecan verici, sürükleyici|Extremely exciting in a way that holds your attention.|The boat ride through the canyon was thrilling.|We watched a thrilling match that ended in overtime.
unforeseen|öngörülmeyen, beklenmedik|Not expected or predicted before something happens.|An unforeseen delay made us miss our connection.|Keep some savings for unforeseen expenses.
unofficial|gayriresmî, resmî olmayan|Not formally recognized or approved by an authority.|We heard the unofficial results from a neighbor.|The meeting was an unofficial chat over coffee.
urban|kentsel, şehirle ilgili|Related to a city rather than the countryside.|They enjoy urban life but miss having a garden.|The new bike lanes are part of an urban improvement plan.
improbable|pek olası olmayan|Unlikely to happen or to be true.|It seems improbable that the package arrived in one hour.|The story has an improbable ending, but it's entertaining.
impulsive|fevri, düşünmeden hareket eden|Acting suddenly without considering consequences.|I made an impulsive decision to book the trip.|She's trying to be less impulsive when shopping online.
inaccurate|hatalı, gerçeği yansıtmayan|Not correct or not reflecting the facts.|The weather forecast was inaccurate yesterday.|That map is inaccurate; the street name has changed.
inflation|enflasyon, fiyatların genel artışı|A general rise in prices that reduces what money can buy.|High inflation has made groceries more expensive.|Our salary increases haven't kept up with inflation.
interruption|kesinti, araya girme|Something that temporarily stops an activity or conversation.|Sorry for the interruption; please continue your story.|A power interruption shut down the elevator.
invariable|değişmez, her zaman aynı|Remaining the same in every relevant situation.|The twins' invariable bedtime routine helps them relax.|Her invariable answer to that question is a smile.
investment|yatırım|Money, time, or effort used now to gain a future benefit.|Learning another language is an investment in yourself.|They made a small investment in home insulation.
irrational|mantıksız, akıl dışı|Not based on reasonable evidence or clear thinking.|I know my fear of elevators is irrational.|It would be irrational to drive during that severe storm.
shrink|küçülmek, daralmak|To become smaller in size, amount, or importance.|My cotton sweater shrank in the wash.|The puddles began to shrink as the sun came out.
specifically|özellikle, açıkça|In a precise way that identifies one thing rather than others.|I asked specifically for a room away from the street.|She specifically asked us to arrive before the doors opened.
squeeze|sıkmak, sıkıştırmak|To press something firmly or fit into a very small space.|Squeeze a little lemon over the fish.|We managed to squeeze three suitcases into the trunk.
statistics|istatistikler, sayısal bilgiler|Numbers gathered and analyzed to explain a situation.|The road safety statistics surprised me.|She checked the statistics before choosing a school.
sympathize|halinden anlamak, empati göstermek|To understand someone's difficulties and feel sorry about them.|I sympathize with anyone who has missed a flight.|He sympathized with her after hearing about the argument.
tackle|ele almak, üstesinden gelmeye çalışmak|To make a serious effort to deal with a problem or task.|Let's tackle the hardest chore first.|She decided to tackle the clutter in her closet this weekend.
terrifying|korkutucu, dehşet verici|Causing extreme fear or alarm.|The sudden thunder was terrifying for the children.|He found the idea of speaking in public terrifying.
urgently|acilen, gecikmeden|In a way that requires immediate action or attention.|The pipe is leaking and needs to be fixed urgently.|She urgently called her parents when the flight was canceled.
immigrant|göçmen|A person who moves to another country to live there.|My neighbor is an immigrant who opened a small bakery.|The museum shares stories of immigrant families in the city.
innate|doğuştan gelen, doğal|Present from birth rather than learned through experience.|She has an innate sense of rhythm.|His innate curiosity makes him ask great questions.
instruct|talimat vermek, öğretmek|To tell someone clearly how to do something or behave.|The guide instructed us to stay on the marked path.|Please instruct the delivery driver to ring the bell twice.
leap|sıçramak; büyük adım|To jump suddenly or make a large change.|The cat leaped onto the kitchen counter.|Moving abroad was a huge leap for their family.
lifetime|ömür, yaşam süresi|The entire period that someone is alive or something exists.|It was the trip of a lifetime for my parents.|This memory will stay with me for a lifetime.
loneliness|yalnızlık|The sadness of feeling that you have little companionship.|Moving to a new city can bring feelings of loneliness.|A weekly phone call helped ease his loneliness.
merchandise|ticari mallar, satılık ürünler|Goods offered for sale, especially in a store.|The shop displays its new merchandise near the entrance.|She returned some damaged merchandise to the seller.
nightmare|kâbus; çok kötü deneyim|A frightening dream or an extremely unpleasant situation.|I had a nightmare about missing my flight.|Finding parking downtown was a complete nightmare.
splash|sıçratmak; su sıçraması|To make liquid move and scatter in drops.|The kids splashed water all over the bathroom floor.|A passing car splashed muddy water onto my jacket.
spur|teşvik etmek, harekete geçirmek|To encourage something to happen or to make someone act.|Her friend's encouragement spurred her to apply for the course.|The good weather spurred us to go for a walk.
stagger|sendelemek; aşamalara ayırmak|To walk unsteadily, or arrange things at different times.|He staggered slightly after standing up too quickly.|The family staggered their arrival times to avoid traffic.
steer|yönlendirmek; direksiyonla sürmek|To control the direction of a vehicle or guide a situation.|She steered the car carefully through the narrow street.|I tried to steer the conversation away from politics.
stingy|cimri, pinti|Unwilling to spend or share money even when reasonable.|He's too stingy to split the taxi fare fairly.|Don't be stingy with the sauce; everyone wants more.
sue|dava açmak|To take legal action against someone in court.|The tenant threatened to sue over the unsafe stairs.|She sued the airline after losing valuable luggage.
thoughtless|düşüncesiz, başkalarını hesaba katmayan|Not considering how your words or actions affect other people.|It was thoughtless to play loud music at midnight.|He apologized for his thoughtless remark.
'''.strip()

# Stronger C1 shortlist; these are existing chosen targets, not new invented levels.
C1_ROWS = '''
elastic|esnek, elastik|Able to stretch and return to its original shape.|These pants have an elastic waistband.|The elastic band snapped when I pulled it too far.
charter|kiralamak; resmî kuruluş belgesi|To hire a vehicle for a group, or an official document setting out rights.|We chartered a small boat for the family reunion.|The organization's charter explains how its board is elected.
rustle|hışırdamak, hışırdatmak|To make a soft, dry sound as something moves or brushes against another thing.|I heard the leaves rustle outside my window.|She rustled through the papers looking for the receipt.
recess|ara, teneffüs; girinti|A short break from work or school, or a space set back into a wall.|The children rushed outside for recess.|The light was installed in a recess above the doorway.
uniformity|tekdüzelik, aynı biçimde olma|The condition of being the same in appearance, behavior, or quality.|The houses all have a surprising uniformity of design.|The teacher wanted more uniformity in how homework was submitted.
staple|temel ürün; zımba teli|A food or product used regularly and considered essential.|Rice is a staple food in many households.|Oatmeal has become a staple of my breakfast routine.
suburban|banliyöye ait|Located in or characteristic of a residential area outside a city center.|They moved to a suburban neighborhood for more space.|Suburban buses don't run as often late at night.
somber|kasvetli, ciddi, hüzünlü|Serious, sad, or dark in mood or appearance.|The room felt somber after the bad news.|He spoke in a somber voice about the accident.
transit|toplu taşıma; geçiş|The movement of people or goods between places, especially by transport.|Public transit is cheaper than driving downtown.|The package was damaged while in transit.
suspension|askıya alma, geçici durdurma|A temporary interruption of an activity, privilege, or service.|The suspension of train service caused long delays.|His account suspension lasted three days.
exhilarating|heyecan verici, coşku uyandıran|Making someone feel extremely excited and full of energy.|The ride down the mountain was exhilarating.|She found her first solo flight exhilarating.
fiddle|kurcalamak, sürekli uğraşmak|To make small adjustments to something, often without much purpose.|Stop fiddling with the thermostat; the room is warm enough.|He fiddled with the radio until he found a clear station.
temperamental|huysuz, değişken davranan|Likely to change moods or behavior suddenly and unpredictably.|Our old printer is temperamental on humid days.|The chef was talented but notoriously temperamental.
ventilate|havalandırmak|To allow fresh air to move through an enclosed space.|Open the windows to ventilate the kitchen after cooking.|We ventilated the room before painting the walls.
rotate|döndürmek; sırayla değiştirmek|To turn around a central point, or take turns using positions or duties.|Remember to rotate the tires regularly.|We rotate who cooks dinner each evening.
terrain|arazi, yeryüzü şekilleri|Land considered in terms of its surface and how easy it is to cross.|The hiking trail crosses rocky terrain.|The car struggled on the muddy terrain outside the village.
squander|çarçur etmek, boşa harcamak|To waste something valuable through careless or foolish decisions.|Don't squander your vacation days on errands.|He squandered his savings on things he didn't need.
sprout|filizlenmek, filiz|To begin growing new shoots or leaves.|The seeds started to sprout after a week.|Tiny green plants sprouted between the stones.
farce|maskaralık, tam bir saçmalık|A situation so badly organized or ridiculous that it seems like a joke.|The meeting turned into a farce when nobody had the right documents.|Their attempt to fix the elevator was a complete farce.
remorseless|acımasız, pişmanlık göstermeyen|Showing no regret for causing harm or distress.|The story depicts a remorseless criminal.|He seemed remorseless after deliberately breaking the rules.
fixture|sabit donanım, demirbaş|An item that is attached to a building and normally stays there.|The bathroom fixtures need replacing.|The kitchen light fixture hangs too low over the table.
realism|gerçekçilik, gerçeğe yakınlık|The quality of showing things as they really are rather than idealizing them.|I liked the realism of the characters in that movie.|The painting's realism made the scene feel alive.
screenwriter|senarist|A person who writes scripts for films or television.|The screenwriter based the story on her childhood.|We met a screenwriter at the film festival.
synopsis|özet, kısa konu anlatımı|A brief description of the main events in a story or film.|Read the synopsis before choosing a movie.|The publisher asked her for a one-page synopsis of the novel.
ventilation|havalandırma, hava dolaşımı|The movement of fresh air into and stale air out of a room.|Good ventilation is important when painting indoors.|The apartment needs better ventilation in the bathroom.
radiator|radyatör, kalorifer peteği|A device that heats a room or cools an engine by transferring heat.|The radiator is making a strange knocking sound.|We placed the sofa away from the radiator.
firewall|güvenlik duvarı|Software or equipment that blocks unauthorized network traffic.|A firewall can block unwanted network connections.|The office firewall prevented access to that website.
socialization|sosyalleşme, toplumla ilişki kurma|The process of learning to interact with other people and society.|Group activities can help with children's socialization.|Working from home reduced her opportunities for socialization.
retrace|izini sürmek, aynı yolu geri gitmek|To follow a route again, often to find something lost.|We retraced our steps to find the missing keys.|He retraced the trail after realizing he'd taken a wrong turn.
riveting|sürükleyici, büyüleyici|So interesting or exciting that you cannot stop paying attention.|The documentary was riveting from beginning to end.|She told a riveting story about her journey overseas.
unsettling|tedirgin edici, huzursuzluk veren|Making you feel anxious or uncomfortable without always knowing why.|The strange noise downstairs was unsettling.|I found the movie's final scene deeply unsettling.
unsettle|tedirgin etmek, huzurunu kaçırmak|To make someone feel nervous, uncertain, or uncomfortable.|The sudden change of plans unsettled the children.|The news unsettled me more than I expected.
quirky|alışılmadık, kendine özgü, sevimli tuhaf|Unusual in an interesting, often charming way.|It's a quirky little cafe filled with old board games.|She has a quirky sense of humor that I love.
synthetic|sentetik, yapay|Made from artificial materials rather than produced naturally.|The jacket is made from synthetic fabric.|Synthetic flowers can look surprisingly realistic.
appallingly|korkunç derecede, son derece kötü|In an extremely bad, shocking, or unacceptable way.|The hotel room was appallingly dirty.|The bus was appallingly late after the storm.
plaque|diş plağı; plaket, levha|A thin film on teeth or a flat sign carrying words or a name.|The dentist explained how to remove plaque from my teeth.|A small plaque outside the theater honors its founder.
neutralization|etkisiz hâle getirme, nötrleştirme|The process of canceling or reducing the effect of something.|The filter helps with the neutralization of unpleasant odors.|The science lesson covered neutralization of acids with bases.
remorsefully|pişmanlıkla, vicdan azabıyla|In a way that shows regret for something wrong you have done.|He looked at the broken vase remorsefully.|She spoke remorsefully about how she had treated her friend.
unassisted|yardım almadan, tek başına|Without help or support from another person.|He walked up the stairs unassisted after physical therapy.|The child managed to tie her shoes unassisted.
cavity|boşluk, oyuk; diş çürüğü|An empty space inside something, especially a hole in a tooth.|The dentist found a small cavity in my molar.|The bird made a nest in a cavity in the tree.
chisel|keskiyle oymak; keski|To cut or shape a hard material using a sharp-edged tool.|The artist used a chisel to shape the wooden frame.|He carefully chiseled the old tile away from the wall.
tract|geniş arazi, belirli alan|A large area of land, often with a common feature.|A huge tract of forest surrounds the village.|They bought a small tract of land near the lake.
stimuli|uyaranlar|Things or events that cause a physical or mental response.|Too many visual stimuli can make it hard to focus.|The study examined how people respond to different stimuli.
carpenter|marangoz|A skilled worker who makes or repairs wooden things.|We hired a carpenter to repair the stairs.|The carpenter built shelves that fit the narrow hallway.
undaunted|yılmayan, cesareti kırılmamış|Not discouraged by difficulty, danger, or failure.|Undaunted by the rain, they continued their hike.|She remained undaunted after her first job interview went badly.
recessive|çekinik, baskın olmayan|Describing a genetic characteristic expressed only under certain inherited conditions.|The doctor explained how a recessive trait can be inherited.|Two parents may carry the same recessive gene without showing the trait.
'''.strip()


def make_rows():
    focus=json.loads((ROOT/'data/fluency-focus.json').read_text(encoding='utf8'))
    levels={x['word']:x['level'] for x in focus['vocabulary'] if x['status'] in ('gloss_draft','context_draft')}
    # Historical authored batches remain valid after low-utility cards retire.
    archive=ROOT/'data/archived-vocabulary.json'
    if archive.exists():
        levels.update({x['word']:x['level'] for x in json.loads(archive.read_text()) if x.get('archivedFromFocus')})
    rows=[]; seen=set()
    for level,block in (('B2',ROWS),('C1',C1_ROWS)):
        for i,raw in enumerate(block.splitlines(),1):
            pieces=[x.strip() for x in raw.split('|')]
            if len(pieces)!=5:raise ValueError(f'{level} row {i} has {len(pieces)} fields')
            word,tr,definition,a,b=pieces
            if word in seen:raise ValueError(f'duplicate: {word}')
            seen.add(word)
            if levels.get(word)!=level:raise ValueError(f'not current {level} quick focus: {word}, status {levels.get(word)}')
            rows.append({'word':word,'level':level,'tr':tr,'definition':definition,'example':a,'examples':[a,b],
                'levelStatus':'source_candidate_unreviewed','meaningReviewed':False,'exampleReviewed':False,
                'prompt':f'Use “{word}” in a sentence about your own life.'})
    return rows

def apply():
    rows=make_rows()
    target=ROOT/'sources/authored-20261028-daily-context-sprint.jsonl'
    target.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf8')
    previous={x['word'] for x in json.loads((ROOT/'data/vocabulary.json').read_text()) if x.get('category')=='general'}
    new=[x for x in rows if x['word'] not in previous]
    if new:
        temp=ROOT/'sources/.daily-context-pending.jsonl'
        temp.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in new),encoding='utf8')
        try:r=process(temp,'general',apply=True)
        finally:temp.unlink(missing_ok=True)
    else:r={'validatedNewCards':0,'mode':'already_applied'}
    print(json.dumps({'authored':len(rows),'new':len(new),'process':r},ensure_ascii=False))

if __name__=='__main__':apply()
