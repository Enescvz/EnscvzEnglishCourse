from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'js/app.js';s=p.read_text()
def r(a,b):
 global s
 n=s.count(a)
 if n!=1:raise ValueError(f'match {n} {a[:120]}')
 s=s.replace(a,b)
r("fluencyWritingReport:null};", "fluencyWritingReport:null,fluencySpeed:1};")
r("if(e.target.id==='fluencyListened')", "if(e.target.dataset.field==='fluencySpeed'){ui.fluencySpeed=Number(e.target.value)||1;if(audio)audio.playbackRate=ui.fluencySpeed;return;}\n if(e.target.id==='fluencyListened')")
r("function resetFluency(){", "function resetFluency(){") if False else None
# source name helper to navigate directly from error coach to exact task
r('function execute(action,buttonEl){', '''function openFluencyReview(id,type){
 if(type==='sentenceSkills'){
  for(const lesson of data.sentenceSkills?.lessons||[]){const i=lesson.exercises.findIndex(x=>x.id===id);if(i>=0){ui.skillArea=lesson.area;ui.skillLesson=lesson.id;ui.skillIndex=i;ui.skillOrder=[];ui.skillFeedback=null;route('sentenceSkills');return true;}}
  return false;
 }
 let index=-1,step=0,tab=type;
 if(type==='realLife'){
  index=(data.fluency?.realLife||[]).findIndex(s=>s.steps.some(x=>x.id===id));
  if(index>=0)step=data.fluency.realLife[index].steps.findIndex(x=>x.id===id);
 }else if(type==='thinking')index=(data.fluency?.thinking||[]).findIndex(x=>x.id===id);
 else if(type==='dictation')index=dictationTargets(data.authentic).findIndex(x=>x.id===id);
 else if(['listening','bridge'].includes(type)){
  const m=id.match(/^(?:listening|bridge)-(.+)-q(\\d+)$/);
  index=m?humanSources(data.authentic).findIndex(x=>x.id===m[1]):-1;
  step=m?Math.max(0,Number(m[2])-(type==='bridge'?1:0)):0;
 }
 if(index<0)return false;
 ui.fluencyTab=tab;ui.fluencyIndex=index;resetFluency();ui.fluencyStep=step;route('fluencyStudio');return true;
}
function execute(action,buttonEl){''')
r("const src=humanSources(data.authentic)[ui.fluencyIndex],q=src?.questions?.[type==='bridge'?Math.min(1,src.questions.length-1):0];", "const src=humanSources(data.authentic)[ui.fluencyIndex],qi=type==='bridge'?Math.min(ui.fluencyStep+1,(src?.questions?.length||1)-1):ui.fluencyStep,q=src?.questions?.[qi];")
r('id=`${type}-${src.id}`,category=', 'id=`${type}-${src.id}-q${qi}`,category=')
r("case 'fluencyStepNext':{const rows=data.fluency.realLife[ui.fluencyIndex]?.steps||[];if(!ui.fluencySaved)break;ui.fluencyStep=(ui.fluencyStep+1)%Math.max(rows.length,1);ui.fluencyChoice=null;ui.fluencyResult=null;ui.fluencySaved=false;render();break;}", """case 'fluencyStepNext':{
  if(!ui.fluencySaved)break;
  const t=ui.fluencyTab;
  if(t==='realLife'){const rows=data.fluency.realLife[ui.fluencyIndex]?.steps||[];ui.fluencyStep=(ui.fluencyStep+1)%Math.max(rows.length,1);}
  else if(t==='listening'||t==='bridge'){const src=humanSources(data.authentic)[ui.fluencyIndex];const cap=src?.questions.length||1;const next=ui.fluencyStep+1+(t==='bridge'?1:0);if(next>=cap){ui.fluencyIndex=Math.min(ui.fluencyIndex+1,humanSources(data.authentic).length-1);resetFluency();render();break;}ui.fluencyStep++;}
  ui.fluencyChoice=null;ui.fluencyResult=null;ui.fluencySaved=false;ui.fluencyReveal=false;render();break;
 }""")
