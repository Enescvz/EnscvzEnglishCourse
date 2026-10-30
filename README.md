> **30 Ekim 2026 — İLERLEME KURTARMA / OTOMATİK TASLAK KORUMASI / KALICILIK QA (PRIVATE):** Bozuk/kota dolu yerel depolama için kayıp koruması, ham kayıt kurtarma, Writing otomatik kayıt ve konservatif kalıcılık raporlaması eklendi. **134 JS + 200 Python = 334/334** otomatik test; Chromium masaüstü ve 390px mobil kurtarma senaryoları PASS. **Fiziksel iPhone, insan sesli kayıt/ses eşleşmesi, bağımsız editör ve 7/30 günlük gerçek kullanıcı ölçümleri hâlâ eksik.** Speaking değiştirilmedi, yayın kilidi açık. Rapor: `docs/20261030_INTEGRITY_AUTOSAVE_RETENTION_FINAL_PRIVATE_QA.md`.

> **30 Ekim 2026 — SON ÖZEL GELİŞTİRME / FLUENCY STUDIO 8 MODÜL:** Listening Master, Dictation Lab, Real-Life Simulator, Personal Error Coach, Writing Coach, Reading + Listening Bridge, English Thinking Trainer ve Adaptive Learning Path eklendi. 30 VOA transkript kaynağı/124 anlama sorusu/120 zaman kodsuz dikte adayı, 12 gerçek yaşam senaryosu/36 karar, 24 düşünme, 12 yazma görevi. **128 JS + 200 Python test geçiyor.** Ayrı masaüstü/mobil simülasyonlar PASS; birleşik tarayıcı kapanış testi aralıklı takılıyor. Gerçek iPhone Safari, uzak ses oynatımı/eşleştirme, editör ve 7/30 günlük kalıcılık QA eksik; **yayın KİLİTLİ**. Speaking kodu ve eski kartlar korunuyor. Ayrıntı: `docs/20261030_FLUENCY_STUDIO_8_MODULE_PRIVATE_QA.md`.

> **29 Ekim 2026 — ROBOTİK PODCASTLER KAPALI / ÖZEL QA:** Kullanıcı isteğiyle 18 robotik podcast + 24 robotik kısa ses alıştırmasının eSpeak MP3 dosyaları paketten çıkarıldı (42/42). Podcast ve kısa ses alıştırmalarında oynatma kapalı; eski transkript/soru/ID ve öğrenme kayıtları korundu. Günlük plan robotik ses önermez. Kullanıcı yalnızca gerçek insan sesli VOA kaynaklarına yönlendirilir. 0 yerel insan sesli MP3, fiziksel iPhone Safari oynatımı test edilmedi. Yayın kilidi korunuyor. `docs/20261029_ROBOTIC_PODCAST_REMOVAL_QA_PRIVATE.md`.

> **29 Ekim 2026 — Özel geliştirme / 500 günlük kalıp:** 300 eski kalıp korundu, 80 bağlaç/geçiş + 70 collocation + 50 cümle başlangıcı eklenerek **B1 150 + B2 210 + C1 140 = 500** taslak kalıba ulaşıldı. Günlük / TOEFL + Daily etiketleri FSRS tekrar kaydını bölmez. **Bağımsız editör onayı, doğrulanmış insan sesleri ve gerçek iPhone QA hâlâ eksiktir. Yayın kilitli.** `docs/20261029_DAILY_EXPRESSIONS_500_PRIVATE.md`.

> **29 Ekim 2026 özel geliştirme güncellemesi:** Günlük Kalıplar modülü **B1 100 + B2 120 + C1 80 = 300/300 özgün kalıp** içeriyor; iki örnek, kısa diyalog ve FSRS ile ayrı ilerleme kayıtları mevcut. **İnsan sesi, bağımsız editör onayı ve gerçek iPhone testi yoktur; yayın kilitli.** Detay: `docs/20261029_DAILY_EXPRESSIONS_300_PRIVATE.md`.

> **29 Ekim 2026 özel geliştirme:** Günlük Kalıplar modülü B1 100/100 eklendi; B2 0/120, C1 0/80. Örnek/diyalog + ayrı FSRS kayıtları. İnsan sesi ve bağımsız editoryal onay yok. Yayın hâlâ kilitli. Ayrıntılar: `docs/20261029_DAILY_EXPRESSIONS_B1_100_PRIVATE.md`.

## 29 Ekim 2026 — KİŞİSEL KULLANIM ÖNCESİ SON QA (PRIVATE / DO NOT DEPLOY)

97 JS + 180 Python = 277/277 otomatik test; 14/14 veri bütünlüğü kontrolü; 34/34 önbellek kaynağı HTTP erişilebilir. Reading yeni oturumlarında dengeli şıklar (13/13/12/12), eski v1 oturumları korunur. Writing sonuç paydası ve taslak kaydet/çık akışı düzeltildi. Sanal Chromium masaüstü/mobil PASS; gerçek Chromium localhost politikası tarafından engellendi, fiziksel iPhone Safari offline **TEST EDİLMEDİ**. Yayın **LOCKED**; Speaking ve Listening kodu değiştirilmedi. Ayrıntılar: `docs/20261029_PERSONAL_USE_FINAL_QA_PRIVATE.md`, `qa/final-personal-use-preflight-20261029.json`.

## 29 October 2026 — VOA Level 2 COMPLETE (transcript integration only, PRIVATE / DO NOT DEPLOY)

**30/50** full VOA lesson transcripts now in app (all Level 2 Lessons 1–30); **20** Level 1 lessons remain publisher-linked. All **204** original questions retain source evidence; **0** local human MP3 recordings, real iPhone playback and offline Safari remain NOT VERIFIED. Added Level 2 Lessons 25–30, online MP3 diagnostic UI, non-destructive ID preservation, and regression tests. **89 JS + 178 Python tests passed; virtual Chromium desktop/mobile targeted tests passed. Release LOCKED; Speaking untouched.** See `docs/20261029_VOA30_9OF10_ENGINEERING_PRIVATE.md`.

## 29 October 2026 — VOA publisher-script reuse (PRIVATE, DO NOT DEPLOY)

24/50 in-app publisher dialogue transcripts, 26 source-linked lessons, 204/204 source-grounded questions. VOA Level 2 Lessons 23 and 24 added with ID-preserving turns and online MP3 source links. Lesson 23 explicitly omits third-party song lyrics. Physical iPhone, offline audio and time-alignment remain unverified. All release gates remain locked. See `docs/20261029_VOA_PUBLIC_DOMAIN_TRANSCRIPT_REUSE_PRIVATE.md`.

## 29 October 2026 — Engineer hardening + VOA22 (PRIVATE; NOT READY FOR RELEASE)

