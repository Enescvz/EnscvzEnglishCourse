import {normalize,reviewItem} from './engine.js';

export const MEMORY_STAGES=[
  {id:'learn',label:'Bağ kur'}, {id:'listen',label:'Dinle'},
  {id:'recall',label:'Hatırla'}, {id:'context',label:'Anla'},
  {id:'produce',label:'Kullan'}
];
/** Accessible five-step progress; only finished phases count as done. */
export function memoryStageProgress(phase,index,total) {
  const active=Math.max(0,MEMORY_STAGES.findIndex(s=>s.id===phase));
  const safeTotal=Math.max(1,total);
  return {active,stages:MEMORY_STAGES.map((s,i)=>({...s,state:i<active?'done':i===active?'current':'upcoming'})),
    sessionPercent:Math.round(100*(Math.max(0,index)+active/MEMORY_STAGES.length)/safeTotal)};
}


/** Build only runnable contextual lessons. Editorial focus headwords are not lessons. */
export function memoryPool(focus, vocabulary, phrasals, toeflCore=null, expressions=[]) {
  const general = new Map(vocabulary.filter(x=>x.category==='general').map(x=>[x.id,x]));
  const phrases = new Map(phrasals.map(x=>[x.id,x]));
  const result=[], seen=new Set();
  for (const [kind,targets,bank] of [['word',focus?.vocabulary||[],general],['phrasal',focus?.phrasals||[],phrases]]) {
    for (const target of targets) {
      if(target.status!=='context_draft'||!target.lessonId)continue;
      const lesson=bank.get(target.lessonId);
      if(!lesson||!lesson.tr||!lesson.definition||!lesson.example)continue;
      const id=`${kind}:${lesson.id}`;
      if(seen.has(id))continue;
      seen.add(id);
      result.push({id,kind,lessonId:lesson.id,word:lesson.word,tr:lesson.tr,
        definition:lesson.definition,example:lesson.example,
        examples:lesson.examples?.length?lesson.examples:[lesson.example],level:target.level||lesson.level,
        contentStatus:'authored_unreviewed'});
    }
  }
  // TOEFL is a shared review scope, not a duplicate deck. Add only academic
  // lessons absent from the focus curriculum; all existing IDs stay intact.
  const toeflWords=new Set(toeflCore?.wordLessonIds||[]);
  const toeflPhrasals=new Set(toeflCore?.phrasalLessonIds||[]);
  for(const card of result)card.toefl=card.kind==='word'?toeflWords.has(card.lessonId):toeflPhrasals.has(card.lessonId);
  for(const lesson of vocabulary){
    if(!toeflWords.has(lesson.id)||lesson.category!=='toeflAcademic'||!lesson.tr||!lesson.definition||!lesson.example)continue;
    const id=`word:${lesson.id}`;
    if(seen.has(id))continue;
    seen.add(id);
    result.push({id,kind:'word',lessonId:lesson.id,word:lesson.word,tr:lesson.tr,
      definition:lesson.definition,example:lesson.example,
      examples:lesson.examples?.length?lesson.examples:[lesson.example],
      level:lesson.level,contentStatus:'authored_unreviewed',toefl:true});
  }
  // Original daily-language chunks have their own stable IDs and FSRS storage.
  for(const lesson of expressions) {
    if(!lesson.id||!lesson.expression||!lesson.tr||!lesson.usageNote||lesson.examples?.length!==2)continue;
    const id=`expression:${lesson.id}`;
    if(seen.has(id))continue;
    seen.add(id);
    result.push({id,kind:'expression',lessonId:lesson.id,word:lesson.expression,tr:lesson.tr,
      definition:lesson.usageNote,example:lesson.examples[0],examples:lesson.examples,
      dialogue:lesson.dialogue,level:lesson.level,contentStatus:'authored_unreviewed',toefl:lesson.contexts?.includes('toefl')===true});
  }
  return result;
}
export const getMemoryProgress=(p,item)=>item.kind==='phrasal'?p.phrasals?.[item.lessonId]:item.kind==='expression'?p.expressions?.[item.lessonId]:p.cards?.[item.lessonId];
/** Review due cards first, then introduce unseen cards. Do NOT schedule future
 * cards early simply because the daily quota has empty slots. An explicit
 * preview/study-ahead mode is not implemented here. Stable IDs are preserved.
 */
