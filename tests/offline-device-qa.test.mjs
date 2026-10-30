import test from 'node:test';import assert from 'node:assert/strict';
import {newOfflineTrial,verifyOfflineTrial} from '../js/offline-device-qa.js';
test('airplane mode without reload or cache cannot pass',()=>{
 const t=newOfflineTrial(100,'stable');
 for(const patch of [{cacheReady:false},{networkOffline:false},{appReloaded:false}]){
  const args={marker:'stable',cacheReady:true,networkOffline:true,appReloaded:true,now:200,...patch};
  assert.equal(verifyOfflineTrial(t,args).pass,false);
 }
 assert.equal(verifyOfflineTrial(t,{marker:'wrong',cacheReady:true,networkOffline:true,appReloaded:true,now:200}).pass,false);
});
test('self-report never claims independent physical iPhone QA',()=>{
 const x=verifyOfflineTrial(newOfflineTrial(10,'t'),{marker:'t',cacheReady:true,networkOffline:true,appReloaded:true,now:20});
 assert.equal(x.pass,true);assert.equal(x.independentIPhoneQA,false);
});
