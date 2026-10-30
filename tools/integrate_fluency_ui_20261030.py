from pathlib import Path
p=Path(__file__).resolve().parents[1]/'js/app.js'
s=p.read_text()
def replace(a,b,expected=1):
 global s
 n=s.count(a)
 if n!=expected:raise ValueError(f'found {n} != {expected}: {a[:90]!r}')
 s=s.replace(a,b)
replace("import {filterCandidates} from './catalog.js';", "import {filterCandidates} from './catalog.js';\nimport {FLUENCY_TABS,humanSources,dictationTargets,compareDictation,wordTokens,writingAudit,persistFluencyReview,persistFluencyDraft,validateFluencyData} from './fluency-studio.js';\nimport {fluencyPage} from './fluency-ui.js';")
replace("['expressions','💬','Günlük Kalıplar'],['sentenceSkills'", "['expressions','💬','Günlük Kalıplar'],['fluencyStudio','🎧','Fluency Studio'],['sentenceSkills'")
replace("skillOrder:[],skillFeedback:null};", "skillOrder:[],skillFeedback:null,fluencyTab:'listening',fluencyIndex:0,fluencyStep:0,fluencyChoice:null,fluencyListened:false,fluencyResult:null,fluencyReveal:false,fluencySaved:false,fluencyWritingReport:null};")
replace('P.skillCards??={};P.skillHistory??=[];', 'P.skillCards??={};P.skillHistory??=[];P.fluencyCards??={};P.fluencyHistory??=[];P.fluencyDrafts??={};')
replace("${button('❓ Soru Kurma Atölyesi','goto','small primary','data-view=\"sentenceSkills\"')}","${button('❓ Soru Kurma Atölyesi','goto','small primary','data-view=\"sentenceSkills\"')}${button('🎧 Fluency Studio','goto','small primary','data-view=\"fluencyStudio\"')}")
replace("['sentenceSkills','❓','Question & Sentence Builder','Soru kurma, edat, bağlaç ve cümle üretimini çalış.']", "['sentenceSkills','❓','Question & Sentence Builder','Soru kurma, edat, bağlaç ve cümle üretimini çalış.'],['fluencyStudio','🎧','Fluency Studio','Dinle, dikte yap, gerçek diyalog ve hatalarını çalış.']")
replace('const pages={sentenceSkills:sentenceSkillsPage,home,', 'const pages={fluencyStudio:()=>fluencyPage({ui,progress:P,data,escape:E,button,link,section}),sentenceSkills:sentenceSkillsPage,home,')
replace(" case 'missionCard':{", """ case 'fluencyTab':{if(!FLUENCY_TABS.some(x=>x[0]===ds.value))break;ui.fluencyTab=ds.value;ui.fluencyIndex=0;resetFluency();render();break;}
 case 'fluencyMove':{const t=ui.fluencyTab,len=t==='listening'||t==='bridge'?humanSources(data.authentic).length:t==='dictation'?dictationTargets(data.authentic).length:t==='realLife'?data.fluency.realLife.length:t==='writing'?data.fluency.writing.length:t==='thinking'?data.fluency.thinking.length:1;ui.fluencyIndex=Math.min(Math.max(0,ui.fluencyIndex+Number(ds.value)),Math.max(0,len-1));resetFluency();render();break;}
 case 'fluencyChoose':if(ui.fluencyResult)break;ui.fluencyChoice=Number(ds.index);render();break;
 case 'fluencyReveal':ui.fluencyReveal=!ui.fluencyReveal;render();break;
 case 'fluencyOpenSource':{const target=humanSources(data.authentic).find(x=>x.id===ds.id);if(!target)break;ui.authenticId=target.id;ui.linkedQuizId=null;ui.authenticAnswers={};ui.authenticListened=false;route('authentic');break;}
 case 'fluencyStepNext':{const rows=data.fluency.realLife[ui.fluencyIndex]?.steps||[];if(!ui.fluencySaved)break;ui.fluencyStep=(ui.fluencyStep+1)%Math.max(rows.length,1);ui.fluencyChoice=null;ui.fluencyResult=null;ui.fluencySaved=false;render();break;}
 case 'fluencyCheck':{
  if(ui.fluencyResult)break;
  const type=ui.fluencyTab;let id='',category=type,good=false,reference='',explanation='',heading='',description='',allowGood=true,accuracy=null,requiresAudio=['listening','dictation','bridge'].includes(type);
  if(requiresAudio&&!ui.fluencyListened){notify('Önce kaydı gerçekten dinlediğini onayla. Ses bağlantısı çalışmadıysa dinleme başarısı kaydedilemez.');break;}
  if(type==='listening'||type==='bridge'){
   const src=humanSources(data.authentic)[ui.fluencyIndex],q=src?.questions?.[type==='bridge'?Math.min(1,src.questions.length-1):0];if(!src||!q||ui.fluencyChoice===null){notify('Önce bir cevap seç.');break;}
   id=`${type}-${src.id}`,category='listening-comprehension';good=ui.fluencyChoice===q.answer;reference=q.options[q.answer];explanation=q.explanation;heading=good?'✓ Doğru cevap':'Henüz doğru eşleşmedi';description='Bu sonuç, dinlediğini beyan ettiğin dersin tek sorusuna dayanır; genel Listening seviyen değildir.';allowGood=good;accuracy=good?100:0;
  }else if(type==='dictation'){
   const ex=dictationTargets(data.authentic)[ui.fluencyIndex],answer=document.querySelector('#fluencyAnswer')?.value||'',report=compareDictation(answer,ex?.target||'');if(!report.submitted){notify('Duyduğun cümleyi yaz.');break;}
   id=ex.id;category='dictation';accuracy=report.accuracy;good=accuracy>=90&&!ui.fluencyReveal;allowGood=good;reference=ex.target;heading=`${accuracy}% kelime eşleşmesi`;description=`${report.expectedWords} beklenen kelime, ${report.typedWords} yazılan kelime, ${report.distance} düzenleme farkı. Bu metin eşleşmesidir; ses algısını tek başına kanıtlamaz.`;
  }else if(type==='realLife'){
   const scenario=data.fluency.realLife[ui.fluencyIndex],step=scenario?.steps[ui.fluencyStep];if(!step||ui.fluencyChoice===null){notify('Önce bir cevap seç.');break;}
   id=step.id;category=scenario.topic.toLowerCase();good=ui.fluencyChoice===step.correct;allowGood=good;reference=step.options[step.correct];explanation=step.explanation;heading=good?'✓ Doğal ifade':'Daha doğal ifade';accuracy=good?100:0;description='Çoktan seçmeli özgün alıştırma; gerçek diyalog performansı ölçümü değildir.';
  }else if(type==='thinking'){
   const task=data.fluency.thinking[ui.fluencyIndex],answer=document.querySelector('#fluencyAnswer')?.value||'';if(wordTokens(answer).length<5){notify('En az 5 kelimelik özgün bir yanıt oluştur.');break;}
   id=task.id;category=task.focus;good=false;allowGood=true;reference=task.modelAnswer;heading='Örnek yanıtla karşılaştır';description='Alternatif doğal yanıtlar da doğru olabilir. Öz değerlendirme yap; otomatik anlam/gramer puanı yok.';
  }else break;
  ui.fluencyResult={id,type,category,good,reference,explanation,heading,description,accuracy,allowGood,requiresAudio};render();break;
 }
 case 'fluencyCommit':{
  const r=ui.fluencyResult;if(!r||ui.fluencySaved)break;const grade=ds.grade;
  if(grade==='good'&&!r.allowGood){notify('Yanlış otomatik cevaba doğru notu verilemez.');break;}
  try{const next=persistFluencyReview(P,{id:r.id,type:r.type,category:r.category,grade,accuracy:r.accuracy,listened:ui.fluencyListened,requiresAudio:r.requiresAudio},localStorage);P=next;ui.fluencySaved=true;render();notify('Akıcılık tekrar kaydı cihazda saklandı.');}catch(err){notify('Kaydedilemedi. İlerleme değiştirilmedi: '+err.message);}break;
 }
 case 'fluencySaveDraft':{
  const item=data.fluency.writing[ui.fluencyIndex],text=document.querySelector('#fluencyWriting')?.value||'';
  if(!item)break;try{P=persistFluencyDraft(P,item.id,text,localStorage);notify('Yazı taslağı cihazda saklandı.');}catch(err){notify('Taslak kaydedilemedi: '+err.message);}break;
 }
 case 'fluencyWritingCheck':{
  const item=data.fluency.writing[ui.fluencyIndex],text=document.querySelector('#fluencyWriting')?.value||'';if(!item||!text.trim()){notify('Önce bir metin yaz.');break;}
  ui.fluencyWritingReport=writingAudit(text,item);/* Keep textarea DOM untouched, so unsaved draft cannot be lost. */
  const host=document.querySelector('.fluency-work');if(host){const old=host.querySelector('.fluency-audit-live');old?.remove();const aside=document.createElement('div');aside.className='notice fluency-audit-live';aside.setAttribute('role','status');let r=ui.fluencyWritingReport;const title=document.createElement('strong');title.textContent=`${r.words} kelime · ${r.sentences} cümle · ${r.paragraphs} paragraf · ${r.connectors} bağlaç`;aside.append(title);for(const message of [...r.steps,r.disclaimer]){let p=document.createElement('p');p.className='mini';p.textContent=message;aside.append(p);}host.append(aside);}break;
 }
 case 'fluencyFixError':{if(ds.source==='sentenceSkills'){route('sentenceSkills');break;}ui.fluencyTab=ds.source==='listening'||ds.source==='bridge'?'listening':ds.source==='dictation'?'dictation':ds.source==='thinking'?'thinking':'realLife';ui.fluencyIndex=0;resetFluency();render();break;}
 case 'fluencyPlanGo':{if(ds.view==='sentenceSkills'){route('sentenceSkills');break;}if(ds.tab)ui.fluencyTab=ds.tab;resetFluency();route('fluencyStudio');break;}
 case 'missionCard':{""")
