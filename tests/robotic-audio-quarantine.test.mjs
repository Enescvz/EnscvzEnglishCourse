import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const root=new URL('../',import.meta.url);
const app=fs.readFileSync(new URL('../js/app.js',import.meta.url),'utf8');
const worker=fs.readFileSync(new URL('../sw.js',import.meta.url),'utf8');
const records=JSON.parse(fs.readFileSync(new URL('../data/audio-provenance.json',import.meta.url),'utf8'));
test('robotic podcast assets absent, VOAs unaffected, and UI has no synthetic player entries',()=>{
 assert.equal(Object.keys(records.recordings).length,42);
 for(const record of Object.values(records.recordings)){
  assert.equal(record.quality,'unapproved_robotic');
  assert.equal(fs.existsSync(new URL('../'+record.audio,import.meta.url)),false);
 }
 assert.ok(app.includes('Robotik podcast yayında değil'));
 assert.ok(app.includes('case \'openEpisode\':stopAudio();ui.episode=null;'));
 assert.ok(app.includes('case \'openDrill\':stopAudio();ui.drill=null;'));
 assert.ok(!app.includes('data-act="openEpisode"'));
 assert.ok(worker.includes('const AUDIO=[];'));
 assert.ok(!worker.includes("'AEL_CACHE_LEGACY_AUDIO'"));
 assert.equal(JSON.parse(fs.readFileSync(new URL('../data/voa-source-catalog.json',import.meta.url))).length,50);
});
