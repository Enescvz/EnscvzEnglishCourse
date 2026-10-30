#!/usr/bin/env python3
"""Stage / validate 10 publisher conversation transcripts, optionally apply after review.

Requires internet for --fetch. BeautifulSoup4 required for HTML parsing. Does not
infer audio approval. Never imports third-party songs without a human review.
"""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT/'data/voa-source-catalog.json'
LINKED = ROOT/'data/voa-source-quizzes.json'
AUTHENTIC = ROOT/'data/authentic-listening.json'
STAGED = ROOT/'qa/voa-source-staging'
IDS = [f'voa-1-{i}' for i in range(33, 43)]
RIGHTS = 'https://learningenglish.voanews.com/p/6861.html'
SPEAKER = re.compile(r'^([\w][\w .’\'/-]{0,35}):\s*(.+)$', re.U)
MIN_TURNS = 10
MIN_WORDS = 120


def normalize(s):
    return re.sub(r'\W+', ' ', s, flags=re.U).casefold().strip()


def parse_publisher_html(html):
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise RuntimeError('Run: python -m pip install beautifulsoup4') from exc
    soup = BeautifulSoup(html, 'html.parser')
    # The primary VOA Conversation transcript is between a Conversation heading
    # and the next Quiz heading. Reject if a clear section cannot be detected.
    heads = soup.find_all(re.compile(r'^h[1-6]$'))
    heading = next((h for h in heads if normalize(h.get_text(' ', strip=True)) == 'conversation'), None)
    if heading is None:
        raise ValueError('Conversation heading missing: no guessing from other parts of the page')
    quiz = next((h for h in heads if h is not heading and re.search(r'\bquiz\b', h.get_text(' ', strip=True), re.I)
                 and h.sourceline != heading.sourceline), None)
    nodes = []
    audio_hrefs=[]
    # Walk forward through DOM nodes, stopping at a subsequent heading whose
    # visible title contains Quiz; uses text-bearing blocks rather than page-wide regex.
    cursor = heading
    for node in heading.next_elements:
        if getattr(node, 'name', '') and re.match(r'^h[1-6]$', str(node.name)) and 'quiz' in node.get_text(' ', strip=True).lower():
            break
        if getattr(node, 'name', '') == 'a' and node.get('href'):
            href=str(node['href'])
            if '.mp3' in href and 'voa' in href.lower():audio_hrefs.append(href)
        if getattr(node, 'name', '') in ('p', 'li'):
            # Include only outer paragraphs; some pages nest spans, but not p inside p.
            txt = node.get_text(' ', strip=True)
            if txt:
                nodes.append(txt)
    # Also support single paragraph scripts with newline-delimited speaker turns.
    turns, dropped = [], []
    for paragraph in nodes:
        for line in paragraph.splitlines():
            line = ' '.join(line.split())
            found = SPEAKER.match(line)
            if found:
                speaker, content = found.groups()
                turns.append({'speaker': speaker.strip(), 'text': content.strip(), 'kind': 'speech'})
            elif line.startswith('(') and line.endswith(')'):
                turns.append({'speaker': 'Stage direction', 'text': line, 'kind': 'stage_direction'})
            elif turns and not re.match(r'^(?:Quiz|Listen to|Related|Start Quiz)', line, re.I):
                # Non-colon publisher line continuation: keep only if likely dialogue,
                # but flag for human verification in report.
                dropped.append(line)
    content_words = sum(len(t['text'].split()) for t in turns if t['kind']=='speech')
    if len(turns)<MIN_TURNS or content_words<MIN_WORDS:
        raise ValueError(f'Conversation seems incomplete: {len(turns)} turns, {content_words} words')
    warnings = [f'{len(dropped)} publisher lines without speaker require review'] if dropped else []
    if re.search(r'\b(song lyrics|sings|music plays|copyright|\blyrics\b)', ' '.join(nodes), re.I):
        warnings.append('Potential third-party song/lyrics: manual exclusion required')
    return turns, warnings, dropped, audio_hrefs


