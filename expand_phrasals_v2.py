#!/usr/bin/env python3
"""A second, manually authored batch of distinct higher-level phrasal verbs.
No claim of external CEFR or native-editor signoff. Definitions/examples are
original; editorialStatus remains authored_unreviewed pending validation.
"""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# word | Turkish contextual gloss | English sense definition | example 1 | example 2 | syntax | level
ROWS='''
back off | baskı yapmayı bırakmak | To stop pressuring or threatening someone and move away from a confrontation. | The reporter backed off when the witness asked for privacy. | After several warnings, the aggressive driver finally backed off. | intransitive | B2
bail out | mali sıkıntıdan kurtarmak | To rescue an organization or person from a serious financial problem by providing money. | The city refused to bail out the failing sports club. | Taxpayers questioned the decision to bail the airline out. | separable | C1
block off | erişimi engellemek | To prevent people or vehicles from entering a particular area. | Workers blocked off the street while repairing a broken water pipe. | Police blocked the entrance off after the safety inspection. | separable | B2
break off | aniden sona erdirmek | To end a conversation, relationship, or negotiation suddenly. | The two companies broke off negotiations after the deadline passed. | She broke off the discussion when the meeting became hostile. | separable | B2
bring along | beraberinde getirmek | To take someone or something with you to a place or activity. | Bring along a printed map in case your phone loses its signal. | She brought her younger cousin along to the exhibition. | separable | B2
bring down | azaltmak, düşürmek | To reduce the level, amount, or price of something. | The retailer hopes to bring down delivery costs next year. | A small change in design brought the production expense down. | separable | B2
bring in | yeni bir sistemi uygulamaya sokmak | To introduce a new rule, system, or practice. | The library brought in a new reservation policy last spring. | The school brought in digital registration after a trial period. | separable | B2
bring out | bir niteliği ortaya çıkarmak | To make a particular quality in someone or something more noticeable. | The quiet setting brought out her creative side. | The bright lighting brought the colors of the painting out. | separable | B2
carry over | sonraki döneme aktarmak | To move an amount, idea, or result from one period or situation to another. | Unused vacation days cannot be carried over into next year. | The accountant carried the remaining balance over to the next period. | separable | B2
chicken out | korkup vazgeçmek | To decide not to do something because you are suddenly afraid. | He planned to jump into the lake but chickened out at the last moment. | I nearly chickened out before making my first public speech. | intransitive | C1
come apart | parçalara ayrılmak | To separate into pieces or stop holding together. | The old chair came apart when someone tried to move it. | The wooden frame began to come apart after years in the rain. | intransitive | B2
come in for | eleştiriye maruz kalmak | To receive criticism, blame, or other unwanted attention. | The agency came in for criticism over the confusing instructions. | The proposal came in for sharp criticism during the public hearing. | inseparable | C1
come off as | izlenimi vermek | To appear to have a certain quality to other people, sometimes unintentionally. | His brief reply came off as dismissive, even though he was busy. | She came off as confident during the interview. | inseparable | B2
crack down on | sert önlemlerle mücadele etmek | To take stronger action to stop illegal or unacceptable behavior. | The city promised to crack down on illegal dumping near the river. | Officials cracked down on the sale of counterfeit tickets. | inseparable | C1
crop up | beklenmedik şekilde ortaya çıkmak | To happen or appear unexpectedly, often as a problem. | Several new questions cropped up after the first inspection. | Minor delays can crop up during any large renovation. | intransitive | C1
cut through | karmaşayı aşarak netleşmek | To get past confusion or unnecessary detail and reach what matters. | Her simple example cut through the confusion in the room. | We need an explanation that cuts through the technical jargon. | inseparable | C1
do away with | yürürlükten kaldırmak | To get rid of a rule, practice, or system completely. | The organization plans to do away with unnecessary paperwork. | The new policy did away with the old registration fee. | inseparable | C1
draw up | belge veya plan hazırlamak | To prepare a formal document or detailed plan. | The attorney drew up a new agreement for both parties. | Volunteers drew up a schedule for maintaining the community garden. | separable | C1
fall back on | son çare olarak başvurmak | To rely on a backup resource or plan when another option fails. | If the train is canceled, we can fall back on the bus route. | She fell back on her savings while looking for another job. | inseparable | C1
fall through | plan gerçekleşmemek | To fail to happen despite earlier plans or expectations. | Our travel plans fell through when the ferry stopped operating. | The agreement fell through just before the scheduled announcement. | intransitive | B2
face up to | zor bir gerçeği kabul etmek | To accept and deal with an unpleasant fact or difficult situation. | The board had to face up to the limits of its budget. | He finally faced up to the mistakes in his report. | inseparable | C1
feel up to | kendini yapabilecek durumda hissetmek | To feel physically or mentally capable of doing something. | She did not feel up to attending the crowded event. | Do you feel up to answering a few more questions? | inseparable | B2
fit in with | uyum sağlamak | To be compatible with an existing plan, group, or arrangement. | The new schedule does not fit in with her evening classes. | His proposal fits in with the museum's long-term goals. | inseparable | B2
go back on | sözünden dönmek | To fail to keep a promise or agreement that you previously made. | The contractor went back on the promise to finish by Friday. | She refused to go back on her word, even under pressure. | inseparable | C1
go in for | bir etkinlikten hoşlanmak | To enjoy or regularly take part in a type of activity. | He does not go in for competitive sports, but he loves hiking. | She has always gone in for puzzles and logic games. | inseparable | B2
hit it off | hemen iyi anlaşmak | To become friendly with someone immediately after meeting them. | The two volunteers hit it off during their first shift. | They hit it off at the conference and stayed in touch afterward. | intransitive | B2
hold out | umudu sürdürmek | To continue to hope or believe that something will happen. | The villagers still hold out hope that the old bridge can be repaired. | Researchers held out hope for a breakthrough despite several setbacks. | inseparable | C1
live up to | beklentileri karşılamak | To be as good as people expected or as good as a claimed standard. | The new exhibition lived up to the impressive reviews. | The hotel struggled to live up to its reputation for exceptional service. | inseparable | B2
make off with | çalıp kaçmak | To steal something and escape with it. | The thief made off with a rare painting before the museum opened. | Someone made off with several expensive cameras during the event. | inseparable | C1
make out | güçlükle seçebilmek | To see, hear, or understand something with difficulty. | Through the fog, we could barely make out the outline of the lighthouse. | I could not make out the announcement over the station noise. | separable | B2
own up to | hatasını itiraf etmek | To admit that you did something wrong or made a mistake. | The employee eventually owned up to the error in the report. | Nobody wanted to own up to leaving the door unlocked. | inseparable | C1
pin down | kesin olarak belirlemek | To identify or define something precisely after uncertainty. | The researchers struggled to pin down the cause of the unusual signal. | We should pin the exact delivery date down before signing. | separable | C1
play down | önemini küçümsemek | To make a problem or event seem less important than it really is. | Officials tried to play down the impact of the service interruption. | The spokesperson played the cost increase down during the interview. | separable | C1
put forward | öneri sunmak | To suggest an idea or proposal for others to consider. | Residents put forward a proposal for safer bicycle lanes. | The committee put three alternatives forward for public discussion. | separable | B2
run up against | beklenmedik bir engelle karşılaşmak | To encounter a difficulty or obstacle while doing something. | The research team ran up against strict budget limitations. | We ran up against a technical problem during the first test. | inseparable | C1
see through | aldatmacayı fark etmek | To recognize that someone is trying to deceive you. | The inspector saw through the fake explanation immediately. | She saw right through his attempt to shift the blame. | separable | C1
set about | bir işe girişmek | To begin doing something, especially a task that requires planning or effort. | The volunteers set about cleaning the riverbank after the storm. | She set about organizing the documents into separate folders. | inseparable | C1
sink in | gerçeğin yavaş yavaş anlaşılması | To be gradually understood or accepted after a surprising event. | The news did not sink in until he spoke with his family. | It took a while for the scale of the damage to sink in. | intransitive | C1
spring up | hızla ortaya çıkmak | To appear or develop suddenly in a place or situation. | New food stalls sprang up around the renovated train station. | Several small parks have sprung up across the neighborhood. | intransitive | B2
stand up to | baskıya karşı durmak | To resist someone who is trying to control or intimidate you. | She stood up to the landlord over the unsafe repairs. | The students stood up to pressure to change their findings. | inseparable | B2
tie in with | bağlantılı olmak | To be connected with or consistent with something else. | The survey results tie in with observations from the field. | The new exhibit ties in with the museum's anniversary program. | inseparable | C1
track down | araştırarak bulmak | To find someone or something after searching carefully. | The historian tracked down the original letter in a regional archive. | They tracked the missing shipment down using its serial number. | separable | B2
weed out | işe yaramayanları ayıklamak | To remove unwanted or unsuitable things or people from a group. | The editor weeded out unsupported claims before publication. | The team weeded duplicate records out of the database. | separable | C1
wear off | etkisi zamanla azalmak | To gradually disappear or become less strong. | The excitement wore off after the first week of the exhibition. | Her headache returned as the pain medication wore off. | intransitive | B2
wind down | yavaş yavaş sonlandırmak | To gradually reduce an activity until it ends. | The organizers began to wind down the festival after sunset. | The company is winding down its operations in the old building. | separable | B2
weigh in on | tartışmaya görüş bildirmek | To express an opinion about a question or public debate. | Several researchers weighed in on the proposed environmental rule. | Residents were invited to weigh in on the new parking plan. | inseparable | C1
zero in on | belirli bir noktaya odaklanmak | To direct attention very precisely to one issue or target. | The investigation zeroed in on a discrepancy in the records. | The team zeroed in on the most likely source of the leak. | inseparable | C1
zoom in on | yakından odaklanmak | To focus on a particular detail or part of a larger picture. | The documentary zoomed in on the lives of two neighborhood volunteers. | Let's zoom in on the final paragraph of the report. | inseparable | B2
phase in | kademeli olarak uygulamaya koymak | To introduce a policy, system, or change in stages over time. | The university will phase in the new registration system over two years. | The transit authority phased the fare changes in gradually. | separable | C1
shore up | zayıf durumu güçlendirmek | To give additional support to something that is weak or at risk. | The theater launched a fundraiser to shore up its finances. | Engineers used temporary supports to shore the damaged wall up. | separable | C1
brush off | önemsemeyip geçiştirmek | To dismiss a concern or criticism without giving it serious attention. | The manager brushed off the complaints about the broken elevator. | She brushed the warning off until the problem became worse. | separable | C1
wipe out | tamamen yok etmek | To destroy or remove something almost completely. | The storm wiped out several sections of the coastal road. | A single software error wiped the unsaved data out. | separable | B2
play out | olayların zamanla gelişmesi | To develop or happen over time, often in an uncertain way. | No one knows how the negotiations will play out. | We watched the final stage of the rescue play out on the news. | intransitive | C1
settle into | yeni düzene alışmak | To become comfortable in a new place or situation. | It took several weeks to settle into the new apartment. | The children settled into their school routine by the end of September. | inseparable | B2
weigh down | yük olmak, baskı yaratmak | To make someone or something feel burdened by a heavy weight or concern. | The unresolved debt weighed the family down for months. | Heavy equipment weighed down the small rescue boat. | separable | C1
wear down | yavaş yavaş yormak | To gradually exhaust a person or make resistance weaker over time. | Constant delays wore down the volunteers' enthusiasm. | The negotiations wore both sides down after several long days. | separable | C1
pitch in | yardım etmek, el atmak | To join an effort by providing help or resources. | Neighbors pitched in to repair the damaged playground. | Everyone pitched in when the community kitchen needed extra hands. | intransitive | B2
pan out | beklendiği gibi sonuçlanmak | To develop in a particular way, especially successfully or unsuccessfully. | The plan did not pan out as the organizers had hoped. | We'll see how the new program pans out over the next few months. | intransitive | C1
let up | şiddeti azalmak | To become less intense, severe, or persistent. | The rain finally let up just before the outdoor performance. | The pressure did not let up after the first round of talks. | intransitive | B2
brush aside | önemsemeyerek kenara itmek | To ignore a concern or objection instead of considering it carefully. | The committee brushed aside residents' concerns about noise. | He brushed the criticism aside without reading the report. | separable | C1
talk down to | küçümseyerek konuşmak | To speak to someone as though they are less intelligent or less capable. | The presenter talked down to the audience during the workshop. | She dislikes being talked down to by customer service staff. | inseparable | C1
round out | tamamlayarak çeşitlendirmek | To complete something by adding what is missing to make it balanced. | A final chapter rounds out the book's account of the expedition. | The course added a speaking unit to round the program out. | separable | C1
carry through | sonuna kadar sürdürmek | To continue a plan or promise until it is fully completed. | The team carried through the plan to restore the park. | They carried the project through despite repeated setbacks. | separable | C1
catch on to | farkına varmak, kavramak | To understand an idea or realize that something is happening. | She quickly caught on to the reason for the unusual delay. | It took me a while to catch on to the instructor's method. | inseparable | B2
back out of | verdiği sözden dönüp çekilmek | To withdraw from an agreement or commitment before completing it. | The supplier backed out of the deal the day before signing. | She did not want to back out of the volunteer commitment. | inseparable | B2
'''

