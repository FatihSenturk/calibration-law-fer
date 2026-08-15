# Konsolide doğrulama turu — altı başlık

> **Yöntem.** Her satırda ölçümün kendisi ve kanıt yolu var. Sayı hafızadan yazılmadı. İddia
> tutmuyorsa **TUTMADI** dendi ve doğrusu yazıldı. Prompt'un beklentisiyle ölçümün ayrıştığı
> üç yer var; üçü de aşağıda açıkça işaretli.
>
> **Tarih notu.** Turun adı Fatih'in verdiği gibi 11 Ağustos; bu turun komutları makinede
> **2026-08-13** damgasıyla koştu ve dosya zaman damgaları öyle görünüyor. Uydurma tarih
> yazılmadı.

---

## 1 · T5/T5a — A12 sonrası yeniden ihraç

**Beklenti tutmadı, ama iyi yönde: depo tarafı zaten günceldi.** Bayatlık **tek taraflı** —
`paper/tables/tab_mechanisms.tex` (makale tarafı, kaynağı "1 Ağu") bayat; deponun ürettiği T5 ise
A12'nin üç-tohum değerlerini **9 Ağu'dan beri** taşıyor.

| soru | ölçüm |
|---|---|
| T5 üreticiden yeniden üretildi mi | ✅ `diagnostics/paper_tables.py` koşuldu (elle düzenleme yok) |
| T5 blogunda `†` işareti | **0 tane** — depo tablosunda hiç olmadı |
| kapı satırlarının tohum sayısı | **8/8 satır n=3** |
| işaret-deseni sütunu | zaten var: `signs @swa`, diğer üç-tohum satırlarla **aynı biçim** |
| kalan tek-tohum işareti | 4 hücre (`ctkd` ×3 öğretmen + `vae9182/g2g_kl+adaptive_t`), 16 `*(n=1)*` damgası — **kapı satırı değil**, hepsi meşru |
| T5a (`logit_std`) | üç öğretmenin üçü de **n=3** |

**Kapı satırları (T5, @swa, `RESULTS_TABLES.json`):**

| hücre | ΔECE | işaret | n |
|---|---|---|---|
| primary × `gate:mean_logvar` | −0.0056 | `--+` | 3 |
| stage1 × `gate:mean_logvar` | −0.0012 | `+--` | 3 |
| vae9182 × `gate:mean_logvar` | +0.0015 | `+--` | 3 |
| primary × `gate:target_logvar` | −0.0008 | `+--` | 3 |
| stage1 × `gate:target_logvar` | −0.0041 | `---` | 3 |
| primary × `gate:oracle_error` | +0.0004 | `-++` | 3 |
| stage1 × `gate:oracle_error` | +0.0015 | `-++` | 3 |
| vae9182 × `gate:oracle_error` | +0.0056 | `+++` | 3 |

Promptdaki iki satırla birebir aynı (`mean logvar` −0.0056[--+] / −0.0012[+--] / +0.0015[+--];
`target logvar` −0.0008[+--] / −0.0041[---] / vae yok).

**`criterion_applied` ile eşleşme — tek satır:** 21 T5 hücresinin **21'i** ortalama, sd ve işaret
deseninde birebir eşleşiyor (**uyuşmazlık 0**; `d_ece_mean` ↔ `mean`, `d_ece_sd` ↔ `sd_paired`,
`d_ece_signs` ↔ `signs`, tolerans 1e-12).

**Tablo kapısı: MOVED YOK, ve beklenen de buydu.** Kapı bu sekiz hücrenin 24 checkpoint
varyantını (`T5/*/gate:*/{swa,best,last}/d_ece`) **9 Ağu 16:29:39 tabanından beri** izliyor ve
değerler o gün bu değerlerdi. Bugünkü yeniden üretim **0 sapma** verdi. Yani "kapı hücrelerinde
MOVED bekleniyor" beklentisi ancak depo bayat olsaydı gerçekleşirdi; depo bayat değildi.

---

## 2 · Değişen yayımlanmış-değer çapaları

Kural uygulandı: **önce çapa listesi işlendi, sonra kapı koşuldu.**

