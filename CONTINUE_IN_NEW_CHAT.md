> **30 Ekim 2026 — İLERLEME KURTARMA / OTOMATİK TASLAK KORUMASI / KALICILIK QA (PRIVATE):** Bozuk/kota dolu yerel depolama için kayıp koruması, ham kayıt kurtarma, Writing otomatik kayıt ve konservatif kalıcılık raporlaması eklendi. **134 JS + 200 Python = 334/334** otomatik test; Chromium masaüstü ve 390px mobil kurtarma senaryoları PASS. **Fiziksel iPhone, insan sesli kayıt/ses eşleşmesi, bağımsız editör ve 7/30 günlük gerçek kullanıcı ölçümleri hâlâ eksik.** Speaking değiştirilmedi, yayın kilidi açık. Rapor: `docs/20261030_INTEGRITY_AUTOSAVE_RETENTION_FINAL_PRIVATE_QA.md`.

> **30 Ekim 2026 — SON ÖZEL GELİŞTİRME / FLUENCY STUDIO 8 MODÜL:** Listening Master, Dictation Lab, Real-Life Simulator, Personal Error Coach, Writing Coach, Reading + Listening Bridge, English Thinking Trainer ve Adaptive Learning Path eklendi. 30 VOA transkript kaynağı/124 anlama sorusu/120 zaman kodsuz dikte adayı, 12 gerçek yaşam senaryosu/36 karar, 24 düşünme, 12 yazma görevi. **128 JS + 200 Python test geçiyor.** Ayrı masaüstü/mobil simülasyonlar PASS; birleşik tarayıcı kapanış testi aralıklı takılıyor. Gerçek iPhone Safari, uzak ses oynatımı/eşleştirme, editör ve 7/30 günlük kalıcılık QA eksik; **yayın KİLİTLİ**. Speaking kodu ve eski kartlar korunuyor. Ayrıntı: `docs/20261030_FLUENCY_STUDIO_8_MODULE_PRIVATE_QA.md`.

**EN GÜNCEL KARAR (2026-10-29):** Robotik podcast / eSpeak kısa dinleme MP3'leri paket ve arayüzden çıkarıldı (18 podcast, 24 drill, 42 MP3). Veri kimlikleri ve geçmiş saklandı. Yalnız uygun lisanslı gerçek insan sesleri ileride podcast olarak sunulabilir. Singing/Speaking dokunulmadı. Yayın LOCKED. Ayrıntı: `docs/20261029_ROBOTIC_PODCAST_REMOVAL_QA_PRIVATE.md`.

## 29 Ekim 2026 — Günlük Kalıplar 500/500 özel geliştirme (DO NOT DEPLOY)

- Kaynak: 300/300 yedeği; **B1 150, B2 210, C1 140 = 500 kalıp**.
- Yeni paket: 80 bağlaç/geçiş, 70 collocation, 50 konuşma başlangıcı; 400 yeni örnek cümle ve 200 kısa diyalog.
- Var olan **300 kartın sözlük nesneleri/ID’leri değişmedi**. Öğrenme geçmişi aynı `expressions` ve FSRS kimliğinde kalır; TOEFL etiketleri kopya kart oluşturmaz.
- Yeni arayüz: seviyeler ve **Daily English / TOEFL + Daily** filtreleri; bu etiket resmî TOEFL sıklık verisi değildir.
- `sources/daily-expressions-200-additions-20261029.tsv` + `tools/expand_daily_expressions_500_20261029.py` yeniden üretilebilir yazım kaynağıdır.
- Speaking, Listening, VOA, TOEFL soru setleri ve bütün eski kart kayıtları korunmalıdır. İzin olmadan Google Drive ve GitHub'a yükleme; yayın ZIP’i oluşturma.
- **Eksikler:** bağımsız insan editörü, insan sesi, fiziksel Safari/offline QA; yayın kapısı LOCKED.
- QA: `qa/daily-expressions-500-20261029.json` ve `docs/20261029_DAILY_EXPRESSIONS_500_PRIVATE.md`.

## 29 Ekim 2026 — Günlük Kalıplar 300/300 gelişim yedeği

B1 100 + B2 120 + C1 80 özgün kalıp, `data/daily-expressions.json`. Her biri iki özgün örnek ve bir mini diyalog içerir. Seviye filtresi Hafıza Koçu FSRS çalışmasını ilgili seviyede başlatır; kart ID ve kayıtları korunur. 200 yeni ifade editoryal taslaktır, doğrulanmış ses yoktur. Gerçek iPhone/Safari ve insan editörü onayı yok, yayın kilidi LOCKED. Ayrıntılar `docs/20261029_DAILY_EXPRESSIONS_300_PRIVATE.md`, `qa/daily-expressions-300-20261029.json`. Speaking, Listening, TOEFL ve eski kartlar değişmedi. GitHub’a yükleme yapılmadı; ZIP’i kullanıcı kendi yüklemek istiyor.

---

## GÜNCEL ÖZEL GELİŞTİRME — 29 EKİM 2026 — GÜNLÜK KALIPLAR B1/100