def parse():
 out=[]
 for raw in ROWS.strip().splitlines():
  parts=[x.strip() for x in raw.split('|')]
  if len(parts)!=7:raise ValueError(f'Malformed row {raw}')
  word,tr,definition,ex1,ex2,syntax,level=parts
  if syntax not in {'separable','inseparable','intransitive'} or level not in {'B2','C1'}:raise ValueError(word)
  if not word.count(' ')>=1 or len(definition)<28 or ex1==ex2:raise ValueError(word)
  out.append({'id':'pv-'+re.sub(r'[^a-z0-9]+','-',word).strip('-'),'word':word,'tr':tr,'definition':definition,'example':ex1,'examples':[ex1,ex2], 'level':level,'syntax':syntax,'register':'neutral','note':{'separable':'A noun object may precede or follow the particle depending on context; place a pronoun between verb and particle when this sense permits.','inseparable':'Keep the object after the full phrasal expression.','intransitive':'This sense does not take a direct object.'}[syntax], 'senses':[{'tr':tr,'definition':definition,'example':ex1}], 'editorialStatus':'authored_unreviewed'})
 return out

def main():
 file=ROOT/'data/phrasals.json';existing=json.loads(file.read_text(encoding='utf8'))
 known={p['word'].lower() for p in existing}
 added=[]
 for item in parse():
  if item['word'].lower() in known:continue
  item['priority']=200+len(added)
  existing.append(item);added.append(item['word'])
 file.write_text(json.dumps(existing,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps({'added':len(added),'total':len(existing),'words':added},ensure_ascii=False))

if __name__=='__main__':main()
