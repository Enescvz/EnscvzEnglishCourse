#!/usr/bin/env python3
"""Idempotent VOA Level-2 lessons 25-30 source-transcript importer. Not an audio QA approval."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RIGHTS='https://learningenglish.voanews.com/p/6861.html'
SOURCES={
 25:{'page':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-25/4322773.html','audio':'https://voa-audio.voanews.eu/vle/2018/03/30/a591e14e-e65c-4370-91fb-06e8f9cad590_hq.mp3?download=1','duration':4.75,'stage':True},
 26:{'page':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-26/4350607.html','audio':'https://voa-audio.voanews.eu/vle/2018/04/25/3b556bb7-8c37-4c22-a390-d79b9f34fd24_hq.mp3?download=1','duration':5.0,'stage':False},
 27:{'page':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-27/4374632.html','audio':'https://voa-audio.voanews.eu/vle/2018/05/03/198277fc-1de6-487a-8196-dc808623e1b6_hq.mp3?download=1','duration':4.42,'stage':False},
 28:{'page':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-28/4396849.html','audio':'https://voa-audio.voanews.eu/vle/2018/05/17/48003699-cb0b-4cb7-8002-27bb38944ebf_hq.mp3?download=1','duration':4.90,'stage':False},
 29:{'page':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-29/4423736.html','audio':'https://voa-audio.voanews.eu/vle/2018/06/08/c954b93d-aacb-40b2-8c20-423d8c100045_hq.mp3?download=1','duration':4.57,'stage':False},
 30:{'page':'https://learningenglish.voanews.com/a/lets-learn-english-level-2-lesson-30/4465315.html','audio':'https://voa-audio.voanews.eu/vle/2018/07/06/931150ac-ddf3-42db-9247-b3ac4aec6180_hq.mp3?download=1','duration':4.87,'stage':False},
}
def parse_transcript(n):
 p=ROOT/f'sources/voa-reviewed-publisher/level2-{n:02d}.txt';out=[]
 for i,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
  if not line.strip():continue
  if '|' not in line:raise ValueError(f'Bad transcript: {p}:{i}')
  speaker,speech=(x.strip() for x in line.split('|',1))
  if not speaker or not speech:raise ValueError(f'Missing speaker or text: {p}:{i}')
  out.append({'speaker':speaker,'text':speech,'kind':'stage_direction' if speaker=='Stage direction' else 'speech'})
 if len(out)<40:raise ValueError(f'Transcript too short: {n}')
 return out

def apply():
 paths={key:ROOT/key for key in ['data/authentic-listening.json','data/voa-source-quizzes.json','data/voa-source-catalog.json','development-status.json']}
 data={key:json.loads(p.read_text(encoding='utf-8')) for key,p in paths.items()}
 full=data['data/authentic-listening.json'];linked=data['data/voa-source-quizzes.json'];catalog=data['data/voa-source-catalog.json'];status=data['development-status.json']
 done=0
 for number,meta in SOURCES.items():
  lid=f'voa-linked-2-{number:02d}'
  if any(x['id']==lid for x in full):continue
  item=next((x for x in linked if x['id']==lid),None)
  if not item or item['sourceUrl']!=meta['page']:raise ValueError(f'Official page mismatch: {lid}')
  turns=parse_transcript(number)
  questions=item['questions']
  for q in questions:
   speaker=q['sourceEvidenceSpeaker'].casefold();proof=q['sourceEvidence'].casefold()
   if q.get('sourceEvidenceKind')=='stage_direction':speaker='stage direction'
   hits=[i for i,t in enumerate(turns) if t['speaker'].casefold()==speaker and proof in t['text'].casefold()]
   if len(hits)!=1:raise ValueError(f'Evidence does not match exactly one turn: {lid} {q["question"]}: {hits}')
   q['sourceEvidenceTurn']=hits[0]
   q['sourceReviewStatus']='publisher_page_turn_reviewed_not_audio_verified'
  entry={
   'id':lid,'title':item['title'],'level':item['level'],'topic':item['topic'],
   'minutes':meta['duration'],'sourceUrl':meta['page'],'audioUrl':meta['audio'],
   'attribution':'VOA Learning English — publisher Conversation',
   'sourceSeries':"Let's Learn English — Level 2",
   'sourceLicense':'VOA original dialogue: public domain with attribution; third-party material excluded',
   'rightsUrl':RIGHTS,'audioProvider':'VOA Learning English',
   'audioType':'human_dialogue_source','audioAvailability':'external_online_stream_only',
   'audioBundled':False,'offlineReady':False,'transcriptSource':'VOA publisher Conversation page; text compared, audio not independently verified',
   'transcriptImported':True,'transcriptVerifiedAgainstAudio':False,'timingVerified':False,
   'quality':'external_source_not_independently_audio_reviewed','turns':turns,
   'questions':questions,'transcriptScope':('published_VOA_original_dialogue_with_exclusions' if number==30 else 'published_VOA_original_dialogue'),
   'transcriptRightsExclusion':('Third-party song lyrics omitted: rights not verified.' if number==30 else None),
  }
  cat=next(c for c in catalog if c['id']==item['catalogId'])
  cat.update({'integrationStatus':'interactive_transcript_quiz','interactiveLessonId':lid,
              'transcriptImported':True,'linkedQuizId':None,'audioBundled':False,
              'audioPlayback':'VOA original online MP3; playback unverified',
              'sourcePageReviewed':'2026-10-29'})
  full.append(entry);linked.remove(item);done+=1
 if done:
  assert len(full)+len(linked)==50
  assert len({x['id'] for x in full+linked})==50
  assert sum(len(x['questions']) for x in full+linked)==204
  status.update({'voaIntegratedPublisherTranscripts':len(full),'voaPublisherOnlyQuizzes':len(linked),
   'voaSpeakerTurnEvidenceQuestions':sum(q.get('sourceEvidenceTurn') is not None and q.get('sourceEvidenceKind')!='stage_direction' for l in full for q in l['questions']),
   'voaStageDirectionTurnEvidenceQuestions':sum(q.get('sourceEvidenceTurn') is not None and q.get('sourceEvidenceKind')=='stage_direction' for l in full for q in l['questions']),
   'voaTranscriptTurnEvidenceQuestions':sum('sourceEvidenceTurn' in q for l in full for q in l['questions']),
   'voaPublisherExcerptEvidenceQuestions':sum('sourceEvidence' in q and 'sourceEvidenceTurn' not in q for l in linked for q in l['questions'])})
  data['data/voa-source-quizzes.json']=linked
  for key,p in paths.items():p.write_text(json.dumps(data[key],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return done
if __name__=='__main__':print('Imported',apply())
