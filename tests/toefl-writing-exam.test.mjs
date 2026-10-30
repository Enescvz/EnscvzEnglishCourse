import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {makeWritingPractice,validateWritingPracticeSession,reviewWritingPractice,WRITING_PRACTICE_MINUTES} from '../js/toefl-writing-exam.js';
import {makeReadingDiagnostic,gradeReadingPractice} from '../js/toefl-prep.js';
const read=p=>JSON.parse(readFileSync(new URL(p,import.meta.url),'utf8'));
const writing=read('../data/toefl-writing-practice.json');const reading=read('../data/toefl-reading-practice.json');
test('2026 reading rehearsal has 50 original questions with 3 supported task types, zero official scores',()=>{
 const x=makeReadingDiagnostic(reading);assert.equal(x.length,50);assert.equal(new Set(x.map(q=>q.id)).size,50);
 for(const type of ['complete_words','daily_life','academic_passage'])assert.ok(x.some(q=>q.type===type));
 const answers=Object.fromEntries(x.map(q=>[q.id,q.answer]));const result=gradeReadingPractice(x,answers,1);
 assert.equal(result.correct,50);assert.equal(result.officialScore,null);
});
test('timed writing set has 10 sentence 1 email 1 discussion, unique ids, study only',()=>{
 for(const n of [0,1,9]){
  const t=makeWritingPractice(writing,n);assert.equal(t.length,12);assert.equal(new Set(t.map(x=>x.id)).size,12);
  assert.equal(t.filter(x=>x.kind==='build_sentence').length,10);
  assert.equal(t.filter(x=>x.kind==='write_email').length,1);
  assert.equal(t.filter(x=>x.kind==='academic_discussion').length,1);
  assert.equal(WRITING_PRACTICE_MINUTES,23);
 }
});
test('writing session rejects corruption, length abuse and missing IDs; valid drafts remain',()=>{
 const t=makeWritingPractice(writing);const now=Date.now();
 const a={version:2,startedAt:now-1000,minutes:23,ids:t.map(x=>x.id),answers:{[t[0].id]:'The library will close early because of renovations.'}};
 assert.equal(validateWritingPracticeSession(a,writing).answers[t[0].id],a.answers[t[0].id]);
 assert.equal(validateWritingPracticeSession({...a,ids:[...a.ids.slice(0,-1),'unknown']},writing),null);
 assert.equal(validateWritingPracticeSession({...a,minutes:999},writing),null);
 assert.equal(validateWritingPracticeSession({...a,startedAt:now+100000},writing),null);
 assert.ok(!('unknown' in validateWritingPracticeSession({...a,answers:{...a.answers,unknown:'x'}},writing).answers));
 assert.ok(!('x' in validateWritingPracticeSession({...a,answers:{[t[0].id]:'x'.repeat(12001)}},writing).answers));
});
test('legacy 8+2+2 session remains resumable without data loss',()=>{
 const legacy=[...writing.filter(x=>x.kind==='build_sentence').slice(0,8),...writing.filter(x=>x.kind==='write_email').slice(0,2),...writing.filter(x=>x.kind==='academic_discussion').slice(0,2)];
 const a={version:1,startedAt:Date.now()-5000,minutes:23,ids:legacy.map(x=>x.id),answers:{[legacy[0].id]:'Saved legacy draft'}};
 const recovered=validateWritingPracticeSession(a,writing);
 assert.equal(recovered.version,1);assert.equal(recovered.answers[legacy[0].id],'Saved legacy draft');
 assert.equal(recovered.ids.length,12);
 assert.equal(validateWritingPracticeSession({...a,version:2},writing),null);
});
test('open writing is not marked correct based on length; grammatical and ETS score fields are absent',()=>{
 const t=makeWritingPractice(writing);const answers=Object.fromEntries(t.map(x=>[x.id,x.kind==='build_sentence'?x.answer:'Hello, I am writing about the meeting. I would appreciate your advice. Best regards.']));
 const r=reviewWritingPractice(t,answers,1234);
 assert.equal(r.completed,12);assert.equal(r.exactReferenceMatches,10);assert.equal(r.officialScore,null);
 assert.equal(r.grammarGraded,false);assert.equal(r.semanticGraded,false);
 for(const x of r.review.filter(x=>x.kind!=='build_sentence')){
  assert.equal(x.editorReviewed,false);assert.ok(x.revisionSteps.length>0);
 }
 const missing=reviewWritingPractice(t,{},2345);assert.equal(missing.completed,0);assert.equal(missing.exactReferenceMatches,0);
});
test('TOEFL UI wires save/restore and does not touch speaking',()=>{
 const ui=readFileSync(new URL('../js/app.js',import.meta.url),'utf8');
 for(const value of ['toeflTimedWriting','persistWritingExam','restoreWritingExam','finishWritingExam','Writing provasını başlat'])assert.ok(ui.includes(value),value);
 assert.ok(ui.includes('Reading kapsam testi · 50 soru / 30 dk'));
});
