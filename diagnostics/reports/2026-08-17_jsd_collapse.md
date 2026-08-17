# 17 Ağustos 2026 — JSD çöküşü: 40× mi 37× mi?

**Tek cümlelik cevap: iki merci de kendi niceliği için doğru hesap yaptı, ama ortada İKİ AYRI
NİCELİK var ve makale birinin adını diğerine vermiş. Pay ikisinde de aynı; payda farklı ve iki
payda dört basamakta aynı görünüyor (`0.0005`). Çöküş cümlesine 37× girer, gürültü cümlesine
40× — 14 Ağustos'un "37 yeniden üretilemiyor" hükmü yanlıştı ve düzeltiliyor.**

Yeni koşu yok, GPU yok, ileri geçiş yok: yalnız yayımlanmış @swa öğrenci logitleri.
Yeni üretici: `diagnostics/jsd_collapse_audit.py` → `paper_tables/jsd_collapse_audit.{md,json}`

---

## 1 — Cümledeki oranın tam tanımı ve değeri

DURUM ✓ — **oran `R_collapse` = açıklık(ham kollar) ÷ açıklık(TS sonrası kollar) = 37.2342.**

`05_results_discussion.tex:693` (alt bölüm `sec:res_human`, `\paragraph{What post-hoc student
scaling can and cannot do}`) cümlesinin payı ve paydası **aynı türden** iki büyüklük: kollar
arası açıklık, ölçeklemeden önce ve sonra.

| | değer | hangi kollar | artefakt · alan |
|---|---|---|---|
| **pay** | **0.02008283** | T=0.26 (0.073681) − T=0.74 (0.053598) | `paper_tables/r3w1_joint_optimum.json` → `arms.0.26.jsd_arm[0]` − `arms.0.74.jsd_arm[0]` |
| pay (aynı sayı, ikinci artefakt) | 0.02008283 | — | `ferplus_jsd/ferplus_student_jsd.json` → `by_checkpoint.swa.{0.26,0.74}.jsd[0]` |
| **payda** | **0.00053936** | T=0.74 (0.054584) − T=0.26 (0.054045) | `paper_tables/r3w1_joint_optimum.json` → `arms.0.74.jsd_ts[0]` − `arms.0.26.jsd_ts[0]` |
| **oran** | **37.2342** | | üretici `r3w1_joint_optimum.py`, `spread_arm / spread_ts` |

Üretici bu oranı kendi raporunda zaten **37×** olarak basıyor
(`paper_tables/r3w1_joint_optimum.md`, "An unasked-for finding" bölümü, `:.0f` biçimiyle).
Yani makale ile artefakt arasında bir ölçüm anlaşmazlığı yok; makalenin kopyası değişmiş.

Dört kol, ham ve TS sonrası (üç tohum, sample sd):

| T | rol | JSD ham | JSD +TS |
|---|---|---|---|
| 0.26 | over-sharpened | 0.073681 ± 0.000733 | **0.054045 ± 0.000399** |
| 0.5063 | T\*_ECE / T\*_NLL | 0.058690 ± 0.000462 | **0.054274 ± 0.000209** |
| 0.74 | T\*_JSD | 0.053598 ± 0.000373 | **0.054584 ± 0.000249** |
| 1.0 | native | 0.055107 ± 0.000450 | **0.054545 ± 0.000506** |

---

## 2 — İkinci bir 40× var mı?

DURUM ✓ — **var, ve dış incelemenin dediği gibi doğru: `R_noise` = 39.8126.**

`05_results_discussion.tex:636` — **aynı alt bölümün gövdesi**, çöküş cümlesinden 57 satır
önce: *"Student JSD varies over 0.0201 against a typical seed spread of 0.0005, roughly forty
times the noise."* Payı aynı 0.02008283; paydası **tohum sd'si**, TS'in hiç girmediği bir
büyüklük.

| oran | payda | payda kaynağı | değer | basılışı |
|---|---|---|---|---|
| `R_collapse` | TS sonrası açıklık **0.00053936** | `r3w1_joint_optimum.json` → `arms.*.jsd_ts[0]` | **37.2342** | 37× |
| `R_noise` | ortalama tohum sd **0.00050443** | `ferplus_student_jsd.json` → `by_checkpoint.swa.*.jsd[1]` ortalaması | **39.8126** | 40× |

**"40" iki yoldan üretilebiliyor ve ikisi de gürültü oranına ait:**

1. **Basılı değerleri bölmek.** `0.0201 / 0.0005 = 40.20`. Defter değerleri `37.23`. Beş-onbinlik
   mertebesinde bir paydayı dört basamağa yuvarlamak oranı **3.0** kaydırıyor — bugün geri alınan
   "13–14 times smaller" hatasıyla aynı sınıf.
2. **Diğer oran gerçekten ≈40.** `R_collapse`'ın tam 40 olması için payda **0.00050207** olmalıydı.
   Ortalama tohum sd'si 0.00050443 — **%0.47** uzak. TS sonrası açıklık 0.00053936 — **%6.91**
   uzak. Yani 40, çöküş oranının yuvarlanması değil; **gürültü oranının kendisi**, kendi
   cümlesinde doğru, bu cümlede yanlış.

