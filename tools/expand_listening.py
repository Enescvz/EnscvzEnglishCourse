#!/usr/bin/env python3
"""Produce six distinct authored podcast conversations and twelve listening drills.
All local audio is synthetic en-US espeak. No imported or claimed human recordings.
Re-runnable, append-only, preserve prior IDs; content stays authored_unreviewed.
"""
import json,subprocess,tempfile,os,wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AUDIO=ROOT/'assets'/'audio'
# Each script is an original two-speaker dialogue; questions refer to its precise claims.
EPISODES=[
 dict(id='mountain-trail',title='The Trail That Changed Overnight',level='B2',category='Travel & Nature',focus=5,turns=[
 'I saw a notice about the Ridge Trail. Apparently, the main route is closed this weekend.',
 'Is it because of the storm? We were planning to hike there on Saturday.',
 'Partly. The storm damaged a bridge, and volunteers found a second problem near the waterfall.',
 'What kind of problem? I assumed the entire trail was safe once the bridge was repaired.',
 'The slope is unstable. The park wants to assess the risk before allowing people through.',
 'So we should rule out the waterfall route, even if the weather looks perfect.',
 'Exactly. There is an alternate path, but it adds about two miles and has very little shade.',
 'Then we should bring extra water. Can we still reach the lake before sunset?',
 'Yes, if we start early. I checked the official map and downloaded it for offline use.',
 'Good idea. A map on your phone is helpful, but a printed backup could be crucial.'
 ],questions=[
 ('Why is the waterfall route restricted?',['The lake has disappeared','The hillside may be unstable','The parking lot is full','The trail has no signs'],1,'The speakers say the slope near the waterfall is unstable, so the park must assess the risk.'),
 ('How is the alternate path different?',['It is about two miles longer','It passes through a museum','It requires a boat','It is completely shaded'],0,'The alternate route adds roughly two miles and offers little shade.'),
 ('What preparation do they agree on?',['Hiking after sunset','Ignoring the map','Starting early and taking extra water','Crossing the damaged bridge'],2,'They plan an early start and extra water, while relying on official route information.')]),
 dict(id='museum-origin',title='Who Owns the Story?',level='C1',category='History & Ethics',focus=7,turns=[
 'Did you read about the museum returning an ancient sculpture to the community where it was found?',
 'Yes. The decision sparked a debate about who should preserve historical objects.',
 'Some visitors argued that the museum had protected the sculpture for generations.',
 'Others pointed out that the community never consented to its removal in the first place.',
 'I think those are distinct questions: who can preserve it, and who has the right to decide?',
 'Exactly. Preserving an object does not automatically justify keeping it.',
 'The museum plans to collaborate with local historians on a traveling exhibition.',
 'That approach may help reconcile competing priorities without pretending the history was simple.',
 'The museum also published the documents behind its decision. That seems important for transparency.',
 'And the community will help write the exhibition labels, so its perspective is represented.'
 ],questions=[
 ('What ethical issue do the speakers emphasize?',['Ticket prices','Rights and consent surrounding an artifact','The sculpture’s weight','Modern architecture'],1,'They distinguish the right to decide about an object from the ability to preserve it.'),
 ('What collaborative solution is proposed?',['Destroying the exhibition','Hiding the records','A traveling exhibition with local historians','Selling tickets abroad'],2,'The speakers mention a traveling exhibition developed together with local historians.'),
 ('Why will the community contribute to the labels?',['To represent its perspective','To shorten every description','To advertise a new store','To avoid publishing documents'],0,'Community members will help write the labels so their interpretation is included.')]),
 dict(id='food-rescue',title='The Rescue Fridge on Elm Street',level='B2',category='Community & Food',focus=4,turns=[
 'A new community refrigerator opened near my apartment yesterday.',
 'Is that the project where restaurants donate food they cannot sell?',
 'Yes, but they have strict safety rules. Volunteers label each item with a date and storage instructions.',
 'That sounds sensible. How do they prevent donated food from going to waste again?',
 'They track which items disappear quickly and adjust collection schedules accordingly.',
 'So the goal is not simply to fill the fridge; it is to match donations with actual demand.',
 'Right. One bakery now delivers bread after lunch instead of late at night.',
 'Do residents have to provide proof that they need the food?',
 'No. Anyone can take a reasonable amount, and signs emphasize respect and privacy.',
 'I appreciate that. The organizers seem to be learning from evidence rather than assumptions.'
 ],questions=[
 ('What information is attached to donated food?',['The name of a sponsor','Dates and storage guidance','A restaurant rating','A suggested retail price'],1,'Volunteers mark items with dates and instructions for storing them safely.'),
 ('Why did one bakery change its delivery time?',['To avoid the lunch rush','To reduce its rent','To match food donations with demand','To stop baking bread'],2,'The schedule was adjusted because the organizers track when items are actually taken.'),
 ('Who can use the refrigerator?',['Only restaurant employees','Only people with paperwork','Only volunteers','Anyone taking a reasonable amount'],3,'The speakers explicitly say no proof of need is required.')]),
 dict(id='missing-suitcase',title='The Case of the Wandering Suitcase',level='B2',category='Travel & Mystery',focus=6,turns=[
 'My suitcase landed in Denver while I landed in Portland. I did not expect that.',
 'That is frustrating. Did the airline give you a tracking number?',
 'Yes. They said my bag was placed on the wrong connecting flight.',
 'At least they identified the problem. Do you know when it will arrive?',
 'They estimate tomorrow morning, but they stressed that the time is not guaranteed.',
 'Have you kept the receipts for the toiletries you had to buy?',
 'I did. I also took screenshots of the baggage report so I can follow up on the claim.',
 'That was smart. It is easier to resolve a dispute when you have a written record.',
 'My plan is to check the tracking page this evening instead of calling every hour.',
 'Good. And keep your medication in your carry-on next time, just in case.'
 ],questions=[
 ('How did the suitcase get misplaced?',['It was sent on the wrong connecting flight','It was left in a taxi','It was stolen at the hotel','It was shipped by train'],0,'The airline says the suitcase was loaded onto an incorrect connecting flight.'),
 ('What does the airline say about the delivery time?',['Delivery is canceled','It is absolutely guaranteed','It is an estimate, not a guarantee','It will take a month'],2,'Tomorrow morning is described as an estimate, with uncertainty remaining.'),
 ('Why were receipts and screenshots saved?',['To share them on social media','To document a possible baggage claim','To change the flight destination','To print luggage tags'],1,'The traveler saves records to follow up on the reimbursement or baggage claim.')]),
 dict(id='financial-forecast',title='A Forecast Is Not a Promise',level='C1',category='Accounting & Finance',focus=5,turns=[
 'Our neighborhood theater is considering a second location, but the financial forecast looks unusually optimistic.',
 'Does it assume ticket sales will increase every month without any setbacks?',
 'Almost. The model projects steady growth and leaves out several maintenance expenses.',
 'That could distort the cash flow forecast. Profit and available cash are not interchangeable.',
 'Exactly. The theater might report a profit and still struggle to pay rent on time.',
 'I would run three scenarios rather than rely on a single projection.',
 'An optimistic case, a base case, and a cautious case?',
 'Yes. And I would disclose the assumptions behind each case so the board can evaluate the uncertainty.',
 'We should also consider liquidity. A delay in ticket revenue could create a short-term problem.',
 'Then our recommendation should be to test demand with temporary events before signing a long lease.'
 ],questions=[
 ('What is missing from the optimistic forecast?',['Some maintenance costs','The name of the theater','The location of the audience','The theater’s opening year'],0,'The model omits some maintenance expenses while assuming steady growth.'),
 ('Why does the conversation distinguish profit from cash?',['Profit is always higher','Profitable organizations may still lack cash when bills are due','Cash cannot be forecast','Rent is never paid in cash'],1,'A theater may be profitable on paper but temporarily unable to cover near-term obligations.'),
 ('What is their proposed next step?',['Immediately sign a long lease','Abandon the existing theater','Test demand with temporary events','Raise every ticket price'],2,'They recommend short trial events to gather evidence before a long commitment.')]),
 dict(id='ocean-mapping',title='The Map Beneath the Waves',level='C1',category='Science & Discovery',focus=7,turns=[
 'I watched a documentary about researchers mapping the seafloor with sound waves.',
 'I assumed they used cameras. How can sound reveal the shape of something underwater?',
 'The instrument sends out a pulse, then measures how long the echo takes to return.',
 'So the return time helps them estimate the distance to the surface below?',
 'Exactly. Multiple measurements can create a detailed map, although the results depend on calibration.',
 'But a strange shape on a map does not necessarily mean they found a shipwreck.',
 'Right. It could be a rock formation or an error in the measurements.',
 'That distinction is crucial. Interesting patterns deserve investigation, not immediate conclusions.',
 'The team plans to send a remotely operated vehicle to examine one unusual area.',
 'Then a photograph might confirm the map, or it might reveal a completely ordinary feature.'
 ],questions=[
 ('How is the underwater map produced?',['By measuring echoes of emitted sound pulses','By interviewing fishermen','By studying satellite photographs only','By placing mirrors on the ocean floor'],0,'The device sends sound pulses and measures the time needed for echoes to return.'),
 ('Why does a strange shape not prove a shipwreck exists?',['All shipwrecks float','The sonar cannot detect rocks','It could be geology or a measurement error','The researchers already found treasure'],2,'They explicitly note that a shape could come from rock or inaccurate measurements.'),
 ('What will help investigate the unusual area?',['A weather balloon','A remotely operated underwater vehicle','A new ticketing system','A public opinion survey'],1,'The team intends to inspect the area with a remotely operated vehicle.')])
]
DRILLS=[
 ('inference-contrast-3','The exception matters','C1','Inference','The report was thorough, yet it overlooked one crucial assumption.','The contrast word yet shifts the conclusion; note which part of the review was incomplete.'),
 ('inference-uncertainty-4','An estimate is not a promise','B2','Inference','The package should arrive by Thursday, although the delivery date is not guaranteed.','Should and not guaranteed express uncertainty rather than a firm promise.'),
 ('numbers-price-3','Price and cents','B2','Numbers & details','The replacement part costs one hundred forty three dollars and sixty five cents.','Listen for the difference between dollar amounts and cents.'),
 ('numbers-flight-4','A gate change','B2','Numbers & details','Flight two hundred eighteen now departs from gate thirty four at nine twenty five.','Record the flight number, the gate number, and the time separately.'),
 ('connected-elision-7','Missing consonants','B2','Connected speech','We asked the staff to check the last train before we left.','Notice how word boundaries can be harder to hear when neighboring consonants meet.'),
 ('connected-linking-8','Linking across words','B2','Connected speech','She came across an old article about the abandoned train station.','Listen for across an: a consonant links to the following unstressed vowel.'),
 ('connected-pronouns-9','Weak forms in a request','B2','Connected speech','Could you send her a copy of the final report before lunch?','Unstressed pronouns and function words may be reduced in casual American speech.'),
 ('connected-contractions-10','Negative contraction','B2','Connected speech',"I wouldn't rule out a second explanation until we review the evidence.",'A negative contraction changes the meaning; do not confuse would with would not.'),
 ('speed-alternative-3','Two valid options','C1','Details & inference','We can either postpone the launch or reduce the scope, but we cannot do both.','Pay attention to either, or, and cannot do both.'),
 ('speed-sequence-4','Order of events','B2','Sentence decoding','After the meeting, she went back to the office and followed up on the complaint.','The sequence markers after and and identify the order of events.'),
 ('detail-comparison-5','Compare two numbers','C1','Numbers & details','The first estimate was eighteen percent, whereas the final figure was thirteen percent.','Write both percentages in the order spoken; whereas marks a contrast.'),
 ('detail-condition-6','A conditional plan','C1','Inference','Unless the weather improves by Friday, the outdoor event will be called off.','Unless introduces a condition; identify what must change to avoid cancellation.')
]

