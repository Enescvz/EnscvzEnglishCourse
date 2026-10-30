/** Author-authored TOEFL-style practice; NOT an ETS test, adaptive algorithm or score predictor. */
export const READING_MINI_MINUTES=12;
export const READING_DIAGNOSTIC_MINUTES=30;
export const OFFICIAL_2026_TASKS=Object.freeze({
 reading:['complete_words','daily_life','academic_passage'],
 listening:['response','conversation','announcement','academic_talk'],
 writing:['build_sentence','write_email','academic_discussion']
});
export function makeReadingMini(readings,attemptNumber=0){
 const out=[];
 for(const type of OFFICIAL_2026_TASKS.reading){
  const pool=readings.filter(r=>r.type===type && Array.isArray(r.questions));
  if(pool.length<3)throw new Error('Reading task pool is insufficient for a balanced practice test');
  for(let slot=0;slot<3;slot++){
   const idx=(slot+Math.max(0,attemptNumber))%pool.length;
   const passage=pool[idx];
   const qi=Math.floor(Math.max(0,attemptNumber)/pool.length)%passage.questions.length;
   const q=passage.questions[qi];
   out.push({id:`${passage.id}::${qi}`,type,title:passage.title,body:passage.body,
     question:q.question,options:[...q.options],answer:q.answer,explanation:q.explanation});
  }
 }
 return out;
}
/** Complete available original Reading corpus. AEL diagnostic, NOT ETS full-length or adaptive. */
export function makeReadingDiagnostic(readings){
 const items=[];const ids=new Set();
 for(const r of readings){
  if(!OFFICIAL_2026_TASKS.reading.includes(r.type)||!Array.isArray(r.questions))continue;
  for(let qi=0;qi<r.questions.length;qi++){
   const q=r.questions[qi],id=`${r.id}::${qi}`;
   if(ids.has(id))throw Error(`Duplicate Reading question ID: ${id}`);
   ids.add(id);items.push({id,type:r.type,title:r.title,body:r.body,question:q.question,
    options:[...q.options],answer:q.answer,explanation:q.explanation});
  }
 }
 if(OFFICIAL_2026_TASKS.reading.some(t=>!items.some(x=>x.type===t)))throw Error('Missing official reading task category');
 return items;
}
/** Data-validated, non-calibrated AEL practice feedback. */
/** Balanced answer-position presentation for *new* AEL Reading sessions only.
 * Old v1 sessions retain the original option order and saved numeric selections.
 * Shuffle is deterministic within the fixed session item order so v2 sessions
 * can be restored without changing question IDs or content answers.
 */
