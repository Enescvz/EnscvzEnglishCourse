import test from 'node:test';
import assert from 'node:assert/strict';
import {FSRS_VERSION,FSRS_WEIGHTS,fsrsInitialDifficulty,fsrsInterval,fsrsRetrievability,fsrsState,reviewItem,MS_DAY} from '../js/engine.js';
const EPS=1e-9;
test('FSRS-5 defaults and 90-percent forgetting curve are grounded',()=>{
  assert.equal(FSRS_VERSION,5);
  assert.equal(FSRS_WEIGHTS.length,19);
  assert.equal(FSRS_WEIGHTS[0],0.40255);
  for(const stability of [0.4,1,3.173,100]){
    assert.ok(Math.abs(fsrsRetrievability(stability,stability)-0.9)<EPS);
    assert.ok(Math.abs(fsrsInterval(stability)-stability)<EPS);
  }
});
test('initial grades match FSRS-5 initial stability weights',()=>{
  for(const [i,grade] of ['again','hard','good','easy'].entries()){
    const s=fsrsState({},grade,1_000_000);
    assert.equal(s.fsrsVersion,5);
    assert.equal(s.stability,FSRS_WEIGHTS[i]);
    assert.equal(s.difficulty,fsrsInitialDifficulty(i+1));
    assert.ok(s.due>1_000_000);
  }
  assert.equal(fsrsState({},'again',1000).interval,15/1440);
});
test('FSRS honors difficulty, memory decay, and performance',()=>{
  const t=100000;
  const good=fsrsState({},'good',t);
  const hard=fsrsState({},'hard',t);
  const easy=fsrsState({},'easy',t);
  assert.ok(good.interval>hard.interval);
  assert.ok(easy.interval>good.interval);
  assert.ok(fsrsRetrievability(20,good.stability)<fsrsRetrievability(5,good.stability));
  const delayed=fsrsState({...good,attempts:1},'good',t+30*MS_DAY);
  const ontime=fsrsState({...good,attempts:1},'good',t+3*MS_DAY);
  assert.ok(delayed.stability>ontime.stability);
});
test('legacy adaptive records migrate without dropping review history',()=>{
  const old={attempts:8,reps:6,interval:24,last:5*MS_DAY,lapses:1,custom:'keep-me',modeSuccess:{recall:2,production:1,context:1,listening:1}};
  const p=reviewItem(old,'good','listening',30*MS_DAY);
  assert.equal(p.attempts,9);
  assert.equal(p.reps,7);
  assert.equal(p.lapses,1);
  assert.equal(p.custom,'keep-me');
  assert.equal(p.fsrsVersion,5);
  assert.ok(p.stability>0);
  assert.ok(p.difficulty>=1&&p.difficulty<=10);
  assert.equal(p.modeSuccess.listening,2);
  assert.equal(p.status,'Pekişmiş');
});
test('same-day successful reviews never lose stability, failed reviews reset modality mastery',()=>{
  const now=MS_DAY*2;
  let p=reviewItem({},'good','recall',now);
  let next=reviewItem(p,'good','recall',now+5*60*1000);
  assert.ok(next.stability>=p.stability);
  next=reviewItem(next,'again','recall',now+20*60*1000);
  assert.equal(next.status,'Tekrar gerekli');
  assert.deepEqual(next.modeSuccess,{});
  assert.equal(next.due,now+35*60*1000);
});
test('invalid grade, retention and stability are rejected',()=>{
  assert.throws(()=>fsrsState({},'perfect'),/Invalid review grade/);
  assert.throws(()=>fsrsInterval(0),/Invalid FSRS inputs/);
  assert.throws(()=>fsrsInterval(2,1),/Invalid FSRS inputs/);
  assert.throws(()=>fsrsRetrievability(2,0),/Stability/);
});