İki paydanın dört basamakta ikisi de `0.0005` basılması, bir cümlenin sayısının diğerine
göçmesini kimsenin fark etmemesini sağlayan mekanizmanın tamamı.

**Gürültü paydasının konvansiyonu hâlâ yazılı değil** (14 Ağustos bunu işaretlemişti, açık kalem):

| konvansiyon | tipik tohum sd | `R_noise` |
|---|---|---|
| **ortalama sd** | **0.00050443** | **39.81** |
| havuzlanmış sd | 0.00052255 | 38.43 |
| medyan sd | 0.00045590 | 44.05 |
| en büyük sd | 0.00073317 | 27.39 |
| en küçük sd | 0.00037277 | 53.87 |

27–54 arası. Kampanya genelinde sabit olan **sd tanımı** (tohumlar üzerinden sample sd); dört
kolun sd'lerinin hangi indirgemesinin "tipik" sayıldığı ise **serbest bir seçim** ve metinde
belirtilmemiş. Yayımlı "roughly forty" ortalama sd okumasına karşılık geliyor.

### Dürüstlük kaydı: çöküş oranının paydası kendisi gürültü seviyesinde

TS sonrası açıklık 0.000539; bir bar (R3-W1'in kendi tanımı, 2 × en büyük TS tohum sd'si)
0.001012. Açıklık **barın içinde** — dört kol birbirinden ayrılamıyor, ki cümlenin iddiası da
tam bu ("onto a common value"). Ama bu, `R_collapse`'ın **sıfırdan ayırt edilemeyen bir
büyüklüğe** oran olduğu anlamına da geliyor. Oran tohum içinde kurulursa 20.9 / 35.4 / 16.9,
yani **24.4 ± 9.8** — üçü de 37.2'nin altında. Yön beklenen: açıklık bir maks eksi min olduğu
için gürültüyle yukarı yanlı, ve kol başına üç tohumu önce ortalamak paydadaki gürültünün bir
kısmını siliyor (ölçtüğü kollar arası sinyal ise zaten ~0). Yayımlı estimand (tohum
ortalamalarının açıklığı) doğru olan ve bu turda her yerde kullanılan; söylenen şu: **çarpan iki
anlamlı basamaktan fazlasını taşımıyor.** Savunulabilir iddia *eksen tohum gürültüsü içinde
çöküyor*; bunun için 37 ile 40 arasındaki fark bilimsel olarak hiçbir şeyi değiştirmiyor —
yalnızca basılı sayıları bölen bir okuyucunun makalenin kendi değerini bulup bulamamasını
değiştiriyor.

---

## 3 — 14 Ağustos hükmünün gözden geçirilmesi

DURUM ✓ — **hüküm yanlıştı; o gün yalnız tohum sd paydaları denendi.**

`number_audit_round3` kalem 7 (14 Ağu) *"~40× doğru, 37× yeniden üretilemiyor"* dedi. Aritmetiği
sağlam, ama **beş paydanın hepsi tohum sd'siydi** (yukarıdaki tablo) ve TS sonrası açıklık hiç
denenmedi. Kalemin okuduğu dosya `ferplus_jsd/ferplus_student_jsd.json`: içinde ham kollar ve
tohum sd'leri var, öğrenci-tarafı ölçekleme hakkında **hiçbir şey** yok. TS sonrası kollar başka
bir artefaktta — `paper_tables/r3w1_joint_optimum.json` — ve kalem 7 o dosyayı **hiç açmadı**.

37× yeniden üretilemez değil: üreticisi doğrudan basıyor ve değeri **37.2342**. Yani soru
"hangisi doğru" değil, "hangi cümlede hangisi" idi; iki cümle iki farklı niceliği adlandırıyor.
Bootstrap veya yuvarlanmış bir payda kullanılmadı — payda **yanlış türdendi**.

