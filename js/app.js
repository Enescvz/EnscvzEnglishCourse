import {filterCandidates} from './catalog.js';
import {createContentLoader,INITIAL_KEYS,VIEW_KEYS} from './content-loader.js';
import {FLUENCY_TABS,humanSources,dictationTargets,compareDictation,wordTokens,writingAudit,persistFluencyReview,persistFluencyDraft,validateFluencyData} from './fluency-studio.js';
import {fluencyPage} from './fluency-ui.js';
import {SKILL_AREAS,validateSentenceSkills,sentenceCloze,assessSkillInput,skillsDue,skillSummary,persistSkillReview} from './sentence-skills.js';
import {offlinePanel,showOfflineStatus} from './offline.js';
import {retentionAudit} from './retention-audit.js';
import {newOfflineTrial,verifyOfflineTrial} from './offline-device-qa.js';
import {checkOffline} from './offline.js';
import {bindHumanAudioStatus} from './human-audio-status.js';
import {mergeProgress} from './progress-safety.js';
import {loadProgressRecord} from './progress-integrity.js';
import {checkBuiltSentence,countWritingWords,writingChecklist} from './toefl-writing.js';
import {makeWritingPractice,validateWritingPracticeSession,reviewWritingPractice,WRITING_PRACTICE_MINUTES} from './toefl-writing-exam.js';
import {makeReadingMini,makeReadingDiagnostic,balanceReadingChoices,gradeReadingMini,gradeReadingPractice,readingAdvice,readingReviewPlan,remainingSeconds,READING_MINI_MINUTES,READING_DIAGNOSTIC_MINUTES,OFFICIAL_2026_TASKS,makeTypedWordCompletion,checkTypedWordCompletion} from './toefl-prep.js';
import {filterVoaCatalog,catalogStats} from './voa-catalog.js';
import {normalizeRapidDeck,rapidFiltered,rapidRecord} from './rapid.js';
import {memoryPool,memoryQueue,memoryAnswer,memorySentenceContains,memoryGrade,memoryContextQuestion,recordMemoryReview,memoryCompletion,memoryStageProgress} from './memory.js';
import {LEVELS,normalize,accuracy,diffWords,analyzeDictation,defaultProgress,reviewItem,dueItems,priority,dailyPlan,dailyAssignments,quizBank,buildExam,escapeHTML as E} from './engine.js';
const nav=[
 ['home','⌂','Dashboard'],['listening','◉','Listening Academy'],['vocabulary','✦','Vocabulary Memory'],['phrasals','↗','Phrasal Verb Mastery'],
 ['expressions','💬','Günlük Kalıplar'],['fluencyStudio','🎧','Fluency Studio'],['sentenceSkills','❓','Soru & Cümle Atölyesi'],['podcasts','◈','İnsan Sesli Podcast'],['authentic','🎧','Real Voices · VOA'],['reading','▤','Reading'],['grammar','⌁','Grammar'],['speaking','◎','Speaking'],
 ['writing','✎','Writing'],['toefl','🎓','TOEFL + Daily'],['conversations','☏','Daily Conversations'],['pronunciation','♫','Pronunciation'],
 ['tests','◷','Practice Tests'],['review','↻','Smart Review'],['analytics','▥','Analytics'],['settings','⚙','Settings'],['catalog','☷','Kaynak Havuzu'],['rapid','⚡','Hızlı Kelime Kartları'],['memory','✺','Hafıza Koçu']
];
const app=document.querySelector('#app');let protectedCorruptRaw=null,progressReadError='';
const contentLoader=createContentLoader(fetch.bind(globalThis));
let routeSequence=0;let restoredDeferredSessions=false;
function restoreDeferredSessions(view){
 if(view!=='toefl'||restoredDeferredSessions)return;
 restoredDeferredSessions=true;
 if(P.toeflActiveReading)restoreReadingSession();
 if(P.toeflActiveWriting)restoreWritingExam();
}
function prepareMemoryItems(){
 if(data.memoryItems)return;
 data.memoryItems=memoryPool(data.focus,data.vocabulary,data.phrasals,data.toeflCore,data.expressions?.cards?.map(x=>({...x,contexts:expressionForToefl(x)?['daily','toefl']:['daily']})));
}
async function ensureViewContent(view){
 const loaded=await contentLoader.load(VIEW_KEYS[view]||[]);
 Object.assign(data,loaded);
 if(loaded.toeflAcademic&&!data.vocabulary.some(x=>x.id===loaded.toeflAcademic[0]?.id))data.vocabulary=[...data.vocabulary,...loaded.toeflAcademic];
 if(loaded.rapid)data.rapid=normalizeRapidDeck(data.rapid,data.vocabulary);
 if(loaded.sentenceSkills)validateSentenceSkills(data.sentenceSkills);
 if(loaded.fluency)validateFluencyData(data.fluency);
 if(view==='memory')prepareMemoryItems();
 restoreDeferredSessions(view);
}

let data={},P=load(),ui={view:'home',filter:'all',search:'',selection:0,mode:'intro',revealed:false,checked:null,feedback:'',entry:'',level:'all',episode:null,reading:null,toeflReadingId:null,drill:null,exam:null,examAnswers:{},examDone:false,transcript:false,quizChoices:{},clipRepeat:false,a:null,b:null,speed:1,modal:null,runTests:false,catalogKind:'all',catalogLevel:'all',catalogAvailability:'all',catalogPage:0,catalogLoading:false,catalogError:'',rapidSearch:'',rapidLevel:'all',rapidStatus:'all',rapidPage:0,rapidSelection:0,rapidRevealed:false,rapidDirection:'en-tr',memoryScope:'all',expressionLevel:'all',expressionContext:'all',expressionPage:0,memoryQueue:[],memoryIndex:0,authenticId:null,authenticAnswers:{},authenticTranscript:false,authenticListened:false,linkedQuizId:null,linkedAnswers:{},linkedListened:false,voaFilter:'all',voaPage:0,voaSearch:'',memoryPhase:'learn',memoryResult:null,memoryListening:null,memoryListenPlayed:false,memoryRecall:null,memoryContext:null,memoryContextChoice:null,memoryProduction:false,memorySentence:'',writingMode:'daily',toeflWritingIndex:0,toeflWritingFeedback:null,toeflMini:null,toeflMiniAnswers:{},toeflMiniResult:null,toeflReadingPage:0,toeflScriptId:null,toeflScriptChoices:{},toeflWritingExam:null,toeflWritingExamIndex:0,toeflWritingExamResult:null,toeflClozeIndex:null,toeflClozeResult:null,skillArea:'question',skillLesson:null,skillIndex:0,skillOrder:[],skillFeedback:null,fluencyTab:'listening',fluencyIndex:0,fluencyStep:0,fluencyChoice:null,fluencyListened:false,fluencyResult:null,fluencyReveal:false,fluencySaved:false,fluencyWritingReport:null,fluencySpeed:1};
let audio=null, recognition=null,voiceStatus='';
function load(){
 try{const loaded=loadProgressRecord(localStorage.getItem('ael-progress'),defaultProgress());
  protectedCorruptRaw=loaded.protectedRaw;progressReadError=loaded.issue||'';return loaded.progress;
 }catch(error){progressReadError='Cihaz depolaması okunamadı: '+error.message;protectedCorruptRaw='__UNREADABLE__';return defaultProgress();}
}
const cloneProgress=value=>JSON.parse(JSON.stringify(value));
let lastGoodSnapshot=null;
function savedSnapshot(){lastGoodSnapshot=JSON.stringify(P);}
function acceptPersisted(next){P=next;savedSnapshot();}
const safeProgressStorage={setItem(key,value){if(protectedCorruptRaw!==null)throw Error('Bozuk mevcut ilerleme kaydı korunuyor; kurtarmadan önce yazılamaz.');localStorage.setItem(key,value);}};
function save(){
 if(protectedCorruptRaw!==null){P=JSON.parse(lastGoodSnapshot);notify('Okunamayan eski kayıt korunuyor. Önce kurtarma verisini dışa aktar veya geçerli yedeğini geri yükle.');return false;}
 try{const payload=JSON.stringify(P);localStorage.setItem('ael-progress',payload);lastGoodSnapshot=payload;return true;}
 catch(error){P=JSON.parse(lastGoodSnapshot);notify('Depolama hatası: kayıt yapılmadı, son kalıcı duruma dönüldü. JSON yedeği alın.');return false;}
}
P.offlineTrialRestored=Boolean(P.offlineTrial?.marker && !globalThis.__aelOfflineTrialStartedHere);
P.rapidCards??={};
P.memoryCues??={};
P.expressions??={};
P.authenticLessons??={};
P.toeflAttempts??=[];
P.toeflWritingAttempts??=[];
P.skillCards??={};P.skillHistory??=[];P.fluencyCards??={};P.fluencyHistory??=[];P.fluencyDrafts??={};
savedSnapshot();
const iso=()=>new Date().toLocaleDateString('sv-SE');
function event(type,amount=1){P.events.push({at:Date.now(),type,amount});if(P.events.length>5000)P.events.shift();const today=iso();P.dateLog[today]=(P.dateLog[today]||0)+amount;return save();}
function notify(message){document.querySelector('.toast')?.remove();let t=document.createElement('div');t.className='toast';t.textContent=message;document.body.append(t);setTimeout(()=>t.remove(),3600);}
function route(view){
 if((pendingDraft&&!flushDraft())||(pendingWriting&&!flushWriting()))return;
 if(!nav.some(x=>x[0]===view))view='home';
 const request=++routeSequence;
 ui.view=view;ui.feedback='';ui.checked=null;ui.examDone=false;stopAudio();
 if(location.hash!=='#/'+view)location.hash='/'+view;
 const finish=()=>{if(request!==routeSequence)return;if(view==='memory'&&!ui.memoryQueue.length)startMemorySession();render();if(view==='catalog')void loadResearchCatalog();scrollTo({top:0,behavior:'instant'});};
 if(contentLoader.ready(VIEW_KEYS[view]||[])){
  if(view==='memory'&&!data.memoryItems)prepareMemoryItems();
  restoreDeferredSessions(view);
  finish();return Promise.resolve();
 }
 const section=app.querySelector?.('main .section');
 if(section)section.innerHTML='<div class="panel" role="status" aria-live="polite">Ders içerikleri yükleniyor…</div>';
 return ensureViewContent(view).then(finish).catch(error=>{
  if(request!==routeSequence)return;
  const host=app.querySelector?.('main .section');
  if(host)host.innerHTML=`<div class="panel" role="alert"><h2>İçerik yüklenemedi</h2><p>${E(error.message)}</p><button class="btn primary" data-act="retryView">Yeniden dene</button></div>`;
 });
}

let draftAutosaveTimer=null,pendingDraft=null;
let writingAutosaveTimer=null,pendingWriting=null;
function writingDraftStatus(message){const node=document.querySelector('#writingDraftStatus');if(node)node.textContent=message;}
function flushWriting(){
 if(writingAutosaveTimer!==null){clearTimeout(writingAutosaveTimer);writingAutosaveTimer=null;}
 if(!pendingWriting)return true;
 const {id,text}=pendingWriting;
 P.writing[id]=text;
 if(!save()){
  writingDraftStatus('✕ Taslak kaydedilemedi. Metni kopyala veya depolamayı kontrol et.');
  return false;
 }
 pendingWriting=null;
 writingDraftStatus('✓ Taslak otomatik kaydedildi.');return true;
}
function queueWriting(id,text){
 pendingWriting={id,text};writingDraftStatus('Taslak kaydediliyor…');
 if(writingAutosaveTimer!==null)clearTimeout(writingAutosaveTimer);
 writingAutosaveTimer=setTimeout(flushWriting,650);
}

function draftStatus(message){const el=document.querySelector('#fluencyDraftStatus');if(el)el.textContent=message;}
function flushDraft(){
 if(draftAutosaveTimer!==null){clearTimeout(draftAutosaveTimer);draftAutosaveTimer=null;}
 if(!pendingDraft)return true;
 const {id,text}=pendingDraft;
 if(protectedCorruptRaw!==null){draftStatus('Kayıt koruma modu: önce eski verini yedekle.');notify('Bozuk mevcut veri korunuyor. Taslak otomatik kaydedilemedi.');return false;}
 try{acceptPersisted(persistFluencyDraft(P,id,text,safeProgressStorage));pendingDraft=null;draftStatus('✓ Taslak cihazda otomatik kaydedildi; JSON yedeğine dahil.');return true;}
 catch(error){draftStatus('✕ Otomatik kaydetme başarısız. Metni kopyala ve depolamayı kontrol et.');notify('Taslak kaydedilemedi: '+error.message);return false;}
}
function queueDraft(text){
 const item=data.fluency?.writing?.[ui.fluencyIndex];if(!item)return;
 pendingDraft={id:item.id,text};draftStatus('Taslak kaydediliyor…');
 if(draftAutosaveTimer!==null)clearTimeout(draftAutosaveTimer);
 draftAutosaveTimer=setTimeout(()=>flushDraft(),650);
}
function stopAudio(){if(audio){audio.pause();audio=null;}if('speechSynthesis'in window)window.speechSynthesis.cancel();if(recognition){try{recognition.stop();}catch{}recognition=null;}ui.a=null;ui.b=null;ui.clipRepeat=false;}
function icon(n){return nav.find(x=>x[0]===n)?.[1]||'◈';}
function countMastered(which){const valid=new Set((which==='cards'?data.vocabulary:data.phrasals||[]).map(x=>x.id));return Object.entries(P[which]).filter(([id,x])=>valid.has(id)&&['Pekişmiş','Aktif kullanılabiliyor'].includes(x.status)).length;}
function section(title,subtitle='',eyebrow='YOUR LEARNING SPACE'){return `<div class="heading"><div class="eyebrow">${eyebrow}</div><h1>${E(title)}</h1>${subtitle?`<p class="sub">${E(subtitle)}</p>`:''}</div>`;}
function button(text,act,cls='soft',attrs=''){return `<button class="btn ${cls}" data-act="${act}" ${attrs}>${text}</button>`;}
function link(view,text='Aç'){return button(text,'goto','small soft',`data-view="${view}"`);}
const metric=(ico,val,label,detail='')=>`<div class="panel metric span-3"><div class="met-icon">${ico}</div><div class="statline"><strong>${E(val)}</strong>${detail?`<small>${E(detail)}</small>`:''}</div><p>${E(label)}</p></div>`;
function navHtml(){return `<aside class="side"><div class="brand"><div class="logo">A</div><div><strong>American<br>English Lab</strong><small>LEARN • RETAIN</small></div></div><div class="nav-caption">MY SPACE</div>${nav.map(([key,ico,label],i)=>`${[1,5,11,13].includes(i)?'<div class="nav-caption">'+(['','LEARNING PATH','','','','SKILLS','','','','','','PRACTICE','', 'YOUR DATA'][i]||'MORE')+'</div>':''}<button class="nav-button ${ui.view===key?'active':''}" data-act="goto" data-view="${key}"><span class="ico">${ico}</span><span>${label}</span>${key==='review'&&numDue()>0?`<em>${numDue()}</em>`:''}</button>`).join('')}<div class="side-note"><div class="orb">✦</div><strong>Every day counts.</strong><p>Kısa ve doğru tekrarlar, uzun ama pasif çalışmalardan daha değerlidir.</p></div></aside>`;}
function mobileNav(){const keys=['home','listening','vocabulary','review','settings'];return `<nav class="mobile-nav" aria-label="Mobil gezinme">${keys.map(key=>`<button data-act="goto" data-view="${key}" class="${ui.view===key?'active':''}"><span>${icon(key)}</span>${{home:'Ana sayfa',listening:'Listening',vocabulary:'Words',review:'Review',settings:'Diğer'}[key]}</button>`).join('')}</nav>`;}
function numDue(){return dueItems(data.vocabulary||[],P.cards).length+dueItems(data.phrasals||[],P.phrasals).length+skillsDue(data.sentenceSkills,P).length;}
function render(){document.documentElement.dataset.theme=P.settings.theme;let body;try{body=pages[ui.view]();}catch(e){console.error(e);body=`<div class="panel"><h2>Bir sorun oluştu</h2><p>${E(e.message)}</p>${link('home','Ana sayfaya dön')}</div>`;}
 app.innerHTML=`<div class="layout">${navHtml()}<main class="main">${progressReadError?`<div class="notice warn" role="alert"><b>Öğrenme kaydı koruma modunda</b><p>${E(progressReadError)} Eski veri otomatik üzerine yazılmayacak. Önce ham kurtarma dosyasını indir, ardından geçerli JSON yedeğini içe aktar veya bilerek sıfırla.</p>${button("Ham kurtarma verisini indir","exportCorrupt","small primary")}</div>`:""}<div class="top"><div class="crumb">AMERICAN ENGLISH <span style="color:var(--mint)">/</span> ${E(nav.find(x=>x[0]===ui.view)?.[2])}</div><div class="top-right"><span class="pill">🇺🇸 EN-US ONLY</span><span class="pill">${Math.round(P.events.length*2)} XP · practice</span><div class="avatar">A</div></div></div><div class="section">${body}</div></main></div>${mobileNav()}${ui.modal?modalHtml():''}`;
 bindAudioIfNeeded();if(ui.view==='settings')void showOfflineStatus();}
function home(){const count=P.listenHistory.length,avg=count?Math.round(P.listenHistory.slice(-10).reduce((s,x)=>s+x.accuracy,0)/Math.min(10,count)):0;const plans=dailyPlan(P,Number(P.settings.minutes)||60);const d=numDue();const mission=dailyAssignments(data.vocabulary,data.phrasals,[],P);return `<section class="hero"><div class="hero-text"><div class="eyebrow">YOUR PERSONAL ENGLISH STUDIO</div><h1>Real progress.<br>One day at a time.</h1><p>Amerikan İngilizcesini dinleyerek anla, kelimeleri gerçekten hatırla ve doğal ifadelerle kendini geliştir.</p>${button('▶ Listening ile başla','goto','primary',`data-view="listening"`)}</div><div class="hero-art" aria-hidden="true"></div></section>
<div class="panel" style="margin-top:18px"><div class="row between"><div><div class="small-label">DAILY ENGLISH + TOEFL</div><h2>Tek öğrenme yolu · ortak tekrar</h2><p class="mini">400 kelime ve 75 phrasal verb. 50 akademik kelime taslağı yeni; diğerleri mevcut ID ve çalışma kaydını korur.</p></div><div class="row">${button("TOEFL kelimeleri", "toeflOpen", "small primary", `data-kind="vocabulary"`)}${button("TOEFL phrasal", "toeflOpen", "small soft", `data-kind="phrasals"`)}${button("TOEFL çalışma merkezi","goto","small primary",'data-view="toefl"')}${button('Günlük kalıplar','goto','small soft','data-view="expressions"')}${button('❓ Soru Kurma Atölyesi','goto','small primary','data-view="sentenceSkills"')}${button('🎧 Fluency Studio','goto','small primary','data-view="fluencyStudio"')}</div></div></div>
<div class="grid metrics">${metric('◉',String(count),'Tamamlanan dictation','ses çalışması')}${metric('✦',countMastered('cards')+'/'+data.vocabulary.length,'Aktif kelime / içerik')}${metric('↗',countMastered('phrasals')+'/'+data.phrasals.length,'Aktif phrasal verb')}${metric('↻',String(d),'Zamanı gelen tekrar')}</div>
<div class="grid" style="margin-top:19px"><div class="span-7 panel"><div class="headline"><div><div class="small-label">TODAY'S ROUTE</div><h2>Bugünün çalışma planı</h2></div><span class="tag green">${P.settings.minutes} DAKİKA</span></div><p class="mini">Plan, son Listening çalışmalarındaki performansına göre dinleme süresini artırabilir.</p>${plans.map((x,i)=>`<div class="daily-item"><div class="daily-bubble">${icon(x.key==='review'?'review':x.key)}</div><div><strong>${x.label}</strong><p class="mini">${x.mins} dakika · ${i===0?'öncelikli beceri':'kişisel müfredat'}</p></div>${link(x.key,'Aç')}</div>`).join('')}</div>
<div class="span-5 panel"><div class="small-label">LEARNING SNAPSHOT</div><h2>Bugünkü özet</h2><div class="statline" style="margin:20px 0"><strong style="font-size:39px">${Math.max(0,P.dateLog[iso()]||0)}</strong><small>bugünkü etkinlik</small></div><div class="small-label">Son dictation başarısı</div><h2 style="margin-top:7px">${count?avg+'%':'Henüz ölçülmedi'}</h2><div class="progress"><span style="width:${avg}%"></span></div><hr class="divider"><p class="mini">Kelimeyi görerek tanımak, dinleyerek tanımak ve üretebilmek ayrı değerlendirilir.</p>${link('analytics','Analizi gör')}</div></div>
<div class="panel" style="margin-top:20px"><div class="row between"><div><div class="small-label">YOUR PERSONAL DAILY MISSION</div><h2>Bugünkü gerçek çalışma sıran</h2></div><span class="tag green">Önce tekrar · Sonra yeni</span></div><p class="mini">Tekrar zamanı gelen kartlar önceliklidir. Liste, çalışma sonuçlarına göre güncellenir.</p><div class="grid"><div class="span-6"><h3>✦ Vocabulary</h3><div class="items">${mission.words.map(x=>`<button class="item" data-act="missionCard" data-kind="vocabulary" data-id="${x.id}"><span><strong>${E(x.word)}</strong><small>${E(x.level)} · ${P.cards[x.id]?'Tekrar':'Yeni'}</small></span><span class="tag green">Başla →</span></button>`).join('')||'<p class="mini">Yeni kart kalmadı.</p>'}</div></div><div class="span-6"><h3>↗ Phrasal verbs</h3><div class="items">${mission.phrasals.map(x=>`<button class="item" data-act="missionCard" data-kind="phrasals" data-id="${x.id}"><span><strong>${E(x.word)}</strong><small>${E(x.level)} · ${P.phrasals[x.id]?'Tekrar':'Yeni'}</small></span><span class="tag green">Başla →</span></button>`).join('')||'<p class="mini">Yeni kart kalmadı.</p>'}</div>${mission.drill?`<hr class="divider"><h3>◉ Listening mission</h3><p class="mini">${E(mission.drill.title)} · ${E(mission.drill.category)}</p>${button('▶ Dinle ve çöz','openDrill','small primary',`data-id="${mission.drill.id}"`)}`:''}</div></div></div>
<div class="panel" style="margin-top:20px"><div class="row between"><div><div class="small-label">B2 / C1 · QUICK RECALL</div><h2>⚡ Hızlı Kelime Kartları</h2><p class="mini">${data.rapid?.length||0} İngilizce–Türkçe hızlı kart · Tam derslerden ayrı</p></div>${link('rapid','Hızlı çalış →')}</div></div>
<div class="panel" style="margin-top:20px"><div class="row between"><div><div class="small-label">LONG-TERM RETENTION · ACTIVE RECALL</div><h2>✺ Hafıza Koçu</h2><p class="mini">Dinle → yaz → hatırla → bağlamı anla → cümle kur → akıllı tekrar</p></div>${link('memory','Hafıza antrenmanını başlat →')}</div></div>
<div class="headline" style="margin-top:28px"><h2>Keşfet ve öğren</h2><span class="tag">Yeni · Soru & Cümle Atölyesi</span></div><div class="grid">${[['listening','◉','Decode real speech','Sesleri çöz, parçaları tekrar dinle, dictation yap.'],['vocabulary','✦','Memory Studio','Kelimeyi görerek, duyarak, hatırlayarak öğren.'],['phrasals','↗','Phrasal Mastery','İfadeleri bağlama ve kullanıma göre öğren.'],['podcasts','◈','Human Voice Podcasts','Robotik podcast yok; insan sesli kaynakları keşfet.'],['reading','▤','Read & Discover','Hikâyeler, düşünce yazıları, anlama soruları.'],['tests','◷','Exam Mode','25 soruluk karışık, açıklamalı denemeler.'],['sentenceSkills','❓','Question & Sentence Builder','Soru kurma, edat, bağlaç ve cümle üretimini çalış.'],['fluencyStudio','🎧','Fluency Studio','Dinle, dikte yap, gerçek diyalog ve hatalarını çalış.']].map(([k,ic,t,desc])=>`<div class="span-4 panel feature"><div class="feature-icon">${ic}</div><h3>${t}</h3><p>${desc}</p><button class="link" data-act="goto" data-view="${k}">Başla</button></div>`).join('')}</div>`;}
const lessonTypes=[['intro','Tanışma'],['recognition','Tanıma'],['recall','Yazma'],['listening','Kelime dinle'],['sentenceListening','Cümle dinle'],['context','Bağlam'],['production','Üretim']];
function lessonItems(){let all=ui.view==='phrasals'?data.phrasals:data.vocabulary;
 if(ui.filter==='toefl'){const ids=new Set(ui.view==='phrasals'?data.toeflCore?.phrasalLessonIds||[]:data.toeflCore?.wordLessonIds||[]);all=all.filter(x=>ids.has(x.id));}
 else if(ui.view==='vocabulary'&&ui.filter!=='all')all=all.filter(x=>x.category===ui.filter||x.level===ui.filter);
 if(ui.search)all=all.filter(x=>(x.word+' '+x.tr).toLocaleLowerCase('tr').includes(ui.search.toLocaleLowerCase('tr')));
 if(ui.level!=='all')all=all.filter(x=>x.level===ui.level||x.level?.startsWith(ui.level));
 return all;}
