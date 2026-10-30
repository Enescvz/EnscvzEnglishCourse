from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'js/app.js';s=p.read_text()
def put(a,b):
 global s
 assert a in s,repr(a[:90]);s=s.replace(a,b,1)
put("import {filterCandidates} from './catalog.js';", "import {filterCandidates} from './catalog.js';\nimport {SKILL_AREAS,validateSentenceSkills,sentenceCloze,assessSkillInput,skillsDue,skillSummary,persistSkillReview} from './sentence-skills.js';")
put("['expressions','💬','Günlük Kalıplar'],", "['expressions','💬','Günlük Kalıplar'],['sentenceSkills','❓','Soru & Cümle Atölyesi'],")
put("toeflClozeIndex:null,toeflClozeResult:null};", "toeflClozeIndex:null,toeflClozeResult:null,skillArea:'question',skillLesson:null,skillIndex:0,skillOrder:[],skillFeedback:null};")
put("P.toeflWritingAttempts??=[];", "P.toeflWritingAttempts??=[];\nP.skillCards??={};P.skillHistory??=[];")
put("${button('Günlük kalıplar','goto','small soft','data-view=\"expressions\"')}", "${button('Günlük kalıplar','goto','small soft','data-view=\"expressions\"')}${button('❓ Soru Kurma Atölyesi','goto','small primary','data-view=\"sentenceSkills\"')}")
anchor='const pages={home,toefl,'
assert anchor in s
component=r'''function sentenceSkillsPage(){
 const curriculum=data.sentenceSkills;
 if(!curriculum)return `${section('Soru & Cümle Atölyesi','Dersler yüklenemedi.')}`;
 const all=curriculum.lessons;
 const area=SKILL_AREAS[ui.skillArea]?ui.skillArea:'question';
 const summary=skillSummary(curriculum,P);
 const counts=Object.keys(SKILL_AREAS).map(key=>({key,count:all.filter(l=>l.area===key).length}));
 const due=skillsDue(curriculum,P);
 const areaButtons=counts.map(({key,count})=>button(`${SKILL_AREAS[key]} (${count})`,'skillArea',area===key?'small primary':'small soft',`data-value="${E(key)}"`)).join('');
 const overview=`${section('Question & Sentence Builder','Soru kurma, edat, bağlaç ve doğal cümle kullanımı. 34 ders, 340 özgün alıştırma.','B1 → B2 · ORIGINAL PRIVATE CURRICULUM')}
 <div class="grid metrics">${metric('❓',String(all.length),'Beceri dersi')}${metric('✍',String(summary.total),'Özgün alıştırma')}${metric('✓',String(summary.practiced),'Denendi')}${metric('↻',String(summary.due),'Tekrar zamanı gelen')}</div>
 <div class="callout" style="margin-top:18px"><b>Öğrenme yöntemi</b><p>2 sıralama + 4 boşluk tamamlama + 4 serbest cümle/aktarım görevi. Serbest yanıtları otomatik doğru/yanlış diye puanlamıyoruz. Model cevapla karşılaştırıp kendin değerlendiriyorsun. Editör onayı bekliyor; CEFR sertifikasyonu veya resmî TOEFL puanı değildir.</p></div>
 <div class="row" style="margin:16px 0">${areaButtons}${due.length?button(`↻ ${due.length} gecikmiş / zamanı gelen`, 'skillDue','small primary'):''}</div>`;
 const lesson=all.find(x=>x.id===ui.skillLesson);
 if(!lesson){
  const windows=summary.windows.map(w=>`<div class="daily-item"><strong>${w.days} günlük bağımsız geri çağırma</strong><span class="mini">${w.observed} gözlem${w.rate===null?' · henüz ölçüm yok':' · %'+w.rate+' model yanıt eşleşmesi'}</span></div>`).join('');
  return `${overview}<div class="grid">${all.filter(l=>l.area===area).map(l=>{const tried=l.exercises.filter(e=>P.skillCards[e.id]).length;return `<div class="panel span-6"><div class="row between"><strong>${E(l.title)}</strong><span class="tag green">${E(l.level)}</span></div><p class="mini" style="margin:8px 0">${E(l.rule)}</p><div class="progress" aria-label="Tamamlanan alıştırma: ${tried}/10"><span style="width:${tried*10}%"></span></div><div class="row between" style="margin-top:12px"><span class="mini">${tried}/10 çalışıldı</span>${button(tried?'Devam et':'Dersi başlat','skillOpen','small primary',`data-id="${E(l.id)}"`)}</div></div>`;}).join('')}</div><div class="panel" style="margin-top:18px"><h3>7 / 30 gün kalıcılık</h3>${windows}<p class="footnote">Yalnızca 7–14 ve 30–45 gün arası tekrar edilen otomatik kontrol görevlerindeki referans eşleşmeleri. Kişisel beceri veya CEFR sertifika puanı değildir.</p></div>`;
 }
 const i=Math.min(lesson.exercises.length-1,Math.max(0,ui.skillIndex));
 const ex=lesson.exercises[i],completed=P.skillCards[ex.id];
 const modeLabel={order:'Kelime sırasını oluştur',guided:'Boşluğu tamamla',production:'Serbest üretim',followup:'Farklı bağlama aktar'}[ex.mode];
 const answer=ui.skillOrder.map(j=>ex.tokens?.[j]).join(' ');
 const cloze=ex.mode==='guided'?sentenceCloze(ex.modelAnswer,lesson.area):null;
 const answerInput=ex.mode==='order'?`<div class="skill-answer"><b>Seçtiğin sıra</b><p aria-live="polite">${answer?E(answer):'Kelime kartlarına dokunarak sırala.'}</p></div><div class="skill-tokens">${ex.tokens.map((token,j)=>button(E(token),'skillToken',ui.skillOrder.includes(j)?'small ghost':'small soft',`data-index="${j}" ${ui.skillOrder.includes(j)||ui.skillFeedback?'disabled':''}`)).join('')}</div><div class="row" style="margin-top:10px">${button('Son kartı geri al','skillUndo','small ghost',ui.skillOrder.length&& !ui.skillFeedback?'':'disabled')}${button('Sırayı temizle','skillClear','small ghost',ui.skillOrder.length&&!ui.skillFeedback?'':'disabled')}</div>`:
 `<label class="small-label" for="skillAnswer">${ex.mode==='guided'?'Boşluk için cevabın':'İngilizce cümlen / sorun'}</label>${cloze?`<div class="skill-prompt" lang="en">${E(cloze.prompt)}</div>`:''}<textarea id="skillAnswer" class="search" rows="3" spellcheck="false" maxlength="600" autocomplete="off" placeholder="Write in English…" ${ui.skillFeedback?'disabled':''}></textarea>`;
 const result=ui.skillFeedback?.result;
 const feedback=ui.skillFeedback?`<div class="notice ${result.automatic&&result.matched?'ok':'warn'}" role="status"><b>${result.automatic?(result.matched?'✓ Referans yanıtla eşleşti':'Referans yanıtla eşleşmedi. Bu mutlaka gramer hatası demek değildir.'):'Serbest cevap · öz değerlendirme'}</b><p><strong>Model cevap:</strong> <span lang="en">${E(ex.modelAnswer)}</span></p><p class="mini"><strong>Yapı:</strong> ${E(lesson.rule)}</p><p class="mini"><strong>Sık hata:</strong> ${E(lesson.commonError)}</p>${!result.matched&&result.automatic?`<p class="mini">Farklı ama doğru bir yanıt yazdıysan otomatik değerlendirmeyi devre dışı bırakıp öz değerlendirme kullanabilirsin.</p>${button('Alternatif doğru yanıtımı öz değerlendir','skillAlternative','small soft')}`:''}</div>
 <div class="flash-actions">${button('Hatırlayamadım · tekrar','skillGrade','small ghost','data-grade="again"')}${button('Kısmen doğru · daha erken tekrar','skillGrade','small soft','data-grade="hard"')}${button('Doğru kullandım · tekrar planla','skillGrade','primary',`data-grade="good" ${result.automatic&&!result.matched?'disabled':''}`)}</div>`:'';
 return `${overview}<div class="panel study skill-studio"><div class="row between">${button('← Ders listesi','skillBack','small ghost')}<span class="tag green">${E(SKILL_AREAS[lesson.area])} · ${i+1}/10</span></div><h2 style="margin-top:16px">${E(lesson.title)}</h2><p class="mini">${E(lesson.description)}</p><div class="progress" aria-label="Dersin ilerleyişi"><span style="width:${(i+1)*10}%"></span></div><div class="notice" style="margin:15px 0"><b>Temel kural</b><p>${E(lesson.rule)}</p></div><div class="row between"><span class="tag">${E(modeLabel)}</span>${completed?`<span class="tag">Daha önce çalışıldı · ${E(completed.status||'tekrar')}</span>`:''}</div><p style="margin-top:14px">${E(ex.task)}</p>${answerInput}${feedback}${!ui.skillFeedback?`<div class="flash-actions">${button('Cevabımı kontrol et ve örneği göster','skillCheck','primary')}</div>`:''}<hr class="divider"><div class="row between">${button('← Önceki','skillPrev','small soft',i===0?'disabled':'')}${button('Sonraki →','skillNext','small soft',i>=9?'disabled':'')}</div><p class="footnote">İlerleme yalnızca değerlendirme seçildikten ve cihaz depolamasına yazma başarılı olduktan sonra kaydedilir. Serbest yanıtlar otomatik gramer puanı değildir. Bu bölüm Speaking modülünden bağımsızdır.</p></div>`;
}
'''
s=s.replace(anchor,component+anchor,1)
put('const pages={home,toefl,', 'const pages={sentenceSkills:sentenceSkillsPage,home,toefl,')
put("case 'goto': ui.linkedQuizId",r'''case 'skillArea':ui.skillArea=SKILL_AREAS[ds.value]?ds.value:'question';ui.skillLesson=null;ui.skillIndex=0;ui.skillOrder=[];ui.skillFeedback=null;render();break;
 case 'skillOpen':{const lesson=data.sentenceSkills?.lessons.find(x=>x.id===ds.id);if(!lesson)break;ui.skillLesson=lesson.id;ui.skillArea=lesson.area;ui.skillIndex=lesson.exercises.findIndex(x=>!P.skillCards[x.id]);if(ui.skillIndex<0)ui.skillIndex=0;ui.skillOrder=[];ui.skillFeedback=null;render();break;}
 case 'skillBack':ui.skillLesson=null;ui.skillFeedback=null;ui.skillOrder=[];render();break;
 case 'skillDue':{const due=skillsDue(data.sentenceSkills,P);if(!due.length){notify('Şu anda zamanı gelen tekrar yok.');break;}const ex=due[0],lesson=data.sentenceSkills.lessons.find(l=>l.id===ex.lessonId);ui.skillArea=lesson.area;ui.skillLesson=lesson.id;ui.skillIndex=lesson.exercises.findIndex(x=>x.id===ex.id);ui.skillOrder=[];ui.skillFeedback=null;render();break;}
 case 'skillToken':{if(ui.skillFeedback)break;const ex=data.sentenceSkills?.lessons.find(l=>l.id===ui.skillLesson)?.exercises[ui.skillIndex];const n=Number(ds.index);if(ex?.mode==='order'&&Number.isInteger(n)&&n>=0&&n<ex.tokens.length&&!ui.skillOrder.includes(n)){ui.skillOrder.push(n);render();}break;}
 case 'skillUndo':if(!ui.skillFeedback&&ui.skillOrder.length){ui.skillOrder.pop();render();}break;
 case 'skillClear':if(!ui.skillFeedback){ui.skillOrder=[];render();}break;
 case 'skillPrev':ui.skillIndex=Math.max(0,ui.skillIndex-1);ui.skillFeedback=null;ui.skillOrder=[];render();break;
 case 'skillNext':ui.skillIndex=Math.min(9,ui.skillIndex+1);ui.skillFeedback=null;ui.skillOrder=[];render();break;
 case 'skillCheck':{if(ui.skillFeedback)break;const lesson=data.sentenceSkills?.lessons.find(l=>l.id===ui.skillLesson),ex=lesson?.exercises[ui.skillIndex];if(!ex)break;const answer=ex.mode==='order'?ui.skillOrder.map(i=>ex.tokens[i]).join(' '):(document.querySelector('#skillAnswer')?.value||'');const result=assessSkillInput(ex,answer,lesson.area);if(!result.submitted){notify('Önce cevabını yaz veya kartları sırala.');break;}ui.skillFeedback={result,answer};render();break;}
 case 'skillAlternative':if(ui.skillFeedback?.result?.automatic&&!ui.skillFeedback.result.matched){ui.skillFeedback.result={...ui.skillFeedback.result,automatic:false,matched:null};render();}break;
 case 'skillGrade':{const lesson=data.sentenceSkills?.lessons.find(l=>l.id===ui.skillLesson),ex=lesson?.exercises[ui.skillIndex];if(!lesson||!ex||!ui.skillFeedback?.result?.submitted)break;try{P=persistSkillReview(P,{...ex,lessonId:lesson.id},lesson.area,ds.grade,ui.skillFeedback.result,localStorage);notify('Çalışma kaydı cihazına yazıldı.');ui.skillFeedback=null;ui.skillOrder=[];if(ui.skillIndex<9)ui.skillIndex++;else ui.skillLesson=null;render();}catch(err){notify('Kaydedilemedi; mevcut kayıtlar korunuyor. JSON yedeği alın. '+err.message);}break;}
 case 'goto': ui.linkedQuizId''')
