#!/usr/bin/env python3
"""Fetch VOA publisher transcripts into a review-only staging file.

This tool never makes an imported lesson playable/approved. No fake audio URLs,
no invented transcripts, no auto-created quiz answers.
Usage:
  python tools/stage_voa_transcripts.py                  # dry run, offline
  python tools/stage_voa_transcripts.py --fetch          # requires network
"""
import argparse
import datetime as dt
import html
import json
import re
import urllib.request
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'data/voa-source-catalog.json'
STAGING=ROOT/'sources/voa-transcripts-staging.json'
USER_AGENT='AmericanEnglishLab/1.0 (educational VOA transcript review)'
SPEAKER=re.compile(r'^([A-Za-z][A-Za-z. ]{0,35}):\s*(.+)$')
MP3=re.compile(r'https?://voa-audio\.voanews\.eu/[^"<>\s]+?\.mp3(?:\?download=1)?',re.I)
BLOCKING_HEADINGS=('listening quiz','quiz','speaking practice','speaking','pronunciation','free materials','for teachers','learn the')


def extract_transcript(html_content):
    """Extract speaker-labelled dialogue from VOA's Conversation section.

    The exact publisher page structure varies. Fail closed for pages where no
    meaningful dialog can be extracted. Discard unlabeled staging text rather
    than pretend it is transcript. A language editor must check completeness.
    """
    soup=BeautifulSoup(html_content,'html.parser')
    for tag in soup(['script','style','noscript']):tag.decompose()
    headings=[h for h in soup.find_all(re.compile('^h[1-6]$')) if h.get_text(' ',strip=True).casefold()=='conversation']
    if not headings:
        return []
    header=headings[0]
    turns=[]
    started=False
    # Select actual visible leaf text containers after Conversation. Ignore nested duplicates.
    for node in header.next_elements:
        if node is header:continue
        if getattr(node,'name',None) and re.fullmatch('h[1-6]',node.name or ''):
            name=node.get_text(' ',strip=True).casefold()
            if name and (name.startswith(BLOCKING_HEADINGS) or 'quiz' in name):break
        if getattr(node,'name',None) not in ('p','li'):
            continue
        if node.find_parent(['script','style']):continue
        line=' '.join(node.stripped_strings)
        if not line or len(line)>1500:continue
        match=SPEAKER.match(line)
        if match:
            speaker,said=match.groups()
            if speaker.casefold() in ('direct link','image','source','related','quiz'):continue
            turns.append({'speaker':speaker.strip(),'text':said.strip()})
            started=True
        elif started and turns and line and not any(line.casefold().startswith(x) for x in BLOCKING_HEADINGS):
            # A continuation paragraph may be a new line of the same speaker.
            if len(line)>=3 and not re.search(r'^\d+:\d+',line):
                turns[-1]['text']+=' '+line
    return turns if len(turns)>=5 else []


def extract_mp3_urls(html_content):
    txt=html.unescape(html_content).replace('\\/','/')
    found=[]
    for raw in MP3.findall(txt):
        url=raw.rstrip('.,;')
        if urlparse(url).hostname=='voa-audio.voanews.eu' and url not in found:
            found.append(url)
    return found


def retrieve_page(url,timeout=25):
    if urlparse(url).hostname!='learningenglish.voanews.com':
        raise ValueError('Disallowed host')
    req=urllib.request.Request(url,headers={'User-Agent':USER_AGENT})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        ctype=r.headers.get('Content-Type','')
        if 'html' not in ctype:raise ValueError('Publisher returned non-HTML')
        buf=r.read(1_500_000+1)
    if len(buf)>1_500_000:raise ValueError('Page exceeds safety limit')
    return buf.decode('utf8','replace')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--fetch',action='store_true',help='Explicit network retrieval; save parsed but unapproved staging only')
    ap.add_argument('--limit',type=int,default=50,help='Maximum number of catalog pages to fetch')
    args=ap.parse_args()
    if not 1<=args.limit<=50:ap.error('--limit must be 1-50')
    catalog=json.loads(CATALOG.read_text(encoding='utf8'))
    pending=[x for x in catalog if not x['transcriptImported']][:args.limit]
    if not args.fetch:
        print(json.dumps({'dryRun':True,'catalog':len(catalog),'alreadyInteractive':sum(bool(x.get('transcriptImported')) for x in catalog),'pending':len(pending),'savedToStaging':0,'releaseApproved':False},indent=2))
        return
    results=[]
    for item in pending:
        try:
            page=retrieve_page(item['sourceUrl'])
            turns=extract_transcript(page)
            urls=extract_mp3_urls(page)
            results.append({'id':item['id'],'sourceUrl':item['sourceUrl'],'speakerTurns':turns,
                            'candidateMp3Urls':urls,'status':'extracted_needs_editor_review' if turns else 'manual_review_required',
                            'publisherTranscriptReviewed':False,'audioVerified':False,'rightsReviewed':False,'quizAuthored':False})
        except Exception as e:
            results.append({'id':item['id'],'sourceUrl':item['sourceUrl'],'status':'fetch_failed',
                            'reason':str(e),'speakerTurns':[],'candidateMp3Urls':[]})
    payload={'generated':dt.date.today().isoformat(),'publicDomainNotice':'VOA originals only; third-party segments excluded',
             'editorApproved':False,'audioDownloaded':False,'results':results}
    STAGING.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'staging':str(STAGING),'parsed':sum(bool(x['speakerTurns']) for x in results),
                      'manualOrFailed':sum(not x['speakerTurns'] for x in results),'publishedLessonsAdded':0},indent=2))
if __name__=='__main__':main()