Son yedek: `AEL_PRIVATE_DEV_BACKUP_20261029_DAILY_EXPRESSIONS_B1_100_QA_DO_NOT_DEPLOY.zip`. Önce testleri çalıştır. `data/daily-expressions.json` içinde özgün 100 B1 kalıbı, her biri iki cümle ve A/B diyaloğu; B2 0/120, C1 0/80. `js/memory.js` üzerinden bağımsız `P.expressions` FSRS tekrar kaydı; `js/progress-safety.js` eski ilerlemeyi korur. Yeni menü: Günlük Kalıplar. Speaking, Listening, TOEFL seçkisi ve eski ID'ler korunmuştur. Sentetik ses gerçek insan sesi değildir. Editör, gerçek Safari/MP3 QA yok. Sadece özel yedek; yayın kilidi LOCKED. Ayrıntı: `docs/20261029_DAILY_EXPRESSIONS_B1_100_PRIVATE.md` ve `qa/daily-expressions-b1-100-20261029.json`.

---

## EN SON ÖZEL QA KONTROLÜ — 29 EKİM 2026

Kaynak ZIP: TOEFL_ONLY_WRITING1011_CLOZE. 97/97 JS, 180/180 Python; 14/14 yapısal kontrol, sanal Chromium masaüstü/mobil akışı geçti. Reading v2 cevap pozisyonları dengeli; v1 eski oturumlar korunuyor. Writing sayaç düzeltmesi ve “Taslağı kaydet ve çık” eklendi. 34 SW core dosyası yerel HTTP 200 yanıtladı. Fiziksel iPhone/gerçek offline hâlâ test edilmedi, ETS/insan editörü onayı yok, 42 robotik ses doğal dinleme onaysız, kalan 20 VOA transkripti dış kaynakta. Yayın LOCKED. Speaking / Listening içeriğine dokunulmadı. Ayrıntı: docs/20261029_PERSONAL_USE_FINAL_QA_PRIVATE.md.

## Latest: 29 October 2026 — VOA30 engineering private checkpoint

Use private development ZIP from this checkpoint. **Do not start over.** All **30 Level 2 VOA** lesson transcripts integrated in-app, last 6 are Lessons 25–30; 20 Level 1 sources still need full text import. All 50 lesson IDs/204 quizzes and TOEFL 400/75 unchanged; human MP3 locally bundled **0**; physical iPhone Safari, MP3 audible playback, WebKit offline QA, human editor signoff and ETS score calibration **not verified**. JS/Python 89+178 PASS and targeted virtual Chromium desktop/mobile PASS. Release **LOCKED**. Speaking unchanged, never touch. No Google Drive/GitHub/release ZIP. See `docs/20261029_VOA30_9OF10_ENGINEERING_PRIVATE.md` and `qa/voa30-9of10-gap-report.json`.

CURRENT PRIVATE CHECKPOINT — VOA PUBLIC-DOMAIN DIALOGUE IMPORT, 29 October 2026: 24/50 VOA in-app transcripts; 26 remaining publisher-linked; 204/204 questions source grounded (100 in-app turns, 104 publisher excerpts). New Level 2 Lessons 23 and 24 have direct official external audio URLs and full VOA-authored dialogue; Lesson 23 excludes third-party song lyrics explicitly. Real MP3 playback, offline and iPhone Safari remain unverified; no human MP3 bundled. New batch backlog: `qa/voa-remaining-transcript-backlog-20261029.json`. Speaking untouched; release LOCKED.

## 29 October 2026 — Engineer hardening + VOA22 (PRIVATE; NOT READY FOR RELEASE)

**258/258 tests (87 JS +171 Python) passed.** Local backup import is non-destructive and conservatively preserves newer FSRS history; offline storage diagnostics added and worker cache bumped; public-domain VOA Level 2 Lesson 22 added as an in-app transcript with four speaker/turn evidence links. **22/50 VOA full transcripts, 28 publisher-linked; 204/204 text-source-evidenced questions.** Real iPhone Safari, genuine offline HTTP Chromium, MP3 playback/alignment, external editor and calibrated ETS scoring remain unverified. Release **LOCKED**. See `docs/20261029_ENGINEERING_HARDENING_PRIVATE.md` and `qa/engineering-release-audit-20261029.json`. Speaking unchanged.

## 2026-10-29 — Hafıza bilimi denetimi (özel geliştirme, yayın kilitli)

PubMed + Cambridge + Anki/Duolingo karşılaştırması: `docs/20261029_MEMORY_SCIENCE_EVIDENCE_AND_AUDIT_PRIVATE.md`. FSRS zamanı gelmemiş kartlar zorla çalıştırılmıyor; TTS başarısı gerçek sesli Listening sayılmıyor; TTS yokluğu yazılı kelimeyi gereksiz düşürmüyor; bağımsız recall öncesi ipucu kaldırıldı. Hafıza Koçu 1.550 bağlamlı karta ve ortak 400 TOEFL kelimesi + 75 phrasal filtresine sahip. Eski kimlikler ve öğrenme geçmişi saklı; Speaking değişmedi. Kişiselleştirilmiş verim, gerçek iPhone, insan editörü ve lisans QA bekliyor. Yayın `LOCKED`.

> **LATEST CHECKPOINT — 29 OCT 2026 TOEFL EDITORIAL:** `docs/20261029_TOEFL_VOCAB_FREQUENCY_EDITORIAL_PRIVATE.md`, `qa/toefl-475-frequency-and-editorial-audit-20261029.json`; AWL all headwords 168/400 (83 in sublists 1–3) and PHaVE top150 38/75; 12 content fixes, all IDs/history intact. Independent editor and full exam corpus frequency NOT verified; release LOCKED; Speaking untouchable, no Google Drive/GitHub/publish. Run tests before continuing.

