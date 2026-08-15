# Final devir — 8 Ağustos 2026

> **Yöntem.** Her satırda ölçümün kendisi var. Yapılmayana **YAPILMADI** dendi. Kısmi
> başarı ayrıca işaretlendi. Bu turda iki gerçek tutarsızlık bulundu ve ikisi de raporda
> duruyor: bandın 100 dosyalık bayatlık uyarısının nasıl çürütüldüğü (§7) ve tarihli public
> klasöründe kapının reddettiği 27 dosyanın durduğu (§7, **çözülmedi**).

---

## 1. A13 hükmü — tam metin

**HÜKÜM: BAŞLATMA TAHMİNİ YANLIŞLANDI — eğim başlatmaya duyarlı.**
T10a (ii) sonuçsuz kalıyor, ama artık *confound* yüzünden değil *gürültü* yüzünden.

### Üç eğim (@swa, aynı üç sıcaklık)

| kol | başlatma | kapasite | eğim b | R² | en büyük artık | tohum-gürültüsü zarfı |
|---|---|---|---|---|---|---|
| `w050` | scratch | 0.712 M | **0.6547** | 0.99996 | +0.00057 | ±0.0585 |
| `2248 ön-eğitimli` | **ön-eğitimli** | 2.248 M | **0.7161** | 0.99997 | +0.00058 | ±0.0219 |
| `w100ns` | **scratch** | 2.248 M | **0.6488** | 0.99882 | **−0.00319** | ±0.0139 |

Artıklar öğretmen ECE'sine göre fit'ten sapma olarak hesaplandı (T = 1.0 / 1.7 / 2.2 →
öğretmen ECE 0.0136 / 0.1454 / 0.2622). A13'ün yeni kolu en büyük artığa sahip (−0.0032)
ama en küçük zarfa (±0.0139) — üç noktası da en dar saçılımlı.

### B4'ün iki şartı, ayrı ayrı

| şart | durum | kanıt |
|---|---|---|
| (i) fit desteği üç kolda da **aynı üç sıcaklık** | ✅ | T = 1.0 / 1.7 / 2.2; `shared_support` alanı JSON'da beyanlı, 5-noktalı fit'e karşı 3-noktalı fit konmadı |
| (ii) belirsizlik **"zarf, güven aralığı DEĞİL"** etiketli | ✅ | hüküm metninde birebir: *"Zarf bir güven aralığı DEĞİLDİR. İki hücrede n=2, tek serbestlik derecesi."* |

### Üç karşılaştırma

| karşılaştırma | izole ettiği | Δb | birleşik zarf | çözünüyor mu |
|---|---|---|---|---|
| `scratch2248` vs `pretrained2248` | **BAŞLATMA** | **−0.0672** | ±0.0358 | ✅ **evet** |
| `scratch2248` vs `scratch0712` | KAPASİTE | −0.0059 | ±0.0724 | ❌ hayır |
| `pretrained2248` vs `scratch0712` | ikisi birden (B4'ün confound'lu hâli) | +0.0614 | ±0.0804 | ❌ hayır |

### Hüküm cümlesi: karışıklık **AYRIŞTI**

Kapasite–başlatma karışıklığı ayrıştı — ama beklenen yönde değil. B4'ün confound'lu
karşılaştırması (+0.0614) **tek başına çözünmüyordu**. Ayrıştırınca görülüyor ki **başlatma
bileşeni tek başına çözünüyor** (0.0672 > 0.0358) ve **kapasite bileşeni sıfıra yakın**
(−0.0059, zarfın on ikide biri). Yani B4'ün gördüğü farkın kaynağı kapasite değil başlatma.

### Ön-beyandaki hangi sonuç-cümlesi gerçekleşti

İki tanesi, ikisi de A13 bloğunun metniyle birebir:

1. **Yanlışlayıcı açıldı** — *"`|b_scratch2248 − b_pretrained2248|` iki zarfın toplamını
   aşarsa, yasanın eğimi başlatmaya duyarlıdır ve §5'teki 'yasa öğrenci artefaktı değil'
   savunması **başlatma ekseninde de** ayrıca savunulmak zorunda kalır."*
