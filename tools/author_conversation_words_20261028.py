#!/usr/bin/env python3
"""Original context-rich vocabulary batch for currently selected 500 B2 / 500 C1.

Human language-review gate remains closed. This script is a deterministic source
of educational draft copy (not copied dictionary definitions or examples).
"""
from pathlib import Path
import json
from promote_content_batch import process
ROOT=Path(__file__).resolve().parents[1]
# word | B2/C1 | TR | original English meaning | two contrasting natural contexts
ROWS="""
straightforward|B2|basit, açık ve anlaşılır|Easy to understand or do because there are no unnecessary complications.|The instructions were straightforward, so we finished quickly.|Her explanation was straightforward and easy to follow.
identify|B2|tanımlamak, tespit etmek|To recognize or determine exactly who or what something is.|Can you identify the song playing in the background?|The mechanic identified the problem after a short test drive.
tolerate|B2|katlanmak, tahammül etmek|To accept something unpleasant without becoming too upset or stopping it.|I can tolerate the noise for another hour.|Some people can't tolerate spicy food at all.
transition|B2|geçiş, değişim süreci|The process of changing from one state, activity, or situation to another.|The transition to a new city was harder than she expected.|They planned a gradual transition to the new schedule.
involvement|B2|katılım, dahil olma|The act of taking part in an activity or being connected with a situation.|Her involvement in the project helped build trust.|The police asked about his involvement in the incident.
nerve|B2|cesaret; sinir|The courage needed to do something frightening or difficult.|She finally found the nerve to ask for a raise.|I don't have the nerve to try skydiving yet.
latter|B2|ikincisi, son sözü edilen|The second of two people or things that have just been mentioned.|We could walk or take the bus; I'd prefer the latter.|Of the two options, the latter costs less.
spite|B2|kin, kötü niyetli inat|An angry desire to upset or hurt someone, often because you feel they treated you badly.|He refused to help his former teammate out of spite.|She admitted that the comment was made out of spite.
slight|B2|hafif, küçük, önemsiz|Small in amount or degree and not usually serious.|There was a slight delay before the train departed.|I noticed a slight change in the way she spoke.
territory|B2|bölge, alan, toprak|An area of land controlled or used by a person, group, or country.|The hikers crossed into unfamiliar territory.|That island is part of a protected territory.
suffering|B2|acı çekme, ıstırap|Physical or emotional pain experienced over a period of time.|The charity helps families affected by prolonged suffering.|He spoke openly about his suffering after the accident.
tenderness|B2|şefkat, hassasiyet|A gentle and caring feeling or behavior toward another person.|She held the injured puppy with great tenderness.|There was real tenderness in the way he spoke to his grandfather.
multiple|B2|birden fazla, çok sayıda|More than one, often involving several people or things at the same time.|The app lets you save multiple addresses.|We had multiple reasons for choosing that apartment.
necessity|B2|gereklilik, zorunluluk|Something that is needed or unavoidable in a particular situation.|A reliable internet connection is a necessity for remote classes.|The storm made an early departure a necessity.
interior|B2|iç kısım, iç mekân|The inside part of a building, vehicle, or other space.|They painted the interior of the house a warm white.|The car's interior was surprisingly spacious.
interfere|B2|müdahale etmek, engel olmak|To become involved in a situation where your actions may cause problems.|I don't want to interfere in their personal decision.|Please don't interfere while I'm explaining the rules.
substance|B2|madde; öz, içerik|A particular kind of material, or the essential meaning of something.|The bottle contained an unknown substance.|Her speech sounded impressive but lacked substance.
headquarters|B2|genel merkez|The main office or central building of an organization.|The company moved its headquarters downtown.|They held the meeting at police headquarters.
instantly|B2|hemen, anında|Immediately or without any noticeable delay.|I recognized her voice instantly.|The room felt warmer instantly when the heater turned on.
somewhat|B2|biraz, bir ölçüde|To a limited degree, but not completely or extremely.|I was somewhat surprised by his answer.|The second apartment is somewhat cheaper.
thoroughly|B2|iyice, baştan sona|Carefully and completely, with attention to all important details.|Please wash the vegetables thoroughly.|We thoroughly checked the reservation before leaving.
surroundings|B2|çevre, etraf, ortam|The places, objects, and conditions that are around a person.|She needed a few days to get used to her new surroundings.|The park's peaceful surroundings made it a good place to read.
mercy|B2|merhamet, acıma|Kind treatment shown to someone when you have the power to punish or hurt them.|The judge asked the jury to consider mercy.|They showed mercy to the injured animal.
intellectual|B2|entelektüel, zihinsel|Connected with thinking, understanding ideas, and using the mind.|The discussion was an interesting intellectual challenge.|She enjoys intellectual debates about history.
trivial|B2|önemsiz, küçük|Too small or unimportant to deserve much attention.|We argued over something trivial and regretted it.|Compared with the safety problem, the delay seemed trivial.
surrender|B2|teslim olmak, vazgeçmek|To stop resisting and accept defeat or another person's control.|The soldiers were ordered to surrender.|He refused to surrender his right to appeal.
invariably|B2|her zaman, değişmez biçimde|In a way that happens almost every time without exception.|He invariably arrives early for family dinners.|The road is invariably crowded on Friday afternoons.
misfortune|B2|talihsizlik, şanssızlık|An unlucky event or difficult situation that happens to someone.|It was a misfortune that they missed the last bus.|She managed to stay optimistic despite her recent misfortunes.
keen|B2|hevesli, çok istekli|Very interested in doing something or eager for it to happen.|She's keen to learn how to cook Italian dishes.|I'm keen on the idea of visiting Chicago someday.
sufficiently|B2|yeterince|To a degree that is enough for a particular purpose.|The instructions weren't sufficiently clear.|Make sure the battery is sufficiently charged before leaving.
hesitation|B2|tereddüt, duraksama|A short pause or delay because you are uncertain about what to do.|After a moment of hesitation, she accepted the invitation.|He answered the question without hesitation.
likewise|B2|aynı şekilde, benzer biçimde|In the same way as someone or something already mentioned.|I enjoyed meeting your family, and I hope they felt likewise.|The first group was excited; the second was likewise enthusiastic.
sincere|B2|samimi, içten|Honest and genuine about what you feel or say.|She offered a sincere apology for the mistake.|I could tell his thanks were sincere.
sympathetic|B2|anlayışlı, halden anlayan|Showing that you understand another person's difficulties or feelings.|My manager was sympathetic when I explained the situation.|He gave me a sympathetic smile after the bad news.
impulse|B2|dürtü, ani istek|A sudden desire to do something without planning it carefully.|I resisted the impulse to check my phone again.|She bought the tickets on impulse.
stimulate|B2|canlandırmak, harekete geçirmek|To make someone or something more active or interested.|The new activities helped stimulate interest in local history.|A short walk can stimulate creative thinking.
significantly|B2|önemli ölçüde, belirgin biçimde|To a degree that is large or important enough to notice.|The changes significantly reduced the waiting time.|Her pronunciation has improved significantly this year.
thoughtful|B2|düşünceli, başkalarını gözeten|Showing that you care about other people's feelings or needs.|It was thoughtful of you to remember her birthday.|He left a thoughtful note for his neighbor.
insufficient|B2|yetersiz|Not enough in amount or quality to achieve a particular result.|The evidence was insufficient to support the claim.|We had insufficient time to finish the tour.
independently|B2|bağımsız olarak, kendi başına|Without depending on another person or organization for help or direction.|She can now travel independently around the city.|The two teams independently reached the same conclusion.
versatility|C1|çok yönlülük, farklı işlere uyum|The ability to be useful or effective in many different roles or situations.|Her versatility makes her a valuable member of the group.|The small room's versatility surprised the new owners.
turmoil|C1|karmaşa, çalkantı, huzursuzluk|A state of intense confusion, uncertainty, or emotional disturbance.|The sudden announcement left the whole office in turmoil.|He tried to stay calm during a period of personal turmoil.
remorse|C1|pişmanlık, vicdan azabı|Deep regret and guilt about something wrong you have done.|She expressed genuine remorse for hurting her friend.|He showed little remorse after admitting the mistake.
verdict|C1|karar, hüküm|A formal decision made by a jury or an opinion reached after consideration.|The jury delivered its verdict late in the afternoon.|The critics' verdict on the new film was mostly positive.
subordinate|C1|ast, daha düşük konumda olan|A person who has less authority than another within an organization.|She made sure her subordinates received proper training.|A good manager listens to concerns raised by subordinates.
vitality|C1|canlılık, enerji, hayat doluluk|The quality of being full of energy, strength, or enthusiasm.|The new neighbors brought fresh vitality to the street.|Regular movement helped him regain his vitality.
temperament|C1|mizaç, kişilik eğilimi|The typical way a person reacts emotionally and behaves in different situations.|His calm temperament helps him handle pressure.|The two siblings have very different temperaments.
enterprising|C1|girişken, fırsatları değerlendiren|Willing to take initiative and find creative ways to achieve something.|An enterprising student started a neighborhood repair service.|Their enterprising approach helped the small business grow.
contested|C1|tartışmalı, çekişmeli|Disputed because different people claim it is true, valid, or theirs.|The election result remained contested for weeks.|They held a public meeting about the contested land.
scathing|C1|çok sert ve yıkıcı (eleştiri)|Severely critical in a way that makes strong disapproval clear.|The newspaper published a scathing review of the show.|Her scathing remarks shocked the whole committee.
restoration|C1|restorasyon, eski haline getirme|The work of returning something old or damaged to a previous good condition.|The restoration of the theater took three years.|They raised money for the restoration of the old bridge.
uninspiring|C1|ilham vermeyen, sıkıcı|Failing to make people feel excited, interested, or motivated.|The presentation was accurate but uninspiring.|They replaced the uninspiring design with something more welcoming.
cost-effective|C1|maliyet açısından verimli|Providing good results or value without costing more money than necessary.|Taking the train is the most cost-effective option for us.|The clinic found a cost-effective way to reduce waste.
restorative|C1|dinlendirici, iyileştirici|Helping someone recover energy, health, or a feeling of well-being.|A quiet walk can be surprisingly restorative.|She found the weekend away both peaceful and restorative.
resort|C1|son çare olarak başvurmak|To use a method when other options have failed or are unavailable.|We didn't want to resort to borrowing money.|They resorted to paper maps when the signal disappeared.
spontaneously|C1|kendiliğinden, plansızca|Without being planned or forced in advance.|The audience spontaneously began to applaud.|We spontaneously decided to drive to the coast.
reassure|C1|içini rahatlatmak, güven vermek|To tell someone something that makes them feel less worried or uncertain.|She reassured me that the flight was still on time.|The doctor tried to reassure the nervous patient.
reluctantly|C1|isteksizce, gönülsüzce|In a way that shows you are unwilling or hesitant to do something.|He reluctantly agreed to join the group photo.|She reluctantly handed over the keys.
hostility|C1|düşmanlık, sert karşıtlık|Strong dislike, anger, or opposition toward someone or something.|There was obvious hostility between the two neighbors.|The proposal was met with hostility at the meeting.
continuity|C1|süreklilik, kesintisizlik|The quality of continuing without an interruption or major change.|The school wanted continuity during the leadership change.|Keeping one teacher gave the class a sense of continuity.
jurisdiction|C1|yargı yetkisi, yetki alanı|The legal authority to make decisions or enforce laws in a particular area.|The case falls under the jurisdiction of the local court.|The agency has no jurisdiction outside the state.
advantageous|C1|avantajlı, yararlı|Likely to provide a benefit or put someone in a better position.|The flexible schedule was advantageous for working parents.|It may be advantageous to book the tickets early.
profoundly|C1|derinden, çok güçlü biçimde|To an extremely great degree, especially in an emotional or important way.|The story profoundly changed how she viewed her hometown.|She was profoundly grateful for the support.
indefinitely|C1|belirsiz süreyle, süresiz olarak|For an unknown period of time with no fixed end date.|The outdoor concert was postponed indefinitely.|He couldn't stay with his relatives indefinitely.
meaningless|C1|anlamsız, hiçbir şey ifade etmeyen|Having no useful purpose, clear meaning, or important value.|The numbers are meaningless without some context.|He felt the apology was meaningless without changed behavior.
trauma|C1|travma, ağır duygusal sarsıntı|A deeply distressing experience or its lasting psychological effects.|The family needed support after the trauma of the accident.|She spoke carefully about the trauma she had experienced.
precision|C1|hassasiyet, kesinlik|The quality of being very exact, accurate, or carefully controlled.|The chef cut each piece with remarkable precision.|The instructions need more precision to avoid confusion.
render|C1|bir hale getirmek, sebep olmak|To cause someone or something to be in a particular condition.|The heavy snow rendered the road impassable.|The power outage rendered the elevator unusable.
insensitive|C1|duyarsız, düşüncesiz|Not showing enough concern for other people's feelings or difficulties.|His joke was insensitive given what had happened.|She apologized for making an insensitive comment.
ingenious|C1|zekice, yaratıcı, dahiyane|Very clever and inventive, especially in solving a difficult problem.|She came up with an ingenious way to save space.|The team's ingenious solution impressed the judges.
""".strip()