replace("function execute(action,buttonEl){", "function resetFluency(){ui.fluencyStep=0;ui.fluencyChoice=null;ui.fluencyListened=false;ui.fluencyResult=null;ui.fluencyReveal=false;ui.fluencySaved=false;ui.fluencyWritingReport=null;}\nfunction execute(action,buttonEl){")
replace("if(e.target.id==='voaListenedConfirm')", " if(e.target.id==='fluencyListened'){ui.fluencyListened=Boolean(e.target.checked);return;}\n if(e.target.dataset.field==='fluencySelect'){ui.fluencyIndex=Math.max(0,Number(e.target.value)||0);resetFluency();render();return;}\n if(e.target.id==='voaListenedConfirm')")
replace("'expressions','sentenceSkills'];", "'expressions','sentenceSkills','fluency'];")
replace("k==='sentenceSkills'?'sentence-skills':k}.json", "k==='sentenceSkills'?'sentence-skills':k==='fluency'?'fluency-studio':k}.json")
replace('validateSentenceSkills(data.sentenceSkills);', 'validateSentenceSkills(data.sentenceSkills);validateFluencyData(data.fluency);')
replace("${link('sentenceSkills','Beceri tekrarlarını aç →')}", "${link('sentenceSkills','Beceri tekrarlarını aç →')} ${link('fluencyStudio','Akıcılık tekrarlarını aç →')}")
replace("${link('sentenceSkills','Beceri istatistiklerini gör →')}", "${link('sentenceSkills','Beceri istatistiklerini gör →')} ${link('fluencyStudio','Fluency Studio →')}")
p.write_text(s)
print('integration app done')
