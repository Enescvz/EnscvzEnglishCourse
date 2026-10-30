import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
const tasks=JSON.parse(readFileSync(new URL('../data/toefl-reading-practice.json',import.meta.url)));
test('Original 2026 TOEFL reading-style tasks cover all three official categories',()=>{
 assert.equal(tasks.length,18);
 assert.equal(new Set(tasks.map(x=>x.id)).size,tasks.length);
 for(const type of ['complete_words','daily_life','academic_passage'])assert.equal(tasks.filter(x=>x.type===type).length,6);
 for(const t of tasks){assert.ok(t.body.length>150);assert.ok(t.questions.length>=2);for(const q of t.questions){assert.equal(q.options.length,4);assert.ok(q.answer>=0&&q.answer<4);assert.ok(q.explanation.length>30);}}
});
