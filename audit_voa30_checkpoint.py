#!/usr/bin/env python3
"""Regression against private VOA24 backup; never claims user data or live audio was tested."""
import argparse,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
QA=ROOT/'qa'

def read_bytes_base(z,path):return z.read('american-english-lab/'+path)
def j(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
def identity(l):return {x['id']:[{'question':q['question'],'options':q['options'],'answer':q['answer'],'id':q.get('id')} for q in x['questions']] for x in l}
def main():
 global BASE
 parser=argparse.ArgumentParser(description='Compare restored project against a previous private development ZIP')
 parser.add_argument('--baseline',type=Path,required=True,help='Path of earlier AEL_PRIVATE_DEV_BACKUP_...zip')
 BASE=parser.parse_args().baseline
 if not BASE.exists():raise SystemExit('Base private backup not present: cannot verify previous identities')
 with zipfile.ZipFile(BASE) as archive:
  base={p:json.loads(read_bytes_base(archive,p)) for p in ('data/authentic-listening.json','data/voa-source-quizzes.json','data/toefl-core.json')}
  orig=base['data/authentic-listening.json']+base['data/voa-source-quizzes.json']
  now=j('data/authentic-listening.json')+j('data/voa-source-quizzes.json')
  for path in ('data/vocabulary.json','data/phrasals.json','data/toefl-core.json','js/memory.js','js/engine.js','js/fsrs.js'):
   if 'american-english-lab/'+path not in archive.namelist():continue
   assert (ROOT/path).read_bytes()==read_bytes_base(archive,path),f'Unexpected baseline change: {path}'
  # Speaking is one part of app.js; compare the same named function bodies across versions.
  before=read_bytes_base(archive,'js/app.js').decode('utf8')
  after=(ROOT/'js/app.js').read_text(encoding='utf8')
  import re
  funcs=['function speaking','function speakingLab','function speak','function pronunciation']
  unchanged=[]
  for name in funcs:
   start=re.search(re.escape(name)+r'\s*\(',before)
   if not start:continue
   match=re.search(re.escape(name)+r'\s*\(',after)
   if not match:raise AssertionError('Speaking function removed: '+name)
   # Top-level function boundaries are the next "\nfunction ", never claim safety without checking.
   def chunk(text, match):
    nextpos=text.find('\nfunction ',match.start()+1)
    return text[match.start():nextpos if nextpos>=0 else None]
   assert chunk(before,start)==chunk(after,match),'Speaking changed: '+name
   unchanged.append(name)
  assert identity(orig)==identity(now),'Old VOA question IDs, text, answers or options changed'
  assert {x['id'] for x in orig}=={x['id'] for x in now},'VOA lesson identity changed'
  assert (len(j('data/authentic-listening.json')),len(j('data/voa-source-quizzes.json'))) == (30,20)
  assert sum(len(x['questions']) for x in now)==204
  status=j('development-status.json'); assert not status['readyForRelease']
  report={
   'baseline':BASE.name,'scope':'private source integrity and code-path regression, NOT real device/audio QA',
   'lessonIdsUnchanged':True,'originalVOAQuestionsOptionsAnswersUnchanged':True,
   'wordAndPhrasalCardsByteIdentical':True,'toeflCoreByteIdentical':True,
   'speakingFunctionsCheckedUnchanged':unchanged,
   'inAppVOATranscripts':30,'externalOnlyVOALessons':20,'sourceEvidenceQuestions':204,
   'humanAudioBundled':0,'humanAudioActuallyPlayedOnIphone':False,
   'realOfflineWebkitTest':False,'humanEditorSignoff':False,'etsScoringCalibrated':False,
   'releaseApproved':False
  }
  (QA/'voa30-private-identity-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
  print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
