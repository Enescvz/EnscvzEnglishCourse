/** Runtime diagnostic, NOT independent audio QA or proof of transcript alignment. */
export function describeHumanAudioEvent(eventName, code = 0, online = true) {
  if (eventName === 'loading') return 'VOA kaydı yükleniyor. İnternet bağlantısı gereklidir.';
  if (eventName === 'loadedmetadata') return 'Ses dosyasının bilgileri alındı; sesin gerçekten duyulduğu henüz doğrulanmadı.';
  if (eventName === 'playing') return 'Tarayıcı oynatma olayını bildirdi. Duyduğunuz sesi siz kontrol edin; bu fiziksel cihaz QA onayı değildir.';
  if (eventName === 'waiting' || eventName === 'stalled') return 'Akış duraksadı. Bağlantıyı kontrol edin, gerekirse VOA kaynağını açın.';
  if (eventName === 'error') {
    if (!online) return 'Çevrimdışı durumdasınız. VOA ses kaydı yerel olarak yüklenmedi; internet gerekir.';
    const cases = {1:'Oynatma durduruldu.',2:'Ağ hatası: ses indirilemedi.',3:'Ses dosyası çözümlenemedi.',4:'Ses biçimi veya URL tarayıcı tarafından desteklenmedi.'};
    return (cases[code]||'VOA ses kaydı açılamadı.')+' Kaynak sayfasından tekrar deneyin.';
  }
  return 'Ses henüz başlatılmadı. Oynat düğmesine basın; oynatma gerçekleşmeden dinleme başarı onayı verilmez.';
}
export function bindHumanAudioStatus(media, status, {online = () => true} = {}) {
  if (!media || !status) return false;
  const set = (eventName) => {status.textContent = describeHumanAudioEvent(eventName, media.error?.code || 0, online());};
  for (const eventName of ['loadstart', 'loadedmetadata', 'playing', 'waiting', 'stalled', 'error']) {
    media.addEventListener(eventName, () => set(eventName === 'loadstart' ? 'loading' : eventName));
  }
  set('idle');
  return true;
}
