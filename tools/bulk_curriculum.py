#!/usr/bin/env python3
"""Build a LICENSED, DEDUPLICATED B2/C1 candidate queue without faking quality review.

Usage:
  python tools/bulk_curriculum.py --download --allow-network
  python tools/bulk_curriculum.py --cefr-b2 sources/B2.json --cefr-c1 sources/C1.json \
     --bloom-words sources/words.jsonl --bloom-meanings sources/meanings.jsonl \
     --bloom-phrasals sources/phrasal-verbs.jsonl

Output: qa/candidate-vocabulary.json, qa/candidate-phrasals.json, qa/bulk-import-report.json.
Never overwrites the reviewed/live data/*.json. Does not award mastering a candidate.
BLOOM data is AI-generated and unreviewed: all imported English examples and senses
are quarantined for editorial validation. Level labels are *candidate*, not certified.
"""
import argparse, hashlib, json, re, unicodedata, urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / 'sources'
QA = ROOT / 'qa'

SOURCES = {
 'cefr-b2': ('https://raw.githubusercontent.com/recepyagmur/EnglishPractice/main/app/content/vocab/B2.json', 'B2.json'),
 'cefr-c1': ('https://raw.githubusercontent.com/recepyagmur/EnglishPractice/main/app/content/vocab/C1.json', 'C1.json'),
 'frequency': ('https://raw.githubusercontent.com/recepyagmur/EnglishPractice/main/app/content/vocab/top3000.json', 'frequency-top3000.json'),
 'bloom-words': ('https://huggingface.co/datasets/Fristail27/vocab-bloom-hub-en/resolve/v0.2.0/data/vocab-bloom-hub-en-words.jsonl', 'bloom-words.jsonl'),
 'bloom-meanings': ('https://huggingface.co/datasets/Fristail27/vocab-bloom-hub-en/resolve/v0.2.0/data/vocab-bloom-hub-en-meanings.jsonl', 'bloom-meanings.jsonl'),
 'bloom-phrasals': ('https://huggingface.co/datasets/Fristail27/vocab-bloom-hub-en/resolve/v0.2.0/data/vocab-bloom-hub-en-phrasal-verbs.jsonl', 'bloom-phrasals.jsonl'),
}
# UK-only spellings must not leak into an American-only curriculum.
UK_ONLY = {'colour','colours','favourite','favour','favourable','favourably','favouritism','favourable','centre','centred','centres','theatre','theatres','metre','litre','litres','travelling','traveller','cancelled','cancelling','organise','organised','realise','realised','analyse','analysed','paralyse','paralysed','licence','grey','neighbour','neighbourhood','behaviour','honour','humour','labour','programme','defence','offence','practise','catalogue','dialogue','cheque','jewellery','tyre','mum','aeroplane','aluminium','whilst','amongst','towards','learnt','burnt','spelt'}
TR_BAD = {'', '-', '?', 'n/a', 'unknown'}
# Transparent, small manual priority cue; NOT an externally calibrated corpus rank.
PRIORITY_LEMMAS = 'acknowledge emphasize anticipate perspective relevant tendency consequently genuinely sufficient inadequate resolve assumption outcome significant establish determine evidence evaluate maintain achieve approach crucial inevitably demonstrate assessment context emphasize sustain enhance distinct adapt insight consistent clarify apparently crucial overall initial complex uncertain'.split()
PRIORITY = {w:i for i,w in enumerate(dict.fromkeys(PRIORITY_LEMMAS))}
PHRASAL_USEFULNESS = {w:i for i,w in enumerate('account for|add up|back up|break down|bring about|bring up|carry out|catch up on|come across|come down to|come up with|cut back on|deal with|draw on|end up|fall apart|fall behind|figure out|follow through|follow up on|get across|get around|get by|get over|give in|go over|hold back|keep up with|lay off|let down|look into|make up for|narrow down|opt out of|phase out|point out|put off|put up with|reach out to|rule out|run into|set aside|set up|sort out|stand out|step down|take over|turn down|work out'.split('|'))}

def norm(w):
 return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC',str(w)).casefold().strip())

def english_form(w,phrase=False):
 if not w or len(w)>64 or any(x in w for x in ('(',')','/','_',':','…')):return False
 if not re.fullmatch(r"[a-z][a-z'\- ]*[a-z]|[a-z]",w):return False
 if not phrase and (' ' in w or '-' in w):return False
 if phrase and not ' ' in w:return False
 return True

