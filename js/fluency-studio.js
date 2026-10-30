/** Private educational fluency pilot. No AI grading, invented audio, or certified CEFR ratings. */
import {reviewItem} from './engine.js';

export const FLUENCY_TABS=Object.freeze([
 ['listening','Listening Master'],['dictation','Dictation Lab'],['realLife','Real-Life Simulator'],
 ['errors','Personal Error Coach'],['writing','Writing Coach'],['bridge','Reading + Listening Bridge'],
 ['thinking','English Thinking'],['adaptive','Adaptive Learning Path']
]);
const DAY=86400000;
const isObject=x=>Boolean(x)&&typeof x==='object'&&!Array.isArray(x);
export function validateFluencyData(d){
 if(!isObject(d)||!isObject(d.meta)||d.meta.independentEditorApproved!==false||d.meta.audioBundled!==false)throw Error('Fluency veri kaynak/QA bildirimi hatalı');
 if(!Array.isArray(d.realLife)||!Array.isArray(d.thinking)||!Array.isArray(d.writing))throw Error('Fluency görev listesi eksik');
 const ids=[];
 for(const s of d.realLife){if(!s.id||!s.opening||!Array.isArray(s.steps)||s.steps.length!==3)throw Error('Eksik senaryo');ids.push(s.id);for(const step of s.steps){ids.push(step.id);if(step.options?.length!==3||!Number.isInteger(step.correct)||step.correct<0||step.correct>2||!step.explanation)throw Error('Hatalı senaryo yanıtı');}}
 for(const v of [...d.thinking,...d.writing]){if(!v.id)throw Error('Görev ID eksik');ids.push(v.id);if(v.editorApproved!==false)throw Error('Editör onayı uydurulamaz');}
 if(new Set(ids).size!==ids.length)throw Error('Fluency ID çakışması');
 return {scenarios:d.realLife.length,decisions:d.realLife.reduce((n,x)=>n+x.steps.length,0),thinking:d.thinking.length,writing:d.writing.length};
}
export function humanSources(sources){return (Array.isArray(sources)?sources:[]).filter(s=>s&&s.audioType==='human_dialogue_source'&&Array.isArray(s.turns)&&s.turns.length&&/^https:\/\//.test(s.sourceUrl)&& (s.audioUrl===null||!s.audioUrl||/^https:\/\//.test(s.audioUrl)));}
export function dictationTargets(sources){
 return humanSources(sources).flatMap(s=>{
  let count=0;
  return s.turns.flatMap((t,i)=>{
   if(count>=4||!t?.text||typeof t.text!=='string'||!t.speaker||/professor bot/i.test(t.speaker))return [];
   const trimmed=t.text.trim().replace(/\s+/g,' '),len=wordTokens(trimmed).length;
   if(len<7||len>27||/\[|\]|\(|\)|“|”/.test(trimmed)||!/[.!?]$/.test(trimmed))return [];
   count++;return [{id:`dict-${s.id}-${i}`,sourceId:s.id,turnIndex:i,speaker:t.speaker,target:trimmed,title:s.title}];
  });
 });
}
export function wordTokens(s=''){return String(s).toLowerCase().replace(/[’‘]/g,"'").match(/[a-z]+(?:'[a-z]+)?|\d+/g)||[];}
export function compareDictation(input,expected){
 const a=wordTokens(input),b=wordTokens(expected);if(!a.length||!b.length)return {submitted:a.length>0,accuracy:0,distance:b.length,expectedWords:b.length,typedWords:a.length};
 let prev=Array.from({length:b.length+1},(_,i)=>i);
 for(let i=1;i<=a.length;i++){const cur=[i];for(let j=1;j<=b.length;j++)cur[j]=Math.min(cur[j-1]+1,prev[j]+1,prev[j-1]+(a[i-1]===b[j-1]?0:1));prev=cur;}
 return {submitted:true,accuracy:Math.round(100*Math.max(0,1-prev[b.length]/Math.max(a.length,b.length))),distance:prev[b.length],expectedWords:b.length,typedWords:a.length};
}
export function writingAudit(text,task){
 const words=wordTokens(text),count=words.length,paragraphs=String(text).trim().split(/\n\s*\n/g).filter(x=>x.trim()).length;
 const connectors=(String(text).match(/\b(because|although|however|therefore|while|whereas|for example|as a result|in addition|since|unless)\b/gi)||[]).length;
 const sentences=(String(text).match(/[.!?]+(?:\s|$)/g)||[]).length;
 const freq={};for(const w of words)if(w.length>=5)freq[w]=(freq[w]||0)+1;
 const repeated=Object.entries(freq).filter(([,n])=>n>=4).sort((a,b)=>b[1]-a[1]).slice(0,4).map(([w,n])=>({word:w,count:n}));
 const steps=[];if(count<task.minWords)steps.push(`Önerilen alt sınırdan ${task.minWords-count} kelime eksik.`);
 if(count>task.maxWords)steps.push(`Önerilen üst sınırın ${count-task.maxWords} kelime üzerindesin.`);
 if(sentences<3)steps.push('Düşüncelerini ayrı cümlelere bölüp açıklayıcı örnekler eklemeyi değerlendir.');
 if(connectors===0)steps.push('Gerekiyorsa neden, zıtlık veya sonuç bağlacıyla fikirlerini ilişkilendir.');
 if(repeated.length)steps.push(`Sık tekrarlanan kelimelerin kullanımını kontrol et: ${repeated.map(x=>x.word).join(', ')}.`);
 return {words:count,paragraphs,sentences,connectors,repeated,steps,withinSuggestedRange:count>=task.minWords&&count<=task.maxWords,
  disclaimer:'Bu yalnızca sayılabilir metin özelliklerini analiz eder. Gramer, anlam ve CEFR/TOEFL puanı ölçülmez.'};
}
export function errorReport(progress,limit=7){
 const rows=[...(progress?.fluencyHistory||[]).filter(r=>r.grade==='again'||r.grade==='hard').map(r=>({category:r.category||r.type||'other',id:r.id,at:r.at,source:r.type})),
 ...(progress?.skillHistory||[]).filter(r=>r.grade==='again'||r.autoChecked===true&&r.autoMatched===false).map(r=>({category:r.area||'grammar',id:r.id,at:r.at,source:'sentenceSkills'}))];
 const groups=new Map();for(const row of rows){if(!Number.isFinite(row.at))continue;const g=groups.get(row.category)||{category:row.category,count:0,last:0,source:row.source};g.count++;g.last=Math.max(g.last,row.at);groups.set(row.category,g);}
 return {attempts:rows.length,groups:[...groups.values()].sort((a,b)=>b.count-a.count||b.last-a.last).slice(0,limit)};
}
export function adaptivePlan(progress,now=Date.now(),minutes=30){
 const errors=errorReport(progress),skillDue=Object.values(progress?.skillCards||{}).filter(x=>Number(x?.due)<=now).length;
 const fluencyDue=Object.values(progress?.fluencyCards||{}).filter(x=>Number(x?.due)<=now).length;
 const recently=(progress?.fluencyHistory||[]).filter(x=>Number.isFinite(x.at)&&now-x.at<14*DAY);
 const listening=recently.filter(x=>['listening','dictation','bridge'].includes(x.type));
 const missed=listening.filter(x=>x.grade!=='good').length;
 const needListening=!listening.length||missed/listening.length>=0.25;
 const total=Math.max(15,Math.min(60,Number(minutes)||30));
 const specs=[
  {view:'fluencyStudio',tab:fluencyDue?'errors':'dictation',label:fluencyDue?'Zamanı gelen akıcılık tekrarları':'Dictation / ses çözümleme',mins:needListening?Math.round(total*.35):Math.round(total*.25),reason:needListening?'Dinleme alanında yeterli iyi sonuç yok':'Yakın dönem dinleme kayıtları mevcut'},
  {view:'sentenceSkills',label:'Soru ve cümle yapılarını pekiştir',mins:Math.round(total*.25),reason:`${skillDue} zamanı gelen beceri kartı`},
  {view:'fluencyStudio',tab:errors.groups.length?'errors':'realLife',label:errors.groups.length?'Kişisel hata koçu':'Günlük diyalog pratiği',mins:Math.round(total*.2),reason:errors.groups.length?`${errors.attempts} kayıtlı zorlanma`:'Yeni bağlamlarda üretim'},
  {view:'fluencyStudio',tab:'writing',label:'Kısa yazma ve aktif üretim',mins:0,reason:'Serbest metin, öz kontrol'}
 ];specs[3].mins=total-specs.slice(0,3).reduce((s,x)=>s+x.mins,0);
 return {minutes:total,skillDue,fluencyDue,errors,needListening,items:specs,notice:'Plan yalnızca cihazdaki kayıtlarla üretilir. Öğrenme düzeyi ve başarı garantisi değildir.'};
}
export function persistFluencyReview(progress,{id,type,category,grade,accuracy=null,listened=false,requiresAudio=false},storage,now=Date.now()){
 if(!id||!type||!category||!['again','hard','good'].includes(grade))throw Error('Geçersiz alıştırma kaydı');
 if(requiresAudio&&!listened)throw Error('Dinlemeden Listening başarısı kaydedilmez');
 const prev=progress.fluencyCards?.[id]||{},mode=['listening','dictation','bridge'].includes(type)?'listening':type==='realLife'?'context':'production';
 const updated=reviewItem(prev,grade,mode,now);const row={id,type,category,at:now,grade,accuracy:accuracy===null?null:Math.max(0,Math.min(100,Number(accuracy))),listenedSelfReported:requiresAudio?true:null,audioVerified:false};
 const next={...progress,fluencyCards:{...(progress.fluencyCards||{}),[id]:updated},fluencyHistory:[...(progress.fluencyHistory||[]),row].slice(-3000)};
 storage.setItem('ael-progress',JSON.stringify(next));return next;
}
export function persistFluencyDraft(progress,id,text,storage,now=Date.now()){
 if(!/^write-[a-z]+$/.test(id)||typeof text!=='string'||text.length>12000)throw Error('Taslak sınır dışı');
 const next={...progress,fluencyDrafts:{...(progress.fluencyDrafts||{}),[id]:{text,updatedAt:now,last:now}}};
 storage.setItem('ael-progress',JSON.stringify(next));return next;
}
