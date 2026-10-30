# American English Lab — Kişisel Kullanım Öncesi Nihai Teknik / İçerik QA

**Tarih:** 29 Ekim 2026  
**Temel:** `AEL_PRIVATE_DEV_BACKUP_20261029_TOEFL_ONLY_WRITING1011_CLOZE_QA_DO_NOT_DEPLOY.zip`  
**Kapsam:** AEL'nin gerçek dosya yapısı, veri bütünlüğü, TOEFL Reading/Writing, öğrenme kayıtları, PWA önbelleği ve kullanıcı arayüzü.  
**Karar:** **KOŞULLU KİŞİSEL PİLOT** (Windows'ta yerel HTTP için); **KAMUYA YAYIN ONAYI VERİLMEDİ.** Fiziksel iPhone Safari ve gerçek offline uçtan uca test **YAPILMADI**. Speaking ve Listening kodu bu turda değiştirilmedi.

## 1. Ölçülebilir kontroller

| Kontrol | Sonuç | Sınır |
|---|---:|---|
| JavaScript birim/regresyon testleri | **97/97 geçti** | Davranışların yalnızca test kapsamındaki bölümü |
| Python içerik/müfredat testleri | **180/180 geçti** | Bağımsız insan editörlüğü değil |
| Toplam otomatik test | **277/277 geçti** | Yayın/onay sertifikası değil |
| Ek yapısal içerik denetimi | **14/14 geçti** | Kaynak metinlerin tek tek anlamsal onayı değil |
| Service worker önbellek listesi | **34/34 dosya yerinde ve yerel HTTP GET 200** | Safari offline çalışma kanıtı değil |
| Chromium sanal origin arayüz testi | **Masaüstü + mobil viewport geçti** | URL ve localStorage sahte katmanla sağlandı |
| Gerçek HTTP + Chromium | **Engellendi** (`ERR_BLOCKED_BY_ADMINISTRATOR`) | Başarılı sayılmadı |
| Otomatik WebKit | **Yüklü WebKit yürütülebilir dosyası yok** | Safari eşdeğer testi yapılamadı |
| Fiziksel iPhone Safari / uçak modu | **Test edilmedi** | Yayın engeli |
| Ses kalite kapısı | **42/42 sentetik ses onaysız** | Doğal insan sesi olarak sunulmamalı |
| Yayın kapısı | **LOCKED** (beklenen) | Kasten açılmadı |

## 2. Bu denetimde bulunan ve düzeltilen hatalar

1. **Reading cevap şıkkı önyargısı:** Eski 50 soruluk kaynak havuzda doğru şıklar A=10, B=27, C=11, D=2 dağılımındaydı. Yeni Reading oturumlarında, orijinal soru kimliği ve doğru metin korunarak **A=13, B=13, C=12, D=12** pozisyon dengesi sağlanıyor. Kaynak JSON ve cevap metni değişmedi. **Önceden başlamış v1 Reading oturumları eski seçenek sırasıyla açılır; yeni v2 oturumları yenileme sonrası aynı dengeli sırayla devam eder.**
2. **Writing sonuç sayacı:** 10 Build a Sentence görevine rağmen eski `/8` ifadesinin gösterildiği yer, yeni/önceki oturumlar için gerçek `buildSentenceTotal` alanından okunacak şekilde düzeltildi.
3. **Writing taslağından güvenli çıkış:** Süreli Writing sırasında **“Taslağı kaydet ve çık”** seçeneği eklendi. Aynı süre dolana kadar, taslak ve yanıtlar yerel kayıttan geri açılıyor. Bu işlem süreyi durdurmaz veya puan üretmez.
4. **PWA yenilemesi:** Service worker önbellek sürümü güncellendi, eski HTML/JS ile yeni kodun karışma olasılığı azaltıldı. Önbelleğin gerçekten hazır olduğu hâlâ gerçek Safari'de kontrol edilmeli.

## 3. Kaynak/kimlik ve müfredat bütünlüğü

- **TOEFL:** 400/400 kelime ID, 75/75 phrasal ID gerçek kaynak kartlarına eşleşiyor; boş/çift ID bulunmadı. Bu sayı resmî ETS kelime frekansı anlamına gelmez.
- **Reading:** 18 özgün alıştırma / 50 soru, 3 görev türü. Seçenekler ayrışıyor; yanıt indeksleri geçerli. Süre 30 dakika, fakat **AEL kaynaklı, adaptif veya ETS kalibre sınav değil**.
- **Writing:** 28 özgün görev havuzu; yeni süreli oturum 10 cümle + 1 e-posta + 1 akademik tartışma. 23 dakika. **Açık uçlu yazının dilsel doğruluğu ve TOEFL 1–6 puanı hesaplanmaz.**
- **Listening/VOA:** 30 uygulama içi transkript + 20 yayıncı bağlantılı ders, toplam 50 ders ve 204 soru. Bu dosyalara dokunulmadı. 0 doğrulanmış, yerel gerçek insan sesi MP3 mevcut.
- **Hafıza:** FSRS-5 altyapısı ve 1.550 odak kartı önceki hâliyle korundu. Zamanla kalıcılık için gerçek öğrenci verileri henüz yok.
- **Örnek cümle denetimi:** 1.784 genel + uzmanlık kelime girdisinin 232'sinde ikinci farklı örnek eksik. Bu sayı TOEFL 400/75 seçkisinde 232 eksik kart olduğu anlamına gelmez. Bağımsız editoryal son inceleme bekliyor.

## 4. Kullanım riski ve karar

| Öncelik | Risk | Karar |
|---|---|---|
| Kritik, kamuya yayın | Gerçek iPhone Safari / offline ve insana ait ses dosyası oynatma doğrulaması yok | Yayın **LOCKED** |
| Kritik, TOEFL puan tahmini | ETS kalibrasyonu ve adaptif psikometri yok | 1–6 puan **üretilmiyor** |
| Yüksek | Yerel `localStorage` Safari tarafından silinebilir | Her hafta JSON ilerleme yedeği alınmalı |
| Yüksek | Açık uçlu Writing'e otomatik dilsel puan verilemiyor | Öz değerlendirme ve ETS resmî örnekleriyle kıyaslanmalı |
| Orta | Bazı içeriklerde ikinci örnek ve bağımsız dil editörü incelemesi eksik | İçeriği taslak olarak kullan; doğrulanmış sertifika değil |
| Orta | 42 eSpeak MP3 robotik | Gerçek insan sesli Listening ile eşdeğer sayma |

**Kişisel pilot kararı:** Windows üzerinde yerel HTTP'den açıp Vocabulary, Hafıza Koçu, Reading, Grammar ve özgün TOEFL Reading/Writing çalışmalarına başlanabilir. İlk kullanımdan sonra otomatik kayıt yapıp JSON yedeği indir. Ses ve puanlama modüllerinin sınırlarını göz önünde tut. Bu karar **fiziksel iPhone Safari offline sertifikasyonu** değildir.

## 5. Kişisel kullanıma başlama — Windows

1. Bu özel geliştirme ZIP'ini bilgisayarında ayrı bir klasöre çıkart.
2. `american-english-lab` kökünde PowerShell veya terminal aç: `py -m http.server 8080` (Python `py` yoksa `python -m http.server 8080`).
3. Tarayıcıda **http://localhost:8080** aç. `index.html` dosyasını doğrudan `file://` şeklinde açma.
4. İlk kez Vocabulary/Hafıza Koçu ve TOEFL Reading'de kısa bir deneme yap; sayfadan çıkıp döndüğünde ilerleme görünüyorsa **Ayarlar → JSON yedekle** seçeneğini kullan.
5. Kişisel çalışma ilerlemesi cihazlar arasında otomatik senkronize olmaz; her hafta ayrıca JSON dışa aktar.

### iPhone / Safari için ek şart

ZIP dosyasını Safari'de açmak PWA kurulumu değildir. iPhone için güvenilir **HTTPS kaynak**, Safari'den **Ana Ekrana Ekle**, Ayarlar'da önbellek doğrulaması ve **uçak modunda gerçek cihaz testi** gerekiyor. Bu denetimde özel HTTPS barındırma veya yeni yayın sitesi **oluşturulmadı**. Doğrulanmadan Safari offline hazır denemez.

## 6. Tekrarlama komutları

```
npm test
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tools/preuse_quality_audit.py
python3 tools/audit_examples.py
python3 tools/audio_quality_gate.py
python3 tools/release_gate.py
python3 tests/final_use_browser_smoke.py
```

Son komut **yalnızca sanal Chromium ve sahte depolama** üzerinden çalışır. `release_gate.py` yayın kilidi nedeniyle **bilerek nonzero** döner.
