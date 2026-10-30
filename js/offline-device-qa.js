/** Local user-observed check. This is NOT independent physical iPhone QA. */
export function newOfflineTrial(now=Date.now(),marker=''){
 if(!Number.isFinite(now)||!marker)throw Error('Missing offline trial identifier');
 return {marker,startedAt:now,status:'awaiting_airplane_mode_test',origin:'user_local_test'};
}
export function verifyOfflineTrial(trial,{marker,cacheReady,networkOffline,appReloaded,now=Date.now()}){
 if(!trial||trial.marker!==marker||!Number.isFinite(trial.startedAt)||now<trial.startedAt)
  return {pass:false,reason:'Yerel test kimliği kayboldu veya değiştirilmiş.'};
 const pass=cacheReady===true&&networkOffline===true&&appReloaded===true;
 return {pass,reason:pass?'Kullanıcı cihazında uçak modu testi raporlandı. Bağımsız iPhone QA değil.':
 'Uçak modu, yeniden açılış veya önbellek kontrolünden biri doğrulanamadı.',
  at:now,method:'device_self_report_only',independentIPhoneQA:false};
}