export function memoryQueue(items,progress,{scope='all',max=10,now=Date.now(),expressionLevel='all'}={}) {
  const filtered=items.filter(x=>scope==='all'||scope===x.kind||(scope==='B2'||scope==='C1')&&x.kind==='word'&&x.level===scope || (scope==='toefl'&&x.toefl) || (scope==='expression'&&x.kind==='expression') || (scope==='expression-toefl'&&x.kind==='expression'&&x.toefl&&(expressionLevel==='all'||x.level===expressionLevel)) || (scope==='expression-daily'&&x.kind==='expression'&&!x.toefl&&(expressionLevel==='all'||x.level===expressionLevel)) || (scope==='expression-b1'&&x.kind==='expression'&&x.level==='B1') || (scope==='expression-b2'&&x.kind==='expression'&&x.level==='B2') || (scope==='expression-c1'&&x.kind==='expression'&&x.level==='C1'));
  return filtered.map((item,index)=>({item,index,p:getMemoryProgress(progress,item)}))
    .filter(x=>!x.p || !Number.isFinite(x.p.due) || x.p.due<=now)
    .sort((a,b)=>{
      const group=x=>x.p?0:1;
      return group(a)-group(b) || (group(a)===0?(a.p.due||0)-(b.p.due||0):0) || a.index-b.index;
    }).slice(0,Math.max(0,max)).map(x=>x.item.id);
}
export function memoryAnswer(answer,word){return normalize(answer)===normalize(word);}
/** Context comprehension question: original sentence plus four distinct Turkish
 * meanings, chosen only from the same content type. The correct option is not
 * leaked through DOM attributes. Semantic plausibility still needs editorial QA.
 */
export function memoryContextQuestion(item, pool) {
  if(!item)return null;
  const tr=x=>String(x.tr||'').trim();
  const distinct=new Set([tr(item).toLocaleLowerCase('tr')]);
  const others=[];
  for(const candidate of pool||[]) {
    if(candidate.kind!==item.kind||candidate.id===item.id||!tr(candidate))continue;
    const k=tr(candidate).toLocaleLowerCase('tr');
    if(distinct.has(k))continue;
    distinct.add(k);others.push(tr(candidate));
  }
  if(others.length<3)return null;
  // Stable per-expression permutation; avoids a fixed correct-choice position.
  const hash=[...item.id].reduce((h,c)=>(Math.imul(h,31)+c.charCodeAt(0))>>>0,17);
  const start=hash%others.length;
  const distractors=[];
  for(let i=0;i<others.length&&distractors.length<3;i++)distractors.push(others[(start+i*17)%others.length]);
  // If the stride cycles in a smaller pool, use unique fallback choices.
  const alternatives=[...new Set(distractors)];
  for(const o of others)if(alternatives.length<3&&!alternatives.includes(o))alternatives.push(o);
  const correct=tr(item);
  const choices=alternatives.slice(0,3);
  choices.splice(hash%4,0,correct);
  return {sentence:item.examples?.[1]||item.example, choices, answer:correct};
}
export function memorySentenceContains(sentence,word){
 const a=normalize(sentence), b=normalize(word);
 return a===b || (` ${a} `).includes(` ${b} `);
}
/** Grade observed vocabulary retrieval, never device availability or self-report.
 * FSRS Hard implies the word WAS retrieved; a failed typed recall is Again.
 * Context is a recognition check, not proof of independent production.
 * Synthetic TTS recognition is optional and cannot create human listening mastery.
 */
export function memoryGrade({listeningCorrect=null,recallCorrect=false,contextCorrect=null,productionConfirmed=false}={}){
 if(!recallCorrect)return 'again';
 if(contextCorrect!==true || listeningCorrect===false)return 'hard';
 // Good means verified typed recall + context recognition; it does not mean
 // verified production, real human listening, or proficiency mastery.
 return 'good';
}
/** One review per completed card; share the existing FSRS schedule and mode history. */
export function recordMemoryReview(progress,item,trial,now=Date.now()) {
 const container=item.kind==='phrasal'?progress.phrasals:item.kind==='expression'?progress.expressions:progress.cards;
 const grade=memoryGrade(trial);
 const old=container[item.lessonId];
 const next=reviewItem(old,grade,'recall',now);
 if (grade!=='again') {
   // Browser speechSynthesis is synthetic, not a licensed human recording.
   // Never credit TTS recognition to modeSuccess.listening, which is used
   // elsewhere for authentic Listening mastery status.
   if(trial.listeningCorrect===true)next.ttsRecognitionSuccess=(next.ttsRecognitionSuccess||0)+1;
   if(trial.contextCorrect===true)next.modeSuccess.context=(next.modeSuccess.context||0)+1;
   // Sentences are self-evaluated, so record as self-reported, not verified production mastery.
   if(trial.productionConfirmed===true)next.selfReportedProduction=(next.selfReportedProduction||0)+1;
 }
 if(trial.listeningCorrect===false)next.ttsRecognitionNeedsPractice=(next.ttsRecognitionNeedsPractice||0)+1;
 container[item.lessonId]=next;
 return {grade,state:next};
}
export function memoryCompletion(items,progress){
 let reviewed=0,due=0;
 for(const x of items){const p=getMemoryProgress(progress,x);if(p){reviewed++;if(p.due<=Date.now())due++;}}
 return {reviewed,due,remaining:items.length-reviewed};
}
