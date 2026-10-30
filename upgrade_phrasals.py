"""Editorially authored sense definitions and 45 additional advanced phrasal verbs.
Run once on existing data, safe to run again. Original sentences written for this project.
No copying from proprietary dictionaries.
"""
from pathlib import Path
import json, re
p=Path(__file__).resolve().parents[1]/'data'/'phrasals.json'
data=json.loads(p.read_text(encoding='utf-8'))
# English language definitions of the specific senses taught by each original card.
defs={
'figure out':'To understand something by thinking or examining the evidence.',
'come across':'To find or meet something or someone unexpectedly.',
'come up with':'To think of or produce an idea, plan, or solution.',
'deal with':'To take action to manage a problem or situation.',
'get over':'To recover emotionally or physically from a difficult experience.',
'get by':'To manage a situation with only the resources available.',
'give up':'To stop trying or abandon an activity or goal.',
'bring up':'To introduce a topic for people to discuss.',
'point out':'To draw attention to a particular fact or detail.',
'look into':'To investigate something to discover more information.',
'turn down':'To reject an offer, request, or opportunity.',
'put off':'To postpone an event or action until a later time.',
'work out':'To find an answer or reach a satisfactory solution.',
'take on':'To accept a task, responsibility, or challenge.',
'carry out':'To perform or complete a plan, order, or piece of work.',
'make up for':'To compensate for something negative or missing.',
'set aside':'To save or reserve time, money, or resources for a purpose.',
'follow through on':'To finish doing something that you promised or planned.',
'keep up with':'To move, learn, or progress at the same rate as someone or something.',
'catch up on':'To do or learn something that you have missed or fallen behind on.',
'run into':'To meet someone unexpectedly or encounter an unplanned difficulty.',
'end up':'To finally be in a particular situation, often unexpectedly.',
'break down':'To stop functioning because of a mechanical or technical problem.',
'back up':'To support a person or a claim with help or evidence.',
'fall behind':'To fail to make progress at the expected rate.',
'cut back on':'To reduce the amount of something used or spent.',
'stick to':'To continue following a plan, agreement, or decision.',
'speak up':'To express an opinion or concern more openly or loudly.',
'pay off':'To produce a worthwhile result after effort or investment.',
'go over':'To examine or review information carefully.',
'get around to':'To finally find the time to do a delayed task.',
'break out':'To begin suddenly, especially an unpleasant event.',
'take off':'To become successful or popular very quickly.',
'hold back':'To prevent someone or something from moving or progressing.',
'narrow down':'To reduce a list of possibilities to a smaller number.',
'rule out':'To decide that an option or explanation is not possible.',
'call off':'To cancel an event or plan before it happens.',
'step down':'To leave an important job or position voluntarily.',
'look up to':'To respect and admire someone.',
'bring about':'To make a change or situation happen.',
'account for':'To explain why something happened or how it is calculated.',
'act on':'To do something because of information or advice.',
'add up':'To make sense or appear reasonable when considered together.',
'back down':'To withdraw a demand or claim after opposition.',
'bear out':'To confirm that an idea or statement is true.',
'blow up':'To make a problem or disagreement seem much more serious.',
'boil down to':'To have one central cause or essential meaning.',
'branch out':'To expand into a different activity or field.',
'break into':'To enter a place by force and without permission.',
'brush up on':'To practice a skill to improve or refresh it.',
'build up':'To increase or develop something gradually.',
'call for':'To require a particular response, measure, or action.',
'catch on':'To begin to understand an idea or how something works.',
'check in on':'To contact or visit someone to see how they are doing.',
'come down to':'To depend ultimately on one central factor.',
'count on':'To rely on someone or something to be dependable.',
'cut off':'To stop the supply, access, or connection to something.',
'draw on':'To use experience, knowledge, or resources for a purpose.',
'drop by':'To visit someone or somewhere briefly without a formal appointment.',
'fall apart':'To break into pieces or lose stability or organization.',
'fill in for':'To temporarily do another person’s job or duties.',
'get across':'To communicate an idea so that other people understand it.',
'get away with':'To do something wrong without receiving the expected punishment.',
'give in':'To stop resisting pressure or demands.',
'lay out':'To explain a proposal or arrangement clearly and in detail.',
'leave out':'To omit something from a group, plan, or explanation.',
'look back on':'To think about an earlier experience from a later perspective.',
'opt out of':'To choose not to participate in something.',
'pass up':'To decide not to accept an opportunity.',
'phase out':'To gradually stop using or providing something.',
'pick up on':'To notice a detail or signal that others might miss.',
'pull off':'To succeed in doing something difficult or unlikely.',
'set out':'To begin a journey with a particular destination or goal.',
'sort out':'To organize something or resolve a confusing problem.',
'stand out':'To be noticeably different from others in a positive or striking way.',
'take after':'To resemble an older relative in appearance or behavior.',
'talk over':'To discuss an issue thoroughly before making a decision.',
'think through':'To consider all the likely consequences before acting.',
'turn out':'To happen or develop in a particular way.',
'wrap up':'To finish a meeting, task, or discussion.',
'zero in on':'To focus attention very closely on one target or issue.',
}
# Word / TR gloss / definition / example / syntax / CEFR editorial tag.
# No template-based auto-generated meanings: every new sense is authored separately.
new=[
('iron out','pürüzleri gidermek','To resolve small differences or problems through discussion.','We need to iron out a few details before signing.','separable','B2'),
('map out','ayrıntılı planlamak','To plan a process or route carefully, step by step.','They mapped out the next six months of training.','separable','B2'),
('weigh up','artı ve eksilerini tartmak','To consider different advantages and disadvantages before deciding.','She weighed up the risks before changing careers.','separable','B2'),
('check up on','durumunu araştırmak','To check that someone or something is safe or doing well.','I called to check up on my grandmother.','inseparable','B2'),
('open up about','içini dökmek','To start speaking honestly about private feelings or experiences.','He opened up about the pressure he felt.','inseparable','B2'),
('shy away from','çekinmek','To avoid something because it feels unpleasant or intimidating.','Do not shy away from asking for help.','inseparable','B2'),
('get ahead','ilerlemek','To make progress in work or life.','Learning to negotiate helped her get ahead.','intransitive','B2'),
('hold on to','elinde tutmak','To keep something instead of giving it away or losing it.','Hold on to the receipt until you get a refund.','inseparable','B2'),
('look out for','göz kulak olmak','To watch carefully for someone or something.','Look out for cyclists at this intersection.','inseparable','B2'),
('reach out to','iletişime geçmek','To contact someone to ask, offer support, or start a discussion.','She reached out to an old friend after moving.','inseparable','B2'),
('sum up','özetlemek','To express the central points briefly.','Could you sum up the proposal in two sentences?','separable','B2'),
('settle for','daha azıyla yetinmek','To accept a less desirable option than the one hoped for.','He did not want to settle for a temporary fix.','inseparable','B2'),
('make do with','eldekiyle idare etmek','To manage with what is available, despite its limitations.','We made do with one laptop during the trip.','inseparable','B2'),
('slip up','hata yapmak','To make a small mistake, often through carelessness.','I slipped up while reading the final number.','intransitive','B2'),
('get through','zorlu bir şeyi atlatmak','To successfully survive or finish a difficult experience.','The family got through a very challenging year.','inseparable','B2'),
('move on from','geride bırakmak','To stop dwelling on a past experience and continue with life.','She was ready to move on from the disagreement.','inseparable','B2'),
('stand up for','savunmak','To defend a person, belief, or principle.','It is important to stand up for your values.','inseparable','B2'),
('turn to','yardım için başvurmak','To seek advice, help, or comfort from someone.','He turned to his neighbor for advice.','inseparable','B2'),
('take up','başlamak','To begin a hobby or regular activity.','She took up hiking during the summer.','separable','B2'),
('come around to','fikrini değiştirmek','To gradually change your opinion and accept an idea.','He eventually came around to the new plan.','inseparable','B2'),
('put up with','katlanmak','To tolerate an unpleasant situation without taking action.','I cannot put up with the noise any longer.','inseparable','B2'),
('step up','çabayı artırmak','To increase effort or take more responsibility.','Local volunteers stepped up during the emergency.','intransitive','B2'),
('check out','incelemek','To examine something to see whether it is interesting or useful.','Check out the new exhibit this weekend.','separable','B2'),
('turn around','iyileştirmek','To improve a failing situation or organization.','The coach turned the team around after a difficult season.','separable','B2'),
('hold off on','erteleme kararı almak','To delay doing something until conditions improve.','Let us hold off on booking until prices settle.','inseparable','B2'),
('come through','zor anda yardım etmek','To provide needed support or achieve a result when it matters.','Our neighbors came through when we needed a ride.','intransitive','B2'),
('follow up on','takip ederek sonuçlandırmak','To take additional action on an earlier request or discussion.','I will follow up on your question tomorrow.','inseparable','B2'),
('get the hang of','mantığını kavramak','To learn how to do something through practice.','It took me a few days to get the hang of the controls.','inseparable','B2'),
('talk into','ikna etmek','To persuade someone to do something.','They talked me into joining the weekend trip.','separable','B2'),
('talk out of','vazgeçirmek','To persuade someone not to do something.','My friend talked me out of buying an expensive gadget.','separable','B2'),
('walk away from','vazgeçip ayrılmak','To leave a deal or situation rather than continue it.','She walked away from an unfair agreement.','inseparable','B2'),
('kick off','başlatmak','To start an event, project, or activity.','We will kick off the workshop with a short discussion.','separable','B2'),
('turn in','teslim etmek','To submit a completed assignment or document.','Please turn in the forms by Friday.','separable','B2'),
('hold up','geciktirmek','To cause a delay in a process or journey.','Heavy traffic held up the delivery.','separable','B2'),
('carry on','devam etmek','To continue doing something despite a difficulty.','She carried on studying after a short break.','intransitive','B2'),
('chime in','sohbete katılmak','To join a conversation by adding a remark.','Several listeners chimed in with their own stories.','intransitive','C1'),
('flesh out','detaylandırmak','To add useful detail to an incomplete idea or plan.','The team fleshed out the outline before presenting it.','separable','C1'),
('home in on','odaklanmak','To focus attention or movement on a specific target.','The discussion homed in on the central disagreement.','inseparable','C1'),
('play down','önemsiz göstermek','To make a risk or problem seem less important than it is.','The official played down the potential impact.','separable','C1'),
('play up','abartarak vurgulamak','To emphasize a feature or issue to make it seem significant.','The campaign played up the benefits and ignored the costs.','separable','C1'),
('run counter to','ters düşmek','To conflict with a principle, expectation, or trend.','The proposal runs counter to the stated goals.','inseparable','C1'),
('skirt around','konuya girmemek','To avoid directly discussing a difficult or sensitive subject.','He kept skirting around the real question.','inseparable','C1'),
('spell out','açıkça anlatmak','To explain something very clearly and in detail.','The agreement spells out each party’s responsibilities.','separable','C1'),
('water down','etkisini azaltmak','To weaken an idea or proposal by making changes to it.','The committee watered down the original recommendations.','separable','C1'),
('weed out','ayıklamak','To identify and remove unwanted or unsuitable elements.','The editor weeded out repeated examples.','separable','C1'),
('wrestle with','üstesinden gelmekte zorlanmak','To struggle mentally with a difficult problem or choice.','She wrestled with whether to accept the offer.','inseparable','C1'),
('hinge on','bağlı olmak','To depend mainly on one particular factor.','The success of the plan hinges on public trust.','inseparable','C1'),
('pan out','beklendiği gibi sonuçlanmak','To develop or succeed in a particular way over time.','We will see how the experiment pans out.','intransitive','C1'),
('phase in','kademeli devreye almak','To introduce a new system gradually.','The school will phase in the policy next semester.','separable','C1'),
('reel off','ard arda sıralamak','To say a long series of facts or names quickly.','She reeled off five reasons without looking at her notes.','separable','C1'),
('single out','özellikle seçmek','To select one person or thing from a group for special attention.','The report singled out two areas for improvement.','separable','C1'),
('stave off','önüne geçmek','To prevent or delay something unpleasant from happening.','Early action helped stave off a larger crisis.','separable','C1'),
('taper off','giderek azalmak','To become gradually smaller, weaker, or less frequent.','Attendance tapered off toward the end of the season.','intransitive','C1'),
('bear down on','baskı kurmak','To put intense pressure on a person, group, or process.','Deadlines were bearing down on the team.','inseparable','C1'),
('clamp down on','sert önlem almak','To take strict action to stop an activity.','Officials clamped down on fraudulent sales.','inseparable','C1'),
('double down on','ısrarla sürdürmek','To increase commitment to a course of action despite criticism.','The company doubled down on its long-term strategy.','inseparable','C1'),
('drum up','destek toplamak','To try actively to attract interest, support, or business.','The organizers drummed up support for the event.','separable','C1'),
('edge out','az farkla geçmek','To defeat someone narrowly or gain a slight advantage.','The local team edged out its rivals in the final.','separable','C1'),
]
for v in data:
    assert v['word'] in defs, f"Missing authored English definition: {v['word']}"
    v['definition']=defs[v['word']]
    # Existing cards tagged only as curriculum; give provisional per-item target by the editorial C1 rare set.
    c1={'follow through on','make up for','get around to','bear out','boil down to','branch out','draw on','opt out of','phase out','pull off','zero in on','bring about','account for','pick up on','act on','back down'}
    v['level']='C1' if v['word'] in c1 else 'B2'
    v['editorialStatus']='authored_unreviewed'
existing={x['word'] for x in data}
for w,tr,d,example,syntax,level in new:
    if w in existing: continue
    assert w not in defs
    data.append({'id':'pv-'+re.sub('[^a-z0-9]+','-',w).strip('-'), 'word':w,'tr':tr,'definition':d,'example':example,'level':level,'syntax':syntax,'register':'neutral','note':{'separable':'The object can come between the verb and its particle when appropriate.','inseparable':'Keep the object after the complete phrase.','intransitive':'No direct object is required for the taught sense.'}[syntax],'priority':50+len(data),'senses':[{'tr':tr,'example':example,'definition':d}],'editorialStatus':'authored_unreviewed'})
for v in data:
    for s in v.get('senses',[]):
        if 'definition' not in s and s.get('tr')==v['tr']:
            s['definition']=v['definition']
data.sort(key=lambda x:(x['priority'],x['word']))
assert len(data)==len({x['word'] for x in data})
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Now',len(data),'phrasals; every entry has a concrete English definition. Editorial review still required.')