2. **T10a için üçüncü cümle açıldı** — *"Çıkmazsa (ii) sonuçsuz kalır — ama artık *confound
   yüzünden* değil, *gürültü yüzünden*; bu, aynı hükmün daha dürüst bir gerekçesidir ve öyle
   yazılır."*

**Yazılmayan cümle:** *"eğim kapasiteyle değişmiyor"* — beyanda yasaklıydı, zarf bir
eşdeğerlik testi değil. Yazılmadı.

### Hücre envanteri (scratch kolu)

| kapasite | T | öğretmen ECE | n | öğrenci ECE ort | sd | tohumlar |
|---|---|---|---|---|---|---|
| 0.712 M (`w050`) | 1.0 | 0.0136 | 3 | 0.0365 | 0.0057 | [1, 42, 43] |
| 0.712 M (`w050`) | 1.7 | 0.1454 | 2 | 0.1236 | 0.0040 | [1, 42] |
| 0.712 M (`w050`) | 2.2 | 0.2622 | 2 | 0.1992 | 0.0087 | [1, 42] |
| 1.380 M (`w075`) | 1.0 | 0.0136 | 3 | 0.0388 | 0.0042 | [1, 42, 43] |
| **2.248 M (`w100ns`)** | 1.0 | 0.0136 | 3 | 0.0374 | 0.0030 | [1, 42, 43] |
| **2.248 M (`w100ns`)** | 1.7 | 0.1454 | 2 | 0.1183 | 0.0011 | [1, 42] |
| **2.248 M (`w100ns`)** | 2.2 | 0.2622 | 2 | 0.1989 | 0.0003 | [1, 42] |

**Tohum tekilliği kapısı: geçildi.** Hiçbir hücrede aynı tohumdan iki koşu yok. Olsaydı
hüküm `RuntimeError` ile durur, çünkü tekrar hücrede tohum dışında bir değişkenin de
oynadığı anlamına gelirdi.

### Makalede hangi ifade değişmeli — benim yazdığım

**T10a, item (ii):** *"INCONCLUSIVE"* **kalıyor**, gerekçesi değişiyor. Şu anda confound'a
işaret ediyor; artık *"the capacity and initialization axes were separated (A13, 4 runs); the
capacity contrast remains inconclusive at the seed-noise envelope (Δb = −0.006, envelope
±0.072), i.e. for noise rather than for confounding"* demeli.

**§5, kapasite paragrafı:** *"yasa öğrenci artefaktı değil"* savunması **başlatma ekseninde
de** kurulmalı. Dayanak hazır ve ölçülü: üç kolun **üçünde de** doz-yanıtı R² > 0.998 ile
duruyor, eğimler 0.649 / 0.716 / 0.649 aralığında. Başlatma **katsayıyı** 0.067 oynatıyor
(0.716'nın %9.4'ü), yasanın **varlığını ya da işaretini** değil. Yani cümle "başlatmadan
bağımsız" değil, **"başlatma katsayıyı ölçülebilir biçimde oynatıyor, yasayı değil"** olmalı.

---

## 2. A12 — 5 hücre × 2 eksen (tablo)

@swa. Bar = o kolun **kendi** `cw=none` kontrolünün aynı metrikteki tohum sd'si; eşik 2.0.