def make():
 out=[]
 for n,line in enumerate(ROWS.splitlines(),1):
  parts=[v.strip() for v in line.split('|')]
  if len(parts)!=6:raise ValueError(f'row {n}: {parts}')
  word,level,tr,definition,a,b=parts
  out.append({'word':word,'level':level,'tr':tr,'definition':definition,
              'example':a,'examples':[a,b],
              'prompt':f'Use “{word}” naturally in your own sentence.',
              'levelStatus':'source_candidate_unreviewed'})
 return out

if __name__=='__main__':
 records=make()
 origin=json.loads((ROOT/'data/fluency-focus.json').read_text())
 focus={r['word']:r['level'] for r in origin['vocabulary']}
 unexpected=[r['word'] for r in records if focus.get(r['word'])!=r['level']]
 if unexpected:raise ValueError(f'Not currently selected with supplied levels: {unexpected}')
 out=ROOT/'sources/authored-20261028-conversational-words.jsonl'
 out.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in records),encoding='utf8')
 existing={x['word'].casefold() for x in json.loads((ROOT/'data/vocabulary.json').read_text()) if x.get('category')=='general'}
 missing=[row for row in records if row['word'].casefold() not in existing]
 if missing:
  pending=ROOT/'sources/.pending-20261028-general.jsonl'
  try:
   pending.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in missing),encoding='utf8')
   result=process(pending,'general',apply=True)
  finally: pending.unlink(missing_ok=True)
 else: result={'mode':'already_applied','validatedNewCards':0,'releaseReady':False}
 print(json.dumps(result,ensure_ascii=False))