**258/258 tests (87 JS +171 Python) passed.** Local backup import is non-destructive and conservatively preserves newer FSRS history; offline storage diagnostics added and worker cache bumped; public-domain VOA Level 2 Lesson 22 added as an in-app transcript with four speaker/turn evidence links. **22/50 VOA full transcripts, 28 publisher-linked; 204/204 text-source-evidenced questions.** Real iPhone Safari, genuine offline HTTP Chromium, MP3 playback/alignment, external editor and calibrated ETS scoring remain unverified. Release **LOCKED**. See `docs/20261029_ENGINEERING_HARDENING_PRIVATE.md` and `qa/engineering-release-audit-20261029.json`. Speaking unchanged.

## 2026-10-29 — Hafıza bilimi denetimi (özel geliştirme, yayın kilitli)

PubMed + Cambridge + Anki/Duolingo karşılaştırması: `docs/20261029_MEMORY_SCIENCE_EVIDENCE_AND_AUDIT_PRIVATE.md`. FSRS zamanı gelmemiş kartlar zorla çalıştırılmıyor; TTS başarısı gerçek sesli Listening sayılmıyor; TTS yokluğu yazılı kelimeyi gereksiz düşürmüyor; bağımsız recall öncesi ipucu kaldırıldı. Hafıza Koçu 1.550 bağlamlı karta ve ortak 400 TOEFL kelimesi + 75 phrasal filtresine sahip. Eski kimlikler ve öğrenme geçmişi saklı; Speaking değişmedi. Kişiselleştirilmiş verim, gerçek iPhone, insan editörü ve lisans QA bekliyor. Yayın `LOCKED`.

> **LATEST TOEFL 475 CARD AUDIT — 29 OCT 2026 / PRIVATE:** 400 vocabulary + 75 phrasals ID-preserving AWL570/PHaVE150 source cross-check; 168 AWL direct headword matches (83 in sublists 1–3), 38 PHaVE top-150 phrasal matches; 12 meaning/example corrections. NOT an ETS frequency ranking; independent human editor signoff, full corpus frequency and release approval OPEN. See `docs/20261029_TOEFL_VOCAB_FREQUENCY_EDITORIAL_PRIVATE.md`. Speaking unchanged, release LOCKED.

> **LATEST PRIVATE CHECKPOINT — 29 October 2026 / TOEFL EXTENDED:** Reading 18 tasks / 50 original questions, 20 Writing tasks, timed 12-item/23-minute Writing draft rehearsal (non-ETS), 8 script-only Listening scenarios remain without audio, 400/75 shared card IDs unchanged; **240/240 automated tests**, virtual Chromium desktop/mobile targeted PASS, physical iPhone/offline/ETS calibration/editor signoff still OPEN; Speaking unchanged; release **LOCKED**. See `docs/20261029_TOEFL2026_EXTENDED_PRIVATE.md`.

> **CURRENT PRIVATE DEVELOPMENT CHECKPOINT — 2026-10-29:** 21/50 VOA complete in-app transcripts, 204/204 questions with text source proof; TOEFL 34-question/30-minute non-ETS diagnostic with resumable progress; locally observable Writing revision guidance; 400/75 shared cards unchanged; real iPhone/audio/offline and editor approval OPEN; release LOCKED. See `docs/20261029_COMPREHENSIVE_GAP_REDUCTION_PRIVATE.md`.

> **29 OCT 2026 — TOEFL 2026 integrated practice / PRIVATE, DO NOT DEPLOY.** 12 original Reading tasks/34 questions, 18 Writing tasks, 8 script-only Listening studies/14 questions without verified audio, 9-question timed Reading mini test (12 minutes, not official or adaptive), non-scoring Writing structural checklist, personal Reading recommendations based only on actual results. Speaking unchanged; 400/75 core, original card IDs, progress, 50 VOA sources/204 questions preserved. True human audio playback, physical Safari/offline verification and editorial signoff remain outstanding. Release **LOCKED**. See `docs/TOEFL_2026_INTEGRATED_PREP_20261029.md` and `qa/toefl-2026-integrated-prep-report.json`.

> **EN GÜNCEL ÖZEL GELİŞTİRME — 29 Ekim 2026 (VOA19 / TOEFL 2026):** 19/50 tam uygulama içi VOA Conversation transkripti, 31 yayıncı bağlantılı ders; 204/204 soru için metin dayanağı (79 konuşma repliği + 1 sahne yönergesi + 124 kısa yayıncı alıntısı). Yeni **6 özgün TOEFL tarzı Reading (14 soru)** ve **9 özgün Writing** görevi eklendi; resmî ETS soru/puanı değildir. **55 JavaScript + 158 Python = 213 otomatik test geçti.** Hedefli sanal Chromium masaüstü/mobil akışı geçti; gerçek HTTP offline testi ortam tarafından engellendi. Fiziksel iPhone Safari, gerçek ses oynatımı, ses/transkript eşleşmesi, bağımsız editör onayı tamamlanmadı. Speaking ve mevcut kart/öğrenme kimlikleri korunuyor; yayın **LOCKED**. Kaynak: `docs/VOA19_TOEFL2026_READING_WRITING_QA_20261029.md`. Aşağıdaki eski snapshot kayıtları tarihîdir.


> **Güncel özel geliştirme (2026-10-28):** VOA Level 1 ders 33–52 için 80 kaynak konuşma alıntısı eklendi. Böylece 204/204 soru **metin kanıtı** taşıyor: 76 uygulama içi replik indeksi + 128 dış kaynak alıntısı. Tam uygulama içi transkript hâlâ 18/50, 32 dış sayfa; ses ve gerçek iPhone/offline doğrulaması eksik. Bkz. `docs/VOA_L1_33_52_SOURCE_EVIDENCE_20261028.md`. Yayın KİLİTLİ; Speaking korunuyor.

> **SON ÖZEL GELİŞTİRME — 28 Ekim 2026, VOA 19–30:** 12 resmî VOA Level 2 kaynak sayfasından 48 özgün soruya konuşmacı veya açıkça etiketlenmiş sahne yönergesi + kısa yayıncı alıntısı bağlantısı eklendi. **18/50** tam transkript (değişmedi), **32** kaynak bağlantılı soru seti, **76** transkript-replik kanıtı + **48** yayıncı-sayfası kısa alıntı kanıtı = **124/204** kaynak dayanaklı soru; **80** soru bekliyor. **51 JS + 141 Python** test başarılı, sanal Chromium desktop/mobile bağlantılı quiz kontrolü geçti (gerçek Safari veya MP3 testi değil). 0 yerel insan MP3. Üçüncü taraf şarkı sözleri dahil edilmedi. TOEFL 400/75, Speaking ve ders/kart ID'leri korundu. Yayın **LOCKED**. Ayrıntı: `docs/VOA_L2_19_30_SOURCE_EVIDENCE_20261028.md`. Eski girişler tarihî kayıttır.

