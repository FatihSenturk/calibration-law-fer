# Kontrol turu — 8 Ağustos 2026

> **Yöntem.** Her satırda ölçümün kendisi var; "uygulandı" gibi bir cümle tek başına
> yazılmadı. Yapılmayan maddeye **YAPILMADI** dendi. Bir işlem N dosyadan M'sinde
> çalıştıysa hem N hem M yazıldı.
>
> Bu tur **kendi ölçümlerimde üç hata** buldu ve üçü de raporda duruyor (1.4, 2.1, 2.2):
> bir ölçüm sıfır veriyorsa önce ölçüme bakılır.

---

## 1. Public depo — kapsam ve dönüşüm

### 1.1 D kovası kararları — ✅ KAPANDI

| kova | dosya | boyut |
|---|---|---|
| A — iddia taşıyan | 153 | 5.7 MB |
| B — süreç kaydı | 28 | 1.9 MB |
| C — girmesin | 93 | 101.0 MB |
| **D — kararsız** | **0** | **0.0 MB** |

**Kapsam içi (A+B): 181 dosya.** D **sıfır**.

13 dosya tek tek karara bağlandı ve karar `public_scope_buckets.py::D_DECIDED`'da **beyan**
olarak duruyor (kural değil, çünkü kök artefaktlarının hangi zincire ait olduğu adından
anlaşılmıyordu):

