# Çalışma raporu — 31 Tem → 4 Ağu 2026

Bant kurulumundan bugüne yapılan her işin dökümü. **Her satır bir dosya yoluna, bir commit'e
ya da bir SHA'ya bağlanır**; sayılar dosyadan okundu, hafızadan yazılmadı. Bilinmeyen
"bilinmiyor" diye yazıldı.

---

## 1. Kimlik

| alan | değer |
|---|---|
| rapor anı | 2026-08-04 10:5x +03:00 |
| depo | `D:\...\poster-var` · branch **`master`** |
| son commit | **`d2dc4f4`** · 04 Ağu 01:30 · *R3-1: multi-metric dose-response inventory…* |
| çalışma ağacı | **temiz** (0 değişiklik, rapor yazımından önce) |
| toplam commit | **32** |

### Tag listesi (beyan tag'leri dahil)

| tag | commit | tarih | ne sabitliyor |
|---|---|---|---|
| `audit-frozen-131` | `32e7d06` | 31 Tem 19:41:40 | Seçim denetimi N=131, kesme `2026-07-31-06-00-00` |
| `p5-predeclared` | `3bba863` | 31 Tem 19:41:40 | P5 karar kuralı, sonuçlardan önce |
| `p5-verdict` | `75d7b11` | 01 Ağu 04:29:34 | P5 hükmü, beyandan harfiyen uygulandı |
| `p6-predeclared` | `2d24427` | 01 Ağu 14:23:31 | P6.1/P6.2/P6.3 kuralları + 0.0012 barı, koşudan önce |
| `r3-predeclared` | `0b8ef2f` | 04 Ağu 00:59:56 | R3 metrik listesi/kutu sayıları/kesitler, hesaptan önce |

### Frozen-window kuralı — **hâlâ geçerli ✅**

Kural (`reports/2026-07-31_git_provenance.md:12`): *ön-kayıtların donduğu 14–31 Temmuz
penceresinde tek bir commit yok.* Yeniden ölçüldü:

```
git log --since="2026-07-14 17:42" --until="2026-07-31 17:03" → 0 commit
```

Pencerenin iki ucu: kampanya öncesi son commit `902c5b4` (14 Tem 17:41:48), kampanya sonrası
ilk commit `9b2d31c` (31 Tem 17:04). Aradaki **17 gün boyunca sıfır commit** — makaledeki
cümle (`git_provenance.md:90-91`) olduğu gibi durabilir.

---

## 2. İş dökümü

> **mtime uyarısı.** `paper_tables/` dosyalarının çoğu **03 Ağu 12:56** damgası taşır; bu
> üretim tarihi değil, İngilizce çeviri geçişinde yeniden üretilme tarihidir (commit
> `a0a07c4`). İçeriğin kaynağı aşağıdaki commit'lerdir.

### 2.1 Export bandı kurulumu

| alan | değer |
|---|---|
| görev kaynağı | `ide_prompt_export_bandi.md` (31 Tem 19:32) |
| yapılan | Repo → Drive tek yönlü, SHA-256'lı MANIFEST'li ihraç bandı; ters yönde yalnız `reports/` kanalı; STATUS heartbeat |
| kod | `diagnostics/export_to_drive.py` · `diagnostics/status_heartbeat.py` · `diagnostics/status_queue.txt` |
| çıktılar | `repo_export/MANIFEST.txt` · `STATUS.md` · `reports/` |
| commit | `a6a18d0` (31 Tem 18:05) · `b7d4ac0` (31 Tem 19:42) · `6421787` (31 Tem 19:43, .gitignore düzeltmesi) |
| sapma | **Sapma yok.** |

### 2.2 R0 paketi

