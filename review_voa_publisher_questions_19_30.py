#!/usr/bin/env python3
"""Audit source-grounded linked quizzes L2 19-30 against 2026-10-28 manual
reading of VOA original Conversation pages. This does NOT import full transcripts,
validate actual audio, or certify passage timestamp/playback. Safe and idempotent.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'voa-source-quizzes.json'
CATALOG=ROOT/'data'/'voa-source-catalog.json'
PROOF=ROOT/'qa'/'source-reviews'/'voa-l2-19-30-evidence-20261028.json'
REVIEW_DATE='2026-10-28'
# (VOA HTML Conversation text role, literal short publisher excerpt, visible
# publisher page text line, kind). The page line is a *review locator*, not a
# timestamp or immutable VOA paragraph ID. Stage directions are not spoken.
EVIDENCE={
19:[('Pete','I love when people are quiet.',160,'speech'),('Professor Bot','indirect questions are more polite',141,'speech'),('Anna',"There's still a lot of milkshake",172,'speech'),('Stage direction','drops it under the seat',226,'stage_direction')],
20:[('Anna','Welcome to the Washington Car Show!',122,'speech'),('Anna','She said that we need to show lots of cars.',116,'speech'),('Robot','What an effort to robot dance.',158,'speech'),('Stage direction','Kurt, the stunt driver, does the driving.',175,'stage_direction')],
21:[('Anna','He has a birthday coming up!',126,'speech'),('Ashley','Tanglewood Works.',135,'speech'),('Anna','I’m getting him a present.',134,'speech'),('Anna','I’ll rent him a clown!',137,'speech')],
22:[('Sue','and a broken toy.',124,'speech'),('Anna','This net said to me',118,'speech'),('Sue','garbage.',127,'speech'),('Sue','a clean shoe box.',137,'speech')],
23:[('Ms. Weaver','interviewing musician Emma G.',121,'speech'),('Anna','a video scrapbook of our friendship.',148,'speech'),('Emma G','Austin, Texas.',155,'speech'),('Emma G','teaching at a music camp in Chicago.',159,'speech')],
24:[('Anna','big superhero convention.',117,'speech'),('Young Man','I’d rather be born a superhero.',126,'speech'),('Prof. Bot','Anna was just hit by lightning.',137,'speech'),('Prof. Bot','had better to give advice.',139,'speech')],
25:[('Announcer','cannot walk through walls.',118,'speech'),('Lightning Bolt Lady','Super-speed walking is definitely one of my superpowers.',147,'speech'),('Stage direction','it turns into ashes.',163,'stage_direction'),('Announcer','past perfect continuous.',125,'speech')],
26:[('Anna','someone who looks just like you.',114,'speech'),('Pete','a woman who looks just like you.',121,'speech'),('Pete','career consultant.',124,'speech'),('Anna','We have to give her a chance.',127,'speech')],
27:[('Anna','My friend has invited me to her houseboat.',120,'speech'),('Fanny','How about you give Anna a tour',146,'speech'),('Phoenix','we really had to downsize!',161,'speech'),('Phoenix','We’re floating on water.',166,'speech')],
28:[('Kelly','Great City Bird Count!',115,'speech'),('Anna','10 ice cream trucks',132,'speech'),('Kelly','put it on the official form.',137,'speech'),('Anna','left his briefcase at the ice cream truck!',160,'speech')],
29:[('Anna','Ms. Weaver named me fire safety monitor.',116,'speech'),('FF H','Test it monthly',156,'speech'),('FF H','Always use the stairs.',169,'speech'),('FF J','The air is clearer close to the ground.',173,'speech')],
30:[('Anna',"I'm dying??",133,'speech'),('Nurse','she won’t be able to make it ... to graduation.',143,'speech'),('Ashley','I would love to be a dog trainer.',122,'speech'),('Jonathan','win the World Karaoke Contest.',159,'speech')]
}
# Some excerpts cover only the core factual fact. Review URL/context for the
# question as a whole; no machine verdict is given on every distractor.
NOTES={20:{1:'VOA line 116 contains the complete three-part instruction: show cars, interview people, have fun.',3:'The driver identity appears only in a stage direction; this is not spoken audio evidence.'},
19:{3:'Under-seat location comes from a stage direction; the speaker says the phone was dropped.'},
22:{1:'The objects being imagined as talking include a net, helmet, and toy.'},
23:{'license':'The publisher page reproduces an excerpt from a third-party commercial song. Lyrics must not be imported or bundled.'},
24:{2:'The fact is described by Professor Bot; no sound-time matching was done.'},
25:{2:'The phone turning to ashes is stage direction, not spoken dialogue.'},
27:{1:'Fanny asks Phoenix to give Anna a tour; Phoenix accepts.'},
30:{0:'Question implies Anna misheard the nurse; nurse confirms that the test relates to her student.'}}

def write(path,obj): path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run():
    data=json.loads(DATA.read_text(encoding='utf-8'))
    catalog=json.loads(CATALOG.read_text(encoding='utf-8'))
    ids=[x['id'] for x in data]; raw=[json.dumps([(q['question'],q['options'],q['answer']) for q in x['questions']],ensure_ascii=False) for x in data]
    bycat={c['id']:c for c in catalog}
    proofs=[]
    for lesson_no,excerpts in EVIDENCE.items():
        lid=f'voa-linked-2-{lesson_no:02d}'
        item=next((x for x in data if x['id']==lid),None)
        promoted=item is None
        if promoted:
            # Completed full transcript with exactly the same original progress ID.
            item=next(x for x in json.loads((ROOT/'data'/'authentic-listening.json').read_text()) if x['id']==lid)
        cat=bycat[f'voa-2-{lesson_no:02d}']
        assert len(excerpts)==len(item['questions'])==4
        assert item['sourceUrl']==cat['sourceUrl']
        assert item['audioBundled'] is False
        if not promoted:assert item['transcriptImported'] is False and item['playerVerified'] is False
        for i,((speaker,short,line,kind),q) in enumerate(zip(excerpts,item['questions'])):
            assert kind in ('speech','stage_direction')
            assert short and len(short.split())<=12 and line>=100
            assert 0<=q['answer']<len(q['options'])
            if not promoted:q.update({'sourceEvidence':short,'sourceEvidenceSpeaker':speaker,
                      'sourceEvidenceKind':kind,
                      'sourceEvidencePublisherLine':line,
                      'sourceEvidencePublisherUrl':item['sourceUrl'],
                      'sourceReviewStatus':'publisher_page_excerpt_reviewed_not_audio_verified'})
            proofs.append({'lessonId':lid,'questionIndex':i,'sourceUrl':item['sourceUrl'],
                           'speakerOrStage':speaker,'literalExcerpt':short,'webReviewLine':line,
                           'evidenceKind':kind,'reviewedDate':REVIEW_DATE,
                           'note':NOTES.get(lesson_no,{}).get(i,'Source page Conversation section; manually checked')})
        if not promoted:item['publisherConversationQuestionReview']=REVIEW_DATE
        if not promoted:item['questionEvidenceOnly']=True
        # Do not mark it as an in-app full transcript or imply human MP3 played.
        if not promoted:cat['questionSourceReview']='publisher_excerpt_verified_audio_unverified'
        if not promoted:cat['questionSourceReviewedOn']=REVIEW_DATE
    assert len(proofs)==48
    assert len(data)<=32 and len(data)>=20 and sum(len(x['questions']) for x in data)==len(data)*4
    assert ids==[x['id'] for x in data]
    assert raw==[json.dumps([(q['question'],q['options'],q['answer']) for q in x['questions']],ensure_ascii=False) for x in data]
    write(DATA,data);write(CATALOG,catalog)
    write(PROOF,{'reviewedAt':REVIEW_DATE,'scope':'12 official publisher page Conversation source excerpt checks; 48 quiz keys','notAudioVerified':True,
                'notFullTranscripts':True,'notIndependentEditorialSignoff':True,
                'thirdPartyCopyrightExclusion':['Lesson 23 commercial song lyrics','Lesson 30 lyric segments'],
                'externalVOASource':'https://learningenglish.voanews.com/p/6861.html',
                'reviews':proofs})
    return {'reviewedSourceLessons':len(EVIDENCE),'reviewedLinkedQuestions':len(proofs),'transcriptImportedByThisRun':0}
if __name__=='__main__':print(json.dumps(run(),indent=2))
