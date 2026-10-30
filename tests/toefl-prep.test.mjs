import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {makeReadingMini,gradeReadingMini,readingAdvice,remainingSeconds,OFFICIAL_2026_TASKS} from '../js/toefl-prep.js';
import {writingChecklist,writingStructureHints} from '../js/toefl-writing.js';
const read=(p)=>JSON.parse(readFileSync(new URL(p,import.meta.url)));
const readings=read('../data/toefl-reading-practice.json');
const writing=read('../data/toefl-writing-practice.json');
const listening=read('../data/toefl-listening-practice.json');
test('existing reading and writing IDs remain stable after content expansion',()=>{
 const expectedR=['tr26-words-01','tr26-words-02','tr26-daily-01','tr26-daily-02','tr26-academic-01','tr26-academic-02'];
 const expectedW=['tw26-sentence-01','tw26-sentence-02','tw26-sentence-03','tw26-email-01','tw26-email-02','tw26-email-03','tw26-discussion-01','tw26-discussion-02','tw26-discussion-03'];
 assert.deepEqual(readings.slice(0,6).map(x=>x.id),expectedR);
 assert.deepEqual(writing.slice(0,9).map(x=>x.id),expectedW);
});
test('balanced reading mini includes 9 items and 3 items per official category',()=>{
 for(const attempt of [0,1,5,20]){
  const mini=makeReadingMini(readings,attempt);assert.equal(mini.length,9);
  assert.equal(new Set(mini.map(x=>x.id)).size,9);
  for(const type of OFFICIAL_2026_TASKS.reading)assert.equal(mini.filter(x=>x.type===type).length,3);
  assert.ok(mini.every(x=>x.body.length>150&&x.question&&x.options.length===4));
 }
});
test('mini grade handles partial responses and does not invent ETS score',()=>{
 const mini=makeReadingMini(readings,0);
 const answers=Object.fromEntries(mini.slice(0,5).map(x=>[x.id,x.answer]));
 const grade=gradeReadingMini(mini,answers,2000);
 assert.equal(grade.correct,5);assert.equal(grade.total,9);assert.equal(grade.officialScore,null);
 assert.equal(grade.responses.filter(x=>x.selected===null).length,4);
 assert.equal(readingAdvice([grade]).weakest,'academic_passage');
 assert.equal(readingAdvice([]).weakest,null);
});
test('wall clock duration cannot become negative',()=>{
 assert.equal(remainingSeconds(0,12,12000),708);
 assert.equal(remainingSeconds(0,12,720001),0);
});
test('Listening task-type coverage is transcript-only and never claims licensed speech',()=>{
 assert.equal(listening.length,8);
 assert.equal(new Set(listening.map(x=>x.id)).size,8);
 for(const type of OFFICIAL_2026_TASKS.listening)assert.equal(listening.filter(x=>x.kind===type).length,2);
 for(const item of listening){
  assert.equal(item.audioStatus,'no_verified_audio');
  assert.equal(item.practiceMode,'transcript_study_only');
  assert.equal(item.source,'original-authored');
  assert.ok(item.script.length>50);assert.ok(item.questions.length>=1);
  for(const q of item.questions){assert.equal(q.options.length,4);assert.ok(q.answer>=0&&q.answer<4);assert.ok(q.explanation.length>30);}
 }
});
test('Writing hints only describe checklists without grammar/score assertions',()=>{
 const t=writing.find(x=>x.kind==='write_email');
 const c=writingChecklist(t,'Hello, I need assistance with a meeting. Thanks.');
 assert.equal(c.autoScore,null);assert.equal(c.editorReviewed,false);assert.ok(c.observations.length);
 assert.ok(writingStructureHints(writing.find(x=>x.kind==='academic_discussion'),'I agree.').length>=2);
});