> **LATEST PRIVATE CHECKPOINT — 29 October 2026 / TOEFL EXTENDED:** Reading 18 tasks / 50 original questions, 20 Writing tasks, timed 12-item/23-minute Writing draft rehearsal (non-ETS), 8 script-only Listening scenarios remain without audio, 400/75 shared card IDs unchanged; **240/240 automated tests**, virtual Chromium desktop/mobile targeted PASS, physical iPhone/offline/ETS calibration/editor signoff still OPEN; Speaking unchanged; release **LOCKED**. See `docs/20261029_TOEFL2026_EXTENDED_PRIVATE.md`.

> **LATEST — 29 OCT 2026 · COMPREHENSIVE PRIVATE GAP REDUCTION / DO NOT DEPLOY.** Read `docs/20261029_COMPREHENSIVE_GAP_REDUCTION_PRIVATE.md` first. 21/50 VOA full in-app transcripts, 29 publisher-linked; all 204 source-anchored, 88 turn-level. Original 34Q/30min non-ETS Reading diagnostic, five questions/page, resumed active session; 9Q/12min mini preserved. Writing observable revision feedback; 475-item independent editorial queue (0 approvals). Offline service worker *simulation* passed, real localhost HTTP offline blocked, virtual Chromium desktop/mobile passed; actual iPhone/remote MP3 still untested. No Speaking edits, no Google Drive, no GitHub, NO release ZIP. Release LOCKED.

> **29 OCT 2026 — TOEFL 2026 integrated practice / PRIVATE, DO NOT DEPLOY.** 12 original Reading tasks/34 questions, 18 Writing tasks, 8 script-only Listening studies/14 questions without verified audio, 9-question timed Reading mini test (12 minutes, not official or adaptive), non-scoring Writing structural checklist, personal Reading recommendations based only on actual results. Speaking unchanged; 400/75 core, original card IDs, progress, 50 VOA sources/204 questions preserved. True human audio playback, physical Safari/offline verification and editorial signoff remain outstanding. Release **LOCKED**. See `docs/TOEFL_2026_INTEGRATED_PREP_20261029.md` and `qa/toefl-2026-integrated-prep-report.json`.

> **EN GÜNCEL ÖZEL GELİŞTİRME — 29 Ekim 2026 (VOA19 / TOEFL 2026):** 19/50 tam uygulama içi VOA Conversation transkripti, 31 yayıncı bağlantılı ders; 204/204 soru için metin dayanağı (79 konuşma repliği + 1 sahne yönergesi + 124 kısa yayıncı alıntısı). Yeni **6 özgün TOEFL tarzı Reading (14 soru)** ve **9 özgün Writing** görevi eklendi; resmî ETS soru/puanı değildir. **55 JavaScript + 158 Python = 213 otomatik test geçti.** Hedefli sanal Chromium masaüstü/mobil akışı geçti; gerçek HTTP offline testi ortam tarafından engellendi. Fiziksel iPhone Safari, gerçek ses oynatımı, ses/transkript eşleşmesi, bağımsız editör onayı tamamlanmadı. Speaking ve mevcut kart/öğrenme kimlikleri korunuyor; yayın **LOCKED**. Kaynak: `docs/VOA19_TOEFL2026_READING_WRITING_QA_20261029.md`. Aşağıdaki eski snapshot kayıtları tarihîdir.

# LATEST — 2026-10-28, VOA Level 1 33–52 source evidence sprint (PRIVATE ONLY)

Use this ZIP (not a blank project) and run `npm run test:all` first. Twenty official VOA Level 1 Conversation pages (33–52) were manually reviewed; 80 new short speaker/excerpt+page-line source proofs were added. **All 204/204 comprehension questions now have text source evidence** (76 complete transcript turn-index, 128 source-page linked excerpt), but **only 18/50 full in-app transcripts** and **32/50 external-only** remain. This is NOT audio playback, voice/time alignment or editorial signoff. Source proof data: `qa/source-reviews/voa-l1-33-52-evidence-20261028.json`. Import script `tools/review_voa_l1_33_52_evidence_20261028.py` is idempotent. Full evidence audit `tools/audit_voa_completion_queue.py` now works correctly with 0 pending rows and emits header-only CSV. Lesson 42 preserves the ambiguous injury claim with visible contextual caveat; Level 1 Lesson 45 Woody Guthrie song lyrics excluded. Earlier stale 07–08 tests/importer adjusted to avoid overwriting newer full-transcript lessons. QA doc `docs/VOA_L1_33_52_SOURCE_EVIDENCE_20261028.md`. Physical iPhone Safari/remote MP3, offline, pronunciation, independent editor, TOEFL Reading/Writing pending. Existing 50 lesson IDs, 204 quiz question+answer identities, TOEFL 400/75 and Speaking unmodified. The publish gate is still LOCKED. NEVER touch Speaking; do not use Google Drive/GitHub or produce publication ZIP. Private development backups ONLY.

---

# Latest handoff — 28 October 2026, VOA L2 19–30 batch (private, NOT FOR RELEASE)

