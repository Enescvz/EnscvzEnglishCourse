#!/usr/bin/env python3
"""Development-only evidence-based release audit; never converts tests to human approvals."""
import argparse, json, subprocess
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def list_ids(items):return [x['id'] for x in items]
def audit(run_tests=False):
    status=read('development-status.json')
    auth=read('data/authentic-listening.json')
    linked=read('data/voa-source-quizzes.json')
    catalog=read('data/voa-source-catalog.json')
    core=read('data/toefl-core.json')
    reading=read('data/toefl-reading-practice.json')
    writing=read('data/toefl-writing-practice.json')
    scripts=read('data/toefl-listening-practice.json')
    questions=sum(len(l.get('questions',[])) for l in auth+linked)
    reading_count=sum(len(x.get('questions',[])) for x in reading)
    results={
      'voa_lessons':len(catalog),
      'in_app_transcripts':len(auth),
      'publisher_link_only':len(linked),
      'voa_questions':questions,
      'toefl_word_ids':len(core['wordLessonIds']),
      'toefl_phrasal_ids':len(core['phrasalLessonIds']),
      'toefl_reading_items':reading_count,
      'toefl_writing_tasks':len(writing),
      'toefl_listening_scripts_without_verified_audio':len(scripts),
      'bundled_approved_human_recordings':status['verifiedHumanAudio'],
      'legacy_synthetic_mp3':status['bundledSyntheticAudio']
    }
    structural={
      '50_unique_voa_sources':len(set(list_ids(catalog)))==len(catalog)==50,
      '50_voa_lesson_integrity':len(auth)+len(linked)==50 and len(set(list_ids(auth)+list_ids(linked)))==50,
      '204_voa_quiz_items':questions==204,
      '400_unique_toefl_words':len(core['wordLessonIds'])==len(set(core['wordLessonIds']))==400,
      '75_unique_toefl_phrasals':len(core['phrasalLessonIds'])==len(set(core['phrasalLessonIds']))==75,
      'toefl_reading_original_questions':reading_count==50,
      'no_unverified_human_mp3_claim':all(not item.get('audioBundled',False) for item in auth+linked),
      'release_gate_stays_locked':status['readyForRelease'] is False
    }
    if not all(structural.values()):raise SystemExit('CORE CONTENT / LOCK INTEGRITY FAILED: '+str(structural))
    tests={}
    if run_tests:
      for key,command in [('node',['npm','test']),('python',['python3','-m','unittest','discover','-s','tests','-p','test_*.py'])]:
        p=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=180)
        if p.returncode!=0:raise SystemExit(f'{key} tests failed: '+p.stderr[-1500:])
        import re
        count=re.search(r'# pass (\d+)',p.stdout) if key=='node' else re.search(r'Ran (\d+) tests',p.stderr)
        tests[key]={'passed':int(count.group(1)) if count else None,'exit':p.returncode}
    blockers={
      'real_iphone_safari_offline_e2e':'OPEN_NOT_PERFORMED',
      'real_device_human_mp3_playback_and_alignment':'OPEN_NOT_PERFORMED',
      'voa_29_in_app_transcripts':'OPEN' if len(linked)>0 else 'COMPLETE',
      'local_human_audio_bundles':'OPEN' if status['verifiedHumanAudio']==0 else 'PARTIAL',
      'toefl_calibrated_adaptive_score':'OPEN_NO_ETS_CALIBRATION',
      'external_language_editor_475_cards':'OPEN_NO_EDITOR_SIGNOFF',
      'real_longitudinal_memory_gain':'OPEN_NOT_MEASURED',
      'copyright_clearance_of_all_older_sources':'OPEN_PENDING_HUMAN_REVIEW',
      'real_webkit_browser_e2e':'OPEN_NOT_AVAILABLE'
    }
    return {'auditDate':datetime.now(timezone.utc).isoformat(), 'project':'American English Lab',
       'scope':'PRIVATE_ENGINEERING_ONLY', 'structural':structural,'content':results,
       'automaticTests':tests, 'externalBlockers':blockers,
       'notes':['Automated unit tests do not validate real iPhone Safari, human speech or TOEFL scoring.',
       'Reading and Writing original AEL exercises do not confer an official ETS result.',
       'VOA online links do not mean bundled audio or verified playback.'],
       'releaseReady':False,'recommendedRating':None,'releaseGate':'LOCKED'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--test',action='store_true')
    args=parser.parse_args()
    report=audit(args.test)
    out=ROOT/'qa/engineering-release-audit-20261029.json'
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'tests':report['automaticTests'],'content':report['content'],'externalBlockers':report['externalBlockers'],'releaseGate':report['releaseGate']},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
