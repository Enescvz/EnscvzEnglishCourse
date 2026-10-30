#!/usr/bin/env python3
"""Add independently worded second examples for 33 older phrasal drafts.

Never overwrites the original example or grants editorial approval. Idempotent.
"""
import json
from pathlib import Path
from promote_content_batch import ROOT

SECOND = {
 'carry on':'Even when the power went out, they carried on with the game.',
 'chime in':'Feel free to chime in if you have a better suggestion.',
 'set out':'They set out for the beach just after breakfast.',
 'flesh out':'Could you flesh out your idea with a few more practical details?',
 'sort out':'We need to sort out who is picking the kids up tonight.',
 'home in on':'After a few guesses, she homed in on the right answer.',
 'play down':'He tried to play down how nervous he felt before the interview.',
 'stand out':'That bright yellow door really stands out on the street.',
 'play up':'The salesperson played up the extra features of the phone.',
 'run counter to':'Leaving early would run counter to our original agreement.',
 'skirt around':'Stop skirting around the issue and tell me what happened.',
 'take after':'His daughter takes after him when it comes to cooking.',
 'spell out':'Can you spell out exactly what you need by Friday?',
 'water down':'Adding too much ice will water down your drink.',
 'talk over':'We talked the travel budget over before booking anything.',
 'weed out':'The coach weeded out the duplicate names on the roster.',
 'think through':'I need another day to think through all my options.',
 'wrestle with':'They wrestled with how to handle the sudden change.',
 'hinge on':'Whether we go hiking tomorrow hinges on the weather.',
 'pan out':'Our last-minute weekend plans panned out surprisingly well.',
 'turn out':'The homemade pizza turned out great, even without a recipe.',
 'phase in':'They will phase in the new parking rules over three months.',
 'reel off':'He reeled off the names of all the streets he remembered.',
 'wrap up':'We should wrap up this call before the next meeting starts.',
 'single out':'The teacher singled out her essay for special praise.',
 'zero in on':"Let's zero in on the one thing causing the delay.",
 'stave off':'A short snack helped stave off hunger until dinner.',
 'taper off':'The rain gradually tapered off in the late afternoon.',
 'bear down on':'The storm was bearing down on the coastal towns.',
 'clamp down on':'The building manager clamped down on overnight noise.',
 'double down on':'After a slow start, she doubled down on her training.',
 'drum up':'They used social media to drum up interest in the event.',
 'edge out':'The newcomer edged out the favorite by just one point.',
}

def run():
    bank=ROOT/'data/phrasals.json'
    rows=json.loads(bank.read_text(encoding='utf8'))
    missing={x['word'] for x in rows if len(x.get('examples',[]))<2}
    if missing-set(SECOND):raise ValueError(f'Uncovered phrases: {missing-set(SECOND)}')
    changed=0
    for row in rows:
        word=row['word']
        if word not in missing:continue
        other=SECOND[word]
        if other == row['example'] or len(other)<25:
            raise ValueError(f'Bad second sentence for {word}')
        if row['examples'] != [row['example']]:
            raise ValueError(f'Unexpected legacy examples for {word}')
        row['examples'].append(other)
        if row.get('editorialStatus')=='approved':raise ValueError('Would touch approved lesson')
        changed+=1
    if changed: bank.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'addedSecondExamples':changed,'remainingSingleExamplePhrasals':sum(len(x.get('examples',[]))<2 for x in rows),'released':False},indent=2))
    return changed

if __name__=='__main__':run()