| hücre | AUROC | eksen | ortalama eşleştirilmiş fark | işaretler | 2×bar | oran | hüküm |
|---|---|---|---|---|---|---|---|
| stage1 × `mean_logvar` | — | ΔECE | −0.00117 | `+--` | 0.00422 | 0.55× | ÇÖZÜNMEDİ |
| stage1 × `mean_logvar` | — | Δacc | −0.0978 pp | `---` | 0.1992 | 0.98× | ÇÖZÜNMEDİ |
| **stage1 × `target_logvar`** | **0.70** | **ΔECE** | **−0.00415** | **`---`** | **0.00422** | **1.965×** | ÇÖZÜNMEDİ |
| stage1 × `target_logvar` | 0.70 | Δacc | +0.2499 pp | `++-` | 0.1992 | **2.509×** | ÇÖZÜNMEDİ |
| primary × `mean_logvar` | — | ΔECE | −0.00558 | `--+` | 0.00666 | 1.67× | ÇÖZÜNMEDİ |
| primary × `mean_logvar` | — | Δacc | +0.1956 pp | `++-` | 0.7886 | 0.50× | ÇÖZÜNMEDİ |
| **primary × `target_logvar`** | **0.84** | ΔECE | −0.00078 | `+--` | 0.00666 | **0.235×** | ÇÖZÜNMEDİ |
| primary × `target_logvar` | 0.84 | Δacc | −0.0869 pp | `-+-` | 0.7886 | 0.220× | ÇÖZÜNMEDİ |
| vae9182 × `mean_logvar` | 0.46 | ΔECE | +0.00148 | `+--` | 0.00540 | 0.55× | ÇÖZÜNMEDİ |
| vae9182 × `mean_logvar` | 0.46 | Δacc | −0.2716 pp | `-++` | 0.4140 | 1.31× | ÇÖZÜNMEDİ |

**İki hücre ölçütün iki koşulundan tam birini sağlayıp diğerinde düştü:**
`stage1 × target_logvar` ΔECE'de 3/3 aynı işaret ama 1.965× (barın %1.74'ü eksik,
|ortalama| 0.00415 vs 2×bar 0.00422); aynı hücre doğrulukta 2.509× ile barın üstünde ama
işaretler `++-`.

### Yorumum (tablodan ayrı) — sinyal-kalitesi örüntüsü YOK, yakınlık tesadüf

Senin koyduğun ölçütü uyguladım: *"daha iyi sinyalli hücre (primary) uzakta kaldıysa örüntü
yok."*

| hücre | sinyalin ölçülmüş AUROC'u | ΔECE oranı | bara uzaklık |
|---|---|---|---|
| primary × `target_logvar` | **0.84** (en iyi) | **0.235×** | **beşin en uzağı** |
| stage1 × `target_logvar` | 0.70 | 1.965× | beşin en yakını |
| vae9182 × `mean_logvar` | 0.46 (en kötü) | 0.55× | ortada |

**En iyi sinyalli hücre barın en uzağında, ikinci en iyi sinyalli hücre en yakınında.**
İlişki yok; olsa olsa **ters**. Dolayısıyla `stage1 × target_logvar`'ın 1.965×'e gelmesi bir
sinyal-kalitesi örüntüsü değil, üç tohumun bu hücrede aynı yöne düşmesiyle oluşan bir
yakınlık.

**Ama "gürültü" deyip geçilemez, iki sebeple.** (a) İşaretler 3/3 aynı yönde ve yön
**kalibrasyon faydası** (ECE düşüyor) — geçseydi beyandaki yanlışlayıcı tetiklenirdi.
(b) Bar, tek bir kolun tohum gürültüsünün iki katıdır; barın %98'ine ulaşan bir etki
*ölçülemedi* demektir, *yoktur* demek değil. Metinde önerdiğim ifade: mekanizma n=3'te
kurulamadı; en güçlü gerçek sinyal barın %98'ine ulaştı ve yönü fayda idi; bu hücre
"etkisiz" diye anılmayacak. **Sinyal kalitesi ile yakınlık arasında bir örüntü ölçülmedi**
(üç AUROC ile zaten sınanamaz).

---

## 3. Aile ve ölçüt — makalede yazılı sayılar

### `criterion_applied`

| kalem | değer |
|---|---|
| sözlükteki hücre | **21** |
| **FPR ailesindeki hücre (n=3)** | **12 → 17** |
| tek-tohum (hüküm verilmeyen, `n/a`) | 4 |

**@swa ΔECE hüküm dağılımı:** **5 kurulmuş · 12 çözünmemiş · 4 n/a.**
"Sınırda" ayrı bir kategori olarak üretilmiyor — ölçüt ikili (kurulmuş / çözünmemiş) ve
sınırdakiler oranıyla görünür (en yakın: `stage1/gate:target_logvar` 1.97, eşik 2.0).

### Yanlış pozitif oranı — teyit