> **EN GÜNCEL ÖZEL GELİŞTİRME (28 Ekim 2026 — VOA18 / TOEFL 400+75):** VOA Level 2 ders 15–18 resmî konuşma metni ve 16 yeni replik kanıtı eklendi. **18/50** uygulama içi transkript, **32** kaynak bağlantılı ders, **76/204** kanıtlı soru. 400 TOEFL kelimesi / 75 phrasal ID korundu. Gerçek Safari, çevrimiçi MP3 oynatımı, insan editör ve çevrimdışı QA yapılmadı; sanal Chromium bu turda zaman aşımına uğradı. Yayın **LOCKED**. Speaking değişmedi. Güncel rapor: `docs/VOA_18_REVIEWED_TRANSCRIPTS_20261028.md`, `qa/voa-source-coverage.json`. Aşağıdaki eski sayıların tümü tarihî kayıt.

> **EN GÜNCEL ÖZEL GELİŞTİRME (28 Ekim 2026 — VOA14):** Level 2 Lesson 13/14 yayıncı konuşmaları ve sekiz sorunun konuşmacı/replik kanıtı eklendi. **14/50** uygulama içi VOA transkripti; **36** kaynak bağlantılı ders; **60/204** replik kanıtlı soru. TOEFL + Daily **400 kelime/75 phrasal** korunuyor. **51 JS + 130 Python test geçti.** Gerçek iPhone/WebKit, çevrimiçi MP3 oynatımı ve offline Chromium testi tamamlanmadı (localhost ortam engeli). Speaking değişmedi, yayın **KİLİTLİ**. Bkz. `docs/VOA_14_REVIEWED_TRANSCRIPTS_20261028.md`.

> **GÜNCEL (28 Ekim 2026) TOEFL + Daily genişletmesi:** **400 kelime + 75 phrasal verb** ortak havuzu. Önceki 200/50 kart sırası ve ID'leri korunmuş; 200 mevcut genel kelime ve 25 mevcut phrasal eklenmiştir. 50 yeni akademik kelime taslağı korunur (toplam 50); kaynak ve anlam onayı tamamlanmadı. Sınavda frekans sıralaması değildir. Speaking değiştirilmedi; özel geliştirme, yayın KİLİTLİ. `docs/TOEFL_DAILY_400_75_SPRINT_20261028.md` detayları.

> **En güncel TOEFL + Daily ek paketi (28 Ekim 2026):** 200 ortak kelime + 50 mevcut phrasal verb; 50 yeni AWL1 akademik kelime kartı, 150 mevcut kelime kartı yeniden kullanılır. Günde 10 kelime + 3 phrasal başlangıç rutini. Bu ETS sıklık sıralaması değildir; editoryal QA sürüyor. Speaking ve 1.000/500 odak kart ID’leri korunmuştur. Testler: 50 Node + 125 Python geçmiştir; sanal Chromium masaüstü/mobil PASS verdi ancak runner temiz kapanış kanıtı yok. Yayın KİLİTLİ. Bkz. `docs/TOEFL_DAILY_CORE_SPRINT_20261028.md`.

> **EN GÜNCEL DOĞRULANMIŞ GELİŞTİRME (28 Ekim 2026, VOA12):** 50 resmi VOA dersi ve 204 özgün soru korunmuştur. **12** derste yayıncı Conversation konuşma replikleri uygulama içinde, **38** derste yayıncı sayfası bağlantısı bulunur; tam metinli derslerin **52/52 sorusu** konuşmacı + replik indeksli kaynağa bağlanmıştır. Son eklenen Level 2 Lessons 11 ve 12; doğrudan MP3 URL'leri kaynakta bulunur fakat gerçek oynatım ve ses-transkript eşleşmesi doğrulanmamıştır. 0 yerel gerçek insan MP3; 42 eski eSpeak dosyası onaysız. Speaking değiştirilmedi, yayın kilitli. Ayrıntı: `docs/VOA_12_REVIEWED_TRANSCRIPTS_20261028.md`.

