// Core offline cache verifier. Only machine-checked readiness is shown as ready.
const SECURE=()=>location.protocol==='https:'||['localhost','127.0.0.1','[::1]'].includes(location.hostname);
export async function checkOffline({repair=false}={}){
 if(!SECURE())return {ready:false,reason:'HTTPS (veya localhost) gerekli. ZIP içindeki index.html dosyasını file:// ile açmayın.'};
 if(!('serviceWorker' in navigator))return {ready:false,reason:'Bu tarayıcıda Service Worker desteklenmiyor.'};
 try{
  let registration=await navigator.serviceWorker.getRegistration('./');
  if(!registration)registration=await navigator.serviceWorker.register('./sw.js');
  if(repair)await Promise.race([registration.update().catch(()=>{}),new Promise(resolve=>setTimeout(resolve,12000))]);
  const readyRegistration=registration.active?registration:await Promise.race([navigator.serviceWorker.ready,new Promise(resolve=>setTimeout(()=>resolve(null),12000))]);
  const active=readyRegistration?.active;
  if(!active)return {ready:false,reason:'Önbellek yükleniyor. İnternet açıkken tekrar kontrol edin.'};
  return await new Promise(resolve=>{
   const channel=new MessageChannel();
   const timeout=setTimeout(()=>resolve({ready:false,reason:'Önbellek doğrulaması zaman aşımına uğradı.'}),20000);
   channel.port1.onmessage=({data})=>{clearTimeout(timeout);channel.port1.close();resolve(data?.ok?data:{ready:false,reason:data?.error||'Önbellek kontrolü başarısız.'});};
   active.postMessage({type:repair?'AEL_CACHE_REPAIR':'AEL_CACHE_STATUS'},[channel.port2]);
  });
 }catch(error){return {ready:false,reason:String(error)};}
}
export async function storageHealth() {
 if(!navigator.storage?.estimate)return {supported:false,warning:'Depolama durumunu bu tarayıcı göstermiyor; düzenli JSON yedeği alın.'};
 try {
  const size=await navigator.storage.estimate();
  const persistent=typeof navigator.storage.persisted==='function'?await navigator.storage.persisted():null;
  const bytes=Number.isFinite(size.usage)?size.usage:null;
  return {supported:true,usageBytes:bytes,quotaBytes:Number.isFinite(size.quota)?size.quota:null,
   persistent,warning:persistent===true?'Kalıcı depolama izni bildirildi; yine de ilerleme yedeği alın.':
    'Depolama Safari tarafından temizlenebilir. Öğrenme kayıtlarını düzenli JSON olarak yedekleyin.'};
 } catch(error){return {supported:false,warning:'Depolama kontrolü başarısız; JSON yedeği alın.'};}
}
export function offlinePanel(){return `<div class="panel" style="margin-top:16px"><h2>Safari · Çevrimdışı kullanım</h2><p class="mini" id="offlineReadiness" role="status" aria-live="polite">Henüz doğrulanmadı. İnternet açıkken kontrol edin.</p><button class="btn small primary" data-act="offlineCheck">İçerikleri indir / doğrula</button><p class="mini">İlk kullanımda HTTPS üzerinden uygulamayı açın ve bu düğmeye basın. Safari'de Paylaş → Ana Ekrana Ekle, ardından ana ekran uygulamasını açın ve internet açıkken bu düğmeye tekrar basın. Hazır onayından sonra uçak modunda kapatıp yeniden açarak test edin.</p><p class="mini" id="offlineStorageHealth" aria-live="polite">Depolama durumu kontrol edilmedi.</p><p class="mini">Kelime, Grammar, Reading, Writing ve TOEFL metinleri çevrimdışı hedeflenir. VOA gerçek insan sesi internet gerektirir. Cihazın depolama temizliği önbelleği veya ilerlemeyi silebilir: JSON yedeği alın.</p><hr class="divider"><h3>Uçak modu · kişisel cihaz testi</h3><p class="mini" id="offlineTrialStatus">Bu cihaz için test başlatılmadı. Bu kontrol bağımsız iPhone kalite onayı değildir.</p><div class="row"><button class="btn small soft" data-act="offlineTrialStart">1. Test işareti oluştur</button><button class="btn small soft" data-act="offlineTrialFinish">2. Uçak modunda doğrula</button></div><p class="mini">Önce içerikleri indir. Test işaretini oluştur, uçak moduna al, ana ekran uygulamasını kapatıp tekrar aç; bu ekrandaki ikinci düğmeyi kullan. Ses dosyaları çevrimdışı değildir.</p></div>`;}
export async function showOfflineStatus({repair=false}={}){
 const node=document.getElementById?.('offlineReadiness');if(!node)return;
 node.textContent='Önbellek dosyaları doğrulanıyor…';
 const result=await checkOffline({repair});
 if(!node.isConnected)return;
 node.textContent=result.ready?`✓ Çevrimdışı metin içeriği hazır: ${result.cached}/${result.total} dosya. iPhone Safari testi ayrıca gerekli.`:`✕ Henüz hazır değil: ${result.reason||`${result.cached||0}/${result.total||'?'} dosya. İnternet açıkken yeniden deneyin.`}`;
 const storage=document.getElementById?.('offlineStorageHealth');
 if(storage?.isConnected) {
  const status=await storageHealth();
  storage.textContent=`Depolama: ${status.usageBytes!==null&&status.usageBytes!==undefined?(status.usageBytes/1048576).toFixed(1)+' MB kullanım · ':''}${status.warning}`;
 }
}