def rejected_us(word,area='common'):
 return area in {'british','australian'} or norm(word) in UK_ONLY

def safe_text(value):
 return re.sub(r'\s+',' ',str(value or '').strip())[:550]

def load_json(path):
 return json.loads(Path(path).read_text(encoding='utf8'))

def jsonl(path):
 if not path:return
 import gzip
 op=gzip.open if str(path).endswith('.gz') else open
 with op(path,'rt',encoding='utf8') as f:
  for n,line in enumerate(f,1):
   if not line.strip():continue
   try: yield json.loads(line)
   except json.JSONDecodeError as exc:raise ValueError(f'{path}:{n}: {exc}') from exc

def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def download_sources(names, allow_network=False):
 if not allow_network:raise SystemExit('Remote fetch is opt-in: add --allow-network (no user data is uploaded).')
 SOURCE_DIR.mkdir(parents=True,exist_ok=True)
 for name in names:
  url,filename=SOURCES[name];dest=SOURCE_DIR/filename
  if dest.exists():continue
  print('Downloading',name,'(can be >100 MB)')
  req=urllib.request.Request(url,headers={'User-Agent':'AmericanEnglishLab-CurriculumBuilder/0.2'})
  with urllib.request.urlopen(req,timeout=90) as reply, dest.open('wb') as f:
   import shutil
   shutil.copyfileobj(reply,f)
  if dest.stat().st_size<100:raise ValueError(f'Incomplete source: {dest}')
 return {name:SOURCE_DIR/filename for name,(_,filename) in SOURCES.items()}

def word_candidates(b2,c1,bloom_words=None,bloom_meanings=None,existing=None,frequency=None):
 """Only B2/C1 candidates, not live cards; maintain source provenance and unresolved gaps."""
 existing = {norm(x['word']):x for x in (existing or [])}
 seeded={};rejections=Counter()
 frequency_map={}
 if frequency:
  ranked=load_json(frequency)
  if not isinstance(ranked.get('words'),list):raise ValueError('Invalid frequency source schema')
  frequency_map={norm(x.get('w','')):x['rank'] for x in ranked['words'] if isinstance(x.get('rank'),int) and x['rank']>0}
 for level,path in [('B2',b2),('C1',c1)]:
  if not path:continue
  source=load_json(path)
  if source.get('level') != level or not isinstance(source.get('words'),list):raise ValueError(f'Invalid {level} source schema')
  for row in source['words']:
   w=norm(row.get('w',''))
   if not english_form(w):rejections['invalid_form']+=1;continue
   if rejected_us(w):rejections['british_only']+=1;continue
   if not safe_text(row.get('tr','')).strip() or safe_text(row['tr']).casefold() in TR_BAD:rejections['missing_tr']+=1;continue
   if w in existing:rejections['already_in_curriculum']+=1;continue
   if w in seeded:
    # C1 is not inherently the right level if another list rates it B2: defer to validation.
    seeded[w]['levelDisagreement'] = sorted(set(seeded[w].get('levelDisagreement',[])+[seeded[w]['levelCandidate'],level]));continue
   seeded[w]={
    'id':'g-'+re.sub(r'[^a-z0-9]+','-',w).strip('-'), 'word':w,
    'levelCandidate':level,'trCandidate':safe_text(row['tr']),
    'posCandidate':row.get('pos',[]), 'ipaCandidate':safe_text(row.get('ipa','')),
    'definitionCandidate':'','exampleCandidate':'',
    'frequencyRank':frequency_map.get(w), 'priorityHint':PRIORITY.get(w,99999),'sourceIds':['cefr-j-compilation' if level=='B2' else 'octanove-c1-compilation']+(['ngsl1.2-frequency'] if w in frequency_map else []),
    'sourceLevelUnverified':True,'editorialStatus':'candidate_unreviewed',
   }
 blooms={}; senses=defaultdict(list)
 if bloom_words:
  for row in jsonl(bloom_words):
   word=norm(row.get('word',''))
   if word not in seeded or rejected_us(word,row.get('area_variant','common')):continue
   if row.get('is_obsolete') or row.get('is_abbreviation') or row.get('noun___is_proper') or row.get('verb___is_phrasal'):continue
   if row.get('part_of_speech') not in {'noun','verb','adjective','adverb'}:continue
   # Upper level candidates may be mislabelled by generated source; flag conflicts.
   blooms[(word,row.get('part_of_speech'))]=row
 if bloom_meanings:
  for row in jsonl(bloom_meanings):
   k=(norm(row.get('word','')),row.get('part_of_speech'))
   if k in blooms and not row.get('is_obsolete') and row.get('area_variant') not in ('british','australian'):
    senses[k].append(row)
 for w,v in seeded.items():
  choices=[(k,x) for k,x in blooms.items() if k[0]==w]
  if not choices:continue
  pos=set(v.get('posCandidate',[]))
  choices.sort(key=lambda z:(z[0][1] not in pos,z[0][1]))
  (key,entry)=choices[0]
  # When multiple senses exist, do not silently assume meaning 1 matches Turkish translation.
  matches=senses.get(key,[])
  v['sourceDefinitionCandidate']=safe_text(entry.get('description',''))
  if len(matches)==1:
   sense=matches[0]
   v['definitionCandidate']=safe_text(sense.get('definition',''))
   v['exampleCandidate']=safe_text(next((s for s in sense.get('examples',[]) if re.search(r'\b'+re.escape(w)+r'\b',s,re.I)),''))
  elif matches:
   v['senseCandidates']=[{'definition':safe_text(s.get('definition','')),'example':safe_text((s.get('examples') or [''])[0])} for s in sorted(matches,key=lambda x:x.get('sort_order',999))[:5]]
  v['ipaCandidate']=v['ipaCandidate'] or safe_text(entry.get('transcription'))
  v['sourceIds'].append('vocab-bloom-hub-en-v0.2.0-ai-generated')
  if entry.get('word_level')!=v['levelCandidate']:v['sourceLevelConflict']=entry.get('word_level')
 # Corpus ranking leads, editorial usefulness cues break ties, then B2 precedes C1.
 # Missing frequency is explicitly flagged; such items are not asserted to be rare.
 result=sorted(seeded.values(),key=lambda x:(x['frequencyRank'] is None, x['frequencyRank'] or 999999, x['priorityHint'], x['levelCandidate']!='B2',x['word']))
 return result,rejections