def get_wav(text,speaker='Alex',speed=146):
 with tempfile.NamedTemporaryFile(suffix='.wav',delete=False) as temp: path=temp.name
 try:
  voice='en-us+f3' if speaker=='Maya' else 'en-us'
  subprocess.run(['espeak','-v',voice,'-s',str(speed),'-w',path,text],check=True,stderr=subprocess.PIPE)
  with wave.open(path,'rb') as wav:return wav.getparams(),wav.readframes(wav.getnframes())
 finally:os.unlink(path)

def encode_mp3(out,turns,speed=146):
 buffer=bytearray();timeline=[];params=None
 for speaker,text in turns:
  p,data=get_wav(text,speaker,speed)
  if params is None:params=p
  if (p.framerate,p.sampwidth,p.nchannels)!=(params.framerate,params.sampwidth,params.nchannels):raise ValueError('Audio format mismatch')
  unit=p.framerate*p.sampwidth*p.nchannels
  start=len(buffer)/unit;buffer.extend(data);end=len(buffer)/unit
  timeline.append({'start':round(start,2),'end':round(end,2)})
  buffer.extend(bytes(round(p.framerate*.22)*p.sampwidth*p.nchannels))
 with tempfile.NamedTemporaryFile(suffix='.wav',delete=False) as temp:path=temp.name
 try:
  with wave.open(path,'wb') as wav:
   wav.setnchannels(params.nchannels);wav.setsampwidth(params.sampwidth);wav.setframerate(params.framerate);wav.writeframes(buffer)
  subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',path,'-codec:a','libmp3lame','-q:a','7',str(out)],check=True)
 finally:os.unlink(path)
 return timeline

