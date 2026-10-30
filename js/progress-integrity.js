/** Conservative v1 progress recovery. Never overwrite unparseable stored data silently.
 * The original raw value stays in browser storage until the learner deliberately imports
 * a valid backup or explicitly resets progress. No network or telemetry.
 */
const record = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const unsafe = new Set(['__proto__','prototype','constructor']);
const safe = value => Object.fromEntries(Object.entries(value).filter(([key]) => !unsafe.has(key)));
const MAPS = ['cards','phrasals','expressions','lessons','writing','authenticLessons','rapidCards','memoryCues','skillCards','fluencyCards','fluencyDrafts','dateLog'];
const HISTORIES = ['listenHistory','quizHistory','events','reviewHistory','toeflAttempts','toeflWritingAttempts','skillHistory','fluencyHistory'];
export function loadProgressRecord(raw,defaults){
 if (!record(defaults) || defaults.version !== 1) throw Error('Default progress must be v1');
 if(raw===null || raw===undefined)return {progress:{...defaults},protectedRaw:null,issue:null};
 try{
  const parsed=JSON.parse(raw);
  if(!record(parsed)||parsed.version!==1)throw Error('İlerleme sürümü bilinmiyor.');
  if(parsed.settings!==undefined&&!record(parsed.settings))throw Error('Ayarların veri biçimi bozuk.');
  for(const key of MAPS)if(parsed[key]!==undefined&&!record(parsed[key]))throw Error(`${key} veri biçimi bozuk.`);
  for(const key of HISTORIES)if(parsed[key]!==undefined&&!Array.isArray(parsed[key]))throw Error(`${key} geçmişi bozuk.`);
  const progress={...defaults,...safe(parsed),settings:{...defaults.settings,...safe(parsed.settings||{})}};
  for(const key of MAPS)progress[key]=safe(parsed[key]||defaults[key]||{});
  for(const key of HISTORIES)progress[key]=parsed[key]||defaults[key]||[];
  return {progress,protectedRaw:null,issue:null};
 }catch(error){
  return {progress:{...defaults},protectedRaw:raw,issue:`Kayıt okunamadı: ${error.message}`};
 }
}