def phrasal_candidates(bloom_words,bloom_meanings,bloom_phrasals,existing):
 existing={norm(x['word']) for x in existing}
 linked=set()
 for r in jsonl(bloom_phrasals):
  for x in r.get('phrasal_variants',[]):linked.add(norm(x))
 entries={};reject=Counter()
 for r in jsonl(bloom_words):
  w=norm(r.get('word',''))
  if w not in linked or not english_form(w,phrase=True):continue
  if w in existing:reject['existing']+=1;continue
  if rejected_us(w,r.get('area_variant','common')):reject['regional_filter']+=1;continue
  if r.get('is_obsolete') or r.get('is_abbreviation'):reject['obsolete_or_abbreviation']+=1;continue
  if not r.get('verb___is_phrasal') or r.get('part_of_speech')!='verb':reject['unverified_phrasal']+=1;continue
  if r.get('word_level') not in ('B2','C1'):reject['out_of_level']+=1;continue
  entries[w]=r
 candidates=defaultdict(list)
 for s in jsonl(bloom_meanings):
  w=norm(s.get('word',''))
  if w in entries and s.get('part_of_speech')=='verb' and not s.get('is_obsolete') and s.get('area_variant') not in ('british','australian'):
   if s.get('meaning_level') in ('B2','C1'):
    candidates[w].append({'definition':safe_text(s.get('definition')),'example':safe_text((s.get('examples') or [''])[0]), 'levelCandidate':s['meaning_level']})
 output=[]
 for w,e in entries.items():
  defs=[s for s in candidates.get(w,[]) if len(s['definition'])>20 and s['example']]
  if not defs:reject['no_teachable_sense']+=1;continue
  syntax=e.get('verb___phrasal_object_pattern','')
  if syntax not in ('separable','inseparable','no_object','separable_pronoun_only'):
   reject['ambiguous_syntax']+=1;continue
  output.append({
   'id':'pv-'+re.sub(r'[^a-z0-9]+','-',w).strip('-'),'word':w,'priorityHint':PHRASAL_USEFULNESS.get(w,99999),
   'levelCandidate':e['word_level'],'ipaCandidate':safe_text(e.get('transcription')),
   'trCandidate':'', 'syntaxCandidate':syntax, 'transitivityCandidate':e.get('verb___transitivity',''),
   'registerCandidate':e.get('language_register',''), 'sensesCandidate':defs,
   'sourceIds':['vocab-bloom-hub-en-v0.2.0-ai-generated'], 'editorialStatus':'candidate_unreviewed',
   'missingRequiredFields':['tr'],
  })
 output.sort(key=lambda e:(e['priorityHint'], e['levelCandidate']!='B2',e['word']))
 return output,reject