| dosya | kova | gerekçe |
|---|---|---|
| `STUDENT_VICH_HEAD_ARCHITECTURE.md` | B | öğrenci mimarisi; başlık eklendi |
| `TEACHER_MODEL_ARCHITECTURE.md` | B | öğretmen mimarisi; başlık eklendi |
| `STATUS.md` | B | zaten `SUPERSEDED 2026-08-01` başlıklı |
| `PHASE0_NOTES.md` | B | mekanizma notları; başlık eklendi |
| `ALL_RESULTS_SUMMARY.md` | C | `RESULTS_TABLES.md` ile karışır |
| `README_STUDENT.md` | C | 13 Haz protokolü, kırık `reference_90_74\` işareti |
| `fig1_overall_kd_framework.{pdf,svg,_600dpi.png}` | C | **makalede kullanılmıyor** (`main_elsarticle.tex`/`sections/` taranarak ölçüldü) |
| `generate_kd_figure.py` | C | yukarıdaki üç şeklin üreticisi |
| `rafdb_mobilenetv2_all_results_table.csv` | C | başka çalışma; öğretmen 92.40547588, üç öğretmenin hiçbiri değil |
| `rafdb_teacher_student_metrics_table_with_best.csv` | C | aynı çalışma; öğrenci 2.232921 M ≠ 2.248291 M |
| `beta_weighted_kd.py` | C | ölü kod (1.2) |

### 1.2 `beta_weighted_kd.py` — ✅ KAPANDI: ölü kod → C

- Taranan `.py`: **133** (kök + `tools/` + `models/` + `diagnostics/` + `dataset_utils/` + `utils/`)
- `import beta_weighted_kd` / `from beta_weighted_kd import`: **0 eşleşme**
- Tek geçiş `tools/build_repro_export.py:40` — ama orası bir `import` değil, `ALLOW` **glob
  listesindeki bir dize**. Kod bağımlılığı değil, ihraç beyanı.
- Modül `BetaWeightedKDLoss` / `train_one_epoch_beta_kd` tanımlıyor; kampanya
  `kd_common.DistillationLoss` kullanıyor.

**→ C.**

### 1.3 B kovasında başlık — ✅ KAPANDI (4/4)

B = **28 dosya**. Bunların **4'ü kök `.md`** (başlık gerektirenler), 24'ü
`diagnostics/reports/*` ve tanılama artefaktı — onlar dosya adında tarih taşıyor, banner
gerektirmiyor.

| dosya | önce | sonra |
|---|---|---|
| `STATUS.md` | ✅ vardı (`SUPERSEDED 2026-08-01`) | değişmedi |
| `PHASE0_NOTES.md` | ❌ yoktu | ✅ eklendi |
| `STUDENT_VICH_HEAD_ARCHITECTURE.md` | ❌ yoktu | ✅ eklendi |
| `TEACHER_MODEL_ARCHITECTURE.md` | ❌ yoktu | ✅ eklendi |

**1/4 → 4/4.**

> **Kendi hatamın düzeltmesi.** Kova önerisini sunarken `STUDENT_VICH_HEAD_ARCHITECTURE.md`
> ve `PHASE0_NOTES.md` için "doğruluk sayısı yok" demiştim. Ölçünce çıktı:
> `STUDENT_VICH_HEAD_ARCHITECTURE.md` **92.41** ve **88.72** taşıyor. (`PHASE0_NOTES.md`
> gerçekten taşımıyor — doksanlık hiçbir değer yok.) 92.41, Mart 2026'daki farklı bir
> çalışmanın öğretmeni; `TEACHER_MODEL_ARCHITECTURE.md` aynı sayıyı **üç kez** taşıyor.
> Üç başlık da bu ölçüme göre, sayıları adıyla anarak yazıldı.

### 1.4 Fırlatıcı işlevsel kuralı — ✅ KAPANDI, ama ölçüm iki kez bozuktu

| uzantı | toplam | defterde koşu başlatan → A | başlatmayan → C |
|---|---|---|---|
| `.bat` | 32 | **13** | **19** |
| `.ps1` | 109 | 21 | 88 |

**`.bat` için 13/19 beklenen değere birebir uydu.**

`.ps1` ölçümü ilk iki denemede yanlıştı ve ikisi de `launches_published_run`'ın regex'inde:

1. **İlk ölçüm 0/109 verdi.** Regex `--name\s+"?(...)` yalnız düz biçimi görüyordu
   (`--name RAFDB_x`). Üretilmiş kuyruklar PowerShell dizi biçimi kullanıyor:
   `"--name", "RAFDB_x"` — `--name`'den sonra boşluk değil `",` geliyor.
2. **Düzeltince 2/109 oldu** — yalnız A12/A13. Çünkü **elle yazılmış kuyruklar adı şablonla
   kuruyor**: `$runName = "RAFDB_$($Stage.Teacher)_gate_oracle_error_..._seed$($Stage.Seed)"`.
   Gerçek koşu adı dosyada **hiç geçmiyor**; çalışma anında bir aşama tablosundan birleşiyor.
   Şablonu desene çevirince (`$(...)` → `.+`) 21/109 oldu.

**Kalan 88'in neden sıfır olduğu (ayrıca ölçüldü):** FERPlus kuyrukları
(`ferplus_*_queue.ps1`) yayımlanmış FERPlus koşuları başlatıyor ama `runs.csv` **yalnız
RAF-DB** — defter onları göremiyor. `rafdb_a12_a13_chain.ps1` gibi zincirler python değil
başka `.ps1` çağırıyor. Geri kalanlar başka kampanya.

> **Bu bulgu kovalama kuralını değiştirmiyor.** `.ps1`'lerin hepsi A'ya giriyor (8 Ağu
> kararı), çünkü ön-beyan metni dosyanın içindedir ve **iptal edilmiş kuyruk defterde hiç
> görünmez**. Ölçüm bu kararı zayıflatmıyor, güçlendiriyor: işlevsel test şablonlu
> kuyruklarda statik olarak karar veremiyor.

### 1.5 5 MB kapsam eşiği — ✅ KAPANDI: 0

- Eşik: 5 MB · kapsam (A+B): 181 dosya · **eşiği aşan: 0**
- Kapsamdaki en büyük dosya: `configs/FERPlus_processed_metadata.csv` — **2.67 MB**

### 1.6 Önbellek logitleri + `configs/*.csv` — ✅ KAPANDI, hepsi A

| kalem | dosya | boyut | kova |
|---|---|---|---|
| önbellek logit | 5 | **567 KB** | A (5/5) |
| `configs/*.csv` | 2 | **4.18 MB** | A (2/2) |

Önbellek logitleri: `ferplus_jsd/ferplus_val_logits.pt` (225 KB),
`ferplus_jsd/per_sample_human_entropy.npy` (12 KB), `teacher_ece_grid/teacher_val_logits_{primary,stage1,vae9182}.pt`
(110 KB × 3). `configs/FERPlus_Created_metadata.csv` (1.51 MB) +
`configs/FERPlus_processed_metadata.csv` (2.67 MB).

---

## 2. Mutlak yol — genelleştirilmiş kapı

### 2.1 Kapı artık desen arıyor — ✅ KAPANDI

Eski hâli **tek bir önek** idi ve adı "mutlak yol kalmadı" diye rapor ediyordu:

```python
ABS_ANY = re.compile(r"D:[\\/]5 temmuz claude".encode())
```

Yeni hâli:

```python
ABS_ANY = re.compile(
    rb"(?<![A-Za-z0-9])[A-Za-z]:[\\/]{1,2}[.+\- ]*[A-Za-z0-9_]"        # C:\x, D:/x, D:\\x (JSON)
    rb"|/(?:Users|home)/[A-Za-z0-9_.\-]"                                # /Users/x, /home/x
    rb"|(?<![A-Za-z0-9:])\\{2,4}[A-Za-z0-9_.\-]+\\{1,2}[A-Za-z0-9_.\-]" # UNC \\sunucu\pay
)
```

Ayrıca ilk bileşen en az bir harf/rakam içermek zorunda — raporlardaki `D:\...\poster-var`
gibi **bilerek kısaltılmış prosa** ifadeleri yol sayılmasın diye.

**Eski kapının kaçırdığı iki sınıf, ikisi de ölçülerek bulundu:**

1. **JSON kaçışı.** `.json` içinde yol `"data"` diye
   yazılır; `D:` ile `5` arasında **iki** ters bölü olur ve `[\\/]` (tek karakter) eşleşmez.
   `diagnostics/dataset_hash_cache.json` hem dönüşümden hem doğrulamadan sessizce geçmişti —
   kaynakla public'teki hâli **bayt bayt aynıydı**. Dönüşüm kuralı kaçışlı biçimi de
   tanıyacak hâle getirildi ve doğrulandı:
   `"data/rafdb_aligned"` → `"data/rafdb_aligned"`.
2. **Küçük harfli sürücü.** `STATUS.md` yolu `d:\5 temmuz claude\...` diye yazıyor; desen
   `D:` bekliyordu. `[Dd]:` yapıldı.

**Kapının çıktısı: 45 → 38 → 36 dosya** (üç düzeltmeden sonra).

### 2.2 Eski-makine öneki taraması — ⚠️ ÖLÇÜLDÜ, üç sınıfta karar bekliyor

`21mar` sorusundan çıkan tarama. **Anahtar kelime listesi kullanılmadı** — biçim tarandı.

| önek | dosya | karar |
|---|---|---|
| `D:/Veriseti/poster-var` | 14 | ⏳ **karar bekliyor** — config veri kökleri |
| `C:/datasets`, `C:/dataset` | 17 | ⏳ **karar bekliyor** — config veri kökleri |
| `D:/27may/poster-var` | 8 | ⏳ **karar bekliyor** — config veri kökleri |
| `D:/lg/datasets`, `D:/lg/logs` | 6 | ⏳ **karar bekliyor** — eski makine veri/log kökleri |
| `C:/Users/mfati/21mar`, `C:/Users/mfati/Desktop/15mar` | 5 | ⏳ **karar bekliyor** — argparse varsayılanları |
| `G:/My Drive` | 3 | ✅ **C'ye alındı** — `export_to_drive.py` META_PUBLIC'e taşındı |
| `F:/0815crossvit`, `C:/Users/86187` | 5 | ✅ **muaf beyan edildi** — POSTERv2/CrossViT'ten miras, üçüncü taraf kodu |
| `D:\\5 temmuz claude` (JSON kaçışlı) | 5 | ✅ **dönüştürüldü** (2.1) |
| `d:\5 temmuz claude` (küçük harf) | 1 | ✅ **dönüştürüldü** (2.1) |

**`21mar`'ın içine bakılmadı ve bakılamaz:** `C:\Users\mfati\21mar` bu makinede **yok**
(`Test-Path` ile ölçüldü). Yol, dosyaların içindeki bir dize.

**Karar bekleyen ne:** 19 config'in `train_root` / `val_root` / `metadata` /
`affectnet_plus_cache_dir` alanları başka makinelerin veri köklerini gösteriyor. Deponun
**kendi konvansiyonu ölçülerek bulundu** — temiz config'ler şöyle yazıyor:

```yaml
# configs/FERPlus_8_teacher_vae_ce_kld.yaml
train_root: data/FERPlus_processed
metadata:   configs/FERPlus_majority_metadata.csv
```

`*/poster-var/<kuyruk>` biçimindekiler bu konvansiyona **mekanik** çevrilebilir. Ama
`C:/datasets/FERPlus_Created` → `data/FERPlus_Created` eşlemesi bir **karar**: depoda
karşılığı olmayan bir dizin adı uydurmak olur. Bu yüzden kendi başıma uygulamadım.

### 2.3 Yazılacak dosyalarda mutlak yol — ❌ SORUNLU: 0 değil, **36**

| kalem | sayı |
|---|---|
| kapının bildirdiği kalan | **36** |
| bunlardan **bloke edilen onaylı aday** (yazılmadı) | **27** |
| zaten izlenen (3 Ağu'dan beri yayımda) | 9 |
| üçüncü taraf muaf (beyanlı) | 5 |

**Kapı işini yapıyor:** 27 dosya mutlak yol taşıdığı için **yazılmadı**. Yani depoda o
yollar yok — ama o 27 dosya da yok, dolayısıyla kapsam listesiyle depo arasında 27 fark var.
2.2'deki konvansiyon kararı verilmeden bu madde kapanamaz.

Bloke edilen 27: 19 config, 6 fırlatıcı `.ps1`, `tools/eval_rafdb_teacher_student_table.py`,
`tools/sanitize_public_export.py`.

---

## 3. Yol/işaret bütünlüğü

### 3.1 Kırık işaret taraması — ❌ SORUNLU: **50** kırık atıf

Yayımlanacak küme 460 dosya; A+B'deki metin dosyaları tarandı.

| sınıf | atıf | not |
|---|---|---|
| `tests/*` (Phase 0 regresyon testleri) | 9 | `PHASE0_NOTES.md`, `STATUS.md` atıf yapıyor; **kaynakta VAR, kapsamda yok** |
| `specs/*.yaml` | 2 | hiç var olmadı — spec'in varsaydığı düzen |
| `reference_90_74/config.json` | 1 | **bilinen kırık işaret**, `run_phase0_rafdb_ce9241_diagnostic.ps1:18` |
| `lg/logs/...best.pt`, `models/mobilefacenet_model_best.pt` | 3 | kaynakta da yok |
| `diagnostics/export_to_drive.py` | 1 | **bu turda ben yarattım** — `level1_gate.py:49` ona atıf yapıyor, ben onu C'ye aldım |
| `planning/ide_prompt_*.md`, `reviews/...` | 3 | Drive'da, depoda hiç olmadı |
| geri kalan | 31 | çoğu `status_heartbeat` ve rapor içi çapraz atıf |

**Öneri (uygulanmadı):** `tests/` kapsama alınsın. Dokuz atıf oraya gidiyor, dosyalar küçük
ve "çalışan kod" vaadini destekliyor; iki B belgesini yayımlayıp atıf ettikleri testleri
yayımlamamak tutarsız.

---

## 4. Level-1 değişmezi

### 4.1 Defter gate-sinyali sütunu — ⏳ **A12 sonrasına bırakıldı**

Yapılmadı. Yalıtılmış adım olarak planlandığı gibi A12 kapanışıyla karıştırılmadı; A12'nin
tablo kapısı zaten 13 sapmayla durdu (7.3), araya bir sütun daha girmesi o sapmaların hangi
nedenden geldiğini bulanıklaştırırdı.

### 4.2 Kalan ihlaller — ❌ YAPILMADI

Level-1 kapısının güncel çıktısı:

| durum | sayı |
|---|---|
| GEÇTİ | **20** |
| **İHLAL** | **13** |
| muaf (beyanlı) | 6 |
| başka hata | 8 |
| zaman aşımı | 0 |

İhlal veren 13: `a12_realsignal_verdict`, `criterion_applied`, `denominator_table`,
`mechanism_diagnostic_figure`, `mechanism_specs`, `noise_units`, `p2_gate_oracle_verdict`,
`p6_verdict`, `paper_tables`, `r3w1_joint_optimum`, `robustness_metrics`,
`section54_numbers`, `t5_pairing_diff`.

**Düzeltilmedi.** Sekizinin kök nedeni tek: `t5_pairing_diff.gate_variant()` koşu dizini
okuyor.

### 4.3 8 "başka hata" — ✅ KAPANDI: **hiçbiri gerçek sorun değil, sekizi de kapının yapaylığı**

| betik | hata | tanı |
|---|---|---|
| `bootstrap_cis.py` | `unrecognized arguments: ...bootstrap_cis.py` | **yapaylık** — kapı betiği `runpy` ile çağırırken yolu `argv[1]`'de bırakıyor, argparse onu görüyor |
| `level1_gate.py` | aynı | **yapaylık** — kapı kendini çalıştırıyor; anlamsız |
| `public_repo_sync.py` | aynı | **yapaylık** — aynı argv sorunu |
| `student_ts_baseline.py` | aynı | **yapaylık** — aynı argv sorunu |
| `order_stat_trend.py` | `UnicodeEncodeError: charmap ... '\u015f'` | **yapaylık** — alt süreç stdout kodlaması, Level-1 ile ilgisiz |
| `tstar_stability.py` | `UnicodeEncodeError: ... '\u0131'` | **yapaylık** — aynı |
| `selection_gain_estimator.py` | `ModuleNotFoundError: stats_convention` | **yapaylık** — `runpy` altında betiğin kendi dizini `sys.path`'te değil |
| `selection_robustness.py` | aynı | **yapaylık** — aynı |

**Hiçbiri koşu dizinine dokunmadan düştü**, yani Level-1 sorusuna cevap vermiyorlar.
**Muaf listesine geçirilmedi** — muafiyet "işi koşu dizini okumak" demek, bunlar o değil.
Doğru düzeltme kapının kendisinde: argv'yi temizlemek, alt sürece `PYTHONIOENCODING=utf-8`
vermek, betiğin dizinini `sys.path`'e eklemek. **Yapılmadı.**

### 4.4 Duran kapılara eklendi mi — ❌ YAPILMADI

Level-1 kapısı elle çağrılıyor (`python diagnostics/level1_gate.py`). Duran bir tetiğe
(ihraç öncesi kanca ya da runbook adımı) **bağlanmadı**.

---

## 5. Runbook ve Zenodo

### 5.1 Adım listesi — ✅ KAPANDI

`0` güvenlik kapısı · `1` ihracı dondur · **`1b` içeriği üret (`public_repo_sync.py`)** ·
**`1c` üç doğrulama kapısı** · `2` tek final commit · `3` yetkiyi ver · `4` sil ·
`5` yeniden kur · `6` commit'i it · `7` doğrula · `8` public'e çevir ·
**`8b` Zenodo DOI** · `9` yetkiyi geri al · `10` URL'i makaleye işle.

1b ve 1c mevcut (satır 61 ve 87).

### 5.2 Zamanlama kutusu — ✅ KAPANDI (satır 171)

> ## ⏱ SIRA DEĞİŞTİ (8 Ağu kararı): bu dizi GÖNDERİM GÜNÜNDE DEĞİL, **1–2 GÜN ÖNCE** koşar
>
> **Gönderimden 1–2 gün önce:** adım 0 → 8b'nin tamamı … **Gönderim günü:** yalnız EM
> yüklemesi. Depo işi yok.
>
> Gerekçe: DOI ancak Release'te doğuyor ve depo public olmadan Zenodo göremiyor. Bunu
> gönderim gününe sıkıştırmak, **webhook'un basınç altında ilk kez denenmesi** demekti.

Ayrıca `yerel kopya` satırı **güncellendi**: artık
`public\calibration-law-fer_2026-08-08`. Eski klasör geri dönüş noktası olarak duruyor.

### 5.3 Zenodo Yol A — ✅ KAPANDI, **çelişki bulundu ve düzeltildi**

Runbook iki yeri birbiriyle çelişiyordu:

- satır ~196: **"KARAR (8 Ağu): Yol A"**
- satır ~211: **"Yol B — elle yükleme (ÖNERİLEN)"**
- altındaki kutu: **"Karar Fatih'in"**

"ÖNERİLEN", çözümlenmeyen-DOI tuzağı ölçülmeden önce yazılmıştı; tuzak belirleyici olunca
karar A'ya döndü ama başlık güncellenmemişti. **Gönderim günü çelişkili bir runbook okunur.**
Düzeltildi: Yol B artık "DEĞERLENDİRİLDİ, SEÇİLMEDİ" ve kutu "KARAR VERİLDİ: Yol A".

**Eksik olan üç şey eklendi** — istenen üç konum runbook'ta hiç yazılı değildi:

| # | konum | ne yazılır |
|---|---|---|
| 1 | Veri/kod erişilebilirlik beyanı | Zenodo DOI + GitHub URL |
| 2 | Kapak mektubu | Zenodo DOI, "kod ve ön-beyan kayıtları" ibaresiyle |
| 3 | **§Conclusion** | Zenodo DOI, yeniden üretilebilirlik cümlesi içinde |

**DOI ne zaman doğar:** her GitHub **Release**'te (bağlantı kurulunca değil). Ön-rezervasyon
GitHub entegrasyonuyla mümkün değil (Zenodo FAQ, birebir).
**Nerede doğrulanır:** `https://doi.org/<DOI>` tarayıcıda açılıp Zenodo kaydına düştüğü
görülerek — **üç konuma yazmadan önce**.

---

## 6. Makale tarafına düşenler

### 6.1 HEADLINE_2 — ✅ KAPANDI, iki depoda aynı

```
diagnostics/graphical_abstract.py:55
HEADLINE_2 = "— dose–response at fixed teacher accuracy, in both directions —"
```

Her iki depoda **aynı satır, aynı metin**. (`2026-08-07_figur_iddia_v2.md:23` daha eski bir
hâli kaydediyor — tarihli kayıt, canlı değer değil.)

### 6.2 Eski iddia cümlesi — ✅ KAPANDI, ama **bir canlı geçiş var**

`grep -rn "calibration governs"`:

| depo | dosya | tür |
|---|---|---|
| poster-var | 8 dosya | 7'si tarihli kayıt ya da bu dizeyi **arayan** meta betik |
| poster-var | **`ferplus_dose_response_queue.ps1:17`** | ⚠️ **canlı** |
| public (tarihli) | 5 dosya | 4'ü tarihli kayıt |
| public (tarihli) | **`ferplus_dose_response_queue.ps1:17`** | ⚠️ **canlı** |

Tek canlı geçiş, iki depoda da aynı satır:

```powershell
# B-007 (teacher calibration governs student calibration; headroom bounds what any mechanism can
# win) is currently RAF-DB-only. This is the external-validity test.
```

Bu bir başlık değil, bir kuyruk dosyasının yorumunda **B-007 iddiasının prosa tekrarı**.
Yayımlanacak bir dosyada duruyor. **Değiştirilmedi** — karar senin: yorumu yeni iddia
cümlesiyle güncelle ya da tarihli-gerekçe olarak bırak.

### 6.3 ρ işaret konvansiyonu — ✅ KAPANDI

`paper_tables/perclass_crossing.md` **iki biçimi de adıyla** yazıyor:

- satır 28: **ρ(n, T_cross) = −0.900** — "negatif işaret *sık sınıf ERKEN kesiyor* demek,
  yani iddianın yönü"
- satır 29: ρ(seyreklik sırası, T_cross) = +0.900 — "aynı ilişki, ters eksen"

Daha önce +0.900'ün "frekans" diye etiketlenmesi hatası düzeltilmiş durumda.

### 6.4 `[final,5p]` sayfa sayısı — ❌ BU MAKİNEDE ÖLÇÜLEMEZ

LaTeX kurulu değil. Sayı **Mac'te** derlenerek ölçülmeli. 28 bekleniyor; A12'nin metne
getirdiği değişiklikler (özet cümlesi + FPR 0.389→0.454 + A12 paragrafı) sayfa sayısını
etkileyebilir.

---

## 7. Kapanış ihracı

### 7.1 A12 sonrası yeniden üretilenler — ✅ KAPANDI

| artefakt | ölçüm |
|---|---|
| `criterion_applied` hücre sayısı | **12 → 17** |
| **aile-bazlı yanlış pozitif oranı** | **0.3892 → 0.4540** |
| gözlenen k medyanı | 1.7487 → 1.6956 |
| hücre-başı FPR | 0.0402 → 0.0350 |
| `denominator_table` | üretildi — logit_std: stage1 58×/77×, primary 55×/57×, vae9182 89×/69× |
| `section54_numbers` | üretildi — B3 iskeleti **17 satır n=3**, 4 tek-tohum, 0 düşen |
| `holm_family` | üretildi — en küçük p_holm 0.0011, en büyük 0.1339 |
| `noise_units` | üretildi — dokuz hücre medyan 27.3×, ortalama 51.7×, min 2.6× |
| `RESULTS_TABLES.md` | üretildi — **429 satır** |
| `runs.csv` | **196 koşu**, A12=10 · A13=1 blok beyanlı |
| `selection_audit_unfrozen.csv` | 196 koşu, **575 ölçüm** |

### 7.2 Donmuş `selection_audit.csv` değişmedi — ✅ KAPANDI

| kanıt | değer |
|---|---|
| `git status --porcelain <dosya>` | **boş** → değişmemiş |
| mtime | **2026-08-01 04:14:34** (A12'nin ilk koşusundan 6 gün önce) |
| satır / tekil koşu | 380 / **131** |
| sha256 (çalışma kopyası) | `2645d8b352bdd6174fcc8a71acf43c7a6f846cda1b82ff096402dbc33a8b1068` |

> **Not, yanlış okumayı önlemek için:** `git show HEAD:<dosya>` farklı bir sha veriyor
> (`de5502ae…`) — bu içerik farkı **değil**, git'in CRLF↔LF normalizasyonu. Değişmezlik
> kanıtı `git status`'un boş dönmesi ve mtime'dır.
>
> Öncesi/sonrası sha karşılaştırması **yapılamadı**: dosyanın kayıtlı bir sha'sı hiçbir yerde
> tutulmuyor. Yerine git kullanıldı, ki daha güçlü. **Öneri:** donmuş dosyanın sha256'sı bir
> manifest'e yazılsın; git dışı bir kopya taşındığında git kanıtı kaybolur.

### 7.3 Tablo kapısı — ⛔ **MOVED > 0 → DUR**

| kalem | değer |
|---|---|
| karşılaştırılan hücre | **780** (temelde de 780) |
| n CHANGED | **12** |
| **MOVED** | **1** |
| APPEARED | 0 |
| VANISHED | 0 |

- 10 × n CHANGED: beş A12 hücresi × iki oran (`ratio_ctrl`, `ratio_paired`), n **1→3**
- 2 × n CHANGED: `G3.2/family_wise` (12→17), `G3.2/k_observed_median`
- 1 × MOVED: `G3.2/per_cell_fpr` 0.0402 → 0.0350, tolerans 0.0007

MOVED bağımsız bir kayma **değil**: hücre-başı FPR gözlenen k medyanında değerlendiriliyor,
medyan da aile 12→17 büyüdüğü için indi. Aynı n değişiminin türevi.

**Kural gereği ihraç edilmedi. Temel kabulü Fatih'in onayını bekliyor.**

> **Yol boyunca kapının kendisinde bir hata bulundu.** Değeri `None` olan bir hücreyi
> biçimlendirirken `TypeError` ile ölüyordu — hem rapor hem konsol yolunda. Bir
> durdurma-kapısının en kötü arıza biçimi "sapma yok" değil, **"kapı koşamıyor"**dur.
> Düzeltildi: `None` artık `—` basılıyor.

### 7.4 `PREREGISTRATIONS.md` sonuç satırları — ⚠️ KISMİ (A12 ✅ / A13 ⏳)

**A12 satırı (dolduruldu):**

> **HİÇBİR HÜCRE ÖLÇÜTÜ KARŞILAMADI** — 5 hücre × 2 eksen = 10 hükmün onu da ÇÖZÜNMEDİ.
> Üç tahminin üçü de tuttu; cümle *"başarısız"*tan **"n=3'te kurulamadı"**a çevrilir.

Ayrıntı bölümü de eklendi; içinde en önemli sayı: `stage1 × target_logvar` ΔECE **3/3
tohumda aynı işaret** (`---`) ve oran **1.965×**, eşik 2.0 — **barın %1.74'ü kadar eksik**,
ve yön **kalibrasyon faydası**. Geçseydi beyandaki yanlışlayıcı tetiklenirdi. Bu hücre
metinde "etkisiz" diye anılamaz.

**A13 satırı: ⏳ bekliyor.** A13 şu an **1/4** — `w100ns/T170/seed42` bitti,
`seed1` epoch 265/400, `T220` çifti başlamadı.

### 7.5 Tam ihraç — ⏳ **BEKLİYOR**

7.3 durdu, ihraç yapılmadı. MANIFEST sayısı ve defter sha256 o adımda üretilecek.
`runs.csv` sha256 (şimdiki): `51d551fd86bef626dfc008817f979571041df8150ef9c307f9d3f89139fd465a`.

---

## Özet

**Kapanan: 17 madde** — 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2.1, 4.3, 5.1, 5.2, 5.3, 6.1, 6.2,
6.3, 7.1, 7.2, 7.3.

**Bekleyen: 4 madde** — 4.1 (A12 sonrasına bırakıldı, bilinçli), 6.4 (LaTeX bu makinede
yok, Mac'te ölçülecek), 7.4 (A13 yarısı), 7.5 (7.3 durdurdu).

**Sorunlu: 5 madde** — 2.2 ve 2.3 (36 dosyada mutlak yol; 19 config'in veri kökü için
konvansiyon kararı gerekiyor, 27 onaylı aday bu yüzden yazılamadı), 3.1 (50 kırık atıf,
9'u yayımlanmayan `tests/`'e), 4.2 (13 Level-1 ihlali düzeltilmedi), 4.4 (kapı duran bir
tetiğe bağlanmadı).

---

## Ek — A13 aynı gün bitti (19:11), 7.3/7.4 güncellendi

Rapor yazıldığında A13 1/4'teydi. Aynı akşam 4/4 bitti ve kapanış koşuldu. **Yukarıdaki
satırlar o anın gerçeği olarak duruyor**; değişenler burada:

**7.4 → ✅ İKİ SATIR DA DOLU.** A13 sonucu: **BAŞLATMA TAHMİNİ YANLIŞLANDI** — eğim
başlatmaya duyarlı (Δeğim −0.0672, birleşik zarf 0.0358 → çözülür). Ayrışım beklenenin
tersini gösterdi: B4'ün confound'lu farkı (+0.0614) tek başına çözülmüyordu, ama başlatma
bileşeni tek başına çözülüyor ve kapasite bileşeni sıfıra yakın (−0.0059). Yanlışlayıcı
tetiklendi, dolayısıyla §5'in *"yasa öğrenci artefaktı değil"* savunması **başlatma
ekseninde de** savunulmak zorunda. Dayanak: üç kolun üçünde de R² > 0.998, eğimler
0.649–0.716 — başlatma **katsayıyı** oynatıyor, yasanın varlığını değil.

**G4.2 üretildi** (`paper_tables/g42_init_matched_lever.{md,json}`, yeni betik). Kaldıraç
oranı başlatma-eşleştirilmiş hâliyle: @swa **76× → 69×**, @best 79× → 75×, @last 27× → 26×.
Ortak payda, yön aşağı, mertebe korunuyor. Confound'lu oran silinmedi.

**7.3 yeniden koşuldu ve KAPSAMI BÜYÜDÜ.** A12/A13 hükümleri ile G4.2 `SOURCES`'a
**kaydedilmemişti** — G4'teki boşluğun aynısı: yayımlanan ama kapının okumadığı artefakt.
Üçü de kaydedildi.

| kalem | önce | sonra |
|---|---|---|
| karşılaştırılan hücre | 780 | **885** |
| APPEARED | 0 | **105** |
| n CHANGED | 12 | **42** |
| **MOVED** | 1 | **1** (aynı hücre) |
| VANISHED | 0 | 0 |

Tek MOVED yine `G3.2/per_cell_fpr` 0.0402 → 0.0350 — ailenin 12→17 büyümesiyle kayan k
medyanının türevi. **Hâlâ MOVED > 0, hâlâ ihraç yok.**

**7.2 yeniden doğrulandı:** donmuş `selection_audit.csv` A13'ten sonra da birebir aynı —
sha256 `2645d8b352bdd6174fcc8a71acf43c7a6f846cda1b82ff096402dbc33a8b1068`, mtime
2026-08-01 04:14:34, `git status` boş.

**Özet farkı:** kapanan 17 → **18** (7.4 kapandı), bekleyen 4 → **3** (4.1, 6.4, 7.5).
Sorunlu 5 değişmedi.

---

Üretici: elle yazıldı; ölçümlerin kaynağı `diagnostics/reports/public_scope_buckets.md`,
`public_repo_sync_dryrun.md`, `level1_gate.md`, `table_diff_gate/last_diff.md`,
`a12_realsignal_gate/a12_verdict.md`.
