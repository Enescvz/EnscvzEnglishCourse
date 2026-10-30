#!/usr/bin/env python3
"""Record 80 short source-page quote/line evidence locators for Level 1 33-52.

Publisher Conversation page text manually checked 2026-10-28, NOT audio-verified.
No transcript import, MP3 download, Speaking edit, card ID or quiz answer mutation.
When running on a new version, refuse to re-label an already promoted lesson.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUIZ = ROOT / 'data/voa-source-quizzes.json'
CAT = ROOT / 'data/voa-source-catalog.json'
REPORT = ROOT / 'qa/source-reviews/voa-l1-33-52-evidence-20261028.json'
DATE = '2026-10-28'
# Format: (speaker as printed by publisher, literal short excerpt, publisher page line)
# Line numbers are inspection locators in the publisher web rendering, not stable IDs.
EVIDENCE = {
33: [('Anna','I can teach children about baseball here!',196),('MINDY','I will try one more time, Anna.',192),('Anna','you really only need a bat, a ball and a glove.',201),('Anna','There are nine innings in a game.',214)],
34: [('Anna','I don’t have a costume. Can you help me?',198),('Genie','Dress as a genie!',200),('Rebecca','I study journalism.',227),('Anna','I’m a rock star!',272)],
35: [('Anna','I am doing the shopping.',180),('Marsha','this is the shopping list for breakfast.',208),('Marsha','on the refrigerator - for dinner!',208),('Marsha','They arrive in 30 minutes!',219)],
36: [('Anna','I put the flour inside the refrigerator.',186),('Anna','The eggs are inside the cabinet under the sink.',193),('Anna','peanut-butter-banana pancakes!',204),('Marsha','Hey, this tastes good!',210)],
37: [('Anna','Someone lost a bag.',179),('Phil',"I'm from a small town in the country.",192),('Anna','The city is exciting! It has more culture than the country.',201),('Anna',"Let's say \"hello!\" to people",215)],
38: [('Anna','My best friend from my hometown is coming here',180),('Anna','So, we split the rent.',197),('Anna','Time Traveling Treehouse.',212),('Penelope','We played in that old treehouse',213)],
39: [('Anna','I am tired of my untidy hair.',180),('Pete','I have the perfect product for you -- Hair Be Good!',190),('Pete','One can costs only $10!',191),('Anna','Hair Be Good did this to my hair.',225)],
40: [('Anna','Today I will audition for a show',180),('Director','you are speaking too softly.',195),('Director','you said that line really late.',209),('Anna',"I'm a tree.",232)],
41: [('Anna','Today my boss will tell me what she thinks of my work.',180),('Anna','I think the chart is upside down.',191),('Ms. Weaver','I want to see these numbers go up',203),('Anna','Look at all those cats!',219)],
42: [('Anna','I left work to get some lunch.',196),('Anna','Two robbers were grabbing her bag',199),('Anna','They didn’t pay.',235),('Anna','someone stepped on my arm!',228)],
43: [('Anna','I lost my wallet!',180),('Marsha','I have to give a big presentation in one hour.',191),('Jonathan',"I'm at the airport with my mother.",208),('Ashley',"I’m babysitting.",229)],
44: [('Anna','healthy food. So, I fight with myself.',188),('Ashley','go to the Giant supermarket.',190),('Junky','Mmm, ice cream!',220),('Healthy','Mmm, frozen peas!',222)],
45: [('Anna','My roommate Marsha and I will be on vacation at the same time.',180),('Anna','the Statue of Liberty!',190),('Marsha','don’t forget the Grand Canyon!',195),('Anna','The largest rocking chair in the world!',237)],
46: [('Marsha','Today is my birthday.',190),('Anna',"I don’t get my paycheck until next week.",196),('Anna','may I borrow your stapler?',198),('Anna','this is your own office supply hat!',229)],
47: [('Pete','I am fixing my car.',183),('Pete','So I took out the extra ones.',196),('Pete','Four hundred and fifty.',207),('Anna','I learned from a master.',222)],
48: [('Jean','I’ve just flown in from Boston.',184),('Jean','I want to see an unusual museum.',195),('Anna','I like the Sculpture Garden.',197),('Anna',"I've never been to D.C.’s zoo.",217)],
49: [('Anna','The International Spy Museum has created an amazing collection',180),('Anna','This is Agent Flamingo, reporting for duty.',184),('Anna',"It’s dark and small. I’m afraid of dark, small places.",198),('Ms. Weaver','have you ever cracked a code?',211)],
50: [('Anna','welcome to Georgetown University in Washington, D.C.!',180),('Taylor','waiting for about 10 minutes.',193),('Anna','going back to school makes me a little nervous.',208),('Anna','I think she said “giraffe.”',221)],
51: [('Ashley','I will run in my first marathon.',191),('Anna','I’ve been training for an hour',204),('Woman','this race is for children.',233),('Woman','raise money for sick children.',240)],
52: [('Kelly','she acted in my play, “The Woods Are Alive!”',185),('Anna','I will be acting in three movies.',198),('Anna','The second is a romantic comedy. And the third is an action movie.',202),('Anna','I’ll make the movies and then come back. Washington, D.C. is my home.',209)],
}
CAVEATS = {
    (40,2): 'İlk replik geç, sonraki replik erken söyleniyor; iki hata da kaynak metninde bulunuyor.',
    (42,3): 'Anna önce birinin koluna bastığını söylüyor; hikâyenin sonunda otomatla ilgili başka bir olay açığa çıkıyor. Soru Anna’nın ilk anlattığını soruyor.',
    (52,2): 'Metinde üç tür açıkça sıralanıyor: bilim kurgu, romantik komedi, aksiyon. Tarihî belgesel bu listede yok.',
}
NOTES = {
    (33,1): 'MINDY uses time travel to send Anna to the baseball field; relevant surrounding text lines 188–197.',
    (37,2): 'The same publisher line also explicitly lists museums, restaurants, theater, music and more jobs.',
    (40,2): 'The director first calls the line late, then the next attempt early (publisher lines 209–221).',
    (42,3): 'TRICK/TWIST: Anna says a bystander stepped on her arm, but the end shows a vending-machine incident. The existing question asks what she *says*, not the actual injury cause.',
    (45,0): 'Only VOA’s own original dialogue is reviewed; the separately credited Woody Guthrie song lyrics (lines 205–208) must be excluded from app imports.',
    (52,2): 'The full same publisher line names the complete three-genre list: science fiction, romantic comedy and action. A historical documentary is absent.',
}

def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', 'utf8')


def run():
    linked = json.loads(QUIZ.read_text('utf8'))
    catalog = json.loads(CAT.read_text('utf8'))
    by_id = {x['id']:x for x in linked}
    by_cat = {x['id']:x for x in catalog}
    before = [(x['id'], [(q['question'], q['options'][:], q['answer']) for q in x['questions']]) for x in linked]
    report=[]
    for no, entries in EVIDENCE.items():
        lesson_id = f'voa-linked-1-{no:02d}'
        lesson = by_id[lesson_id]
        catalog_item=by_cat[f'voa-1-{no:02d}']
        if lesson['sourceUrl'] != catalog_item['sourceUrl']:
            raise ValueError(f'Catalog URL differs from quiz for {lesson_id}')
        if len(lesson['questions']) != 4 or len(entries) != 4:
            raise ValueError(f'Wrong question count for {lesson_id}')
        if lesson.get('transcriptImported',False) or lesson.get('audioBundled',False) or lesson.get('playerVerified',False):
            raise ValueError(f'This excerpt-only source is already promoted/verified: {lesson_id}')
        for q_index, ((speaker,excerpt,line),q) in enumerate(zip(entries,lesson['questions'])):
            if not excerpt or not speaker or line < 150 or len(excerpt.split()) > 22:
                raise ValueError(f'Invalid evidence: {lesson_id} q{q_index}')
            if not (0 <= q['answer'] < len(q['options'])):
                raise ValueError(f'Invalid answer index: {lesson_id} q{q_index}')
            # Do not invent speaker-turn indexes for non-imported transcripts.
            assert 'sourceEvidenceTurn' not in q
            q.update({
                'sourceEvidence':excerpt,
                'sourceEvidenceSpeaker':speaker,
                'sourceEvidenceKind':'speech',
                'sourceEvidencePublisherLine':line,
                'sourceEvidencePublisherUrl':lesson['sourceUrl'],
                'sourceReviewStatus':'publisher_page_excerpt_reviewed_not_audio_verified'
            })
            if (no,q_index) in CAVEATS:
                q['sourceEvidenceCaveat']=CAVEATS[no,q_index]
            report.append({'lessonId':lesson_id,'questionIndex':q_index,'sourceUrl':lesson['sourceUrl'],
                          'speaker':speaker,'literalExcerpt':excerpt,'publisherWebLine':line,
                          'reviewedOn':DATE,'note':NOTES.get((no,q_index),'VOA Conversation page original transcript')})
        lesson['publisherConversationQuestionReview']=DATE
        lesson['questionEvidenceOnly']=True
        catalog_item['questionSourceReview']='publisher_excerpt_verified_audio_unverified'
        catalog_item['questionSourceReviewedOn']=DATE
    after = [(x['id'], [(q['question'], q['options'], q['answer']) for q in x['questions']]) for x in linked]
    if before != after or len(report)!=80 or len(linked)>32 or len(linked)<20 or len(catalog)!=50:
        raise ValueError('Question identity or data-count drift')
    dump(QUIZ,linked);dump(CAT,catalog)
    dump(REPORT,{'reviewedOn':DATE,'sourceSeries':"VOA Let's Learn English Level 1 33–52",
                 'countLessons':20,'countQuestions':80,'evidenceType':'publisher page short excerpt + rendered line locator',
                 'notFullTranscript':True,'notVerifiedAudioOrTiming':True,
                 'thirdPartyExcluded':['Lesson 45 Woody Guthrie This Land Is Your Land lyrics'],
                 'independentEditorialSignoff':False,'reviews':report})
    return {'reviewedLessons':20,'reviewedQuestions':80,'totalPublisherEvidenceQuestions':204,
            'integratedTranscripts':50-len(linked),'stillExternalOnly':len(linked),'audioVerified':False}

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
