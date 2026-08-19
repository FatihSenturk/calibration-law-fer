# 18 Ağustos 2026 — son sekiz kayıtsız + iki küçük karar (N17)

**Tek cümlelik sonuç: kayıtsız sayı 8'den 0'a indi, `check_numbers` ilk kez çıkış 0 veriyor; ve
dünkü kapı bugün GERÇEK bir vakada sınandı — üretici değişip artefakt yenilenmeyince BAYAT verdi,
düzgün yenilendiğinde sustu.** Yeni koşu yok, GPU yok.

Turun içinde bir de düzeltme var ve raporun başına yazılıyor, sonuna değil: **dün "sekizinin de
JSON alanı yok" dedim; ölçünce bu fazla genel çıktı.** Kırılım §1.1'de.

> Not — takvim: bu tur 18 Ağustos akşamı istendi ve makine saati tur içinde 19 Ağustos'a döndü;
> kapı çıktılarının damgaları o yüzden `2026-08-19` yazıyor. Dosya adı istendiği gibi bırakıldı.

---

## 1 · Sekiz kayıtsız sayı — sekizi de bağlandı

### 1.1 Düzeltme: sekizi tek sebebe bakmıyordu

Dünkü rapor ve `status_queue` kaydı şöyle diyordu: *"sekizi de `robustness_metrics`'in md'ye basıp
JSON'a yazmadığı uzlaşı sayaçları ve FERPlus NLL istisnası 0.74."* Bugün artefaktı açıp baktım —
hafızadan değil, dosyadan — ve **üç ayrı durum** çıktı:

| kaç | sayı | JSON'daki durumu (17 Ağu itibarıyla) |
|---|---|---|
| 3 | uzlaşı sayaçlarının **payı** (7, 7, 6) | **gerçekten yoktu** — yalnız md'de hesaplanıyordu |
| 3 | uzlaşı sayaçlarının **paydası** (7, 7, 7) | skaler alan olarak yoktu; `metric_order` listesinin **uzunluğu** olarak vardı |
| 2 | `0.74` (tablo istisnası + S2 düzyazısı) | `series["FERPlus"].metrics.nll.argmin_T_modal` olarak **ZATEN VARDI** |

Yani son ikisinin kayıtsız kalma sebebi alanın yokluğu değil, **bağın kurulmamış olmasıydı**.
Dünkü cümle üç durumu tek sebebe indirmişti. Eski rapora dokunulmadı (tarihli artefakt); düzeltme
`table_diff_gate` kabul notuna ve buraya yazıldı.

### 1.2 Üreticinin değişikliği: iki yeni alan, ve md artık ikinci kez saymıyor

`diagnostics/robustness_metrics.py`:

* `series[...]._consensus_metrics_agreeing` — "7/7"nin payı,
* `series[...]._n_metrics` — paydası,
* `metrics[...].argmin_T_all_seeds` — **her** tohumun aynı yeri gösterdiği T, oybirliği yoksa
  `null` (§1.3).

Ayrıca özet tablosunu basan md döngüsü artık payı **yeniden hesaplamıyor**, aynı alanları okuyor.
Bu bir üslup değişikliği değil: iki ayrı sayım kodu, ayrışabilen iki sayı demektir.

Artefakt yeniden üretildi ve **`robustness_metrics.md` bayt düzeyinde değişmedi** — yani md'nin
sayımı ile JSON'un sayımı bugün aynıydı; alanlar sadece görünür oldu.

### 1.3 İki `0.74` — tek alana bağlanmadı, ve gerekçesi ölçüldü

Uyarınız tam yerine düştü. İki `0.74` var:

* `tab:app_argmin`'in istisna sütunu: *"NLL: 0.74 (all seeds)"*,
* S2 düzyazısı: *"all three seeds of the NLL metric place the minimum at T = 0.74"*.

Aynı niceliğe mi bakıyorlar? **Hayır** — ve bunu varsayımla değil, artefaktı sayarak buldum.
`argmin_T_modal` **çoğunluğun** koyduğu yerdir; düzyazının iddiası ise **her tohumun** aynı yeri
koyduğudur. Aynı artefaktta 21 (seri × metrik) hücrenin **5'inde** bu ikisi farklı:

