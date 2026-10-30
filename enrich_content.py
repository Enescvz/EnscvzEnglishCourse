"""Hand-reviewed supplement of multiple phrasal senses and passage-specific questions."""
from pathlib import Path
import json
D=Path(__file__).resolve().parents[1]
p=D/'data'/'phrasals.json';d=json.loads(p.read_text())
extra={
 'take off':[('uçak havalanmak','The plane took off twenty minutes late.'),('kıyafeti çıkarmak','Please take off your shoes before entering.')],
 'break down':[('duygusal olarak çökmek','She broke down in tears after hearing the news.'),('parçalara ayırarak açıklamak','Could you break down the total cost for me?')],
 'work out':[('egzersiz yapmak','She works out three times a week.'),('iyi sonuçlanmak','I hope everything works out for you.')],
 'bring up':[('çocuk yetiştirmek','He was brought up in a small town.')],
 'back up':[('verileri yedeklemek','Remember to back up your photos regularly.')],
 'cut off':[('birinin sözünü kesmek','I am sorry to cut you off, but we are out of time.')],
 'get over':[('engeli aşmak','It is difficult to get over a high fence.')],
 'pay off':[('borcu tamamen ödemek','She finally paid off her student loan.')],
 'put off':[('birinden soğutmak','The rude comment put me off the restaurant.')],
 'take on':[('yeni çalışan almak','The company plans to take on two new employees.')],
 'turn down':[('sesi kısmak','Could you turn down the music?')],
 'set aside':[('bir kenara koymak','Set aside those papers until tomorrow.')],
 'look into':[('yakından incelemek','An independent team will look into the problem.')],
 'come across':[('izlenim vermek','He came across as thoughtful and patient.')],
 'give up':[('bir şeyi bırakmak','She gave up coffee for a month.')],
}
for v in d:
 v['senses']=[{'tr':v['tr'],'example':v['example']}]+[{'tr':a,'example':b} for a,b in extra.get(v['word'],[])]
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))

# Two additional DIFFERENT passage-specific questions for each reading.
# Every key is checked against the corresponding original text.
extra_reading=[
 [('What did the museum website offer?',['A digital copy of the photograph','A replacement train ticket','A new suitcase','A hotel reservation'],0,'Nora suggested looking for a digital copy of the photo on the museum website.'),('What did the caption do?',['It raised further questions','It confirmed every detail','It identified Nora as the sailor','It announced the museum had moved'],0,'The caption raised more questions than it answered.')],
 [('Which condition involved notifications?',['The second reading routine','The first reading routine','Both routines required music','Neither routine included phones'],0,'Participants kept phones nearby with notifications enabled in the second routine.'),('Why did some volunteers silence notifications afterward?',['They personally preferred fewer distractions','The event conclusively proved a scientific theory','The center required them to','The reading passages were identical'],0,'They made an individual choice; the informal comparison was not a controlled study.')],
 [('How did volunteers answer concerns about maintenance?',['With a budget and rotating schedule','By hiring a permanent chef','By closing the courtyard','By canceling the garden'],0,'The volunteers made a modest budget and shared a rotating maintenance schedule.'),('What does the story say about food production?',['It produces a limited amount of food','It feeds every resident in the district','It exports all its vegetables','It stopped producing food years ago'],0,'The text explicitly calls the quantity of food produced limited.')],
 [('Why can profitability be insufficient for survival?',['Bills may be due before enough cash arrives','Profit always equals cash in the bank','A profitable shop cannot have debts','Rent can never change'],0,'The owner considers liquidity because cash outflows and inflows occur at different times.'),('What is the main advantage of weekend test events?',['Gathering evidence without a long commitment','Making expansion legally mandatory','Avoiding all business expenses','Guaranteeing future revenue'],0,'Temporary events test demand without an irreversible lease.')],
 [('Why may the same melody affect people differently?',['Associations and experiences differ','All people hear identical memories','Music has no emotional associations','Every melody has one fixed meaning'],0,'The passage attributes different responses partly to personal associations.'),('What was the facilitator’s attitude to varied responses?',['Neither response was wrong','Only detailed memories were acceptable','Everyone had to identify a song','No written reflections were permitted'],0,'The facilitator expressly said that neither response was wrong.')],
 [('What advantage of remote work was mentioned?',['Less commuting and greater flexibility','Guaranteed increases in salary','Fewer written documents','No need for any collaboration'],0,'One owner mentioned reduced commuting and flexible personal responsibilities.'),('What advantage of working face-to-face was mentioned?',['Spontaneous interaction and mentoring','The elimination of meetings','No commute for employees','Automatic higher productivity'],0,'The other owner emphasized unplanned conversations and face-to-face mentoring.')],
 [('How was the discrepancy discovered?',['During an online collection project','While building a train station','By a visitor comparing paintings','Through a new security camera'],0,'Curators noticed the label mismatch while preparing the online collection.'),('How did many visitors respond to the correction?',['Positively, because it explained changing knowledge','They demanded the exhibition close','They all stopped visiting museums','They concluded the artifact was fake'],0,'Several visitors appreciated the public explanation of how evidence is reviewed.')],
 [('Why were some residents skeptical?',['Benefits would be hard to observe on ordinary days','Engineers denied the storms happened','Drainage projects were completed already','The proposal excluded all neighborhoods'],0,'The proposed risk reduction is less obvious outside severe weather.'),('How did officials address uncertainty?',['By presenting scenarios and acknowledging limits','By promising zero future floods','By refusing public discussion','By publishing only one prediction'],0,'Officials presented scenarios and noted uncertainty instead of guaranteeing outcomes.')]
]
rp=D/'data'/'readings.json';rs=json.loads(rp.read_text())
for i,r in enumerate(rs):
 r['questions']=r['questions'][:3]+[
  {'question':q,'options':choices,'answer':correct,'explanation':expl}
  for q,choices,correct,expl in extra_reading[i]]
rp.write_text(json.dumps(rs,ensure_ascii=False,indent=2))
print('Enriched',len(d),'phrasals and',len(rs),'reading lessons')

# Editorial prioritization of common conversational phrasal verbs.
frequent=['figure out','come across','come up with','deal with','get over','get by','give up','bring up','point out','look into','turn down','put off','work out','take on','carry out','make up for','set aside','follow through on','keep up with','catch up on','run into','end up','break down','back up','fall behind','cut back on','stick to','speak up','pay off','go over','get around to','break out','take off','hold back','narrow down','rule out','call off','step down','look up to','bring about']
rank={w:i for i,w in enumerate(frequent)}
for v in d:v['priority']=rank.get(v['word'],100+v['priority'])
d.sort(key=lambda x:(x['priority'],x['word']))
p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
