import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
import {checkBuiltSentence,countWritingWords,writingChecklist} from '../js/toefl-writing.js';
const tasks=JSON.parse(readFileSync(new URL('../data/toefl-writing-practice.json',import.meta.url),'utf8'));
test('TOEFL 2026 author-created practice has three question types and stable unique IDs',()=>{
 assert.equal(tasks.length,28);assert.equal(new Set(tasks.map(x=>x.id)).size,28);
 assert.equal(tasks.filter(x=>x.kind==='build_sentence').length,16);
 for(const kind of ['write_email','academic_discussion'])assert.equal(tasks.filter(x=>x.kind===kind).length,6);
 assert.ok(tasks.every(x=>x.prompt&&x.title&&x.id));
});
test('build sentence exact normalized order: a word bag cannot pass',()=>{
 for(const t of tasks.filter(x=>x.kind==='build_sentence')){
  assert.ok(checkBuiltSentence(t,t.answer.toUpperCase()).correct);
  assert.ok(!checkBuiltSentence(t,'').correct);
  assert.ok(!checkBuiltSentence(t,t.answer.split(' ').reverse().join(' ')).correct);
 }
});
test('writing feedback gives no invented language grade',()=>{
 for(const t of tasks.filter(x=>x.kind!=='build_sentence')){
  const r=writingChecklist(t,'My first idea is to arrange another meeting.');
  assert.equal(r.autoScore,null);assert.equal(r.editorReviewed,false);
  assert.equal(r.words,8);assert.ok(r.requirements.length>=3);
 }
});
