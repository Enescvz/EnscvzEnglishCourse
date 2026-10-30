#!/usr/bin/env python3
"""Bind older VOA in-app answer keys to existing publisher-script speaker turns.

Every string must match an existing turn exactly and unambiguously. This does
not verify MP3 playback or that the transcript aligns to the audio.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/authentic-listening.json'
# Order matches the ORIGINAL multiple-choice question order. IDs/options untouched.
EVIDENCE={
 'voa-level2-01-budget-cuts':[
  ('Jonathan','I have heard people in the building talking about budget cuts.'),
  ('Jonathan','Mark in Accounting.'),
  ('Anna',"We shouldn't gossip. That's how rumors start."),
  ('Kaveh','When there are budget cuts, people lose their jobs.'),
  ('Ms. Weaver','The reason for this meeting is to tell you what a good job you’ve been doing and give out new assignments.'),
 ],
 'voa-level2-02-interview':[
  ('Ms. Weaver','someone who is very "different" from you.'),
  ('Anna','My boss wants me to team up with someone to host a talk show.'),
  ('Anna','I have a job offer for you!'),
  ('Pete','sometimes I think people talk too much.'),
  ('Pete','And, I got the job!'),
  ('Ms. Weaver','I need to find out if you have the skills for this job.'),
 ],
 'voa-level2-10-peru':[
  ('Anna','I have to research Peru for a story.'),
  ('Bruna','The museum where I work is having a Peruvian festival today!'),
  ('Bruna','let’s watch the dancers.'),
  ('Anna','I’m not ready to get married.'),
  ('Anna','I’ll check out the art.'),
 ],
 'voa-linked-2-03':[
  ('Anna','meeting with a consultant who will help us with our new show.'),
  ('Kelly','exactly 43 minutes late!'),
  ('Anna',"He had to get his 'special' coffee"),
  ('Pete','a scooter would be much faster.'),
 ],
}
ADDITIONAL={
 ('voa-level2-01-budget-cuts',0):('Kaveh','When there are budget cuts, people lose their jobs.'),
 ('voa-level2-01-budget-cuts',3):('Kaveh','Update your résumé.'),
 # This question asks about two events, described by Pete in successive turns.
 ('voa-linked-2-03',3):('Pete','Then Anna stopped by a pond to feed the birds.'),
}
def run():
 lessons=json.loads(DATA.read_text(encoding='utf8'))
 for lesson_id,quotes in EVIDENCE.items():
  lesson=next(x for x in lessons if x['id']==lesson_id)
  if len(quotes)!=len(lesson['questions']):raise ValueError('Question order changed for '+lesson_id)
  for qi,(speaker,quote) in enumerate(quotes):
   hits=[(idx,t) for idx,t in enumerate(lesson['turns']) if t['speaker']==speaker and quote in t['text']]
   if len(hits)!=1:raise ValueError(f'Cannot uniquely anchor {lesson_id} question {qi}: {quote}')
   idx,t=hits[0]
   q=lesson['questions'][qi]
   q['sourceEvidence']=quote;q['sourceEvidenceTurn']=idx;q['sourceEvidenceSpeaker']=speaker
   if (lesson_id,qi) in ADDITIONAL:
    more_speaker,more_text=ADDITIONAL[lesson_id,qi]
    extra=[(k,turn) for k,turn in enumerate(lesson['turns']) if turn['speaker']==more_speaker and more_text in turn['text']]
    if len(extra)!=1:raise ValueError('Secondary answer evidence missing')
    q['sourceEvidenceAdditional']=[{'speaker':more_speaker,'turn':extra[0][0],'text':more_text}]
 DATA.write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 return {'evidencedQuestions':sum('sourceEvidenceTurn' in q for l in lessons for q in l['questions']),'questionCount':sum(len(l['questions']) for l in lessons)}
if __name__=='__main__':print(json.dumps(run(),indent=2))