function curr(){const items=lessonItems();ui.selection=Math.min(ui.selection,Math.max(0,items.length-1));return items[ui.selection];}
function statusFor(item){let p=(ui.view==='phrasals'?P.phrasals:P.cards)[item.id];return p?.status||'Yeni';}
function vocab(isPhrasal=false){const all=isPhrasal?data.phrasals:data.vocabulary;const title=isPhrasal?'Phrasal Verb Mastery':'Vocabulary Memory';const sub=isPhrasal?'Günlük ve akademik bağlamda ifadeleri öğren.':'Günlük + akademik Amerikan İngilizcesi, ortak TOEFL çekirdek kartları ve finans koleksiyonu.';
 const items=lessonItems();const item=curr();return `${section(title,sub,'ACTIVE RECALL LEARNING')}<div class="row between"><span class="tag green">${all.length} editoryal başlangıç kaydı</span><span class="mini">${isPhrasal?`${data.phrasals.length} phrasal verb · 500 hedef`:`${data.vocabulary.filter(x=>x.category==='general').length} genel + ${data.vocabulary.filter(x=>x.category==='toeflAcademic').length} yeni akademik + ${data.vocabulary.filter(x=>['finance','accounting'].includes(x.category)).length} finans · 1.000 odak hedefi`}</span></div>
 <div class="notice"><b>🎓 Ortak TOEFL paketi:</b> ${data.toeflCore?.wordLessonIds?.length||0} kelime + ${data.toeflCore?.phrasalLessonIds?.length||0} phrasal verb. Kartlar günlük İngilizce ile aynı öğrenme ve tekrar kaydını kullanır. Resmî TOEFL sıklık sıralaması veya dil editörü onayı değildir.</div><div class="filter">${(isPhrasal?['all','toefl','B2','C1']:['all','toefl','general','toeflAcademic','accounting','finance','B2','C1']).map(k=>`<button class="chip ${ui.filter===k?'sel':''}" data-act="filter" data-value="${k}">${{all:'Tümü',toefl:'🎓 TOEFL + Daily',general:'Genel İngilizce',toeflAcademic:'Yeni akademik',accounting:'Accounting',finance:'Finance'}[k]||k}</button>`).join('')}</div><input class="search" data-field="search" placeholder="Kelime veya anlam ara…" value="${E(ui.search)}" aria-label="Kelime ara"><div class="row between" style="margin:16px 0"><strong>${items.length} sonuç</strong><div class="row">${button('← Önceki','prev','small soft')}${button('Sonraki →','next','small soft')}</div></div>
 ${item?studyCard(item,isPhrasal):'<div class="empty"><span class="emoji">⌕</span>Bu filtre için kayıt bulunamadı.</div>'}
 <div class="headline" style="margin-top:28px"><h2>İçerik havuzu</h2><span class="mini">Liste son 40 kayıtla sınırlıdır. Arama ile diğerlerini bulabilirsin.</span></div><div class="items">${items.slice(0,40).map((x,i)=>`<button class="item" data-act="select" data-index="${i}"><span><strong>${E(x.word)}</strong><small>${E(x.tr)}</small></span><span class="tag">${E((isPhrasal?P.phrasals:P.cards)[x.id]?.status||x.level)}</span></button>`).join('')}</div>`;}
function optionsFor(item,isPhrasal){const all=isPhrasal?data.phrasals:data.vocabulary;const comparable=isPhrasal?all:all.filter(x=>x.category===item.category);
 const start=all.indexOf(item);
 const distract=comparable.filter(x=>x.id!==item.id&&x.tr!==item.tr).slice((start+2)%Math.max(1,comparable.length)).concat(comparable.filter(x=>x.id!==item.id&&x.tr!==item.tr)).slice(0,3);
 return [item,...distract].sort((a,b)=>a.word.localeCompare(b.word));}
function sentenceExamples(item){
 const examples=(item.examples?.length?item.examples:[item.example]).filter(Boolean);
 return `<div class="examples" aria-label="Bağlam içinde örnek cümleler"><div class="small-label">AMERICAN ENGLISH · CONTEXT EXAMPLES</div>${examples.map((text,i)=>`<div class="example-row"><span class="example-number">${i+1}</span><p>${E(text)}</p>${button('🔊','speak','small soft',`aria-label="${i+1}. cümleyi Amerikan İngilizcesiyle dinle" data-text="${encodeURIComponent(text)}"`)}</div>`).join('')}</div>`;
}
function studyCard(item,isPhrasal){let modes=lessonTypes.map(([k,label])=>`<button class="chip ${ui.mode===k?'sel':''}" data-act="mode" data-mode="${k}">${label}</button>`).join('');let p=isPhrasal?P.phrasals[item.id]:P.cards[item.id];let main='';
 if(ui.mode==='intro'){main=`<div class="tr">${E(item.tr)}</div><p class="definition">${E(item.definition)}</p>${sentenceExamples(item)}${isPhrasal?`<div class="notice"><b>Yapı:</b> ${E(item.syntax)} · <b>Kullanım:</b> ${E(item.register)}<p>${E(item.note)}</p>${item.senses?.length>1?`<hr class="divider"><b>Diğer anlamlar:</b>${item.senses.slice(1).map(x=>`<p>• ${E(x.tr)} — <i>${E(x.example)}</i></p>`).join('')}`:''}</div>`:''}<p class="muted-ex">İlk bakışta öğrenildi sayılmaz. Şimdi farklı alıştırmalarla hatırla.</p>${button('Tanıma testine geç →','mode','primary',`data-mode="recognition"`)}`;}
 else if(ui.mode==='recognition'){main=`<p class="small-label">DOĞRU ANLAMI SEÇ</p><h3>“${E(item.word)}” bu bağlamda ne anlama geliyor?</h3><p class="mini">${E(item.example)}</p>${choiceUI(optionsFor(item,isPhrasal).map(x=>({label:x.tr,correct:x.id===item.id})), 'practice')}`;}
 else if(ui.mode==='context'){const sentence=item.example;main=`<p class="small-label">CONTEXT CHALLENGE</p><h3>Bu örnek cümlede hangi kelime / kalıp doğru kullanılmış?</h3><div class="notice">${E(sentence.replace(new RegExp('\\b'+item.word.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\b','i'),'_____'))}</div>${choiceUI(optionsFor(item,isPhrasal).map(x=>({label:x.word,correct:x.id===item.id})), 'practice')}`;}
 else if(ui.mode==='listening'){main=`<p class="small-label">LISTEN & TYPE · SESİ AÇMADAN YANIT GÖSTERİLMEZ</p><h3>Seslendirmeyi dinleyip kelimeyi / kalıbı yaz.</h3>${button('▶ En-US seslendir','speak','primary',`data-text="${encodeURIComponent(item.word)}"`)}${typeInput('Dinlediğin ifadeyi yaz', 'gradeWord')}`;}
 else if(ui.mode==='sentenceListening'){main=`<p class="small-label">LISTEN & DECODE · CÜMLEYİ TRANSCRIPT OLMADAN YAZ</p><h3>Örnek cümleyi dinle, duyduğunu İngilizce yaz.</h3><p class="mini">İlk dinlemede yazılı cümle görünmez. Kontrol sonrasında kelime sırası ve eksik kelimeler gösterilir. Tarayıcında en-US ses bulunmalıdır.</p>${button('▶ Amerikan aksanıyla cümleyi dinle','speak','primary',`data-text="${encodeURIComponent(item.example)}"`)}${typeInput('Duyduğun cümleyi yaz', 'gradeSentence')}`;}
 else if(ui.mode==='recall'){main=`<p class="small-label">ACTIVE RECALL</p><h3>“${E(item.tr)}” İngilizcede nasıl ifade edilir?</h3><p class="mini">İpucu: ${E(item.example.replace(new RegExp('\\b'+item.word.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'\\b','i'),'_____'))}</p>${typeInput('İngilizce cevabı yaz', 'gradeWord')}`;}
 else if(ui.mode==='production'){main=`<p class="small-label">USE IT IN CONTEXT</p><h3>“${E(item.word)}” ile özgün bir İngilizce cümle oluştur.</h3><p class="mini">Bu alıştırma otomatik olarak doğru dil bilgisi tespit edemez; örnek cümle ile karşılaştırıp öz değerlendirme yap.</p><textarea class="search" style="min-height:95px;resize:vertical" id="answer" placeholder="Write a sentence in English..."></textarea><div class="flash-actions">${button('Örnekle karşılaştır','productionCheck','primary')}</div>`;}
 const feedback=ui.feedback?`<div class="notice ${ui.checked===true?'ok':ui.checked===false?'warn':''}">${ui.feedback}</div>`:'';
 const gradeBtns=ui.checked!==null?`<p class="mini">Bu yanıtın ne kadar kolay hatırlandığını seçerek tekrar zamanını belirle:</p><div class="flash-actions">${button('Tekrar gerekli','grade','small ghost','data-grade="again"')}${button('Zorlandım','grade','small soft','data-grade="hard"')}${button('Hatırladım','grade','small primary','data-grade="good"')}${button('Çok kolaydı','grade','small soft','data-grade="easy"')}</div>`:'';
 return `<div class="study"><div class="panel" style="padding:15px"><div class="row between"><b>Öğrenme aşamasını seç</b><span class="mini">${ui.selection+1}/${lessonItems().length}</span></div><div class="filter" style="margin-bottom:0">${modes}</div></div><article class="flash"><div class="card-top"><span class="tag green">${E(item.level)}</span><span class="tag">${E(p?.status||'Yeni')}</span></div><div class="row between" style="margin-top:11px"><h1 style="margin:0">${['listening','sentenceListening'].includes(ui.mode)?'Listen carefully':E(item.word)}</h1>${!['listening','sentenceListening'].includes(ui.mode)?button('🔊','speak','small soft',`aria-label="Telaffuzu dinle" data-text="${encodeURIComponent(item.word)}"`):''}</div>${main}${feedback}${gradeBtns}<div class="flash-actions">${button('Sonraki kelime →','next','small soft')}</div></article><p class="footnote">${isPhrasal?'Her anlam için bağlam önemlidir. Bu ilk sürüm her fiilin örneklenen bir anlamını çalıştırır.':'Aktif cümle kurma öz değerlendirmelidir; otomatik dil yeterliliği puanlaması yapılmaz.'}</p></div>`;}
function choiceUI(options,source='practice',id=''){return `<div class="choice-list">${options.map((x,i)=>`<button class="choice ${ui.checked!==null&&source==='practice'?(x.correct?'correct':ui.checked===false&&ui.entry===String(i)?'wrong':''):''}" data-act="${source==='practice'?'practiceChoice':'choose'}" data-index="${i}" ${source==='practice'&&ui.checked!==null?'disabled':''}>${String.fromCharCode(65+i)} · ${E(x.label)}</button>`).join('')}</div>`;}
function typeInput(place,act){return `<div class="input-row"><input class="search" autocomplete="off" autocapitalize="off" spellcheck="false" id="answer" placeholder="${E(place)}" aria-label="${E(place)}"><button class="btn primary" data-act="${act}">Kontrol et</button></div>`;}
function pods(){return `${section('İnsan Sesli Podcast & Listening','Robotik sesli podcastler devre dışı bırakıldı. Yeni içerikler yalnızca gerçek insan sesi ve uygun kullanım hakkıyla eklenir.','HUMAN VOICE ONLY')}<div class="callout"><b>Robotik podcast yayında değil.</b><p>Önceki 18 eSpeak podcastin ses dosyaları kaldırıldı. Metin, soru ve eski öğrenme kayıtları korunuyor ancak dinleme veya test olarak sunulmuyor. Henüz bağımsız doğrulamadan geçmiş yeni podcast kaydı yok.</p><p>Gerçek insan sesli VOA derslerini uygulamadaki Listening bölümünden açabilirsin. Çevrimiçi MP3 oynatımı fiziksel iPhone Safari'de doğrulanmış değildir.</p>${link('authentic','🎧 Gerçek sesli VOA derslerini aç →')}</div>`;}
function episodeDetail(){return pods();}

function questions(qs,prefix){return qs.map((q,i)=>`<div class="test-question"><b>${i+1}. ${E(q.question)}</b><div class="choice-list">${q.options.map((o,j)=>`<button class="choice ${ui.quizChoices[prefix+'-'+i]===j?'correct':''}" data-act="answerQuestion" data-key="${prefix}-${i}" data-index="${j}">${E(o)}</button>`).join('')}</div>${ui.quizChoices[prefix+'-'+i]!==undefined?`<div class="notice ${ui.quizChoices[prefix+'-'+i]===q.answer?'ok':'warn'}">${ui.quizChoices[prefix+'-'+i]===q.answer?'✓ Doğru':'✕ Tekrar değerlendir'} · ${E(q.explanation)}</div>`:''}</div>`).join('');}
function authenticLibrary(){
 const lessons=data.authentic||[],sources=data.voaCatalog||[],linked=data.voaLinkedQuizzes||[];
 const stat=catalogStats(sources,lessons);
 const view=filterVoaCatalog(sources,{filter:ui.voaFilter,query:ui.voaSearch,page:ui.voaPage,pageSize:12});
 ui.voaPage=view.page;
 const filters=[['all','Tümü'],['interactive','Sorulu dersler'],['imported','Transkript içeride'],['linked','VOA üzerinden dinle'],['source','Yalnız kaynak'],['level2','Orta seviye'],['level1','Kolay dinleme']];
 return `${section('Real Voices · VOA',`50 ücretsiz VOA kaynağı · ${stat.quizEnabled} sorulu ders · ${stat.full} uygulama içi transkript · ${stat.linked} VOA bağlantılı soru seti`,'HUMAN SPEECH • ONLINE SOURCES')}
 <div class="callout"><b>Kaynak sayısı ile tamamlanmış ders sayısı farklıdır.</b><p><strong>${stat.sources} doğrulanmış VOA ders sayfası</strong> var. Bunların <strong>${stat.full}</strong> tanesinde transkript ve soru uygulamada, <strong>${stat.linked}</strong> tanesinde transkript/ses VOA sayfasında ve özgün sorular uygulamada; <strong>${stat.sourceOnly}</strong> tanesi yalnızca VOA kaynak bağlantısıdır. Kaynak sayfaların oynatılması ve çevrimdışı çalışması bu ortamda doğrulanmadı.</p><p class="mini">Level 2: orta seviye konuşma çalışması. Level 1 son dersleri: daha kolay ısınma; CEFR etiketleri yaklaşık çalışma gruplarıdır. İkisi de öğretim amaçlı senaryolaştırılmış insan sesidir, spontane röportaj değildir.</p><p class="footnote">Atıf: <a href="https://learningenglish.voanews.com/p/6861.html" target="_blank" rel="noopener noreferrer">VOA Learning English kullanım koşulları</a>. Üçüncü taraf ses/müzik içeren kayıtlar ayrıca lisans kontrolü gerektirir. ${stat.sources} kayıt için yerel MP3 iddiası yoktur.</p></div>
 <div class="row" style="flex-wrap:wrap;gap:7px;margin:15px 0">${filters.map(([key,label])=>button(label,'voaFilter',ui.voaFilter===key?'chip sel':'chip',`data-value="${key}"`)).join('')}</div>
 <input class="search" data-field="voaSearch" aria-label="VOA dinleme kaynağı ara" placeholder="Örn. travel, habits, work…" value="${E(ui.voaSearch)}" autocomplete="off">
 <div class="row between" style="margin:14px 0"><b>${view.count} kaynak</b><span class="mini">Sayfa ${view.page+1}/${view.pages}</span></div>
 <div class="grid">${view.items.map(x=>{
  const lesson=lessons.find(l=>l.id===x.interactiveLessonId),quiz=linked.find(l=>l.id===x.linkedQuizId),last=(P.authenticLessons||{})[lesson?.id||quiz?.id];
  return `<div class="panel episode-card span-4"><div class="cover">♫</div><div class="row"><span class="tag green">${E(x.learnerDifficulty)}</span><span class="tag">${E(x.levelGroup)}</span></div><h3 style="margin-top:11px">${E(x.title)}</h3><p>${E(x.topic)}</p>${lesson?`<p class="mini">${lesson.minutes.toFixed(1)} dk · ${lesson.questions.length} özgün soru · transkript uygulamada${last?' · '+(last.audioPlaybackSelfReported?'✓ ':'⚠ dinleme beyanı yok ')+last.correct+'/'+last.total:''}</p>${button('▶ Sorulu dersi aç','authenticOpen','small primary',`data-id="${E(lesson.id)}"`)}`:quiz?`<p class="mini">${quiz.questions.length} özgün soru · ses ve transkript VOA sayfasında${last?' · ✓ '+last.correct+'/'+last.total:''}</p>${button('▶ Soruları çöz','linkedQuizOpen','small primary',`data-id="${E(quiz.id)}"`)}`:`<p class="mini">Gerçek insan sesi ve transkript VOA sayfasında · Uygulama soruları henüz hazırlanmadı</p><a class="btn small soft" href="${E(x.sourceUrl)}" target="_blank" rel="noopener noreferrer">🎧 VOA'da dinle ve transkripti oku ↗</a>`}</div>`;
 }).join('')}</div>
 <div class="row between" style="margin-top:16px">${button('← Önceki','voaPrev','small soft')}${button('Sonraki →','voaNext','small soft')}</div>`;
}
function authenticEvidence(q){if(!Number.isInteger(q.sourceEvidenceTurn)||!q.sourceEvidence)return '';const more=Array.isArray(q.sourceEvidenceAdditional)?q.sourceEvidenceAdditional.map(x=>`<p class="mini">Ek kanıt: ${Number(x.turn)+1}. replik · ${E(x.speaker)}: “${E(x.text)}”</p>`).join(''):'';return `<p class="mini">Kaynak: ${q.sourceEvidenceTurn+1}. ${q.sourceEvidenceKind==='stage_direction'?'sahne yönergesi (sesli replik değil)':'replik'} · ${E(q.sourceEvidenceSpeaker||'VOA')}: “${E(q.sourceEvidence)}”</p>${more}`;}
function authenticDetail(){const x=(data.authentic||[]).find(x=>x.id===ui.authenticId);if(!x)return authenticLibrary();const last=(P.authenticLessons||{})[x.id];return `<div class="row" style="margin-bottom:15px">${button('← Real Voices','authenticBack','small ghost')}<span class="tag green">${E(x.level)}</span><span class="tag">${E(x.topic)}</span></div>${section(x.title,'Önce transkript kapalıyken dinle, ardından soruları cevapla.','REAL HUMAN VOICES · VOA')}
<div class="panel"><div class="row between"><b>▶ Voice of America · ${x.minutes.toFixed(1)} dk</b><span class="tag">${x.offlineReady&&x.localAudio?'LOCAL MP3 · HUMAN':x.audioUrl?'ONLINE MP3 · HUMAN':'VOA SAYFASINDA DİNLE'}</span></div>${x.audioUrl||x.localAudio?`<audio id="media" aria-label="VOA doğal İngilizce dinleme" controls preload="none" src="${E(x.offlineReady&&x.localAudio?x.localAudio:x.audioUrl)}"></audio><div class="row"><label for="speed">Hız</label><select id="speed" class="search" style="width:auto" data-field="speed">${[.75,.9,1,1.15,1.3].map(v=>`<option ${ui.speed===v?'selected':''} value="${v}">${v}×</option>`).join('')}</select></div><p class="mini" id="humanAudioStatus" role="status" aria-live="polite">Ses henüz başlatılmadı. Oynatmaya basın.</p>`:'<p class="notice warn">Bu ders için doğrulanmış doğrudan MP3 bağlantısı bulunamadı. Ses oynatıcı gösterilmiyor; yayıncı sayfasında dinleyip sorulara dönebilirsin.</p>'}<p class="mini">${x.offlineReady&&x.localAudio?'Bu dersin MP3 kopyası yerel olarak paketlenmiştir; ilk çevrimdışı önbellekleme tamamlanmış olmalıdır.':x.audioUrl?'Bu ses VOA sunucusundan internet üzerinden açılır. İnternet bağlantısı olmadan çalışmaz.':'Ses VOA kaynak sayfasında dinlenir; uygulamada oynatıcı yoktur.'} Oynatılmazsa <a href="${E(x.sourceUrl)}" target="_blank" rel="noopener noreferrer">orijinal kaydı VOA üzerinde aç</a>.</p></div>
<div class="grid" style="margin-top:16px"><div class="span-7 panel"><div class="row between"><h2>Kaynak transkripti</h2>${button(ui.authenticTranscript?'Metni gizle':'Metni göster','authenticToggleTranscript','small soft')}</div><p class="mini">Metin, VOA tarafından yayımlanan transkripttir. Saniye bazında ses eşleşmesi henüz doğrulanmadı.</p>${x.transcriptRightsExclusion?`<p class="notice warn">Telif ayrımı: Üçüncü taraf şarkı sözleri çıkarıldı. Bu dersin metni, kaydın tüm sözlerini kapsamaz. Orijinal VOA sayfasında dinleyebilirsin.</p>`:""}<div id="authenticTranscript" ${ui.authenticTranscript?'':'hidden'} class="transcript">${x.turns.map(t=>`<div class="turn" style="cursor:default"><strong>${E(t.speaker)}${t.kind==='stage_direction'?' · sahne yönergesi (seslendirilmiş olduğu doğrulanmadı)':''}</strong><p>${E(t.text)}</p></div>`).join('')}${x.publisherAppendix?`<div class="turn"><strong>VOA yayımlanmış kelime listesi · Sesle zaman eşleşmesi doğrulanmadı</strong><p>${x.publisherAppendix.items.map(E).join(' · ')}</p></div>`:''}</div>${ui.authenticTranscript?'':'<p id="authenticTranscriptNote" class="mini">İlk dinlemede metin gizlidir.</p>'}</div>
<div class="span-5 panel"><label class="notice" style="display:flex;gap:12px;align-items:center;cursor:pointer"><input id="authenticListenedConfirm" type="checkbox" ${ui.authenticListened?'checked':''}> <span>Bu kaydı dinledim (kendi beyanım; harici MP3 oynatımı teknik olarak doğrulanmadı).</span></label><div class="small-label">LISTEN AND UNDERSTAND</div><h2>Özgün anlama soruları</h2><p class="mini">Sorular bu projede hazırlandı; VOA’nın özgün quizini kopyalamıyor.</p>${x.questions.map((q,i)=>`<div class="test-question" data-auth-q="${i}"><b>${i+1}. ${E(q.question)}</b><div class="choice-list">${q.options.map((o,j)=>`<button class="choice ${ui.authenticAnswers[i]===j?'correct':''}" data-act="authenticAnswer" data-q="${i}" data-choice="${j}" ${ui.authenticAnswers[i]!==undefined?'disabled':''}>${E(o)}</button>`).join('')}</div><div class="auth-feedback">${ui.authenticAnswers[i]===undefined?'':`<div class="notice ${ui.authenticAnswers[i]===q.answer?'ok':'warn'}">${ui.authenticAnswers[i]===q.answer?'✓ Doğru':'✕ Tekrar çalış'} · ${E(q.explanation)}${authenticEvidence(q)}</div>`}</div></div>`).join('')}
${button('Dinlemeyi tamamla','authenticFinish','primary')}${last?`<div class="notice ${last.audioPlaybackSelfReported?'ok':'warn'}">Önceki kayıt: ${last.correct}/${last.total} · ${last.audioPlaybackSelfReported?'Dinleme kullanıcı beyanına dayanır.':'Önceki sürümde dinleme onayı alınmamıştı.'} Bu skor tek başına CEFR seviyesi değildir.</div>`:''}</div></div><div class="panel" style="margin-top:16px"><h3>Kelime ve phrasal verb bağlantıları</h3><p>${(Array.isArray(x.focus)?x.focus:[]).map(E).join(' · ')||"Dersin kaynak metninden kelime alıştırmaları hazırlanıyor."}</p><p class="mini">Bu ifadeleri dinlerken tanıyıp kendi cümlende kullanmaya çalış. Ayrıntılı alıştırmalar sonraki kalite aşamasında.</p><p class="footnote">Atıf: <a href="${E(x.sourceUrl)}" target="_blank" rel="noopener noreferrer">${E(x.attribution)} — ${E(x.sourceSeries)}</a></p></div>`;}
function linkedEvidence(q){
 if(!q.sourceEvidencePublisherLine||!q.sourceEvidencePublisherUrl)return '';
 const k=q.sourceEvidenceKind==='stage_direction'?'Yayıncı sahne yönergesi (sesli replik değil)':'Yayıncı Conversation konuşması';
 return `<p class="mini">Kaynak kontrolü: ${E(k)} · ${E(q.sourceEvidenceSpeaker||'VOA')} · “${E(q.sourceEvidence)}” <a href="${E(q.sourceEvidencePublisherUrl)}" target="_blank" rel="noopener noreferrer">VOA metnini aç ↗</a>. Ses eşleşmesi doğrulanmadı.</p>${q.sourceEvidenceCaveat?`<p class="mini"><strong>Bağlam notu:</strong> ${E(q.sourceEvidenceCaveat)}</p>`:''}`;
}
function linkedQuizDetail(){
 const x=(data.voaLinkedQuizzes||[]).find(x=>x.id===ui.linkedQuizId);if(!x)return authenticLibrary();
 const last=(P.authenticLessons||{})[x.id];
 return `<div class="row" style="margin-bottom:15px">${button('← Real Voices','linkedQuizBack','small ghost')}<span class="tag green">${E(x.level)}</span><span class="tag">VOA kaynak bağlantılı</span></div>${section(x.title,'VOA sayfasında metni gizleyerek dinle. Ardından buraya dönüp soruları cevapla.','REAL HUMAN VOICES · EXTERNAL AUDIO')}
 <div class="panel"><h2>1. Önce gerçek konuşmayı dinle</h2><p>Bu dersin sesi ve tam transkripti VOA yayıncı sayfasındadır; uygulamanın içine alınmamıştır. Dinlemeyi yeni sekmede açıp bitirince bu ekrana geri dön.</p><a class="btn primary" href="${E(x.sourceUrl)}" target="_blank" rel="noopener noreferrer">🎧 VOA'da sesi ve transkripti aç ↗</a><p class="footnote">Sesin çevrimiçi oynatımı cihazda henüz doğrulanmadı. Sorular, yayımlanmış Conversation metnindeki bilgilere göre özgün hazırlandı. Bu soru puanı dinleme sesinin gerçekten oynatıldığını kanıtlamaz.</p></div>
 <div class="panel" style="margin-top:15px"><label class="notice" style="display:flex;gap:12px;align-items:center;cursor:pointer"><input id="voaListenedConfirm" type="checkbox" ${ui.linkedListened?'checked':''}> <span>VOA kaydını dinledim (kendi beyanım; uygulama teknik olarak doğrulayamıyor).</span></label><div class="small-label">2. LISTEN & UNDERSTAND</div><h2>${x.questions.length} anlama sorusu</h2>${x.questions.map((q,i)=>`<div class="test-question" data-linked-q="${i}"><b>${i+1}. ${E(q.question)}</b><div class="choice-list">${q.options.map((o,j)=>`<button class="choice" data-act="linkedQuizAnswer" data-q="${i}" data-choice="${j}" ${ui.linkedAnswers[i]!==undefined?'disabled':''}>${E(o)}</button>`).join('')}</div><div class="auth-feedback">${ui.linkedAnswers[i]===undefined?'':`<div class="notice ${ui.linkedAnswers[i]===q.answer?'ok':'warn'}">${ui.linkedAnswers[i]===q.answer?'✓ Doğru':'✕ Tekrar dinle'} · ${E(q.explanation)}${linkedEvidence(q)}</div>`}</div></div>`).join('')}
 ${button('Sonucumu kaydet','linkedQuizFinish','primary')}${last?`<div class="notice ok">Önceki sonuç: ${last.correct}/${last.total}</div>`:''}<p class="footnote">Kaynak: <a href="${E(x.sourceUrl)}" target="_blank" rel="noopener noreferrer">VOA Learning English – ${E(x.title)}</a> · ses ve transkript sağlayıcıda kalır.</p></div>`;
}
function listening(){const recent=P.listenHistory.slice(-10),avg=recent.length?Math.round(recent.reduce((s,x)=>s+x.accuracy,0)/recent.length):null;return `${section('Listening Academy','Yalnızca gerçek insan sesli kaynaklar dinleme çalışması olarak sunulur.','HUMAN VOICES FIRST')}<div class="panel" style="margin-top:18px"><h2>🎧 Gerçek Amerikan İngilizcesi · VOA</h2><p>${(data.authentic||[]).length} uygulama içi transkriptli ders, ${(data.voaLinkedQuizzes||[]).length} kaynak bağlantılı ders; toplam ${(data.authentic||[]).reduce((n,x)=>n+x.questions.length,0)+(data.voaLinkedQuizzes||[]).reduce((n,x)=>n+x.questions.length,0)} soru. Sesler çevrimiçi yayıncı kaynağındadır; oynatım gerçek iPhone'da doğrulanmadı.</p>${link('authentic','Gerçek insan sesli dersleri aç →')}</div><div class="grid metrics">${metric('🎧',(data.authentic||[]).length+(data.voaLinkedQuizzes||[]).length,'VOA kaynaklı ders')}${metric('◈','0','Robotik podcast (aktif değil)')}${metric('◎',avg===null?'—':avg+'%','Önceki dictation ortalaması')}${metric('↻',P.listenHistory.length,'Geçmiş dinleme kaydı')}</div><div class="callout" style="margin-top:18px"><b>Eski 18 podcast ve 24 kısa ses alıştırması arşivlendi.</b><p>Robotik eSpeak MP3 dosyaları bu pakete dahil edilmedi ve dinleme görevleri olarak gösterilmez. Önceki öğrenme kayıtların silinmez.</p>${link('podcasts','Podcast durumu →')}</div>`;}
function drillDetail(){return listening();}

