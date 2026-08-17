# 17 Ağustos 2026 — sayı provenans defteri (N13)

**Tek cümlelik sonuç: defter kuruldu ve çalışıyor. Kapsamdaki 714 sayının 689'u (%96,1) artık
bir alana bağlı, türetilmiş ya da "ölçüm değil" diye beyanlı; basılı-değer ↔ alan uyuşmazlığı
0; kalan 28 sayı ise KAYITSIZ ve bu bir kusur kaydıdır, örtülmedi. Denetçi bugünün beş
hatasının hepsini + iki ek senaryoyu yakaladı (7/7) ve şu an makaleye karşı çıkış kodu 1
veriyor — çünkü o 28 sayı gerçekten kayıtsız.**

Yeni koşu yok, GPU yok: tamamı önbellek/CPU/metin.

| çıktı | ne |
|---|---|
| `diagnostics/paper_number_scan.py` | ORTAK tarayıcı — defter ile denetçi aynı jetonları görmek zorunda |
| `diagnostics/number_ledger.py` | beyanlar (bağ/türetme/muafiyet) + üretici |
| `paper_tables/number_ledger.{md,json}` | alan bağlama defteri |
| `paper_tables/derived_registry.{md,json}` | oran/fark kütüğü, pay ve payda alan yoluyla |
| `diagnostics/check_numbers.py` | denetçi, ihlalde **çıkış kodu 1** |
| `diagnostics/check_numbers_selftest.py` | bugünün hatalarını geri koyup yakalandığını gösterir |

---

## 1 — Kapsam ve sayım

| | sayı |
|---|---|
| kapsamdaki sayı jetonu | **714** |
| bir artefakt alanına bağlı | **590** |
| türetilmiş (oran/fark, pay+payda alan yoluyla) | **10** |
| düzyazıda tek tek beyanlı bağ | **1** |
| "ölçüm değil" diye beyanlı | **88** |
| **kayıtsız** | **28** |
| basılı değer ↔ alan uyuşmazlığı | **0** |
| tanım sorunu (belirsiz/çürümüş/çift bağ) | **0** |
| tarayıcının attığı yerleşim jetonu | 166 |

**Giren:** `paper/tables/*.tex` (10 dosya, 11 tablo) · özet · `supplementary` S8–S11.
**Girmeyen (beyanlı):** `sections/*.tex` düzyazısı (revizyon penceresi) · supplementary S1–S3
(bugünkü headroom hükmü oraya henüz işlenmedi; değişecek bir hücreyi bağlamak çürük).
**Ölçüm değil (14 sınıf, hepsi gerekçeli):** hiperparametre · tohum kimliği · örneklem
büyüklüğü · popülasyon sayımı · mimari boyutu · donanım adı · veri tipi adı · ölçüm protokolü
sabiti · ölçüt sabiti (2σ) · sütun başlığı · öğretmen adındaki basamak · tablo atfı · tarih ·
yuvarlama uyarısı · ön-kayıt provenansı (S11).

Yuvarlama konvansiyonu **yarıyı yukarı** (`ROUND_HALF_UP`) olarak beyan edildi; elle yazılan bir
sayı böyle yuvarlanır. 590 bağın tamamı bu konvansiyonla tutuyor.

## 2 — Denetçi ne yakalıyor (beş sınıf)

1. `rounding_mismatch` — basılı değer, bağlı alanın beyan edilen yuvarlamasıyla eşleşmiyor
2. `unresolved_path` — bağlı alan artefaktta **artık yok** (bayatlık)
3. `derived_mismatch` / `printed_not_found_at_location` — türetilmiş nicelik pay/paydadan
   yeniden hesaplanınca tutmuyor, ya da defterdeki değer o cümlede geçmiyor
4. `unregistered` — makalede deftere kayıtlı olmayan ölçüm sayısı var
5. `ledger_drift` — depodaki artefakt ile beyanlar ayrışmış (artefaktı elle düzeltme yolu kapalı)

