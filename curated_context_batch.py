#!/usr/bin/env python3
"""Add manually authored, distinct American-English contextual examples.
These examples are new authored teaching copy, NOT independently signed off.
Idempotent: running the script twice never duplicates existing examples.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GENERAL='''
acknowledge | The mayor acknowledged the concerns raised during the public meeting.
appreciate | You begin to appreciate the quiet once the traffic dies down.
crucial | Clear instructions are crucial when a team works across different time zones.
outcome | Neither side could predict the outcome of the negotiations.
reluctant | He seemed reluctant to admit that he needed additional help.
maintain | The volunteers struggled to maintain the trail after a harsh winter.
consistent | Her explanation remained consistent even after several difficult questions.
assumption | The entire plan rested on the assumption that prices would remain stable.
emphasize | The instructor emphasized the importance of checking your sources.
apparent | It became apparent that the bridge would need extensive repairs.
relevant | Please include only documents relevant to this particular claim.
significant | The study found a significant difference between the two groups.
ensure | We installed a backup battery to ensure the lights would stay on.
assess | The rescue team assessed the damage before entering the building.
enhance | Simple lighting changes can enhance the atmosphere of a room.
obtain | Guests must obtain a permit before camping in the protected area.
encounter | Travelers may encounter sudden storms along the coastal road.
overlook | It's easy to overlook small details when you're working under pressure.
prioritize | The committee agreed to prioritize repairs to the oldest schools.
investigate | Local officials promised to investigate the unexplained water leak.
skeptical | Residents were skeptical of the company's optimistic forecast.
plausible | Her explanation sounded plausible, but there was no supporting evidence.
equivalent | The two programs offer equivalent benefits despite their different names.
transparent | The organizers made the selection process transparent to all applicants.
awareness | The campaign raised awareness of food waste in local restaurants.
inevitable | Some delays were inevitable because the roads were still flooded.
insight | Talking to former residents gave the historian valuable insight into the neighborhood.
profound | The experience had a profound impact on the way she viewed her hometown.
reinforce | The repeated practice helped reinforce the patterns she had just learned.
sustain | A small town may struggle to sustain a large cultural festival every year.
resolve | The neighbors met to resolve a disagreement about the shared driveway.
articulate | He found it hard to articulate why the painting moved him so deeply.
justify | The report did not provide enough evidence to justify the expense.
sophisticated | The museum uses a sophisticated system to protect fragile exhibits.
distinct | Although the twins look alike, their personalities are quite distinct.
evaluate | Before joining the program, she evaluated its long-term commitments.
diverse | The festival attracted a diverse crowd from several generations.
concrete | The proposal needs concrete details about costs and deadlines.
perspective | Listening to the other side changed her perspective on the dispute.
retain | Students retain new expressions better when they use them in different contexts.
credible | The journalist waited for a credible source before publishing the claim.
acquire | Over time, he acquired a deep understanding of the local culture.
allocate | The school plans to allocate more funding to its library.
arbitrary | The deadline felt arbitrary because no reason was given for choosing it.
assert | The witness continued to assert that she had seen the vehicle leave.
authentic | The restaurant serves authentic regional dishes using local ingredients.
bias | The team examined the survey for possible bias in its questions.
breakthrough | Researchers described the new treatment as an important breakthrough.
capability | The small drone has the capability to operate in strong winds.
coherent | Her argument was coherent and easy to follow, even on a complex topic.
comprehensive | The guide provides a comprehensive overview of regional hiking routes.
concede | After reviewing the evidence, the editor conceded that the criticism was fair.
consequence | A consequence of the policy was longer lines at the station.
considerable | The renovation required considerable effort from the entire community.
constraint | Limited access to clean water was the project's main constraint.
conventional | They rejected the conventional approach and designed an outdoor classroom.
convey | A short handwritten note can convey genuine gratitude.
decisive | The final interview proved decisive in the hiring process.
dedicate | She decided to dedicate a year to restoring the historic house.
deduce | From the wet footprints, they deduced that someone had entered recently.
deficient | The inspection revealed that the building's ventilation was deficient.
deliberate | His deliberate pause gave the audience time to consider the question.
demonstrate | The experiment was designed to demonstrate the effect of temperature on pressure.
deprive | The new highway would deprive several homes of direct access to the river.
derive | Many modern English expressions derive from older forms of the language.
deteriorate | The wooden steps began to deteriorate after years of exposure to rain.
dominant | One company became dominant in the regional shipping industry.
dramatic | A dramatic change in the weather forced the hikers to turn back.
elaborate | Could you elaborate on how the proposed schedule would work?
eliminate | The organizers redesigned the route to eliminate unnecessary delays.
emerge | A clearer picture began to emerge after the witnesses compared notes.
endure | Some desert plants can endure months without significant rainfall.
entail | Organizing the event will entail working with several different teams.
establish | The researchers hope to establish a reliable baseline for future studies.
evident | Her disappointment was evident despite her polite response.
'''
PHRASALS='''
get around to | I finally got around to fixing the loose cabinet door last weekend.
break out | A fire broke out in the warehouse shortly after midnight.
hold back | She held back her tears until the ceremony was over.
narrow down | We narrowed down the list to three promising candidates.
rule out | The doctor could not rule out an allergic reaction without further tests.
call off | They called off the outdoor concert because of the lightning.
step down | The director announced that she would step down at the end of the year.
look up to | As a child, he looked up to his grandfather for his patience and kindness.
bring about | The new rail line brought about major changes to the neighborhood.
account for | How do you account for the sudden increase in electricity use?
act on | The city acted on the complaints and repaired the damaged sidewalk.
add up | His explanation doesn't add up when you compare it with the receipts.
back down | Neither side was willing to back down during the final round of talks.
bear out | The later measurements bore out the engineer's initial estimate.
blow up | A minor disagreement blew up into a much larger argument.
boil down to | For most visitors, the choice boils down to cost and convenience.
branch out | The bakery branched out into catering after receiving several requests.
break into | Someone tried to break into the storage room during the night.
brush up on | She brushed up on her French before visiting relatives in Montreal.
build up | The hikers built up their endurance through regular weekend walks.
call for | The unexpected snowfall called for a change in the travel plans.
catch on | The new board game caught on quickly among local students.
check in on | I checked in on my neighbor after the power outage.
come down to | The final decision came down to whether the family could afford the move.
count on | You can count on her to arrive early and prepare the room.
cut off | The storm cut off access to several mountain villages.
draw on | The novelist drew on childhood memories to create the setting.
drop by | We dropped by the bookstore on our way home.
iron out | The organizers met again to iron out the last scheduling problems.
map out | The volunteers mapped out a safer route through the forest.
fall apart | Their travel plans fell apart after the ferry was canceled.
weigh up | She weighed up the advantages and disadvantages before accepting the offer.
check up on | The landlord stopped by to check up on the repairs.
open up about | He eventually opened up about how difficult the transition had been.
fill in for | Maya filled in for the host while he was recovering from surgery.
shy away from | She never shies away from a difficult conversation.
get ahead | The interns learned practical strategies to get ahead in a competitive field.
get across | He used a simple diagram to get his point across.
hold on to | She held on to the old letters because they reminded her of home.
look out for | Look out for falling rocks along this section of the trail.
get away with | The driver didn't get away with parking in the restricted zone.
reach out to | The nonprofit reached out to local businesses for donations.
sum up | At the end, the speaker summed up the main findings in two sentences.
settle for | We didn't want to settle for a smaller apartment without a kitchen.
give in | After hours of discussion, the committee finally gave in to the pressure.
make do with | We had to make do with candles when the electricity went out.
slip up | Even experienced performers can slip up during a live show.
get through | She got through the long winter by meeting friends every weekend.
move on from | It took him several months to move on from the disappointing result.
stand up for | She stood up for her colleague when the accusation proved unfounded.
lay out | The architect laid out the design choices in a short presentation.
turn to | Many residents turned to the community center for information.
leave out | Don't leave out the final paragraph when you submit the report.
take up | She took up photography after moving closer to the coast.
come around to | He eventually came around to the idea of sharing the workspace.
look back on | They look back on their first trip together with affection.
put up with | I can't put up with that constant noise any longer.
step up | Local volunteers stepped up their efforts after the first storm.
check out | We checked out the new exhibit before heading to lunch.
turn around | The new manager helped turn around the struggling restaurant.
hold off on | They decided to hold off on buying furniture until the move was confirmed.
opt out of | Participants may opt out of the survey at any time.
come through | Her friends came through when she needed help moving.
pass up | He passed up the chance to travel because he had other commitments.
follow up on | The reporter followed up on the tip with two independent sources.
get the hang of | It took a few lessons to get the hang of the new camera.
phase out | The town plans to phase out the old buses over the next five years.
pick up on | The interviewer picked up on a hesitation in his answer.
talk into | His friends talked him into joining the weekend cycling group.
talk out of | Her parents tried to talk her out of taking the risky shortcut.
pull off | The small team pulled off a successful festival despite the rain.
walk away from | She walked away from the deal when the terms changed unexpectedly.
kick off | The celebration kicked off with a performance by the school choir.
turn in | Please turn in your application before the office closes on Friday.
hold up | Heavy traffic held up the delivery truck for nearly an hour.
'''

def parse(text):
 data={}
 for line in text.strip().splitlines():
  w,sep,example=line.partition(' | ')
  if not sep or not example or w in data:raise ValueError(f'Malformed or duplicate source row {line!r}')
  data[w]=example
 return data

def apply():
 stats={}
 for filename,source in [('vocabulary',GENERAL),('phrasals',PHRASALS)]:
  path=ROOT/'data'/f'{filename}.json'
  cards=json.loads(path.read_text(encoding='utf8'))
  lookup={x['word']:x for x in cards}
  missing=set(parse(source))-set(lookup)
  if missing:raise ValueError(f'Curated words missing from {filename}: {missing}')
  added=0
  for word,sentence in parse(source).items():
   if not sentence[0].isupper() or sentence[-1] not in '.!?':raise ValueError(word)
   card=lookup[word]
   if sentence==card['example']:raise ValueError(f'Not distinct context: {word}')
   card.setdefault('examples',[card['example']])
   if sentence not in card['examples']:
    card['examples'].append(sentence);added+=1
  path.write_text(json.dumps(cards,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
  stats[filename]={'newContextSentences':added,'newlyCoveredTerms':len(parse(source))}
 print(json.dumps(stats,ensure_ascii=False,indent=2))
 return stats

if __name__=='__main__':apply()
