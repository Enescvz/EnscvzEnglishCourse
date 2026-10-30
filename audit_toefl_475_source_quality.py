#!/usr/bin/env python3
"""Reproducible *limited* evidence cross-check. Not a human editorial signoff.
Reference headwords transcribed from the cited public AWL sublists 1-3 and
PHaVE frequency-ranked appendix; labels are membership only, not ETS ranks.
"""
import json,csv,re,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AWL = {
1: '''analyse approach area assess assume authority available benefit concept consist constitute context contract create data define derive distribute economy environment establish estimate evident export factor finance formula function identify income indicate individual interpret involve issue labour legal legislate major method occur percent period policy principle proceed process require research respond role section sector significant similar source specific structure theory vary'''.split(),
2: '''achieve acquire administrate affect appropriate aspect assist category chapter commission community complex compute conclude conduct consequent construct consume credit culture design distinct element equate evaluate feature final focus impact injure institute invest item journal maintain normal obtain participate perceive positive potential previous primary purchase range region regulate relevant reside resource restrict secure seek select site strategy survey text tradition transfer'''.split(),
3: '''alternative circumstance comment compensate component consent considerable constant constrain contribute convene coordinate core corporate correspond criteria deduce demonstrate document dominate emphasis ensure exclude framework fund illustrate immigrate imply initial instance interact justify layer link locate maximise minor negate outcome partner philosophy physical proportion publish react register rely remove scheme sequence sex shift specify sufficient task technical technique technology valid volume'''.split(),
4: '''access adequate annual apparent approximate attitude attribute civil code commit communicate concentrate confer contrast cycle debate despite dimension domestic emerge error ethnic goal grant hence hypothesis implement implicate impose integrate internal investigate job label mechanism obvious occupy option output overall parallel parameter phase predict principal prior professional project promote regime resolve retain series statistic status stress subsequent sum summary undertake'''.split(),
5: '''academy adjust alter amend aware capacity challenge clause compound conflict consult contact decline discrete draft enable energy enforce entity equivalent evolve expand expose external facilitate fundamental generate generation image liberal licence logic margin medical mental modify monitor network notion objective orient perspective precise prime psychology pursue ratio reject revenue stable style substitute sustain symbol target transit trend version welfare whereas'''.split(),
6: '''abstract accurate acknowledge aggregate allocate assign attach author bond brief capable cite cooperate discriminate display diverse domain edit enhance estate exceed expert explicit federal fee flexible furthermore gender ignorant incentive incidence incorporate index inhibit initiate input instruct intelligent interval lecture migrate minimum ministry motive neutral nevertheless overseas precede presume rational recover reveal scope subsidy tape trace transform transport underlie utilise'''.split(),
7: '''adapt adult advocate aid channel chemical classic comprehensive comprise confirm contrary convert couple decade definite deny differentiate dispose dynamic eliminate empirical equip extract file finite foundation globe grade guarantee hierarchy identical ideology infer innovate insert intervene isolate media mode paradigm phenomenon priority prohibit publication quote release reverse simulate sole somewhat submit successor survive thesis topic transmit ultimate unique visible voluntary'''.split(),
8: '''abandon accompany accumulate ambiguous append appreciate arbitrary automate bias chart clarify commodity complement conform contemporary contradict crucial currency denote detect deviate displace drama eventual exhibit exploit fluctuate guideline highlight implicit induce inevitable infrastructure inspect intense manipulate minimise nuclear offset paragraph plus practitioner predominant prospect radical random reinforce restore revise schedule tense terminate theme thereby uniform vehicle via virtual visual widespread'''.split(),
9: '''accommodate analogy anticipate assure attain behalf bulk cease coherent coincide commence compatible concurrent confine controversy converse device devote diminish distort duration erode ethic format found inherent insight integral intermediate manual mature mediate medium military minimal mutual norm overlap passive portion preliminary protocol qualitative refine relax restrain revolution rigid route scenario sphere subordinate supplement suspend team temporary trigger unify violate vision'''.split(),
10: '''adjacent albeit assemble collapse colleague compile conceive convince depress encounter enormous forthcoming incline integrity intrinsic invoke levy likewise nonetheless notwithstanding odd ongoing panel persist pose reluctance so-called straightforward undergo whereby'''.split(),
}
# PHaVE 2015 ranked list (Appendix 2) retrieved via UC Davis reference.
PHAVE = '''
go on|pick up|come back|come up|go back|find out|come out|go out|point out|grow up|set up|turn out|get out|come in|take on|give up|make up|end up|get back|look up|figure out|sit down|get up|take out|come on|go down|show up|take off|work out|stand up|come down|go ahead|go up|look back|wake up|carry out|take over|hold up|pull out|turn around|take up|look down|put up|bring back|bring up|look out|bring in|open up|check out|move on|put out|look around|catch up|go in|break down|get off|keep up|put down|reach out|go off|cut off|turn back|pull up|set out|clean up|shut down|turn over|slow down|wind up|turn up|line up|take back|lay out|go over|hang up|go through|hold on|pay off|hold out|break up|bring out|pull back|hang on|build up|throw out|hang out|put on|get down|come over|move in|start out|call out|sit up|turn down|back up|put back|send out|get in|blow up|carry on|set off|keep on|run out|make out|shut up|turn off|bring about|step back|lay down|bring down|stand out|come along|play out|break out|go around|walk out|get through|hold back|write down|move back|fill out|sit back|rule out|move up|pick out|take down|get on|give back|hand over|sum up|move out|come off|pass on|take in|set down|sort out|follow up|come through|settle down|come around|fill in|give out|give in|go along|break off|put off|come about|close down|put in|set about
'''.strip().split('|')
assert [len(AWL[k]) for k in range(1,11)] == [60]*9+[30], [len(AWL[k]) for k in range(1,11)]
assert len(PHAVE)==150
normalize=lambda x:re.sub(r'\s+',' ',x.casefold().strip()).replace('analyse','analyze').replace('labour','labor').replace('maximise','maximize')
awl={normalize(w):k for k,ws in AWL.items() for w in ws}
phave={normalize(p):i+1 for i,p in enumerate(PHAVE)}
assert len(awl)==570 and len(phave)==150
j=lambda file:json.loads((ROOT/file).read_text())
core=j('data/toefl-core.json'); vocab={x['id']:x for x in j('data/vocabulary.json')+j('data/toefl-academic.json')}; phrasal={x['id']:x for x in j('data/phrasals.json')}
def contains_headword(term, sentence):
  # Cheap morphology heuristic, NOT an English lemmatizer or semantic validator.
  if term in ('undertake','shrink','trade-off'):
    irregular={'undertake':('undertake','undertakes','undertook','undertaken','undertaking'),
               'shrink':('shrink','shrinks','shrank','shrunk','shrinking'),
               'trade-off':('trade-off','trade-offs')}[term]
    return any(re.search(r'(?<![a-z-])'+re.escape(f)+r'(?![a-z-])',sentence.casefold()) for f in irregular)
  forms={term,term+'s',term+'es',term+'ed',term+'d',term+'ing'}
  if term.endswith('e'):forms.add(term[:-1]+'ing')
  if term.endswith('y'):forms|={term[:-1]+'ies',term[:-1]+'ied'}
  if term.endswith('c'):forms.add(term+'ked')
  if len(term)>2:forms|={term+term[-1]+'ed',term+term[-1]+'ing'}
  return any(re.search(r'(?<![a-z])'+re.escape(f)+r'(?![a-z])',sentence.casefold()) for f in forms)