put("'expressions'];const res=", "'expressions','sentenceSkills'];const res=")
put("k==='expressions'?'daily-expressions':k", "k==='expressions'?'daily-expressions':k==='sentenceSkills'?'sentence-skills':k")
put("keys.forEach((k,i)=>data[k]=res[i]);if(P.toeflActiveReading)","keys.forEach((k,i)=>data[k]=res[i]);validateSentenceSkills(data.sentenceSkills);if(P.toeflActiveReading)")
p.write_text(s)
p=root/'js/progress-safety.js';s=p.read_text().replace("'memoryCues'];","'memoryCues','skillCards'];").replace("'toeflWritingAttempts'];","'toeflWritingAttempts','skillHistory'];");p.write_text(s)
p=root/'js/engine.js';s=p.read_text().replace("writing:{},settings:","writing:{},skillCards:{},skillHistory:[],settings:",1);p.write_text(s)
p=root/'sw.js';s=p.read_text().replace('ael-dev-20261030-learning-quality-v1','ael-dev-20261030-sentence-skills-v2').replace("'./js/app.js'","'./js/app.js','./js/sentence-skills.js'").replace("'./data/grammar.json'","'./data/grammar.json','./data/sentence-skills.json'");p.write_text(s)
p=root/'styles.css';p.write_text(p.read_text()+r'''
/* Sentence Skills: responsive authored exercise studio */
.skill-studio{max-width:860px}
.skill-answer,.skill-prompt{background:var(--raised);border:1px solid var(--line);padding:13px 15px;border-radius:12px;margin:12px 0;font-size:16px;line-height:1.7}
.skill-answer p{margin:6px 0 0;min-height:26px;overflow-wrap:anywhere}
.skill-tokens{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.skill-tokens button{min-width:40px;max-width:100%;overflow-wrap:anywhere}
.skill-studio #skillAnswer{margin:8px 0;resize:vertical;min-height:90px}
.skill-studio .notice p{margin:8px 0 0}
@media(max-width:650px){.skill-studio{padding:15px}.skill-studio .flash-actions .btn{flex:1 1 100%}.skill-studio .skill-tokens .btn{min-height:41px}}
''')
print('App integrated')
