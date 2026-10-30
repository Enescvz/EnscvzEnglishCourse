/** Sentence Skills: private authored curriculum, review and honest answer checking.
 * Never assumes an arbitrary free-text alternative is grammatically wrong.
 * No external language service or speech data is used.
 */
import {reviewItem} from './engine.js';
export const SKILL_AREAS=Object.freeze({
 question:'Question Builder',preposition:'Preposition Lab',connector:'Connector Lab',sentence:'Sentence Builder'
});
const NORMALIZE_CONTRACTIONS=[[/\bwon['’]t\b/g,'will not'],[/\bcan['’]t\b/g,'cannot'],[/\bshan['’]t\b/g,'shall not'],[/\bain['’]t\b/g,'is not'],[/n['’]t\b/g,' not'],[/['’]re\b/g,' are'],[/['’]ve\b/g,' have'],[/['’]ll\b/g,' will'],[/['’]m\b/g,' am'],[/['’]d\b/g,' would'],[/['’]s\b/g,' is']];
export function skillNormalize(text=''){
 let s=String(text).toLocaleLowerCase('en-US').normalize('NFKC').trim();
 for(const [a,b] of NORMALIZE_CONTRACTIONS)s=s.replace(a,b);
 return s.replace(/[^a-z0-9\s]/g,'').replace(/\s+/g,' ').trim();
}
const FOCUS={
 question: ['does','did','have','has','are','were','would','could','should','do','will','what','where','why','when','who','how'],
 preposition:['because of','in spite of','in charge of','in favor of','in time','on time','in touch with','in effect','within','over','across','through','onto','into','since','until','during','while','at','in','on','of','to','for','with','by','about','from'],
 connector:['as a result','on the other hand','as long as','provided that','even though','in spite of','for instance','for example','in addition','due to','because of','such as','whereas','although','however','therefore','consequently','nevertheless','moreover','furthermore','unless','since','because','first','then','meanwhile','eventually','finally','afterward','while','but','so'],
 sentence:['even though','would have','should have','could','should','might','if','because','although','however','whose','which','where','who','that','an','a','the','some','any','few','little','much','many']
};
const LESSON_FOCUS={
 'yes-no':['does','do','are','is','can','have','will'],
 'wh-questions':['where','what','why','how','which','when','who','did','does','do'],
 'tense-questions':['did','have','has','are','were','will','had'],
 'modal-questions':['could','would','may','should','can','must','might'],
 'subject-questions':['who','what','which'],
 'object-questions':['who','what','which','did','does','have'],
 'negative-questions':["didn’t","don’t","isn’t","haven’t","couldn’t","wouldn’t","aren’t","hasn’t","shouldn’t"],
 'indirect-questions':['where','what','why','how','whether','if','when','who'],
 'question-tags':["don’t","isn’t","haven’t","wasn’t","can’t","shouldn’t","didn’t","shall","aren’t"],
 'preposition-questions':['for','to','about','with','in','on'],
 'hypothetical-questions':['would','if'],
 'follow-up-questions':['what','how','why','could','can'],
 'prepositions-time':['at','on','in'],
 'prepositions-place':['at','on','in'],
 'movement-prepositions':['through','onto','across','into','out of','over','past','along','up','down'],
 'verb-preposition':['on','to','for','about','with'],
 'adjective-preposition':['in','at','of','for','with','about','by'],
 'noun-preposition':['for','in','to','on'],
 'because-during':['because of','because','during','while'],
 'for-since-until':['for','since','until','by'],
 'to-for-with':['to','for','with'],
 'fixed-preposition-chunks':['on time','in time','in charge of','at risk','in touch with','on his way','in effect','in favor of','within'],
 'cause-connectors':['because of','due to','because','since','as'],
 'result-connectors':['as a result','therefore','consequently','so'],
 'contrast-connectors':['in spite of','even though','despite','although','however','nevertheless','but'],
 'condition-connectors':['as long as','provided that','unless','if'],
 'addition-connectors':['in addition','furthermore','moreover','as well as','besides','also','and'],
 'comparison-connectors':['on the other hand','compared with','unlike','whereas','while','than','but','however'],
 'examples-connectors':['for instance','for example','such as','including'],
 'sequence-connectors':['as soon as','in the meantime','meanwhile','eventually','afterward','before','first','then','finally','while'],
 'articles-quantifiers':['much','many','few','little','some','any','an','a','the'],
 'relative-pronouns':['whose','who','that','which','where','why'],
 'modals-conditionals':['should have','would have','mustn’t','should','might','could','if','must'],
 'natural-sentence-flow':['although','however','because','when','if','before','but','and']
};
export function sentenceCloze(sentence,area,lessonId=''){

 const source=String(sentence);
 const lower=source.toLowerCase();
 const slug=String(lessonId).replace(/^sl-/ ,'').replace(/^sk-/ ,'').replace(/-\d{2}$/,'');
 for(const candidate of LESSON_FOCUS[slug]||FOCUS[area]||[]){
  const p=lower.search(new RegExp(`(^|[^a-z])${candidate.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')}(?=$|[^a-z])`));
  if(p<0)continue;
  const match=new RegExp(`(^|[^a-z])(${candidate.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')})(?=$|[^a-z])`,'i').exec(source);
  if(match){const at=match.index+match[1].length;return {prompt:source.slice(0,at)+'_____'+source.slice(at+match[2].length),expected:match[2]};}
 }
 const match=/\b[A-Za-z]+\b/.exec(source);if(!match)throw Error('Cloze için kelime yok');
 return {prompt:source.slice(0,match.index)+'_____'+source.slice(match.index+match[0].length),expected:match[0]};
}
export function validateSentenceSkills(dataset){
 if(!dataset||!Array.isArray(dataset.lessons)||dataset.meta?.independentEditorApproved!==false)throw Error('Sentence Skills inceleme etiketi eksik');
 const ids=new Set();let total=0;
 for(const lesson of dataset.lessons){
  if(!SKILL_AREAS[lesson.area]||!/^sl-[a-z-]+$/.test(lesson.id)||!Array.isArray(lesson.exercises)||lesson.exercises.length!==10)throw Error('Geçersiz Sentence Skills dersi: '+lesson.id);
  for(const ex of lesson.exercises){
   if(ids.has(ex.id)||!ex.id.startsWith('sk-')||!ex.modelAnswer||!ex.task||!['order','guided','production','followup'].includes(ex.mode))throw Error('Geçersiz egzersiz: '+ex.id);
   if(ex.mode==='order'&&(!Array.isArray(ex.tokens)||ex.tokens.length<3))throw Error('Sıralama tokenları yok: '+ex.id);
   ids.add(ex.id);total++;
  }
 }
 if(total!==dataset.meta.totalExercises||dataset.lessons.length!==dataset.meta.totalLessons)throw Error('Sentence Skills sayı tutarsızlığı');
 return {lessons:dataset.lessons.length,exercises:total};
}
export function assessSkillInput(ex,answer,area){
 const text=String(answer||'').trim();if(!text)return {submitted:false,automatic:false,matched:false};
 if(ex.mode==='order')return {submitted:true,automatic:true,matched:skillNormalize(text)===skillNormalize(ex.modelAnswer),expected:ex.modelAnswer};
 if(ex.mode==='guided'){
  const {expected}=sentenceCloze(ex.modelAnswer,area,ex.lessonId||ex.id);
  return {submitted:true,automatic:true,matched:skillNormalize(text)===skillNormalize(expected),expected};
 }
 return {submitted:true,automatic:false,matched:null,expected:ex.modelAnswer};
}
export function listSkillExercises(dataset){return (dataset?.lessons||[]).flatMap(l=>l.exercises.map(e=>({...e,area:l.area,lessonId:l.id})));}
export function skillsDue(dataset,progress,now=Date.now()){
 return listSkillExercises(dataset).filter(e=>progress?.skillCards?.[e.id] && Number(progress.skillCards[e.id].due)<=now).sort((a,b)=>progress.skillCards[a.id].due-progress.skillCards[b.id].due);
}
export function skillSummary(dataset,progress,now=Date.now()){
 const items=listSkillExercises(dataset), done=items.filter(x=>progress?.skillCards?.[x.id]);
 const windows=[{days:7,after:7,before:14},{days:30,after:30,before:45}].map(w=>{
  const records=(progress?.skillHistory||[]).filter(x=>x.autoChecked===true&&x.reassessmentDays>=w.after&&x.reassessmentDays<=w.before);
  return {days:w.days,observed:records.length,matched:records.filter(x=>x.autoMatched).length,rate:records.length?Math.round(records.filter(x=>x.autoMatched).length*100/records.length):null};
 });
 return {total:items.length,practiced:done.length,due:skillsDue(dataset,progress,now).length,windows};
}
export function prepareSkillReview(progress,ex,area,grade,answerResult,now=Date.now()){
 if(!['again','hard','good'].includes(grade))throw Error('Geçersiz tekrar notu');
 if(!answerResult?.submitted)throw Error('Cevap verilmedi');
 if(answerResult.automatic&&answerResult.matched===false&&grade==='good')throw Error('Otomatik eşleşmeyen yanıt doğrulandı sayılmaz; alternatif yanıt varsa öz değerlendirme kullanılmalı');
 const previous=progress?.skillCards?.[ex.id]||{};
 const reassessmentDays=Number.isFinite(previous.last)?(now-previous.last)/86400000:null;
 const mode=ex.mode==='order'||ex.mode==='guided'?'recall':'production';
 const state=reviewItem(previous,grade,mode,now);
 const record={id:ex.id,lessonId:ex.lessonId,area,mode:ex.mode,at:now,grade,autoChecked:answerResult.automatic,
  autoMatched:answerResult.automatic?answerResult.matched:null,
  reassessmentDays:reassessmentDays===null?null:Math.round(reassessmentDays*100)/100};
 const next={...progress,skillCards:{...(progress.skillCards||{}),[ex.id]:{...state,lastOutcome:grade,lastMode:ex.mode}},skillHistory:[...(progress.skillHistory||[]),record].slice(-5000)};
 return {next,record};
}
export function persistSkillReview(progress,ex,area,grade,answerResult,storage,now=Date.now()){
 const prepared=prepareSkillReview(progress,ex,area,grade,answerResult,now);
 // Fail closed: callers must NOT update in-memory progress or display success
 // before localStorage confirms the write.
 storage.setItem('ael-progress',JSON.stringify(prepared.next));
 return prepared.next;
}
