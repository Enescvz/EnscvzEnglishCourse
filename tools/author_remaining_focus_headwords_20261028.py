#!/usr/bin/env python3
"""Finish the last 17 source-headword-only focus targets with original contexts.
Level/meaning editorial verification remains outstanding.
"""
import json
import tempfile
from pathlib import Path
from promote_content_batch import process
ROOT=Path(__file__).resolve().parents[1]
ROWS='''
degrading|aşağılayıcı, küçük düşürücü|Treating someone in a way that takes away their dignity or self-respect.|Being shouted at in front of customers was a degrading experience.|Nobody should have to accept degrading treatment at work.
dispensary|revir, ilaç dağıtım merkezi|A place where medicines or basic medical supplies are provided.|The camp has a small dispensary for minor injuries.|Visitors can collect their prescribed medicine at the dispensary.
elaboration|ayrıntılı açıklama, detaylandırma|Additional details that explain an idea or statement more fully.|Your plan sounds interesting, but it needs some elaboration.|She offered a brief elaboration on why the date had changed.
estimation|tahmin, yaklaşık hesap|An approximate calculation or judgment made from available information.|My estimation of the travel time was far too optimistic.|The contractor gave us an estimation of the repair costs.
extravagance|savurganlık, aşırı harcama|Spending or behavior that goes far beyond what is necessary or reasonable.|They decided that another expensive vacation would be an extravagance.|He regretted the extravagance of buying things he never used.
fatality|ölümle sonuçlanan olay, can kaybı|A death caused by an accident, disaster, or other serious event.|The highway accident resulted in one fatality.|Safety improvements helped reduce fatalities on the road.
ferocious|vahşi, çok şiddetli|Extremely fierce, violent, or intense in force or behavior.|A ferocious storm kept everyone inside all evening.|The dog looked ferocious but was actually very gentle.
harass|taciz etmek, sürekli rahatsız etmek|To repeatedly bother, threaten, or pressure someone in an unwelcome way.|Strangers began to harass her with unwanted phone calls.|Nobody should harass someone for expressing a different opinion.
harassment|taciz, ısrarlı rahatsız etme|Repeated unwanted behavior that makes another person feel unsafe or upset.|She reported the online harassment to the platform.|The apartment building has rules against harassment of neighbors.
marginally|çok az, küçük bir farkla|By a small amount or to a limited degree.|The second apartment is marginally more expensive.|His pronunciation sounded marginally better after a week of practice.
monotony|tekdüzelik, sürekli aynı olma|A lack of variety that makes a routine feel dull and repetitive.|A weekend trip helped break the monotony of daily life.|She listens to podcasts to escape the monotony of her commute.
neutralize|etkisiz hâle getirmek, nötrleştirmek|To stop something from having an effect or cancel its influence.|A little lemon juice can help neutralize the strong flavor.|The new filters are designed to neutralize unpleasant odors.
numb|uyuşmuş, hissiz|Unable to feel something normally, physically or emotionally.|My fingers went numb while I waited outside in the cold.|She felt numb after hearing the unexpected news.
obscurely|belirsiz biçimde, anlaşılması güç şekilde|In a way that is difficult to understand or not clearly expressed.|The instructions were written so obscurely that nobody could follow them.|He explained the rule obscurely instead of giving a simple example.
plausibly|makul biçimde, inandırıcı şekilde|In a way that seems reasonable or could be believed.|She plausibly explained why her train was delayed.|The missing keys could plausibly have been left at the cafe.
posture|duruş, bedenin duruş biçimi|The position in which you hold your body while sitting or standing.|My posture improves when I raise the laptop screen.|The instructor reminded us to check our posture while stretching.
psyche|ruh, zihinsel yapı|The thoughts, feelings, and mental characteristics of a person.|That childhood memory left a lasting mark on his psyche.|The documentary explores how isolation affects the human psyche.
'''.strip()

def make():
    out=[]
    for n,line in enumerate(ROWS.splitlines(),1):
        cells=[s.strip() for s in line.split('|')]
        if len(cells)!=5:raise ValueError(f'bad source row {n}')
        word,tr,definition,e1,e2=cells
        out.append({'word':word,'level':'C1','tr':tr,'definition':definition,'example':e1,'examples':[e1,e2],
                    'levelStatus':'source_candidate_unreviewed','prompt':f'Use “{word}” in a natural sentence.'})
    return out

def apply():
    out=make()
    current=json.loads((ROOT/'data/fluency-focus.json').read_text())
    pending={x['word'] for x in current['vocabulary'] if x['status']=='headword_only'}
    if pending and pending!={x['word'] for x in out}:raise ValueError(f'headword shortlist changed: {sorted(pending)}')
    orig=json.loads((ROOT/'data/vocabulary.json').read_text())
    existing={x['word'] for x in orig if x.get('category')=='general'}
    new=[x for x in out if x['word'] not in existing]
    target=ROOT/'sources/authored-20261028-remaining-focus-headwords.jsonl'
    target.write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out),encoding='utf8')
    if new:
        with tempfile.NamedTemporaryFile('w',suffix='.jsonl',encoding='utf8',delete=False) as f:
            tmp=Path(f.name)
            f.write(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in new))
        try:result=process(tmp,'general',apply=True)
        finally:tmp.unlink(missing_ok=True)
    else:result={'validatedNewCards':0,'mode':'noop'}
    print(json.dumps({'authored':len(out),'import':result},ensure_ascii=False))
if __name__=='__main__':apply()