| alan | değer |
|---|---|
| görev kaynağı | `ide_prompt_R0.md` (1 Ağu 14:28) |
| yapılan | Öğrenci-TS baseline kolu, eşleştirilmiş t + Holm düzeltmesi, Eq.8 headroom konvansiyonu |
| kod | `diagnostics/student_ts_baseline.py` · `inferential_tests.py` · `headroom_review.py` |
| çıktılar | `paper_tables/student_ts_baseline.{md,json}` · `inferential_tests.{md,json}` · `headroom_review.{md,json}` |
| commit | **`f381704`** (1 Ağu 14:48) |
| sapma | **Sapma yok.** |

### 2.3 R2 paketi

| alan | değer |
|---|---|
| görev kaynağı | `ide_prompt_R2.md` (2 Ağu 14:25) |
| yapılan | T* split-half stabilitesi (SHA yarıları), kanonik cümleler, beş gerçek, mekanizma spec eki, sıra-istatistiği trendi |
| kod | `diagnostics/tstar_stability.py` · `order_stat_trend.py` · `mechanism_specs.py` |
| çıktılar | `paper_tables/tstar_stability.{md,json}` · `order_stat_trend.{md,json}` · `mechanism_specs.{md,json}` · `reports/2026-08-02_r2_2_canonical_sentences.md` · `reports/2026-08-02_r2_4_five_facts.md` |
| commit | **`a29defc`** (2 Ağu 16:14) |
| sapma | **Bir tanesi, raporlandı:** FERPlus'ta \|T*_A−T*_B\| = 0.0263, kendi grid adımını (0.02) aşıyor. "Grid adımının altında" cümlesi yalnız RAF-DB için yazılabilir; tablo bunu açıkça söylüyor ve dört öğretmeni kapsayan doğru cümleyi öneriyor. |

### 2.4 P5 verdikt zinciri

| alan | değer |
|---|---|
| görev kaynağı | `ide_prompt_P5.md` (31 Tem 14:10) |
| yapılan | oracle_error gate'in kalibrasyon hasarı iki öğretmende tekrarlanıyor mu; kural koşulardan önce donduruldu, sonra harfiyen uygulandı |
| kod | `diagnostics/p5_oracle_replication_verdict.py` |
| çıktılar | `p5_oracle_replication/p5_verdict.{md,json}` |
| zincir | beyan mtime 31 Tem 14:14:11 → koşu 1/6 14:14:40 (**+29 sn**) → tag `p5-predeclared` → hüküm `0e615f2` (1 Ağu 04:29) → tag `p5-verdict` |
| sonuç | **0/2 KURULU** — her iki kol da ÇÖZÜNMEDİ (işaretler 3/3 değil **ve** büyüklük 2×bar altında) |
| sapma | **Sapma yok.** Önceden yazılmış "null kalırsa" metni yürürlüğe girdi. |

### 2.5 P6 — beyan → commit → tag → kuyruk

| alan | değer |
|---|---|
| görev kaynağı | `ide_prompt_gonderim_ve_P6.md` (1 Ağu 13:03) |
| yapılan | τ×T faktöriyeli (P6.1 çökme) + α modülasyonu (P6.2/P6.3); ilk **tam zincir** ön-kayıt |
| kod | `rafdb_p6_tau_alpha_queue.ps1` · `diagnostics/p6_1_early_reading.py` |
| zincir | beyan mtime 1 Ağu 14:21:57 → commit+tag `3d9dbee`/`p6-predeclared` 14:23:31 → ilk koşu `2026-08-01-14-23-45` (**+14 sn**) |
| erken okuma | `d896e42` (2 Ağu 14:40) — **ÇÖKME YANLIŞLANDI**, iki eşleşmiş çiftte de (~16× ve ~13.5× bar) · `reports/2026-08-02_p6_1_early_reading.md` |
| anlık durum | **29/42** bitti, 1 koşuyor, 12 sırada · ETA **05 Ağu 17:52** (~31 sa) — `diagnostics/status_heartbeat.md`'den okundu |
| sapma | **Sapma yok.** Erken okuma öncesi uygulayıcı ayrı commit'lendi (`2771534`, sonuç okunmadan). |