> **Son doğrulanmış geliştirme (28 Ekim 2026):** VOA kaynak sayısı 50, özgün soru 204; **10** dersin yayımlanmış konuşma metni uygulama içinde (40'ı yalnızca VOA sayfasında), transkriptli derslerde **44/44** soru konuşmacı ve replik kanıtına bağlandı. Lesson 8 için doğrulanmış doğrudan MP3 olmadığı için oynatıcı sunulmaz. Sanal Chromium testleri gerçek iPhone Safari testi yerine geçmez. Listening doğal ses ve editoryal QA / gerçek cihaz testleri tamamlanmadı. Speaking değiştirilmedi; yayın kilitli. Bkz. `docs/VOA_10_REVIEWED_TRANSCRIPTS_20261028.md`.

> **CURRENT VERIFIED DEVELOPMENT STATE — 28 Oct 2026 (newer than historical entries below):** 50 VOA Listening sources with 204 original questions; **7** full in-app publisher transcripts and **43** publisher-linked transcript/audio lessons. 12 questions now cite exact transcript turns. Both quiz flows require listening self-report (NOT verified playback). Reading 30 / 150 questions; Grammar 20; general vocab 1,000 and phrasals 500 draft lessons; audio playback on physical iPhone NOT tested; bundled human MP3 0; release LOCKED. **49 JS + 113 Python tests** passed, virtual Chromium desktop/mobile targeted QA passed. Speaking out of scope. See `docs/VOA_7_REVIEWED_TRANSCRIPTS_20261028.md` and `qa/non-speaking-quality-report.json`. Older counts below are historical.

## 28.10.2026 — En güncel çalışma durumu (Speaking hariç)

**4 tam uygulama içi VOA transkripti + 46 yayıncı bağlantılı sorulu ders, 204 soru; 30 Reading (150 soru) ve 20 Grammar.** Reading/Grammar doğru cevap konumları dengelendi. Source-linked quiz için dinleme self-report kontrolü eklendi. Gerçek sesli MP3 sıfır, ses senkronizasyonu ve Safari QA tamamlanmadı. Yayın KİLİTLİ. Ayrıntı: `docs/NON_SPEAKING_QUALITY_SPRINT_20261028.md` ve `qa/non-speaking-quality-report.json`.

# CURRENT DEVELOPMENT STATE — 28 OCT 2026 (1,000 GENERAL CONTEXT DRAFTS)

**PRIVATE DEVELOPMENT ONLY — DO NOT PUBLISH, UPLOAD TO GITHUB, OR ENABLE PAGES.**

- **500 B2 + 500 C1** general lessons have an English definition, Turkish gloss and two independent contextual example sentences (**1,000 context drafts**). **500 phrasal-verb context drafts** are also present.
- **284** additional accounting/finance terms; **401** non-focus rapid gloss cards.
- **18** podcasts, **24** listening drills, **8** readings, **10** grammar lessons, **42** synthetic MP3 files, **0** licensed human-voice recordings.
- All focused lessons are **unreviewed drafts**. Source B2/C1 candidate labels do not establish verified advanced senses. **The shortlist has not been proven to be the 1,000 most frequently useful words in spoken US English**; low-priority items are listed in `qa/daily-use-selection-review-20261028.json`.
- Last run: **118/118 automated tests (46 JS + 72 Python)**. Actual iPhone/WebKit E2E not confirmed. **Release gate remains LOCKED**.
- Primary source: `docs/GENERAL_1000_CONTEXT_SPRINT_20261028.md`; the older snapshots in the rest of this README are **historical and may show outdated counts and obsolete GitHub publishing instructions**. Do not follow any publishing instructions while release is locked.

---

# ACTIVE WORKING CHECKPOINT — 28 October 2026 (PHRASAL 500 MILESTONE)

**User-approved focus: 500 B2 + 500 C1 general words, plus 500 useful conversational phrasal verbs.** The latest real state is **422 focused contextual general drafts (of 1,000)** and **500 contextual phrasal drafts (of 500)**, each phrasal with two distinct examples, definition, translation and usage note. None is independently editor-approved or certified B2/C1 sense-level. **451 word targets remain gloss-only and 127 word targets remain headword-only**; the 852 separate rapid bilingual cards are not contextual lessons. Accounting/Finance extra is 284.

The last sprint authored 70 source-grounded phrasal drafts and fixed 33 older phrasal lessons with a single example. **46 JS + 58 Python tests passed**; real iPhone Safari test and human audio remain unverified. `npm run release:check` must remain **LOCKED**. No Google Drive, GitHub upload, deployment or publication package. See `docs/PHRASAL_500_SPRINT_20261028.md`.

**All tables below are historical snapshots and may use old 3,500/600 targets.**

---

**Legacy checkpoints, tables and production queues below refer to OLD 3,500/600 goal; do not use them as the current target.**

---

# American English Lab 🇺🇸

**B2–C1 Amerikan İngilizcesi · ücretsiz ve statik · iPhone + Windows**

Tek bir GitHub Pages deposunda çalışan, Listening + aktif kelime hatırlama odaklı kişisel İngilizce çalışma platformunun **GELİŞTİRME KOPYASI**. **Henüz yayınlama!** Tam içerik, lisanslı doğal kayıt ve cihaz QA koşulları tamamlanmadı.

## Geliştirme notu — GitHub Pages kurulumu yayına hazır olana kadar uygulanmayacak

1. Teslim edilen `.zip` dosyasını bilgisayarında **çıkar**. GitHub'a doğrudan ZIP dosyasını yüklemek uygulamayı yayımlamaz; **ZIP'in içindeki tüm dosyaları** repo köküne yüklemelisin.
2. GitHub'da örneğin `american-english-lab` adlı **public** repository oluştur. `index.html`, `styles.css`, `js`, `data`, `assets`, `sw.js` ve diğer dosyaları **kök dizine** yükle. `.github` klasörünü de yükleyebilirsin.
3. `Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: main → /(root) → Save` seç.
4. Açılan adres: `https://GITHUB_KULLANICI_ADIN.github.io/american-english-lab/` (repo adın farklıysa bağlantı da değişir). GitHub Pages'in yayımlama süresi değişebilir.

Kurulumda npm, ücretli API, veritabanı veya sunucu gerekmez. Projeyi ZIP'ten doğrudan `file://` olarak çalıştırmak içerik `fetch()` çağrılarını engelleyebilir; GitHub Pages veya yerel HTTP sunucusu kullan.

## Yerelde açma

```bash
cd american-english-lab
python3 -m http.server 8081
# http://localhost:8081
```

## İçerik durumu — güncel çalışma ağacı

| Koleksiyon | Bu ZIP'teki gerçek içerik | Uzun vadeli müfredat hedefi |
|---|---:|---:|
| Genel B2–C1 vocabulary | **422** bağlamlı taslak + **852** farklı hızlı kart | 500 B2 + 500 C1 |
| Accounting & Finance vocabulary | **284** ayrı terim | en az 200 (karşılandı) |
| Phrasal verbs | **318** bağlamlı taslak | 500 |
| Özgün çift sesli podcast | **18** adet MP3 + transcript + ikişer soru | sürekli büyüyecek |
| Odaklı listening laboratuvarı | **24** adet MP3 + dictation | sürekli büyüyecek |
| Reading | **8** özgün pasaj, her birinde 5 soru | sürekli büyüyecek |
| Grammar | **10** karşılaştırmalı örnek ve soru | genişletilecek |
| 25 soruluk deneme bankası | Dinamik B2/C1 kelime ve phrasal anlam soruları; cevap sırası karışık | çeşitlenecek |

**Dürüst kapsam:** 1.000 genel kelime ve 500 phrasal verb bu geliştirme kopyasında **tamamlanmış değildir**. Sayı dolsun diye üretilmiş tekrarlar veya sahte içerikler gösterilmez. Phrasal verbs için ilk sürümde çoğunlukla bir anlam kullanılır; bazı çok anlamlı fiiller ek anlamlarıyla açıklanmıştır. Finans terimlerinin English definition, Türkçe gloss ve bağlamsal cümleleri bulunsa da her kart bağımsız bir sözlük uzmanı tarafından son kontrolden geçirilmiş değildir.

## 12 eğitim modülü

Listening Academy, Vocabulary Memory, Phrasal Verb Mastery, Podcasts, Reading, Grammar, Speaking, Writing, Daily Conversations, Pronunciation, Practice Tests, Smart Review. Bunlara ek Dashboard, Analytics ve Settings ekranları vardır.

**Listening**: özel ses dosyaları, hız seçimi, bölüm aralıkları, A/B tekrarı, konuşmacı zamanlarıyla etkileşimli transcript, transcript gizleme, kısa parçaları yazma, sözcük bazında doğruluk ve geçmiş grafiği. Sözcük eşleşme skoru, konuşmayı tamamen anladığını veya CEFR seviyeni göstermez.

**Vocabulary**: tanışma, çoktan seçmeli tanıma, bağımsız yazma, dinleyip yazma, örnek cümle bağlamında seçme, öz değerlendirmeli özgün cümle üretimi. Üretim otomatik gramer değerlendirmesi yapmaz. “Pekişmiş” durumu için üretim ve dinleme görevi başarı geçmişi de gerekir.

**Smart Review**: açık biçimde tanımlı, test edilmiş adaptif tekrar aralıkları; **FSRS-5 varsayılan parametreleri** kullanır (hedef hatırlama %90, kullanıcı bazlı parametre optimizasyonu yoktur). Yanlış yanıt sonrası yaklaşık 15 dakikalık öğrenme adımı vardır. Mevcut eski tekrar verileri, ilk yeni değerlendirmede korunarak FSRS durumuna geçirilir.

**Tests**: 25 soruluk denemede 10 genel vocabulary + 7 finans terimi + 8 phrasal verb; cevaplar sınav sonuna kadar gösterilmez. Önce görülmemiş soru kimlikleri tercih edilir, sonrasında tekrar mümkündür.

**Daily Plan**: 15/30/60 dakika; dinleme doğruluğu düşükse listening ağırlığı yükselir. Başlangıç bütünü 60 dakikadır.

**Progress**: `localStorage` ile yerel saklama; JSON yedek alma / geri yükleme; manuel cihazlar arası taşıma, **otomatik senkronizasyon yok**.

## Ses kaydı gerçekliği

- **42 adet MP3** geliştirme kopyasında (`assets/audio/`) bulunmaktadır ve doğrudan oynatılabilir. Bunlar yerel `eSpeak` sentezinden üretilmiş **yapay/robotik Amerikan İngilizcesi sesleridir; insan kaydı değildir**. Podcast Maya ve Alex rollerinin sentez sesi farklılaştırılmıştır.
- Anlık kelime ve Reading seslendirmesi cihazda yüklü bir **en-US SpeechSynthesis** sesine bağlıdır. en-US sesi yoksa kullanıcıya hata mesajı gösterilir. Başka aksana sessizce geçilmez.
- Gerçek konuşmacı içeriği için Podcasts bölümünde **VOA Learning English podcastleri** bağlantısı bulunur. **Harici bağlantıdır**; MP3'ler kopyalanmaz, transcript ile eşlenmez ve çalışırlığı uygulama tarafından garanti edilmez.
- TTS sesleri doğal konuşmadaki vurgu/indirgemeleri eksiksiz yansıtmaz; özellikle connected speech için gerçek insan kayıtlarıyla destekleyici çalışma önerilir.
- Service worker içerik ve MP3'leri arka planda önbelleğe almaya çalışır; tarayıcı kota sınırlamaları nedeniyle tamamen çevrimdışı kullanım garanti değildir.

## Gizlilik ve tarayıcı desteği

- Kayıtlar cihazda tutulur. Kullanıcı harici kaynak bağlantılarına tıklamadıkça uygulama kendi başına üçüncü taraf servislere veri göndermek için kod içermez.
- **Speaking** modunda Web Speech Recognition isteğe bağlıdır ve açılmadan önce uyarı gösterilir: bazı tarayıcılar konuşma sesini sunucu tarafında işleyebilir.
- iPhone Safari seslendirme / ses tanıma yetenekleri cihazın işletim sistemine bağlıdır. Mikrofon bulunmazsa manuel yazma alanı kullanılır. PWA kurulum desteği modele ve sürüme göre değişebilir.
- Writing için yapay zekâ notlandırması, gerçek zamanlı konuşma telaffuz notu veya resmî CEFR seviye sertifikası **yoktur**.

## Geliştirici testleri

```bash
npm test
```

Çalışan Node.js testleri içerik yapısını, ses ve transcript zamanlarını, 25 soruluk anahtarları, tekrar algoritmasını ve 12 modülün HTML ekran üretimini denetler.

Playwright otomasyon betiği `tests/e2e_playwright.py` altında hazırdır. Çalıştırmak için:

```bash
python -m pip install playwright
python -m playwright install chromium
python -m http.server 8973
# başka terminalde
python tests/e2e_playwright.py
```

**Önemli:** Teslimin üretildiği araç ortamında yönetilen Chromium, URL'leri `ERR_BLOCKED_BY_ADMINISTRATOR` ile engelledi; Playwright testi bu nedenle **başarıyla çalıştırılamadı**. Kodun gerçek iPhone Safari üzerinde test edildiği iddia edilmemektedir. CI'da yalnızca Node.js içerik/engine testleri çalışır.

## Öğrenme ve içerik referansları

Bu kaynakların içerik ve sesleri topluca kopyalanmadı; model ve beceri standartları için referans olarak kullanıldı:

- [CEFR descriptors — Council of Europe](https://www.coe.int/en/web/common-european-framework-reference-languages/cefr-descriptors)
- [Oxford 3000 and 5000 methodology](https://www.oxfordlearnersdictionaries.com/about/wordlists/oxford3000-5000)
- [Cambridge Dictionary](https://dictionary.cambridge.org/us/)
- [Merriam-Webster](https://www.merriam-webster.com/)
- [VOA Learning English podcasts](https://learningenglish.voanews.com/podcasts)
- [LibriVox — public domain notes](https://librivox.org/pages/public-domain/) — ses hakları ülkeye göre değişebilir
- [FSRS-5 algoritma referansı](https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm) — bu projede FSRS-5 varsayılan ağırlıklarıyla uygulanır; kişiselleştirilmiş optimizasyon yapılmaz

**Lisans:** Uygulama kaynak kodu MIT lisansıyla yayımlanır. Özgün ders metinleri, örnekler ve transkriptler CC BY 4.0 koşullarıyla sunulur. Sesler eSpeak ile üretilen sentetik dosyalardır; orijinal insan kayıtlarının kopyaları değildir. Harici kaynakların ayrı kullanım koşulları geçerlidir.

## Sürümün gerçek sınırlamaları

Phrasal verb çok-anlamlı kartlarını, B2–C1 kapsamının tamamını, insan sesli lisanslı parçaları, bağımsız seviye ölçümünü, shadowing puanlamasını ve Reading Türkçe çevirilerini sonraki içerik/özellik geliştirmelerine bırakır. Mevcut ilk sürüm öğrenilebilir bir prototip olarak kullanılabilir ama **C1 seviyesine tek başına garantili hazırlık sağlamaz**.

## Release kilidi

`npm run release:check` komutu eksik hedefleri listeler ve yayın şartlarının tamamı sağlanmadan hata koduyla durur. İçeriklerin editoryal denetimi ve iPhone WebKit/Windows Chromium E2E sonuçları sunulmadan yayınlanma onayı üretmez.

**İstisna yok:** Dosyaların mevcut olması, yayınlanabilecekleri anlamına gelmez. Bu depo yerel geliştirme amacıyla tutuluyor ve GitHub Pages'e henüz yüklenmemelidir.

## Bu geliştirme turunda

- 67 özgün genel İngilizce kartı eklendi; toplam 281 genel ve 284 finans/muhasebe kartı.
- Phrasal verbs 81'den 139'a çıkarıldı; 157 ayrı anlam kullanımını kapsıyor. Bütün İngilizce tanımlar özgün editoryal taslak; bağımsız Cambridge/Oxford seviyelendirme denetimi yapılmış değil.
- Deneme soruları çok anlamlı kalıpları farklı bağlamlarda soruyor. Deneme sonrası her şık için açıklama sunuluyor.
- Dictation değerlendirmesi kelime sırasını hesaba katıyor; önceki kelime hatırlama başarısıyla kaçırılan kelimeleri ilişkilendiriyor, neden hakkında tanı koymuyor.
- Akıllı tekrar, bağlam + dinleme + bağımsız hatırlama + üretim ölçütlerini birlikte arıyor. Yanlışlardan sonra eski başarıların ustalık sayımını temizliyor.
- Ana ekran, due-first günlük kelime ve dinleme görevleri öneriyor.
- `npm test` ile 16 otomatik kontrol geçti; `npm run qa:audio` gerçek MP3 sürelerini kontrol eder.
- E2E tarayıcı geçişleri bu çalışma ortamında Chromium URL bloklama politikasına takıldı. Windows/iphone gerçek QA raporları yok.

**Not:** Geliştirme kodunun varlığı; eksik içeriklerin, lisans incelemesinin ya da ileri seviye öğretim QA'sının tamamlandığı anlamına gelmez.

## Development update — multiple context sentences and sentence dictation

This repository is **still development-only and not approved for publication**.

- Existing cards now carry an `examples` array whose first element matches `example` (the original question-bank field). This is backward-compatible with existing local progress.
- Original, contextualized example sentences replaced the repetitive samples for all **284** accounting/finance entries.
- Of **704** vocabulary/phrasal entries, **107** now have at least two distinct contextual examples. The remaining **597** are still in an editorial queue; this is a blocker for publication.
- Examples render with optional browser **en-US TTS**; sentence dictation hides its answer until submission and calculates order-aware word accuracy. This is speech synthesis, **not** a human voice recording or a verified proficiency test.
- `python3 tools/context_examples.py` reapplies curated data idempotently. `npm run qa:examples` writes `qa/example_audit.json` with a transparent remaining-work list.
- The browser Playwright suite continues to be blocked from local navigation in this container (`ERR_BLOCKED_BY_ADMINISTRATOR`); passing Node tests do not replace desktop/WebKit end-to-end testing.
- **Do not package a release or publish to GitHub Pages** until `npm run release:check` exits successfully and manual expert sign-off is recorded truthfully.

## Toplu içerik üretim sistemi (geliştirme)

`tools/bulk_curriculum.py`, büyük B2/C1 kelime ve phrasal verb kaynaklarının yinelenmeyen **aday kayıtlarını** topluca işler. Kaynağı ve lisansı kaydeder; NGSL 1.2 sıklık sırasını ve Amerikan yazım filtrelerini uygular, phrasal verb anlamlarını ayrı tutar ve çelişkileri doğrulama kuyruğuna ayırır. Yapay zekâ tarafından üretilen sözlük tanımlarını otomatik olarak insan tarafından doğrulanmış kabul etmez.

Kullanımı ve veri kaynağı sınırları: [`docs/BULK_IMPORT.md`](docs/BULK_IMPORT.md). Komut: `python3 tools/bulk_curriculum.py --download --allow-network`. Hızlı alternatif: `npm run curriculum:bulk-fast` (resmi CEFR-J B2 / Octanove C1 ve açık lisanslı phrasal aday listeleri, staging-only). Geliştirme için B2/C1 ve phrasal headword kaynakları **artık yerel `sources/` klasöründe mevcuttur**, ancak bunlar aktif öğrenme kartı değildir. Veri lisansları ve seviye güvenilirliği `docs/BULK_IMPORT.md` ve `docs/CURRICULUM_QUEUE.md` içinde ayrıca belirtilmiştir. Geliştirilen kodun fixture tabanlı corpus unit testleri `npm run test:corpus` ile çalışır.

Yayın için ilk kez oluşturulan bütün B2/C1 kartların kaynak, açıklama, örnek, anlam, seviye, ses ve en-US uygunluğu editoryal olarak doğrulanmalıdır; sayı dolduran adaylar öğrenilmiş müfredat değildir.


### Development batch notes (not a release)

Additional authoring tools: `python3 tools/curated_context_batch.py`, `python3 tools/expand_phrasals_v2.py`, `python3 tools/expand_listening.py`. Each is idempotent and preserves existing entries. The added lessons are authored examples, **not** certified native-speaker reviewed content. To check the restricted-sandbox browser flows, run `npm run qa:sandbox`; for genuine Playwright against the served app, run `python3 tests/e2e_playwright.py` with a working local HTTP server. The simulated harness cannot replace desktop/iPhone real-device E2E.


### Geliştirme checkpoint — 27 Ekim 2026 (YAYIN DEĞİL)

- B2/C1 kaynak CSV dosyaları yerelde mevcut ve 3.647 benzersiz **kelime başlığı adayı** olarak işlendi (3.530'u mevcut 281 genel ders kartından farklı).
- Üçüncü taraf açık kaynak phrasal veri havuzundan 1.204 benzersiz **başlık adayı** çıkarıldı; mevcut 199 phrasal kartından 123'ü örtüşüyor, 1.081 yenisi aday. B2/C1 etiketleri eksik; bunlar **henüz ders kartı değil**.
- `cmudict` üzerinden 3.466 kelimeye ve 1.201 phrasal ifadeye **sadece aday** ABD sesletim bilgisi eklendi.
- Yeni araçlar: `tools/import_offline_phrasals.py`, `tools/enrich_candidate_pronunciation.py`. Testler otomasyonla doğrulanır.
- Google Drive kullanılmadı; kullanıcı özellikle herhangi bir Google Drive izni istemememizi talep etti.
- `npm run curriculum:stage-local` çevrimdışı staging işlemlerini yeniden çalıştırır. **Üretim `data/*.json` ders sayıları değişmedi; yayın hâlâ kilitli.**


## Development checkpoint — FSRS-5 + full editorial production queues (NOT RELEASE)

- The old simple interval scheduler was replaced with an FSRS-5 implementation (19 published default weights; target retention 90%; conservative legacy record migration). See [`docs/FSRS.md`](docs/FSRS.md). It is not personalized FSRS optimization.
- `npm run curriculum:review-queues` now generates deterministic, unique **3,500-general-word** and **600-phrasal-verb** editorial queues, kept private in `sources/`. **3,219** and **401** respectively are *source-only* records with missing teaching semantics and must not be treated as ready cards. New phrasal candidate levels remain null.
- Current target split: B2 2,393; C1 1,107 candidate levels; initial goal of 1,500 C1 needs 393 more source-level candidates.
- Safe `tools/promote_content_batch.py` validates authored JSONL records and defaults to `dry-run`; `--apply` never overwrites existing cards and marks newcomers unreviewed. See [`docs/CURRICULUM_QUEUE.md`](docs/CURRICULUM_QUEUE.md).
- **28 Node + 43 Python = 71 automated checks pass**, virtual-origin Chromium desktop/mobile smoke passes. This is not real WebKit/iPhone release evidence. `release:check` remains nonzero.
- Current actual learner cards **unchanged**: 281 general + 284 accounting/finance + 199 phrasal verbs. Human voice: zero.


## Geliştirme checkpoint — kaynak havuzu ekranı (27 Ekim 2026)

- `npm run curriculum:build-browser-catalog`: 3.647 B2/C1 kelime adayı + 1.204 çok sözcüklü fiil adayı = **4.851 kaynak başlığını** yerel `data/candidate-catalog.json` dosyasına derler. Bu dosya `sources/` içindeki ham veri ile **aynı şey değildir**; anlamlar/telifli örnekler içermez.
- Sidebar'daki **Kaynak Havuzu** ekranı arama, B2/C1 filtresi, phrasal aday ayrımı, 30'luk sayfalama ve mevcut öğrenme kartına dönüş sağlar. Ana öğrenme, FSRS ve deneme kartlarına kaynak adayları **asla otomatik eklenmez**.
- Phrasal kaynak başlıklarının hiçbirine B2/C1 etiketi **uydurulmaz**; fiil+edat birleşimleri editoryal eleme bekler.
- `npm run qa:offline-manifest`: tüm podcast/drill MP3 yollarını `sw.js` içindeki çevrimdışı listeyle eşler. Önceden 24 olan liste artık **42 sesi** kapsar. Dinamik kaynak kataloğu ise ziyaret üzerine yüklenir, ilk bağlantıdan sonra fırsat buldukça önbelleğe alınır.
- Kontrol: **28 Node + 43 Python = 71** otomatik test ve sanal Chromium masaüstü/mobil tarayıcı akışları başarılıdır. **Gerçek iPhone WebKit testleri yapılmadı.**
- Aktif dersler yine **281 B2/C1 genel kelime + 284 finans/accounting + 199 phrasal**. Kaynak taraması bir müfredat onayı veya yayın yeterliliği sağlamaz.
- `npm run release:check` beklenen şekilde başarısızdır. **Google Drive / GitHub deploy kullanılmadı.**

## Toplu dönüşüm partisi — 27 Ekim 2026

- Bu geliştirme turundaki iki partide toplam 178 genel B2/C1 kartı ve 130 phrasal kartı eklendi; her biri özgün English definition, Türkçe anlam ve 2 ayrı bağlam içeriyor.
- Öğrenilebilir genel kartlar: 459; phrasal kartlar: 329. Dış editör onayı verilmedi (`authored_unreviewed`).
- Phrasal kaynaklar CEFR etiketi vermediğinden 73 yeni B2 sınıflandırması **editoryal tahmindir**, onaylı CEFR değil.
- 3.041 genel ve 271 phrasal daha hedef müfredat sırasına alınmıştır, ancak ders kartı değildir.
- Oluşturulan öğretim kayıtları `sources/authored-*-batch.jsonl` dosyalarında; köken ayrımı ve şema kontrolleri için `tools/promote_content_batch.py` kullanılır.
- `sources/` özel geliştirme verisidir; doğrudan GitHub Pages’e aktarılmaz.

## Rapid bilingual deck (separate from full lessons)

`data/rapid-vocabulary.json` is a local, source-attributed **gloss-only** deck.
It includes 905 unique B2/C1 entries not already present in the 979 complete-semantic-field
general lesson cards. Each rapid entry supports English–Turkish recall, en-US device
speech (when installed), B2/C1 and text filters, and locally persisted spaced
review. Rapid entries are deliberately **not** passed to the contextual quiz bank,
full SRS mastery, release counts, or skill certification.

To rebuild from the locally checked bilingual glossary:

```bash
npm run curriculum:rapid-import
```

To ingest downloaded public EnglishPractice `B2.json` and `C1.json` together
with local corrections, without hand-authoring items individually:

```bash
python3 tools/rapid_gloss_import.py --upstream-json /path/to/B2.json --upstream-json /path/to/C1.json
```

Direct downloads are not possible from this sandbox network. The importer uses
only local supplied files and never requests Google Drive or GitHub write access.
It cannot claim publisher or editorial approval. Source EnglishPractice code is
MIT licensed, but source vocabulary/translation rights must be reviewed before any
public redistribution. The other CEFR source list licenses are not replaced by
the software license. Full contextual lessons are maintained in `data/vocabulary.json`.


## 28 Ekim 2026 — Son doğrulanmış durum (Phrasal + Memory Studio)

- **Yeni nihai kullanıcı hedefi:** 500 B2 + 500 C1 bağlamlı kelime, 500 günlük kullanışlı phrasal verb. Bu değerler müfredat hedefleri, tamamlanmış ders sayısı değil.
- **422 bağlamlı genel kelime, 430 bağlamlı phrasal verb, 284 Accounting/Finance, 852 ek hızlı kart** mevcut. Yeni +112 phrasal `tools/author_useful_phrasals_20261028.py` aracılığıyla kaynaklı, özgün iki örnekli taslaklar halinde eklendi. `editorialStatus=authored_unreviewed`; B2 atamaları provisional. Geriye **70 phrasal** ve **578 general** bağlamlı taslak kalıyor.
- `js/memory.js` / `js/app.js` / `styles.css`: Hafıza Koçu artık erişilebilir görsel **5-adım merdivenine** sahip. FSRS-5 review engine değiştirilmedi.
- **100/100** otomatik test başarılı (46 JS + 54 Python), 42 sentez MP3 teknik kontrolü başarılı. Eski içerikte **447** eksik ikinci bağımsız örnek var.
- Sanal tarayıcı QA bu turda desktop PASS sonrası **timeout** verdi; mobil SUCCESS **iddia edilmemeli**. Gerçek iPhone Safari zaten henüz test edilmedi. Yayın kontrolü kırmızı (**LOCKED**), Google Drive ve GitHub kullanılmadı.
- Ayrıntı: `docs/PHRASAL_MEMORY_STUDIO_SPRINT_20261028.md`. Geçmiş bölümlerdeki eski 3.500 / 600 hedefleri yerine **yukarıdaki güncel 1000 / 500** hedef geçerlidir.


### 28 Ekim 2026 özel geliştirme durumu

**584** bağlamlı genel kelime, **500** bağlamlı phrasal verb, **284** finans terimi; 1.000 hedefli genel müfredatta **416 hızlı anlam kartı** bağlamlı derse yükseltilmeyi bekliyor. 111 otomatik test geçti, yayın kilidi kapalı. Detaylar: `docs/GENERAL_CONTEXT_SPRINT_20261028.md`.

### 28 Ekim 2026 — En yeni kelime geliştirme sprinti (önceki durumların yerine geçer)

- **762 / 1.000 bağlamlı genel kelime taslağı** (bu tur **+178**: 132 B2 + 46 C1), **238** hedef hızlı anlam kartı bağlama yükseltme bekliyor.
- **500 / 500 bağlamlı phrasal verb taslağı**, **284** finans/muhasebe terimi. **639** bağımsız hızlı anlam kartı, bunların 238'i seçili 1.000 kelime içinde.
- Yeni derslerin tümünde İngilizce tanım, Türkçe karşılık, iki farklı doğal bağlam örneği var. 178 örtüşen hızlı kart ayıklandı; geçmiş `localStorage` ve mevcut kart ID'leri değiştirilmedi.
- **115 / 115 otomatik test başarılı** (46 JavaScript, 69 Python); sanal tarayıcı iki görünümde PASS yazdı fakat runner kapanışta timeout verdi. Gerçek Safari test edilmedi.
- **Yayın kilitli**: uzman dil kontrolü, Listening/Reading/Grammar/Podcast kotaları, lisanslı insan sesleri ve Safari QA eksik. Kaynak CEFR etiketleri aday seviyelerdir.
- Ayrıntılar: `docs/DAILY_CONTEXT_762_SPRINT_20261028.md`.

### 28 Oct 2026 — Current quality-first curriculum (supersedes older status sections)

- **1,000 focus word context drafts, 500 focus phrasal context drafts**, **284 separate finance/accounting entries**. Drafts are *not* human-approved or corpus-frequency-verified.
- **91 general headwords replaced** in the focus deck (55 B2 + 36 C1); original cards and stable IDs archived in `data/archived-vocabulary.json`. 399 independent rapid cards remain after duplicate reconciliation.
- **13 foundational/high-utility phrasal verbs** are marked `placementCheckFirst` and editorially labeled B1 instead of unverified B2; 487 advanced-priority expressions remain. No independent CEFR-sense validation was performed.
- **125/125 automated tests passed** (46 JavaScript + 79 Python). The release remains **LOCKED**.
- Complete candid methodology and caveats: `docs/SPOKEN_QUALITY_CURATION_20261028.md`. Research-corpus verification is still required; **the 1,000 items are not established as the most frequent words in American speech**.


## Real human VOA listening pilot (online only)
Three VOA Learning English Level 2 episodes with publisher transcripts and 16 original comprehension questions now live under **Real Voices · VOA**. Unlike the 42 legacy synthetic local MP3s, these are linked to VOA human-spoken recordings, but the three remote MP3 files **are not bundled or verified for playback in this development container**. Source transcript timestamps are not verified. See `docs/VOA_AUTHENTIC_LISTENING_PILOT_20261028.md`. All source rights/attribution must remain intact. Release remains locked.


## Real Voices VOA — 50-source discovery (28 Oct 2026)

Verified 50 official VOA lesson pages (30 intermediate Level 2, 20 easier Level 1 warm-ups). Only 3 are fully integrated in-app with transcript + 16 original questions; the remaining 47 open the official publisher page and are not falsely presented as completed quizzes. No new MP3 bundled or remote playback/device QA confirmed. See `docs/VOA_50_SOURCE_EXPANSION_20261028.md` and `qa/voa-50-source-links.csv`. Release remains blocked.

## Real Voices — 20 sorulu Listening dersi (28 Oct 2026)

Önceki 50 resmî VOA kaynağının **20 tanesinde özgün soru seti** bulunuyor (toplam 84 soru). **3 ders** uygulama içi tam transkript + kaynak MP3 bağlantılı; **17 yeni ders** yalnızca orijinal VOA sayfasında dinlenip transkripti okunuyor, **4 özgün soru** uygulamada çözülüyor. **Kalan 30 sayfa** henüz soru hazırlanmamış kaynak. `data/voa-source-quizzes.json` ve `docs/VOA_20_QUIZ_EXPANSION_20261028.md` ayrıntıları içeriyor. Yeni yerel insan sesli MP3 yok, gerçek cihaz playback QA bekliyor. Bu bölüm, önceki 3/50 kaydını **günceller**.


## 28 October 2026 — VOA 50 quizzes (latest, supersedes 20-quiz status)

**All 50 publisher sources have an original question set:** 3 with imported application transcripts (16 questions) and 47 with publisher-external transcript/audio (188 questions), **204 comprehension questions total**. Newly authored questions were manually checked against publisher Conversation text. The 47 externally linked lessons do **not** bundle audio or transcripts; remote playback and listening completion cannot be technically verified. Such scores are marked `assessmentType: source-linked-comprehension` and `audioPlaybackVerified: false`. No claims of offline natural-human audio readiness. Release remains locked. See `docs/VOA_50_QUIZ_SPRINT_20261028.md`.


## 28 Oct 2026 — Latest verified non-Speaking quality sprint (supersedes earlier VOA status)

**50 source-linked/original-question VOA listening lessons, 204 questions: 4 in-app publisher transcripts and 46 publisher-linked external transcript/audio quizzes.** 30 original Reading texts and 20 Grammar lessons. 152 automated tests passed; virtual Chromium desktop/mobile targeted smoke passed, actual remote-audio/device WebKit not tested. **No licensed human audio bundled.** Old eSpeak remains distinctly synthetic. Release gate **LOCKED** (11/21 passing). See `docs/NON_SPEAKING_QUALITY_SPRINT_20261028.md`.


## 29 Oct 2026 — Safari offline development (PRIVATE, DO NOT DEPLOY)
Core files and complete JSON/candidate catalog are now explicitly precached; Settings includes verified download/repair and missing-file reporting. 71 JavaScript + 164 Python tests passed. Virtual Chromium settings UI desktop/mobile passed. Real local HTTP Chromium blocked by administrator; physical iPhone Safari and human-voice VOA offline audio NOT tested. Keep release LOCKED, preserve Speaking and existing card/progress IDs. See `docs/20261029_SAFARI_OFFLINE_PRIVATE.md` and `qa/safari-offline-qa-report.json`.

## October 30, 2026 private engineering checkpoint

This development snapshot includes a 7/30-day observational retention view, local Safari airplane-mode self-test, a two-human-rater TOEFL Writing review comparator (NOT ETS scoring), and a source-verifying VOA Lessons 33–42 import utility. All are private development features; independent iPhone, editor, and learner-trial validation is still pending. Full transcripts remain 30/50 until real source files are downloaded, reviewed and applied. See `docs/20261030_PERSONAL_USE_ENGINEERING_QA_PRIVATE.md`. **DO NOT DEPLOY.**


## 2026-10-30 · Sentence Skills private development update

Added 34 lessons / 340 original exercises in Question Builder (12), Preposition Lab (10), Connector Lab (8), Sentence Builder (4). Access from “Soru & Cümle Atölyesi” in the app. Includes tap-to-order, contextual cloze, scenario-based production, feedback, separate stable review IDs, backup merge, and offline cache. **No public release, no editor sign-off and no iPhone Safari validation**. Speaking unchanged; no synthetic audio introduced. See `docs/20261030_SENTENCE_SKILLS_IMPLEMENTATION_PRIVATE.md`.


## 2026-10-30 — Finalization Candidate (PRIVATE, DO NOT DEPLOY)

See `docs/20261030_FINALIZATION_RELEASE_CANDIDATE_PRIVATE.md`. Initial data requests are lazy; offline texts require explicit Settings > İçerikleri indir / doğrula, and real-human audio is online-only. No editorial sign-off or physical iPhone test is implied.