Open this actual private backup; run `npm run test:all` first. Speaking MUST NOT be edited. Do not use Google Drive, GitHub or generate release archives.

12 new publisher **excerpt-evidence reviews** for VOA Level 2 lessons 19–30 (48 questions). These are still **external source-linked** lessons, NOT 12 complete in-app transcript imports. Count remains 18 complete transcripts + 32 linked pages. 76 existing transcript-turn proofs + 48 new publisher excerpt proofs = 124 source-supported quiz questions; 80 original question answers still need source evidence. 50 lesson IDs and 204 question texts/choices/answer indices retained; TOEFL shared core 400 words/75 phrasals retained. Three new proofs are source stage directions, NOT actual utterances. No commercial-song lyrics imported.

Repo artifacts: `tools/review_voa_publisher_questions_19_30.py`, `qa/source-reviews/voa-l2-19-30-evidence-20261028.json`, `qa/source-reviews/voa-l2-19-30-question-identity-baseline.json`, `tools/audit_voa_completion_queue.py`, `docs/VOA_L2_19_30_SOURCE_EVIDENCE_20261028.md`, `tests/test_reviewed_voa_19_30.py`.

Baseline prior to edits: 51 JavaScript, 136 Python passed. After: 51 JavaScript, 141 Python passed and virtual desktop/mobile Chromium linked-quiz QA passed. Other existing browser/audio/offline/physical iPhone tests are not thereby certified. Publish gate remains LOCKED.

Next: verify remaining 20 Level 1 external-linked lessons / 80 question sources; import complete official transcripts only with source checks and third-party exclusions; independently test actual iPhone Safari and audio playback; complete editorial/frequency, TOEFL Reading/Writing and offline QA. No fake completion.

---

# EN GÜNCEL 28.10.2026 — VOA18 / TOEFL400+75 özel geliştirme

Devam başlangıcı: bu ZIP. Başlangıç testi `npm run test:all`. 18 resmi VOA konuşma transkripti entegre, 32 kaynak-bağlantılı, toplam 50 ders/204 soru, 76 replik kanıtlı, kalan 128 soru. Dosyalar: `docs/VOA_18_REVIEWED_TRANSCRIPTS_20261028.md`, `qa/voa-source-coverage.json`, `qa/voa-question-review-queue.csv`. 400 TOEFL kelime / 75 phrasal ortak havuz, 50 akademik taslak değişmedi. Bu tur dört resmî ders 15–18 ve 16 kanıt eklendi; `tools/import_reviewed_voa_15_18.py` yeniden çalıştırılabilir. Speaking ve kart ID/progress değişmedi. Gerçek iPhone Safari/MP3/offline, bağımsız editoryal kontroller yok. Chromium kapanışı zaman aşımına uğradı, başarı deme. 42 eski eSpeak hâlâ kalite onaysız. Release LOCKED; GitHub/Google Drive/deploy/yayın ZIP yok. Yalnızca özel geliştirme ZIP.

---

## LATEST 28 OCT 2026 — VOA14 / TOEFL 400+75 private development snapshot

Start from this backup, not a blank project. Read `README.md`, `development-status.json`, `docs/VOA_14_REVIEWED_TRANSCRIPTS_20261028.md` and `qa/non-speaking-quality-report.json`; run `npm run test:all` before edits. Integrated official publisher transcripts: **14**, linked-only: **36**; 60/204 turn-grounded questions, 144 linked-only questions remain. Listening completion self-report still required. TOEFL shared core 400 word IDs/75 phrasal IDs preserved. 51 JS + 130 Python tests pass. Virtual Chromium assertions passed but runner exit unverified; local HTTP Chromium offline blocked by environment. Real iPhone and VOAs MP3 playback not tested. Speaking and old progress IDs must not change; no Google Drive, GitHub or release ZIP; keep release LOCKED. Source reviewed 13–14; use `tools/import_reviewed_voa_13_14.py` idempotently.

---

> **GÜNCEL — TOEFL + DAILY 400/75:** `data/toefl-core.json` içinde 400 mevcut/yeni kelime ve 75 mevcut phrasal ID var. Önceki 200/50 ID'ler ilk sıralarda birebir korunur. Yeni 200 genel kelime ve 25 phrasal önceki AEL kartlarından referans edilmiştir; 50 akademik kart sayısı değişmez. `tools/curate_toefl_core_20261028.py` tekrar üretilebilir. `sources/toefl-curated-extension-20261028.txt`, `sources/toefl-phrasal-extension-20261028.txt` ve `sources/toefl-core-original-200-50-20261028.json` okunmalı. `docs/TOEFL_DAILY_400_75_SPRINT_20261028.md` + `qa/toefl-core-report.json`. Speaking'e kesinlikle dokunma; gerçek iPhone Safari, editoryal onay, TOEFL frekansı/çevrimdışı QA tamamlanmadı; yayın KİLİTLİ, Google Drive/GitHub yok.

> **LATEST / TOEFL + DAILY CORE 28 OCT 2026:** `data/toefl-academic.json` (50 new unreviewed academic lessons), `data/toefl-core.json` (200 existing/new word IDs + 50 existing phrasal IDs), `docs/TOEFL_DAILY_CORE_SPRINT_20261028.md` and `qa/toefl-core-report.json`. Use `python tools/curate_toefl_core_20261028.py` for idempotent rebuild. 50 JS + 125 Python passing. Speaking untouched. No official ETS ranking or human US editor approval. Physical Safari and offline/audio not verified; release LOCKED. No Google Drive/GitHub/deploy.

