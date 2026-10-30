# Robotik Podcastlerin Kaldırılması — Özel QA (29.10.2026)

**Karar:** Kullanıcı robotik sesli podcast istemiyor. 18 eski podcast + 24 kısa alıştırmanın 42 eSpeak MP3 dosyası çıkarıldı. Script ve testleri silinmedi; eski öğrenme kayıtlarıyla uyumluluk için ID'ler ve `data/episodes.json`, `data/drills.json`, `data/audio-provenance.json` dosyaları birebir korundu.

## Değişiklikler
- `Podcasts` ekranı robotik kayıtları listelemiyor/oynatmıyor. Gerçek insan sesli VOA kaynaklarına yönlendiriyor.
- Listening ana ekranından robotik kısa alıştırmaların düğmeleri kaldırıldı; günlük görev planından robotik kayıt önerileri çıkarıldı.
- `Daily Conversations` kayıtlı robotik ses yerine gerçek ses kaynaklarına yönlendiriyor. Eski konuşma metinleri saklandı.
- Doğrudan eski `openEpisode`/`openDrill` eylemleri ve ilerleme kaydı oluşturma korumalı; sesli etkinlik sayılmaz.
- Service worker 42 robotik MP3'ü önbelleğe almıyor; yeni sürüm etkinleşince eski AEL cache'leri siliniyor. Önceden açık sekmeler için yeniden yükleme gerekir.
- Yeni MP3 oluşturulmadı. Kelime okunuşundaki isteğe bağlı tarayıcı TTS bu podcast kararı kapsamı dışındadır; gerçek insan sesli Listening başarısı değildir.

## Testler ve eksikler
- 107 JavaScript + 190 Python = 297/297 otomatik test PASS.
- Kaynak yedeğe göre 14 kritik veri dosyası, Speaking fonksiyonu ve mikrofon olay kodu aynı; hiçbir kart ID'si veya öğrenme geçmişi aktarımı silinmedi.
- Sanal Chromium web sayfası yönlendirmesi ortam politikasından engellendi; fiziksel iPhone/Safari testi yok.
- Mevcut 50 VOA yayımcı dersinin MP3'leri çevrimiçi kaynakta; 0 yerel doğrulanmış insan sesli MP3. Gerçek oynatma doğrulanmadı.
- Arşivlenen 18 eski podcast ve 24 kısa alıştırma, yeni onaylı insan sesleri eklenene kadar **kapalıdır**.
- Yayın kapısı **LOCKED**. Bu dosya ve ZIP yalnızca özel geliştirme yedeğidir; Github Pages'e yayımlamayın.

Bu rapor *yeni insan podcast üretildiğini* veya ses QA onayı verildiğini iddia etmez.
