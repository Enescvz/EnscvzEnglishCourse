import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const ui=readFileSync(new URL('../js/app.js',import.meta.url),'utf8');
test('dashboard reflects current 400 word / 75 phrasal TOEFL shared set without older totals',()=>{
  assert.ok(ui.includes('400 kelime ve 75 phrasal verb.'));
  assert.ok(!ui.includes('200 kelime ve 50 phrasal verb.'));
});
