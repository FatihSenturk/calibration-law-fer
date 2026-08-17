# Mutlak-yol kapısı — diske YAZILANDA beyansız mutlak yol var mı

Hedef klasör: `calibration-law-fer_2026-08-08`

> **Neden senkronun kendi doğrulamasından ayrı.** `public_repo_sync.py` "hiçbir dosyada mutlak yol kalmadı" derken kendi DÖNÜŞÜMÜNE bakar; bu kapı DİSKE yazılana bakar. Senkron hiç yazmadığı — ya da bir gün yazıp sonra kapsam dışına çıkardığı — bir dosyayı göremez.

> **Neden grep değil.** Gönderim dizisi 1c'nin ilk hâli yalnız kampanya deposunun önekini arayan tek bir `grep` idi. Ölçüldü: o desen 0 derken diskte 21 dosya mutlak yol taşıyordu — başka veri kökleri, başka kullanıcı ev dizinleri, UNC payları ve JSON kaçışlı çift-ters-bölü biçimi. Bu kapı deseni `public_repo_sync.ABS_ANY`'den ithal eder, yeniden yazmaz.

> **Hata sınıfı boş değilken GEÇTİ raporlanmaz** (9 Ağu 2026 kuralı). Bu betik okunamayan bir dosyayı `except OSError: continue` ile sessizce geçiyordu — o dosyaya soru sorulmuyor ama kapı yine GEÇTİ diyebiliyordu. Level-1 kapısında aynı desen (`başka hata` sütunu) üç gerçek ihlali gizlemişti. Okunamayan dosya artık sayılıyor ve sıfır değilse kapı düşüyor.

**SONUÇ: KAPI GEÇTİ** — beyansız mutlak yol 0 · okunamayan dosya 0

**Birim: DOSYA.** Bir dosyada kaç eşleşme olduğu ayrı sütunda; kapı dosya sayar.

| sınıf | dosya | eşleşme |
|---|---|---|
| BEYAN EDİLMEMİŞ | 0 | 0 |
| tek tek gerekçelendirilmiş kalıntı | 15 | 28 |
| üçüncü taraf (POSTERv2/CrossViT mirası, beyanlı muaf) | 3 | 7 |
| tarihli rapor sınıfı (o günün gerçeği, geriye dönük değişmez) | 4 | 35 |
| **toplam** | **22** | **70** |

Metin dışı (ikili) dosya atlandı: 97. Uzantı listesi betikte yazılı — kapsam daralması sessiz olmasın. **Okunamayan dosya: 0** (sıfır olmak zorunda; değilse kapı düşer).

## Beyanlı listenin tamamı

Depo günü "36'dan şuna indi, kalanlar şunlar ve muaf" cümlesi bu tablodan kurulur.

| dosya | sınıf | eşleşme |
|---|---|---|
| `diagnostics/DIAGNOSTIC_REPORT.md` | tek tek gerekçelendirilmiş kalıntı | 3 |
| `diagnostics/ferplus_abstention_entropy.py` | tek tek gerekçelendirilmiş kalıntı | 1 |
| `diagnostics/reports/2026-08-01_calisma_durumu.md` | tek tek gerekçelendirilmiş kalıntı | 1 |
| `diagnostics/reports/2026-08-08_final_devir.md` | tarihli rapor sınıfı (o günün gerçeği, geriye dönük değişmez) | 6 |
| `diagnostics/reports/2026-08-08_kapanis_turu.md` | tarihli rapor sınıfı (o günün gerçeği, geriye dönük değişmez) | 6 |
| `diagnostics/reports/2026-08-08_kontrol_turu.md` | tarihli rapor sınıfı (o günün gerçeği, geriye dönük değişmez) | 22 |
| `diagnostics/reports/2026-08-13_n5_selection.md` | tarihli rapor sınıfı (o günün gerçeği, geriye dönük değişmez) | 1 |
| `run_affectnetplus_unified_student.ps1` | tek tek gerekçelendirilmiş kalıntı | 1 |
| `run_ferplus_dual_lr_sam.ps1` | tek tek gerekçelendirilmiş kalıntı | 1 |
| `run_ferplus_foreground.ps1` | tek tek gerekçelendirilmiş kalıntı | 1 |
| `run_ferplus_other_splits_10e_pretrain.ps1` | tek tek gerekçelendirilmiş kalıntı | 1 |
| `run_ferplus_unified_student.ps1` | tek tek gerekçelendirilmiş kalıntı | 1 |
| `run_rafdb_kd_resolution_compare.ps1` | tek tek gerekçelendirilmiş kalıntı | 5 |
| `run_rafdb_nokd_resolution_compare.ps1` | tek tek gerekçelendirilmiş kalıntı | 2 |
| `run_rafdb_unified_student.ps1` | tek tek gerekçelendirilmiş kalıntı | 1 |
| `tools/build_ferplus_majority_metadata.py` | tek tek gerekçelendirilmiş kalıntı | 2 |
| `tools/eval_rafdb_teacher_student_table.py` | tek tek gerekçelendirilmiş kalıntı | 4 |
| `trails/posterv2/PosterV2_7cls.py` | üçüncü taraf (POSTERv2/CrossViT mirası, beyanlı muaf) | 1 |
| `trails/posterv2/ir50.py` | üçüncü taraf (POSTERv2/CrossViT mirası, beyanlı muaf) | 4 |
| `trails/posterv2/vit_vae_model.py` | üçüncü taraf (POSTERv2/CrossViT mirası, beyanlı muaf) | 2 |
| `train_affectnetplus_kd.py` | tek tek gerekçelendirilmiş kalıntı | 1 |
| `train_rafdb_kd.py` | tek tek gerekçelendirilmiş kalıntı | 3 |

---

Üretici: `diagnostics/abs_path_gate.py` · desen ve beyan sınıfları `public_repo_sync`'ten ithal (tek kaynak)

