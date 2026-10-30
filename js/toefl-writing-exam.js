/** Original 2026-format writing *practice* only. No ETS score, no grammar grading. */
import {checkBuiltSentence,writingChecklist} from './toefl-writing.js';
export const WRITING_PRACTICE_MINUTES=23;
// ETS 2026 published operational mix: 10 Build a Sentence, 1 Email, 1 Academic Discussion.
// Version 1 sessions used the older AEL 8/2/2 mix and remain resumable.
export const WRITING_PRACTICE_TASK_COUNTS=Object.freeze({build_sentence:10,write_email:1,academic_discussion:1});
export const LEGACY_WRITING_PRACTICE_TASK_COUNTS=Object.freeze({build_sentence:8,write_email:2,academic_discussion:2});
export function makeWritingPractice(tasks,attempt=0){
 if(!Number.isInteger(attempt)||attempt<0)throw Error('Invalid attempt number');
 const selection=[];
 for(const [kind,n] of Object.entries(WRITING_PRACTICE_TASK_COUNTS)){
  const pool=tasks.filter(x=>x.kind===kind);
  if(pool.length<n)throw Error(`Insufficient ${kind} tasks`);
  for(let i=0;i<n;i++)selection.push(pool[(i+attempt)%pool.length]);
 }
 if(new Set(selection.map(x=>x.id)).size!==12)throw Error('Duplicate writing task ID');
 return selection;
}
export function validateWritingPracticeSession(session,tasks){
 if(!session||![1,2].includes(session.version)||!Number.isFinite(session.startedAt)||session.startedAt<0||session.startedAt>Date.now()+60000||session.minutes!==WRITING_PRACTICE_MINUTES||!Array.isArray(session.ids)||session.ids.length!==12||new Set(session.ids).size!==12)return null;
 const byId=new Map(tasks.map(x=>[x.id,x]));
 const ordered=session.ids.map(id=>byId.get(id));
 if(ordered.some(x=>!x))return null;
 const counts=session.version===1?LEGACY_WRITING_PRACTICE_TASK_COUNTS:WRITING_PRACTICE_TASK_COUNTS;
 for(const [type,n] of Object.entries(counts))if(ordered.filter(x=>x.kind===type).length!==n)return null;
 if(!session.answers||typeof session.answers!=='object'||Array.isArray(session.answers))return null;
 const answers={};
 for(const id of session.ids){const value=session.answers[id];if(typeof value==='string' && value.length<=12000)answers[id]=value;}
 return {version:session.version,startedAt:session.startedAt,minutes:session.minutes,ids:[...session.ids],answers};
}
export function reviewWritingPractice(tasks,answers={},at=Date.now()){
 if(tasks.length!==12||new Set(tasks.map(x=>x.id)).size!==12)throw Error('Invalid writing practice tasks');
 let referenceMatches=0,completed=0;
 const review=tasks.map(t=>{
  const answer=typeof answers[t.id]==='string'?answers[t.id]:'';
  const filled=answer.trim().length>0;if(filled)completed++;
  if(t.kind==='build_sentence'){
   const r=checkBuiltSentence(t,answer);if(r.correct)referenceMatches++;
   return {id:t.id,kind:t.kind,filled,exactReferenceMatch:r.correct,reference:t.answer,comment:'Yalnızca referans cümleyle birebir eşleşme; alternatif doğru cümleler ayrıca değerlendirilmeli.'};
  }
  const checklist=writingChecklist(t,answer);
  return {id:t.id,kind:t.kind,filled,wordCount:checklist.words,requirements:checklist.requirements,observations:checklist.observations,revisionSteps:checklist.revisionSteps,editorReviewed:false};
 });
 return {at,kind:'original_timed_writing_practice',completed,total:12,exactReferenceMatches:referenceMatches,buildSentenceTotal:tasks.filter(x=>x.kind==='build_sentence').length,distribution:Object.fromEntries(['build_sentence','write_email','academic_discussion'].map(kind=>[kind,tasks.filter(x=>x.kind===kind).length])),
  officialScore:null,grammarGraded:false,semanticGraded:false,review};
}
