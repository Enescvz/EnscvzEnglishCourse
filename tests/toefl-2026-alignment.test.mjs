import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {makeTypedWordCompletion,checkTypedWordCompletion,readingAdvice} from '../js/toefl-prep.js';
import {makeWritingPractice,validateWritingPracticeSession,reviewWritingPractice,WRITING_PRACTICE_TASK_COUNTS} from '../js/toefl-writing-exam.js';
const source=p=>JSON.parse(readFileSync(new URL(p,import.meta.url)));
const reading=source('../data/toefl-reading-practice.json'),writing=source('../data/toefl-writing-practice.json');
test('ETS 2026 writing rehearsal uses 10+1+1, retains old session 8+2+2',()=>{
 assert.deepEqual(WRITING_PRACTICE_TASK_COUNTS,{build_sentence:10,write_email:1,academic_discussion:1});
 for(const n of [0,1,4,12]){
  const tasks=makeWritingPractice(writing,n);
  assert.equal(tasks.length,12);
  assert.equal(new Set(tasks.map(x=>x.id)).size,12);
  const sess={version:2,startedAt:Date.now()-1000,minutes:23,ids:tasks.map(t=>t.id),answers:{[tasks[0].id]:'draft'}};
  assert.equal(validateWritingPracticeSession(sess,writing).answers[tasks[0].id],'draft');
  assert.equal(validateWritingPracticeSession({...sess,version:1},writing),null);
  const r=reviewWritingPractice(tasks,{},Date.now());
  assert.equal(r.officialScore,null);assert.equal(r.buildSentenceTotal,10);
 }
 const legacy=[...writing.filter(t=>t.kind==='build_sentence').slice(0,8),...writing.filter(t=>t.kind==='write_email').slice(0,2),...writing.filter(t=>t.kind==='academic_discussion').slice(0,2)];
 const s={version:1,startedAt:Date.now()-1000,minutes:23,ids:legacy.map(t=>t.id),answers:{[legacy[0].id]:'legacy'}};
 assert.equal(validateWritingPracticeSession(s,writing).answers[legacy[0].id],'legacy');
});
test('typing full words without MC feedback uses all 16 existing IDs safely',()=>{
 const items=makeTypedWordCompletion(reading);
 assert.equal(items.length,16);
 assert.equal(new Set(items.map(x=>x.id)).size,16);
 for(const item of items){
  assert.ok(item.prompt.includes('_'));
  assert.equal(checkTypedWordCompletion(item,item.expected.toUpperCase()).correct,true);
  assert.equal(checkTypedWordCompletion(item,' '+item.expected+' ').correct,true);
  assert.equal(checkTypedWordCompletion(item,'incorrect').correct,false);
  assert.equal(checkTypedWordCompletion(item,'').correct,false);
  assert.equal(checkTypedWordCompletion(item,item.expected).officialScore,null);
  assert.equal(checkTypedWordCompletion(item,item.expected).editorReviewed,false);
 }
 assert.throws(()=>checkTypedWordCompletion(items[0],'a'.repeat(101)),/too long/);
 assert.throws(()=>makeTypedWordCompletion([{...reading[0],questions:[{...reading[0].questions[0],question:'broken'}]}]),/Invalid/);
});
test('typed-only submissions do not bias MC Reading level guidance',()=>{
 const a=checkTypedWordCompletion(makeTypedWordCompletion(reading)[0],'volunteer');
 assert.equal(readingAdvice([a]).weakest,null);
});
test('new writing sentence source tokens reconstruct the reference',()=>{
 for(const t of writing.filter(x=>Number(x.id.split('-').at(-1))>=9&&x.kind==='build_sentence')){
  let sentence=t.answer.toLowerCase().replace(/[^a-z0-9\p{L}’']/gu,' ').replace(/\s+/g,' ').trim();
  for(const token of t.tokens){
   const pattern=token.toLowerCase().replace(/[^a-z0-9\p{L}’']/gu,' ').replace(/\s+/g,' ').trim();
   assert.ok(sentence.includes(pattern),`${t.id}: missing '${token}'`);
   sentence=sentence.replace(pattern,'').replace(/\s+/g,' ').trim();
  }
  assert.equal(sentence,'',`${t.id}: not all reference parts accounted for`);
 }
});