function bindAudioIfNeeded(){audio=document.querySelector('#media');if(!audio)return;audio.playbackRate=ui.view==='fluencyStudio'?(ui.fluencySpeed||1):(ui.speed||1);if(ui.view==='authentic'&&ui.authenticId)bindHumanAudioStatus(audio,document.querySelector('#humanAudioStatus'),{online:()=>typeof navigator==='undefined'?true:navigator.onLine!==false});audio.addEventListener('timeupdate',()=>{if(ui.clipRepeat&&ui.a!==null&&ui.b!==null&&ui.b>ui.a&&audio.currentTime>=ui.b)audio.currentTime=ui.a;let ep=data.episodes.find(x=>x.id===ui.episode),turn=ep?ep.timings.findIndex(x=>audio.currentTime>=x.start&&audio.currentTime<x.end):-1;document.querySelectorAll('.turn').forEach((el,i)=>el.classList.toggle('active',i===turn));});audio.addEventListener('error',()=>notify('Ses dosyası açılmadı. Sayfayı internet bağlantısıyla yenileyin.'));}
function reading(){if(ui.toeflReadingId)return toeflReadingDetail();if(ui.reading)return readingDetail();
 const t=data.toeflReading||[];
 const intro=`<div class="panel" style="margin-bottom:18px"><div class="row between"><h2>TOEFL 2026 Reading Practice</h2><span class="tag green">${t.length} özgün alıştırma</span></div><p class="mini">2026 görev türlerine göre düzenlendi: Complete the Words, Read in Daily Life, Read an Academic Passage. ETS resmî soruları veya gerçek sınav simülasyonu değildir.</p><div class="grid">${t.map(r=>`<div class="span-4"><p><strong>${E(r.title)}</strong></p><p class="mini">${E({complete_words:'Complete the Words',daily_life:'Read in Daily Life',academic_passage:'Read an Academic Passage'}[r.type])} · ${r.questions.length} soru</p>${button('Alıştırmayı aç','openToeflReading','small primary',`data-id="${r.id}"`)}</div>`).join('')}</div></div>`;
 return `${section('Reading Library','Özgün hikâyeler, makaleler ve açıklamalı anlama testleri.','READ & UNDERSTAND')}${intro}<div class="grid">${data.readings.map(r=>`<div class="panel feature span-4"><div class="feature-icon">▤</div><div class="row"><span class="tag green">${r.level}</span><span class="tag">${E(r.category)}</span></div><h3 style="margin-top:12px">${E(r.title)}</h3><p>${r.body.split(' ').length} kelime · 5 açıklamalı soru · cihaz TTS (insan sesi değil)</p>${button('Metni oku','openReading','small primary',`data-id="${r.id}"`)}</div>`).join('')}</div>`;}
function toeflReadingDetail(){const r=(data.toeflReading||[]).find(x=>x.id===ui.toeflReadingId);if(!r)return reading();return `<div class="row" style="margin-bottom:14px">${button('← Reading Library','backToeflReading','small ghost')}<span class="tag green">TOEFL 2026 · ${E(r.level)}</span></div>${section(r.title,'Özgün alıştırma; resmî ETS soru seti değildir.','READING PRACTICE')}<div class="grid"><div class="span-7 panel"><div class="text-body">${E(r.body)}</div></div><div class="span-5 panel"><h2>Questions</h2>${questions(r.questions,'tr-'+r.id)}${button('Alıştırmayı kaydet','completeToeflReading','primary',`data-id="${E(r.id)}"`)}</div></div>`;}

