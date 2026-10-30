import test from 'node:test';
import assert from 'node:assert/strict';
import {retentionAudit} from '../js/retention-audit.js';
import {compareHumanReviews} from '../js/toefl-human-review.js';
const DAY=86400000,now=45*DAY;
test('7-day and 30-day windows count only real followups, no invented success',()=>{
 const hist=[{at:0,id:'a',grade:'good'},{at:7*DAY,id:'a',grade:'good'},
 {at:30*DAY,id:'a',grade:'again'},{at:0,id:'b',grade:'good'},
 {at:9*DAY,id:'b',grade:'hard'},{at:0,id:'c',grade:'again'}];
 const result=retentionAudit(hist,now);
 assert.deepEqual(result.windows.map(x=>[x.eligible,x.observed,x.remembered,x.failed]),[[3,2,1,0],[3,1,0,1]]);
 assert.equal(result.windows[1].observedRecallRate,0);
 assert.equal(result.windows[0].effortful,1);assert.equal(result.windows[0].observedRecallRate,50);
 assert.equal(result.windows[1].missingFollowUps,2);
});
test('missing follow-up never becomes success',()=>{
 const x=retentionAudit([{id:'a',at:0,grade:'easy'}],35*DAY).windows;
 assert.equal(x[0].observed,0);assert.equal(x[0].observedRecallRate,null);
});
test('invalid future or malformed review skipped',()=>{
 const x=retentionAudit([{at:40*DAY,id:'future',grade:'good'},{at:0,id:'a',grade:'unknown'}],10*DAY);
 assert.equal(x.cardsWithHistory,0);
});
test('two human reviews never yield an official TOEFL score',()=>{
 const a={taskFulfillment:4,coherence:3,languageUse:4,development:2};
 const b={taskFulfillment:4,coherence:5,languageUse:3,development:2};
 const v=compareHumanReviews(a,b);
 assert.equal(v.needsAdjudication,true);assert.equal(v.officialTOEFLScore,null);
 assert.throws(()=>compareHumanReviews(a,{...b,development:6}));
});