| kalem | eski | **yeni** |
|---|---|---|
| aile-bazlı üst sınır | 0.3892 | **0.45405** |
| gözlenen k medyanı | 1.7487 | **1.69559** |
| hücre-başı FPR (gözlenen k'da) | 0.0402 | **0.034975** |
| aile büyüklüğü | 12 | **17** |

Simülasyon: 200 000 tekrar, `rng_seed` 20260806. k'ya göre FPR: 0.5→0.0000, 1.0→0.000505,
1.41→0.01303, 2.0→0.066015, 3.0→0.15225. Gözlenen k aralığı [0.2997, 3.8292].

### Kurulmuş hücrelerin oranları — **56–77× korunuyor, ama yalnız `logit_std` için**

| hücre | oran | işaret |
|---|---|---|
| `stage1/logit_std` | **76.62×** | `+++` |
| `vae9182/logit_std` | **69.49×** | `+++` |
| `primary/logit_std` | **56.68×** | `+++` |
| `stage1/g2g_kl` | 3.57× | `---` |
| `vae9182/gate:oracle_error` | 2.08× | `+++` |

**56.68–76.62 → "56–77×" aralığı aynen duruyor.** Ama dikkat: kurulmuş beş hücrenin
**ikisi bu aralığın çok altında** (3.57 ve 2.08). Aralık `logit_std` üçlüsünü tarif ediyor,
"kurulmuş hücreler"i değil; metinde bu ayrım yapılmalı, yoksa okur beş hücrenin hepsinin
56×'in üstünde olduğunu sanır.

### `denominator_table` — iki konvansiyon yan yana

| öğretmen | ΔECE | havuz paydası | kendi-kolu paydası |
|---|---|---|---|
| stage1 | +0.0906 | 58× | **77×** |
| primary | +0.0859 | 55× | 57× |
| vae9182 | +0.1388 | 89× | 69× |

### `section54_numbers` — tek-tohum listesi

**B3 iskeleti: 17 satır n=3, 4 tek-tohum, 0 düşen.** Tek-tohum kalanlar `ctkd` üçlüsü
(stage1/primary/vae9182) ve `vae9182/g2g_kl+adaptive_t`. A12 gate hücrelerini n=3'e çıkardı,
dolayısıyla tek-tohum listesi 9'dan 4'e indi.

Diğer §5.4 sayıları: (ii) gate vs **temiz** kontrol +0.0056 ± 0.0040 `[+++]`, (iii) gate vs
**kirlenmiş** kontrol +0.0004 ± 0.0011 `[+-+]`, kimlik artığı −2.7e−19.

### `noise_units` — **23× tabanı duruyor**

Dokuz hücre (kendi paydası): 2.6 / 2.8 / 6.1 / **23.5** / 27.3 / 32.3 / 43.2 / 114.3 / 213.0
→ medyan **27.3×**, ortalama 51.7×, min **2.6×**, max 213.0×.
Sorduğun 23× tabanı `swa|primary` hücresi = **23.5×**, yerinde.

Havuz paydasıyla @swa: stage1 47.57 · primary 32.67 · vae9182 139.13 → medyan 47.57,
**ortalama 73.12**, min 32.67. Makalenin "tipik 77" ifadesinin kaynağı bu havuz ortalaması;
*"hiçbir zaman 55'in altına inmiyor"* **iki konvansiyonda da yanlış** (kendi paydası min 2.6,
havuz min 32.7).

---

## 4. G4 kalanları

### G4.2 — kaldıraç oranı, başlatma eşleştirilmiş ✅ (A13'ü bekliyordu)

| ckpt | kapasite açıklığı (ortak payda) | sıcaklık açıklığı — ön-eğitimli | oran (yayımlanan) | sıcaklık açıklığı — **scratch** | oran (**başlatma-eşleştirilmiş**) |
|---|---|---|---|---|---|
| **@swa** | 0.00235 | 0.1780 | 76× | **0.1615** | **69×** |
| @best | 0.00254 | 0.2010 | 79× | 0.1898 | 75× |
| @last | 0.00743 | 0.1974 | 27× | 0.1955 | 26× |

Payda üç satırda da ortak; değişen yalnız sıcaklık kolunun başlatması. **Yön aşağı, mertebe
korunuyor** — sıcaklık ekseni kapasite ekseninden hâlâ iki mertebe geniş. *"Yasa öğretmen
tarafında yaşıyor"* cümlesi ayakta, sayısı **69×** olmalı. Confound'lu oran silinmedi, kendi
sütununda duruyor (beyanda öyle yazılmıştı).

Üretici: `diagnostics/g42_init_matched_lever.py` (yeni). Hücre üyeliği ve donmamış denetim
yolu A13'ten **ithal**, kapasite açıklığı `RESULTS_TABLES.json`'dan **okunuyor** — iki yerde
ayrı hesaplanan bir payda birbirinden sessizce kayabilirdi.

### Asimetri estimand'ı — "1.7–1.9×" kararı

Altı karşılaştırma, mutlak oran (@swa, 20 000 bootstrap, `rng_seed` 20260807):

| kol / idx | mutlak oran | %95 CI | ekstrapolasyon? | CI 1'i içeriyor mu |
|---|---|---|---|---|
| rafdb_stage1 / 0 | 2.25 | [1.41, 4.53] | ✅ evet | hayır |
| rafdb_stage1 / 1 | 1.88 | [1.55, 2.38] | ✅ evet | hayır |
| **rafdb_stage1 / 2** | **1.77** | **[1.50, 2.13]** | ❌ **hayır** | hayır |
| rafdb_vae9182 / 0 | 1.33 | [0.89, 2.19] | ✅ evet | **EVET** |
| rafdb_vae9182 / 1 | 1.13 | [0.90, 1.46] | ✅ evet | **EVET** |
| **ferplus / 0** | **2.04** | **[1.64, 2.48]** | ❌ **hayır** | hayır |

- **Altısının ortalaması: 1.735 ± 0.429** (sd, altı sayı üzerinden)
- **Ekstrapolasyonsuz ikisi: 1.905 ± 0.191** — ve buradaki ± bir **CI DEĞİL**, iki sayının
  sd'si. n=2 ile belirsizlik iddiası kurulamaz.

**Kararım ve gerekçesi.** Makaleye **tek sayı değil, iki estimand arasındaki aralık** yazın:
*"1.7–1.9×"* zaten bu iki okumayı kapsıyor ve ikisini de saklamıyor. İddianın **dayanağı**
ise ekstrapolasyonsuz iki karşılaştırmanın **bootstrap CI'ları** olmalı — [1.50, 2.13] ve
[1.64, 2.48] — çünkü (a) ölçülen destek dışına çıkmıyorlar, (b) ikisi de 1'i dışlıyor, (c)
n=2'nin sd'si değil gerçek belirsizlik ifadesi onlar.

**Bunu saklamayın:** `vae9182` kolunun **iki karşılaştırmasının da CI'ı 1'i içeriyor** — o
kolda asimetri **saptanamadı**. Cümle "üç öğretmende de asimetri var" diye yazılamaz;
"iki kolda saptandı, iyi kalibre kolda saptanamadı" diye yazılmalı. Estimand B
(optimum-üstü fazla) **kullanılmıyor**: altı karşılaştırmanın üçünde tanımsız ve CI'ları
[1.05, 543] gibi aralıklara yayılıyor.

### Denetim popülasyonu (G4.6) — son hâl

| kalem | değer |
|---|---|
| denetimdeki koşu | **131** (donmuş) |
| standart tarif dışı | **28 (%21.4)** |
| örüntü: `epochs` + `swa_start` | 16 |
| örüntü: yalnız `epochs` | 9 |
| örüntü: `epochs` + `swa_start` + `kd_temperature` | 2 |
| örüntü: `epochs` + `swa_start` + `alpha` | 1 |

Standart tarif: `epochs 400, swa_start 200, alpha 0.3, kd_temperature 6.0`. **28'inin tamamı
`epochs`'ta farklı** — yani "az sayıda legacy koşu" ifadesi %21'i tarif ediyor ve makalede
sayıyla yazılmalı.

### Gürültü-birimi tablosu (G4.5) — son hâl

Yukarıda §3'te. Dokuz hücre medyan 27.3×, havuz @swa ortalama 73.12×.

---

## 5. Dünkü kontrol turunun sorunlu beş maddesi

| # | ne çözülmedi | engel | kapanması ne gerektiriyor |
|---|---|---|---|
| **2.2** | 19 config'in veri kökü hâlâ yabancı makineleri gösteriyor (`C:/datasets`, `D:/lg`, `D:/27may`, `D:/Veriseti`) | `*/poster-var/<kuyruk>` biçimi mekanik çevrilebilir ama `C:/datasets/X → data/X` eşlemesi **depoda karşılığı olmayan bir dizin adı uydurmak**; konvansiyon kararı senin | Tek cümlelik karar: yabancı veri kökleri `data/<son bileşen>`e mi çevrilsin, yoksa `<VERI_KOKU>/…` gibi bir yer tutucuya mı |
| **2.3** | Mutlak-yol kapısı **0 değil, 36** | 2.2'nin kararı | 2.2 kapanınca 26 dosya dönüşür; kalan 10'u ya üçüncü taraf (5, beyanlı muaf) ya tarihli rapor |
| **3.1** | **50 kırık atıf**, en önemlisi 9 tanesi yayımlanmayan `tests/`'e (iki B belgesi ona atıf yapıyor) | `tests/` kapsam dışı; ayrıca `reference_90_74/config.json` bilinen kırık işaret | `tests/` A'ya alınsın (küçük, "çalışan kod" vaadini destekliyor) + `run_phase0_rafdb_ce9241_diagnostic.ps1:18`'deki ölü işaret ya silinsin ya yorum yapılsın |
| **4.2** | **13 Level-1 ihlali** düzeltilmedi (geçti 20 · İHLAL 13 · muaf 6 · başka hata 8) | Sekizinin kök nedeni tek: `t5_pairing_diff.gate_variant()` koşu dizini okuyor | Gate sinyalini deftere sütun olarak eklemek (§6) → sekizi birden düşer; kalan 5 tek tek |
| **4.4** | Level-1 kapısı duran bir tetiğe bağlanmadı | Karar yok, iş küçük | Runbook adım 1c'ye üçüncü kapı olarak yazılması (zaten orada iki kapı var) |

---

## 6. Level-1 defter sütunu

**YAPILMADI — A12/A13 sonrasına bırakıldı.**

**Karışmadığının kanıtı:** tablo kapısının kabul edilen temel gerekçesi yalnız A12, A13 ve
G4.2'yi adlandırıyor; 105 APPEARED hücresinin tamamı bu üç artefaktın `SOURCES`'a ilk kaydı
(`A12/…`, `A13/…`, `G4.2/…` önekleri). Defter sütunundan gelen tek bir hücre yok. Yani iki
değişiklik birbirine karışmadı; sütun eklendiğinde onun tek başına **0 sapma** vermesi
beklenir ve o zaman ayrıca ölçülmeli.

---

## 7. Kapanış ihracı

### Yeniden üretilenler

**A12/A13 kapanışı için:** `selection_audit_table --ignore-cutoff` (199 koşu, 575→ güncel
ölçüm), `build_runs_ledger` (199 koşu), `a12_realsignal_verdict`, `a13_scratch_dose_verdict`,
`g42_init_matched_lever` (**yeni**), `t5_pairing_diff`, `criterion_applied`, `holm_family`,
`denominator_table`, `section54_numbers`, `noise_units`, `paper_tables` (RESULTS_TABLES,
429 satır).

**Bayatlık uyarısını çürütmek için ayrıca:** `efficiency_retention`, `inferential_tests`,
`p5_oracle_replication_verdict`, `p6_verdict`, `capacity_law_check`,
`control_grid_refinement`, `asymmetry_estimand`, `audit_population`.

### Donmuş `selection_audit.csv` — öncesi = sonrası

| kalem | değer |
|---|---|
| sha256 (A12'den önce, A13'ten sonra — **aynı**) | `2645d8b352bdd6174fcc8a71acf43c7a6f846cda1b82ff096402dbc33a8b1068` |
| mtime | **2026-08-01 04:14:34** |
| `git status --porcelain` | **boş** |
| satır / tekil koşu | 380 / **131** |

> `git show HEAD:<dosya>` farklı bir sha verir (`de5502ae…`) — bu içerik farkı **değil**,
> git'in CRLF↔LF normalizasyonu. Değişmezlik kanıtı `git status`'un boşluğu ve mtime'dır.

### Tablo kapısı

| kalem | değer |
|---|---|
| hücre | **885** (öncesi 780) |
| **APPEARED** | **105** |
| **MOVED** | **1** |
| **VANISHED** | **0** |
| n CHANGED | 42 |

**Her MOVED için tek satırlık gerekçe:**

- `G3.2/per_cell_fpr` **0.0402 → 0.0350** — bağımsız bir kayma değil: hücre-başı FPR
  *gözlenen k medyanında* değerlendirilir ve medyan, aile 12→17 büyüdüğü için 1.7487'den
  1.6956'ya indi; aynı n değişiminin türevi.

**105 APPEARED:** A12/A13 hükümleri ve G4.2'nin `SOURCES`'a **ilk** kaydı. Üretildikleri gün
kaydedilmemişlerdi, yani kapı onları hiç okumuyordu — G4'te yaşanan boşluğun aynısı.
Temel bu gerekçeyle kabul edildi (`2026-08-08T20:08:40`).

**Kabulün döngüsel olmadığının kanıtı:** temel mevcut dosyalardan alındığı için, yeniden
üretmediğim bir dosya bayat olsa temel de bayat değeri yakalardı. O yüzden donmamış denetimi
okuyan **sekiz üreticiyi** yeniden çalıştırıp kapıyı tekrar koştum → **885/885, 0 sapma.**
A13'ün dört koşusu kayıtlı hücrelerin hiçbirini oynatmadı.

### `PREREGISTRATIONS.md` sonuç satırları

**A12:** *"**HİÇBİR HÜCRE ÖLÇÜTÜ KARŞILAMADI** — 5 hücre × 2 eksen = 10 hükmün onu da
ÇÖZÜNMEDİ. Üç tahminin üçü de tuttu; cümle 'başarısız'tan **'n=3'te kurulamadı'**a
çevrilir."*

**A13:** *"**BAŞLATMA TAHMİNİ YANLIŞLANDI — eğim başlatmaya duyarlı.** T10a (ii) sonuçsuz
kalıyor, ama artık *confound* yüzünden değil *gürültü* yüzünden."*

İkisinin altına ayrıntı bölümleri eklendi (paydalar, hücre tabloları, kıl payı kaçan
yanlışlayıcı, G4.2 tablosu). **Beyanların kendisine dokunulmadı** — yalnız `sonuç` yuvaları
dolduruldu.

### MANIFEST

| kalem | değer |
|---|---|
| ihraç zamanı | 2026-08-08 20:10:18 +0300 |
| dosya | **136** (toplam 2386.8 KB) |
| **"bu çalışmada N yazıldı"** | **1 yazıldı, 135 zaten aynı** |
| günün ilk geçişinde | 35 yazıldı, 101 aynı |
| **defter sha256** | `18676a5953059e7ac925fe1955115cc6ad7c96b82e9f31364664c073fc410a39` |
| defter satır / mtime | 199 / 2026-08-08 19:49:27 |
| defter durumu | **önceki ihraçla aynı → yeni bayatlayan dosya yok** |
| repo commit | `17c38b5a5fb0` (KİRLİ, 44 dosya) |

> **Bandın 100 dosyalık bayatlık uyarısı çürütüldü.** İlk ihraçta defterin sha256'sı
> değişmişti (A13'ün 4 koşusu), o yüzden defterden eski her üretilmiş dosya işaretlendi —
> 100 dosya. Bandın kendi talimatı *"kesin cevap ilgili betiği yeniden çalıştırmaktır"*
> diyor; sekiz üretici yeniden çalıştırıldı, kapı 0 sapma verdi, ikinci ihraçta yalnız
> **1 dosya** değişti ve uyarı listesi **boşaldı**.

### Public senkron

| kalem | değer |
|---|---|
| kova A | **153** (5.7 MB) |
| kova B | **28** (1.9 MB) |
| kova C | 93 (101.0 MB) |
| **kova D** | **0** ✅ |
| kapsam içi (A+B) | **181** |
| izlenen / güncellenen / aynı | 279 / 19 / 255 |
| taşınabilirlik uyarlaması uygulandı | **100 dosya** |
| onaylı aday **yazılan** | **154** |
| hedef klasör | `public\calibration-law-fer_2026-08-08` (git + remote korunmuş) |

**❌ Mutlak-yol kapısı 0 DEĞİL: 36 dosya.** Ve ayrıca **tarihli klasörde 27 fazla dosya
var** — bunlar kapıyı genelleştirmeden önceki ilk `--apply`'da yazıldı, şimdi kapı onları
reddediyor ama diskte duruyorlar (460 dosya var, yazılması gereken 433). 26'sı mutlak yol
taşıyor, 1'i `diagnostics/export_to_drive.py` (C'ye alındı).

**Bu iki maddeden hiçbiri kendiliğinden kapanmaz.** 0'a inmenin iki yolu var: (a) §5'teki
2.2 konvansiyon kararı verilir ve 26 dosya dönüştürülerek yeniden yazılır, ya da (b) o 27
dosya tarihli klasörden **silinir** ve depo 433'e iner. **Silme yapmadım** — dışa dönük bir
artefaktı senin onayın olmadan eksiltmem.

---

## 8. Kapanış beyanı

1. **Gönderim öncesi planlı GPU işi kalmadı — hayır, iş yok.** A12 (10 koşu) ve A13
   (4 koşu) bitti; ön-beyanlı kuyrukların tamamı kapandı. Çalışan hiçbir eğitim süreci yok.

2. **Makale tarafına düşen açık kalemler (sende):** (i) §5.4/T10a'nın "item (ii)
   INCONCLUSIVE" gerekçesini *confound*'dan *gürültü*ye çevirmek; (ii) §5 kapasite
   paragrafına başlatma ekseni savunmasını eklemek; (iii) özet cümlesini "beş mekanizma
   başarısız"dan "n=3'te kurulamadı"ya çevirmek ve `stage1 × target_logvar`'ın barın %98'ine
   ulaştığını yazmak; (iv) aile-bazlı FPR'yi **0.389 → 0.454** güncellemek; (v) kaldıraç
   oranını **76× → 69×** güncellemek; (vi) asimetri cümlesini iki ekstrapolasyonsuz CI'ya
   dayandırmak ve vae9182 kolunda saptanamadığını yazmak; (vii) "56–77×" aralığının yalnız
   `logit_std` üçlüsünü tarif ettiğini belirtmek; (viii) `[final,5p]` sayfa sayısını Mac'te
   ölçmek (bu makinede LaTeX yok).

3. **Repo tarafında gönderim gününe kalan tek iş dizisinin adı:**
   **`diagnostics/reports/2026-08-04_gonderim_gunu_dizisi.md`** — adım 0 → 8b, gönderimden
   **1–2 gün önce** koşar (ihracı dondur → `public_repo_sync.py` → üç kapı → tek commit →
   sil/yeniden kur → public → Release → Zenodo DOI → DOI'nin çözümlendiğini doğrula → üç
   konuma işle). Gönderim günü yalnız EM yüklemesi. **Ön koşul:** yukarıdaki 2.2 konvansiyon
   kararı, çünkü dizinin 1c kapısı "0 mutlak yol" istiyor ve şu an 36.

---

Üretici: elle yazıldı. Ölçüm kaynakları: `a12_realsignal_gate/a12_verdict.{md,json}`,
`a13_scratch_dose/a13_verdict.{md,json}`, `paper_tables/g42_init_matched_lever.{md,json}`,
`paper_tables/criterion_applied.json`, `paper_tables/asymmetry_estimand.json`,
`paper_tables/audit_population.json`, `paper_tables/noise_units.json`,
`paper_tables/section54_numbers.json`, `paper_tables/denominator_table.md`,
`table_diff_gate/last_diff.md`, `reports/public_scope_buckets.md`,
`reports/public_repo_sync_dryrun.md`, `reports/level1_gate.md`,
`G:\My Drive\Claude\Makale\repo_export\MANIFEST.txt`.