### 2.6 GitHub repro deposu — `calibration-law-fer`

| alan | değer |
|---|---|
| görev kaynağı | `ide_prompt_github.md` (3 Ağu 10:36) |
| yapılan | `git archive HEAD` ile kesit → temizlik taraması → sanitizasyon → makaleye bağlanmayan malzemenin budanması → Türkçe taraması ve çevirisi → private depo + push |
| kod | `tools/build_repro_export.py` · `tools/sanitize_public_export.py` |
| commit'ler | `d5ba10c` (3 Ağu 11:07) · `b7a9fe0` (11:23) · `0bd6c02` (12:16) · `a0a07c4` (13:06) · `0a4b4f2` (13:07) |
| depo | https://github.com/FatihSenturk/calibration-law-fer · **private** · commit **`9e514b1`** · **tek commit** · **277 dosya** |
| tarama | mutlak yol **0** (belgelenmiş tek istisna: `trails/posterv2/ir50.py` içindeki dört yorum satırı, üçüncü taraf POSTER++ dosyası) · kimlik bilgisi 0 · veri/checkpoint 0 · makale kaynağı 0 |
| public öncesi bekleyen | (i) public'e çevirme anı, (ii) depo sil+yeniden kur — Fatih'in `gh auth refresh -h github.com -s delete_repo` komutunu bekliyor (force-push sonrası GitHub'da SHA ile hâlâ çekilebilen eski commit nesnelerini temizlemek için) |
| sapma | **İki tane, ikisi de talep üzerine:** (1) "sil ve bildir, kendiliğinden silme" kuralı gereği bulgular önce raporlandı, silme kararı ayrıca alındı; (2) commit geçmişi tek commit'e indirildi ve yazar e-postası GitHub noreply adresine çevrildi — 4 Ağu talebi. |

### 2.7 Figür rötuşları — **2 Ağu'da istendi, HİÇBİRİ YAPILMADI**

Kanıt: `paper/figures/` altındaki **her PDF 1 Ağu tarihli** (en yenisi `graphical_abstract.pdf`
1 Ağu 14:38). 1 Ağu 14:18'den (`8a02b61` "Two figure fixes for the submission compile") sonra
tek bir figür commit'i yok.

| # | kalem | durum | kanıt |
|---|---|---|---|
| (a) | `ferplus_dual` 0.5063→0.51 etiketi + T=0.26 etiket kaydırma | ❌ **yapılmadı** | `ferplus_dual_axis_figure.py:40` hâlâ `"0.5063"` anahtarını basıyor; `ferplus_dual_axis.pdf` 1 Ağu 14:18 |
| (b) | `mechanism_diagnostic` `logit_std` etiket çakışması | ❌ **yapılmadı** | `mechanism_diagnostic_figure.py:91-92` sabit `xytext=(9, -2)` ofseti; çakışma giderici yok |
| (c) | `vote_examples` üst sıra hizası | ❌ **yapılmadı** | `vote_examples.pdf` **1 Ağu 10:13**, üreticide hiza değişikliği yok |
| (d) | `mechanism_diagnostic` PDF'inin P5-sonrası yeniden ihracı | ✅ **kapalı görünüyor** | `mechanism_diagnostic.json` altı P5 koşusunu **içeriyor** (`gate:oracle_error` **n=3**, stage1 *ve* primary) ve `mechanism_diagnostic.pdf` 1 Ağu **14:18** > P5 verdikti 1 Ağu **04:29** |

> **(d) hakkında bir düzeltme.** Prompt "fig dosyası yorumu hâlâ *bekleniyor* diyor" diyor.
> Depoda böyle bir yorum **bulamadım**: `bekleniyor` dizesi yalnız dört ilgisiz dosyada geçiyor
> (`ferplus_student_logit_cache.py`, `inferential_tests.py`, `p5_oracle_replication_verdict.py`,
> `tstar_stability.py`) ve hiçbiri figür ihracıyla ilgili değil. O yorum makale tarafında
> olabilir; **repo tarafında (d) kapalı**. Yanlışsam işaret et.

### 2.8 R3 turu (bu sabah)

| alan | değer |
|---|---|
| görev kaynağı | `ide_prompt_review_robustness.md` (4 Ağu 00:47) |
| ön beyan | `0b8ef2f` · tag `r3-predeclared` · **00:59:56** — üç üreticinin hiçbiri o commit'te yok |
| R3-2 | `diagnostics/tstar_sensitivity.py` → `paper_tables/tstar_sensitivity.{md,json}` (04 Ağu **01:03**) · T14 |
| R3-3 | `diagnostics/jsd_sensitivity.py` → `paper_tables/jsd_sensitivity.{md,json}` (04 Ağu **01:09**) · T15 |
| R3-1 | `diagnostics/robustness_metrics.py` + `calibration_metrics.py` + `ferplus_student_logit_cache.py` → `paper_tables/robustness_metrics.{md,json}` (04 Ağu **01:25**) · T13 |
| commit'ler | `ccf3b36` (01:17) · `d2dc4f4` (01:30) |
| R3-4 | **bekliyor** — P6 42/42 sonrası |
| sapma | **Üç tane, üçü de raporlandı ve beyana işlendi:** (1) prompt'un kapsam satırı depodaki hiçbir yapıyla eşleşmiyordu — düzeltilip **42 koşu**da sabitlendi, hesaptan önce; (2) "her yerde CUDA" kararı FERPlus'ta yanlıştı, kapı yakaladı, kural "her seri kendi denetiminin cihazında" oldu; (3) R3-1'in monotonluk sayımına, 0/3'ün yapısal olduğunu göstermek için betimleyici `argmin T` sütunu eklendi (eşik değil, konum). |

---

## 3. Öz-denetim

| # | kontrol | durum | kanıt |
|---|---|---|---|
| 1 | MANIFEST güncel mi? | ✅ | `MANIFEST.txt` **04 Ağu 01:31:09** — prompt yazıldığında (01:17) bayattı, R3 ihracıyla tazelendi. **77 dosya**; `tstar_sensitivity`/`jsd_sensitivity`/`robustness_metrics` için **24 SHA satırı** mevcut |
| 2 | reports/ dosyalarının hepsi MANIFEST'te mi? | ✅ | 7 rapor dosyası var (`reports/` glob'uyla ihraç ediliyor, tek tek liste değil); MANIFEST'te **21 `reports/` satırı** |
| 3 | STATUS "bekleyen" listesi yeni planla uyumlu mu? | ✅ **düzeltildi** | `status_queue.txt` güncellendi: gönderim ~8–9 Ağu, P6 makale kapsamında, figür rötuşları ve depo-silme adımı eklendi → **5 kalem** |
| 4 | PREREGISTRATIONS A1–A10 eksiksiz mi? | ✅ | A1…A10 hepsi mevcut (satır 36, 57, 79, 104, 132, 148, 165, 177, 446, 500); ayrıca B1–B4 |
| 5 | A9 hüküm alanı | ⏳ **açık, doğru** | *"(koşuyor — 42 koşu, ≈2–6 Ağu)"* — kuyruk 29/42, hüküm henüz okunmadı. Kapsam değişikliği (makaleye alınması) 26/42'deyken yazıldı |
| 6 | A10 hüküm alanı | ✅ | 4 Ağu hesaplandı; üç tabloya ve T13/T14/T15'e işaret ediyor |
| 7 | paper_tables → RESULTS_TABLES (tek kaynak) | ⚠ **bir kalem** | Aşağıdaki tablo |
| 8 | table_diff_gate kapsamı | ✅ | **432 hücre** (278 → 432; 56'sı R3, kalanı yeni serilerin kolonları). R3 öncesi R3 sayıları kapının dışındaydı, `cells_from_r3_*` eklendi |
| 9 | Bant kayıt kapısı | ✅ **yeni** | `export_to_drive.py::unregistered_tables()` — `paper_tables/` içinde olup EXPORTS'ta olmayan dosyayı bağırıyor. 4 Ağu'da `tstar_sensitivity.md` tam bu şekilde sessizce düşmüştü |

### 7. numaralı kalemin ayrıntısı — tek-kaynak ölçümü

Yöntem: her `paper_tables/*.json`'un sayısal yaprakları 2/3/4 ondalıklı biçimlerde
`RESULTS_TABLES.md` içinde aranır. Kaba bir gösterge (tesadüfi eşleşme mümkün), ama tek yönlü
güvenli: **eşleşmeyen sayı kesinlikle işlenmemiştir.**

| dosya | eşleşen / toplam | oran |
|---|---|---|
| mechanism_diagnostic | 65/66 | 98% |
| t5_pairing_diff | 106/110 | 96% |
| section54_numbers | 76/81 | 94% |
| headroom_review | 31/34 | 91% |
| student_ts_baseline | 43/48 | 90% |
| robustness_metrics | 572/685 | 84% |
| tstar_sensitivity | 51/61 | 84% |
| jsd_sensitivity | 53/66 | 80% |
| inferential_tests | 43/55 | 78% |
| denominator_table | 125/163 | 77% |
| order_stat_trend | 17/24 | 71% |
| tstar_stability | 50/78 | 64% |
| **mechanism_specs** | **0/20** | **0%** |

**Tek gerçek boşluk `mechanism_specs`.** Sebebi de belli: içeriği sonuç değil **hiperparametre
spesifikasyonu** (`gate_alpha_lo`, `gate_k`, kol başına koşu sayısı…). `RESULTS_TABLES.md`'de
yeri yok; ama `METHODS_DATA.md`'de de **geçmiyor** (arama: 0 eşleşme). Yani bu tablo şu an
yalnız kendi dosyasında yaşıyor ve banttan Drive'a gidiyor. **Karar Fatih'te:** metot/ek
bölümüne bu dosyadan mı alınacak, yoksa `METHODS_DATA.md`'ye mi işlenecek?

Kalan dosyaların %64–98 aralığı beklenen tablodur: JSON'lar ara değerleri de (grid noktaları,
sd'ler, n'ler) taşır, hepsinin makale tablosuna girmesi gerekmez.