rows=[]; flags=[]
for typ,ids,idx in (('word',core['wordLessonIds'],vocab),('phrasal',core['phrasalLessonIds'],phrasal)):
 for id in ids:
  card=idx[id]; term=normalize(card['word']); examples=card.get('examples',[])
  if typ=='word':
   matched=awl.get(term); source_type='AWL_headword_match' if matched else 'AWL_headword_not_matched_related_forms_unchecked'; rank=None
  else:
   rank=phave.get(term);matched=None;source_type='PHaVE_top_150' if rank else 'not_in_PHaVE_top_150'
  problem=[]
  if len(examples)!=2 or any(not isinstance(e,str) or len(e.strip())<15 for e in examples):problem.append('missing_or_short_example')
  if len(examples)==2 and examples[0].strip().casefold()==examples[1].strip().casefold():problem.append('duplicated_examples')
  for field in ('tr','definition'):
   if not card.get(field): problem.append('missing_'+field)
  # Stemming fails for irregular forms; those are review flags, never automatic errors.
  if typ=='word':
   for n,e in enumerate(examples):
    if not contains_headword(term,e):problem.append(f'headword_not_detected_example_{n+1}')
  if typ=='phrasal' and card.get('syntax') not in ('separable','inseparable','intransitive'):problem.append('syntax_enum_unrecognized')
  if problem:flags.append({'id':id,'flags':problem})
  rows.append({'id':id,'type':typ,'headword':card['word'],'sourceMatch':source_type,'awlSublist':matched,'phaveCorpusRank':rank,'examples':len(examples),'automatedEditorialFlags':problem,'externalEditorApproval':False,'TOEFLExamFrequencyKnown':False})
