#!/usr/bin/env python3
"""Only allow independently approved licensed human recordings in offline audio manifest."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
def audio_files():
    recordings=json.loads((ROOT/'data/episodes.json').read_text())+json.loads((ROOT/'data/drills.json').read_text())
    provenance=json.loads((ROOT/'data/audio-provenance.json').read_text())['recordings']
    approved={key for key,value in provenance.items() if value.get('quality')=='approved' and value.get('license_evidence') and value.get('human_reviewer') and value.get('transcript_verified') and value.get('timing_verified')}
    names=sorted({str(x['audio']).lstrip('/') for category,items in [('episode',recordings[:len(json.loads((ROOT/'data/episodes.json').read_text()))]),('drill',recordings[len(json.loads((ROOT/'data/episodes.json').read_text())):])] for x in items if f'{category}:{x["id"]}' in approved})
    for n in names:
        if not n.startswith('assets/audio/') or not (ROOT/n).is_file():raise ValueError('Missing recording: '+n)
    return names

def update():
    p=ROOT/'sw.js';src=p.read_text(encoding='utf-8')
    names=audio_files()
    lines='const AUDIO='+json.dumps(['./'+x for x in names],ensure_ascii=False,separators=(',',':'))+';'
    src,count=re.subn(r'const AUDIO=\[[^\n]*\];',lambda _:lines,src,count=1)
    if count!=1:raise ValueError('sw.js AUDIO declaration not found')
    # CACHE version belongs to the caller; do not overwrite new PWA revisions.
    # Candidates are research content, cache opportunistically when research page is visited.
    # Preserve existing cached scripts; never inject duplicate entries.
    p.write_text(src,encoding='utf-8')
    print(f'Offline audio entries: {len(names)}; total bytes {sum((ROOT/n).stat().st_size for n in names):,}')
    return names
if __name__=='__main__':update()
