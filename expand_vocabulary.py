"""Original B2/C1 general English candidate cards (editorial level tags, not CEFR certification).
Every card has a specific English definition, Turkish gloss, and original American-English example.
No proprietary dictionary records are copied. Idempotent update.
"""
from pathlib import Path
import json,re
p=Path(__file__).resolve().parents[1]/'data'/'vocabulary.json'; data=json.loads(p.read_text())
# word|level|Turkish|English definition|original sentence
raw='''
resilience|C1|dayanıklılık|The ability to recover or adapt after difficulties.|Her resilience helped her rebuild her life after the storm.
nuance|C1|ince anlam farkı|A subtle difference in meaning, attitude, or expression.|The translation missed an important nuance in her argument.
ambiguous|C1|belirsiz, birden fazla anlamlı|Open to more than one reasonable interpretation.|The instructions were ambiguous, so we asked for clarification.
compelling|C1|ikna edici, etkileyici|Strong enough to attract attention or persuade someone.|She presented a compelling case for changing the rules.
contemplate|C1|üzerine derin düşünmek|To think carefully about a possible action or situation.|He contemplated moving abroad for several months.
underlying|C1|temelde yatan|Existing beneath the surface or being the fundamental cause.|The team investigated the underlying cause of the delay.
subtle|C1|ince, fark edilmesi zor|Small or delicate enough to be difficult to notice.|I noticed a subtle shift in her tone of voice.
pervasive|C1|yaygın, her yere işlemiş|Present or influential throughout a situation or place.|Distrust had become pervasive in the organization.
arbitrary|C1|keyfi, rastgele|Based on personal choice rather than a clear principle.|The deadline seemed arbitrary and hard to justify.
inherent|C1|doğasında var olan|Existing as a natural or permanent feature of something.|Every approach has inherent limitations.
plausible|C1|makul, inandırıcı|Seeming reasonable or likely to be true.|The witness offered a plausible explanation for the noise.
coherent|C1|tutarlı, anlaşılır|Logical and organized so that the parts fit together.|Her essay presented a coherent argument from start to finish.
concise|C1|özlü, kısa ve net|Giving information clearly with very few unnecessary words.|Please keep your summary concise but informative.
substantiate|C1|kanıtla desteklemek|To provide evidence that supports a claim.|The journalist tried to substantiate the allegations.
refute|C1|çürütmek|To show that a claim or argument is incorrect.|New evidence may refute the original explanation.
elaborate|C1|ayrıntılandırmak|To explain something in more detail.|Could you elaborate on what happened after the meeting?
cumulative|C1|birikimli|Increasing through the addition of successive amounts or effects.|The cumulative impact of small expenses surprised us.
consecutive|B2|art arda gelen|Following one another without a break.|It rained for five consecutive days.
preliminary|C1|ön hazırlık niteliğinde|Done before a more complete or final stage.|The preliminary results look promising but remain uncertain.
provisional|C1|geçici, kesinleşmemiş|Arranged or accepted temporarily until confirmed.|We made a provisional reservation for Saturday.
feasible|C1|uygulanabilir|Possible to carry out successfully with available resources.|A shorter schedule may be more feasible.
viable|C1|uzun vadede uygulanabilir|Capable of working successfully over time.|The plan is not financially viable without additional support.
robust|C1|sağlam, güçlü|Strong and able to function under difficult conditions.|We need a robust process for reviewing each application.
fragile|B2|kırılgan, hassas|Easily broken, damaged, or affected by change.|Their agreement remained fragile after the dispute.
volatile|C1|istikrarsız, oynak|Likely to change quickly and unpredictably.|Demand was volatile throughout the summer.
lucrative|C1|kazançlı|Producing a large amount of money.|She left a lucrative job to start a small studio.
scarcity|C1|kıtlık|The condition of not having enough of a needed resource.|Water scarcity affects communities in different ways.
allocation|C1|kaynak dağılımı|The act of distributing resources for particular purposes.|The committee discussed the allocation of public funds.
constraint|C1|kısıt|A condition that limits available choices or actions.|Time was the main constraint on our research.
trade-off|C1|ödünleşim|A choice that gains one benefit while giving up another.|There is a trade-off between price and convenience.
contingency|C1|olasılık için yedek plan|A possible event requiring a planned response.|We prepared a contingency plan for heavy rain.
accountability|C1|hesap verebilirlik|The obligation to explain and accept responsibility for actions.|Public accountability is essential to building trust.
transparency|C1|şeffaflık|The quality of being open and honest about decisions or actions.|Greater transparency helped reduce confusion.
credibility|C1|güvenilirlik|The degree to which someone or something can be believed.|The correction improved the publication's credibility.
authenticity|C1|özgünlük, sahicilik|The quality of being real or true to its origins.|Experts questioned the authenticity of the painting.
integrity|C1|dürüstlük, bütünlük|Honesty and strong principles, or the state of being whole.|She handled the disagreement with integrity.
incentive|C1|teşvik|Something that encourages a person to take action.|The program offers an incentive for using public transit.
disincentive|C1|caydırıcı unsur|Something that discourages a particular action.|High fees can be a disincentive to participation.
compliance|C1|kurallara uyum|The act of following rules, laws, or requirements.|The audit examined compliance with the new standards.
discrepancy|C1|tutarsızlık, uyuşmazlık|A difference between things that should agree.|We found a discrepancy between the two invoices.
inconsistency|C1|tutarsızlık|A lack of agreement between actions, facts, or statements.|The report contained an inconsistency in the dates.
substantial|B2|önemli miktarda|Large enough in amount or importance to matter.|The renovation required a substantial investment.
subsequent|C1|sonraki|Happening or coming after something else.|Subsequent interviews revealed more details.
preceding|C1|önce gelen|Existing or happening immediately before something.|The preceding chapter explains the basic terminology.
simultaneous|C1|eş zamanlı|Happening at the same time.|Two simultaneous events made planning difficult.
intermittent|C1|aralıklı, kesintili|Starting and stopping at irregular intervals.|We experienced intermittent internet access all evening.
sporadic|C1|ara sıra görülen|Occurring occasionally and without a regular pattern.|There were sporadic complaints about the service.
inevitable|B2|kaçınılmaz|Certain to happen or impossible to avoid.|Some delays are inevitable during major construction.
unprecedented|C1|benzeri görülmemiş|Never known or experienced in the same way before.|The city faced unprecedented demand for temporary housing.
conventional|B2|geleneksel, alışılmış|Following methods or ideas that are generally accepted.|They chose an unconventional route instead of the conventional one.
innovative|B2|yenilikçi|Introducing useful new methods or ideas.|The students proposed an innovative solution.
obsolete|C1|kullanım dışı kalmış|No longer useful because something newer has replaced it.|The old equipment became obsolete within a decade.
redundant|C1|gereksiz, yinelenen|No longer needed because something else does the same job.|The editor removed several redundant sentences.
reconcile|C1|uzlaştırmak|To make different ideas or accounts consistent with each other.|She tried to reconcile their conflicting accounts.
mediate|C1|arabuluculuk etmek|To help two sides reach an agreement through discussion.|A volunteer offered to mediate the disagreement.
compromise|B2|uzlaşma|An agreement in which each side gives up something.|They reached a compromise after a long discussion.
consensus|C1|fikir birliği|General agreement among members of a group.|The committee reached a consensus on the next step.
dissent|C1|karşı görüş, itiraz|Strong public disagreement with a decision or view.|A few members expressed dissent during the vote.
adversity|C1|zorluk, sıkıntı|A difficult or unpleasant situation.|She showed patience and humor in the face of adversity.
adversarial|C1|çatışmacı, karşıt|Characterized by opposition or competition between sides.|The debate became unnecessarily adversarial.
empathetic|C1|empati kuran|Able to understand and share another person's feelings.|Her empathetic response made the patient feel heard.
apprehensive|C1|endişeli, tedirgin|Feeling nervous about something that may happen.|He felt apprehensive before his first public speech.
indifferent|C1|ilgisiz, kayıtsız|Having no particular interest or concern.|She was not indifferent to their concerns.
resentment|C1|gücenme, içerleme|A lasting feeling of anger about unfair treatment.|Unspoken resentment eventually damaged the friendship.
reassurance|C1|güvence, iç rahatlatma|Words or actions that reduce someone's worry.|The clear explanation gave everyone some reassurance.
frustration|B2|hayal kırıklığı, öfke|The feeling of being upset by an obstacle or failure.|He expressed frustration with the repeated delays.
curiosity|B2|merak|A strong desire to learn or understand something.|Her curiosity led her to explore unfamiliar subjects.
skepticism|C1|şüphecilik|An attitude of questioning claims rather than accepting them easily.|Healthy skepticism can improve how we assess evidence.
scrutiny|C1|titiz inceleme|Very careful observation or examination.|The new proposal came under intense public scrutiny.
concede|C1|kabul etmek, teslim etmek|To admit a point despite originally arguing against it.|He conceded that the alternative had some advantages.
assert|C1|kesin biçimde ileri sürmek|To state something strongly and confidently.|She asserted that the figures had been checked.
maintainable|C1|sürdürülebilir biçimde korunabilir|Able to be kept in good condition or continued without excessive effort.|A simple routine is more maintainable in the long run.
perception|B2|algı|The way in which someone understands or interprets something.|Our perception of time changes when we are distracted.
misconception|C1|yanlış kanı|An incorrect belief about how something works.|The teacher addressed a common misconception about memory.
inference|C1|çıkarım|A conclusion reached from evidence rather than directly stated facts.|The final question required an inference about the speaker's intention.
implication|C1|dolaylı anlam, sonuç|A possible effect or unstated meaning of something.|The policy has implications for people who work remotely.
assess|B2|değerlendirmek|To evaluate the quality, importance, or likely effects of something.|We need to assess the results before changing the plan.
evaluate|B2|değerlendirmek|To judge how well something meets an objective or standard.|The researchers evaluated several possible explanations.
examine|B2|incelemek|To look at something closely to learn more about it.|The doctor examined the patient carefully.
interpret|B2|yorumlamak|To explain or understand the meaning of something.|Different readers may interpret the ending differently.
distinguish|B2|ayırt etmek|To recognize the difference between similar things.|Can you distinguish the two speakers by their voices?
reinforce|C1|pekiştirmek|To make an idea, behavior, or structure stronger.|Regular feedback can reinforce good study habits.
retain|C1|akılda tutmak, korumak|To continue to have or remember something over time.|Active recall helps learners retain new information.
retrieve|C1|geri çağırmak|To bring back information stored in memory or another place.|The exercise asks you to retrieve the word without hints.
consolidate|C1|sağlamlaştırmak, birleştirmek|To strengthen something or combine parts into a whole.|The review session helped consolidate earlier learning.
internalize|C1|içselleştirmek|To understand something so well that it becomes natural.|With practice, learners internalize common sentence patterns.
articulate|C1|açıkça ifade etmek|To express an idea clearly and effectively.|She struggled to articulate why the decision bothered her.
paraphrase|C1|başka sözcüklerle anlatmak|To express the same idea using different words.|Try to paraphrase the argument without changing its meaning.
summarize|B2|özetlemek|To state the main points using fewer words.|After listening, summarize the conversation in two sentences.
misinterpret|C1|yanlış yorumlamak|To understand a message in a way the speaker did not intend.|The listener misinterpreted the sarcastic remark.
overlook|C1|gözden kaçırmak|To fail to notice or consider something important.|Do not overlook the final paragraph of the agreement.
underestimate|B2|hafife almak|To judge something as smaller or less difficult than it is.|We underestimated how long the journey would take.
overestimate|B2|olduğundan fazla tahmin etmek|To judge something as greater than it actually is.|He overestimated the amount of free time he would have.
exaggerate|B2|abartmak|To make something seem greater or worse than it is.|The headline exaggerated the significance of the findings.
mitigate|C1|etkisini azaltmak|To make the harmful effects of something less severe.|Planting trees can help mitigate extreme urban heat.
alleviate|C1|hafifletmek|To reduce pain, anxiety, or another unpleasant condition.|A clearer schedule helped alleviate her concerns.
aggravate|C1|kötüleştirmek|To make a problem or situation worse.|Constant interruptions can aggravate an existing problem.
facilitate|C1|kolaylaştırmak|To make a process easier or more likely to succeed.|The moderator facilitated a productive discussion.
coordinate|B2|koordine etmek|To organize people or activities so that they work together.|The volunteers coordinated deliveries across the neighborhood.
collaborate|B2|iş birliği yapmak|To work with someone toward a common goal.|The researchers collaborated on a public health project.
negotiate|B2|müzakere etmek|To discuss terms with others in order to reach an agreement.|They negotiated a flexible payment schedule.
advocate|C1|savunmak, desteklemek|To publicly support a particular policy or idea.|She advocated for safer streets near the school.
prioritize|C1|önceliklendirmek|To decide which tasks or needs deserve attention first.|We should prioritize essential repairs this week.
streamline|C1|yalınlaştırmak, hızlandırmak|To improve a process by removing unnecessary steps.|The team streamlined the registration process.
optimize|C1|en uygun hale getirmek|To adjust something to achieve a better result.|They optimized the route to reduce travel time.
implement|B2|uygulamaya koymak|To put a decision, plan, or system into practice.|The city implemented the new recycling program.
monitor|B2|izlemek, takip etmek|To check a process regularly for changes or problems.|The team monitored air quality throughout the year.
fluctuate|C1|dalgalanmak|To rise and fall irregularly in amount or level.|Ticket prices fluctuate depending on the season.
stabilize|C1|istikrara kavuşturmak|To make something steady after it has been changing.|Several measures helped stabilize the situation.
accelerate|C1|hızlandırmak|To cause a process or change to happen more quickly.|The grant accelerated the renovation project.
decelerate|C1|yavaşlamak|To reduce speed or make progress more slowly.|The vehicle began to decelerate near the intersection.
threshold|C1|eşik değer|A level at which a change or response begins.|The alert activates when the temperature crosses a threshold.
benchmark|C1|karşılaştırma ölçütü|A standard used to compare performance or quality.|The team used a benchmark to assess the new design.
criterion|C1|ölçüt|A condition used when making a judgment or decision.|Cost was only one criterion in their decision.
objective|B2|hedef, amaç|A specific result that someone plans to achieve.|Our main objective is to understand spoken English more easily.
initiative|C1|girişim, yeni çalışma|An organized effort to achieve a particular goal.|The library launched an initiative to encourage reading.
'''
existing={v['word'].lower() for v in data}; added=0
for line in raw.strip().splitlines():
 parts=line.strip().split('|')
 assert len(parts)==5,line
 word,level,tr,definition,example=parts
 if word in existing: continue
 assert len(definition)>25 and len(example)>30,(word,definition,example)
 assert level in ('B2','C1')
 data.append({'id':'g-'+re.sub('[^a-z0-9]+','-',word),'word':word,'tr':tr,'definition':definition,'example':example,'level':level,'category':'general','priority':220+added,'prompt':f'Use “{word}” naturally in your own sentence.','editorialStatus':'authored_unreviewed'})
 existing.add(word);added+=1
assert len({x['id'] for x in data})==len(data)
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Added {added} original vocabulary cards; general total {sum(x["category"]=="general" for x in data)}; no outside review claimed')