14 Ağustos kaydı olduğu gibi duruyor (tarihli beyan); düzeltme burada, bugünün tarihiyle.
Hükmün tehlikeli yarısı aritmetik değil, ima ettiği talimattı: *"37 yeniden üretilemiyor"*
cümlesi 37'yi 40'a çevirmeye davet ediyor ve doğru bir cümleyi yanlış hâle getiriyor. Değişimin
olduğu kayıtta duruyor: kalem 7'nin `published` alanı 14 Ağustos'ta **`37× ve ~40× (aynı
0.0005)`** yazıyor — yani çöküş cümlesi o gün 37× taşıyordu, bugün 40× taşıyor
(`05_results_discussion.tex` bugün 10:54'te değişmiş).

Bu, 15 Ağustos'taki kalem 9 vakasıyla **aynı yapıda üçüncü olay**: kapsamı eksik bir kontrol,
kesin bir hükümle rapor edilmiş. Kalem 9'da atlanan bir ızgaraydı, kalem 7'de bir artefakt.

---

## 4 — Makaleye hangi sayı, hangi adla

DURUM ✓ — **iki sayı da kalır, ama yerleri sabitlenir ve payda cümlede adlandırılır.**

| satır | şu an | olması gereken | ad |
|---|---|---|---|
| `05_results_discussion.tex:693` | "a $40\times$ collapse onto a common value" | **`37\times`** | **collapse** — pay da payda da kollar arası açıklık |
| `05_results_discussion.tex:636` | "a typical seed spread of $0.0005$, roughly forty times the noise" | **`0.00050` + konvansiyon adı**, "roughly forty" kalır | **noise** — payda tohum sd'si |

Üç hareket:

1. **`:693` → 37×.** Üretici zaten 37× basıyor; makale ile artefakt arasındaki tek fark
   makalenin kopyasının değiştirilmiş olması. "Collapse" adı yalnız buraya ait.
2. **`:636`'da paydayı adlandır ve beş basamak yaz**: *"a typical seed spread of 0.00050 (the
   mean of the four arms' seed sds), roughly forty times the noise."* Böylece iki cümle `0.0005`
   dizgesini paylaşmayı bırakır. Adlandırma kozmetik değil: indirgeme serbest ve oran 27–54
   arasında geziyor. Havuzlanmış tahmin edici tercih edilirse 0.00052 → 38.4×, aynı ifade onu da
   karşılıyor.
3. **"Collapse" kelimesi gürültü cümlesinde, "noise" kelimesi çöküş cümlesinde geçmesin.** İkisi
   57 satır arayla, aynı alt bölümde duruyor; ayrımı taşıyan tek şey şu an bu iki kelime.

Ek olarak: çarpan iki anlamlı basamakla yazılsın (§2'nin dürüstlük kaydı) — "37×" evet,
"37.2×" hayır.

---

## Yayımlı sayıların yeniden üretimi

Bu betik hiçbir sayıyı okuyup yeniden yazmıyor: dört kolu üç tohumda yayımlanmış logitlerden
**ithal edilmiş** R0-1 / R3-W1 kod yoluyla yeniden ölçüyor.

| grup | kontrol sayısı | en büyük \|Δ\| |
|---|---|---|
| `r3w1_joint_optimum` dört kol (ham + TS, JSD + ECE, ortalama + sd) | 24 | **0.00e+00** |
| `ferplus_student_jsd` @swa JSD (ortalama + sd) | 8 | **0.00e+00** |
| `number_audit_round3` kalem 7 (açıklık, ortalama sd, oran) | 3 | **0.00e+00** |

**35 kontrol, tamamı 0.00e+00** (eşik 1e-12). Sapmanın tam sıfır olması beklenen sonuç, çünkü
üçüncü bir tanım eklenmedi: bölme kuralı / TS fit'i / iki-eksen ölçümü `student_ts_baseline`'dan,
çapraz-fit bloğu ile dört kolun listesi `r3w1_joint_optimum`'dan ithal edildi. Sorulan soru "iki
sayı neden farklı" olduğu için, kopyalamak cevabın kendisini bozardı.

`r3w1_joint_optimum.py`'de tek değişiklik: `main()` içindeki çapraz-fit bloğu `crossfit_arm()`
fonksiyonuna çıkarıldı. Betik yeniden koşuldu, `.md` ve `.json` **bayt bayt aynı** kaldı.

---

## Kapılar

| kapı | sonuç |
|---|---|
| tablo farkı | **1332/1332 sapma yok** (1294 → 1332). 38 sapmanın **tamamı APPEARED**; CHANGED / MOVED / VANISHED yok |
| Level-1 | **geçti 52** (51'den) · İHLAL 0 · muaf 9 · başka hata 0 |
| mutlak yol (public depo) | 22 dosya beyanlı · **beyansız 0** · okunamayan 0 |
| kapsam taraması (public depo) | commit kümesi 556 · **ihlal 0** (checkpoint 0 · yeniden dağıtılamaz veri 0 · ham yüz 0) |
| figür | **10/10**, 0 failing |
| `r3w1_joint_optimum` ataleti | çıktılar **bayt bayt aynı** (`.json` ve `.md`) |

---

## Bu turun kuralı (kalıcı)

**Türetilmiş nicelikler — oranlar, yüzdeler, kat sayıları — asla basılı yuvarlak değerlerden
hesaplanmaz; her zaman defterden.** Bugün üç örneği var: `0.0015/0.0220 = 14.67` yerine
`0.00154/0.02198 = 14.27`; `0.0201/0.0005 = 40.20` yerine `0.02008283/0.00053936 = 37.23`; ve
aynı `0.0005`'in iki ayrı büyüklüğü gizlemesi. Kural ayrıca şunu gerektiriyor: **bir oranın
paydası cümlede adlandırılmalı** — payda adsızsa oran denetlenemez, ve denetlenemeyen oran iki
farklı niceliğin aynı adı taşımasına açıktır.