| # | çapa | depoda karşılığı | yapılan |
|---|---|---|---|
| 1 | Asimetri 1.7–1.9× → **1.8–2.0×** | `asymmetry_estimand.py` başlığındaki alıntı | ✅ güncellendi |
| 2 | Order-stat +0.64–0.77 → **+0.65–0.76** | kod çapası **YOK**; `PUBLISHED_A2` zaten çifti taşıyor | ✅ + `BULGULAR.md` B-014'e güncel sürüm notu düşüldü |
| 3 | §5.5 başlığı "upper bound, not a guarantee" → "does not guarantee recovery" | depoda bu ifade **hiç geçmiyor** | çapa yok — dokunulmadı |
| 4 | Oracle çerçevesi "upper bound" → **"error-informed diagnostic"** | `p2_gate_oracle_verdict.py`, `equivalence_tests.py` | ✅ ikisi de güncellendi |
| 5 | FERPlus headroom 0.120 → **grid 0.113 birincil** | `headroom_review.py` (İtiraz 2 + Bölüm 2 + bağlayıcı kural) | ✅ güncellendi |
| 6 | `PUBLISHED_A2` = 0.6445 / 0.7640 | `order_stat_trend.py:50` | ✅ 9 Ağu'da işlendi — **ama "1 MOVED" ile değil**, aşağıya bak |

**Ölçülen değerler (hepsi artefakttan, elle yazılmadı):**

- **Asimetri.** Ekstrapolasyona dayanmayan çift: `rafdb_stage1/2` → **1.7706** [1.5021, 2.1329] ve
  `ferplus/0` → **2.0443** [1.6446, 2.4808] (`asymmetry_estimand.json`). Manşetin değişimi
  sayısal değil **sunum**: aynı iki sayının aralığı veriliyor (1.8–2.0), önceki manşet aynı iki
  sayının ortalama±sd'siydi (1.91 ± 0.19) ve alt ucu 1.72'ye çekiyordu.
- **FERPlus headroom.** ECE(T=1) = 0.128233. Fiilen taranan ızgara **G = 4 nokta**
  {0.26, 0.5063, 0.74, 1.0}, argmin T=0.5063 → **0.112605 ≈ 0.113**. İnce tarama **196 nokta**,
  T∈[0.1, 4.0], adım 0.02, argmin T=0.46 → **0.119824 ≈ 0.120**. `min_{T∈G}` tanımıyla birincil
  sayı 0.113 oldu ve **tanımın değeri ile koşulan kolun gerçekleşen azalması artık aynı sayı** —
  eskiden iki ayrı isme muhtaçtı. Üreticiye bir de **kapı** eklendi: G üzerindeki ECE argmin'i
  koşulan sıcaklık değilse `RuntimeError` ile durur.

**`PUBLISHED_A2` — teyit isteniyordu, dürüst cevap:** işlendi (9 Ağu), **ama "1 MOVED gerekçesi"
ile kapanmadı, çünkü 1 MOVED hiç olmadı.** `paper_tables/order_stat_trend.json` o gün SOURCES'a
**kayıtlı değildi**; yayımlı, Drive'a ihraç edilen ve §5.6'nın de-trend çiftini taşıyan artefakt
kapının dışındaydı. Kaydedilince **16 APPEARED** çıktı (14 hücre + 2 büyüme oranı), MOVED sıfır —
popülasyon değişmediği için. Ayrıntı: `reports/2026-08-09_selection_gain_kapsam.md` EK bölümü.

**Kapıya etkisi:** bu turun çapa düzenlemeleri **metinsel**; hiçbiri sayısal hücre üretmiyor.
Tablo kapısı düzenlemelerden sonra **999/999, 0 sapma** — yani sahte MOVED üretilmedi.

Bilgi olarak verilen iki kaleme (mekanizma özet cümlesi, "one-directional" ifadesi) **dokunulmadı**:
depoda çapa karşılığı yok. `robustness_metrics.py:248`'deki "one-directional" kendi metriğinin
tanımını anlatıyor, makalenin cümlesini alıntılamıyor.

