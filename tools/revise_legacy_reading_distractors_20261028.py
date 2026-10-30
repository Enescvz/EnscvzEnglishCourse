#!/usr/bin/env python3
"""Replace weak filler distractors in original eight readings; preserve IDs and answers."""
import json
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'data/readings.json'
# Correct answer remains at index zero for these legacy questions.
DIST={
 'the-midnight-train':[
 ['She was collecting a repaired suitcase','She was working at the ticket window','She had arranged to tour the museum'],
 ['To attend a concert nearby','To meet a former colleague','To photograph the train station'] ],
 'the-attention-experiment':[
 ['Whether music helped readers remember more','How room temperature affected sleep','Why volunteers preferred digital magazines'],
 ['Every participant had already read the passage','Scores were identical in both routines','The session included a randomly assigned control group'] ],
 'a-hidden-garden':[
 ['The building was about to be demolished','The courtyard was too sunny for vegetables','Residents wanted the garden to charge admission'],
 ['Lower apartment rents for residents','A year-round source of all household food','A reduction in the building’s electricity use'] ],
 'a-calculated-risk':[
 ['A shortage of books at the original shop','A temporary sign outside the store','A delay in scheduling a weekend event'],
 ['Signing a second long-term lease immediately','Stopping sales at the original store','Opening a branch without testing demand'] ],
 'the-memory-of-a-song':[
 ['That instrumental music can prompt reflection','That people associate songs with experiences','That a workshop can invite personal memories'],
 ['Formal clinical diagnosis of memory problems','Comparing hearing ability with age','Testing whether everyone knew the same tune'] ],
 'a-debate-about-remote-work':[
 ['That every job benefits equally from remote work','That all team meetings should be canceled','That productivity can never be evaluated'],
 ['Personal preferences without any evidence','A fixed rule that applies to every company','Assumptions about productivity without measurement'] ],
 'the-museum-label':[
 ['It gave the wrong name for the donor','It described a replica as authentic','It listed the artifact under the wrong city'],
 ['To avoid publishing the online collection','To remove the artifact from display permanently','To persuade visitors the mistake had never happened'] ],
 'a-more-resilient-city':[
 ['Building only a single sea wall','Replacing all green spaces with concrete','Moving every resident out of the city'],
 ['Every neighborhood had received equal funding','The proposed works would be finished immediately','The city already had a zero-flood guarantee'] ]
}
rows=json.loads(p.read_text()); changed=0
for lesson in rows:
 if lesson['id'] not in DIST: continue
 for idx,repl in enumerate(DIST[lesson['id']]):
  q=lesson['questions'][idx]
  assert 0 <= q['answer'] < len(q['options'])
  old=q['options']
  if old[-1]=='A completely unrelated technical requirement':
   correct=old[q['answer']]
   q['options']=[correct]+repl
   q['answer']=0
   changed+=1
  else:
   assert set(o for j,o in enumerate(q['options']) if j!=q['answer'])==set(repl), lesson['id']
p.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'legacyQuestionsImprovedThisRun':changed,'legacyQuestionsWithoutGenericDistractors':16}))
