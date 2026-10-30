#!/usr/bin/env python3
"""Optional offline import of licensed VOA-original audio.

Requires internet. This action is NOT used to claim audio exists until each
recording passes download/content checks. Originals are unmodified; attribution
and the source URL stay in the lesson metadata.
"""
import argparse
import hashlib
import json
import mimetypes
import os
import tempfile
import urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/authentic-listening.json'


def retrieve(lesson, timeout=45):
    url=lesson['audioUrl']
    request=urllib.request.Request(url,headers={'User-Agent':'American-English-Lab/1.0 (educational audio download)'})
    with urllib.request.urlopen(request,timeout=timeout) as response:
        typ=(response.headers.get('Content-Type') or '').lower()
        if 'text/html' in typ:
            raise ValueError('Expected MP3, received HTML for '+lesson['id'])
        audio=response.read(18*1024*1024+1)
    if not 20_000<=len(audio)<=18*1024*1024:
        raise ValueError('Unexpected MP3 size for '+lesson['id'])
    if not (audio.startswith(b'ID3') or (audio[0]==0xff and (audio[1]&0xe0)==0xe0)):
        raise ValueError('Audio header does not appear to be MP3: '+lesson['id'])
    return audio


def main():
    parser=argparse.ArgumentParser(description='Download the VOA pilot MP3s only when network access is available')
    parser.add_argument('--download',action='store_true',help='Explicitly permit network access and file writes')
    args=parser.parse_args()
    lessons=json.loads(DATA.read_text(encoding='utf-8'))
    if not args.download:
        print(json.dumps({'dryRun':True,'status':'NO_AUDIO_DOWNLOADED','count':len(lessons),'urlList':[x['sourceUrl'] for x in lessons]},ensure_ascii=False,indent=2))
        return
    results=[]
    for lesson in lessons:
        try:
            audio=retrieve(lesson)
            dest=ROOT/'assets/audio'/f'{lesson["id"]}.mp3'
            dest.parent.mkdir(parents=True,exist_ok=True)
            with tempfile.NamedTemporaryFile(dir=dest.parent,delete=False) as temp:
                temp.write(audio)
                tmp=Path(temp.name)
            os.replace(tmp,dest)
            results.append({'id':lesson['id'],'status':'downloaded','sha256':hashlib.sha256(audio).hexdigest(),'bytes':len(audio),'localPath':str(dest.relative_to(ROOT))})
        except Exception as exc:
            results.append({'id':lesson['id'],'status':'failed','error':str(exc)})
    # Update offline paths only after actual validated downloads. Editing the
    # supplied transcript / QA state is intentionally forbidden here.
    success={r['id']:r for r in results if r['status']=='downloaded'}
    if success:
        for lesson in lessons:
            if lesson['id'] in success:
                lesson['localAudio']=success[lesson['id']]['localPath']
                lesson['offlineReady']=True
                lesson['audioAvailability']='bundled_original_mp3'
        DATA.write_text(json.dumps(lessons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        # Retain every prior cached MP3 and include only the downloaded files.
        import re
        sw=ROOT/'sw.js'
        content=sw.read_text(encoding='utf-8')
        match=re.search(r'const AUDIO=(\[[^\n]*\]);',content)
        if not match:
            raise ValueError('Service worker AUDIO declaration missing')
        audio_paths=json.loads(match.group(1))
        for item in success.values():
            local='./'+item['localPath']
            if local not in audio_paths:
                audio_paths.append(local)
        content=content[:match.start()]+('const AUDIO='+json.dumps(sorted(audio_paths),separators=(',',':'))+';')+content[match.end():]
        content=re.sub(r"const CACHE='[^']+';", "const CACHE='ael-dev-20261028-voa-bundled-'+str(len(success))+';", content,count=1)
        sw.write_text(content,encoding='utf-8')
    # Important: downloaded does not equal QA approved or time alignment.
    report={'source':'VOA Learning English','licenseEvidence':'https://learningenglish.voanews.com/p/6861.html','recordings':results}
    (ROOT/'qa/voa-audio-download-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if any(x['status']=='failed' for x in results):
        raise SystemExit(1)
if __name__=='__main__':main()
