import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {makeReadingMini,makeReadingDiagnostic,gradeReadingPractice,readingAdvice,readingReviewPlan,remainingSeconds,READING_DIAGNOSTIC_MINUTES} from '../js/toefl-prep.js';
import {writingChecklist,writingDraftMetrics,writingRevisionSteps} from '../js/toefl-writing.js';
const data=JSON.parse(readFileSync(new URL('../data/toefl-reading-practice.json',import.meta.url)));
const write=JSON.parse(readFileSync(new URL('../data/toefl-writing-practice.json',import.meta.url)));
test('Reading diagnostic preserves all authored question identities and does not inflate ETS-equivalence',()=>{
 const q=makeReadingDiagnostic(data);
 assert.equal(q.length,50);
 assert.equal(new Set(q.map(x=>x.id)).size,50);
 assert.equal(q.filter(x=>x.type==='complete_words').length,16);
 assert.equal(q.filter(x=>x.type==='daily_life').length,16);
 assert.equal(q.filter(x=>x.type==='academic_passage').length,18);
 assert.equal(READING_DIAGNOSTIC_MINUTES,30);
 const answers=Object.fromEntries(q.slice(0,8).map(x=>[x.id,x.answer]));
 const score=gradeReadingPractice(q,answers,1);
 assert.equal(score.correct,8);assert.equal(score.total,50);assert.equal(score.unanswered,42);
 assert.equal(score.officialScore,null);
 assert.equal(score.kind,'original_timed_reading_diagnostic');
 assert.ok(readingAdvice([score]).weakest);
 assert.equal(readingReviewPlan([score]).length,3);
});
test('scoring rejects tampered items, forged answers and duplicate IDs',()=>{
 const q=makeReadingDiagnostic(data);
 assert.throws(()=>gradeReadingPractice([q[0],q[0]],{}),/Invalid/);
 assert.throws(()=>gradeReadingPractice([{...q[0],answer:77}],{}),/Invalid/);
 const out=gradeReadingPractice([q[0]],{[q[0].id]:999},4);
 assert.equal(out.correct,0);assert.equal(out.unanswered,1);assert.equal(out.responses[0].selected,null);
});
test('expired timers cannot gain extra time',()=>{
 assert.equal(remainingSeconds(1,30,1+30*60000+100),0);
 assert.equal(remainingSeconds(1,30,1+29*60000),60);
});
test('writing analysis gives concrete revision suggestions but never grades language',()=>{
 const t=write.find(x=>x.kind==='write_email');
 const content='Hello, I am writing about the workshop. I cannot attend today. Can I come tomorrow? Thank you. Regards, Student.';
 const m=writingDraftMetrics(content);assert.ok(m.wordCount>10);assert.ok(m.sentenceCount>=3);
 const c=writingChecklist(t,content);
 assert.equal(c.autoScore,null);assert.equal(c.editorReviewed,false);
 assert.ok(c.revisionSteps.some(x=>x.includes('Alıcının rolünü')));
 assert.ok(writingRevisionSteps(t,'').some(x=>x.includes('Önce İngilizce')));
});