export function balanceReadingChoices(items){
 if(!Array.isArray(items)||new Set(items.map(q=>q.id)).size!==items.length)throw Error('Invalid Reading question collection');
 return items.map((q,i)=>{
  if(!Array.isArray(q.options)||q.options.length!==4||!Number.isInteger(q.answer)||q.answer<0||q.answer>=4)
   throw Error('Invalid Reading answer options');
  const answerIndex=i%4;
  const shift=(answerIndex-q.answer+4)%4;
  return {...q,options:q.options.map((_,j)=>q.options[(j-shift+4)%4]),answer:answerIndex};
 });
}
export function gradeReadingPractice(items,answers={},at=Date.now(),kind='original_timed_reading_diagnostic'){
 if(!Array.isArray(items)||!items.length||new Set(items.map(x=>x.id)).size!==items.length)throw Error('Invalid Reading question set');
 const byType={};let correct=0,unanswered=0;
 for(const item of items){
  if(!OFFICIAL_2026_TASKS.reading.includes(item.type)||!Array.isArray(item.options)||!Number.isInteger(item.answer)||item.answer<0||item.answer>=item.options.length)throw Error('Invalid Reading answer key');
  const group=byType[item.type]??={correct:0,total:0};group.total++;
  const selected=Number.isInteger(answers[item.id])&&answers[item.id]>=0&&answers[item.id]<item.options.length?answers[item.id]:null;
  if(selected===null)unanswered++;
  else if(selected===item.answer){correct++;group.correct++;}
 }
 return {at,correct,total:items.length,unanswered,byType,kind,officialScore:null,
  responses:items.map(x=>({id:x.id,type:x.type,selected:Number.isInteger(answers[x.id])&&answers[x.id]>=0&&answers[x.id]<x.options.length?answers[x.id]:null,correct:x.answer}))};
}
export function gradeReadingMini(items,answers={},at=Date.now()){
 if(!Array.isArray(items)||items.length!==9)throw Error('Nine questions required');
 return gradeReadingPractice(items,answers,at,'original_timed_reading_mini');
}
export function readingAdvice(attempts=[]){
 const types=OFFICIAL_2026_TASKS.reading;
 const totals=Object.fromEntries(types.map(t=>[t,{correct:0,total:0}]));
 for(const attempt of attempts){
  if(!['original_timed_reading_mini','original_timed_reading_diagnostic'].includes(attempt?.kind))continue;
  for(const t of types){const row=attempt.byType?.[t];if(row&&Number.isInteger(row.correct)&&Number.isInteger(row.total)&&row.total>=row.correct&&row.correct>=0){totals[t].correct+=row.correct;totals[t].total+=row.total;}}
 }
 const observed=types.filter(t=>totals[t].total>0);
 const weakest=observed.length?observed.sort((a,b)=>totals[a].correct/totals[a].total-totals[b].correct/totals[b].total)[0]:null;
 return {observations:totals,weakest,readingRecommendation:weakest?{
  complete_words:'Kelime tamamlama ve akademik sözcük bağlamı',daily_life:'Günlük duyuru/e-posta okuma',academic_passage:'Akademik paragraf, çıkarım ve ana fikir'
 }[weakest]:'Önce süreli Reading mini denemesini çöz; sonucun olmadan zayıf alan tahmini yapılmaz.'};
}
export function remainingSeconds(startedAt,minutes=READING_MINI_MINUTES,now=Date.now()){
 return Math.max(0,Math.ceil((startedAt+minutes*60000-now)/1000));
}

/** Never infer unmeasured skills; no official score or proficiency estimate. */
export function readingReviewPlan(attempts=[]){
 const advice=readingAdvice(attempts);
 const types=OFFICIAL_2026_TASKS.reading;
 return types.map(type=>{
  const {correct,total}=advice.observations[type];
  return {type,correct,total,accuracy:total?Math.round(100*correct/total):null,
   status:total===0?'not_measured':correct/total<.6?'needs_practice':'observed',
   guidance:{complete_words:'Bağlama göre eksik sözcüğü tamamlama; 10 dakika aktif kelime hatırlama',
    daily_life:'Günlük e-posta, duyuru ve ayrıntı bulma; 10 dakika',
    academic_passage:'Akademik ana fikir, gerekçe ve çıkarım; 15 dakika'}[type]};
 });
}

/** Optional typed word-completion training for the 2026 Reading task category.
 * Existing MC practice attempts and card IDs stay untouched; this is not an ETS item.
 */
export function makeTypedWordCompletion(readings){
 const result=[];
 for(const lesson of readings.filter(x=>x.type==='complete_words')){
  for(let i=0;i<lesson.questions.length;i++){
   const q=lesson.questions[i],expected=q.options?.[q.answer];
   const masked=q.question?.match(/[A-Za-z]+_[A-Za-z]+/u)?.[0];
   if(!masked||typeof expected!=='string'||!new RegExp(`^${masked.replace('_','.')}$`,'i').test(expected))
    throw new Error(`Invalid typed-completion source: ${lesson.id}::${i}`);
   result.push({id:`${lesson.id}::${i}`,title:lesson.title,context:lesson.body,
    prompt:q.question,expected:expected.toLowerCase(),explanation:q.explanation,kind:'original_typed_word_completion'});
  }
 }
 if(new Set(result.map(x=>x.id)).size!==result.length)throw Error('Duplicate word completion ID');
 return result;
}
export function checkTypedWordCompletion(item,value,at=Date.now()){
 if(!item||item.kind!=='original_typed_word_completion'||typeof item.expected!=='string')throw Error('Invalid word item');
 const answer=String(value??'').trim().toLowerCase();
 if(answer.length>100)throw Error('Word answer too long');
 const correct=answer===item.expected;
 return {at,kind:item.kind,id:item.id,correct,total:1,correctCount:Number(correct),submitted:answer,
   expected:item.expected,officialScore:null,editorReviewed:false};
}
