#!/usr/bin/env python3
"""One-command, 3-source B2/C1 headword + phrasal-verb harvest.

This pulls the original, attributed CEFR-J / Octanove level profiles and
attributed CC-BY-NC 4.0 phrasal-verb EN/TR lexicons. It writes an isolated
staging index. It never invents definitions or certifies phrasal CEFR levels.
No backend/API subscription; needs internet only to fetch the sources once.

python3 tools/fast_source_import.py --download
python3 tools/fast_source_import.py --offline
"""
import argparse,csv,io,json,re,urllib.request,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'sources'; QA=ROOT/'qa'
BASE='https://raw.githubusercontent.com/'
URLS={
 'cefr_b2':BASE+'openlanguageprofiles/olp-en-cefrj/master/cefrj-vocabulary-profile-1.5.csv',
 'octanove_c1':BASE+'openlanguageprofiles/olp-en-cefrj/master/octanove-vocabulary-profile-c1c2-1.0.csv',
 'phrasal_en':BASE+'tema4p/english-vocabulary/main/content/phrasal-verbs/English_Phrasal_Verbs_in_Action_EN.txt',
 'phrasal_tr':BASE+'tema4p/english-vocabulary/main/content/phrasal-verbs/English_Phrasal_Verbs_in_Action_TR.txt',
}
LICENSES={
 'cefr_b2':'CEFR-J Wordlist Version 1.5, compiled by Yukio Tono, Tono Laboratory, TUFS; free use with attribution',
 'octanove_c1':'Octanove Vocabulary Profile C1/C2 1.0, CC BY-SA 4.0',
 'phrasal_en':'English Vocabulary by tema4p, CC BY-NC 4.0',
 'phrasal_tr':'English Vocabulary by tema4p, CC BY-NC 4.0',
}
# For headword *index* only. This is not a claim that every sense is US-specific.
UK_ONLY={'colour','favourite','favour','centre','theatre','metre','litre','travelling','traveller','cancelled','cancelling','organise','organised','realise','realised','analyse','analysed','grey','neighbour','behaviour','honour','humour','labour','programme','defence','offence','licence','cheque','jewellery','tyre','mum','aeroplane','aluminium','whilst','amongst'}

def download(url,destination):
    request=urllib.request.Request(url,headers={'User-Agent':'AmericanEnglishLab/1.0 (+personal-education)'})
    with urllib.request.urlopen(request, timeout=35) as response: raw=response.read()
    if len(raw)<300:raise ValueError(f'Empty / interrupted download: {url}')
    destination.write_bytes(raw)

def rows_from_csv(path,level):
    rows=[]
    with path.open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream)
        if not {'headword','pos','CEFR'}<=set(reader.fieldnames or []):raise ValueError('Unexpected CSV headers: '+str(path))
        for row in reader:
            if row['CEFR'].upper()!=level:continue
            head=row['headword'].strip().lower()
            # Do not mistake punctuation, multiword terms or UK-only forms for American single-word cards.
            if not re.fullmatch("[a-z][a-z'-]*",head) or head in UK_ONLY:continue
            rows.append({'word':head,'levelCandidate':level,'partOfSpeech':row['pos'].strip(),
                         'source':'cefr_b2' if level=='B2' else 'octanove_c1',
                         'status':'levelled_headword_only','americanPronunciationVerified':False})
    return rows

def parse_phrasals(path):
    parsed={}
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        if ' - ' not in line:continue
        phrase,definition=line.split(' - ',1)
        phrase=' '.join(phrase.strip().lower().split())
        if len(phrase)>72 or len(phrase.split())<2 or not definition.strip():continue
        if not re.fullmatch(r"[a-z]+(?:[ '\-()a-z]+)",phrase):continue
        # Parenthetical variants are structural alternatives; discard rather than guess.
        if '(' in phrase or ')' in phrase:continue
        if phrase not in parsed:parsed[phrase]=definition.strip()
    return parsed

def stage(paths):
    QA.mkdir(parents=True,exist_ok=True)
    existing=json.loads((ROOT/'data/vocabulary.json').read_text(encoding='utf-8'))
    oldwords={x['word'].lower() for x in existing if x.get('category')=='general'}
    oldpv={x['word'].lower() for x in json.loads((ROOT/'data/phrasals.json').read_text(encoding='utf-8'))}
    candidates={}; disagreement=set(); source_counts={}
    for key,level in [('cefr_b2','B2'),('octanove_c1','C1')]:
        source_rows=rows_from_csv(paths[key],level);source_counts[key]=len(source_rows)
        for row in source_rows:
            w=row['word']
            if w in candidates:
                if candidates[w]['levelCandidate']!=level: disagreement.add(w)
            else:candidates[w]=row
    for w in disagreement:candidates[w]['sourceLevelDisagreement']=['B2','C1']
    to_add=[v for w,v in candidates.items() if w not in oldwords]
    to_add.sort(key=lambda x:(x['levelCandidate']!='B2',x['word']))
    en=parse_phrasals(paths['phrasal_en']);tr=parse_phrasals(paths['phrasal_tr'])
    ph=[]
    for w,definition in en.items():
        if w in oldpv:continue
        ph.append({'word':w,'definitionCandidate':definition,'turkishCandidate':tr.get(w,''),
                   'levelCandidate':None,'americanUsageVerified':False,'source':'phrasal_en',
                   'status':'UNCLASSIFIED_LEVEL_UNREVIEWED'})
    ph.sort(key=lambda x:x['word'])
    (QA/'fast-vocabulary-candidates.json').write_text(json.dumps(to_add,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (QA/'fast-phrasal-candidates.json').write_text(json.dumps(ph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report={'releaseReady':False,'sourceB2Rows':source_counts['cefr_b2'], 'sourceC1Rows':source_counts['octanove_c1'],
            'distinctSourceHeadwords':len(candidates),'newHeadwordCandidates':len(to_add),
            'candidateLevelDisagreements':len(disagreement),'phrasalSourceUnique':len(en),
            'newUnlevelledPhrasalCandidates':len(ph),'phrasalWithTurkish':sum(bool(x['turkishCandidate']) for x in ph),
            'newReviewedLearningCards':0,
            'warning':'Source headwords and phrasal candidates are not reviewed cards. 600 B2/C1 phrasals are not yet certified.',
            'sources':{key:{'url':URLS[key],'licensing':LICENSES[key], 'sha256':hashlib.sha256(paths[key].read_bytes()).hexdigest()} for key in URLS}}
    (QA/'fast-import-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--download',action='store_true')
    mode.add_argument('--offline',action='store_true')
    args=parser.parse_args();SRC.mkdir(exist_ok=True)
    paths={key:SRC/(key+'.'+('csv' if 'cefr' in key or 'octanove' in key else 'txt')) for key in URLS}
    if args.download:
        for key,url in URLS.items():
            if not paths[key].is_file() or paths[key].stat().st_size<300:download(url,paths[key])
    for key,path in paths.items():
        if not path.is_file():parser.error('Missing '+str(path)+'; use --download where internet is available')
    print(json.dumps(stage(paths),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