r("case 'fluencyFixError':{if(ds.source==='sentenceSkills'){route('sentenceSkills');break;}ui.fluencyTab=ds.source==='listening'||ds.source==='bridge'?'listening':ds.source==='dictation'?'dictation':ds.source==='thinking'?'thinking':'realLife';ui.fluencyIndex=0;resetFluency();render();break;}", """case 'fluencyFixError':{
  const all=[...(P.fluencyHistory||[]),...(P.skillHistory||[]).map(x=>({...x,type:'sentenceSkills',category:x.area}))].filter(x=>x.category===ds.category&&['hard','again'].includes(x.grade)).sort((a,b)=>b.at-a.at);
  if(!all.length||!openFluencyReview(all[0].id,all[0].type))notify('İlgili göreve ulaşılamadı; eski kayıt korunuyor.');break;
 }
 case 'fluencyOpenDue':{
  const row=(P.fluencyHistory||[]).filter(x=>x.id===ds.id).sort((a,b)=>b.at-a.at)[0];
  if(!row||!openFluencyReview(row.id,row.type))notify('Tekrar görevine ulaşılamadı.');break;
 }""")
r("audio.playbackRate=ui.speed||1;if(ui.view==='authentic'", "audio.playbackRate=ui.view==='fluencyStudio'?(ui.fluencySpeed||1):(ui.speed||1);if(ui.view==='authentic'")
p.write_text(s)

p=root/'js/fluency-ui.js';s=p.read_text()
def rr(a,b):
 global s
 n=s.count(a)
 if n!=1:raise ValueError(f'ui match {n} {a[:130]}')
 s=s.replace(a,b)
rr("<p class=\"mini\"><a href=\"${E(src.sourceUrl)}\" target=\"_blank\" rel=\"noopener noreferrer\">VOA yayıncı sayfasından aç</a> · Bağlantı çalışmazsa dinleme başarısı kaydedilmez.</p></div>`;", "<div class=\"row\" style=\"gap:9px\"><label for=\"fluencySpeed\">Hız</label><select class=\"search\" style=\"width:auto\" id=\"fluencySpeed\" data-field=\"fluencySpeed\">${[.8,1,1.15].map(v=>`<option value=\"${v}\" ${ui.fluencySpeed===v?'selected':''}>${v}×</option>`).join('')}</select></div><p class=\"mini\"><a href=\"${E(src.sourceUrl)}\" target=\"_blank\" rel=\"noopener noreferrer\">VOA yayıncı sayfasından aç</a> · Bağlantı çalışmazsa dinleme başarısı kaydedilmez.</p></div>`;")
rr("const src=lesson[ui.fluencyIndex%Math.max(1,lesson.length)],q=src?.questions?.[ui.fluencyTab==='bridge'?Math.min(1,src.questions.length-1):0];", "const src=lesson[ui.fluencyIndex%Math.max(1,lesson.length)],qIndex=ui.fluencyTab==='bridge'?Math.min(ui.fluencyStep+1,(src?.questions?.length||1)-1):ui.fluencyStep,q=src?.questions?.[qIndex];")
rr("<p>${ui.fluencyTab==='bridge'?'Önce aşağıdaki transkripti oku, sonra aynı insan sesli kaydı dinle ve metni kapatarak soruyu cevapla.':'Önce transkripti açmadan dinle; ana fikri ve ayrıntıları yakala. Ardından soruya cevap ver.'}</p>", "<p>${ui.fluencyTab==='bridge'?'Önce aşağıdaki transkripti oku, sonra aynı insan sesli kaydı dinle. Sorular ses içeriğine ilişkindir.':'1. Transkript kapalıyken dinle. 2. Aşağıdaki soruları tek tek çöz. 3. Sonrasında transkripti karşılaştır.'}</p><span class=\"tag green\">Anlama sorusu ${qIndex+1}/${src.questions.length}</span>")
rr("${ui.fluencyReveal?`<div class=\"transcript\"", "${ui.fluencySaved?b(qIndex+1>=src.questions.length?'Sonraki VOA kaynağı →':'Sonraki dinleme sorusu →','fluencyStepNext','small primary'):''}${ui.fluencyReveal?`<div class=\"transcript\"")
rr("${report.groups.length?report.groups.map(g=>", "${Object.entries(progress.fluencyCards||{}).filter(([,state])=>Number(state?.due)<=Date.now()).slice(0,12).length?`<h3>Bugün zamanı gelen tekrarlar</h3>${Object.entries(progress.fluencyCards||{}).filter(([,state])=>Number(state?.due)<=Date.now()).sort((a,b)=>a[1].due-b[1].due).slice(0,12).map(([id])=>`<div class=\"daily-item\"><strong>${E(id)}</strong>${b('Tam bu görevi aç','fluencyOpenDue','small primary',`data-id=\"${E(id)}\"`)}</div>`).join('')}`:''}${report.groups.length?report.groups.map(g=>")
rr("data-category=\"${E(g.category)}\" data-source=\"${E(g.source)}\"", "data-category=\"${E(g.category)}\" data-source=\"${E(g.source)}\"") if False else None
p.write_text(s)
print('refined exact error targeting and multi question listening')