# ÖNCELİKLİ DEVAM NOKTASI — VOA12 / ÖZEL GELİŞTİRME

VOA10 yedeğinden devam edilerek Level 2 Lessons 11 ve 12 kaynak Conversation metninden aktarıldı ve 8 quiz sorusu konuşmacı/replik indeksiyle kanıtlandı. **12 tam transkript / 38 yayıncıya bağlı ders / 204 toplam soru / 52 replik kanıtı.** `tools/import_reviewed_voa_11_12.py` idempotent. Lesson 11 malzeme şıkkı yayımcı metniyle uyumlu hale getirildi. `docs/VOA_12_REVIEWED_TRANSCRIPTS_20261028.md` ve `qa/non-speaking-quality-report.json` üzerinden kontrol et.

**KATI KİLİTLER:** Speaking'e dokunma, Google Drive/GitHub/yayın yok, mevcut öğrenme kayıtları/kart ID'leri korunacak. 0 gerçek iPhone Safari doğrulaması; 0 yerel insan MP3. Virtual Chromium kontrolleri desktop/mobile geçti fakat test runner kapanışı zaman aşımına uğradı, temiz süreç çıkışı iddia edilmemeli. 38 transkript ve 152 soru replik bazında kaynak kontrolü bekliyor.

---

# GÜNCEL KAYIT — 28 Ekim 2026, VOA 10 QA

- 50 VOA resmi kaynak sayfası, toplam 204 özgün soru; **10** uygulama içi VOA Conversation transkripti, **40** kaynak sayfasında dinlenip soruları uygulamada çözülen ders. Transkriptli derslerin **44/44 sorusu** replik bazında kanıtlı, kalan 160 soru henüz bu seviyede kaynak doğrulaması bekliyor.
- Son üç ders: Level 2 Lesson 7, 8 ve 9; Lesson 8 için doğrudan MP3 URL'si **yok**, bunun yerine VOA yayıncı bağlantısı gösteriliyor. Lesson 7'nin yayımlanmış edat şarkısı kelime listesi ayrı eklendi, ses eşleşmesi doğrulanmadı.
- 49 JS + 118 Python testleri, sanal Chromium masaüstü/mobil QA geçti. **iPhone Safari veya gerçek MP3 oynatma testi yapılmadı**. 0 yerel insan MP3, 42 eski eSpeak (robotik, kalite onaysız).
- 1.000 genel kelime, 500 phrasal verb bağlamlı taslak; bağımsız editoryal onay yok. Reading 30 / 150 soru; Grammar 20. Speaking'e kesinlikle dokunma. Öğrenme kayıtlarını ve kart ID'lerini silme.
- Google Drive izni isteme veya kullanma. Uygulama bitmeden GitHub'a yükleme veya yayın paketi üretme. Yalnızca **özel geliştirme yedeği** yapabilirsin. Yayın kilitli.
- Devam: 40 kalan VOA transkriptini yayımlanmış kaynaktan kontrol ederek içeri al, 160 sorunun yanıtına kaynak repliği kanıtı ekle; ses linkleri, transkript doğruluğu, dil seçimi ve offline/iPhone QA.
- Tam ilerleme ve açık sınırlamalar: `docs/VOA_10_REVIEWED_TRANSCRIPTS_20261028.md`, `qa/non-speaking-quality-report.json`, `development-status.json`.

---

> **CURRENT VERIFIED DEVELOPMENT STATE — 28 Oct 2026 (newer than historical entries below):** 50 VOA Listening sources with 204 original questions; **7** full in-app publisher transcripts and **43** publisher-linked transcript/audio lessons. 12 questions now cite exact transcript turns. Both quiz flows require listening self-report (NOT verified playback). Reading 30 / 150 questions; Grammar 20; general vocab 1,000 and phrasals 500 draft lessons; audio playback on physical iPhone NOT tested; bundled human MP3 0; release LOCKED. **49 JS + 113 Python tests** passed, virtual Chromium desktop/mobile targeted QA passed. Speaking out of scope. See `docs/VOA_7_REVIEWED_TRANSCRIPTS_20261028.md` and `qa/non-speaking-quality-report.json`. Older counts below are historical.

## 28.10.2026 — En güncel çalışma durumu (Speaking hariç)

**4 tam uygulama içi VOA transkripti + 46 yayıncı bağlantılı sorulu ders, 204 soru; 30 Reading (150 soru) ve 20 Grammar.** Reading/Grammar doğru cevap konumları dengelendi. Source-linked quiz için dinleme self-report kontrolü eklendi. Gerçek sesli MP3 sıfır, ses senkronizasyonu ve Safari QA tamamlanmadı. Yayın KİLİTLİ. Ayrıntı: `docs/NON_SPEAKING_QUALITY_SPRINT_20261028.md` ve `qa/non-speaking-quality-report.json`.

# LATEST VERIFIED HANDOFF — 28 OCT 2026 — 1,000 / 500 CONTEXT DRAFTS

**Ignore older numerical status snapshots below.** This is the current on-disk checkpoint.

