#!/usr/bin/env python3
"""Original authored batch; idempotent, sourced headwords, not editor-approved."""
import json
from pathlib import Path
from promote_content_batch import process
ROOT=Path(__file__).resolve().parents[1]
# Each meaning/definition and both examples composed independently, not source dictionary text.
GENERAL='''
compel|zorlamak, mecbur bırakmak|To make someone do something, often because circumstances leave little choice.|A sudden storm compelled the hikers to turn back.|The evidence may compel officials to reopen the investigation.
compromised|tehlikeye düşmüş, ödün verilmiş|Weakened or exposed to harm because a safeguard has failed.|The leaked password left the customer's account compromised.|Engineers replaced the compromised support beam immediately.
consultation|danışma, görüş alışverişi|A meeting or discussion held to obtain advice before making a decision.|The city held a public consultation about the new transit plan.|After consultation with her doctor, she changed her schedule.
consultancy|danışmanlık şirketi veya hizmeti|A business or professional service that provides specialist advice.|She joined a consultancy that advises small manufacturers.|The nonprofit hired a consultancy to review its operations.
contractor|yüklenici, sözleşmeli çalışan|A person or company hired under a contract to complete particular work.|The contractor promised to repair the roof before winter.|Independent contractors must track their own invoices carefully.
convict|suçlu bulmak, hüküm giymiş kişi|To find someone guilty in court, or a person serving a criminal sentence.|The jury could not convict the suspect without stronger evidence.|The former convict later volunteered at a community center.
conviction|mahkûmiyet; güçlü inanç|A formal finding of guilt, or a firmly held belief.|The appeal court overturned the conviction after new evidence emerged.|She spoke with conviction about the value of public libraries.
coverage|kapsam; haber kapsamı|The extent of protection, service, or attention provided to something.|The insurance policy includes coverage for water damage.|Local coverage of the election focused on housing costs.
crave|çok istemek, canı çekmek|To feel a strong desire for something, especially food or attention.|After the long hike, everyone craved a hot meal.|She sometimes craves a quiet evening without notifications.
craving|şiddetli istek, aşerme|A powerful wish to have or experience something particular.|He resisted the craving for another cup of coffee.|Her craving for adventure led her to travel across the country.
credential|yetkinlik belgesi, kimlik bilgisi|A qualification or document proving someone's identity or ability.|The hospital verified the nurse's credentials before hiring her.|You need a valid credential to enter the restricted area.
credibly|inandırıcı biçimde|In a way that is believable because it is supported by evidence.|The witness explained the timeline credibly and without exaggeration.|She could not credibly claim that the message was accidental.
crumble|ufalanmak, parçalanmak, yıkılmak|To break into small pieces or gradually lose strength or structure.|The old brick wall began to crumble after years of neglect.|Their agreement crumbled when neither side would compromise.
customary|alışılagelmiş, geleneksel|Regularly done or expected because it is normal in a particular setting.|It is customary to thank the host before leaving the dinner.|The judge asked the witness the customary opening questions.
cynic|kuşkucu, insanların niyetlerinden şüphe eden|A person who tends to doubt that others act for good reasons.|Even the biggest cynic appreciated the neighbors' generosity.|He described himself as a cynic, but still donated to the cause.
daunt|gözünü korkutmak, yıldırmak|To make someone feel discouraged or intimidated by a difficult task.|The steep climb did not daunt the experienced hikers.|The amount of paperwork might daunt a first-time applicant.
daunting|göz korkutucu, yıldırıcı|Seeming difficult or intimidating before someone attempts it.|Moving to a new city can be daunting at first.|The students faced a daunting amount of material before the exam.
daydream|hayal kurmak, gündüz düşü|To imagine pleasant events while not paying attention to the present.|She began to daydream about a cabin near the lake.|During the dull lecture, his daydream turned into a travel plan.
debut|ilk kez ortaya çıkma, çıkış|A person's or product's first public appearance or performance.|The young actor made her debut in a local theater production.|The company announced the debut of its new electric bicycle.
deceit|aldatma, hile|Behavior intended to make another person believe something false.|The investigation uncovered years of deceit in the accounting records.|He apologized for the deceit that had damaged their friendship.
degradation|bozulma, kötüleşme|A process in which something becomes worse in quality or condition.|Researchers measured soil degradation near the abandoned mine.|Repeated delays caused a gradual degradation of customer trust.
degrade|kalitesini düşürmek; aşağılamak|To make something worse in quality or treat someone without respect.|Harsh chemicals can degrade the plastic over time.|No employee should be allowed to degrade a colleague in public.
demise|sona erme, ölüm|The end of something that previously existed, or a person's death.|The demise of the factory changed the entire neighborhood.|Rumors about the demise of the newspaper proved premature.
demographic|demografik, nüfus grubuna ait|Relating to the age, income, or other characteristics of a population.|The survey revealed a significant demographic shift in the city.|Different demographic groups responded differently to the policy.
demography|nüfus bilimi|The statistical study of populations and how they change over time.|She studied demography to understand changing birth rates.|Urban demography helps planners predict housing demand.
demolition|yıkım|The deliberate destruction of a building or another structure.|Demolition of the unsafe warehouse began on Monday.|Residents asked whether the demolition would affect nearby homes.
depict|tasvir etmek, betimlemek|To show or describe a person, scene, or event in words or images.|The mural depicts workers building the first railroad.|The documentary depicts daily life in a remote mountain town.
depiction|tasvir, betimleme|A written or visual representation of someone or something.|Critics praised the film's realistic depiction of family life.|The museum questioned the painting's depiction of the battle.
deprivation|yoksunluk|A condition in which someone lacks something important for well-being.|Sleep deprivation can make it harder to concentrate.|Childhood deprivation may affect educational opportunities later on.
detriment|zarar, aleyhine durum|Harm or a disadvantage caused to someone or something.|The company expanded too quickly, to the detriment of service quality.|He worked late every night to the detriment of his health.
detrimental|zararlı, olumsuz etkili|Causing harm or making a situation worse.|A lack of clean water is detrimental to public health.|The new rule could have a detrimental effect on small businesses.
discard|atmak, gözden çıkarmak|To get rid of something because it is unwanted or no longer useful.|Please discard the damaged packaging before using the product.|The researchers did not discard data simply because it was unexpected.
discourse|söylem, tartışma|Serious discussion or communication about a subject or issue.|Public discourse about climate policy has become more urgent.|The professor encouraged thoughtful discourse rather than personal attacks.
disillusionment|hayal kırıklığı, inanç kaybı|The loss of trust or enthusiasm after discovering that reality is disappointing.|Widespread disillusionment followed the broken campaign promises.|Her disillusionment with the industry led her to change careers.
dislodge|yerinden çıkarmak, sökmek|To force something out of the position where it was fixed or stuck.|The rescue team worked to dislodge a rock blocking the tunnel.|A sharp tap should dislodge the loose piece of wood.
dismal|kasvetli, çok kötü|Very poor in quality or likely to cause sadness or disappointment.|The team had a dismal record during the first half of the season.|Rain and empty streets made the afternoon feel dismal.
dismay|dehşete düşürmek; üzüntü ve kaygı|A feeling of alarm or disappointment, or to cause that reaction.|To her dismay, the train left ten minutes early.|The abrupt cancellation dismayed families who had already traveled.
diverge|farklı yönlere ayrılmak|To separate and move in different directions or become less similar.|The two hiking trails diverge just beyond the bridge.|Their opinions began to diverge after the first meeting.
divergence|ayrışma, farklılaşma|A growing difference between ideas, patterns, or paths.|The report describes a divergence in household incomes.|A divergence between the two forecasts prompted further analysis.
diversity|çeşitlilik|The presence of many different kinds of people, ideas, or living things.|The company wants greater diversity among its leadership teams.|The park protects an impressive diversity of native plants.
docile|uysal, kolay yönetilen|Calm and willing to follow instructions rather than resist.|The normally docile dog barked at the sudden noise.|Farmers selected docile animals for the children's demonstration.
drawback|dezavantaj, sakınca|A feature of a plan or product that makes it less useful or appealing.|The main drawback of the apartment is the lack of sunlight.|One drawback of remote classes is reduced face-to-face discussion.
duration|süre|The amount of time that an activity or event continues.|The duration of the flight was shorter than expected.|Participants were told the duration of each interview in advance.
durable|dayanıklı, uzun ömürlü|Able to remain in good condition after repeated use or stress.|The company chose durable fabric for its outdoor furniture.|A durable agreement requires cooperation from both sides.
eccentric|alışılmadık, tuhaf|Behaving in an unusual way that differs from social expectations.|The eccentric inventor kept clocks in every room of his house.|Her eccentric style made her instantly recognizable at events.
eclectic|farklı tarzlardan seçilmiş, eklektik|Made up of ideas or styles chosen from a wide variety of sources.|The restaurant offers an eclectic menu from several regions.|His eclectic music collection ranges from jazz to electronic pop.
ego|benlik, ego|A person's sense of self or importance, sometimes excessive.|His ego made it difficult for him to accept constructive criticism.|She put her ego aside and apologized to the team.
effortless|zahmetsiz görünen|Seeming to require very little effort, even when skill is involved.|The dancer made the difficult routine look effortless.|Her effortless command of the material impressed the class.
elevate|yükseltmek; düzeyini artırmak|To raise something to a higher place, level, or degree of importance.|A narrow platform elevates the stage above the audience.|The new training program could elevate the quality of service.
elevation|yükseklik, yükselme|The height of a place above sea level or an act of raising something.|The trail reaches an elevation of eight thousand feet.|At higher elevations, the air contains less oxygen.
elude|kaçıp kurtulmak; akla gelmemek|To escape someone trying to catch or understand something.|The missing document continued to elude the investigators.|A clear explanation eluded him despite hours of thought.
elusive|ele geçirilmesi veya anlaşılması zor|Difficult to find, achieve, or explain despite repeated efforts.|The rare bird remained elusive throughout the expedition.|An elusive solution kept the research team working late.
embark|başlamak, yola çıkmak|To begin a major undertaking or board a ship for a journey.|She decided to embark on a new career in education.|Passengers were asked to embark before the weather changed.
endorsement|destek açıklaması, onay|A public statement of support or formal approval for someone or something.|The proposal received an endorsement from the local teachers' union.|A celebrity endorsement does not guarantee product quality.
engross|tüm dikkatini çekmek|To hold someone's attention so completely that they notice little else.|The mystery novel engrossed her for the entire afternoon.|A complex puzzle can engross the children for hours.
engrossing|sürükleyici, çok ilgi çekici|So interesting that it holds a person's full attention.|The documentary offered an engrossing account of the rescue.|We had an engrossing conversation about the future of cities.
enormously|son derece, çok büyük ölçüde|To a very large extent or to an unusually high degree.|The updated instructions improved the process enormously.|She was enormously grateful for the neighbors' help.
envisage|tasavvur etmek, gözünde canlandırmak|To imagine a possible future or think of something as likely to happen.|We envisage a neighborhood with fewer cars and more trees.|She could not envisage returning to the old system.
ethically|etik biçimde|In a way that follows accepted principles about right and wrong.|The researchers agreed to handle personal data ethically.|Buying ethically sourced supplies can cost more initially.
evoke|çağrıştırmak, akla getirmek|To bring a feeling, memory, or image into someone's mind.|The smell of bread evoked memories of her grandmother's kitchen.|The photograph evoked a sense of hope among the volunteers.
exert|güç veya etki uygulamak|To apply effort, force, or influence to achieve a result.|The athlete had to exert more effort during the final mile.|Large investors can exert significant influence on company decisions.
expire|süresi dolmak, geçerliliğini yitirmek|To stop being valid or usable after a particular date or time.|Your parking permit will expire at the end of the month.|The offer expires before the holiday weekend.
expedite|hızlandırmak|To make a process move forward more quickly than usual.|The agency hired temporary staff to expedite the applications.|Providing complete documents should expedite the approval process.
explanatory|açıklayıcı|Intended to clarify a subject or make information easier to understand.|The report includes an explanatory diagram of the water system.|She added explanatory notes for readers unfamiliar with the topic.
exploitation|sömürü; haksız yararlanma|Using people or resources unfairly to obtain a personal advantage.|The workers protested against exploitation by their employers.|The documentary examines the exploitation of coastal fisheries.
fatigue|yorgunluk, bitkinlik|A state of extreme tiredness caused by effort, illness, or stress.|Long shifts left the nurses struggling with fatigue.|The driver pulled over when fatigue began to affect his concentration.
faction|hizip, grup|A smaller organized group within a larger group, often with different opinions.|A faction of the committee opposed the proposed changes.|The party struggled to reach agreement between competing factions.
forensic|adli incelemeye ilişkin|Related to scientific methods used to investigate crime or legal evidence.|Forensic investigators examined fibers found at the scene.|The court requested a forensic analysis of the damaged documents.
forfeit|kaybetmek, hakkından olmak|To lose a right or possession as a penalty for breaking a rule.|Teams that arrive too late may forfeit the match.|Passengers could forfeit their reservation by missing the deadline.
fragmentation|parçalanma, bölünme|The process of breaking into many separate pieces or groups.|Habitat fragmentation threatens animals that need large territories.|The fragmentation of the market made regulation more difficult.
fusion|birleşim, kaynaşma|The process of joining separate elements into a new whole.|The chef's menu offers a fusion of regional cooking traditions.|Researchers study nuclear fusion as a potential energy source.
'''.strip()
PHRASAL='''
get away|uzaklaşmak, kaçmak|To leave a place or situation, especially in order to escape pressure or danger.|We decided to get away for the weekend and visit the mountains.|The thief tried to get away before the police arrived.|intransitive
get down|moralini bozmak; aşağı inmek|To make someone feel unhappy or discouraged, or to move to a lower position.|Constant complaints can really get the whole team down.|The child got down from the chair without help.|separable
get in|içeri girmek; varmak|To enter a place or vehicle, or to arrive at a destination.|We couldn't get in because the door was locked.|What time does your flight get in tonight?|intransitive
get into|ilgilenmeye başlamak; girmek|To begin enjoying an activity, or to enter a place or situation.|She got into photography after buying a used camera.|The students got into the theater before the show began.|inseparable
get off|inmek; işten çıkmak|To leave a bus, train, or plane, or finish a period of work.|We need to get off at the next subway stop.|I usually get off work around six in the evening.|intransitive
get on|binmek; devam etmek|To board a bus or train, or make progress with a task.|The passengers got on the bus in an orderly line.|How are you getting on with the apartment renovation?|intransitive
get out|dışarı çıkmak|To leave a room, building, or other enclosed space.|Everyone got out of the building safely during the drill.|The dog slipped through the gate and got out.|intransitive
get over with|bitirip aradan çıkarmak|To finish an unpleasant task so that it no longer needs attention.|I want to get the dental appointment over with.|They got the difficult conversation over with before lunch.|separable
get up|kalkmak, ayağa kalkmak|To rise from bed or move from sitting to standing.|I usually get up early when I have a morning meeting.|The audience got up to applaud the musicians.|intransitive
take away|götürmek; ortadan kaldırmak|To remove something from a place or deprive someone of it.|The server took away the empty plates after dinner.|The new policy could take away an important benefit.|separable
take down|indirmek; not almak|To remove something from a higher position or record information in writing.|They took down the old sign before painting the wall.|Please take down the phone number before you forget it.|separable
take in|anlamak; içine almak|To understand information or admit someone into a place or household.|It took a moment to take in the surprising news.|The shelter agreed to take in another abandoned puppy.|separable
take out|dışarı çıkarmak; çıkarmak|To remove something from a place, or invite someone on a social date.|She took out the recycling before leaving the house.|He decided to take his friend out for dinner.|separable
take over|kontrolü devralmak|To assume control or responsibility from another person or organization.|A new director will take over the department next month.|She took over the project after her colleague left.|separable
go after|peşine düşmek; hedeflemek|To pursue someone or actively try to obtain an opportunity.|He decided to go after the scholarship despite the competition.|The police went after the suspect who fled the scene.|inseparable
go away|uzaklaşmak; seyahate çıkmak|To leave a place or travel elsewhere for a period of time.|The family plans to go away during the school break.|The noise finally went away when the truck departed.|intransitive
go down|azalmak; aşağı inmek|To decrease in amount or move from a higher to a lower position.|Energy prices went down after the winter ended.|We watched the sun go down behind the hills.|intransitive
go for|seçmek; denemek|To choose something or make an effort to achieve it.|I think I'll go for the vegetarian option tonight.|She decided to go for the open management position.|inseparable
go into|ayrıntılı incelemek|To examine a subject carefully or explain it in more detail.|The report goes into the causes of the traffic delays.|We don't have enough time to go into every detail.|inseparable
go off|çalmak; bozulmak; patlamak|To begin making a noise unexpectedly, or to explode or stop working normally.|The smoke alarm went off while we were cooking dinner.|My alarm went off earlier than I had planned.|intransitive
go through|yaşamak; ayrıntılı incelemek|To experience a difficult situation or examine something carefully.|She went through a difficult recovery after the accident.|Let's go through the contract before we sign it.|inseparable
go up|artmak; yükselmek|To increase in level, quantity, or price, or move upward.|Rent prices have gone up sharply in the neighborhood.|The hikers watched the balloons go up into the sky.|intransitive
go against|karşı çıkmak; aykırı olmak|To oppose a person or rule, or be inconsistent with something.|The proposal goes against the committee's original agreement.|She refused to go against her professional judgment.|inseparable
come down|aşağı inmek; düşmek|To move from a higher to a lower position or become less expensive.|The temperature came down after the storm passed.|House prices have come down in several nearby towns.|intransitive
come in|içeri girmek; gelmek|To enter a room or arrive somewhere.|Please come in and make yourself comfortable.|New applications continued to come in throughout the week.|intransitive
come off|gerçekleşmek; çıkmak|To happen successfully, or become detached from a surface.|The outdoor event came off despite the rain.|One of the buttons came off his jacket.|intransitive
come out|ortaya çıkmak; yayımlanmak|To become known or available, or to leave an enclosed place.|The full report will come out next Tuesday.|The truth eventually came out during the hearing.|intransitive
come over|ziyarete gelmek|To visit someone at the place where they are staying or living.|Would you like to come over for dinner on Friday?|Some neighbors came over to help move the furniture.|intransitive
come up|gündeme gelmek; ortaya çıkmak|To arise unexpectedly or become a subject for discussion.|A scheduling problem came up just before the meeting.|The issue came up again during the final review.|intransitive
put away|yerine kaldırmak|To return something to its proper storage place.|The children put away their toys after the game.|Please put the tools away when you finish repairing the shelf.|separable
put down|yere bırakmak; küçük düşürmek|To place something on a surface or make someone feel less important.|She put down her bag beside the front door.|He shouldn't put down his coworkers during meetings.|separable
put out|söndürmek; rahatsız etmek|To stop a fire from burning or cause someone inconvenience.|Firefighters managed to put out the kitchen fire quickly.|I hope the last-minute change didn't put you out.|separable
put through|telefonda bağlamak; zor bir durum yaşatmak|To connect a telephone call or cause someone to experience something difficult.|The receptionist put me through to the billing department.|The long investigation put the family through months of stress.|separable
put up|kurmak; inşa etmek|To erect or attach something, such as a tent, sign, or building.|We put up the tent before it started raining.|The city put up new signs near the intersection.|separable
look after|bakmak; ilgilenmek|To care for someone or something and keep them safe or well.|Could you look after my cat while I'm away?|The nurse looked after patients throughout the night.|inseparable
look for|aramak|To try to find a person or thing that is missing or needed.|I've been looking for my keys since breakfast.|They are looking for a quieter apartment closer to work.|inseparable
look up|bilgi araştırmak; düzelmek|To search for information in a reference source, or become more positive.|You can look up the unfamiliar word in a dictionary.|Business began to look up after the summer slowdown.|separable
turn away|geri çevirmek; uzaklaştırmak|To refuse entry or service, or direct one's face away.|The museum had to turn away visitors when it reached capacity.|She turned away so the photographer couldn't see her reaction.|separable
turn off|kapatmak|To stop a device, light, or machine from operating.|Remember to turn off the lights before leaving the office.|He turned off his phone while the concert was playing.|separable
turn on|açmak, çalıştırmak|To start a machine, light, or other electronic device.|Could you turn on the heater before the guests arrive?|She turned on the laptop to check the reservation.|separable
turn up|ortaya çıkmak; sesi artırmak|To arrive unexpectedly or become noticeable, or increase a device's volume.|An old friend turned up at the festival without warning.|Please turn up the volume so everyone can hear the interview.|intransitive
break away|ayrılmak, kopmak|To separate from a group or escape from something holding you.|Three cyclists broke away from the main group near the hill.|The region voted to break away from the larger organization.|intransitive
break through|engel aşmak; önemli ilerleme kaydetmek|To overcome a barrier or make an important advance.|The firefighters managed to break through the locked door.|Researchers hope to break through the remaining technical obstacles.|intransitive
hold off|ertelemek; uzak tutmak|To delay an action or prevent something from approaching.|Let's hold off making a decision until the results arrive.|The defenders held off the opposing team in the final minutes.|separable
keep away|uzak tutmak|To prevent someone or something from approaching a place or person.|Please keep the children away from the construction equipment.|The fence keeps stray animals away from the garden.|separable
carry away|kendini kaptırmak; sürüklemek|To become so excited that judgment is temporarily lost, or to move something elsewhere.|Don't get carried away by the excitement of the auction.|The flood carried away several wooden bridges overnight.|separable
work through|adım adım çözmek|To deal with a problem by carefully considering each part.|The counselor helped the family work through their disagreement.|We need to work through the remaining technical issues.|inseparable
cut down|azaltmak; kesmek|To reduce an amount or knock down a tree by cutting it.|The family is trying to cut down on unnecessary spending.|The crew cut down the damaged tree after the storm.|separable
pick out|seçmek; ayırt etmek|To choose someone or something from a group of options.|She picked out a blue jacket for her brother's birthday.|From the back row, I couldn't pick out the speaker's face.|separable
call on|ziyaret etmek; söz vermek|To visit someone or ask a particular person to speak or act.|The teacher called on Maya to answer the question.|The charity called on local businesses to contribute supplies.|inseparable
pull through|iyileşip atlatmak|To survive a serious illness or difficult situation.|Doctors expect her to pull through after the operation.|The family helped the shop pull through a difficult winter.|intransitive
stand for|temsil etmek; anlamına gelmek|To represent an idea, value, or phrase through words or symbols.|The initials stand for the name of the organization.|Our group stands for fairness and equal opportunity.|inseparable
fall for|kanmak; âşık olmak|To believe a trick or become romantically attracted to someone.|Don't fall for messages promising money without any effort.|He fell for her after they worked together on the project.|inseparable
move on|devam etmek, geride bırakmak|To leave a subject or situation behind and focus on what comes next.|After answering the questions, the presenter moved on to the next topic.|It took her several months to move on after the breakup.|intransitive
pass on|iletmek; reddetmek|To give information to someone else or decide not to accept an offer.|Please pass on the updated schedule to the whole team.|I think I'll pass on dessert because I'm already full.|separable
check in|giriş yapmak; kayıt yaptırmak|To register upon arriving at a hotel, airport, or other place.|We need to check in at the airport two hours before departure.|The guests checked in shortly after the room was ready.|intransitive
find out|öğrenmek, keşfetmek|To discover information that was not known previously.|She found out that the museum is closed on Mondays.|We need to find out why the payment was delayed.|separable
'''.strip()