| seri | metrik | modal | tohumlar |
|---|---|---|---|
| RAF-DB stage1 | Brier | 1.3406 | 1.3406 · **1.70** · 1.3406 |
| RAF-DB stage1 | ECE ew-15 | 1.3406 | **1.70** · 1.3406 · 1.3406 |
| RAF-DB stage1 | classwise-ECE | 1.3406 | 1.3406 · **1.70** · 1.3406 |
| RAF-DB vae9182 | NLL | 1.00 | 1.00 · **0.85** · 1.00 |
| RAF-DB vae9182 | Brier | 1.00 | 1.00 · **1.3406** · 1.00 |

Beş karşı örnek varken tek alana bağlamak, bu ailenin dördüncü üyesini kurardı (`T*` iki estimand,
`0.1126` üç alan, `0.0005` iki büyüklük). Bağlar ayrıldı:

| nerede | alan |
|---|---|
| `tab:app_argmin` istisna sütunu | `...metrics.nll.argmin_T_modal` |
| S2 düzyazısı | `...metrics.nll.argmin_T_all_seeds` |

İkinci alan oybirliği yoksa `null`'dur ve defter `null`'u sayı saymaz. Sonuç: **FERPlus'ta bir gün
bir tohum ayrışırsa, düzyazı cümlesi sessizce modal'i takip etmez — `unresolved_path` verir.**
Bu öz sınamaya senaryo olarak kondu (§3), çünkü kurulup denenmemiş bağ, kurulmamış bağdır.

### 1.4 Sonuç

```
jeton 862 · bagli 695 · turetilmis 21 · muaf 150 · KAYITSIZ 0 · uyusmazlik 0 · teyit 3 · sorun 0
```

Jeton muhasebesi yine tam kapanıyor: **695 + 17 + 150 + 0 = 862**. `check_numbers` **çıkış 0**.
Bağlanamayan kalmadı — kaçının kaldığını yazacak bir şey yok.

---

## 2 · Kapının ilk GERÇEK vakası

Dün kapının kanıtı sentetikti (42 `per_seed` bloğunu silip geri koymak). Bugün üreticiyi
gerçekten değiştirdim ve **artefaktı yenilemeden önce** kapıyı koşturdum:

```
  [1/1] A  BAYAT              diagnostics/robustness_metrics.py  (15.7s)
  Katman A 1 · Katman B 0
  BAYAT 1 · KAYNAK AYRIŞMASI 0 · olculemez 0 · başka hata 0
    !! BAYAT  diagnostics/robustness_metrics.py  [{'artifact':
       'diagnostics/paper_tables/robustness_metrics.json',
        'stored': 'dac7a8ba1bcb3ea5', 'regenerated': ...}]
  SONUÇ: DÜŞTÜ  (1 kalem)
```

Sonra iki şey doğrulandı:

1. **Kapı artefaktı bozmadı.** Koşudan hemen sonra `git status` bu iki dosya için **boş** —
   anlık kopya geri yazıldı. Kapı ölçer, düzeltmez; tasarım kararı işledi.
2. **Düzgün üretince sustu.** Artefakt yeniden üretildikten sonra tam koşu: **GEÇTİ**,
   `Katman A 52 · Katman B 8 · BAYAT 0 · kaynak ayrışması 0 · ölçülemez 0 · başka hata 0`.
   (Aynı koşu kapının kendisinde ikinci bir kusur açığa çıkardı — §2.1.)

Yani kapı iki yönde de doğru davrandı: unutulmuş yenilemede bağırdı, yapılmış yenilemede sessiz
kaldı. İki koşu arasında değişen tek şey artefaktın kendisiydi.

**Kapının kapsamadığı bir şeyi de yazayım:** bu turda `tools/build_repro_export.py` de değişti
(§4) ve o dosya bandın üretici listesinde **değil** — tazelik kapısı yalnız `diagnostics/`
üreticilerini görüyor. O değişiklik depoda duran bir artefaktı bayatlatmıyor (betik dışarıya,
`--dest` ile verilen dizine yazıyor), ama kapının sınırı budur ve burada yazılı olsun.

### 2.1 İkinci gerçek bulgu: kapı çalışma ağacını kirli bırakıyordu