- User goal: speak and understand everyday **US English**, B1 to advanced; prioritize Listening/Speaking and strong memory retention. User explicitly changed target to **500 B2 + 500 C1 general words + 500 essential phrasal verbs**. Finance terms are separate, optional.
- **1,000 general (500 B2, 500 C1) context drafts and 500 phrasal context drafts** in `data/vocabulary.json` and `data/phrasals.json`, all with two distinct examples and a Turkish meaning, but **NONE editorially approved**.
- Additional **284** accounting/finance cards; **401** non-target quick bilingual cards. 232 finance terms still have one example.
- This sprint: imported **238** additional general context drafts (183 B2 + 55 C1) from `sources/authored-20261028-final-b2-part1.txt`, `sources/authored-20261028-final-b2-part2.txt`, `sources/authored-20261028-final-c1.txt`. Reproducible `tools/author_final_focus_words_20261028.py` checks provenance and is idempotent. Exact JSONL input: `sources/authored-20261028-final-focus-238.jsonl`.
- Validation: **46 Node + 72 Python = 118 tests passed**; release gate still intentionally exits 1, **LOCKED**. Never fake human editorial, independent CEFR validation, licensed human audio or real iPhone Safari QA.
- **IMPORTANT QUALITY PROBLEM:** This 1,000 shortlist is NOT verified US spoken-frequency-ranked; some rare, archaic or regional words were carried over from the B2/C1 source lists. Review `qa/daily-use-selection-review-20261028.json` and **replace weak focus targets with truly practical spoken-language alternatives** only after source/sense review. Do not wipe old lesson IDs or learner progress. No automatic mass “approved” flags.
- Still lacking 50 podcast / 60 drill / 30 reading / 20 grammar minimums, licensed human voices, natural connected-speech listening validation, live device browser QA, and finance second examples.
- `docs/GENERAL_1000_CONTEXT_SPRINT_20261028.md` is the latest detailed report. `development-status.json` is the status source of truth.
- Do not ask for Google Drive permissions or use Drive. Do not upload to GitHub, enable Pages, or distribute incomplete app as a release. Only encrypted/private-style explicitly marked development backups are allowed; current ZIP is not encrypted.

---

# **EN GÜNCEL DOĞRULANMIŞ DURUM — 28 Ekim 2026 (762 bağlamlı kelime)**

Bu bölüm önceki dosyadaki **584/416/817/111** gibi eski sayıları hükümsüz kılar.

- 500 B2 + 500 C1 müfredatında **762 bağlamlı ders taslağı**, **238 gloss-only** (0 headword-only). Bu tur **178 özgün yeni ders** (132 B2, 46 C1) eklendi.
- **500 bağlamlı phrasal**, **284 finans/muhasebe**, **639 bağımsız hızlı kart**.
- **115/115** otomatik test: 46 Node + 69 Python. Sanal Chromium desktop/mobile PASS yazdı, ancak runner kapanışta timeout; gerçek Safari doğrulanmadı.
- Genel derslerde iki farklı örnek tamam; finansta 232 eksik ikinci örnek.
- `docs/DAILY_CONTEXT_762_SPRINT_20261028.md`, `tools/author_daily_context_sprint_20261028.py`, `tools/reconcile_rapid_promotions.py`, `tests/test_daily_context_sprint_20261028.py` bu sprintin ana dosyaları.
- Hedef: Kalan 238 kelimeyi **günlük yarar filtresinden geçirerek** dönüştür; az kullanılan kelimeyi sayıya ulaşmak için içeri alma. Uzman dil, telaffuz ve gerçek iPhone QA kısıtları devam eder.
- GitHub, Pages, Google Drive kullanılmadı; yayın kilidi açık.

---

# American English Lab — Devam devir notu (28 Ekim 2026)

Bu dosya **özel, yayımlanamaz geliştirici projesine** aittir. Önceki sohbetlerde verilen varsayımsal sayılar yerine güncel `development-status.json` ve gerçek `data/*.json` dosyalarını esas al.

## Kilitlenmiş kullanıcı hedefi

- Kullanıcı B1; öncelik günlük **Amerikan İngilizcesi dinleme + akıcı konuşma**.
- **500 B2 + 500 C1 = 1.000** günlük işlevsel kelime ve **500 phrasal verb** hedefi. İş/meslek odaklı daraltma yapma; ayrıca isteğe bağlı finans modülü var.
- Doping Hafıza benzeri etkin ama kanıta dayalı **aktif hatırlama, kendi cümlesi, farklı bağlam, dinleme, FSRS-5 tekrar**.
- %100 ücretsiz, offline-capable iPhone Safari/Windows PWA.
- Eksik sürüm asla GitHub'a/Pages'e yüklenmeyecek veya yayın paketi olarak sunulmayacak. Özel geliştirme yedeği ayrı ve açık etiketli olabilir.
- Google Drive kullanma ve izin isteme.

## Son gerçek durum

