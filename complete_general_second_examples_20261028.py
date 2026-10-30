#!/usr/bin/env python3
"""Add independently authored second American-English context examples in place.

Existing IDs and primary examples remain untouched. Idempotent and not an editorial
approval; semantic review still required before release.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SECOND='''
exceed|Our bags cannot exceed the airline's weight limit.
exclude|I felt hurt when my friends excluded me from the plan.
exhaustive|We made an exhaustive list of everything we need for the move.
expand|The family plans to expand their kitchen next summer.
explicit|Be explicit about what time you want me to arrive.
exploit|Some scams exploit people's fear of missing out.
facilitate|A shared calendar can facilitate planning for the whole family.
feasible|Working from home three days a week seems feasible now.
fluctuate|My energy levels tend to fluctuate throughout the day.
formulate|We need to formulate a response before the meeting starts.
fundamental|Getting enough sleep is fundamental to feeling better.
furthermore|The apartment is noisy; furthermore, it's far from the subway.
grant|The university granted her an extension on the assignment.
highlight|He highlighted the most important dates on the calendar.
hypothesis|Her hypothesis was that the noise came from the pipes.
identical|I accidentally bought two identical phone cases.
illustrate|This photo illustrates how crowded the beach was.
implement|The school will implement a new pickup policy in January.
imply|Are you implying that I forgot your birthday on purpose?
incentive|A free breakfast is a nice incentive to wake up early.
incorporate|Try to incorporate a short walk into your lunch break.
inherent|There's an inherent risk in driving during a snowstorm.
initiative|She took the initiative and organized the neighborhood cleanup.
legitimate|That's a legitimate concern, and we should talk about it.
manipulate|He tried to manipulate the conversation to avoid answering.
marginal|The new route saves only a marginal amount of time.
moderate|The hike is of moderate difficulty, so bring comfortable shoes.
notion|I don't like the notion that everyone has to be available all day.
obscure|The restaurant is hidden on an obscure side street.
ongoing|Our ongoing renovations have made the house pretty noisy.
paradox|It's a paradox that more choices can make decisions harder.
perceive|People may perceive the same comment in very different ways.
precise|Can you give me a precise time for your arrival?
predominant|Blue is the predominant color in the new living room.
preliminary|The preliminary results look promising, but nothing is final.
presume|I presume you'll want some coffee when you get here.
prominent|The hotel has a prominent sign above the entrance.
prospect|The prospect of moving abroad makes her both excited and nervous.
pursue|He decided to pursue photography as a hobby.
rationale|What's the rationale behind changing the dinner reservation?
remarkable|It's remarkable how quickly the kids have grown.
resilient|She's been remarkably resilient through all the recent changes.
reveal|The surprise party was ruined when someone revealed the plan.
rigorous|Their training schedule is rigorous but manageable.
scenario|Let's consider a scenario where our flight gets canceled.
scope|Planning the entire wedding is beyond the scope of this weekend.
simultaneously|She was cooking dinner and talking on the phone simultaneously.
speculate|We can speculate about the reason, but we don't know yet.
stability|Having a regular routine gives the children a sense of stability.
substantial|We made substantial progress cleaning out the garage.
tangible|After weeks of practice, I finally saw tangible improvement.
tentative|We have a tentative plan to leave on Friday morning.
thorough|Give the apartment a thorough cleaning before the guests arrive.
threshold|The noise level crossed my threshold for a peaceful evening.
transmit|The baby monitor transmits sound to the other room.
trigger|That smell can trigger memories of my grandmother's kitchen.
ultimately|We ultimately decided to stay home instead of going out.
unprecedented|The city saw unprecedented crowds during the festival.
undergo|The old house will undergo major repairs next month.
undertake|We shouldn't undertake such a long trip without planning.
valid|Your ticket is valid until the end of the month.
viable|Taking the train is a viable alternative to driving.
vulnerable|Older neighbors may be especially vulnerable during a heat wave.
widespread|There was widespread confusion about the new parking rules.
affluent|It's an affluent neighborhood with many large homes.
alleviate|A warm bath may alleviate some of the tension in your shoulders.
anecdote|He told a funny anecdote about his first day at school.
apt|She's apt to forget her keys when she's in a hurry.
bolster|Positive feedback helped bolster her confidence before the interview.
cautious|I'm cautious about buying a used car without an inspection.
compromise|We compromised and chose a restaurant halfway between our homes.
consecutive|It rained for three consecutive days during our vacation.
contradict|His explanation seems to contradict what he said yesterday.
correlate|Does the amount of sleep you get correlate with your mood?
counterpart|I met my counterpart from the other office at lunch.
culminate|The celebration will culminate in a fireworks display.
discrepancy|There's a discrepancy between the receipt and my bank statement.
dispute|The neighbors are in a dispute over the shared fence.
disrupt|Road construction may disrupt our usual commute.
distinguish|It's hard to distinguish the twins when they're wearing hats.
diminish|The noise began to diminish as the traffic cleared.
dilemma|I'm facing a dilemma: attend the wedding or take the trip.
empathy|She showed real empathy when I told her about my bad day.
ethical|Is it ethical to share a private message without permission?
exaggerate|Don't exaggerate how bad the traffic was; we were ten minutes late.
exemplify|Her willingness to help exemplifies what I love about this town.
foster|Community events can foster friendships between neighbors.
grievance|He raised a grievance about how the building is maintained.
hostile|The crowd became hostile after the concert was canceled.
impartial|We asked an impartial friend to help settle the disagreement.
inadequate|The hotel room's heating was inadequate for the cold weather.
inclined|I'm inclined to take the earlier train to avoid traffic.
indispensable|A reliable phone charger is indispensable when I travel.
intact|Luckily, the glass vase arrived intact after the move.
intriguing|That sounds like an intriguing idea for a weekend trip.
irrelevant|The color of the car is irrelevant to how safely it drives.
leverage|We can leverage our shared contacts to organize the reunion.
mandatory|Wearing a helmet is mandatory on this cycling tour.
mutual|We discovered a mutual love of old movies.
objective|Let's try to stay objective while we compare the options.
obstacle|Finding childcare was the biggest obstacle to attending the event.
outweigh|For me, the benefits of a short commute outweigh the higher rent.
persistent|A persistent cough kept him awake all night.
prevalent|Seasonal allergies are particularly prevalent here in the spring.
reconcile|It took them a while to reconcile after the argument.
redundant|The last paragraph is redundant because it repeats the same point.
repercussion|Missing the last bus had an unexpected repercussion: a long walk home.
skepticism|I understand your skepticism about such an unbelievable offer.
spontaneous|We took a spontaneous road trip on Sunday afternoon.
streamline|Packing the night before can streamline the morning routine.
susceptible|My phone is more susceptible to damage without a case.
unanimous|The family was unanimous in choosing the beach for our vacation.
undermine|Constant interruptions can undermine someone's confidence.
versatile|This jacket is versatile enough for work or the weekend.
warrant|The strange noise may warrant a visit from a mechanic.
whereas|I prefer quiet mornings, whereas my sister likes loud music.
withdraw|I decided to withdraw my application after learning more.
withstand|The outdoor furniture should withstand a rainy winter.
pervasive|The smell of fresh bread was pervasive throughout the house.
substantiate|Can you substantiate your claim with a receipt or a photo?
refute|She used the video to refute the rumor about the incident.
provisional|Our provisional booking will be confirmed after payment.
robust|This backpack feels robust enough for everyday use.
fragile|Handle that antique mirror carefully because it's fragile.
volatile|Gas prices have been volatile over the past few months.
lucrative|Renting out the extra room became a lucrative side business.
scarcity|A scarcity of parking spaces makes this street difficult to visit.
allocation|We agreed on an allocation of chores for the week.
trade-off|Living downtown involves a trade-off between space and convenience.
contingency|We have a contingency plan in case our flight is delayed.
accountability|Clear responsibilities help create accountability in a shared apartment.
transparency|We appreciate the landlord's transparency about the repair costs.
credibility|The article lost credibility when its facts turned out to be wrong.
authenticity|I love the authenticity of the small family-run restaurant.
integrity|She showed integrity by admitting she had made a mistake.
disincentive|The high parking fee is a disincentive to driving downtown.
compliance|The building needs to be in compliance with safety regulations.
inconsistency|I noticed an inconsistency between the two versions of the story.
subsequent|The first class was difficult, but subsequent lessons felt easier.
preceding|She hadn't slept well during the preceding week.
simultaneous|The two children made simultaneous requests for a snack.
intermittent|We had intermittent internet access during the storm.
sporadic|The neighbors made sporadic attempts to repair the old gate.
innovative|It's an innovative way to make a small apartment feel bigger.
obsolete|My old phone became obsolete when the network changed.
mediate|A neighbor offered to mediate the disagreement about the fence.
consensus|After a long discussion, we reached a consensus on the venue.
dissent|There was some dissent when the group chose the expensive restaurant.
adversity|She stayed hopeful even in the face of serious adversity.
adversarial|The discussion became adversarial when neither side would listen.
empathetic|He was empathetic when I explained why I was upset.
apprehensive|I'm apprehensive about speaking in front of so many strangers.
indifferent|He seemed indifferent to which movie we watched.
resentment|Unspoken resentment can grow after repeated small disagreements.
reassurance|Her calm words gave me the reassurance I needed.
frustration|He sighed with frustration when the train was delayed again.
curiosity|My curiosity led me into a little bookstore on the corner.
scrutiny|The new proposal came under scrutiny at the neighborhood meeting.
maintainable|A simpler garden design will be more maintainable over time.
perception|My perception of the city changed after I spent a week there.
misconception|It's a common misconception that you have to be fluent to travel.
inference|From her smile, I made the inference that the surprise went well.
implication|One implication of moving farther away is a longer commute.
examine|The dentist will examine my teeth at the next appointment.
retrieve|Could you retrieve my suitcase from the back of the car?
consolidate|We decided to consolidate our subscriptions into one account.
internalize|It takes practice to internalize a new pronunciation pattern.
paraphrase|Can you paraphrase what the speaker said in simpler words?
summarize|Please summarize the movie without giving away the ending.
misinterpret|I hope you don't misinterpret my silence as disagreement.
underestimate|Don't underestimate how long it takes to get to the airport.
overestimate|I think we overestimated how much food the guests would eat.
aggravate|Loud music can aggravate a headache after a long day.
coordinate|We need to coordinate pickup times with the other parents.
collaborate|We collaborated on a neighborhood garden last summer.
negotiate|Try to negotiate a better price before buying the bicycle.
optimize|We reorganized the kitchen to optimize the limited space.
monitor|I'll monitor the weather before deciding whether to drive.
stabilize|The table stopped wobbling after we stabilized its legs.
accelerate|Traffic began to accelerate once we passed the construction zone.
decelerate|Drivers should decelerate as they approach the sharp turn.
criterion|Price isn't the only criterion when choosing a new apartment.
'''.strip()

def apply(root=ROOT):
    lines=[line.split('|',1) for line in SECOND.splitlines() if line.strip()]
    if len(lines)!=len(set(k for k,_ in lines)):raise ValueError('duplicate authored second example')
    authored=dict(lines)
    path=root/'data/vocabulary.json'
    data=json.loads(path.read_text(encoding='utf8'))
    missing={x['word'] for x in data if x.get('category')=='general' and len(set(x.get('examples',[])))<2}
    not_found=missing-set(authored)
    if not_found:raise ValueError(f'missing handcrafted second examples: {sorted(not_found)}')
    for x in data:
        if x.get('category')!='general' or x['word'] not in missing:continue
        example=authored[x['word']]
        if len(example)<25:raise ValueError(f'example too short: {x["word"]}')
        if example.lower()==x['example'].lower():raise ValueError(f'duplicate primary: {x["word"]}')
        x['examples']=[x['example'],example]
    changed=len(missing)
    if changed:path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return {'fixed':changed,'generalRemainingWithOneExample':sum(x.get('category')=='general' and len(set(x.get('examples',[])))<2 for x in data),'editorialApproval':False}

if __name__=='__main__':print(json.dumps(apply(),ensure_ascii=False))
