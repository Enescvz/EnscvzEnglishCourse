# Smart Review — FSRS-5 (development implementation)

Previous custom interval multipliers have been replaced with an FSRS-5 memory state
model in `js/engine.js`. The UI and review history remain compatible.

Reference: https://github.com/open-spaced-repetition/awesome-fsrs/wiki/The-Algorithm
(Section "FSRS-5", 19 parameters, defaults published in the wiki, edit 2026-07-28).

- Default retention: 90%. `fsrsInterval(stability)` uses the FSRS-4.5/5 forgetting curve with `FACTOR=19/81` and `DECAY=-0.5`.
- Initial difficulty and stability are defined by FSRS-5 default weights. Review updates use difficulty damping, mean reversion, same-day stability updates, FSRS recall/forgetting equations.
- Failed reviews are scheduled for a 15-minute learning step; this is **not** the 90%-retention interval. FSRS stability/difficulty are preserved separately.
- Each card retains cross-modality `modeSuccess` proof. Recall, recognition, context, listening and production are separate counters for mastery status. **Scheduling still uses ONE FSRS memory state per card; there is not yet an independent DSR model per modality.**
- Existing records have no memory state (`stability`,`difficulty`,`fsrsVersion`). They are migrated conservatively on the **next review** without discarding attempts, lapses or demonstrated-mode counters. This approximation does not reconstruct prior exact FSRS state and should not be described as history-optimized scheduling.
- No personalized parameter optimization (requires substantial longitudinal review data). No guarantee of C1 achievement or independently validated spaced-review outcomes.

Tests: `tests/fsrs.test.mjs`. All online licensing and release restrictions remain in force.

## 29 Ekim 2026 — kanıt odaklı öğrenme düzeltmeleri

- `memoryQueue` sadece zamanı gelmiş veya henüz hiç çalışılmamış kartları döndürür. Gelecekteki tekrarlar boş kontenjan sebebiyle öne çekilmez; `due` alanı eksik eski kayıtlar geriye dönük olarak ele alınır.
- Hafıza Koçu'nda `again` başarısız İngilizce geri çağırma; `hard` zor/eksik bağlam veya yanlış TTS yazımı (ama kelime hatırlandı); `good` doğru yazılı geri çağırma + bağlam tanımadır. Cihazda TTS olmaması `good`u engellemez. İsteğe bağlı cümle öz değerlendirmesi FSRS notunu belirlemez.
- Browser speechSynthesis yalnızca sentetik cihaz sesidir. Yeni TTS başarıları `ttsRecognitionSuccess` alanına yazılır, doğrulanmış insan sesi dinleme `modeSuccess.listening` alanına yazılmaz. Geçmiş TTS/listening sayıları geçmişin kökeni belirlenemediğinden silinmez veya otomatik sertifikalandırılmaz.
- Kişisel çağrışım öğrenme aşamasında kalır; bağımsız yazılı recall sırasında açılıp doğru yanıtı ipucuyla bozmaz.
- 400 TOEFL kelimesi ve 75 TOEFL phrasal verb, Hafıza Koçu'nda aynı `cards`/`phrasals` bankasına bağlanır. 50 yeni akademik kelime de tekrar motorunda görünür; eski kayıt ID'si değişmez.
- Bu çalışma FSRS-5 algoritmasının AEL öğrencileri üzerinde etkili olduğuna veya kişiye özel optimize edildiğine dair bağımsız kanıt değildir. Detay: `docs/20261029_MEMORY_SCIENCE_EVIDENCE_AND_AUDIT_PRIVATE.md`.