---

## 3 · §4 envanteri — ön-kayıt tahmin sayımı

| blok | **tahmin** | ek karar yapıları | dondurma kanıtı |
|---|---|---|---|
| **A11** (R3-W1 çift-eksen) | **0** | 3 karar kolu + köşe tanımı (sayı görülmeden sabitlendi) | commit `2d6bed2` · **2026-08-06 00:38:04 +0300** · mesaj: "…HESAPTAN ONCE"; blok kendi tablosunda "`r3w1_joint_optimum.py` bu commit'te henüz YOKTU" diyor |
| **A12** (gerçek-sinyal gate n=3) | **3** | 3 tahminden birinde açık yanlışlayıcı + 3 cümle-sonucu | commit `b71e6ad` · **2026-08-06 12:06:59 +0300** · etiket **`a12-a13-predeclared`** · mesaj: "…KOSULARDAN ONCE" |
| **A13** (init-eşleştirilmiş kapasite) | **1** | 1 yanlışlayıcı + 3 karşılaştırma (üçü de raporlanacak) | aynı commit ve etiket |

**A11'in cevabı "0" ve bu bir eksiklik değil, bloğun kendi beyanı:** *"Hipotez testi DEĞİL, alt
yazı yeterlilik kontrolü. Başarı ölçütü yok."* Envantere tahmin olarak yazılırsa sayı şişer;
karar kuralı olarak yazılması gerekir.

**Dondurma zinciri saatiyle doğrulanabilir (A12/A13):**

| adım | zaman | kanıt |
|---|---|---|
| ön-beyan commit'i | 2026-08-06 **12:06:59** | `b71e6ad` — aynı commit PREREGISTRATIONS'a +117 satır ve **iki kuyruk dosyasını** birlikte ekliyor |
| hüküm uygulayıcıları commit'i | 2026-08-06 **21:47:53** | `ca5d75a` — "A12 + A13 hukum uygulayicilari — ILK SONUC OKUNMADAN commit" |
| ilk A12 koşu dizini | 2026-08-06 **22:29:13** | `results/unified_students/RAFDB_stage1_gate_noclassweight_.../2026-08-06-22-29-13` |

Beyan → uygulayıcı → koşu sırası 10 saat 22 dakikalık bir pencerede, üç bağımsız zaman damgasıyla.
Ayrıca `preregistration_blocks.csv` A12'ye **10**, A13'e **1** koşu beyan ediyor (A13'ün diğer üç
koşusu `w050` kolundan devralınan noktalar). Diskte 11 A12 dizini var: biri kesinti sonrası
`ABANDONED.json` taşıyor, yani **10 geçerli koşu**.

---

## 4 · §4 provenans iddiaları — çapraz teyit

### (a) Manifest bölünmesi — **28 sayısı TUTMADI**

| sınıf | ölçülen | dosya alanı |
|---|---|---|
| launch-time doğrulanmış | **26** | `manifest.json` → `code_state_verified: true` |
| retroaktif | **62** ✅ | `code_state_verified: false` |
| **bitmemiş (değerlendirilemez)** | **2** | `code_state_verified: null` |
| toplam manifest | **90** | `results/unified_students/*/*/manifest.json` |

62 doğru; 28 değil **26**. 28'in kaynağı görünüşe göre 90 − 62 = 28, yani **değerlendirilemez
olan 2 koşu doğrulanmış sınıfına katılmış.** Üreticinin kendi çıktısı bu üçlüyü ayrı basıyor
(`run_manifest.py:214`: "n verified, n with post-run code edits, n unfinished (not evaluable)").

**Belgelenen pencere:** **2026-06-17-13-17-49 … 2026-07-24-22-22-33.** Kanonik defter (199 koşu)
**2026-08-08-16-49-26**'ya kadar uzanıyor; yani **113 koşunun manifesti hiç yok**. Cümle
kurulurken bu sınır yazılmalı: bölünme kampanyanın tamamını değil, 24 Temmuz'a kadarki 90 koşuyu
anlatıyor.

