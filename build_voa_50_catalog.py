#!/usr/bin/env python3
"""Build a source-verified 50-item VOA listening discovery list.

DO NOT mistake a publisher page for a fully imported, QA-approved lesson.
Existing question/transcript imports remain authoritative in authentic-listening.json.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HOST='https://learningenglish.voanews.com'
L2=[
(1,'Budget Cuts','lets-learn-english-level-2-lesson1/3960391.html','Workplace rumors'),
(2,'The Interview','lets-learn-english-level-2-lesson-2/3960471.html','Interviews & teamwork'),
(3,'He Said - She Said','lets-learn-english-level-2-lesson-3/4027340.html','Different points of view'),
(4,'Run Away With the Circus!','lets-learn-english-level-2-lesson-4-run-away-with-the-circus/4034187.html','Agreeing & disagreeing'),
(5,'Greatest Vacation of All Time','lets-learn-english-level-2-lesson-5-greatest-vacation/4035571.html','Travel & telling stories'),
(6,'Will It Float?','lesson-6-will-it-float/4064553.html','Predictions & experiments'),
(7,'Tip Your Tour Guide','lesson-7-tip-your-tour-guide/4064769.html','Travel & giving advice'),
(8,'The Best Barbecue','lets-learn-english-level-2-lesson-8-best-barbecue/4073994.html','Food & opinions'),
(9,'Pets Are Family, Too!','lets-learn-english-level-2-lesson-9-pets-are-family-too/4074883.html','Pets & relationships'),
(10,'Visit to Peru','lets-learn-english-lesson-10-visit-to-peru/4079037.html','Travel plans'),
(11,'The Big Snow','lets-learn-english-level-2-lesson-11-the-big-snow/4102755.html','Weather & emergencies'),
(12,'Run! Bees!','lets-learn-english-level-2-lesson-12-run-bees/4139015.html','Nature & reactions'),
(13,'Save the Bees!','lets-learn-english-level-2-lesson-13-save-the-bees/4145716.html','Environment'),
(14,'Made for Each Other','lets-learn-english-level-2-lesson-14-made-for-each-other/4159000.html','Relationships'),
(15,'Before and After','lets-learn-english-level-2-lesson-15-before-after/4159057.html','Changes over time'),
(16,'Find Your Joy!','lets-learn-english-level-2-lesson-16/4198066.html','Hobbies & feelings'),
(17,'Flour Baby, Part 1','lets-learn-english-level-2-lesson-17/4220576.html','Responsibility'),
(18,'Flour Baby, Part 2','lets-learn-english-level-2-lesson-18/4231290.html','Responsibilities & consequences'),
(19,'Movie Night','lets-learn-english-level-2-lesson-19/4242927.html','Entertainment & plans'),
(20,'The Test Drive','lets-learn-english-level-2-lesson-20/4254704.html','Driving & decisions'),
(21,'Trash to Treasure, Part 1','lets-learn-english-level-2-lesson-21/4273059.html','Shopping & creativity'),
(22,'Trash to Treasure, Part 2','lets-learn-english-level-2-lesson-22/4283017.html','Shopping & making things'),
(23,'Rock Star','lets-learn-english-level-2-lesson-23/4287922.html','Music & interviews'),
(24,'I Feel Super!','lets-learn-english-level-2-lesson-24/4307612.html','Emotions & abilities'),
(25,'Only Human','lets-learn-english-level-2-lesson-25/4322773.html','Abilities & limitations'),
(26,'Look-alikes','lets-learn-english-level-2-lesson-26/4350607.html','Appearances & personality'),
(27,'Fish out of Water','lets-learn-english-level-2-lesson-27/4374632.html','Unfamiliar places'),
(28,'For the Birds','lets-learn-english-level-2-lesson-28/4396849.html','Nature & mysteries'),
(29,"Where There's Smoke...",'lets-learn-english-level-2-lesson-29/4423736.html','Safety & emergencies'),
(30,'Dream a Little Dream','lets-learn-english-level-2-lesson-30/4465315.html','Future plans & dreams'),
]
L1=[
(33,"Learning America's Sport",'lesson-33-learning-americas-sport/3555047.html','Sports'),
(34,'What Will I Do?','lets-learn-english-lesson-34-what-will-i-do/3566043.html','Career decisions'),
(35,"Let's Make Dinner!",'lets-learn-english-lesson-35-lets-make-dinner/3571922.html','Cooking'),
(36,'I Can Fix This!','lets-learn-english-lesson-36-i-can-fix-this/3568962.html','Fixing problems'),
(37,"Let's Agree to Disagree",'lets-learn-english-lesson-37-lets-agree-to-disagree/3574029.html','Opinions'),
(38,"She's My Best Friend!",'lets-learn-english-lesson-38-shes-my-best-friend/3591967.html','Friendship'),
(39,"It's Unbelievable!",'lets-learn-english-lesson-39-its-unbelieveable/3598920.html','Surprise & reactions'),
(40,'The Woods Are Alive','lets-learn-english-lesson-40-the-woods-are-alive/3630341.html','Travel & outdoors'),
(41,'Teamwork Works Best With a Team','lets-learn-english-lesson-41-teamwork/3635015.html','Collaboration'),
(42,'I Was Minding My Own Business','lets-learn-english-lesson-42-i-was-minding-my-own-business/3647264.html','Everyday situations'),
(43,'Time for Plan B','lets-learn-english-lesson-43-time-for-plan-b/3666458.html','Changing plans'),
(44,'Making Healthy Choices','lets-learn-english-lesson-44-making-healthy-choices/3688552.html','Shopping & choices'),
(45,'This Land is Your Land','lesson-45-this-land-is-your-land/3710209.html','Road trips'),
(46,'May I Borrow That?','lets-learn-english-lesson-46-may-i-borrow-that/3723588.html','Asking for help'),
(47,'How Can I Help?','lets-learn-english-lesson-47-how-can-i-help/3737352.html','Helping others'),
(48,'Have You Ever ...?','lets-learn-english-lesson-48-have-you-ever/3753664.html','Life experiences'),
(49,'Operation Spy!','lets-learn-english-lesson-49-operation-spy/3763537.html','Describing activities'),
(50,'Back to School','lets-learn-english-lesson-50-back-to-school/3771173.html','Education'),
(51,'A Good Habit','lets-learn-english-lesson-51-a-good-habit/3773577.html','Habits & routines'),
(52,'Taking Chances','lets-learn-english-lesson-52-taking-chances/3805454.html','Taking risks'),
]
existing=json.loads((ROOT/'data/authentic-listening.json').read_text(encoding='utf8'))
ready_by_url={v['sourceUrl']:v for v in existing}
previous_path=ROOT/'data/voa-source-catalog.json'
previous={x['id']:x for x in json.loads(previous_path.read_text(encoding='utf8'))} if previous_path.exists() else {}
rows=[]
for series,items in [('Level 2',L2),('Level 1',L1)]:
 for n,title,path,topic in items:
  url=f'{HOST}/a/{path}'
  ready=ready_by_url.get(url)
  rows.append(dict(
   id=f'voa-{2 if series=="Level 2" else 1}-{n:02d}',title=title,topic=topic,
   sourceSeries=f"Let's Learn English — {series}",sourceUrl=url,sourcePublisher='VOA Learning English',
   sourceIndex=f'{HOST}/p/{"6765" if series=="Level 2" else "5644"}.html',
   publisherTranscriptOnSourcePage=True,
   origin='VOA original-course page (confirm individual third-party segments before bundling)',
   speakingType='human_spoken_scripted_dialogue',
   levelGroup=series,learnerDifficulty='B1–B2 (approximate)' if series=='Level 2' else 'A2–B1 (approximate)',
   educationalRole='main_intermediate' if series=='Level 2' else 'optional_listening_warmup',
   integrationStatus='interactive_transcript_quiz' if ready else 'publisher_source_only',
   interactiveLessonId=ready['id'] if ready else None,
   audioPlayback='VOA MP3 linked; playback unverified' if ready else 'Open publisher page to hear audio/video; local MP3 not imported',
   transcriptImported=bool(ready),questionCount=len(ready['questions']) if ready else 0,
   audioBundled=False,sourcePageReviewed='2026-10-28',
   rightsUrl=f'{HOST}/p/6861.html',
  ))
# Preserve linked quizzes when rebuilding the source directory; a catalog rebuild must
# never silently demote a completed external questionnaire to a bare source link.
for row in rows:
 old=previous.get(row['id'],{})
 if not row['transcriptImported'] and old.get('linkedQuizId'):
  row.update(integrationStatus='source_linked_quiz',linkedQuizId=old['linkedQuizId'],
             questionCount=old['questionCount'])
assert len(rows)==50 and len({r['id'] for r in rows})==50
assert len({r['sourceUrl'] for r in rows})==50
assert sum(r['transcriptImported'] for r in rows)==len(existing)
(ROOT/'data/voa-source-catalog.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print('50 source pages; interactive=',sum(r['transcriptImported'] for r in rows),'source only=',sum(not r['transcriptImported'] for r in rows))