---

## 4. Bekleyenler

| kalem | sahibi | ETA | bloklayan |
|---|---|---|---|
| P6 kuyruk sonu 42/42 → çıkış kontrolü | IDE | **05 Ağu 17:52** (29/42, ölçülen) | GPU |
| R3-4: T11/T12 + A9 resmî hüküm + `p6_collapse_test.md` | IDE | 05 Ağu akşamı | P6'nın bitmesi |
| Figür rötuşları (a)(b)(c) | IDE | rötuş başına <1 sa | **Fatih'in teyidi** — 2 Ağu'dan beri bekliyor |
| `mechanism_specs` tek-kaynak kararı | Fatih | — | karar |
| Depo sil + yeniden kur (asılı commit temizliği) | Fatih → IDE | komut sonrası ~5 dk | `gh auth refresh -h github.com -s delete_repo` |
| Depoyu public'e çevirme | Fatih | gönderim günü | gönderim |
| Gönderim | Fatih | **~8–9 Ağu** | makale entegrasyonu |
| ERTELENDİ: gerçek-sinyal gate n=3 (10 koşu) | IDE | revizyon dönemi | P6 sonrası GPU |
| ERTELENDİ: 2.248M scratch doz-yanıt (4 koşu) | IDE | revizyon dönemi | P6 sonrası GPU |

**Bilinmiyor:** figür rötuşlarının hâlâ istenip istenmediği (2 Ağu'dan beri teyit gelmedi);
`mechanism_specs`'in makalede nereye gireceği; gönderim gününün kesin tarihi.