- Genel **584** iki örnekli bağlamlı ders (eski 422'ye 145+17 ilave), **500** iki örnekli phrasal verb, **284** finans/accounting, **817** genel hızlı anlam kartı (odak müfredatında 416). 1.000'lik focus hedefinde kalan yalnızca **416 gloss-only** kelime; **0 headword-only**.
- Genel kategoride **0** tek örnekli ders; finans/accounting'de **232** tek örnekli ders var.
- 18 podcast, 24 dinleme alıştırması, 8 okuma, 10 gramer, 42 sentetik MP3, 0 lisanslı gerçek insan kaydı.
- **111/111 test** (46 Node + 65 Python) geçti. Sanal Chromium E2E ekranlarında PASS desktop ve PASS mobile çıktısı var, ancak runner kapanışta timeout; gerçek iPhone Safari henüz doğrulanmadı.
- `python tools/release_gate.py` beklenen şekilde nonzero ve **LOCKED**. `development-status.json` güncel.

## En son geliştirilen dosyalar

- `tools/complete_general_second_examples_20261028.py`: 182 bağımsız ikinci bağlam cümlesi, idempotent.
- `tools/author_fluency_general_20261028.py`: 145 yeni bağlamlı kelime; idempotent, kaynak doğrulamalı.
- `tools/author_remaining_focus_headwords_20261028.py`: 17 C1 başlığı tamamladı.
- `tools/promote_content_batch.py`: CEFR katalog + focus eşleşmesine bağlı güvenli izin kuralı.
- `tests/test_general_context_sprint_20261028.py`: kaynaksız kelimeyi reddetme, içerik bütünlüğü, idempotence testleri.
- `docs/GENERAL_CONTEXT_SPRINT_20261028.md`: ayrıntılı rapor.

## Sıradaki görev

Kalan 416 odak kelimeyi toplu ama **gerçekten anlamlı/orijinal örnekli** derslere yükselt. Hazır gloss kartlarını tam ders sayma. Aynı kelimeleri tekrar ekleme, ID/progress bozma. C1/B2 seviyeleri kaynak adayıdır; uzman onayı olmadan kesin CEFR sertifikası uydurma. Sonra 232 finans ikinci örneğini tamamla, Listening/Speaking içeriklerini ve WebKit QA'yı geliştirmeye devam et. Testleri çalıştır, yayın kilidini koru.

### NEWEST CURRENT STATE — 2026-10-28 spoken quality pass

Read `docs/SPOKEN_QUALITY_CURATION_20261028.md` before further curriculum work. Focus vocabulary is 1000 context drafts (500 B2, 500 C1), phrasal focus 500 context drafts (13 marked foundational B1 placement-first, 487 provisional advanced), extra finance/accounting 284. A total of 91 low-value general candidates were swapped for more conversationally useful sourced candidates, retaining 91 original IDs and lessons in `data/archived-vocabulary.json`; 399 distinct rapid cards remain. **125 tests pass (46 JS + 79 Python)**, release LOCKED. The word selection is a qualitative editorial pass, NOT corpus-frequency verified. Do not publish an incomplete ZIP or upload to GitHub; do not request Google Drive permissions. Next: licensed actual US conversational corpora (SUBTLEX-US, COCA Spoken/TV/Movies) frequency validation at sense-level, human en-US review, then listening/speaking training improvements. Never assert 0 initial red flags means all words frequent.


### 2026-10-28 — VOA natural-audio listening pilot
- New `data/authentic-listening.json`: 3 attributed public-domain VOA Level-2 dialogues, 118 transcript turns, 16 originally authored comprehension questions. Publisher transcripts structured, NOT automatic speech recognition; actual MP3-to-text timing unverified.
- New `Real Voices · VOA` navigation and Listening section route: online MP3 stream, transcript hidden by default, four-option questions, persisted result.
- No downloaded human MP3 files yet. The external audio playback has NOT been browser-verified due environment restrictions.
- `tools/download_voa_audio.py` supports future authenticated public source retrieval into local assets when network becomes available; not executed here.
- Removed 506 pre-existing rapid-card duplicates against active/archived lessons; preserved all progress IDs and archived/full cards. Remaining quick cards: 399. Fixed upstream-JSON-only importer edge case.
- Read `docs/VOA_AUTHENTIC_LISTENING_PILOT_20261028.md`. Explicitly no Google Drive, no GitHub publish, no release ZIP until all release criteria pass.


### VOA 50 source expansion, 28 October 2026

New `data/voa-source-catalog.json` provides 50 official source URLs (30 intermediate, 20 warm-ups) with search/filter in `js/app.js`. **Only 3 have full in-app transcript + quiz**; other 47 source-only; no new MP3 bundled. `tools/stage_voa_transcripts.py` stages publisher text when connected but has not been run with real network. Consult `docs/VOA_50_SOURCE_EXPANSION_20261028.md`. Preserve strict status separation and release lock.

### 2026-10-28 — VOA linked-question expansion (CURRENT)

- **50 VOA official source pages; 20 quiz-enabled lessons, 84 originally authored questions total**. Keep precise distinctions: 3 fully imported transcripts + 16 questions; 17 new source-linked listening quizzes + 68 questions; 30 source-only.
- `data/voa-source-quizzes.json`, `tools/build_voa_source_quizzes.py`, `js/voa-catalog.js`, `js/app.js` and service-worker manifest updated. New quizzes only open external VOA source for audio and transcript; **no new bundled MP3, no imported transcript**, no verified remote playback. Self-reported completion is marked in `P.authenticLessons`.
- Source pages reviewed for Level 2 lessons 3–9 and 11–20. See `docs/VOA_20_QUIZ_EXPANSION_20261028.md`. **Do not count 50 as quiz enabled**, 20 is the honest count. Continue with 30 remaining source pages for possible quizzes, consider publisher transcript import and source/audio QA.
- Also restored rapid list invariants by removing 415 general-lesson duplicates and 91 archived-word duplicates. 399 rapid-gloss-only cards remain; importer now accepts upstream JSON alone. All previous card IDs and study progress remain untouched.
- No Google Drive, GitHub push, or public release.


## Latest handoff — 28 Oct 2026 non-Speaking QA sprint

Authoritative state: 50 VOA sorulu ders, 204 soru; 4 tam transkript uygulamada, 46 ses/transkript VOA sitesinde (0 yerel insan MP3); Reading 30, Grammar 20; 1,000 kelime + 500 phrasal *taslak*; 18 eski sentetik mini podcast, 24 eski sentetik mikro-dinleme; Node 49 + Python 103 test başarılı; sanal Chromium hedefli smoke başarılı, gerçek iPhone ve uzaktan ses oynatma QA yapılmadı. **Speaking şu aşamada kapsam dışı.** `docs/NON_SPEAKING_QUALITY_SPRINT_20261028.md` ve `qa/non-speaking-sprint-report.json` dosyalarını oku. Yayın kilidini kaldırma, Google Drive kullanma, GitHub'a yükleme. Kaynak ve çalışma geçmişini silme.


## 29 Oct 2026 — Safari offline development (PRIVATE, DO NOT DEPLOY)
Core files and complete JSON/candidate catalog are now explicitly precached; Settings includes verified download/repair and missing-file reporting. 71 JavaScript + 164 Python tests passed. Virtual Chromium settings UI desktop/mobile passed. Real local HTTP Chromium blocked by administrator; physical iPhone Safari and human-voice VOA offline audio NOT tested. Keep release LOCKED, preserve Speaking and existing card/progress IDs. See `docs/20261029_SAFARI_OFFLINE_PRIVATE.md` and `qa/safari-offline-qa-report.json`.

## 2026-10-30 — QUALITY / SAFARI SELF-CHECK / RETENTION / TOEFL HUMAN REVIEW / VOA IMPORT TOOL (PRIVATE)

- Base: `AEL_PRIVATE_DEV_BACKUP_20261029_NO_ROBOTIC_PODCASTS_QA_DO_NOT_DEPLOY.zip`; do not regenerate from zero.
- Tests: 113 JS + 194 Python = **307 passing**, virtual Chromium desktop/mobile **pass**; real HTTP localhost Chromium **blocked by administrator**; WebKit binary unavailable; physical iPhone **not tested**.
- VOA: **30/50** in-app full transcripts, **20** linked source transcripts, **204/204** source-evidenced original quiz questions. Lesson 33–42 publisher pages identified. `tools/import_voa_level1_33_42.py` can fetch, stage and safely review them when external network works; **no ten transcripts imported in this sandbox**, so the requested pending count **10** is a target, not the current result.
- Human editorial workflow: `qa/20261030-editor-review/review-queue.csv` contains **975** priority cards, `full-curriculum-review-queue.csv` contains **2,334** total teaching cards. Automated structural fields checked, but **zero human approval**; `tools/validate_editor_signoff.py` remains a blocker.
- Safari settings includes a **user self-test** for airplane-mode relaunch and local cache. This is not an external device approval. `js/offline-device-qa.js` exports fail-closed validation.
- Learning Analytics has **7/30-day observed review** reports; no learner follow-ups existed in this development run. Not a randomized validation or guarantee of efficacy.
- TOEFL Writing: `js/toefl-human-review.js` allows comparing two independent human reviewers; always returns `officialTOEFLScore:null`, flags major disagreements. No ETS calibration, no automated essay semantics claim.
- Speaking untouched. No robotic MP3 reintroduced. All original data files unchanged, no card IDs deleted, progress schema preserved.
- Release remains **LOCKED**; no GitHub upload or deploy. User will manually handle GitHub when appropriately ready.
- Read `docs/20261030_PERSONAL_USE_ENGINEERING_QA_PRIVATE.md`, `qa/20261030-private-quality-audit.json`, and `qa/voa-source-staging/README.md` before any future changes.


## 2026-10-30 · Sentence Skills private development update

Added 34 lessons / 340 original exercises in Question Builder (12), Preposition Lab (10), Connector Lab (8), Sentence Builder (4). Access from “Soru & Cümle Atölyesi” in the app. Includes tap-to-order, contextual cloze, scenario-based production, feedback, separate stable review IDs, backup merge, and offline cache. **No public release, no editor sign-off and no iPhone Safari validation**. Speaking unchanged; no synthetic audio introduced. See `docs/20261030_SENTENCE_SKILLS_IMPLEMENTATION_PRIVATE.md`.


## 2026-10-30 finalize candidate
Performance reduced first-load raw bytes 3.44 MB -> 1.98 MB in virtual harness; UI wall time did not improve conclusively. Added content-loader.js, sw.js boot/full offline tiers, daily/TOEFL Writing autosave and late TOEFL session restoration. 338/338 unit/content tests passed, virtual mobile and desktop smokes passed; release gates remain blocked. See docs/20261030_FINALIZATION_RELEASE_CANDIDATE_PRIVATE.md. Speaking was unchanged. Do not deploy.