> **Level-1 uyarısı.** Bu üç sayı `runs.csv`'de **yok** (27 kolonun hiçbiri manifest taşımıyor);
> yalnız koşu dizinlerinden türetilebiliyor. Yani §4'e yeni giren bir sayının Level-1 yolu yok.
> Kapanış için ya küçük bir sınır-defteri (epok eğrileri gibi) yayımlanmalı ya da cümle
> "koşu dizinlerinden" diye kaynaklanmalı. Bu turda **yapılmadı** — ayrı karar.

### (b) Gecikme protokolü ✅

`diagnostics/latency_benchmark.py` — `--cpu-warmup 5` / `--cpu-iters 20` (satır 199-200),
`--gpu-warmup 50` / `--gpu-iters 200` (satır 197-198); dtype kuralı satır 19: *"fp32 always;
fp16 via autocast on CUDA (skipped on CPU, where fp16 conv is not accelerated)"*. Dördü de
iddiayla birebir.

> Dikkat: `tools/eval_rafdb_teacher_student_table.py::_measure_latency` **20/100** varsayılanı
> taşıyor. O ayrı bir araç ve makaledeki sayıların kaynağı değil; karıştırılırsa protokol
> cümlesi yanlış dosyaya bağlanır.

### (c) CPU b=32 oranı ✅ (ve ikinci bir oturum var)

`diagnostics/p5_efficiency/latency_benchmark.json` → `speedups[device=cpu, batch=32, fp32]`:
öğretmen **716.70 ms** / öğrenci **161.64 ms** = **4.4340×** → 4.43 ✅.
İkinci oturum (`latency_benchmark_session2.json`): 754.71 / 171.83 = **4.3922×**. İki oturum
arasındaki yayılım 0.04×; makale hangisini verdiğini söylüyorsa oturum-1'dir.

### (d) `vich_use_sampling` ✅ (öğrenci tarafı için kesin ifade gerekiyor)

| taraf | ölçüm | kanıt |
|---|---|---|
| Stage1 öğretmen | `vich_use_sampling: True` | `results/teacher_logs/RAFDB/POSTERv2/2026-07-17-04-41-04/RAFDB_posterv2_vich_klb1e4_200e.yaml:31` |
| Primary öğretmen | `vich_use_sampling: True` | `configs/RAFDB_posterv2_vich_recipe.yaml:31` |
| öğrenci (VICH başlı) | **230/230 koşuda `False`** | her koşunun `run_args.json` → `use_vich_sampling` |
| öğrenci (linear başlı) | 3 koşuda `True` — **atıl** | `models/mobilenetv2_plus.py:345-349`: `use_sampling` yalnız `VICHHead` kurulurken geçiyor; linear başta VICHHead hiç kurulmuyor |
| değerlendirmede | **yapısal olarak kapalı** | `models/mobilenetv2_plus.py:131` — `if self.training and self.use_sampling` |

Yani "öğrenci başında iki aşamada da kapalı" doğru; tek incelik, bayrağın **varsayılanı `True`**
(`train_rafdb_kd.py:1081-1082`) ve kapatan şey her koşunun `--no-vich-sampling` bayrağı — bir
sonraki koşu bunu unutursa varsayılan geri gelir.

### (e) Kapı koşu sayımı ✅ birebir

`runs.csv` → `gate_signal` kolonu, filtre `manipulation == "gate"` (üretici
`diagnostics/build_runs_ledger.py`):

| sinyal | koşu |
|---|---|
| `mean_logvar` | **10** |
| `oracle_error` | **9** |
| `target_logvar` | **6** |
| `top2_logvar` | **0** (defterde hiç geçmiyor) |
| `entropy` | **0** (defterde hiç geçmiyor) |

Toplam 25 kapı koşusu; defterdeki `gate_signal` taşıyan satır sayısı da 25, yani sızıntı yok.

---

## 5 · Tazelik + kapılar

**9 Ağu 16:34'ten beri değişen üretici/doküman: 6.**

