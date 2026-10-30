/** Non-destructive local backup import for a personal, offline-first learning app.
 * No cloud transfer, no progress keys/IDs removed, no fabricated mastery.
 */
const OBJECT = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const BLOCKED = new Set(['__proto__','constructor','prototype']);
const safeEntries = value => Object.entries(value).filter(([key]) => !BLOCKED.has(key));
function cleanMap(value) {
  if(!OBJECT(value)) throw Error('Beklenen veri nesnesi eksik veya hatalı.');
  return Object.fromEntries(safeEntries(value));
}
const timestamp = item => Number.isFinite(item?.last) ? item.last :
  Number.isFinite(item?.at) ? item.at : Number.isFinite(item?.startedAt) ? item.startedAt : -1;
function mergeKeyed(current = {}, incoming = {}) {
  const a=cleanMap(current), b=cleanMap(incoming), out={...b,...a};
  for (const key of Object.keys(b)) {
    // Never let an older exported FSRS state roll back a newer reviewed card.
    if(OBJECT(a[key]) && OBJECT(b[key])) {
      out[key]=timestamp(b[key])>timestamp(a[key])?b[key]:a[key];
    }
  }
  return out;
}
function mergeHistory(current = [], incoming = []) {
  if(!Array.isArray(current)||!Array.isArray(incoming)) throw Error('Çalışma geçmişi hatalı.');
  // Multiset union: retain even identical records that were genuinely recorded
  // twice on the device, without doubling a history re-imported from the same backup.
  const existingCount=new Map(),importedCount=new Map(),out=[...current];
  for(const item of current) {
    if(!OBJECT(item))continue;
    const id=JSON.stringify(item);
    existingCount.set(id,(existingCount.get(id)||0)+1);
  }
  for(const item of incoming) {
    if(!OBJECT(item))continue;
    const id=JSON.stringify(item),count=(importedCount.get(id)||0)+1;
    importedCount.set(id,count);
    if(count>(existingCount.get(id)||0))out.push(item);
  }
  return out;
}
const MAPS=['cards','phrasals','expressions','lessons','writing','authenticLessons','rapidCards','memoryCues','skillCards','fluencyCards','fluencyDrafts'];
const HISTORIES=['listenHistory','quizHistory','events','reviewHistory','toeflAttempts','toeflWritingAttempts','skillHistory','fluencyHistory'];
export function validateProgressBackup(backup) {
  if(!OBJECT(backup)||backup.app!=='American English Lab'||backup.format!==1||!OBJECT(backup.progress)||backup.progress.version!==1)
    throw Error('Bu dosya American English Lab v1 ilerleme yedeği değil.');
  const p=backup.progress;
  for(const key of ['settings','cards','phrasals'])if(!OBJECT(p[key]))throw Error(`${key} alanı eksik veya hatalı.`);
  for(const key of MAPS)if(p[key]!==undefined&&!OBJECT(p[key]))throw Error(`${key} alanı hatalı.`);
  for(const key of HISTORIES)if(p[key]!==undefined&&!Array.isArray(p[key]))throw Error(`${key} geçmişi hatalı.`);
  if(p.dateLog!==undefined&&!OBJECT(p.dateLog))throw Error('dateLog alanı hatalı.');
  return p;
}
export function mergeProgress(current,backup) {
  const incoming=validateProgressBackup(backup);
  if(!OBJECT(current)||current.version!==1)throw Error('Mevcut ilerleme verisi hatalı.');
  // Preserve all unknown current fields (including legacy progress and learning IDs).
  // If the imported file has extra fields, retain them too, except unsafe object keys.
  const merged={...Object.fromEntries(safeEntries(incoming)),...Object.fromEntries(safeEntries(current)),version:1};
  for(const key of MAPS)merged[key]=mergeKeyed(current[key]||{},incoming[key]||{});
  for(const key of HISTORIES)merged[key]=mergeHistory(current[key]||[],incoming[key]||[]);
  merged.settings={...cleanMap(incoming.settings),...cleanMap(current.settings||{})};
  const dayA=cleanMap(current.dateLog||{}),dayB=cleanMap(incoming.dateLog||{});
  merged.dateLog={...dayB,...dayA};
  for(const [day,value] of safeEntries(dayB)) {
    if(Number.isFinite(value)&&Number.isFinite(dayA[day]))merged.dateLog[day]=Math.max(dayA[day],value);
  }
  // Do not roll active timed exercises back to an older session.
  for(const key of ['toeflActiveReading','toeflActiveWriting']){
    const a=current[key], b=incoming[key];
    if(!a&&b)merged[key]=b;
    else if(a&&b)merged[key]=timestamp(b)>timestamp(a)?b:a;
  }
  return merged;
}
