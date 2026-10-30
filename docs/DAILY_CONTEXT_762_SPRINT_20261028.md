# American English Lab — 762 günlük bağlamlı genel kelime (28 Ekim 2026)

**Durum: ÖZEL GELİŞTİRME / YAYINLAMA KİLİTLİ.** Bu kayıt eğitim içeriğinin bağımsız bir İngilizce editörü tarafından onaylandığı anlamına gelmez.

## Gerçekte yapılanlar

- Mevcut 584 genel bağlamlı derse **178 özgün ders taslağı** eklendi: **132 B2 + 46 C1**. Yeni kayıtların tamamında Türkçe anlam, açıklayıcı İngilizce tanım, birbirinden farklı iki somut gündelik kullanım cümlesi ve kendi cümleni kurma yönlendirmesi var.
- Bütün yeni başlıklar mevcut odak müfredatında ve B2/C1 kaynak aday kataloğunda teyit edildi. Kod, kaynaksız başlığı veya kaynak seviyesiyle uyuşmayan girdiyi reddediyor. B2/C1 seviyeleri **kaynak adayıdır; bağımsız düzey doğrulaması değildir**.
- Tüm eski bağlamlı dersler ve kart ID'leri değişmeden korundu. Hızlı kartlardan bağlamlı derse dönüşen **178 tekrar kaydı** `data/rapid-vocabulary.json` dosyasından çıkarıldı; cihazdaki `localStorage` / JSON ilerleme dosyaları değiştirilmedi. Hızlı karttaki tanıma başarıları bağlamlı konuşma ustalığına aktarılmadı.
- `data/fluency-focus.json` ve `data/candidate-catalog.json` yeniden üretildi. Çevrimdışı uygulama cache sürümü güncellendi, 42 MP3 servis çalışanı manifestinde kaldı.
- Toplu yazar idempotent: ikinci kez çalıştırıldığında 0 yeni kart oluşturuyor.

## Doğrulanan rakamlar

| Kapsam | Önce | Şimdi |
|---|---:|---:|
| Bağlamlı genel ders taslağı | 584 | **762** |
| Hedef müfredatta hızlı anlam kartı | 416 | **238** |
| Hedef müfredatta yalnızca başlık | 0 | **0** |
| Bağlamlı phrasal verb | 500 | **500** |
| Muhasebe/finans terimi | 284 | **284** |
| Toplam bağımsız hızlı kart | 817 | **639** |
| Genel kelimede eksik ikinci örnek | 0 | **0** |
| Finans/muhasebede eksik ikinci örnek | 232 | **232** |

- `npm run test:all`: **46 Node + 69 Python = 115 test başarılı**.
- `python tools/audit_examples.py`: 762 genel + 500 phrasal kartta en az iki farklı örnek; kalan 232 tek örnekli uzmanlık kartı açıkça raporlanıyor.
- Sanal Chromium test günlükleri `PASS desktop`, `PASS mobile` dedi, fakat süreç kapanışta **zaman aşımına uğradı**. Bu yüzden tam başarılı E2E sonucu olarak sunulmuyor. Bu test sanal origin ve sahte localStorage kullanıyor; gerçek iPhone Safari/WebKit testinin yerine geçmez.
- `python tools/release_gate.py`: **LOCKED**, beklenen çıkış kodu 1. Hiçbir yayın / Pages / GitHub / Drive eylemi yapılmadı.

## Önemli sınırlamalar

- Hedef liste, ölçülmüş Amerikan konuşma korpus frekansına göre sıralanmamıştır. Özellikle kalan 238 kelime arasında günlük kullanım açısından zayıf adaylar bulunuyor; yalnızca hedef sayıyı doldurmak için otomatik bağlam uydurulmayacak. Bir sonraki adım: seçim ve gerekirse yer değiştirme editoryal kontrolü ile 238 hızlı kartı bağlamlı derslere dönüştürmek.
- Sentetik ses dosyaları insan kaydı değildir. Telaffuz ve bağlam kontrolü için bağımsız dil doğrulaması gerekir.
- Bu yedek kaynakları, önbelleği ve testleri içerir; yayımlanabilir son paket değildir.

## Bu turun dosyaları

- `tools/author_daily_context_sprint_20261028.py`: 178 özgün bağlamlı kartı kaynak doğrulamalı ve idempotent ekler.
- `sources/authored-20261028-daily-context-sprint.jsonl`: aynı derslerin taşınabilir JSONL kaynağı.
- `tools/reconcile_rapid_promotions.py`: dersle örtüşen hızlı kartları idempotent temizler.
- `qa/rapid-promotion-reconcile.json`: 178 dönüşüm, 639 kalan hızlı kart.
- `tests/test_daily_context_sprint_20261028.py`: yeni kaynak/kart/tekillik/idempotence regresyon testleri.

**Sıradaki görev:** 238 odak kelimenin konuşma yararını tekrar seç, bağlamlı dersler hâline getir; ayrıca finans bölümünde 232 eksik ikinci örneği tamamla; aktif dinleme ve üretim alıştırmalarını genişlet. Bütün yayın kısıtları geçerli.