def report_and_save(vocab,phrasals,word_stats,pv_stats,inputs):
 QA.mkdir(exist_ok=True)
 (QA/'candidate-vocabulary.json').write_text(json.dumps(vocab,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 (QA/'candidate-phrasals.json').write_text(json.dumps(phrasals,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 report={
  'status':'STAGING_ONLY_NOT_REVIEWED_DO_NOT_PUBLISH',
  'vocabularyCandidates':len(vocab),'phrasalCandidates':len(phrasals),
  'candidateVocabularyWithDefinitionAndExample':sum(bool(v['definitionCandidate'] and v['exampleCandidate']) for v in vocab),
  'candidatePhrasalsWithTurkish':sum(bool(p.get('trCandidate')) for p in phrasals),
  'b2C1Only':all(v['levelCandidate'] in ('B2','C1') for v in vocab) and all(x['levelCandidate'] in ('B2','C1') for x in phrasals),
  'wordsWithCorpusRank':sum(x['frequencyRank'] is not None for x in vocab),
  'noDuplicateCandidates':len({v['word'] for v in vocab})==len(vocab) and len({p['word'] for p in phrasals})==len(phrasals),
  'rejectedVocabulary':dict(word_stats),'rejectedPhrasals':dict(pv_stats),
  'inputSHA256':{k:digest(v) for k,v in inputs.items() if v and Path(v).is_file()},
  'sources':{'ngsl1.2-frequency':{'url':'https://www.newgeneralservicelist.com/new-general-service-list','license':'CC BY-SA 4.0','notice':'rank is a broad corpus frequency proxy, not a verified American podcast frequency ranking'},'cefr-j-compilation':{'url':'https://github.com/recepyagmur/EnglishPractice','upstream':'CEFR-J Wordlist 1.5','licensing':'source compilation with CEFR-J / Octanove attribution; verify individual license before distribution'},'vocab-bloom-hub-en-v0.2.0-ai-generated':{'url':'https://huggingface.co/datasets/Fristail27/vocab-bloom-hub-en','license':'CC BY 4.0','note':'AI-generated; NOT independently verified'}},
  'limitations':['Candidate CEFR labels not certified','No automatic sense/TR alignment','No automatically verified examples','Frequency rank covers only terms present in NGSL top 3000','No candidate appears in live lessons or release totals','US accent requires audio QA, IPA does not prove accent'],
 }
 (QA/'bulk-import-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 return report

def run(paths):
 oldv=load_json(ROOT/'data/vocabulary.json');oldp=load_json(ROOT/'data/phrasals.json')
 vocab,vstats=word_candidates(paths.get('cefr-b2'),paths.get('cefr-c1'),paths.get('bloom-words'),paths.get('bloom-meanings'),oldv,paths.get('frequency'))
 phrasals,pstats=([],Counter())
 if all(paths.get(k) for k in ('bloom-words','bloom-meanings','bloom-phrasals')):
  phrasals,pstats=phrasal_candidates(paths['bloom-words'],paths['bloom-meanings'],paths['bloom-phrasals'],oldp)
 return report_and_save(vocab,phrasals,vstats,pstats,paths)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 for key in SOURCES:parser.add_argument('--'+key, type=Path)
 parser.add_argument('--download',action='store_true',help='Download licensed source files to local sources/ (never send user data)')
 parser.add_argument('--allow-network',action='store_true',help='Explicit network opt-in for --download')
 args=parser.parse_args()
 paths={k:getattr(args,k.replace('-','_')) for k in SOURCES}
 if args.download:paths.update({k:v for k,v in download_sources(SOURCES.keys(),args.allow_network).items() if not paths[k]})
 if not paths['cefr-b2'] and not paths['cefr-c1']:parser.error('Specify CEFR B2/C1 source files or --download --allow-network')
 report=run(paths)
 print(json.dumps({k:v for k,v in report.items() if k in ('status','vocabularyCandidates','phrasalCandidates','candidateVocabularyWithDefinitionAndExample','candidatePhrasalsWithTurkish','b2C1Only','noDuplicateCandidates')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
