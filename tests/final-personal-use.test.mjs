import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {makeReadingDiagnostic,makeReadingMini,balanceReadingChoices,gradeReadingPractice} from '../js/toefl-prep.js';
const readings=JSON.parse(readFileSync(new URL('../data/toefl-reading-practice.json',import.meta.url)));
const app=readFileSync(new URL('../js/app.js',import.meta.url),'utf8');

test('new 50-question TOEFL practice balances answer positions without changing correct meanings, IDs or base items',()=>{
 const original=makeReadingDiagnostic(readings);
 const initial=JSON.stringify(original);
 const items=balanceReadingChoices(original);
 assert.equal(items.length,50);
 const count=[0,0,0,0];
 for(let i=0;i<items.length;i++){
  const a=original[i],b=items[i];
  assert.equal(a.id,b.id);assert.equal(a.type,b.type);assert.equal(b.options[b.answer],a.options[a.answer]);
  assert.deepEqual([...b.options].sort(),[...a.options].sort());
  count[b.answer]++;
 }
 assert.deepEqual(count,[13,13,12,12]);
 assert.equal(JSON.stringify(original),initial,'source content and prior sessions must not be mutated');
 assert.deepEqual(balanceReadingChoices(original),items,'session v2 must recreate identical choices on refresh');
 const score=gradeReadingPractice(items,Object.fromEntries(items.map(q=>[q.id,q.answer])));
 assert.equal(score.correct,50);assert.equal(score.officialScore,null);
});
test('nine-question practice is balanced and old unpermuted answers remain supported',()=>{
 const old=makeReadingMini(readings,0),now=balanceReadingChoices(old);
 assert.equal(now.length,9);
 const count=[0,0,0,0]; for(const q of now)count[q.answer]++;
 assert.deepEqual(count,[3,2,2,2]);
 assert.equal(gradeReadingPractice(old,Object.fromEntries(old.map(q=>[q.id,q.answer]))).correct,9);
 assert.match(app,/\!\[1,2\]\.includes\(a\.version\)/);
 assert.match(app,/a\.version===2.*balanceReadingChoices/);
 assert.match(app,/version:ui\.toeflMini\.version\|\|1/);
});
test('new Writing result denominator uses actual sentence task total, not legacy eight',()=>{
 assert.doesNotMatch(app,/exactReferenceMatches}\/8/);
 assert.ok(app.includes('${done.exactReferenceMatches}/${done.buildSentenceTotal||8}'));
});