Çıkış kodları: **0** ihlal yok · **1** ihlal var · **2** denetlenemedi (kâğıt ağacı yok).

**Yetkili değer makalenin kendisidir.** Türetilmiş bir nicelik bir hücreye bağlıysa
karşılaştırma koda yazılı `printed` ile değil **makalede basılı** değerle yapılır. Bu, öz
sınamada ölçüldü: ilk sürüm `16.3 → 18.0` enjeksiyonunu **kaçırdı**, çünkü koda yazılı değere
bakıyordu. Düzeltildi ve senaryo yakalandı.

## 3 — Doğrulama: bugünün hataları geri konduğunda

`check_numbers_selftest.py` makalenin bir **kopyasını** kurar (Drive'daki kaynağa dokunmaz), her
hatayı tek tek enjekte eder ve beklenen ihlal sınıfını arar. **Taban temiz kopyada 0 tanım
sorunu.**

| senaryo | beklenen sınıf | sonuç |
|---|---|---|
| `tab_selection` ECE sütunu bayat (0.0627→0.0631 · 0.0606→0.0608 · 0.0274→0.0273) | `rounding_mismatch` ×3 | **YAKALANDI** |
| `tab_selection` öğrenci doğruluğu bayat (89.75→89.74) | `rounding_mismatch` | **YAKALANDI** |
| `tab_collapse` türetilmiş oran bozuk (16.3→18.0) | `derived_mismatch` | **YAKALANDI** |
| §5.7 çöküş çarpanı 40× geri kondu (37 yerine) | `printed_not_found_at_location` | **YAKALANDI** |
| tabloya kayıtsız bir sayı eklendi | `unregistered` | **YAKALANDI** |
| **r=0.724 bağı T=1 yerine T=0.74 koluna kuruldu** | `unresolved_path` / `printed_not_found_at_location` | **YAKALANDI** |
| bağlı alan artefaktta yok (bayatlık) | `unresolved_path` | **YAKALANDI** |

**7/7.** Sonuncusu Fatih'in "en zoru ve en değerlisi" dediği vaka: sayı doğru, artefakt doğru,
**bağ yanlış**. Yakalanmasının sebebi defterin `r=0.724`'ü `ferplus_jsd.json →
entropy_correlation.T1.pearson` alanına bağlaması; bağ T=0.74 koluna çevrildiğinde o alan
çözülemiyor ve cümlede o değer geçmiyor. **Bilinen sınır aynen geçerli:** cümle sayıyı yanlış
kola *atfediyorsa* ve defter de aynı yanlışı taşıyorsa denetçi bunu göremez — dili okumaz.
Defterin işi bağı kurmaya zorlamak.

## 4 — Kayıtsız kalan 28 sayı (kusur kaydı, örtülmedi)

| kaç | nerede | neden kayıtsız |
|---|---|---|
| 3 | `tab_pooled` `r` (unsigned) sütunu: +0.930 / +0.970 / +0.948 | **Hiçbir artefakt havuzlanmış 14 nokta üzerinde Pearson hesaplamıyor.** Spearman sütunları temiz bağlanıyor (`two_dataset_overlay.pooled_stats`), Pearson'un üreticisi yok |
| 10 | `tab_selection_audit` FERPlus satırları | `selection_gain.audit_deltas` yalnız RAF-DB kırılımı taşıyor; FERPlus'ın 12 koşulu satırlarının üreticisi kayıtlı değil |
| 6 | özet: 0.51 · 41–76% · 1.8–2.0× · 27× | dördü de türetilmiş nicelik; operandları henüz kütüğe girmedi |
| 4 | `tab_logitstd` alt yazısı: 23× / 27× / 52× / 2.6× | gürültü-birimi oranları; operandları (`noise_units`/`criterion_applied`) kütüğe girmedi |
| 3 | `tab_selection` alt yazısı: ρ_s −0.50 / +1.00 ve 0.52'nin ikinci geçişi | üç öğretmen üzerinden sıra korelasyonu; artefaktı yok |
| 2 | `tab_mechanisms` "G2G + adaptive T" satırı (−0.07 / −0.0018) | `RESULTS_TABLES.T5` yalnız 3×7 = 21 tekil mekanizma taşıyor; bu bileşik hücre yok |

Bunların hiçbiri "yanlış" demek değil — **kaynağı gösterilemiyor** demek. Denetçi bu yüzden şu an
çıkış kodu 1 veriyor ve öyle kalması doğru: yeşil bir kapı bu 28 kalemi görünmez yapardı.

## 5 — Bağ kurarken ortaya çıkan iki kalem

**(a) `T*` adı iki farklı niceliği taşıyor.** `tab_dose_response`'un blok başlıkları:
Stage1'de basılan `T^*=1.34` **dağıtılan** sıcaklık (1.3406; fit 1.3494 olsa 1.35 basılırdı),
VAE9182'de basılan `T^*=0.98` ise **fit** (0.98294; dağıtılan kol 1.00). Aynı etiket, iki
estimand — bugünün 37×/40× vakasıyla aynı hastalık. Defter ikisini ayrı alanlara bağladı
(`points[2].T` ve `recipe_step3_ranking.rows[teacher=vae9182].T_star`), ama **makale tarafında
adlandırma düzeltilmeli.**

**(b) `tab_selection_audit`'in sıra-istatistiği satırları** ilk sütunu boş bıraktığı için
tablonun kendi yapısında üstteki `FERPlus` etiketini miras alıyor. Sayılar RAF-DB'nin donmuş
131 koşusundan geliyor. Defter bunu olduğu gibi kaydetti; okuyucu için yanıltıcı, satır etiketi
verilmeli.

**(c) Dünün önerileri uygulanmış:** `05_results_discussion` artık `a $37\times$ collapse` ve
`0.00054` yazıyor, gürültü cümlesi de `0.00050` + "roughly forty" biçiminde. Defter ikisini de
doğruladı.

## 6 — Kapılar

| kapı | sonuç |
|---|---|
| tablo farkı | **1364/1364 sapma yok** (1332 → 1364). 32 sapmanın **tamamı APPEARED** |
| Level-1 | **geçti 53** (52'den) · İHLAL 0 · muaf 9 · başka hata 0 |
| figür | **10/10**, 0 failing |
| `check_numbers` (makaleye karşı) | **çıkış 1** — 28 kayıtsız sayı, 0 uyuşmazlık |
| `check_numbers_selftest` | **7/7 yakalandı**, çıkış 0 |

Kâğıt ağacı yolu koda yazılmadı: `--paper-root` / `VELD_PAPER_ROOT`. Yol verilmezse üretici
mevcut defteri **korur** ve 0 döner — Level-1 kapısı üreticileri argümansız çağırdığı için bu
şart, ve artefakt hiçbir makinede bozulmaz.

## 7 — Sıradaki (defterin kendi kuyruğu)

1. `tab_pooled`'un Pearson sütunu: ya üreten bir artefakt (havuzlanmış 14 nokta) ya da sütunun
   kaldırılması. Şu an makalede kaynağı olmayan üç sayı var.
2. FERPlus seçim-denetimi satırları: `selection_gain`'e FERPlus kırılımı ya da satırların
   kaynağının ayrı artefaktta gösterilmesi.
3. Özet ve `tab_logitstd` oranları (0.51 · 41–76% · 1.8–2.0× · 23/27/52/2.6×) türetilmiş
   kütüğe: operand alanları bulunup yazılacak. **§3.2'nin "13–14×"i de buraya girer** —
   operandlarını tahmin etmedim, çünkü bu turun bütün amacı tahmin edilmiş bağı yasaklamak.
4. Kapsam genişletmesi: supplementary S1–S3 (headroom düzeltmesi işlendikten sonra) ve
   `sections/*.tex` düzyazısındaki ~470 sayı (revizyon penceresi kapandıktan sonra).