function clickableText(t){let entries=new Map(data.vocabulary.filter(x=>!x.word.includes(' ')).map(x=>[x.word.toLowerCase(),x]));return t.split(/(\b[A-Za-z]+(?:'[A-Za-z]+)?\b)/).map(x=>entries.has(x.toLowerCase())?`<button class="word known" data-act="lookup" data-id="${entries.get(x.toLowerCase()).id}">${E(x)}</button>`:E(x)).join('');}
function readingDetail(){const r=data.readings.find(x=>x.id===ui.reading);if(!r){ui.reading=null;return reading();}return `<div class="row" style="margin-bottom:14px">${button('← Reading Library','backReading','small ghost')}<span class="tag green">${r.level}</span></div>${section(r.title,'Yeşil altı çizili kelimelere dokunarak sözlüğe erişebilirsin.','READ & DISCOVER')}<div class="grid"><div class="span-7 panel"><div class="row">${button('🔊 Cihaz TTS ile dinle (en-US)','speak','small soft',`data-text="${encodeURIComponent(r.body)}"`)}</div><hr class="divider"><div class="text-body">${clickableText(r.body)}</div></div><div class="span-5 panel"><h2>Comprehension check</h2><p class="mini">5 soru · Her seçimin açıklaması</p>${questions(r.questions,'rd-'+r.id)}${button('Dersi tamamla','completeReading','primary',`data-id="${r.id}"`)}</div></div>`;}
function review(){const v=dueItems(data.vocabulary,P.cards),p=dueItems(data.phrasals,P.phrasals);const visibleIds=new Set([...data.vocabulary,...data.phrasals].map(x=>x.id));const upcoming=Object.entries({...P.cards,...P.phrasals}).filter(([k,x])=>visibleIds.has(k)&&x.due>Date.now()).sort((a,b)=>a[1].due-b[1].due).slice(0,8);return `${section('Smart Review','Görme, dinleme ve aktif hatırlama performansına göre tekrar.','MEMORY SCIENCE')}<div class="grid metrics">${metric('◷',v.length,'Bekleyen kelimeler')}${metric('↗',p.length,'Bekleyen phrasal verbs')}${metric('◉',countMastered('cards'),'Aktif kullanılabilen kelime')}${metric('✦',countMastered('phrasals'),'Aktif phrasal verbs')}</div><div class="panel" style="margin-top:19px"><h3>Soru ve cümle tekrarları</h3><p class="mini">${skillsDue(data.sentenceSkills,P).length} soru / edat / bağlaç alıştırmasının tekrar zamanı geldi.</p>${link('sentenceSkills','Beceri tekrarlarını aç →')} ${link('fluencyStudio','Akıcılık tekrarlarını aç →')}</div><div class="panel" style="margin-top:19px"><h2>Bugünün tekrarları</h2>${!(v.length+p.length)?'<div class="empty"><span class="emoji">✓</span>Şu an zamanı gelmiş tekrar yok. Önce yeni kelimeler çalışabilirsin.</div>':`<div class="items">${[...v.slice(0,10).map(x=>({...x,kind:'vocabulary'})),...p.slice(0,10).map(x=>({...x,kind:'phrasals'}))].map(x=>`<button class="item" data-act="reviewOpen" data-kind="${x.kind}" data-id="${x.id}"><span><strong>${E(x.word)}</strong><small>${E(x.tr)}</small></span><span class="tag green">Tekrar et →</span></button>`).join('')}</div>`}<hr class="divider"><h3>Yakında tekrar edilecekler</h3>${upcoming.length?`<div class="items">${upcoming.map(([id,p])=>`<div class="item"><b>${E(data.vocabulary.find(x=>x.id===id)?.word||data.phrasals.find(x=>x.id===id)?.word||'İfade')}</b><small>${new Date(p.due).toLocaleDateString('tr-TR')}</small></div>`).join('')}</div>`:'<p class="mini">Öğrendiğin kelimeler burada görünecek.</p>'}<p class="footnote">Algoritma: FSRS-5 (açık kaynak varsayılan parametreler, hedef hatırlama %90); yanlış yanıtta yaklaşık 15 dakika sonra yeniden çalışma. Eski kayıtlar sonraki değerlendirmede korunarak dönüştürülür. “Pekişmiş” için bağımsız hatırlama, bağlam, dinleme ve üretim başarısı birlikte gerekir.</p></div>`;}
function grammar(){return `${section('Grammar Workshop','B2–C1 yapıları karşılaştırmalı örneklerle keşfet.','BUILD ACCURACY')}<div class="grid">${data.grammar.map((g,i)=>`<div class="panel span-6"><div class="row between"><h3>${E(g.title)}</h3><span class="tag green">${g.level}</span></div><p class="mini">${E(g.explanation)}</p><div class="notice"><b>Örnek:</b> ${E(g.example)}</div><b>${E(g.question)}</b>${questions([{question:'Doğru ifadeyi seç',options:g.options,answer:g.answerIndex??0,explanation:g.explanation}], 'gram-'+g.id)}</div>`).join('')}</div>`;}
function speaking(){const prompts=['Describe a challenging decision you made and what you learned from it.','Explain why a particular city appeals to you.','Discuss a claim you heard recently and whether the evidence supports it.','Describe how you would resolve a misunderstanding between friends.'];let prompt=prompts[ui.selection%prompts.length];return `${section('Speaking Studio','Konuşma pratiği ve sınırlılıkları açık bir ses-yazı karşılaştırması.','SPEAK OUT LOUD')}<div class="panel study"><span class="tag green">B2–C1 • en-US</span><h2 style="margin-top:14px">Speak for 45 seconds</h2><div class="notice">${E(prompt)}</div>${button('🔊 Konuyu dinle','speak','small soft',`data-text="${encodeURIComponent(prompt)}"`)} <div class="flash-actions">${button('🎙 Mikrofonla dene','mic','primary')}${button('Yeni konuşma konusu','next','soft')}</div><p class="mini" id="mic-status">${E(voiceStatus||'Mikrofon desteği olan tarayıcıda en-US konuşma metne çevrilir. Bazı tarayıcılar internet üzerinden konuşma tanıma yapabilir; izin vermeden açılmaz.')}</p><textarea id="speech-output" class="search" rows="4" placeholder="Konuşma tanıma metni burada görünecek. Alternatif: konuşmanı kendin yaz."></textarea><div class="notice">Bu özellik telaffuz seviyeni veya CEFR Speaking puanını güvenilir biçimde ölçmez. Gerçek geribildirim için bir öğretmen veya dil partneri gerekir.</div></div>`;}
function writing(){
 const prompts=[['B2','Tell a story about a plan that did not work out as expected.'],['B2','Write an email politely disagreeing with a proposal.'],['C1','Discuss whether convenience should outweigh privacy.'],['C1','Evaluate the advantages and limitations of remote work.']];
 const tabs=`<div class="row" style="margin-bottom:16px">${button('Daily Writing', 'writingMode',ui.writingMode==='daily'?'small primary':'small soft','data-mode="daily"')}${button('TOEFL 2026', 'writingMode',ui.writingMode==='toefl'?'small primary':'small soft','data-mode="toefl"')}</div>`;
 if(ui.writingMode==='daily'){
  const idx=ui.selection%prompts.length;
  return `${section('Writing Desk','Paragraf, e-posta ve essay oluştur; ilerlemeni cihazında sakla.','WRITE & REFLECT')}${tabs}<div class="panel study"><div class="row between"><span class="tag green">${prompts[idx][0]}</span>${button('Başka konu','next','small soft')}</div><h2 style="margin-top:15px">${E(prompts[idx][1])}</h2><p class="mini">Hedef: 150–220 kelime. Giriş, destekleyici örnekler, karşı görüş ve sonuç üzerinde çalış.</p><textarea class="search" id="writing" rows="12" style="resize:vertical;line-height:1.65" placeholder="Start writing in English...">${E(P.writing[idx]||'')}</textarea><div class="row between" style="margin-top:12px"><span class="mini" id="wordcount">${countWritingWords(P.writing[idx]||'')} words</span>${button('Taslağı kaydet','saveWriting','primary')}</div><p id="writingDraftStatus" class="mini" role="status">Taslak değişiklikleri otomatik kaydedilir; düzenli JSON yedeği alın.</p><div class="notice">Öz kontrol: Açık tez cümlesi var mı? Örnekler iddianı destekliyor mu? Paragraflar birbirine bağlanıyor mu?<p>Yapay zekâ veya doğrulanmış dil bilgisi değerlendiricisi bulunmadığından otomatik puan verilmez.</p></div></div>`;
 }
 const tasks=data.toeflWriting||[];
 const idx=Math.min(ui.toeflWritingIndex,Math.max(0,tasks.length-1)),t=tasks[idx];
 if(!t)return `${section('TOEFL Writing','Yazma görevleri yüklenmedi.','PRACTICE')}${tabs}`;
 const key='toefl:'+t.id, draft=P.writing[key]||'';
 const typeName={build_sentence:'Build a Sentence',write_email:'Write an Email',academic_discussion:'Write for an Academic Discussion'}[t.kind];
 const feedback=ui.toeflWritingFeedback?`<div class="notice ${ui.toeflWritingFeedback.correct?'ok':'warn'}">${E(ui.toeflWritingFeedback.message)}${(ui.toeflWritingFeedback.notes||[]).map(n=>`<p class="mini">${E(n)}</p>`).join('')}</div>`:'';
 const hint=t.kind==='build_sentence'?`<p class="mini">Karışık parçalar: ${t.tokens.map(w=>`<span class="tag">${E(w)}</span>`).join(' ')}</p>`:t.kind==='academic_discussion'?`<div class="notice">${E(t.context)}</div>`:`<p class="mini">Kime: ${E(t.audience)}</p>`;
 const checklist=t.points?`<div class="notice"><b>Kendini kontrol et:</b><ul>${t.points.map(x=>`<li>${E(x)}</li>`).join('')}</ul></div>`:`<div class="notice">Yalnızca kelime sırası birebir kontrol edilir; resmî TOEFL notu değildir.</div>`;
 return `${section('TOEFL 2026 · Writing','Günlük İngilizce ile ortak öğrenme. ETS soruları değil, bu projeye özgü alıştırmalar.','WRITING PRACTICE')}${tabs}<div class="panel study"><div class="row between"><span class="tag green">${typeName} · ${idx+1}/${tasks.length}</span>${button('Sonraki görev','nextToeflWriting','small soft')}</div><h2 style="margin-top:15px">${E(t.title)}</h2><p>${E(t.prompt)}</p>${hint}<textarea class="search" id="toeflWriting" rows="10" style="resize:vertical;line-height:1.65" placeholder="Write your answer in English...">${E(draft)}</textarea><div class="row between" style="margin:12px 0"><span class="mini" id="wordcount">${countWritingWords(draft)} words${t.suggestedWords?' · Alıştırma hedefi '+t.suggestedWords.join('–')+' (resmî eşik değil)':''}</span><div class="row">${button('Taslağı kaydet','saveToeflWriting','small soft')}${t.kind==='build_sentence'?button('Kelime sırasını kontrol et','checkToeflSentence','primary'):button('Yapısal geri bildirim','toeflWritingHints','small primary')}</div></div>${feedback}${checklist}<p class="footnote">Başarı puanı üretilmez. E-posta ve tartışma yanıtlarında yapı/gramer editör incelemesi bekler. Taslak cihazında ve JSON yedeğinde tutulur.</p></div>`;
}
function conversations(){return `${section('Daily Conversations','Özgün diyalog metinleri arşivi. Robotik sesleri kaldırıldı; gerçek sesli Listening VOA bölümünde.','CONVERSATION PRACTICE')}<div class="grid">${data.episodes.slice(0,9).map(ep=>`<div class="panel feature span-4"><div class="feature-icon">☏</div><span class="tag green" style="align-self:flex-start">${ep.level}</span><h3 style="margin-top:12px">${E(ep.title)}</h3><p>${E(ep.turns[0].text)}</p>${button('VOA insan sesli dinleme →','goto','small primary','data-view="authentic"')}</div>`).join('')}</div>`;}
function pronunciation(){const pairs=[['ship','sheep','/ɪ/ vs /i/'],['sit','seat','/ɪ/ vs /i/'],['full','fool','/ʊ/ vs /u/'],['bad','bed','/æ/ vs /ɛ/'],['cot','caught','Dialect-sensitive: vowel merger possible'],['rice','rise','/s/ vs /z/'],['think','sink','/θ/ vs /s/'],['light','right','/l/ vs /r/']];return `${section('Pronunciation Lab','Amerikan İngilizcesinde ses ayrımı, vurgu ve bağlı konuşmayı çalış.','SOUND DESIGN')}<div class="callout"><b>Not:</b><p>Tarayıcıda en-US ses mevcutsa kelimeleri onunla duyarsın. Bazı minimal pair ayrımları Amerikan İngilizcesinin bölgesel çeşitlerinde birleşebilir (örneğin cot–caught).</p></div><div class="grid">${pairs.map(([a,b,focus],i)=>`<div class="panel span-6"><span class="tag green">SOUND PAIR ${i+1}</span><h3 style="margin-top:12px">${E(a)} <span style="color:var(--muted)">vs</span> ${E(b)}</h3><p class="mini">${E(focus)}</p><div class="row">${button('▶ '+E(a),'speak','small soft',`data-text="${encodeURIComponent(a)}"`)}${button('▶ '+E(b),'speak','small soft',`data-text="${encodeURIComponent(b)}"`)}</div></div>`).join('')}</div><div class="panel" style="margin-top:16px"><h2>Connected speech practice</h2><p class="mini">Sözcükler tek tek söylendiğindeki sesleri, cümle içindeki akıştan farklı algılayabilirsin.</p>${link('listening','Bağlı konuşma alıştırmalarına git →')}</div>`;}
function tests(){if(ui.exam)return examPage();return `${section('Practice Tests','25 özgün soru, sınav sırasında gizli cevaplar, sınav sonrası ayrıntılı çözümler.','ASSESS & IMPROVE')}<div class="panel study"><div class="small-label">B2–C1 VOCABULARY / PHRASAL VERBS</div><h2 style="margin:14px 0">25-question challenge</h2><p class="sub">Her deneme bankadan seçilir. Önce görülmeyen sorulara öncelik verilir; havuz bitince tekrarlar başlayabilir. Bu test tek başına CEFR seviyeni ölçmez.</p><div class="grid"><div class="span-6">${metric('◷',data.bank.length,'Soru havuzu')}</div><div class="span-6">${metric('▣',P.quizHistory.length,'Tamamlanan deneme')}</div></div><div class="flash-actions">${button('▶ Denemeyi başlat','startExam','primary')}</div><hr class="divider"><h3>Geçmiş denemeler</h3>${P.quizHistory.length?`<div class="table-wrap"><table class="simple-table"><thead><tr><th>Tarih</th><th>Skor</th><th>Doğru</th></tr></thead><tbody>${P.quizHistory.slice(-8).reverse().map(x=>`<tr><td>${new Date(x.at).toLocaleDateString('tr-TR')}</td><td>${x.score}%</td><td>${x.correct}/25</td></tr>`).join('')}</tbody></table></div>`:'<p class="mini">Henüz sınav sonucu yok.</p>'}</div>`;}
function examPage(){let exam=ui.exam,answered=Object.keys(ui.examAnswers).length;return `<div class="row between" style="margin-bottom:18px">${button('← Testlere dön','exitExam','small ghost')}<span class="tag green">${ui.examDone?'TAMAMLANDI':`${answered}/25 YANITLANDI`}</span></div>${section(ui.examDone?'Sınav Sonuçları':'25-Question Challenge','Cevapları sınavı teslim ettikten sonra göreceksin.','PRACTICE EXAM')}<div class="panel"><div class="row between"><h2>${ui.examDone?`${exam.filter((q,i)=>ui.examAnswers[i]===q.answer).length}/25 doğru`: 'Soruları dikkatlice cevapla'}</h2>${ui.examDone?button('Yeni deneme','newExam','small primary'):button('Sınavı bitir','submitExam','primary')}</div>${exam.map((q,i)=>`<div class="test-question"><div class="row between"><span class="tag">${i+1}/25 · ${E(q.kind)}</span>${ui.examDone?`<span class="tag ${ui.examAnswers[i]===q.answer?'green':'pink'}">${ui.examAnswers[i]===q.answer?'✓':'✕'}</span>`:''}</div><h3 style="margin-top:10px">${E(q.question)}</h3><div class="choice-list">${q.options.map((o,j)=>`<button class="choice ${ui.examDone&&(o===q.answer?'correct':ui.examAnswers[i]===o?'wrong':'')}" data-act="examAnswer" data-index="${i}" data-answer="${encodeURIComponent(o)}" ${ui.examDone?'disabled':''}>${String.fromCharCode(65+j)}. ${E(o)}</button>`).join('')}</div>${ui.examDone?`<div class="notice ${ui.examAnswers[i]===q.answer?'ok':'warn'}"><b>Doğru:</b> ${E(q.answer)}<p>${E(q.explanation)}</p><details><summary>4 seçeneğin ayrı ayrı açıklaması</summary>${q.options.map(o=>`<p><strong>${E(o)}</strong> — ${E(q.optionExplanations?.[o]||'Bu seçenek için açıklama henüz hazırlanmadı.')}</p>`).join('')}</details></div>`:''}</div>`).join('')}${!ui.examDone?`<div class="row" style="margin-top:18px">${button('Denemeyi teslim et','submitExam','primary')}</div>`:''}</div>`;}
function analytics(){
 const hist=P.listenHistory.slice(-12);
 const bars=hist.map(h=>`<div class="bar" title="${new Date(h.at).toLocaleDateString('tr-TR')}: %${h.accuracy}" style="height:${h.accuracy}%"><small>${h.accuracy}%</small></div>`).join('');
 const rows=hist.slice().reverse().map(h=>`<tr><td>${new Date(h.at).toLocaleString('tr-TR')}</td><td>${E(h.title)}</td><td>${h.accuracy}%</td></tr>`).join('');
 const retention=retentionAudit(P.reviewHistory);
 const liveWords=new Set(data.vocabulary.map(x=>x.id));const practicedWords=Object.keys(P.cards).filter(id=>liveWords.has(id)).length;const stats=[['Kelime - yeni',data.vocabulary.length-practicedWords],['Kelime - çalışılan',practicedWords],['Phrasal - çalışılan',Object.keys(P.phrasals).length],['Bekleyen tekrar',numDue()]];
 return `${section('Learning Analytics','Gelişimi yalnızca süreyle değil, hatırlama ve gerçek cevap başarısıyla izle.','MEASURE WHAT MATTERS')}
 <div class="grid metrics">${metric('✦',countMastered('cards'),'Aktif kelime')}${metric('↗',countMastered('phrasals'),'Aktif phrasal verbs')}${metric('◉',P.listenHistory.length,'Dictation denemesi')}${metric('◷',P.quizHistory.length,'25 soruluk deneme')}</div>
 <div class="grid" style="margin-top:18px"><div class="panel span-8"><h2>Listening / Dictation gelişimi</h2><p class="mini">Son ${hist.length} ölçüm · kelime eşleşme yüzdesi</p>${hist.length?`<div class="graph" aria-label="Dictation başarı grafiği">${bars}</div>`:'<div class="empty">Grafik için Listening Academy\'de dictation çöz.</div>'}</div>
 <div class="panel span-4"><h2>Bilgi durumu</h2>${stats.map(([k,v])=>`<div class="daily-item"><strong>${E(k)}</strong><b style="margin-left:auto">${v}</b></div>`).join('')}</div></div>
 <div class="panel" style="margin-top:18px"><h2>7 / 30 günlük gerçek hatırlama takibi</h2><p class="mini">${E(retention.notice)}</p>${retention.windows.map(x=>`<div class="daily-item"><strong>${x.days} gün</strong><span>Gözlenen: ${x.observed}/${x.eligible} · ${x.observedRecallRate===null?"Henüz ölçüm yok":x.observedRecallRate+"% bağımsız hatırlama"} · Zorlanarak ${x.effortful} · Takipsiz ${x.missingFollowUps}</span></div>`).join("")}</div>
 <div class="panel" style="margin-top:18px"><h2>Soru ve cümle becerileri</h2><p class="mini">${skillSummary(data.sentenceSkills,P).practiced}/340 farklı alıştırma çalışıldı. ${skillsDue(data.sentenceSkills,P).length} tekrar bekliyor. Serbest metinler otomatik puanlanmaz.</p>${link('sentenceSkills','Beceri istatistiklerini gör →')} ${link('fluencyStudio','Fluency Studio →')}</div><div class="panel" style="margin-top:18px"><h2>Listening geçmişi</h2>${hist.length?`<div class="table-wrap"><table class="simple-table"><thead><tr><th>Tarih</th><th>Görev</th><th>Doğruluk</th></tr></thead><tbody>${rows}</tbody></table></div>`:'<p class="mini">Ölçüm henüz yok.</p>'}</div>`;
}
function settings(){return `${section('Preferences & Data','Ücretsiz, hesap gerektirmeyen ve cihazda saklanan kişisel eğitim alanın.','YOUR STUDIO')}<div class="grid"><div class="panel span-7"><h2>Tercihler</h2><div class="setting-row"><div><strong>Günlük çalışma hedefi</strong><div class="mini">15–60 dakika arasında seç</div></div><select data-field="minutes"><option value="15" ${P.settings.minutes==15?'selected':''}>15 dk</option><option value="30" ${P.settings.minutes==30?'selected':''}>30 dk</option><option value="60" ${P.settings.minutes==60?'selected':''}>60 dk</option></select></div><div class="setting-row"><div><strong>Görünüm</strong><div class="mini">Aydınlık / karanlık</div></div><select data-field="theme"><option value="dark" ${P.settings.theme==='dark'?'selected':''}>Karanlık</option><option value="light" ${P.settings.theme==='light'?'selected':''}>Aydınlık</option></select></div><div class="setting-row"><div><strong>İlerleme yedeği</strong><div class="mini">Başka cihaza taşımak için JSON indir</div></div>${button('↓ JSON yedekle','export','small primary')}</div><div class="setting-row"><div><strong>Yedekten geri yükle</strong><div class="mini">Mevcut kartları silmeden öğrenme geçmişini birleştirir</div></div><label class="btn small soft" for="importFile">↑ JSON yükle</label><input type="file" id="importFile" accept=".json,application/json" hidden></div><div class="setting-row"><div><strong>Tüm ilerlemeyi sıfırla</strong><div class="mini">Bu cihazdaki çalışma kayıtlarını siler</div></div>${button('Verileri sıfırla','reset','small danger')}</div></div><div class="panel span-5"><h2>Şeffaflık</h2><p class="mini">• Ücretli API yok, giriş sistemi yok.<br>• Ders metinleri statiktir; insan sesli VOA içerikleri çevrimiçidir. Robotik MP3 sunulmuyor.<br>• TTS kullanımı tarayıcının en-US ses kurulumuna bağlıdır.<br>• Konuşma tanıma cihaz desteğine bağlıdır; bazı tarayıcılarda üçüncü taraf işleme olabilir.<br>• Cihazlar arası senkronizasyon yok; JSON yedek kullan.<br>• CEFR sertifikası veya otomatik essay notu verilmez.</p><hr class="divider"><h3>İçerik durumu</h3><p class="mini">${data.vocabulary.length} kelime/terim · ${data.phrasals.length} phrasal verb · 0 dinlenebilir robotik podcast · ${(data.authentic||[]).length+(data.voaLinkedQuizzes||[]).length} çevrimiçi VOA dersi · ${data.readings.length} okuma · ${data.sentenceSkills?.meta.totalExercises||0} soru/cümle alıştırması.</p><p class="mini">Yeni odak: 500 B2 + 500 C1 bağlamlı kelime, 500 phrasal verb + ayrı Accounting & Finance modülü. İlk sürümde doğrulanmamış kalan içerikler eklenmiş gibi gösterilmez.</p>${link('catalog','Araştırma havuzunu incele')} ${link('rapid','Hızlı kartları aç')}</div></div>${offlinePanel()}<div class="panel" style="margin-top:16px"><h2>Kaynaklar ve lisans</h2><p class="mini">Özgün ders metinleri ve uygulama kodu: MIT (eğitim içerikleri için ayrıca lisans açıklamaları README'de). Referans: CEFR Companion Volume, Oxford 5000 seviye/sıklık ilkesi, Cambridge Dictionary ve Merriam-Webster anlam doğrulama, eSpeak NG açık kaynak konuşma sentezi.</p><p class="mini">İncelenen kaynakların ücretli veya telifli sözlük verileri kopyalanmamıştır. Finans terimlerinin örnek kullanımları derlenmiştir; toplu dış uzman doğrulaması henüz yapılmamıştır.</p><div class="row"><a href="https://www.coe.int/en/web/common-european-framework-reference-languages/cefr-descriptors" target="_blank" rel="noopener">CEFR Descriptors ↗</a><a href="https://www.oxfordlearnersdictionaries.com/about/wordlists/oxford3000-5000" target="_blank" rel="noopener">Oxford 5000 ↗</a></div></div>`;}
/** The research catalog is loaded on demand, not part of the reviewed lesson deck. */
async function loadResearchCatalog(){
 if(data.catalog||ui.catalogLoading)return;
 ui.catalogLoading=true;ui.catalogError='';
 try{
  const response=await fetch('data/candidate-catalog.json');
  if(!response.ok)throw Error('Kaynak kataloğu sunucudan okunamadı ('+response.status+')');
  const catalog=await response.json();
  if(!catalog.meta||!Array.isArray(catalog.entries)||catalog.meta.total!==catalog.entries.length)throw Error('Kaynak kataloğu bozuk');
  data.catalog=catalog;
 }catch(error){ui.catalogError=String(error.message||error);}
 finally{ui.catalogLoading=false;if(ui.view==='catalog')render();}
}
function catalog(){
 const intro=section('B2/C1 Kaynak Havuzu','Kaynaklardan topluca getirilen kelime ve phrasal verb başlıklarını ara. Bu sayfa doğrulanmış eğitim modülü değildir.','CURRICULUM RESEARCH • NOT LESSONS');
 if(!data.catalog){return `${intro}<div class="panel"><div class="notice warn"><b>Öğrenme kartı değil.</b> Kaynak seviyeleri / çok anlamlılık / Amerikan kullanımı henüz editoryal kontrolden geçmedi.</div><p>${ui.catalogError?E(ui.catalogError):'Kaynak başlıkları yükleniyor…'}</p>${ui.catalogError?button('Yeniden dene','loadCatalog','small soft'):''}</div>`;}
 const rows=data.catalog.entries;
 const view=filterCandidates(rows,{kind:ui.catalogKind,level:ui.catalogLevel,query:ui.search,availability:ui.catalogAvailability,page:ui.catalogPage,pageSize:30});
 const rapidWords=new Set((data.rapid||[]).map(x=>x.word));
 ui.catalogPage=view.page;
 const kindButton=(name,text)=>button(text,'catalogKind',ui.catalogKind===name?'chip sel':'chip',`data-value="${name}"`);
 const levelButton=(name,text)=>button(text,'catalogLevel',ui.catalogLevel===name?'chip sel':'chip',`data-value="${name}"`);
 const availabilityButton=(name,text)=>button(text,'catalogAvailability',ui.catalogAvailability===name?'chip sel':'chip',`data-value="${name}"`);
 return `${intro}<div class="callout"><strong>Bu 4.851 başlık, tamamlanmış 4.851 ders değildir.</strong><p>3.647 B2/C1 kelime adayı, 1.204 phrasal verb adayı. Phrasal verb'lere B2/C1 seviyesi atanmamıştır. Öğrenme istatistikleri ve tekrar takvimi yalnızca ana Vocabulary ve Phrasal derslerinden beslenir.</p></div>
 <div class="grid metrics">${metric('▤',String(data.catalog.meta.vocabulary),'Kelime başlığı','B2/C1 kaynak seviyesi')}${metric('↗',String(data.catalog.meta.phrasal),'İfade başlığı','Seviye henüz yok')}${metric('✦',String(data.catalog.meta.lessonOverlaps),'Mevcut dersle ortak','İlgili derse geçilebilir')}${metric('⌕',String(data.catalog.meta.total-data.catalog.meta.lessonOverlaps),'Eğitime alınmamış','Anlam/örnek kontrolü gerekiyor')}</div>
 <div class="panel" style="margin-top:18px"><div class="filter" style="margin-bottom:12px">${kindButton('all','Tümü')}${kindButton('v','Genel kelimeler')}${kindButton('p','Phrasal verb adayları')}</div>
 <div class="filter" style="margin-bottom:12px">${levelButton('all','Tüm seviyeler')}${levelButton('B2','B2 kaynak listesi')}${levelButton('C1','C1 kaynak listesi')}</div>
 <div class="filter" style="margin-bottom:14px">${availabilityButton('all','Tüm kayıtlar')}${availabilityButton('lesson','Mevcut dersi olanlar')}${availabilityButton('unmade','Henüz ders değil')}</div>
 <input class="search" data-field="search" aria-label="Kaynak havuzunda ara" placeholder="Örn. compensate, take over…" value="${E(ui.search)}" autocomplete="off"><div class="row between" style="margin:14px 0"><b>${view.count} kaynak kaydı</b><span class="mini">Sayfa ${view.page+1}/${view.pageCount} · sayfada 30 kayıt</span></div>
 <div class="catalog-list">${view.items.map(x=>`<div class="catalog-entry"><div><div class="row" style="gap:7px;flex-wrap:wrap"><strong>${E(x.w)}</strong><span class="tag ${x.lesson?'green':''}">${x.lesson?'Aktif ders var':x.t==='p'?'Seviye yok':E(x.l)}</span></div><p class="mini">${x.t==='p'?'Multiword expression · Seviye doğrulanmadı':`B2/C1 kaynak adayı · ${E(x.pos.join(', ')||'Tür belirtilmedi')}`} · ${E(x.s)}</p></div><div class="row" style="flex-wrap:nowrap">${button('🔊','speak','small soft',`data-text="${encodeURIComponent(x.w)}" aria-label="Seslendir: ${E(x.w)}"`)}${x.lesson?button('Derste aç','catalogOpenLesson','small primary',`data-id="${E(x.lesson)}" data-kind="${x.t}"`):x.t==='v'&&rapidWords.has(x.w)?button('Hızlı kart','catalogOpenRapid','small soft',`data-word="${E(x.w)}"`):'<span class="mini">İnceleme bekliyor</span>'}</div></div>`).join('')||'<div class="empty">Aramanla eşleşen kayıt yok.</div>'}</div>
 <div class="row between" style="margin-top:17px">${button('← Önceki sayfa','catalogPrev','small soft',view.page===0?'disabled':'')}${button('Sonraki sayfa →','catalogNext','small soft',view.page===view.pageCount-1?'disabled':'')}</div><p class="footnote">Kaynaklar: CEFR-J, Octanove C1/C2, tema4p. Buradaki İngilizce seviyesi kaynak sınıflandırmasıdır; kişisel CEFR sertifikası değildir. Phrasal verb veri kaynağı CC BY-NC 4.0 kapsamındadır.</p></div>`;
}
function rapidPage(){
 const cards=data.rapid||[];
 const view=rapidFiltered(cards,{query:ui.rapidSearch,level:ui.rapidLevel,status:ui.rapidStatus,page:ui.rapidPage,pageSize:25},P.rapidCards);
 ui.rapidPage=view.page;
 const filtered=view.items;
 // Selection stays within visible results, including after filtering.
 const active=filtered[Math.min(ui.rapidSelection,Math.max(0,filtered.length-1))];
 const totalReviewed=cards.filter(x=>!!P.rapidCards[x.id]).length;
 const totalDue=cards.filter(x=>P.rapidCards[x.id]&&P.rapidCards[x.id].dueAt<=Date.now()).length;
 const levelButton=(value,label)=>button(label,'rapidLevel',`small ${ui.rapidLevel===value?'primary':'soft'}`,`data-value="${value}"`);
 const statusButton=(value,label)=>button(label,'rapidStatus',`small ${ui.rapidStatus===value?'primary':'soft'}`,`data-value="${value}"`);
 return `${section('Hızlı Kelime Kartları','B2/C1 İngilizce–Türkçe anlam tekrarları. Bu kartlar tam bağlamlı ders değildir.','QUICK RECALL · UNREVIEWED GLOSSES')}
 <div class="grid metrics">${metric('⚡',String(cards.length),'Hızlı kart')}${metric('◎',String(totalReviewed),'En az bir kez bakılan')}${metric('↻',String(totalDue),'Tekrar zamanı gelen')}${metric('✦',String(cards.length-totalReviewed),'Yeni')}</div>
 <div class="panel" style="margin-top:18px"><div class="row" style="flex-wrap:wrap">${levelButton('all','B2 + C1')}${levelButton('B2','B2')}${levelButton('C1','C1')} <span class="mini">·</span>${statusButton('all','Tümü')}${statusButton('new','Yeni')}${statusButton('due','Tekrar vakti')}${statusButton('seen','Çalışılan')}</div>
 <input class="search" data-field="rapidSearch" placeholder="İngilizce veya Türkçe anlam ara…" aria-label="Hızlı kart ara" value="${E(ui.rapidSearch)}" autocomplete="off">
 <p class="mini">${view.total} sonuç · Sayfa ${view.page+1}/${view.pages} · Türkçe anlamlar kaynaktan alınmıştır; editör onayı yoktur.</p>
 ${active?`<div class="panel study"><div class="row between"><span class="tag green">${E(active.level)} · ${ui.rapidDirection==='en-tr'?'EN → TR':'TR → EN'}</span><span class="mini">${Math.min(ui.rapidSelection+1,filtered.length)} / ${filtered.length}</span></div>
 <h2 style="font-size:clamp(24px,4vw,40px);margin:20px 0;text-align:center">${E(ui.rapidDirection==='en-tr'?active.word:active.tr)}</h2>
 <div class="row" style="justify-content:center">${button('🔊 en-US Dinle','rapidSpeak','small soft')}</div>
 ${ui.rapidRevealed?`<div class="notice" style="text-align:center"><strong>${E(ui.rapidDirection==='en-tr'?active.tr:active.word)}</strong></div><div class="flash-actions" style="justify-content:center">${button('Tekrar çalışacağım','rapidAgain','soft')}${button('Hatırladım ✓','rapidKnow','primary')}</div>`:`<div class="flash-actions" style="justify-content:center">${button('Cevabı göster','rapidReveal','primary')}</div>`}
 <div class="flash-actions" style="justify-content:center">${button('← Önceki kart','rapidPrevious','small soft')}${button('Sonraki kart →','rapidNext','small soft')}${button('Yönü değiştir','rapidDirection','small soft')}</div></div>`:'<p class="empty">Bu filtrede kelime yok. Diğer seviyeyi veya Tümü filtresini seçebilirsin.</p>'}
 <div class="row between" style="margin-top:16px">${button('← Önceki sayfa','rapidPrevPage','small soft',view.page===0?'disabled':'')}${button('Sonraki sayfa →','rapidNextPage','small soft',view.page>=view.pages-1?'disabled':'')}</div>
 <p class="footnote">Bu kartları doğru bildiğinde yalnızca hızlı anlam tanıma ilerlemesi kaydedilir. Gerçek aktif kelime ustalığı, listening, bağlam ve üretim için tam ders modülünde ayrıca ölçülür.</p></div>`;
}
// Original short, everyday American English expressions. Do not conflate a
// synthetic voice option with a licensed human recording or claim CEFR certification.
function expressionForToefl(x){
 return x.contexts?.includes('toefl') || (data.expressions?.meta?.legacyToeflDailyIds||[]).includes(x.id);
}
function expressionsPage(){
 const all=data.expressions?.cards||[];
 const filtered=all.filter(x=>(ui.expressionLevel==='all'||x.level===ui.expressionLevel)
   && (ui.expressionContext==='all' || (ui.expressionContext==='toefl' ? expressionForToefl(x) : !expressionForToefl(x))));
 const pages=Math.max(1,Math.ceil(filtered.length/12));
 ui.expressionPage=Math.max(0,Math.min(ui.expressionPage,pages-1));
 const rows=filtered.slice(ui.expressionPage*12,(ui.expressionPage+1)*12);
 const tabs=['all','B1','B2','C1'].map(l=>button(l==='all'?'Tümü':l,'expressionLevel',`small ${ui.expressionLevel===l?'primary':'soft'}`,`data-value="${l}"`)).join('');
 const counts=Object.fromEntries(['B1','B2','C1'].map(l=>[l,all.filter(x=>x.level===l).length]));
 const contexts=[['all','Tüm kullanım alanları'],['daily','Yalnız Daily English'],['toefl','TOEFL + Daily']].map(([v,t])=>button(t,'expressionContext',`small ${ui.expressionContext===v?'primary':'soft'}`,`data-value="${v}"`)).join('');
 return `${section('Günlük İngilizce Kalıpları','Amerikan İngilizcesinde gerçek durumlar için kısa, kullanışlı ifadeler. Her kalıp iki örnek ve mini diyalogla öğretilir.','EVERYDAY EXPRESSIONS · EN-US')}
 <div class="grid metrics">${metric('💬',String(all.length)+'/500','Hazırlanan kalıp','B1 150 · B2 210 · C1 140 hedef')}${metric('◎',String(counts.B1),'B1 kalıpları')}${metric('↗',String(counts.B2),'B2 kalıpları')}${metric('✦',String(counts.C1),'C1 kalıpları')}</div>
 <div class="notice warn" style="margin-top:18px">Bu içerik bağımsız dil editöründen geçmemiş özgün taslaktır. TOEFL + Daily etiketi sınavda çıkma garantisi veya resmî sıklık sıralaması değildir. Kalıpların insan sesli kayıtları sağlanmadı. Hafıza Koçu'ndaki cihaz sesi sentetik TTS'dir; gerçek insan sesli Listening başarısı olarak sayılmaz. CEFR seviyeleri öğretim gruplamasıdır.</div>
 <div class="row" style="margin:16px 0;flex-wrap:wrap">${tabs} ${contexts} ${button('FSRS ile kalıpları çalış','expressionPractice','primary')}</div>
 <div class="grid">${rows.map(x=>`<article class="span-6 panel"><span class="tag green">${E(x.level)}</span> <span class="tag">${expressionForToefl(x)?'TOEFL + Daily':'Daily English'}</span> ${x.category?`<span class="tag">${E(({connectors:'Bağlaç / Geçiş',collocations:'Collocation',conversation_starters:'Cümle Kalıbı'})[x.category]||x.category)}</span>`:''}<h3 style="margin:9px 0">${E(x.expression)}</h3><p><b>${E(x.tr)}</b></p><p class="mini">${E(x.usageNote)}</p><div class="notice"><strong>İki örnek</strong>${x.examples.map(ex=>`<p>${E(ex)}</p>`).join('')}</div><p class="mini"><b>Kısa diyalog:</b> ${x.dialogue.map(t=>`${E(t.speaker)}: ${E(t.text)}`).join(' · ')}</p><p class="mini">${P.expressions?.[x.id]?'FSRS tekrar kaydı mevcut':'Yeni kalıp'}</p></article>`).join('')||'<p class="empty">Bu seviyenin kartları sonraki içerik partilerinde eklenecek.</p>'}</div>
 <div class="row between" style="margin:18px 0">${button('Önceki','expressionPrev','small soft',ui.expressionPage===0?'disabled':'') }<span class="mini">Sayfa ${ui.expressionPage+1}/${pages}</span>${button('Sonraki','expressionNext','small soft',ui.expressionPage>=pages-1?'disabled':'')}</div>`;
}
// A focused multisensory practice session: no false mastery for passive reveals.
function startMemorySession(){
 ui.memoryQueue=memoryQueue(data.memoryItems||[],P,{scope:ui.memoryScope,expressionLevel:ui.memoryScope.startsWith('expression-')?ui.expressionLevel:'all',max:10});
 ui.memoryIndex=0;resetMemoryStep();
}
function resetMemoryStep(){
 ui.memoryPhase='learn';ui.memoryResult=null;ui.memoryListening=null;ui.memoryListenPlayed=false;
 ui.memoryRecall=null;ui.memoryContext=null;ui.memoryContextChoice=null;ui.memoryProduction=false;ui.memorySentence='';
}
function activeMemory(){return (data.memoryItems||[]).find(x=>x.id===ui.memoryQueue[ui.memoryIndex]);}
function memoryPage(){
 const focus=data.focus;
 if(!focus)return `${section('Hafıza Koçu','Müfredat yüklenemedi.')}`;
 const readiness=focus.meta;
 const pool=data.memoryItems||[],completed=memoryCompletion(pool,P);
 const scopes=[['all','Tümü'],['B2','500 B2'],['C1','500 C1'],['phrasal','500 Phrasal verb'],['toefl','🎓 TOEFL + Daily'],['expression','💬 Günlük kalıplar'],['expression-b1','B1 Kalıplar'],['expression-b2','B2 Kalıplar'],['expression-c1','C1 Kalıplar'],['expression-toefl','🎓 Kalıplar · TOEFL + Daily'],['expression-daily','💬 Yalnız Daily English']];
 const tabs=scopes.map(([name,label])=>button(label,'memoryScope',`small ${ui.memoryScope===name?'primary':'soft'}`,`data-value="${name}"`)).join('');
 const head=`${section('Hafıza Koçu','İşitsel tanıma, aktif hatırlama, kişisel çağrışım ve kendi cümleni oluşturma. Yalnız zamanı gelen tekrarlar ve yeni kartlar seçilir; takvim FSRS ile korunur.','RETENTION LAB · EN-US')}
 <div class="grid metrics">${metric('◎','1.000','Kelime hedefi','500 B2 + 500 C1')}${metric('↗','500','Phrasal verb hedefi')}${metric('✦',String(pool.length),'Bağlamlı çalışma kartı','Editör onayı bekliyor')}${metric('↻',String(completed.due),'Zamanı gelen tekrar')}</div>
 <div class="panel" style="margin-top:17px"><p class="mini">Müfredat, hedef listesidir; tümü tamamlanmış ders değil. Kelimeler: ${readiness.generalBreakdown.context_draft} bağlam taslağı, ${readiness.generalBreakdown.gloss_draft} hızlı anlam, ${readiness.generalBreakdown.headword_only} yalnız başlık. Phrasals: ${readiness.phrasalBreakdown.context_draft} bağlam taslağı, ${readiness.phrasalBreakdown.headword_only} yalnız başlık. <b>Yayıma hazır değil.</b></p></div>
 <div class="row" style="margin:17px 0;flex-wrap:wrap">${tabs}</div>`;
 const item=activeMemory();
 if(!item)return head+`<div class="panel study"><h2>Bugünkü oturum tamamlandı.</h2><p>Zamanı gelmeyen kartlar erken açılmaz; yeni içerik veya zamanı gelen tekrar yoksa bugün tekrar gerekmez. Kişisel ipuçların ve tekrar aralıkların bu cihazda saklanır.</p>${button('Yeni 10 kartlık oturum','memoryRestart','primary')} ${link('listening','Listening çalış')}</div>`;
 const num=ui.memoryIndex+1,total=ui.memoryQueue.length;
 const clue=P.memoryCues[item.id]||'';
 const stage=memoryStageProgress(ui.memoryPhase,ui.memoryIndex,total);
 const stagebar=`<ol class="memory-steps" aria-label="Hafıza antrenmanının aşamaları">${stage.stages.map((s,i)=>`<li class="memory-step ${s.state}" ${s.state==='current'?'aria-current="step"':''}><span class="memory-step-number">${s.state==='done'?'✓':i+1}</span><span>${E(s.label)}</span></li>`).join('')}</ol>`;
 const header=`${head}<div class="panel study memory-studio"><div class="row between"><span class="tag green">${E(item.kind==='phrasal'?'PHRASAL VERB':item.kind==='expression'?`GÜNLÜK KALIP · ${item.level}`:item.level)} · ${num}/${total}</span><span class="mini">${E(({learn:'1. Bağ kur',listen:'2. Duy ve yaz',recall:'3. Aktif hatırla',context:'4. Bağlamı anla',produce:'5. Cümle kur'})[ui.memoryPhase])}</span></div><div class="progress" role="progressbar" aria-label="Oturum ilerlemesi" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${stage.sessionPercent}" style="margin:12px 0 18px"><span style="width:${stage.sessionPercent}%"></span></div>${stagebar}`;
 if(ui.memoryPhase==='learn')return header+`<div class="small-label">Anlamı gör, bağlamı hisset, zihinsel kanca oluştur</div><h2 class="memory-word">${E(item.word)}</h2><p class="memory-meaning">${E(item.tr)}</p><p>${E(item.definition)}</p><div class="notice"><strong>Doğal kullanım</strong>${item.examples.slice(0,2).map(x=>`<p>${E(x)}</p>`).join('')}</div>${item.kind==='expression'?`<div class="notice"><strong>Kısa diyalog</strong>${(item.dialogue||[]).map(t=>`<p><b>${E(t.speaker)}:</b> ${E(t.text)}</p>`).join('')}</div>`:''}<div class="row">${button('🔊 Kelimeyi dinle','memorySpeak','small soft')}${button('▶ Cümleyi dinle ve tekrar et','memorySpeakContext','small soft')}</div><label for="memoryCue" class="small-label" style="display:block;margin-top:19px">Kişisel hafıza kancan (isteğe bağlı)</label><p class="mini">Kelimeyi kendi hayatından bir olay, küçük bir hikâye veya görsel çağrışımla ilişkilendir. Sahte etimoloji yerine kendi bağlantını kur.</p><textarea id="memoryCue" class="search" rows="2" maxlength="500" placeholder="Bu sözcüğü bana ne hatırlatıyor?">${E(clue)}</textarea><div class="flash-actions">${button('Dinleme testine geç →','memoryStart','primary')}</div></div>`;
 if(ui.memoryPhase==='listen')return header+`<div class="memory-locked">${ui.memoryResult!==null?`<h2>${E(item.word)}</h2>`:'<div class="memory-ear">♫</div><h2>Ne duydun?</h2>'}</div><p class="mini">Bu ses cihazın sentetik en-US TTS sesidir, gerçek insan sesi değildir. Dinleyip duyduğunu yaz; cihazda ses yoksa atlayabilirsin. Ses bulunmaması yazılı kelime hatırlama notunu düşürmez.</p><div class="flash-actions">${button('▶ Dinle (en-US)','memorySpeak','primary')} ${ui.memoryResult===null?button('Cihazımda ses yok, atla','memorySkipListen','small ghost'):''}</div>${ui.memoryResult===null?`<div class="input-row"><input id="memoryAnswer" aria-label="Duyduğum İngilizce ifade" class="search" autocomplete="off" placeholder="Duyduğunu İngilizce yaz">${button('Kontrol et','memoryCheckListen','primary')}</div>`:`<div class="notice ${ui.memoryListening?'ok':'warn'}">${ui.memoryListening===null?'Ses denemesi yapılmadı.':ui.memoryListening?'Doğru duydun.':'Henüz doğru çözemedin.'} <strong>${E(item.word)}</strong></div><div class="flash-actions">${button('Aktif hatırlamaya geç →','memoryNextRecall','primary')}</div>`}</div>`;
 if(ui.memoryPhase==='recall')return header+`<div class="small-label">Türkçe anlamdan İngilizceyi geri çağır</div><h2 class="memory-word">${E(item.tr)}</h2><p class="mini">Önce ipucu açmadan hatırla. Kişisel çağrışımını öğrenme aşamasında kullanabilirsin; burası bağımsız hatırlama testi.</p>${ui.memoryResult===null?`<div class="input-row"><input id="memoryAnswer" aria-label="İngilizceyi hatırla" class="search" autocomplete="off" placeholder="İngilizce ifade"><button class="btn primary" data-act="memoryCheckRecall">Kontrol et</button></div><div class="flash-actions">${button('Hatırlayamadım — cevabı göster','memoryRevealRecall','small ghost')}</div>`:`<div class="notice ${ui.memoryRecall?'ok':'warn'}">${ui.memoryRecall?'Doğru hatırladın!':'Bu kelimeyi tekrar çalışacağız.'}<p><strong>${E(item.word)}</strong> — ${E(item.definition)}</p></div><div class="flash-actions">${button('Bağlam sorusuna geç →','memoryNextContext','primary')}</div>`}</div>`;
 if(ui.memoryPhase==='context'){
  const q=memoryContextQuestion(item,data.memoryItems||[]);
  if(!q)return header+`<p class="mini">Yeterli farklı anlam seçeneği bulunmadı. Bu adım puanlanmayacak.</p>${button('Cümle kurmaya geç →','memoryNextProduce','primary')}</div>`;
  return header+`<div class="small-label">Yeni bağlam: Anlamı ezberden seç</div><div class="notice"><strong>Which meaning fits this sentence?</strong><p>${E(q.sentence)}</p></div><div class="choice-list memory-context-options">${q.choices.map((choice,i)=>button(E(choice),'memoryChooseContext',`choice ${ui.memoryContextChoice===i?'selected':''}`,`data-value="${i}" ${ui.memoryResult!==null?'disabled':''}`)).join('')}</div>${ui.memoryResult!==null?`<div class="notice ${ui.memoryContext?'ok':'warn'}">${ui.memoryContext?'Doğru anlamı bağlama yerleştirdin.':'Tekrar çalışılacak.'}<p>Doğru: ${E(q.answer)}</p></div>${button('Cümle kurmaya geç →','memoryNextProduce','primary')}`:''}</div>`;
 }
 if(ui.memoryPhase==='produce')return header+`<h2 class="memory-word">${E(item.word)}</h2><p class="memory-meaning">${E(item.tr)}</p><p class="mini">Bu ifadeyi kullanarak kendinle ilgili farklı bir İngilizce cümle yaz. Herhangi bir örneği kopyalama. Öz değerlendirmen otomatik doğrulanmış üretim başarısı değildir.</p><div class="notice">Örnek bağlam: ${E(item.example)}</div>${ui.memoryResult===null?`<textarea id="memorySentence" class="search" rows="3" placeholder="Kendi özgün İngilizce cümlen…" aria-label="Özgün İngilizce cümlen"></textarea><div class="flash-actions">${button('Cümlemi kontrol aşamasına getir','memoryCheckProduce','primary')} ${button('Bu adımı yapamadım','memorySkipProduce','small ghost')}</div>`:`<div class="notice"><strong>Senin cümlen:</strong> ${ui.memorySentence?E(ui.memorySentence):'Yazılmadı'}<p class="mini">Otomatik kontrol yalnızca yazı uzunluğunu ve hedef ifadenin aynen geçmesini görebilir; dil bilgisi ve anlam doğruluğunu kanıtlayamaz.</p>${ui.memorySentence?`<p>İfade aynen geçti mi? <b>${memorySentenceContains(ui.memorySentence,item.word)?'Evet':'Hayır (çekimlenmiş biçim olabilir)'}</b></p>`:''}</div><div class="flash-actions">${button('Cümlemi doğru kullandığımı düşünüyorum','memoryFinishYes','primary')} ${button('Emin değilim · tekrar et','memoryFinishNo','soft')}</div>`}</div>`;
 return header+`<p>Bir sorun oluştu.</p>${button('Oturumu yenile','memoryRestart','small soft')}</div>`;
}
function modalHtml(){const item=ui.modal;return `<div class="modal-wrap" role="dialog" aria-modal="true" aria-label="Kelime bilgisi"><div class="modal"><div class="row between"><span class="tag green">${E(item.level)}</span>${button('✕','closeModal','small ghost')}</div><h2>${E(item.word)}</h2><h3 style="color:var(--mint)">${E(item.tr)}</h3><p>${E(item.definition)}</p>${sentenceExamples(item)}<div class="flash-actions">${button('🔊 Dinle','speak','small soft',`data-text="${encodeURIComponent(item.word)}"`)}${button('Sözlüğe kaydet','saveWord','primary',`data-id="${item.id}"`)}</div></div></div>`;}

/** Resume-only local snapshot; progress and previous attempts are never reset. */
function snapshotReadingSession(){
 if(!ui.toeflMini||ui.toeflMiniResult)return;
 P.toeflActiveReading={version:ui.toeflMini.version||1,mode:ui.toeflMini.mode||'mini',startedAt:ui.toeflMini.startedAt,
  minutes:ui.toeflMini.minutes,ids:ui.toeflMini.questions.map(q=>q.id),answers:{...ui.toeflMiniAnswers}};
 save();
}
function restoreReadingSession(){
 const a=P.toeflActiveReading;
 if(!a||![1,2].includes(a.version)||!['mini','diagnostic'].includes(a.mode)||!Number.isFinite(a.startedAt)||!Array.isArray(a.ids))return false;
 const expectedMinutes=a.mode==='mini'?READING_MINI_MINUTES:READING_DIAGNOSTIC_MINUTES;
 const items=makeReadingDiagnostic(data.toeflReading||[]),byId=new Map(items.map(q=>[q.id,q]));
 const baseQuestions=a.ids.map(id=>byId.get(id));
 const qs=a.version===2&&baseQuestions.every(Boolean)?balanceReadingChoices(baseQuestions):baseQuestions;
 if(a.minutes!==expectedMinutes||!((a.mode==='mini'&&qs.length===9)||(a.mode==='diagnostic'&&[34,items.length].includes(qs.length)))||qs.some(x=>!x)||new Set(a.ids).size!==qs.length)return false;
 ui.toeflMini={version:a.version,mode:a.mode,minutes:a.minutes,startedAt:a.startedAt,questions:qs};
 ui.toeflMiniAnswers=Object.fromEntries(Object.entries(a.answers||{}).filter(([id,n])=>byId.has(id)&&Number.isInteger(n)&&n>=0&&n<byId.get(id).options.length));
 ui.toeflMiniResult=null;return true;
}
function finishReadingSession(){
 if(!ui.toeflMini||ui.toeflMiniResult)return;
 const m=ui.toeflMini;
 const result=m.mode==='diagnostic'?gradeReadingPractice(m.questions,ui.toeflMiniAnswers,Date.now(),'original_timed_reading_diagnostic'):gradeReadingMini(m.questions,ui.toeflMiniAnswers);
 (P.toeflAttempts??=[]).push(result);if(P.toeflAttempts.length>100)P.toeflAttempts.shift();
 ui.toeflMiniResult=result;delete P.toeflActiveReading;event('toefl-reading-practice');
}
// Original timed Writing rehearsal: drafts persist locally, but no essay or ETS grading.
function restoreWritingExam(){
 const session=validateWritingPracticeSession(P.toeflActiveWriting,data.toeflWriting||[]);
 if(!session)return false;
 const byId=new Map(data.toeflWriting.map(t=>[t.id,t]));
 ui.toeflWritingExam={...session,tasks:session.ids.map(id=>byId.get(id))};
 ui.toeflWritingExamIndex=Math.min(ui.toeflWritingExamIndex,11);
 ui.toeflWritingExamResult=null;return true;
}
function persistWritingExam(){
 if(!ui.toeflWritingExam||ui.toeflWritingExamResult)return;
 const {version,startedAt,minutes,ids,answers}=ui.toeflWritingExam;
 P.toeflActiveWriting={version,startedAt,minutes,ids:[...ids],answers:{...answers}};
 save();
}
function finishWritingExam(){
 if(!ui.toeflWritingExam||ui.toeflWritingExamResult)return;
 const session=ui.toeflWritingExam;
 const review=reviewWritingPractice(session.tasks,session.answers);
 (P.toeflWritingAttempts??=[]).push({...review,answers:{...session.answers}});
 if(P.toeflWritingAttempts.length>20)P.toeflWritingAttempts.shift();
 ui.toeflWritingExamResult=review;
 delete P.toeflActiveWriting;
 event('toefl-writing-practice');
}
function writingExamHtml(){
 const m=ui.toeflWritingExam;if(!m)return '';
 const secs=remainingSeconds(m.startedAt,m.minutes),done=ui.toeflWritingExamResult;
 const i=ui.toeflWritingExamIndex,t=m.tasks[i],current=m.answers[t.id]||'';
 const count=m.tasks.filter(task=>(m.answers[task.id]||'').trim()).length;
 const feedback=done?.review[i];
 return `<div class="panel" style="margin-top:18px"><div class="row between"><div><div class="small-label">ORIGINAL WRITING PRACTICE · NOT ETS</div><h2>12 görev · 23 dakika</h2></div><span class="tag green" id="toeflWritingClock">${done?'Bitti':`${String(Math.floor(secs/60)).padStart(2,'0')}:${String(secs%60).padStart(2,'0')}`}</span></div>
 <p class="mini">Görev ${i+1}/12 · ${count}/12 taslak girildi. Süre sayfa kapalıyken de ilerler. Taslaklar bu cihazda saklanır. Resmî TOEFL puanı veya dil değerlendirmesi üretilmez.</p>
 <p class="tag">${E(t.kind==='build_sentence'?'Build a Sentence':t.kind==='write_email'?'Write an Email':'Academic Discussion')}</p>
 <h3>${E(t.title)}</h3><p>${E(t.prompt)}</p>${t.tokens?`<p class="notice">Kullanılacak ifadeler: ${E(t.tokens.join(' · '))}</p>`:''}
 <textarea id="toeflTimedWriting" rows="${t.kind==='build_sentence'?3:8}" aria-label="TOEFL Writing taslağı" placeholder="Yanıtını İngilizce yaz" ${done?'disabled':''}>${E(current)}</textarea>
 ${feedback?`<div class="notice"><b>Görev öz değerlendirmesi:</b> ${feedback.kind==='build_sentence'?`Referans eşleşmesi: ${feedback.exactReferenceMatch?'Eşleşti':'Eşleşmedi'} · ${E(feedback.reference)}`:`${feedback.wordCount} kelime · ${E((feedback.requirements||[]).join(' | '))}<p>${E((feedback.revisionSteps||[]).join(' '))}</p>`}</div>`:''}
 <div class="row">${button('Önceki','writingExamPrev','small soft',i===0?'disabled':'')}${button('Sonraki','writingExamNext','small soft',i===11?'disabled':'')}${!done?button('Writing provasını teslim et','finishWritingExam','primary')+button('Taslağı kaydet ve çık','pauseWritingExam','small soft'):button('Kapat','exitWritingExam','small soft')}</div>
 ${done?`<div class="notice ok"><b>${done.completed}/12 görev yanıtlandı</b> · Cümle kurma görevlerinde ${done.exactReferenceMatches}/${done.buildSentenceTotal||8} referans metinle birebir eşleşme. Açık uçlu metinler puanlanmadı. Sonuç TOEFL 1–6 veya 0–120 puanı değildir.</div>`:''}</div>`;
}
const toeflLabels={complete_words:'Complete the Words',daily_life:'Read in Daily Life',academic_passage:'Read an Academic Passage',response:'Listen and Choose a Response',conversation:'Listen to a Conversation',announcement:'Listen to an Announcement',academic_talk:'Listen to an Academic Talk'};
function toeflMiniHtml(){
 const m=ui.toeflMini;
 if(!m)return '';
 const elapsed=remainingSeconds(m.startedAt,m.minutes||READING_MINI_MINUTES);
 const done=ui.toeflMiniResult;
 const answered=Object.keys(ui.toeflMiniAnswers).length;
 const pageSize=m.mode==='diagnostic'?5:m.questions.length;
 const pages=Math.ceil(m.questions.length/pageSize);
 ui.toeflReadingPage=Math.min(ui.toeflReadingPage,pages-1);
 const page=ui.toeflReadingPage,visible=m.questions.slice(page*pageSize,(page+1)*pageSize);
 return `<div class="panel" style="margin-top:16px"><div class="row between"><div><div class="small-label">ORIGINAL READING ${m.mode==='diagnostic'?'DIAGNOSTIC':'MINI TEST'} · NOT ETS</div><h2>${m.questions.length} soru · ${m.minutes||READING_MINI_MINUTES} dakika</h2></div><span class="tag green" id="toeflMiniClock">${done?'Tamamlandı':`${String(Math.floor(elapsed/60)).padStart(2,'0')}:${String(elapsed%60).padStart(2,'0')}`}</span></div><p class="mini">Süre dolunca otomatik teslim edilir. Cevaplar teslim sonrasında açılır. Bu bir resmî TOEFL denemesi, puanı veya adaptif sınav değildir.</p>
 ${m.mode==='diagnostic'?`<div class="row between"><span class="mini">Sayfa ${page+1}/${pages} · ${answered}/${m.questions.length} yanıt</span><div class="row">${button('← Önceki 5 soru','toeflReadingPrev','small soft',page===0?'disabled':'')}${button('Sonraki 5 soru →','toeflReadingNext','small soft',page>=pages-1?'disabled':'')}</div></div>`:''}
 ${visible.map((x,i)=>`<div class="test-question"><div class="row between"><span class="tag">${page*pageSize+i+1}/${m.questions.length} · ${E(toeflLabels[x.type])}</span>${done?`<span class="tag ${ui.toeflMiniAnswers[x.id]===x.answer?'green':'pink'}">${ui.toeflMiniAnswers[x.id]===x.answer?'✓':'✕'}</span>`:''}</div><h3>${E(x.title)}</h3><p class="text-body">${E(x.body)}</p><p><b>${E(x.question)}</b></p><div class="choice-list">${x.options.map((option,j)=>`<button class="choice ${done?(j===x.answer?'correct':ui.toeflMiniAnswers[x.id]===j?'wrong':''):(ui.toeflMiniAnswers[x.id]===j?'selected':'')}" data-act="toeflMiniAnswer" data-id="${E(x.id)}" data-choice="${j}" ${done?'disabled':''}>${String.fromCharCode(65+j)}. ${E(option)}</button>`).join('')}</div>${done?`<div class="notice ${ui.toeflMiniAnswers[x.id]===x.answer?'ok':'warn'}"><b>Doğru:</b> ${E(x.options[x.answer])}<p>${E(x.explanation)}</p></div>`:''}</div>`).join('')}
 ${done?`<div class="notice"><b>${done.correct}/${done.total} · özgün Reading alıştırması</b><p>Bu sonuç TOEFL 1–6 ya da 0–120 puanı değildir.</p></div>`:button(`Reading denemesini teslim et (${answered}/${m.questions.length})`,'finishToeflMini','primary')}${button('Denemeden çık','exitToeflMini','small soft')}</div>`;
}
function toeflTypedWordHtml(){
 if(ui.toeflClozeIndex===null)return '';
 const items=makeTypedWordCompletion(data.toeflReading||[]);
 const item=items[ui.toeflClozeIndex%items.length],result=ui.toeflClozeResult;
 return `<div class="panel" style="margin-top:18px"><div class="row between"><div><div class="small-label">TYPED COMPLETION · ORIGINAL AEL PRACTICE</div><h2>Eksik harfi yazarak tamamla · ${ui.toeflClozeIndex+1}/${items.length}</h2></div>${button('Kapat','closeToeflCloze','small ghost')}</div>
 <p class="mini">Bu çalışma çoktan seçmeli değildir. Eksik harfi bağlamdan çıkarıp tam İngilizce kelimeyi yaz. Resmî ETS sorusu veya sınav puanı değildir.</p>
 <h3>${E(item.title)}</h3><p>${E(item.context)}</p><div class="notice"><b>${E(item.prompt)}</b></div>
 <div class="row"><input id="toeflClozeAnswer" class="search" autocomplete="off" spellcheck="false" aria-label="Eksik kelimeyi İngilizce tamamla" maxlength="100" placeholder="Tam kelimeyi yaz" ${result?'disabled':''}/>
 ${!result?button('Kontrol et','submitToeflCloze','small primary'):button('Sonraki','nextToeflCloze','small primary')}</div>
 ${result?`<div class="notice ${result.correct?'ok':'warn'}"><b>${result.correct?'Doğru':'Tekrar çalış'}</b> · ${E(result.expected)}<p>${E(item.explanation)}</p></div>`:''}</div>`;
}
function toeflListeningPreview(){
 const list=data.toeflListening||[];const selected=list.find(x=>x.id===ui.toeflScriptId);
 return `<div class="panel" style="margin-top:18px"><h2>Listening soru türleri · transkript çalışması</h2><p class="notice warn">Bu ${list.length} senaryonun doğrulanmış ses kaydı yok. Ekrandaki çalışmalar <b>okuma destekli ön hazırlık</b> içindir; dinleme başarısı, dinleme tamamlanma kaydı veya TOEFL puanı üretmez. Gerçek insan sesli pratik için VOA bağlantılarını aç.</p>${link('authentic','VOA gerçek insan sesli kaynaklarına git')}
 <div class="grid" style="margin-top:12px">${list.map(item=>`<div class="span-6"><b>${E(item.title)}</b><p class="mini">${E(toeflLabels[item.kind])} · ${item.questions.length} soru</p>${button('Metin çalışması','toeflScriptOpen','small soft',`data-id="${item.id}"`)}</div>`).join('')}</div>
 ${selected?`<hr class="divider"><h3>${E(selected.title)}</h3><p class="notice">Metin provası (ses kaydı değildir): ${E(selected.script)}</p>${selected.questions.map((q,i)=>`<div class="test-question"><b>${E(q.question)}</b><div class="choice-list">${q.options.map((o,j)=>button(E(o),'toeflScriptAnswer','small soft',`data-q="${i}" data-choice="${j}"`)).join('')}</div>${ui.toeflScriptChoices[i]!==undefined?`<div class="notice ${ui.toeflScriptChoices[i]===q.answer?'ok':'warn'}">${E(q.explanation)}</div>`:''}</div>`).join('')}`:''}</div>`;
}
function toefl(){
 if(ui.toeflMini&&!ui.toeflMiniResult&&remainingSeconds(ui.toeflMini.startedAt,ui.toeflMini.minutes)===0)finishReadingSession();
 if(ui.toeflWritingExam&&!ui.toeflWritingExamResult&&remainingSeconds(ui.toeflWritingExam.startedAt,ui.toeflWritingExam.minutes)===0)finishWritingExam();
 const attempts=P.toeflAttempts||[],last=attempts.at(-1),advice=readingAdvice(attempts),plan=readingReviewPlan(attempts),written=(P.toeflWritingAttempts||[]).at(-1);
 return `${section('TOEFL + Daily · 2026','Günlük Amerikan İngilizcesi ve sınav hazırlığı aynı öğrenme kaydını paylaşır. Speaking değiştirilmedi.','ONE LEARNING PATH')}
 <div class="notice"><b>ETS 2026 görev yapısı:</b> Reading: Complete the Words, Read in Daily Life, Read an Academic Passage. Listening: Response, Conversation, Announcement, Academic Talk. Writing: Build a Sentence, Write an Email, Academic Discussion. Bu uygulamadaki görevler özgündür; ETS sorusu veya resmî puan değildir.</div>
 <div class="grid metrics">${metric('▤',`${(data.toeflReading||[]).length}`,'Reading alıştırması',`${(data.toeflReading||[]).reduce((n,r)=>n+r.questions.length,0)} soru`)}${metric('✎',String((data.toeflWriting||[]).length),'Writing görevi','yapısal geri bildirim')}${metric('🎧',`${(data.toeflListening||[]).length}`,'Transkript senaryosu','doğrulanmış ses yok')}${metric('◷',String(attempts.filter(x=>['original_timed_reading_mini','original_timed_reading_diagnostic'].includes(x.kind)).length),'Reading denemesi')}</div>
 <div class="panel" style="margin-top:18px"><div class="row between"><div><div class="small-label">PERSONAL LEARNING ROUTE</div><h2>Bugünkü önceliğin</h2></div><span class="tag green">Kanıta dayalı plan</span></div><p><b>Reading:</b> ${E(advice.readingRecommendation)}</p><p class="mini">${last?`Son Reading mini denemesi: ${last.correct}/${last.total}. Yalnızca çözdüğün sorulara dayalı analiz.`:'Önce mini Reading sınavını çöz; veri olmadan seviye veya zayıflık tahmini yapılmaz.'}</p><div class="row">${ui.toeflMini?'':P.toeflActiveReading?button('Yarım kalan Reading denemesine dön','resumeToeflReading','primary'):button('Reading mini deneme · 12 dk','startToeflMini','primary')}${!ui.toeflMini&&!P.toeflActiveReading?button('Reading kapsam testi · 50 soru / 30 dk','startToeflDiagnostic','small soft'):''}${link('reading','Reading soruları')}${link('writing','Writing görevleri')}${link('vocabulary','Ortak kelime tekrarları')}</div><p class="footnote">50 soruluk kapsam denemesi ETS sınavı, adaptif mod veya resmî puan değildir. Öğrenilmiş tüm soruları kullanır; tekrar çözülürken sorular tanıdık gelebilir. Yarım kalan sınav cihazda tutulur, kapatıldığında süre işlemeye devam eder.</p>
 ${written?`<p class="mini"><b>Son Writing provası:</b> ${written.completed}/12 göreve yanıt, ${written.exactReferenceMatches}/${written.buildSentenceTotal||8} cümlede referansla birebir eşleşme. Açık uçlu yazılar değerlendirilemedi; bu bir TOEFL puanı değildir.</p>`:'<p class="mini"><b>Writing:</b> Henüz süreli prova sonucu yok, yazma seviyen tahmin edilmedi.</p>'}
 <h3>Ölçülen Reading alanları</h3><div class="grid">${plan.map(x=>`<div class="span-4"><b>${E(toeflLabels[x.type])}</b><p class="mini">${x.total?`${x.correct}/${x.total} doğru (${x.accuracy}%)`:'Henüz ölçülmedi'} · ${E(x.guidance)}</p></div>`).join('')}</div></div>
 ${ui.toeflMini?toeflMiniHtml():''}
 <div class="panel" style="margin-top:18px"><h2>Complete the Words · yazarak çalışma</h2><p class="mini">Özgün kelime tamamlama bankası; seçenekleri görmeden kelimeyi kendin yazarsın. Standart Reading denemeleri önceki biçimiyle korunur.</p>${ui.toeflClozeIndex===null?button('Yazılı kelime tamamlama başlat','startToeflCloze','small primary'):''}</div>
 ${toeflTypedWordHtml()}
 <div class="panel" style="margin-top:18px"><h2>Writing · süreli prova</h2><p class="mini">Yeni provalar: 10 cümle kurma + 1 e-posta + 1 akademik tartışma. Eski 8/2/2 oturumların kayıtları da korunur. 23 dakika, taslakları kaydetme ve yapısal kontrol. ETS 2026 görev dağılımına göre hazırlanmış özgün AEL sorularıdır; resmî sınav, adaptif deneme veya puanlama değildir.</p>${ui.toeflWritingExam?'':P.toeflActiveWriting?button('Yarım kalan Writing provasına dön','resumeWritingExam','primary'):button('Writing provasını başlat · 23 dk','startWritingExam','primary')}</div>
 ${ui.toeflWritingExam?writingExamHtml():''}
 ${toeflListeningPreview()}
 <div class="panel" style="margin-top:18px"><h2>ETS resmî sınav kaynakları (harici)</h2><p class="mini">Gerçek ses, ETS örnek soruları ve otomatik puanlama yalnızca ETS tarafından sunulur. Bu kaynaklar internet ve ETS giriş koşulları gerektirebilir; AEL ilerlemesiyle otomatik senkronize değildir. Bu bağlantılar AEL testine resmî statü kazandırmaz.</p><div class="row"><a class="btn small soft" href="https://www.eu.ets.org/toefl/test-takers/ibt/prepare/sample-test.html" target="_blank" rel="noopener noreferrer">ETS ücretsiz örnek test</a><a class="btn small soft" href="https://www.ets.org/toefl/test-takers/ibt/prepare.html" target="_blank" rel="noopener noreferrer">ETS TestReady ve hazırlık</a></div></div>
 <div class="panel" style="margin-top:18px"><h2>Eksik kalan resmî sınav gereklilikleri</h2><p class="mini">Tam uzunlukta ve ETS kalibreli adaptif Reading/Listening, güvenilir ses kayıtları, geçerli 1–6 puan ölçeği, Speaking testleri ve fiziksel iPhone Safari QA henüz yok. AEL denemeleri ile gerçek sınav sonucu eşdeğer tutulamaz.</p></div>`;
}

function sentenceSkillsPage(){
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
 const cloze=ex.mode==='guided'?sentenceCloze(ex.modelAnswer,lesson.area,lesson.id):null;
 const answerInput=ex.mode==='order'?`<div class="skill-answer"><b>Seçtiğin sıra</b><p aria-live="polite">${answer?E(answer):'Kelime kartlarına dokunarak sırala.'}</p></div><div class="skill-tokens">${ex.tokens.map((token,j)=>button(E(token),'skillToken',ui.skillOrder.includes(j)?'small ghost':'small soft',`data-index="${j}" ${ui.skillOrder.includes(j)||ui.skillFeedback?'disabled':''}`)).join('')}</div><div class="row" style="margin-top:10px">${button('Son kartı geri al','skillUndo','small ghost',ui.skillOrder.length&& !ui.skillFeedback?'':'disabled')}${button('Sırayı temizle','skillClear','small ghost',ui.skillOrder.length&&!ui.skillFeedback?'':'disabled')}</div>`:
 `<label class="small-label" for="skillAnswer">${ex.mode==='guided'?'Boşluk için cevabın':'İngilizce cümlen / sorun'}</label>${cloze?`<div class="skill-prompt" lang="en">${E(cloze.prompt)}</div>`:''}<textarea id="skillAnswer" class="search" rows="3" spellcheck="false" maxlength="600" autocomplete="off" placeholder="Write in English…" ${ui.skillFeedback?'disabled':''}></textarea>`;
 const result=ui.skillFeedback?.result;
 const feedback=ui.skillFeedback?`<div class="notice ${result.automatic&&result.matched?'ok':'warn'}" role="status"><b>${result.automatic?(result.matched?'✓ Referans yanıtla eşleşti':'Referans yanıtla eşleşmedi. Bu mutlaka gramer hatası demek değildir.'):'Serbest cevap · öz değerlendirme'}</b><p><strong>Model cevap:</strong> <span lang="en">${E(ex.modelAnswer)}</span></p><p class="mini"><strong>Yapı:</strong> ${E(lesson.rule)}</p><p class="mini"><strong>Sık hata:</strong> ${E(lesson.commonError)}</p>${!result.matched&&result.automatic?`<p class="mini">Farklı ama doğru bir yanıt yazdıysan otomatik değerlendirmeyi devre dışı bırakıp öz değerlendirme kullanabilirsin.</p>${button('Alternatif doğru yanıtımı öz değerlendir','skillAlternative','small soft')}`:''}</div>
 <div class="flash-actions">${button('Hatırlayamadım · tekrar','skillGrade','small ghost','data-grade="again"')}${button('Kısmen doğru · daha erken tekrar','skillGrade','small soft','data-grade="hard"')}${button('Doğru kullandım · tekrar planla','skillGrade','primary',`data-grade="good" ${result.automatic&&!result.matched?'disabled':''}`)}</div>`:'';
 return `${overview}<div class="panel study skill-studio"><div class="row between">${button('← Ders listesi','skillBack','small ghost')}<span class="tag green">${E(SKILL_AREAS[lesson.area])} · ${i+1}/10</span></div><h2 style="margin-top:16px">${E(lesson.title)}</h2><p class="mini">${E(lesson.description)}</p><div class="progress" aria-label="Dersin ilerleyişi"><span style="width:${(i+1)*10}%"></span></div><div class="notice" style="margin:15px 0"><b>Temel kural</b><p>${E(lesson.rule)}</p></div><div class="row between"><span class="tag">${E(modeLabel)}</span>${completed?`<span class="tag">Daha önce çalışıldı · ${E(completed.status||'tekrar')}</span>`:''}</div><p style="margin-top:14px">${E(ex.task)}</p>${answerInput}${feedback}${!ui.skillFeedback?`<div class="flash-actions">${button('Cevabımı kontrol et ve örneği göster','skillCheck','primary')}</div>`:''}<hr class="divider"><div class="row between">${button('← Önceki','skillPrev','small soft',i===0?'disabled':'')}${button('Sonraki →','skillNext','small soft',i>=9?'disabled':'')}</div><p class="footnote">İlerleme yalnızca değerlendirme seçildikten ve cihaz depolamasına yazma başarılı olduktan sonra kaydedilir. Serbest yanıtlar otomatik gramer puanı değildir. Bu bölüm Speaking modülünden bağımsızdır.</p></div>`;
}
const pages={fluencyStudio:()=>fluencyPage({ui,progress:P,data,escape:E,button,link,section}),sentenceSkills:sentenceSkillsPage,home,toefl,authentic:()=>ui.authenticId?authenticDetail():ui.linkedQuizId?linkedQuizDetail():authenticLibrary(),listening:()=>ui.drill?drillDetail():listening(),vocabulary:()=>vocab(false),phrasals:()=>vocab(true),podcasts:()=>ui.episode?episodeDetail():pods(),reading,grammar,speaking,writing,conversations,pronunciation,tests,review,analytics,settings,catalog,rapid:rapidPage,memory:memoryPage,expressions:expressionsPage};
function tts(text,onStart=null){if(!('speechSynthesis'in window)){notify('Bu tarayıcıda konuşma sentezi desteklenmiyor. Podcast MP3 kayıtlarını kullanabilirsiniz.');return;}
const speak=()=>{let voices=window.speechSynthesis.getVoices(),v=voices.find(x=>x.lang.toLowerCase()==='en-us')||voices.find(x=>x.lang.toLowerCase().startsWith('en-us'));
 if(!v){notify('Cihazda Amerikan İngilizcesi (en-US) sesi bulunamadı. Podcast MP3 kayıtlarını deneyin.');return;}
 window.speechSynthesis.cancel();let utterance=new SpeechSynthesisUtterance(text);utterance.lang='en-US';utterance.voice=v;utterance.rate=ui.speed||.95;utterance.onerror=()=>notify('Seslendirme başarısız oldu; cihaz seslerini kontrol edin.');if(onStart)utterance.onstart=onStart;window.speechSynthesis.speak(utterance);};
 let voices=window.speechSynthesis.getVoices();if(voices.length)speak();else{window.speechSynthesis.onvoiceschanged=()=>{window.speechSynthesis.onvoiceschanged=null;speak();};setTimeout(()=>{if(window.speechSynthesis.getVoices().length)speak();else notify('en-US ses listesi yüklenemedi; MP3 dinleme modülleri kullanılabilir.');},1200);}}
function gradeWord(answer){let item=curr(),correct=normalize(answer)===normalize(item.word);ui.checked=correct;ui.feedback=`<b>${correct?'✓ Doğru hatırladın!':'✕ Beklenen yanıtı henüz tam hatırlayamadın.'}</b><p>Beklenen ifade: <strong>${E(item.word)}</strong> · ${E(item.example)}</p>`;ui.entry=answer;render();}
function gradeSentence(answer){
 const item=curr();const result=diffWords(answer,item.example);
 const pct=accuracy(answer,item.example);
 ui.checked=pct>=90;
 ui.feedback=`<b>${ui.checked?'✓ Cümleyi başarıyla çözdün!':'✕ Cümlenin bazı bölümleri eksik veya farklı.'}</b><p><strong>Dictation doğruluğu: %${pct}</strong></p><p>${result.map(x=>x.ok?`<span class="highlight">${E(x.word)}</span>`:`<span class="badword">${E(x.word)}</span>`).join(' ')}</p><p class="mini">Eksik duydukların kırmızı gösterilir; cümle sırası da kontrol edilir. Bu çalışmanın sesi tarayıcı en-US TTS özelliğidir.</p>`;
 ui.entry=answer;render();
}
function gradeReview(grade){let item=curr(),isPV=ui.view==='phrasals',bank=isPV?P.phrasals:P.cards,mode=ui.mode;
 if(ui.checked===false&&grade!=='again'){notify('Bu denemede yanlış yanıtlandı; tekrar gerekli olarak işlenecek.');grade='again';}
 if(ui.checked===null){notify('Önce bir alıştırmayı tamamla.');return;}
 let modality=mode==='production'?'production':['listening','sentenceListening'].includes(mode)?'listening':mode==='recognition'?'recognition':mode==='context'?'context':'recall';
 bank[item.id]=reviewItem(bank[item.id],grade,modality);P.reviewHistory.push({at:Date.now(),id:item.id,mode:modality,grade});const savedStatus=bank[item.id].status;if(event(isPV?'phrasal':'vocabulary'))notify('Tekrar kaydedildi · '+savedStatus);ui.checked=null;ui.feedback='';ui.entry='';ui.mode='intro';ui.selection=Math.min(ui.selection+1,Math.max(0,lessonItems().length-1));render();}
function recordDictation(target,answer,title){
 const detail=analyzeDictation(answer,target,data.vocabulary,P.cards),pct=detail.accuracy,parts=diffWords(answer,target);
 const msg=`<div class="notice ${pct>=80?'ok':'warn'}"><b>Dictation doğruluğu: ${pct}%</b><p>${parts.map(x=>x.ok?`<span class="highlight">${E(x.word)}</span>`:`<span class="badword">${E(x.word)}</span>`).join(' ')}</p><p class="mini">Yeşil = eşleşen, kırmızı = eksik/yanlış kelime. Sözcük sırası dikkate alınır.</p>${detail.missedWords.length?`<p class="mini">Eksik / yanlış duyulan sözcükler: ${E([...new Set(detail.missedWords)].join(', '))}</p>`:''}${detail.previouslyRecalledButMissed.length?`<p class="mini">Daha önce doğru hatırlayıp bu kayıtta kaçırdıkların: ${E(detail.previouslyRecalledButMissed.join(', '))}</p>`:''}<p class="mini">${E(detail.observation)}</p></div>`;
 P.listenHistory.push({at:Date.now(),title,...detail});if(P.listenHistory.length>600)P.listenHistory.shift();const stored=event('dictation');ui.feedback=msg;const box=document.querySelector('#dictation-feedback');if(box)box.innerHTML=msg;if(stored)notify(`Listening sonucu kaydedildi: %${pct}`);}
function updateAB(){const p=document.querySelector('#ab-info');if(p)p.textContent=`A: ${ui.a===null?'—':ui.a.toFixed(1)+'s'} · B: ${ui.b===null?'—':ui.b.toFixed(1)+'s'}${ui.clipRepeat?' · Döngü aktif':''}`;}
function resetFluency(){ui.fluencyStep=0;ui.fluencyChoice=null;ui.fluencyListened=false;ui.fluencyResult=null;ui.fluencyReveal=false;ui.fluencySaved=false;ui.fluencyWritingReport=null;}
function openFluencyReview(id,type){
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
  const m=id.match(/^(?:listening|bridge)-(.+)-q(\d+)$/);
  index=m?humanSources(data.authentic).findIndex(x=>x.id===m[1]):-1;
  step=m?Math.max(0,Number(m[2])-(type==='bridge'?1:0)):0;
 }
 if(index<0)return false;
 ui.fluencyTab=tab;ui.fluencyIndex=index;resetFluency();ui.fluencyStep=step;route('fluencyStudio');return true;
}
function execute(action,buttonEl){if((pendingDraft&&!flushDraft())||(pendingWriting&&!flushWriting()))return;const ds=buttonEl.dataset;
 switch(action){
 case 'fluencyTab':{if(!FLUENCY_TABS.some(x=>x[0]===ds.value))break;ui.fluencyTab=ds.value;ui.fluencyIndex=0;resetFluency();render();break;}
 case 'fluencyMove':{const t=ui.fluencyTab,len=t==='listening'||t==='bridge'?humanSources(data.authentic).length:t==='dictation'?dictationTargets(data.authentic).length:t==='realLife'?data.fluency.realLife.length:t==='writing'?data.fluency.writing.length:t==='thinking'?data.fluency.thinking.length:1;ui.fluencyIndex=Math.min(Math.max(0,ui.fluencyIndex+Number(ds.value)),Math.max(0,len-1));resetFluency();render();break;}
 case 'fluencyChoose':if(ui.fluencyResult)break;ui.fluencyChoice=Number(ds.index);render();break;
 case 'fluencyReveal':ui.fluencyReveal=!ui.fluencyReveal;render();break;
 case 'fluencyOpenSource':{const target=humanSources(data.authentic).find(x=>x.id===ds.id);if(!target)break;ui.authenticId=target.id;ui.linkedQuizId=null;ui.authenticAnswers={};ui.authenticListened=false;route('authentic');break;}
 case 'fluencyStepNext':{
  if(!ui.fluencySaved)break;
  const t=ui.fluencyTab;
  if(t==='realLife'){const rows=data.fluency.realLife[ui.fluencyIndex]?.steps||[];ui.fluencyStep=(ui.fluencyStep+1)%Math.max(rows.length,1);}
  else if(t==='listening'||t==='bridge'){const src=humanSources(data.authentic)[ui.fluencyIndex];const cap=src?.questions.length||1;const next=ui.fluencyStep+1+(t==='bridge'?1:0);if(next>=cap){ui.fluencyIndex=Math.min(ui.fluencyIndex+1,humanSources(data.authentic).length-1);resetFluency();render();break;}ui.fluencyStep++;}
  ui.fluencyChoice=null;ui.fluencyResult=null;ui.fluencySaved=false;ui.fluencyReveal=false;render();break;
 }
 case 'fluencyCheck':{
  if(ui.fluencyResult)break;
  const type=ui.fluencyTab;let id='',category=type,good=false,reference='',explanation='',heading='',description='',allowGood=true,accuracy=null,requiresAudio=['listening','dictation','bridge'].includes(type);
  if(requiresAudio&&!ui.fluencyListened){notify('Önce kaydı gerçekten dinlediğini onayla. Ses bağlantısı çalışmadıysa dinleme başarısı kaydedilemez.');break;}
  if(type==='listening'||type==='bridge'){
   const src=humanSources(data.authentic)[ui.fluencyIndex],qi=type==='bridge'?Math.min(ui.fluencyStep+1,(src?.questions?.length||1)-1):ui.fluencyStep,q=src?.questions?.[qi];if(!src||!q||ui.fluencyChoice===null){notify('Önce bir cevap seç.');break;}
   id=`${type}-${src.id}-q${qi}`,category='listening-comprehension';good=ui.fluencyChoice===q.answer;reference=q.options[q.answer];explanation=q.explanation;heading=good?'✓ Doğru cevap':'Henüz doğru eşleşmedi';description='Bu sonuç, dinlediğini beyan ettiğin dersin tek sorusuna dayanır; genel Listening seviyen değildir.';allowGood=good;accuracy=good?100:0;
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
  try{const next=persistFluencyReview(P,{id:r.id,type:r.type,category:r.category,grade,accuracy:r.accuracy,listened:ui.fluencyListened,requiresAudio:r.requiresAudio},safeProgressStorage);acceptPersisted(next);ui.fluencySaved=true;render();notify('Akıcılık tekrar kaydı cihazda saklandı.');}catch(err){notify('Kaydedilemedi. İlerleme değiştirilmedi: '+err.message);}break;
 }
 case 'fluencySaveDraft':{
  const item=data.fluency.writing[ui.fluencyIndex],text=document.querySelector('#fluencyWriting')?.value||'';
  if(!item)break;try{acceptPersisted(persistFluencyDraft(P,item.id,text,safeProgressStorage));notify('Yazı taslağı cihazda saklandı.');}catch(err){notify('Taslak kaydedilemedi: '+err.message);}break;
 }
 case 'fluencyWritingCheck':{
  const item=data.fluency.writing[ui.fluencyIndex],text=document.querySelector('#fluencyWriting')?.value||'';if(!item||!text.trim()){notify('Önce bir metin yaz.');break;}
  ui.fluencyWritingReport=writingAudit(text,item);/* Keep textarea DOM untouched, so unsaved draft cannot be lost. */
  const host=document.querySelector('.fluency-work');if(host){const old=host.querySelector('.fluency-audit-live');old?.remove();const aside=document.createElement('div');aside.className='notice fluency-audit-live';aside.setAttribute('role','status');let r=ui.fluencyWritingReport;const title=document.createElement('strong');title.textContent=`${r.words} kelime · ${r.sentences} cümle · ${r.paragraphs} paragraf · ${r.connectors} bağlaç`;aside.append(title);for(const message of [...r.steps,r.disclaimer]){let p=document.createElement('p');p.className='mini';p.textContent=message;aside.append(p);}host.append(aside);}break;
 }
 case 'fluencyFixError':{
  const all=[...(P.fluencyHistory||[]),...(P.skillHistory||[]).map(x=>({...x,type:'sentenceSkills',category:x.area}))].filter(x=>x.category===ds.category&&(['hard','again'].includes(x.grade)||(x.type==='sentenceSkills'&&x.autoChecked===true&&x.autoMatched===false))).sort((a,b)=>b.at-a.at);
  if(!all.length||!openFluencyReview(all[0].id,all[0].type))notify('İlgili göreve ulaşılamadı; eski kayıt korunuyor.');break;
 }
 case 'fluencyOpenDue':{
  const row=(P.fluencyHistory||[]).filter(x=>x.id===ds.id).sort((a,b)=>b.at-a.at)[0];
  if(!row||!openFluencyReview(row.id,row.type))notify('Tekrar görevine ulaşılamadı.');break;
 }
 case 'fluencyPlanGo':{if(ds.view==='sentenceSkills'){route('sentenceSkills');break;}if(ds.tab)ui.fluencyTab=ds.tab;resetFluency();route('fluencyStudio');break;}
 case 'missionCard':{const kind=ds.kind;const pool=kind==='phrasals'?data.phrasals:data.vocabulary;const idx=pool.findIndex(x=>x.id===ds.id);if(idx<0)break;ui.filter='all';ui.level='all';ui.search='';ui.selection=idx;ui.mode=P[kind==='phrasals'?'phrasals':'cards'][ds.id]?'recall':'intro';ui.checked=null;ui.feedback='';route(kind);break;}
 case 'skillArea':ui.skillArea=SKILL_AREAS[ds.value]?ds.value:'question';ui.skillLesson=null;ui.skillIndex=0;ui.skillOrder=[];ui.skillFeedback=null;render();break;
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
 case 'skillGrade':{const lesson=data.sentenceSkills?.lessons.find(l=>l.id===ui.skillLesson),ex=lesson?.exercises[ui.skillIndex];if(!lesson||!ex||!ui.skillFeedback?.result?.submitted)break;try{acceptPersisted(persistSkillReview(P,{...ex,lessonId:lesson.id},lesson.area,ds.grade,ui.skillFeedback.result,safeProgressStorage));notify('Çalışma kaydı cihazına yazıldı.');ui.skillFeedback=null;ui.skillOrder=[];if(ui.skillIndex<9)ui.skillIndex++;else ui.skillLesson=null;render();}catch(err){notify('Kaydedilemedi; mevcut kayıtlar korunuyor. JSON yedeği alın. '+err.message);}break;}
 case 'retryView':void route(ui.view);break;
 case 'goto': ui.linkedQuizId=null;ui.linkedAnswers={};ui.authenticId=null;ui.authenticAnswers={};ui.authenticTranscript=false;ui.episode=null;ui.reading=null;ui.toeflReadingId=null;ui.drill=null;ui.exam=null;ui.filter='all';ui.level='all';ui.search='';ui.selection=0;ui.mode='intro';ui.quizChoices={};ui.feedback='';ui.transcript=false;ui.catalogPage=0;route(ds.view);break;
 case 'expressionLevel':ui.expressionLevel=ds.value;ui.expressionPage=0;render();break;
 case 'expressionContext':ui.expressionContext=ds.value;ui.expressionPage=0;render();break;
 case 'expressionPrev':ui.expressionPage=Math.max(0,ui.expressionPage-1);render();break;
 case 'expressionNext':ui.expressionPage++;render();break;
 case 'expressionPractice':ui.memoryScope=ui.expressionContext==='all'?(ui.expressionLevel==='all'?'expression':`expression-${ui.expressionLevel.toLowerCase()}`):`expression-${ui.expressionContext}`;ui.memoryQueue=[];void route('memory');break;
 case 'memoryScope':ui.memoryScope=ds.value;ui.expressionLevel='all';startMemorySession();render();break;
 case 'memoryRestart':startMemorySession();render();break;
 case 'memorySpeak':{const item=activeMemory();if(item)tts(item.word,ui.memoryPhase==='listen'?()=>{ui.memoryListenPlayed=true;}:null);break;}
 case 'memorySpeakContext':{const item=activeMemory();if(item)tts(item.example);break;}
 case 'memoryStart':{
  const cue=document.querySelector('#memoryCue')?.value?.trim()||'';
  const item=activeMemory();if(cue)P.memoryCues[item.id]=cue;else delete P.memoryCues[item.id];
  save();ui.memoryPhase='listen';ui.memoryResult=null;render();break;}
 case 'memorySkipListen':ui.memoryListening=null;ui.memoryResult='skipped';render();break;
 case 'memoryCheckListen':{
  const item=activeMemory(),answer=document.querySelector('#memoryAnswer')?.value||'';
  if(!ui.memoryListenPlayed){notify('Önce sesi dinle; en-US sesin yoksa Dinlemeyi atla seç.');return;}
  if(!answer.trim()){notify('Önce duyduğunu yaz veya ses yoksa atla.');return;}
  ui.memoryListening=memoryAnswer(answer,item.word);ui.memoryResult='graded';render();break;}
 case 'memoryNextRecall':ui.memoryPhase='recall';ui.memoryResult=null;render();break;
 case 'memoryRevealRecall':ui.memoryRecall=false;ui.memoryResult='revealed';render();break;
 case 'memoryCheckRecall':{
  const item=activeMemory(),answer=document.querySelector('#memoryAnswer')?.value||'';
  if(!answer.trim()){notify('Yanıtını yaz veya hatırlayamıyorsan cevabı göster.');return;}
  ui.memoryRecall=memoryAnswer(answer,item.word);ui.memoryResult='graded';render();break;}
 case 'memoryNextContext':ui.memoryPhase='context';ui.memoryResult=null;render();break;
 case 'memoryChooseContext':{
  const item=activeMemory(),q=memoryContextQuestion(item,data.memoryItems||[]);
  if(!q||ui.memoryResult!==null)break;
  const i=Number(ds.value);
  if(!Number.isInteger(i)||i<0||i>=q.choices.length)break;
  ui.memoryContextChoice=i;ui.memoryContext=q.choices[i]===q.answer;
  ui.memoryResult='graded';render();break;}
 case 'memoryNextProduce':ui.memoryPhase='produce';ui.memoryResult=null;render();break;
 case 'memorySkipProduce':ui.memorySentence='';ui.memoryResult='skipped';render();break;
 case 'memoryCheckProduce':{
  const sentence=document.querySelector('#memorySentence')?.value?.trim()||'';
  if(sentence.split(/\s+/).length<4){notify('En az dört kelimelik bir cümle yaz veya yapamadım seç.');return;}
  ui.memorySentence=sentence;ui.memoryResult='review';render();break;}
 case 'memoryFinishYes':case 'memoryFinishNo':{
  const item=activeMemory();if(!item||ui.memoryResult===null)return;
  const selfChecked=action==='memoryFinishYes'&&ui.memorySentence.length>0;
  const trial={listeningCorrect:ui.memoryListening,recallCorrect:ui.memoryRecall===true,contextCorrect:ui.memoryContext,productionConfirmed:selfChecked};
  const summary=recordMemoryReview(P,item,trial);P.reviewHistory.push({at:Date.now(),id:item.lessonId,mode:'memory',grade:summary.grade});
  if(event('memory'))notify(summary.grade==='again'?'Henüz hatırlanamadı · 15 dk tekrar':'FSRS tekrar zamanı kaydedildi');
  ui.memoryIndex++;resetMemoryStep();render();break;}
 case 'rapidLevel':ui.rapidLevel=ds.value;ui.rapidPage=0;ui.rapidSelection=0;ui.rapidRevealed=false;render();break;
 case 'rapidStatus':ui.rapidStatus=ds.value;ui.rapidPage=0;ui.rapidSelection=0;ui.rapidRevealed=false;render();break;
 case 'rapidPrevPage':ui.rapidPage=Math.max(0,ui.rapidPage-1);ui.rapidSelection=0;ui.rapidRevealed=false;render();break;
 case 'rapidNextPage':ui.rapidPage++;ui.rapidSelection=0;ui.rapidRevealed=false;render();break;
 case 'rapidReveal':ui.rapidRevealed=true;render();break;
 case 'rapidDirection':ui.rapidDirection=ui.rapidDirection==='en-tr'?'tr-en':'en-tr';ui.rapidRevealed=false;render();break;
 case 'rapidPrevious':ui.rapidSelection=Math.max(0,ui.rapidSelection-1);ui.rapidRevealed=false;render();break;
 case 'rapidNext':{
  const view=rapidFiltered(data.rapid||[],{query:ui.rapidSearch,level:ui.rapidLevel,status:ui.rapidStatus,page:ui.rapidPage},P.rapidCards);
  if(ui.rapidSelection+1<view.items.length)ui.rapidSelection++;
  else if(view.page<view.pages-1){ui.rapidPage++;ui.rapidSelection=0;}
  ui.rapidRevealed=false;render();break;}
 case 'rapidSpeak':{
  const view=rapidFiltered(data.rapid||[],{query:ui.rapidSearch,level:ui.rapidLevel,status:ui.rapidStatus,page:ui.rapidPage},P.rapidCards);
  const item=view.items[Math.min(ui.rapidSelection,view.items.length-1)];if(item)tts(item.word);break;}
 case 'rapidKnow': case 'rapidAgain':{
  const view=rapidFiltered(data.rapid||[],{query:ui.rapidSearch,level:ui.rapidLevel,status:ui.rapidStatus,page:ui.rapidPage},P.rapidCards);
  const item=view.items[Math.min(ui.rapidSelection,view.items.length-1)];if(!item||!ui.rapidRevealed)break;
  P.rapidCards[item.id]=rapidRecord(P.rapidCards[item.id],action==='rapidKnow');
  event('rapid');ui.rapidRevealed=false;
  // Refreshed status filter may remove this card; do not skip the next one.
  if(ui.rapidStatus==='all'||ui.rapidStatus==='seen'){
   if(ui.rapidSelection+1<view.items.length)ui.rapidSelection++;
   else if(view.page<view.pages-1){ui.rapidPage++;ui.rapidSelection=0;}
  }
  render();break;}
 case 'loadCatalog':loadResearchCatalog();break;
 case 'catalogKind':ui.catalogKind=ds.value;ui.catalogPage=0;render();break;
 case 'catalogLevel':ui.catalogLevel=ds.value;ui.catalogPage=0;render();break;
 case 'catalogAvailability':ui.catalogAvailability=ds.value;ui.catalogPage=0;render();break;
 case 'catalogPrev':ui.catalogPage=Math.max(0,ui.catalogPage-1);render();break;
 case 'catalogNext':ui.catalogPage++;render();break;
 case 'catalogOpenRapid':ui.rapidSearch=ds.word;ui.rapidLevel='all';ui.rapidStatus='all';ui.rapidPage=0;ui.rapidSelection=0;ui.rapidRevealed=false;route('rapid');break;
 case 'catalogOpenLesson':{const kind=ds.kind==='p'?'phrasals':'vocabulary',pool=ds.kind==='p'?data.phrasals:data.vocabulary,idx=pool.findIndex(x=>x.id===ds.id);if(idx<0){notify('Ders kaydı bulunamadı.');break;}ui.filter='all';ui.level='all';ui.search='';ui.selection=idx;ui.mode='intro';route(kind);break;}
 case 'toeflOpen':ui.filter='toefl';ui.level='all';ui.search='';ui.selection=0;ui.mode='intro';route(ds.kind==='phrasals'?'phrasals':'vocabulary');break;
 case 'offlineCheck':void showOfflineStatus({repair:true});break;
 case 'offlineTrialStart':{
  const trial=newOfflineTrial(Date.now(),`${Date.now()}-${Math.random().toString(36).slice(2)}`);
  P.offlineTrial=trial;P.offlineTrialRestored=false;globalThis.__aelOfflineTrialStartedHere=true;const trialSaved=event('offline_trial_started');
  if(trialSaved)notify('İşaret kaydedildi. Şimdi uçak moduna geçip uygulamayı yeniden aç.');render();break;}
 case 'offlineTrialFinish':{
  const trial=P.offlineTrial;
  if(!trial){notify('Önce uçak modu test işaretini oluştur.');break;}
  void (async()=>{
   const cache=await checkOffline();
   const verdict=verifyOfflineTrial(trial,{marker:trial.marker,cacheReady:cache.ready,
      networkOffline:navigator.onLine===false,appReloaded:Boolean(P.offlineTrialRestored),now:Date.now()});
   P.offlineTrialResult=verdict;save();
   notify(verdict.reason);render();
  })();break;}

 case 'filter':ui.filter=ds.value;ui.selection=0;ui.checked=null;ui.feedback='';render();break;
 case 'level':ui.level=ds.level;render();break;
 case 'select':ui.selection=Number(ds.index);ui.checked=null;ui.feedback='';ui.mode='intro';render();document.querySelector('.study')?.scrollIntoView({behavior:'smooth',block:'start'});break;
 case 'prev':ui.selection=Math.max(0,ui.selection-1);ui.checked=null;ui.feedback='';ui.mode='intro';render();break;
 case 'next':ui.selection=(ui.selection+1)%Math.max(1,(ui.view==='vocabulary'||ui.view==='phrasals')?lessonItems().length:ui.view==='speaking'?4:ui.view==='writing'?4:1);ui.checked=null;ui.feedback='';ui.mode='intro';render();break;
 case 'mode':ui.mode=ds.mode;ui.checked=null;ui.feedback='';ui.entry='';render();break;
 case 'speak':tts(decodeURIComponent(ds.text||''));break;
 case 'practiceChoice':if(ui.checked!==null)return;let item=curr(),opts=optionsFor(item,ui.view==='phrasals'),chosen=opts[Number(ds.index)];ui.entry=ds.index;ui.checked=chosen?.id===item.id;ui.feedback=`<b>${ui.checked?'✓ Doğru seçim.':'✕ Yanlış seçim.'}</b><p>${E(item.word)}: ${E(item.tr)} · ${E(item.example)}</p>`;render();break;
 case 'gradeWord':gradeWord(document.querySelector('#answer')?.value||'');break;
 case 'gradeSentence':gradeSentence(document.querySelector('#answer')?.value||'');break;
 case 'productionCheck':{let answer=document.querySelector('#answer')?.value||'';if(!answer.trim()){notify('Önce kendi cümleni yaz.');return;}let item=curr(),mentions=normalize(answer).includes(normalize(item.word));ui.checked=mentions;ui.feedback=`<b>Örnek cümle:</b> ${E(item.example)}<p>Senin cümlen: ${E(answer)}</p><p>${mentions?'Hedef ifade cümlende geçiyor.':'Hedef ifadeyi kendi cümlende kullanmayı dene.'} Bu öz değerlendirmedir, otomatik dil doğrulaması değildir. Doğru kullandığından emin değilsen “Tekrar gerekli”yi seç.</p>`;render();break;}
 case 'grade':gradeReview(ds.grade);break;
 case 'voaFilter':ui.voaFilter=ds.value;ui.voaPage=0;render();break;
 case 'voaPrev':ui.voaPage=Math.max(0,ui.voaPage-1);render();break;
 case 'voaNext':ui.voaPage++;render();break;
 case 'linkedQuizOpen':stopAudio();ui.authenticId=null;ui.linkedQuizId=ds.id;ui.linkedAnswers={};ui.linkedListened=false;ui.view='authentic';location.hash='/authentic';render();scrollTo(0,0);break;
 case 'linkedQuizBack':ui.linkedQuizId=null;ui.linkedAnswers={};ui.linkedListened=false;render();break;
 case 'linkedQuizAnswer':{const lesson=(data.voaLinkedQuizzes||[]).find(x=>x.id===ui.linkedQuizId),i=Number(ds.q),choice=Number(ds.choice);if(!lesson||ui.linkedAnswers[i]!==undefined||!lesson.questions[i]||!Number.isInteger(choice))break;const q=lesson.questions[i];if(choice<0||choice>=q.options.length)break;ui.linkedAnswers[i]=choice;const wrap=document.querySelector(`[data-linked-q="${i}"]`);if(wrap){wrap.querySelectorAll('button.choice').forEach(b=>b.disabled=true);const f=wrap.querySelector('.auth-feedback');if(f)f.innerHTML=`<div class="notice ${choice===q.answer?'ok':'warn'}">${choice===q.answer?'✓ Doğru':'✕ Tekrar dinle'} · ${E(q.explanation)}${linkedEvidence(q)}</div>`;}break;}
 case 'linkedQuizFinish':{const lesson=(data.voaLinkedQuizzes||[]).find(x=>x.id===ui.linkedQuizId);if(!lesson)break;const n=lesson.questions.length;if(!ui.linkedListened){notify('Dinlemeyi tamamladıysan bunu onayla. Yalnızca soru çözdüysen sonucu Listening olarak kaydetmeyelim.');break;}if(Object.keys(ui.linkedAnswers).length!==n){notify(`Önce ${n} sorunun tamamını cevapla.`);break;}const correct=lesson.questions.filter((q,i)=>ui.linkedAnswers[i]===q.answer).length;P.authenticLessons[lesson.id]={correct,total:n,completedAt:Date.now(),audioPlaybackSelfReported:true,audioPlaybackVerified:false,assessmentType:'source-linked-comprehension'};if(event('source-comprehension-quiz'))notify(`Kaynak bağlantılı dinleme soruları: ${correct}/${n}`);break;}
 case 'authenticOpen':stopAudio();ui.authenticId=ds.id;ui.authenticAnswers={};ui.authenticTranscript=false;ui.authenticListened=false;ui.view='authentic';ui.speed=1;location.hash='/authentic';render();scrollTo(0,0);break;
 case 'authenticBack':stopAudio();ui.authenticId=null;ui.authenticAnswers={};ui.authenticTranscript=false;ui.authenticListened=false;render();break;
 case 'authenticToggleTranscript':{ui.authenticTranscript=!ui.authenticTranscript;const t=document.querySelector('#authenticTranscript');if(t)t.hidden=!ui.authenticTranscript;const note=document.querySelector('#authenticTranscriptNote');if(note)note.hidden=ui.authenticTranscript;buttonEl.textContent=ui.authenticTranscript?'Metni gizle':'Metni göster';break;}
 case 'authenticAnswer':{const lesson=(data.authentic||[]).find(x=>x.id===ui.authenticId),i=Number(ds.q),choice=Number(ds.choice);if(!lesson||ui.authenticAnswers[i]!==undefined||!lesson.questions[i]||!Number.isInteger(choice))break;const q=lesson.questions[i];if(choice<0||choice>=q.options.length)break;ui.authenticAnswers[i]=choice;const wrap=document.querySelector(`[data-auth-q="${i}"]`);if(wrap){wrap.querySelectorAll('button.choice').forEach((b,j)=>{b.disabled=true;if(j===choice)b.classList.add('correct');});const f=wrap.querySelector('.auth-feedback');if(f)f.innerHTML=`<div class="notice ${choice===q.answer?'ok':'warn'}">${choice===q.answer?'✓ Doğru':'✕ Tekrar çalış'} · ${E(q.explanation)}${authenticEvidence(q)}</div>`;}break;}
 case 'authenticFinish':{const lesson=(data.authentic||[]).find(x=>x.id===ui.authenticId);if(!lesson)break;const n=lesson.questions.length;if(!ui.authenticListened){notify('Kaydı dinlediysen bunu onayla; yalnızca soruları cevaplamak dinleme tamamlandı sayılmaz.');break;}if(Object.keys(ui.authenticAnswers).length!==n){notify(`Önce ${n} sorunun tamamını cevapla.`);break;}const correct=lesson.questions.filter((q,i)=>ui.authenticAnswers[i]===q.answer).length;P.authenticLessons[lesson.id]={correct,total:n,completedAt:Date.now(),audioPlaybackSelfReported:true,audioPlaybackVerified:false,assessmentType:'publisher-transcript-comprehension'};if(event('authentic-comprehension-selfreport'))notify(`Dinlediğini beyan ettiğin kaydın soruları: ${correct}/${n}`);break;}
 case 'openEpisode':stopAudio();ui.episode=null;route('podcasts');notify('Robotik podcast dinleme kapatıldı. Gerçek insan sesli VOA derslerini açabilirsin.');break;
 case 'backPods':ui.episode=null;ui.feedback='';ui.transcript=false;stopAudio();render();break;
 case 'openDrill':stopAudio();ui.drill=null;route('listening');notify('Robotik ses alıştırmaları dinlemeye kapalıdır.');break;
 case 'backListening':ui.drill=null;ui.feedback='';stopAudio();render();break;
 case 'openToeflReading':ui.toeflReadingId=ds.id;ui.reading=null;ui.view='reading';ui.quizChoices={};location.hash='/reading';render();scrollTo(0,0);break;
 case 'backToeflReading':ui.toeflReadingId=null;ui.quizChoices={};render();break;
 case 'completeToeflReading':{let r=(data.toeflReading||[]).find(x=>x.id===ds.id);if(!r)break;let answered=r.questions.filter((_,i)=>ui.quizChoices[`tr-${r.id}-${i}`]!==undefined).length;if(answered!==r.questions.length){notify('Tüm soruları yanıtla.');break;}let correct=r.questions.filter((q,i)=>ui.quizChoices[`tr-${r.id}-${i}`]===q.answer).length;P.lessons[r.id]={at:Date.now(),correct,total:r.questions.length};if(event('reading'))notify(`TOEFL Reading alıştırması kaydedildi: ${correct}/${r.questions.length} (resmî puan değil)`);break;}
 case 'openReading':ui.reading=ds.id;ui.toeflReadingId=null;ui.view='reading';ui.quizChoices={};location.hash='/reading';render();scrollTo(0,0);break;
 case 'backReading':ui.reading=null;ui.quizChoices={};render();break;
 case 'answerQuestion':ui.quizChoices[ds.key]=Number(ds.index);render();break;
 case 'completeEpisode':notify('Robotik podcastler kapatıldı; önceki ilerleme kayıtları korundu.');break;
 case 'completeReading':{let r=data.readings.find(x=>x.id===ds.id),answered=r.questions.filter((_,i)=>ui.quizChoices[`rd-${r.id}-${i}`]!==undefined).length;if(answered<r.questions.length){notify('Lütfen tüm anlama sorularını cevapla.');return;}let correct=r.questions.filter((q,i)=>ui.quizChoices[`rd-${r.id}-${i}`]===q.answer).length;P.lessons[r.id]={at:Date.now(),correct,total:r.questions.length};if(event('reading'))notify(`Reading tamamlandı: ${correct}/${r.questions.length}`);break;}
 case 'toggleTranscript':ui.transcript=!ui.transcript;let time=audio?.currentTime||0,playing=audio?!audio.paused:false;render();if(audio){audio.currentTime=time;if(playing)audio.play().catch(()=>{});}break;
 case 'checkDrill':notify('Robotik alıştırmalar kapatıldı.');break;
 case 'checkDictation':notify('Robotik podcastler kapatıldı.');break;
 case 'setA':if(audio){ui.a=audio.currentTime;updateAB();}break;
 case 'setB':if(audio){ui.b=audio.currentTime;updateAB();}break;
 case 'clearAB':ui.a=null;ui.b=null;ui.clipRepeat=false;updateAB();break;
 case 'repeat':if(ui.a===null||ui.b===null||ui.a>=ui.b){notify('Önce A ve B noktalarını sırayla seç.');return;}ui.clipRepeat=!ui.clipRepeat;updateAB();buttonEl.textContent=ui.clipRepeat?'⟳ Döngü açık':'⟳ A–B döngü';break;
 case 'seekSegment':playSegment(Number(ds.index));break;
 case 'playFocus':notify('Robotik podcastler kapatıldı.');break;
 case 'relisten':ui.transcript=false;render();if(audio)audio.play().catch(()=>{});break;
 case 'saveFocus':{const ep=data.episodes.find(x=>x.id===ui.episode);let m=(ep.focus.match(/\b[a-zA-Z]+\b/g)||[]).find(w=>data.vocabulary.some(v=>v.word.toLowerCase()===w.toLowerCase()));if(!m){notify('Bu parçada sözlükte eşleşen tekil kelime bulunamadı.');break;}let v=data.vocabulary.find(v=>v.word===m.toLowerCase());if(v){P.cards[v.id]??={status:'Yeni',due:Date.now(),attempts:0};if(save())notify(v.word+' sözlüğe kaydedildi.');}break;}
 case 'lookup':ui.modal=data.vocabulary.find(x=>x.id===ds.id);render();break;
 case 'closeModal':ui.modal=null;render();break;
 case 'saveWord':{let v=data.vocabulary.find(x=>x.id===ds.id);if(v){P.cards[v.id]??={status:'Yeni',due:Date.now(),attempts:0};if(save())notify('Sözlüğe kaydedildi: '+v.word);ui.modal=null;render();}break;}
 case 'reviewOpen':ui.view=ds.kind;ui.filter='all';ui.search='';ui.mode='recall';ui.feedback='';ui.checked=null;ui.selection=(ds.kind==='phrasals'?data.phrasals:data.vocabulary).findIndex(x=>x.id===ds.id);location.hash='/'+ui.view;render();scrollTo(0,0);break;
 case 'startExam':{let recent=P.quizHistory.flatMap(x=>x.ids||[]),exam=buildExam(data.bank,recent,Date.now());ui.exam=exam;ui.examAnswers={};ui.examDone=false;render();break;}
 case 'examAnswer':if(ui.examDone)return;ui.examAnswers[Number(ds.index)]=decodeURIComponent(ds.answer||'');document.querySelectorAll(`[data-act="examAnswer"][data-index="${ds.index}"]`).forEach(b=>b.classList.toggle('selected',b===buttonEl));break;
 case 'submitExam':{if(ui.examDone||!ui.exam)return;const answered=Object.keys(ui.examAnswers).length;if(answered<25&&!confirm(`${answered}/25 soruyu yanıtladın. Sınavı şimdi teslim etmek istiyor musun?`))return;let correct=ui.exam.filter((q,i)=>ui.examAnswers[i]===q.answer).length;P.quizHistory.push({at:Date.now(),correct,score:Math.round(correct*4),ids:ui.exam.map(x=>x.id)});if(P.quizHistory.length>100)P.quizHistory.shift();event('exam');ui.examDone=true;render();scrollTo(0,0);break;}
 case 'exitExam':ui.exam=null;ui.examAnswers={};ui.examDone=false;render();break;
 case 'newExam':ui.exam=null;ui.examDone=false;execute('startExam',buttonEl);break;
 case 'startToeflMini':case 'startToeflDiagnostic':{if(ui.toeflMini||P.toeflActiveReading){notify('Önce mevcut Reading oturumunu tamamla veya devam et.');break;}const mode=action==='startToeflDiagnostic'?'diagnostic':'mini';const n=(P.toeflAttempts||[]).filter(x=>['original_timed_reading_mini','original_timed_reading_diagnostic'].includes(x.kind)).length;ui.toeflMini={version:2,mode,minutes:mode==='diagnostic'?READING_DIAGNOSTIC_MINUTES:READING_MINI_MINUTES,questions:balanceReadingChoices(mode==='diagnostic'?makeReadingDiagnostic(data.toeflReading||[]):makeReadingMini(data.toeflReading||[],n)),startedAt:Date.now()};ui.toeflMiniAnswers={};ui.toeflMiniResult=null;ui.toeflReadingPage=0;snapshotReadingSession();ui.view='toefl';render();break;}
 case 'resumeToeflReading':{if(!restoreReadingSession()){notify('Oturum kaydı doğrulanamadı. Önce JSON ilerleme yedeği al.');break;}ui.view='toefl';ui.toeflReadingPage=0;render();break;}
 case 'toeflReadingPrev':ui.toeflReadingPage=Math.max(0,ui.toeflReadingPage-1);render();break;
 case 'toeflReadingNext':if(ui.toeflMini)ui.toeflReadingPage=Math.min(Math.ceil(ui.toeflMini.questions.length/5)-1,ui.toeflReadingPage+1);render();break;
 case 'toeflMiniAnswer':{if(!ui.toeflMini||ui.toeflMiniResult)break;if(remainingSeconds(ui.toeflMini.startedAt,ui.toeflMini.minutes)===0){execute('finishToeflMini',buttonEl);break;}const item=ui.toeflMini.questions.find(x=>x.id===ds.id);const choice=Number(ds.choice);if(item&&Number.isInteger(choice)&&choice>=0&&choice<item.options.length){ui.toeflMiniAnswers[item.id]=choice;snapshotReadingSession();render();}break;}
 case 'finishToeflMini':{finishReadingSession();render();break;}
 case 'exitToeflMini':ui.toeflMini=null;ui.toeflMiniAnswers={};ui.toeflMiniResult=null;render();break;
 case 'startToeflCloze':{const items=makeTypedWordCompletion(data.toeflReading||[]);ui.toeflClozeIndex=(P.toeflAttempts||[]).filter(x=>x.kind==='original_typed_word_completion').length%items.length;ui.toeflClozeResult=null;render();break;}
 case 'submitToeflCloze':{if(ui.toeflClozeIndex===null||ui.toeflClozeResult)break;
  const items=makeTypedWordCompletion(data.toeflReading||[]),item=items[ui.toeflClozeIndex];
  const value=document.querySelector('#toeflClozeAnswer')?.value||'';
  if(!value.trim()){notify('Önce eksik kelimeyi yaz.');break;}
  const result=checkTypedWordCompletion(item,value);ui.toeflClozeResult=result;
  (P.toeflAttempts??=[]).push(result);if(P.toeflAttempts.length>100)P.toeflAttempts.shift();save();render();break;}
 case 'nextToeflCloze':{if(ui.toeflClozeIndex!==null&&ui.toeflClozeResult){const items=makeTypedWordCompletion(data.toeflReading||[]);ui.toeflClozeIndex=(ui.toeflClozeIndex+1)%items.length;ui.toeflClozeResult=null;render();}break;}
 case 'closeToeflCloze':ui.toeflClozeIndex=null;ui.toeflClozeResult=null;render();break;
 case 'startWritingExam':{if(ui.toeflWritingExam||P.toeflActiveWriting){notify('Önce mevcut Writing oturumunu tamamla.');break;}
  const tasks=makeWritingPractice(data.toeflWriting||[],(P.toeflWritingAttempts||[]).length);
  ui.toeflWritingExam={version:2,startedAt:Date.now(),minutes:WRITING_PRACTICE_MINUTES,ids:tasks.map(t=>t.id),tasks,answers:{}};
  ui.toeflWritingExamIndex=0;ui.toeflWritingExamResult=null;if(!persistWritingExam()){ui.toeflWritingExam=null;render();break;}ui.view='toefl';render();break;}
 case 'resumeWritingExam':{if(!restoreWritingExam()){notify('Writing oturumu kaydı doğrulanamadı; JSON yedeğinizi koruyun.');break;}ui.view='toefl';render();break;}
 case 'writingExamPrev':if(ui.toeflWritingExam)ui.toeflWritingExamIndex=Math.max(0,ui.toeflWritingExamIndex-1);render();break;
 case 'writingExamNext':if(ui.toeflWritingExam)ui.toeflWritingExamIndex=Math.min(11,ui.toeflWritingExamIndex+1);render();break;
 case 'pauseWritingExam':if(!persistWritingExam())break;ui.toeflWritingExam=null;ui.toeflWritingExamResult=null;ui.toeflWritingExamIndex=0;render();notify('Writing taslağı korundu. Süre işlemeye devam eder.');break;
 case 'finishWritingExam':finishWritingExam();render();break;
 case 'exitWritingExam':ui.toeflWritingExam=null;ui.toeflWritingExamResult=null;ui.toeflWritingExamIndex=0;render();break;
 case 'toeflScriptOpen':ui.toeflScriptId=ds.id;ui.toeflScriptChoices={};render();break;
 case 'toeflScriptAnswer':{const item=(data.toeflListening||[]).find(x=>x.id===ui.toeflScriptId);const i=Number(ds.q),j=Number(ds.choice);if(item?.questions[i]&&Number.isInteger(j)&&j>=0&&j<item.questions[i].options.length){ui.toeflScriptChoices[i]=j;render();}break;}
 case 'toeflWritingHints':{const t=(data.toeflWriting||[])[ui.toeflWritingIndex];if(!t||t.kind==='build_sentence')break;const answer=document.querySelector('#toeflWriting')?.value||'';P.writing['toefl:'+t.id]=answer;const result=writingChecklist(t,answer);ui.toeflWritingFeedback={correct:result.inSuggestedRange,message:`${result.words} kelime · ${result.inSuggestedRange?'Önerilen alıştırma aralığında':'Önerilen aralık dışında'} (resmî TOEFL eşiği değildir).`,notes:[...result.observations,...result.revisionSteps,`Ölçülebilenler: ${result.observableMetrics.sentenceCount} cümle, ${result.observableMetrics.paragraphCount} paragraf; dil doğruluğu ölçülmedi.`]};event('writing');render();break;}
 case 'writingMode':ui.writingMode=ds.mode==='toefl'?'toefl':'daily';ui.toeflWritingFeedback=null;render();break;
 case 'nextToeflWriting':{const tasks=data.toeflWriting||[];ui.toeflWritingIndex=(ui.toeflWritingIndex+1)%Math.max(1,tasks.length);ui.toeflWritingFeedback=null;render();break;}
 case 'saveToeflWriting':{const t=(data.toeflWriting||[])[ui.toeflWritingIndex];if(!t)break;P.writing['toefl:'+t.id]=document.querySelector('#toeflWriting')?.value||'';if(event('writing'))notify('TOEFL taslağı bu cihazda kaydedildi.');break;}
 case 'checkToeflSentence':{const t=(data.toeflWriting||[])[ui.toeflWritingIndex];if(!t||t.kind!=='build_sentence')break;const answer=document.querySelector('#toeflWriting')?.value||'';P.writing['toefl:'+t.id]=answer;save();const result=checkBuiltSentence(t,answer);ui.toeflWritingFeedback={correct:result.correct,message:result.correct?'Kelime sırası referans cümleyle eşleşiyor. Bu, resmî puan değildir.':'Referans cümle: '+result.expected};render();break;}
 case 'saveWriting':{let idx=ui.selection%4;P.writing[idx]=document.querySelector('#writing')?.value||'';if(event('writing'))notify('Taslak bu cihazda kaydedildi.');break;}
 case 'mic':{const Speech=window.SpeechRecognition||window.webkitSpeechRecognition;if(!Speech){voiceStatus='Bu tarayıcıda konuşma tanıma desteklenmiyor. Aşağıya manuel transkript yazabilirsin.';const p=document.querySelector('#mic-status');if(p)p.textContent=voiceStatus;return;}if(!confirm('Konuşma tanıma bazı tarayıcılarda sesini harici sunuculara gönderebilir. Mikrofonu açmayı kabul ediyor musun?'))return;recognition=new Speech();recognition.lang='en-US';recognition.continuous=false;recognition.interimResults=false;recognition.onresult=e=>{let v=e.results[0][0].transcript;document.querySelector('#speech-output').value=v;document.querySelector('#mic-status').textContent='Algılanan metin yazıldı. Bu bir telaffuz puanı değildir.';};recognition.onerror=e=>{document.querySelector('#mic-status').textContent='Mikrofon / konuşma tanıma sorunu: '+e.error+' · Metni elle yazabilirsin.';};try{recognition.start();document.querySelector('#mic-status').textContent='Dinleniyor...';}catch(err){notify('Mikrofon başlatılamadı: '+err.message);}break;}
 case 'export':{if(protectedCorruptRaw!==null){notify('Bu yalnızca boş geçici ilerlemedir; önce ham kurtarma verisini indir.');break;}let text=JSON.stringify({app:'American English Lab',format:1,exportedAt:new Date().toISOString(),progress:P},null,2);const url=URL.createObjectURL(new Blob([text],{type:'application/json'}));let a=document.createElement('a');a.href=url;a.download='american-english-lab-backup-'+iso()+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);notify('JSON yedeği hazır.');break;}
 case 'exportCorrupt':{
  if(protectedCorruptRaw===null){notify('Korunması gereken bozuk kayıt bulunmuyor.');break;}
  const text=protectedCorruptRaw==='__UNREADABLE__'?'Cihaz depolaması okunamadı; ham veri dışa aktarılamadı.':protectedCorruptRaw;
  const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));
  const a=document.createElement('a');a.href=url;a.download='ael-ham-kurtarma-'+iso()+'.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  notify('Ham kurtarma dosyası indirildi. Bu dosya geçerli bir JSON ilerleme yedeği olmak zorunda değildir.');break;
 }
 case 'reset':if(confirm('Bu cihazdaki bütün çalışma kayıtlarını silmek istediğine emin misin? Bu işlem geri alınamaz.')){
  if(protectedCorruptRaw!==null&&!confirm('Mevcut kayıt BOZUK ama hâlâ korunuyor. Ham kurtarma verisini indirdiğinden emin misin? Üzerine yazmayı özellikle onaylıyor musun?'))break;
  const next={...defaultProgress(),rapidCards:{},memoryCues:{}};
  try{localStorage.setItem('ael-progress',JSON.stringify(next));protectedCorruptRaw=null;progressReadError='';acceptPersisted(next);ui.selection=0;render();notify('İlerleme kayıtları sıfırlandı.');}
  catch(error){notify('Sıfırlama depolamaya yazılamadı: '+error.message);}
 }break;
 }
}
app.addEventListener('click',e=>{const b=e.target.closest('[data-act]');if(!b)return;e.preventDefault();execute(b.dataset.act,b);});
app.addEventListener('input',e=>{if(e.target.id==='writing'&&ui.writingMode==='daily'){queueWriting(ui.selection%4,e.target.value);const count=document.querySelector('#wordcount');if(count)count.textContent=countWritingWords(e.target.value)+' words';return;}if(e.target.id==='toeflWriting'&&ui.writingMode==='toefl'){const lesson=(data.toeflWriting||[])[ui.toeflWritingIndex];if(lesson)queueWriting('toefl:'+lesson.id,e.target.value);return;}if(e.target.id==='fluencyWriting'){queueDraft(e.target.value);return;}const field=e.target.dataset.field;
 if(e.target.id==='toeflTimedWriting'&&ui.toeflWritingExam&&!ui.toeflWritingExamResult){const task=ui.toeflWritingExam.tasks[ui.toeflWritingExamIndex];if(task){ui.toeflWritingExam.answers[task.id]=e.target.value.slice(0,12000);persistWritingExam();}return;}
 if(field==='voaSearch'){const pos=e.target.selectionStart;ui.voaSearch=e.target.value;ui.voaPage=0;render();const el=document.querySelector('[data-field="voaSearch"]');if(el){el.focus();el.setSelectionRange(pos,pos);}return;}
 if(field==='rapidSearch'){const pos=e.target.selectionStart;ui.rapidSearch=e.target.value;ui.rapidPage=0;ui.rapidSelection=0;ui.rapidRevealed=false;render();const el=document.querySelector('[data-field="rapidSearch"]');if(el){el.focus();el.setSelectionRange(pos,pos);}return;}
 if(field==='search'){let pos=e.target.selectionStart;ui.search=e.target.value;ui.selection=0;ui.catalogPage=0;render();let el=document.querySelector('[data-field="search"]');if(el){el.focus();el.setSelectionRange(pos,pos);} }
 if(e.target.id==='writing'||e.target.id==='toeflWriting'){const el=document.querySelector('#wordcount');if(el)el.textContent=countWritingWords(e.target.value)+' words';}
});
app.addEventListener('change',e=>{if(e.target.id==='fluencyWriting'){queueDraft(e.target.value);flushDraft();return;} if(e.target.dataset.field==='fluencySpeed'){ui.fluencySpeed=Number(e.target.value)||1;if(audio)audio.playbackRate=ui.fluencySpeed;return;}
 if(e.target.id==='fluencyListened'){ui.fluencyListened=Boolean(e.target.checked);return;}
 if(e.target.dataset.field==='fluencySelect'){ui.fluencyIndex=Math.max(0,Number(e.target.value)||0);resetFluency();render();return;}
 if(e.target.id==='voaListenedConfirm'){ui.linkedListened=Boolean(e.target.checked);return;}if(e.target.id==='authenticListenedConfirm'){ui.authenticListened=Boolean(e.target.checked);return;}if(e.target.dataset.field==='speed'){ui.speed=Number(e.target.value);if(audio)audio.playbackRate=ui.speed;}if(e.target.dataset.field==='theme'||e.target.dataset.field==='minutes'){P.settings[e.target.dataset.field]=e.target.dataset.field==='minutes'?Number(e.target.value):e.target.value;save();render();}if(e.target.id==='importFile')importBackup(e.target.files?.[0]);});
document.addEventListener?.('visibilitychange',()=>{if(document.visibilityState==='hidden'){if(pendingDraft)flushDraft();if(pendingWriting)flushWriting();}});
window.addEventListener('pagehide',()=>{if(pendingDraft)flushDraft();if(pendingWriting)flushWriting();});
app.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.id==='answer'){e.preventDefault();const b=document.querySelector('[data-act="gradeWord"], [data-act="gradeSentence"], [data-act="checkDrill"], [data-act="checkDictation"]');b?.click();}});
async function importBackup(file){
 if(!file)return;
 try{
  if(file.size>12e6)throw Error('Dosya çok büyük (en fazla 12 MB).');
  const backup=JSON.parse(await file.text());
  // Validate before asking for confirmation. Import is additive and conservative.
  const merged=mergeProgress(P,backup);
  if(!confirm('Yedekteki öğrenme kayıtlarını mevcut kayıtları silmeden birleştirmek istiyor musun? Önce mevcut veriyi JSON olarak dışa aktarman önerilir.'))return;
  // Do not overwrite in-memory progress until the persistent write succeeds.
  localStorage.setItem('ael-progress',JSON.stringify(merged));
  protectedCorruptRaw=null;progressReadError='';acceptPersisted(merged);
  render();notify('Yedek birleştirildi: mevcut kartlar ve öğrenme kayıtları korundu.');
 }catch(e){notify('Yedek birleştirilemedi, mevcut veriler korundu: '+e.message);}
}
async function init(){try{
 const initialData=await contentLoader.load(INITIAL_KEYS);
 Object.assign(data,initialData);
 // Explicitly opted-in only by the legacy synchronous DOM test fixture.
 if(globalThis.__AEL_TEST_EAGER__===true){Object.assign(data,await contentLoader.load(Object.keys(VIEW_KEYS).flatMap(k=>VIEW_KEYS[k])));} 
 data.vocabulary=[...data.vocabulary,...data.toeflAcademic];
 data.rapid=normalizeRapidDeck(data.rapid,data.vocabulary);
 validateSentenceSkills(data.sentenceSkills);
 data.bank=quizBank(data.vocabulary,data.phrasals);
 const initial=(location.hash.match(/^#\/(\w+)/)||[])[1];
 ui.view='home';
 if(initial&&initial!=='home'&&nav.some(x=>x[0]===initial))await route(initial);
 else render();
 if('serviceWorker' in navigator&&location.protocol.startsWith('http'))navigator.serviceWorker.register('./sw.js').catch(()=>{});
 }catch(e){console.error(e);app.innerHTML=`<div class="empty"><h2>İçerik yüklenemedi</h2><p>${E(e.message)}</p><p>index.html dosyasını doğrudan dosya sisteminden değil, HTTPS veya yerel HTTP sunucusu üzerinden açın.</p></div>`;}}
window.addEventListener('hashchange',()=>{const target=(location.hash.match(/^#\/(\w+)/)||[])[1]||'home';if(target!==ui.view)route(target);});
init();

// The mini-test timer is wall-clock based, including time away from this tab.
if(typeof window.setInterval==='function')window.setInterval(()=>{if(ui.view!=='toefl'||!ui.toeflMini||ui.toeflMiniResult)return;const secs=remainingSeconds(ui.toeflMini.startedAt,ui.toeflMini.minutes);const el=document.querySelector('#toeflMiniClock');if(el)el.textContent=`${String(Math.floor(secs/60)).padStart(2,'0')}:${String(secs%60).padStart(2,'0')}`;if(secs===0){execute('finishToeflMini',{dataset:{}});notify('Reading süresi doldu. Depolama hatası varsa ilerleme yedeğini kontrol et.');}},1000);

// Writing practice timer uses real wall-clock time, including tab backgrounding.
if(typeof window.setInterval==='function')window.setInterval(()=>{if(ui.view!=='toefl'||!ui.toeflWritingExam||ui.toeflWritingExamResult)return;const secs=remainingSeconds(ui.toeflWritingExam.startedAt,ui.toeflWritingExam.minutes);const el=document.querySelector('#toeflWritingClock');if(el)el.textContent=`${String(Math.floor(secs/60)).padStart(2,'0')}:${String(secs%60).padStart(2,'0')}`;if(secs===0){finishWritingExam();render();}},1000);