def read_lines(text,n):
    for line in text.splitlines():
        fields=line.split('|')
        if len(fields)!=n:raise ValueError(f'bad authored line: {line[:90]}: {len(fields)}')
        yield [x.strip() for x in fields]

def stage(kind):
    q={x['word']:x for x in json.loads((ROOT/'sources'/('general-production-queue.json' if kind=='general' else 'phrasal-production-queue.json')).read_text())}
    existing={x['word'] for x in json.loads((ROOT/'data'/('vocabulary.json' if kind=='general' else 'phrasals.json')).read_text())}
    rows=[]
    for item in read_lines(GENERAL if kind=='general' else PHRASAL,5 if kind=='general' else 6):
        if kind=='general':word,tr,definition,e1,e2=item
        else:word,tr,definition,e1,e2,syntax=item
        if word in existing:continue
        if word not in q:raise ValueError(f'No sourced word: {word}')
        obj={'word':word,'level':q[word].get('levelCandidate') if kind=='general' else 'B2','tr':tr,'definition':definition,'example':e1,'examples':[e1,e2]}
        if kind=='general':
            if obj['level'] not in ('B2','C1'):raise ValueError(f'bad source level {word}')
            obj['prompt']=f'Use “{word}” in an original American-English sentence.'
        else:
            obj.update({'levelEvidence':'Provisional educational estimate; this headword list does not certify CEFR.','levelStatus':'editorial_estimate_unverified',
                'syntax':syntax,'register':'neutral',
                'note':{'separable':'A noun object may be placed after the particle or between verb and particle; pronouns generally go between.',
                        'intransitive':'This usage needs no direct object; a prepositional complement may follow.',
                        'inseparable':'A noun or pronoun object normally follows the entire expression.'}[syntax],
                'senses':[{'tr':tr,'definition':definition,'example':e1}]})
        rows.append(obj)
    if not rows:
        print(f'NOOP {kind}: already imported')
        return 0
    path=ROOT/'sources'/f'authored-20261027-{kind}.jsonl'
    path.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf8')
    print(process(path,kind,apply=True))
    return len(rows)

if __name__=='__main__':
    total=0
    for kind in ('general','phrasal'):total+=stage(kind)
    print('Imported',total,'new authored, unreviewed lessons')
