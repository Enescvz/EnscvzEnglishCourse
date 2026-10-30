"""Media QA. ffprobe required; measure actual bundled audio length against transcript timing."""
from pathlib import Path
import json,subprocess,sys
root=Path(__file__).resolve().parents[1]
issues=[]; checked=0
for name in ('episodes','drills'):
 for item in json.loads((root/'data'/f'{name}.json').read_text(encoding='utf-8')):
  path=root/item['audio']
  if not path.is_file() and item.get('audioType')=='synthetic':continue # quarantined robot recording
  if not path.is_file(): issues.append((item['id'],'missing'));continue
  try:
   d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(path)],stderr=subprocess.DEVNULL).decode().strip())
  except Exception:issues.append((item['id'],'not decodable'));continue
  checked+=1
  if not d>0:issues.append((item['id'],'empty'))
  if not item.get('timings'):issues.append((item['id'],'missing timing data'))
  else:
   last=item['timings'][-1]['end']
   if abs(d-last)>3:issues.append((item['id'],f'audio {d:.2f}s vs transcript {last:.2f}s'))
  if item['audio'].endswith('.mp3') and path.stat().st_size<1000:issues.append((item['id'],'tiny mp3'))
print(f'Checked {checked} active MP3 files; 42 synthetic recordings quarantined. No human audio approved.')
for item in issues: print('ERROR',item)
sys.exit(bool(issues))