assert len(rows)==475
counter=collections.Counter(r['sourceMatch'] for r in rows)
report={'reportDate':'2026-10-29','type':'bounded_frequency_crosscheck_and_automated_editorial_audit','summary':{'cardsChecked':len(rows),'words':400,'phrasals':75,'referenceMembershipCounts':dict(counter),'flaggedCards':len(flags),'humanEditorApproved':0,'ETSExamFrequencyRanked':0},
 'methodology':{'AWL':'Coxhead Academic Word List; all 570 published headwords from sublists 1–10 crosschecked (direct headword only), NOT an ETS test frequency list.',
                'PHaVE':'Garnier and Schmitt COCA-based 150 phrasal verb frequency rank; rank is for expression, not the teaching sense and NOT ETS.',
                'automatedQuality':'ID/schema, two examples, definition and Turkish gloss presence, rough morphology; lexical meaning, register, translation and collocation need expert human signoff.',
                'noFalseNegative':'No direct AWL headword match does not exclude membership via a related family form or relevance to everyday and academic English. Not in PHaVE top-150 does NOT mean infrequent in TOEFL.'},
 'references':[{'url':'https://www.eapfoundation.com/vocab/academic/awllists/index.php','scope':'AWL full 570 published headwords' },{'url':'https://globalaffairs.ucdavis.edu/iae/graduate/language-tips/high-frequency-phrasal-verbs','scope':'PHaVE-ranked appendix'},{'url':'https://afa4be34-0fda-46d9-8e64-5adf13d4216b.filesusr.com/ugd/5f2482_dd3f49d53f484b33b904bf7606641e1b.pdf','scope':'PHaVE ranks 1–150'}],
 'rows':rows,'flags':flags,'officialTOEFLFrequencyClaim':False,'independentEditorialSignoff':False,'releaseReady':False}
(ROOT/'qa/toefl-475-frequency-and-editorial-audit-20261029.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
with (ROOT/'qa/toefl-475-frequency-and-editorial-audit-20261029.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=('id','type','headword','sourceMatch','awlSublist','phaveCorpusRank','examples','externalEditorApproval','TOEFLExamFrequencyKnown','automatedEditorialFlags'))
 w.writeheader()
 for r in rows:w.writerow({**r,'automatedEditorialFlags':';'.join(r['automatedEditorialFlags'])})
print(json.dumps({'counts':report['summary'],'flags':flags},ensure_ascii=False,indent=2))