Gerçek vaka koşusundan sonra ağacı denetlerken beklenmedik bir dosya değişmiş çıktı:
`paper/figures/graphical_abstract.pdf`. Sebep, kapının kendi tasarımında:

**Anlık kopya yalnız bandın BEYAN ETTİĞİ artefaktı kapsıyordu.** `graphical_abstract.py` bantta
sadece `.png` ile duruyor, ama `.pdf`i de yazıyor. Kapı `.png`i kopyalayıp geri yazıyor, `.pdf`e
dokunmuyor — ve üretici onu her koşuda yeniden yazdığı için ağaç kirli kalıyordu. "Kapı ölçer,
düzeltmez" kuralı **beyan edilmiş** artefaktta işliyordu, beyan edilmemişte değil.

İki ölçüm bunu ilginç kılıyor:

* Fark **3 bayt**, üçü de `/CreationDate` içinde (`D:20260817154419+03'00'` →
  `D:20260819144412+03'00'`); içerik birebir aynı.
* Yani o `.pdf` **bayt-yeniden-üretilebilir değil**. Bandta olmaması iki ayrı şey olabilirdi
  (unutulmuş olması ya da karşılaştırılamaz olması) ve ölçüm ikincisini söylüyor. Bantta olsaydı
  kapı **her koşuda** BAYAT verirdi — bir saat damgası yüzünden.

Kapıya buna göre bir sınıf eklendi: **beyansız yan çıktı**. Katman A artık koşudan önce ve sonra
`git status`u okuyor; farkı beyan edilen artefaktlardan düşüyor; kalanı raporluyor ve **yalnız
koşudan önce temiz olan** dosyaları geri alıyor (önceden değişmiş bir dosyaya dokunmuyor —
kapı kullanıcının çalışmasını silmez). Kapıyı **düşürmüyor**: hüküm bandın kararıdır, kapının
değil; ama artık görünmeden geçmiyor.

Son koşu: `beyansız yan çıktı 1` — yukarıdaki `.pdf`. Koşudan sonra `git status paper/` **boş**.

> Eklerken kapının kendi anlık kopya dizini yanlış pozitif verdi (`_freshness_snapshot/`: git onu
> boşken görmüyor, ilk kopyadan sonra "yeni izlenmeyen dizin" diye bildiriyor ve ilk üreticinin
> yan çıktısı gibi görünüyordu). Elendi.

### 2.2 Yan bulgu: kapının kendi `--help`'i cp1252'de düşüyordu

`--help` metni Türkçe ve argparse onu **parse sırasında** basıp çıkıyor; `reconfigure` bloğu
`parse_known_args()`ten **sonra** olduğu için varsayılan Windows konsolunda `--help`
`UnicodeEncodeError` ile düşüyordu. Blok parser'ın önüne alındı. Küçük ama kapıya ait: bir kapının
yardım metni de kapının parçasıdır.

---

## 3 · Öz sınama 14 → 17

Üç senaryo eklendi, üçü de bu turda kurulan bağları hedefliyor:

| senaryo | beklenen sınıf |
|---|---|
| `app_argmin` uzlaşı sayacı bayat (6/7 → 5/7) | `rounding_mismatch` |
| `app_argmin` FERPlus NLL istisnası bayat (0.74 → 0.75) | `rounding_mismatch` |
| oybirliği alanı çökerse düzyazı bağı düşer (0.74 modal'a **kaymaz**) | `unresolved_path` |

Üçüncüsü §1.3'ün yapısal güvencesini sınıyor: bağ, tohumların **ayrıştığı** bir seriye çevriliyor
(RAF-DB vae9182/NLL, alan `null`) ve defterin düşmesi bekleniyor. **İki `0.74` tek alana bağlanmış
olsaydı bu senaryo yakalanamazdı** — senaryo, ayrımın yaşadığının kanıtı.

`SONUC: HEPSI YAKALANDI` — **17/17** (taban satırı hariç).

---

## 4 · `requirements_27may.txt` silindi

Karar uygulandı. Silmenin asıl işi dosyayı kaldırmak değil, **ona işaret eden yaşayan yolları**
çevirmekti; kaldırılıp atıfları bırakılan bir dosya, olmayan bir dosyaya `pip install -r` diyen
bir depo bırakır.

| dosya | ne yapıldı |
|---|---|
| `README_27MAY_RAFDB.md` | `requirements.txt`e çevrildi |
| `README_27MAY_REPRODUCTION.md` | `requirements.txt`e çevrildi |
| `tools/build_repro_export.py` | ürettiği kurulum talimatı `requirements.txt`e çevrildi |
| `diagnostics/requirements_lock.py` | başlıktaki gerekçe güncellendi (+ aşağıdaki tutarsızlık) |
| `diagnostics/status_queue.txt` | kararın kaydı düşüldü |
| `STATUS.md` | **gövdesine dokunulmadı**; başlığındaki devretme notunun altına tarihli ek |
| `diagnostics/reports/2026-08-14_*`, `2026-08-18_*` | **dokunulmadı** — tarihli artefakt |

`STATUS.md` 2026-07-22 tarihli bir denetim anlık görüntüsü ve §5'inde *"`requirements_27may.txt`
EXISTS"* yazıyor. O cümle o gün doğruydu; silinmedi, **altına 18 Ağustos tarihli bir ek** düşüldü
ve neyin geçersizleştiği (env kilidi yok hükmü) ile neyin ayakta kaldığı (git SHA / config hash
yok, cuDNN belirsizliği) ayrı ayrı yazıldı.

**Yan bulgu — dünkü dosyada iç çelişki.** `requirements_lock.py`'nin başlığı *"eşlenemeyen import
adı ... bu betik çıkış kodu 1 verir"* diyordu; oysa `main()` **0** dönüyor ve gerekçesi kodun
içinde yazılı (dün bilerek değiştirilmişti, başlık güncellenmemişti). Başlık koda göre düzeltildi.

---

## 5 · `numpy==2.4.0rc1` ve çift opencv — dosya değil README

Dosyaya dokunulmadı, gerekçeniz aynen geçerli: `requirements.txt` fiilen koştuğumuz ortamı
kaydediyor. Public depo README'sinin **Environment** bölümüne iki cümle eklendi: sürüm adayının
bilerek orada durduğu (dosya daha derli toplu bir ortamı değil, **ölçülen** ortamı kaydediyor) ve
`cv2` import adının iki dağıtıma birden eşlendiği, dolayısıyla temiz bir kurulumda ikisinin de
gerektiği.

---

## 6 · Kapılar

| kapı | sonuç |
|---|---|
| `check_numbers` | **GEÇTİ · çıkış 0** — kayıtsız 0, uyuşmazlık 0 |
| `check_numbers_selftest` | **17/17** (14'ten yükseldi) |
| üretici tazeliği | **GEÇTİ** — Katman A 52 · Katman B 8 · BAYAT 0 · kaynak ayrışması 0 · ölçülemez 0 · başka hata 0 · **beyansız yan çıktı 1** (§2.1) |
| tazelik öz sınaması | **2/2** |
| tablo diff | **1496/1496** — 45 sapma kabul edildi: 2 MOVED (defterin kendi sayacı, kayıtsız 8→0) + 43 APPEARED; **CHANGED/VANISHED yok** |
| Level-1 | **GEÇTİ** — geçti 58 · İHLAL 0 · muaf 10 · başka hata 0 |
| figür | **10/10**, 0 başarısız |
| mutlak yol | **GEÇTİ** — beyansız 0 |
| public kapsam taraması | **İHLAL 0** (checkpoint 0 · yeniden-dağıtılamaz lisanslı veri 0 · ikili içinde yol 42 beyanlı · ham yüz 0) |

43 yeni hücrenin dökümü: 21 (seri × metrik) için `argmin_T_modal`, oybirliği olan 16 hücre için
`argmin_T_all_seeds`, üç seri için `consensus_T` + `metrics_agreeing`. **21 − 16 = 5** hücrede
oybirliği yok ve o hücreler bilerek düşürüldü — böylece bir gün oybirliği çökerse kapı `VANISHED`
diye bağırır, sessizce kaymaz.

---

## 7 · Açık kalan

* **Zenodo DOI** — 14 Ağustos'tan beri açık; `v1.0.0-submission`dan basılacak, başlanmadı.
* **`sections/*.tex` düzyazısı** — 821 jeton, bilinçli olarak bağlanmadı (N16'da ölçüldü).
* Bu turda **bağlanamayan sayı kalmadı**.
