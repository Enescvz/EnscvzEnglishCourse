import test from 'node:test';
import assert from 'node:assert/strict';
import {describeHumanAudioEvent,bindHumanAudioStatus} from '../js/human-audio-status.js';
test('VOA audio state never labels loading or metadata as validated Listening',()=>{
 const idle=describeHumanAudioEvent('idle');
 const loading=describeHumanAudioEvent('loading');
 const meta=describeHumanAudioEvent('loadedmetadata');
 for(const text of [idle,loading,meta]) assert.doesNotMatch(text,/başarıyla doğrulandı|onaylandı/i);
 assert.match(describeHumanAudioEvent('playing'),/tarayıcı oynatma/i);
 assert.match(describeHumanAudioEvent('error',4,true),/desteklenmedi/i);
 assert.match(describeHumanAudioEvent('error',2,false),/çevrimdışı/i);
});
test('VOA player attaches diagnostics without auto-play or modifying learning progress',()=>{
 const listeners={};let played=0;
 const media={addEventListener:(event,fn)=>{listeners[event]=fn;},play(){played++;},error:null};
 const output={textContent:''};
 assert.equal(bindHumanAudioStatus(media,output,{online:()=>false}),true);
 assert.match(output.textContent,/henüz/i);
 media.error={code:2};listeners.error();
 assert.match(output.textContent,/internet gerekir/i);
 media.error=null;listeners.playing();
 assert.match(output.textContent,/cihaz QA onayı değildir/i);
 assert.equal(played,0);
 assert.equal(bindHumanAudioStatus(null,output),false);
});