| dosya | ne değişti |
|---|---|
| `diagnostics/public_repo_staleness.py` | hedef + normalleştirici tek kaynağa bağlandı (9 Ağu bulgusu) |
| `diagnostics/asymmetry_estimand.py` | çapa 1.7–1.9 → 1.8–2.0 |
| `diagnostics/equivalence_tests.py` | oracle çerçevesi |
| `diagnostics/p2_gate_oracle_verdict.py` | oracle çerçevesi + kapsam cümlesi |
| `diagnostics/headroom_review.py` | `min_{T∈G}` + argmin kapısı |
| `BULGULAR.md` | B-014'e güncel order-stat sürümü |

Yeniden ihraç yapıldı (aşağıda).

**Kapılar — madde 1 ve 2 işlendikten SONRA:**

| kapı | sayı | sapma | sonuç |
|---|---|---|---|
| tablo (`table_diff_gate`) | **999** hücre | **0** | ✅ taban 2026-08-09T16:29:39 |
| figür (`verify_paper_figures`) | **10** figür | **0 failing** | ✅ vektör-only, TrueType/Type1, ≥7.0 pt, tek sayfa |
| mutlak yol (`abs_path_gate`) | 20 dosya / 68 eşleşme | beyansız **0** · okunamayan **0** | ✅ GEÇTİ |
| Level-1 (`level1_gate`) | 42 üretici | İHLAL **0** · başka hata **0** · muaf 9 | ✅ GEÇTİ |
| bayatlık (`public_repo_staleness`) | 274 izlenen | **GERÇEK BAYAT 0** | ✅ 115 aynı + 80 satır-sonu + 79 uyarlama |

---

## 6 · STATUS temizliği

Düzenleme `STATUS.md`'ye değil, onu üreten beyan dosyasına yapıldı
(`diagnostics/status_queue.txt`; `status_heartbeat.py` onu okuyor).

| kalem | yapılan |
|---|---|
| 1 · BAŞLIK v2 | bayat "AÇIK: HEADLINE_2 tekrar ediyor" notu **düşürüldü**. Yerine ölçüm: satır `"— dose–response at fixed teacher accuracy, in both directions —"` ve **iki depoda birebir aynı** (`graphical_abstract.py:55`, poster-var ve `calibration-law-fer_2026-08-08`) |
| 3 · C kalemi | "279 dosya" bayattı → güncel hedef tarihli klasör, **531 dosya**, eşitleme 0 güncellenecek / 79 uyarlama / gerçek bayat 0; git'te **249 giriş commit edilmemiş** (192 izlenmeyen + 57 değişmiş), karar Fatih'te |
| 5(c) · DA-5 | "hiçbirine dokunulmadı" bayattı → DA-5 kapandı, estimand ve manşet kaydedildi |
| 7 · A12/A13 | "KALAN İŞ: uygulayıcılar commit'lenecek" bayattı → **KAPANDI 8 Ağu**, üç zaman damgalı zincir yazıldı |

Kapanmamış kalemler (2 · gönderim tarihi, 3'ün sil/yeniden-kur adımı, 5'in makale tarafı)
olduğu gibi duruyor.

---

## Kalan açık kalemler (karar Fatih'te)

1. **§4'ün manifest cümlesi 26/62/2 olmalı** (28 değil) ve "24 Temmuz'a kadarki 90 koşu" sınırı
   yazılmalı.
2. **Manifest sayılarının Level-1 yolu yok** — sınır-defteri yayımlanacak mı, yoksa cümle koşu
   dizinlerine mi kaynaklanacak.
3. **Genel depoda 249 commit edilmemiş giriş** + kapsam içinde olup depoda hiç olmayan 149 dosya.
4. `public_repo_sync.py --prune-extras` hâlâ yazılmadı (8 Ağu'da beyan edilen yapısal boşluk).

---

Üretici: elle yazıldı · ölçümler `paper_tables.py`, `criterion_applied.py`, `asymmetry_estimand.py`,
`headroom_review.py`, `latency_benchmark.py` çıktıları, `runs.csv`, `PREREGISTRATIONS.md`,
`preregistration_blocks.csv`, koşu dizinlerinin `manifest.json`/`run_args.json` dosyaları ve
`git log` üzerinden
