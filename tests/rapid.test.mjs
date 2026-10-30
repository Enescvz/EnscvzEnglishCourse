import test from 'node:test';
import assert from 'node:assert/strict';
import {normalizeRapidDeck,rapidFiltered,rapidDue,rapidRecord} from '../js/rapid.js';
const cards=[{id:'r1',word:'credible',tr:'inandırıcı',level:'C1'},{id:'r2',word:'scrutiny',tr:'inceleme',level:'C1'},{id:'r3',word:'durable',tr:'dayanıklı',level:'B2'}];
test('rapid deck excludes overlaps with full general lessons and duplicate headwords',()=>{
 assert.deepEqual(normalizeRapidDeck([...cards,cards[0],{id:'oops',word:' ',tr:'x',level:'B2'}],[{word:'scrutiny',category:'general'}]).map(x=>x.id),['r1','r3']);
});
test('rapid filters Turkish as well as English, without altering input',()=>{
 assert.equal(rapidFiltered(cards,{query:'İNandırıcı'}).total,1);
 assert.equal(rapidFiltered(cards,{level:'B2'}).items[0].word,'durable');
 assert.equal(cards.length,3);
});
test('a correct rapid recognition schedules review but never claims mastery',()=>{
 const x=rapidRecord(null,true,1000);
 assert.equal(x.streak,1);assert.equal(x.dueAt,1000+86400000);
 assert.equal(x.lastAnswer,'remembered');assert.equal(x.mastered,undefined);
 assert.equal(rapidDue(x,1000),false);
});
test('unknown answer returns in ten minutes and resets streak',()=>{
 const x=rapidRecord(rapidRecord(null,true,1000),false,3000);
 assert.equal(x.dueAt,3000+600000);assert.equal(x.streak,0);
 assert.equal(x.seen,2);assert.equal(x.correct,1);
});
test('due filter excludes unseen cards and retrieves the due card',()=>{
 const prog={r1:{dueAt:10},r2:{dueAt:30000}};
 const result=rapidFiltered(cards,{status:'due'},prog,100);
 assert.deepEqual(result.items.map(x=>x.id),['r1']);
 assert.equal(rapidFiltered(cards,{status:'new'},prog,100).total,1);
});
test('empty result clamps page and handles no card',()=>{
 const result=rapidFiltered(cards,{query:'NOT_PRESENT',page:900});
 assert.equal(result.page,0);assert.equal(result.pages,1);assert.equal(result.items.length,0);
});
