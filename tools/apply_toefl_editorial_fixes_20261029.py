#!/usr/bin/env python3
"""Small, author-reviewed sense consistency corrections. Never recreates IDs."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
changes={
 'toefl-benefit':{'definition':'As a noun, a positive effect or advantage; as a verb, to help someone or something.'},
 'toefl-export':{'definition':'To sell goods or services to another country (verb), or goods and services sold abroad (noun).'},
 'toefl-finance':{'definition':'Money management or funding (noun), or to provide money for an activity (verb).'},
 'toefl-individual':{'definition':'A single person (noun), or relating to one person rather than a group (adjective).'},
 'pv-back-up':{'examples':['Can you back up that claim with evidence?', 'The professor used detailed records to back up her conclusion.']},
 'pv-take-off':{'examples':['The business took off after the interview.', 'Her podcast took off after students began sharing it online.']},
 'pv-step-up':{'syntax':'separable','note':'Can be intransitive (“volunteers stepped up”) or separable with a direct object (“step up their efforts”).'},
 'pv-make-up-for':{'examples':['We worked late to make up for lost time.', 'An extra practice session can make up for the class we missed.']},
 'pv-break-down':{'examples':['The car broke down outside the town.', 'Our printer broke down while we were preparing the report.']},
 'pv-come-up-with':{'examples':['She came up with a creative solution.', 'The research team came up with a new way to measure air quality.']},
 'pv-turn-down':{'examples':['She turned down the invitation politely.', 'The committee turned down the proposal because it lacked evidence.']},
 'pv-set-out':{'examples':['We set out before sunrise.', 'The hikers set out for the summit despite the cloudy forecast.']},
}
reference={
 'toefl-benefit':'https://dictionary.cambridge.org/dictionary/english/benefit',
 'pv-back-up':'https://dictionary.cambridge.org/dictionary/english/back-up',
 'pv-take-off':'https://dictionary.cambridge.org/dictionary/english/take-off',
 'pv-step-up':'https://dictionary.cambridge.org/dictionary/english/step-up',
}
files=['data/toefl-academic.json','data/phrasals.json']; trace=[]
for path in files:
 p=root/path; original=json.loads(p.read_text())
 for card in original:
  k=card['id']
  if k not in changes:continue
  changed=[]
  for field,val in changes[k].items():
   before=card.get(field)
   if before==val:continue
   card[field]=val
   if field=='examples':card['example']=val[0]
   changed.append({'field':field,'before':before,'after':val})
  if changed:trace.append({'id':k,'file':path,'changes':changed,'senseReference':reference.get(k),'editor':'AI-assisted targeted self-review; NOT independent human signoff'})
 p.write_text(json.dumps(original,ensure_ascii=False,indent=2)+'\n')
assert len(trace)==len(changes),len(trace)
(root/'qa/toefl-editorial-corrections-20261029.json').write_text(json.dumps({'date':'2026-10-29','approvedByHumanEditor':False,'fixCount':len(trace),'corrections':trace},ensure_ascii=False,indent=2)+'\n')
print(len(trace),'corrected cards (IDs preserved)')