def stage_one(catalog_item, linked_item, html):
    turns, warnings, dropped, audio_hrefs = parse_publisher_html(html)
    speech_text=' '.join(t['text'] for t in turns if t['kind']=='speech')
    evidence=[]
    reviewed_questions=copy.deepcopy(linked_item['questions'])
    for i,q in enumerate(reviewed_questions):
        quote=q.get('sourceEvidence') or ''
        exact=bool(quote and normalize(quote) in normalize(speech_text))
        turn_index=next((j for j,t in enumerate(turns) if quote and normalize(quote) in normalize(t['text'])),None)
        if turn_index is not None:
            q['sourceEvidenceTurn']=turn_index
            q['sourceReviewStatus']='publisher_page_turn_reviewed_not_audio_verified'
        evidence.append({'questionIndex':i, 'foundInTranscript':exact,
                         'publisherEvidence':quote[:200], 'evidenceKind':q.get('sourceEvidenceKind')})
    if not all(row['foundInTranscript'] for row in evidence):
        warnings.append('At least one quiz evidence excerpt not found verbatim; manually reconcile before import')
    resolved=[urljoin(catalog_item['sourceUrl'],path) for path in audio_hrefs]
    safe_audio=next((url for url in resolved if urlparse(url).scheme=='https' and
        urlparse(url).hostname in ('voa-audio.voanews.eu','voa-audio.voanews.com')),None)
    if not safe_audio:warnings.append('No publisher-linked MP3 URL extracted; verify audio link manually')
    lesson={
        'id':linked_item['id'], 'title':linked_item['title'], 'level':linked_item['level'],
        'topic':linked_item['topic'], 'minutes':None, 'sourceUrl':linked_item['sourceUrl'],
        'audioUrl':safe_audio, 'attribution':'VOA Learning English — original publisher conversation',
        'sourceSeries':"Let's Learn English — Level 1", 'sourceLicense':'VOA original public domain with attribution; third-party excluded',
        'rightsUrl': RIGHTS, 'audioProvider':'VOA Learning English', 'audioType':'human_dialogue_source',
        'audioAvailability':'external_online_stream_only' if safe_audio else 'publisher_page_link_only_unverified', 'audioBundled':False, 'offlineReady':False,
        'transcriptSource':'VOA publisher Conversation HTML; not independently compared to audio',
        'transcriptImported':True, 'transcriptVerifiedAgainstAudio':False, 'timingVerified':False,
        'quality':'external_source_not_independently_audio_reviewed', 'turns':turns,
        'questions':reviewed_questions, 'transcriptScope':'publisher_conversation_only',
        'transcriptRightsExclusion':'Third-party music, lyrics, images and other non-VOA content excluded'
    }
    return lesson, {'catalogId':catalog_item['id'],'lessonId':linked_item['id'],
                    'publisherURL':catalog_item['sourceUrl'],'publisherMp3URL':safe_audio,'turns':len(turns),
                    'words':sum(len(t['text'].split()) for t in turns), 'questions':evidence,
                    'warnings':warnings, 'nonDialogueLines':dropped[:15],
                    'sourceChecksum':hashlib.sha256(html.encode('utf-8')).hexdigest(),
                    'independentHumanReviewed':False, 'audioTestedOnIPhone':False}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--fetch', action='store_true', help='Fetch ten VOA pages over HTTPS')
    ap.add_argument('--html-dir',type=Path,help='Folder with voa-1-33.html...voa-1-42.html')
    ap.add_argument('--apply',action='store_true',help='Modify app data only after source review')
    ap.add_argument('--confirmed-publisher-comparison',action='store_true',help='Affirm manual review and third-party exclusion for all ten')
    args=ap.parse_args()
    if (args.fetch == bool(args.html_dir)):
        ap.error('Choose exactly one of --fetch or --html-dir')
    if args.apply and not args.confirmed_publisher_comparison:
        ap.error('--apply requires --confirmed-publisher-comparison; automatic parsing is not a human review')
    catalog=json.loads(CATALOG.read_text(encoding='utf-8'))
    linked=json.loads(LINKED.read_text(encoding='utf-8'))
    authentic=json.loads(AUTHENTIC.read_text(encoding='utf-8'))
    cat_by={x['id']:x for x in catalog}; link_by={x['catalogId']:x for x in linked}
    STAGED.mkdir(parents=True,exist_ok=True)
    report=[]; lessons=[]
    for key in IDS:
        cat=cat_by[key]; li=link_by[key]
        if args.fetch:
            req=Request(cat['sourceUrl'],headers={'User-Agent':'AmericanEnglishLab-PrivateResearch/1.0'})
            with urlopen(req,timeout=25) as res:
                if res.status!=200:raise RuntimeError(f'{key}: HTTP {res.status}')
                html=res.read(2_500_000).decode('utf-8','replace')
        else:
            html=(args.html_dir/f'{key}.html').read_text(encoding='utf-8')
        lesson, row=stage_one(cat,li,html)
        (STAGED/f'{key}.json').write_text(json.dumps(lesson,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        lessons.append(lesson); report.append(row)
    (STAGED/'source-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if args.apply:
        blockers=[x for x in report if x['warnings'] or not all(q['foundInTranscript'] for q in x['questions'])]
        if blockers:raise RuntimeError(f'Blocked: {len(blockers)} sources have unchecked lines/evidence. Resolve manually first.')
        existing={x['id'] for x in authentic}
        if existing.intersection({x['id'] for x in lessons}):raise RuntimeError('Transcript already imported; refusing duplicate')
        new_linked=[x for x in linked if x['catalogId'] not in IDS]
        for c in catalog:
            if c['id'] in IDS:
                li=link_by[c['id']]
                c.update(integrationStatus='interactive_transcript_quiz', interactiveLessonId=li['id'],
                         transcriptImported=True,audioPlayback='Publisher MP3 source page; playback unverified', audioBundled=False)
                c.pop('linkedQuizId',None)
        assert len(authentic)+len(new_linked)==40 and len(catalog)==50
        assert sum(len(x['questions']) for x in authentic+lessons+new_linked)==204
        for path, value in [(CATALOG,catalog),(LINKED,new_linked),(AUTHENTIC,authentic+lessons)]:
            path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print('Applied 10 original-source transcripts; physical audio QA still NOT completed')
    else:
        print('Staged 10 publisher pages. NOT imported; human line/rights check required.')
    print(json.dumps({'rows':len(report),'warnings':sum(bool(x['warnings']) for x in report),
                      'allQuizEvidenceMatched':all(all(q['foundInTranscript'] for q in x['questions']) for x in report)},indent=2))

if __name__=='__main__':main()