def main():
 raise RuntimeError('Robotic eSpeak podcast and drill generation is prohibited. Source scripts remain archived; use licensed human voice only.')
 AUDIO.mkdir(exist_ok=True,parents=True)
 ep_file=ROOT/'data/episodes.json';ep=json.loads(ep_file.read_text(encoding='utf8'))
 dr_file=ROOT/'data/drills.json';dr=json.loads(dr_file.read_text(encoding='utf8'))
 existing_ep={v['id'] for v in ep};existing_dr={v['id'] for v in dr}
 count_ep=0;count_dr=0
 for item in EPISODES:
  if item['id'] in existing_ep:continue
  turns=[{'speaker':'Maya' if i%2==0 else 'Alex','text':line} for i,line in enumerate(item['turns'])]
  focus=item['turns'][item['focus']]
  questions=[{'question':q,'options':opts,'answer':idx,'explanation':reason,'optionExplanations':[reason if k==idx else 'Bu seçenek konuşmadaki bilgiyle desteklenmiyor.' for k in range(4)]} for q,opts,idx,reason in item['questions']]
  output=AUDIO/f"episode-{item['id']}.mp3"
  timings=encode_mp3(output,[(t['speaker'],t['text']) for t in turns])
  ep.append({'id':item['id'],'title':item['title'],'level':item['level'],'category':item['category'],'source':'Original script · locally synthesized en-US speech (eSpeak)','audioType':'synthetic','editorialStatus':'authored_unreviewed','turns':turns,'questions':questions,'focus':focus,'minutes':max(1,round(timings[-1]['end']/60,1)),'audio':f'assets/audio/{output.name}','timings':timings})
  count_ep+=1
 for slug,title,level,category,text,tip in DRILLS:
  if slug in existing_dr:continue
  output=AUDIO/f'drill-{slug}.mp3';timings=encode_mp3(output,[('Alex',text)],speed=166)
  dr.append({'id':slug,'title':title,'level':level,'category':category,'text':text,'tip':tip,'audioType':'synthetic','editorialStatus':'authored_unreviewed','audio':f'assets/audio/{output.name}','timings':timings})
  count_dr+=1
 ep_file.write_text(json.dumps(ep,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 dr_file.write_text(json.dumps(dr,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 print(json.dumps({'addedPodcastEpisodes':count_ep,'addedListeningDrills':count_dr,'totalPodcastEpisodes':len(ep),'totalListeningDrills':len(dr)},ensure_ascii=False))

if __name__=='__main__':main()
