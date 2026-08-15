# Kapanış turu — üç karar, üç teyit, kapanış beyanı

**Tarih:** 8 Ağu 2026 (ölçümler 9 Ağu 02:00–02:35 arasında alındı)
**Girdi:** `planning/ide_kapanis_turu_2026-08-08.md`
**Kural:** ölçmeden yazma; kısmi başarıyı ayrıca işaretle.

---

## Özet — ne geçti, ne geçmedi

| kalem | beklenen | ölçülen | |
|---|---|---|---|
| K1 — 2 beyansız fazlalığı sil | silinsin | **silindi** (9 Ağu, izin verildikten sonra) | ✅ |
| K1 — kapı notu | düşülsün | düşüldü (`abs_path_gate.OUT_OF_SCOPE_NOTE`) | ✅ |
| K2 — sha256 özdeşliği | 42/42 | **42/42** (ayrıca public depoya kadar 42/42) | ✅ |
| K2 — tablo kapısı 0 sapma | 0 sapma | **885/885, sapma yok** (yalıtılmış adım) | ✅ |
| K2 — README cümlesi | genişletilsin | genişletildi, 554 KB → 3,9 MB (+ npz `meta` beyanı) | ✅ |
| K3 — iki yer tutucu | ikisi de tanımlı | tanımlıydı; **örnekler yanlıştı, düzeltildi** | ⚠️→✅ |
| mutlak-yol kapısı | beyansız 0 | **20 dosya / 68 eşleşme / 0 beyansız — GEÇTİ** | ✅ |
| tablo kapısı | 0 MOVED | **973/973, 0 MOVED / 0 CHANGED / 0 VANISHED** | ✅ |
| Level-1 | İHLAL 0 | **geçti 42 · İHLAL 0 · muaf 9 · başka hata 0** | ✅ |

> **Sayıların anı.** Mutlak-yol kapısının sayısı bu rapor yayımlandıktan sonra alındı.
> Silme öncesi 22 dosya / 100 eşleşme; sonrası **20 / 68 / 0 beyansız**. Ara sayılar burada
> bırakılıyor ki "21 mi 22 mi" sorusu T1'in tekrarı olmasın: popülasyon değişti, ölçüm
> değişti, ikisi de yazılı.

### Turun asıl bulgusu: "İHLAL 0" sorulmamış sorulara dayanıyordu

T3'ün "parse_args teyidi" kalemi kapının **harness'ının bozuk olduğunu** ortaya çıkardı: 9
üretici `başka hata` sütununda duruyordu ve o sütun "ihlal yok" demek DEĞİL, **"soru hiç
sorulmadı"** demekti. Beş arıza düzeltilip `başka hata` **0**'a indiğinde arkasından **üç
gerçek ihlal** çıktı — ve üçü de kapatıldı:

| betik | ne okuyordu | çözüm | çıktı |
|---|---|---|---|
| `student_ts_baseline.py` | koşu dizini logitleri + `run_args.json` | yayımlanmış logit önbelleği + `val_from_published()` | **BAYT ÖZDEŞ** (`1129ad0c…`) |
| `order_stat_trend.py` | 131 koşunun `training_log.csv`'si (`val_acc`) | `epoch_curves.npz` | **BAYT ÖZDEŞ** (8 Ağu hâli) |
| `selection_gain_estimator.py` | 199 koşunun `training_log.csv`'si (`val_acc`+`val_loss`) | `epoch_curves.npz` | **BAYT ÖZDEŞ** (199-koşu hâli) |

**8 Ağu'nun "İHLAL 0"'ı kısmen sorulmamış sorulara dayanıyordu.** Bugün 51 üreticinin 51'ine
soru soruldu, hiçbiri "ölçülemedi" değil, ve İHLAL gerçekten 0.

### Epok-eğrisi yan dosyası — biçim ölçülerek seçildi

Yayımlama kararı 9 Ağu'da verildi (42 npz kararının aynı sınıfı). Biçim adayları:

| seçenek | boyut |
|---|---|
| 216 tam `training_log.csv` (10 sütun) | 15.599.427 bayt (14,88 MiB) |
| 3 sütunlu tek CSV (ad her satırda tekrar) | 14.985.525 bayt (14,29 MiB) |
| aynısı gzip'li | 2.273.314 bayt (2,17 MiB) |
| koşu başına dizi, `.npz`, **float32** | 761.408 bayt (0,73 MiB) — **KULLANILAMAZ**, aşağıya bak |
| koşu başına dizi, `.npz`, **float64** | **1.237.133 bayt (1,18 MiB)** — seçilen |

`diagnostics/epoch_curves.npz`: **199 koşu** (donmuş denetim 131 ⊂ RAF-DB bitmiş 199),
**76.700 epok satırı**, 597 dizi, sha256 `a0f7cc90…`.

> **Popülasyon sayısı düzeltmesi.** Önce "330 koşu × 126.200 epok" diye ölçmüştüm; yanlıştı.
> Ön ölçümde donmuş denetimin yolları CSV'den **mutlak**, RAF-DB tarafı **göreli** geliyordu,
> dolayısıyla küme birleşimi aynı koşuyu iki kez sayıyordu. Toplayıcıda iki taraf da mutlak
> ve gerçek sayı 199 / 76.700. Dosya boyutu ilk ölçümde de doğruydu (sözlük anahtarları
> zaten tekilleştiriyordu).

#### float32 SAYIYI OYNATTI — ve bir ortalamayı değil bir SEÇİMİ

İlk sürüm `float32` yazdı ve iki tüketicinin çıktısı da değişti, iki farklı büyüklükte:

| büyüklük | float64 (doğru) | float32 | fark |
|---|---|---|---|
| `order_stat_trend` a2_raw K=50 ort. | 0,6445305843 | 0,6445301854 | ~4e-7 |
| `order_stat_trend` a2_raw K=100 ort. | 0,7639534297 | 0,7639530269 | ~4e-7 |
| **`selection_gain` argmax_in_last_K K=50** | **0,3417085** | **0,3266332** | **−1,5 puan** |
| **aynısı K=100** | **0,6482412** | **0,6281407** | **−2,0 puan** |
| `val_loss_at_selected − mean_lastK` K=50 | −0,013179 | −0,012822 | 3,6e-4 |

Sebep: `training_log.csv` `val_acc`'i tam float64 gösterimiyle yazıyor
(`81.28766245165968`). `float32`'ye indirilince ayrı olan değerler **eşitleniyor** ve
`acc.index(max(acc))` daha **erken** bir epoku seçiyor — böylece hem `argmax_in_last_K` hem
`loss[gargmax]` kayıyor. Hassasiyet kaybı bir ortalamayı değil bir **seçimi** değiştirdi.

`float64`'e geçilince iki çıktı da birebir geri geldi. Bedeli 0,73 → 1,18 MiB. Ders, 42
npz'yi bayt kopyası tutma gerekçesinin aynısı: **sayı üreten bir dosyayı yeniden paketlemek
"sadece biçim" değildir** — ve bu kez kapının 0-sapma şartı bunu yakaladı.

---

## K1 — beyansız 2 fazlalık: SİLİNDİ

| dosya | neden kapsam dışı | git'te | durum |
|---|---|---|---|
| `diagnostics/export_to_drive.py` | ihraç altyapısı; repro deposunun konusu makalenin sayıları | izlenmiyordu | **silindi** |
| `tools/sanitize_public_export.py` | aynı sınıf | izlenmiyordu | **silindi** |

İkisi de git tarafından izlenmiyordu (ölçüldü: `git ls-files` boş döndü), yani silme yalnız
çalışma ağacından kaldırdı, geçmişe dokunmadı. Silme sonrası kapı:

```
mutlak yol taşıyan DOSYA : 20  (eşleşme 68)
   14  tek tek gerekçelendirilmiş kalıntı
    3  üçüncü taraf (POSTERv2/CrossViT mirası, beyanlı muaf)
    3  tarihli rapor sınıfı
    0  BEYAN EDİLMEMİŞ
KAPI GEÇTİ: beyansız mutlak yol YOK.
```

22 → 20 dosya, 100 → 68 eşleşme. Kova kararı doğruydu ve değişmedi.

### Kapı notunun düşüldüğü yer

`diagnostics/abs_path_gate.py` içindeki `OUT_OF_SCOPE_NOTE` sözlüğü. Notun kendisi Fatih'in
cümlesi, birebir:

> "sync silme yapmaz; depo günü sil/yeniden-kur zaten sıfırdan kurar."

Not **muafiyet değil teşhis** olarak konumlandırıldı ve bu betikte yazılı: notu olan dosya
için de kapı düşer, sütun adı "not", sınıf adı hâlâ `BEYAN EDİLMEMİŞ`. Sebep açık — bu iki
dosya beyanlı muaf olsaydı kapı bir daha onları göstermezdi ve silme unutulabilirdi. Not
silme sonrası da yerinde duruyor: aynı sınıftan bir dosya yarın yine kapsam dışına
çıkarıldığında teşhis hazır olsun.

**Kalan yapısal boşluk (kapatılmadı).** `public_repo_sync.py` hâlâ **hiç silmiyor**: bir
dosya A/B kovasındayken yazılıp sonra C'ye taşınırsa diskte kalır. Bu tur o durumu elle
kapattı, mekanizmayı değil. Dar kapsamlı bir `--prune-extras` bayrağı (yalnız git'in
izlemediği VE onaylı A+B listesinde olmayan dosyaları silen, `--add-approved` olmadan
çalışmayı reddeden) doğru mühendislik cevabıdır ve **yazılmadı** — ayrı bir karar. O gelene
kadar `abs_path_gate.py` bu sınıfı yakalayan tek şeydir; runbook 1c'nin birinci kapısı
olması bu yüzden önemli.

---

## K2 — 42 npz yayımlandı

### Toplayıcı ve özdeşlik kapısı

Yeni betik: `diagnostics/publish_student_logits.py`. Sınıfı `build_runs_ledger.py` ile aynı
— **Level 3**, koşu dizinlerini okumak işi, `level1_gate.ALLOWED` içinde beyanlı. Sınır tam
orada: bilgi bir kez burada çıkarılır, tüketiciler bir daha koşu dizinine bakmaz.

Kopya **bayt kopyasıdır**, yeniden paketleme değil. Yeniden paketlemek `meta` alanını
(koşu dizini, `ece_recomputed`, `audit_ece`) kaybetme ya da kayan-nokta biçimini değiştirme
riski taşırdı; bayt kopyası ikisini de kaldırır ve özdeşliği tek satırda kanıtlanabilir
kılar.

```
sha256 ÖZDEŞLİK: 42/42
toplam 42 dosya · 3.518.317 bayt (3,36 MiB) · bu koşuda 42 kopyalandı
```

Özdeşlik **iki durak boyunca** ayrıca ölçüldü — senkronun `transform`'u ikili bir dosyayı
bozmuş olabilirdi:

| zincir | sonuç |
|---|---|
| koşu dizini == `diagnostics/student_logits/` kopyası == MANIFEST sha256 | **42/42** |
| koşu dizini == **public depodaki** kopya | **42/42** |

`diagnostics/student_logits/MANIFEST.json` her dosya için köken koşu dizinini (depo-göreli),
sha256'yı, baytı, `n_val`'i ve önbelleğin kendi `acc/ece` kaydını taşıyor.

**Tekillik kapısı taşındı, silinmedi.** "Bir koşu adına tam bir bitmiş dizin düşmeli" kapısı
`robustness_metrics.rafdb_curve()` içindeydi ve koşu dizinlerini `iterdir` ile geziyordu —
Level-1 ihlalinin kaynağı buydu. Kapı `publish_student_logits.sources()`'a geçti: sınırı
geçen tek betik orası.

### İki betiğin yol değişikliği — sayı oynadı mı

Yalıtılmış adım, ölçüm önce ve sonra:

| artefakt | sonuç |
|---|---|
| `robustness_metrics.json` | `sources`/`origins` dışında **birebir aynı** (özyinelemeli diff, tek fark yok) |
| `robustness_metrics.md` | tek fark: eklenen Level-1 paragrafı + köken satırları |
| `r3w1_joint_optimum.json` | **BAYT ÖZDEŞ** — sha256 `e259be69b3a9…` değişmedi |
| `r3w1_joint_optimum.md` | tek fark: kaynak cümlesi |
| **tablo kapısı** | **885/885, sapma yok** |

`sources` alanı kasten değişti (`results/unified_students/...` → `diagnostics/student_logits/...`)
ve köken kaybolmasın diye yanına `origins` eklendi: her satır için köken koşu dizini +
sha256. Köken azalmadı, arttı.

**r3w1 neden bayt özdeş çıktı.** İki ayrı önbellek vardı: `student_logits_swa.pt` (r3w1'in
okuduğu) ve `logits_swa.npz` (yayımlanan). Aynı sayı mı diye ölçüldü: 12 FERPlus koşusunda
`max |fark| = 0.0`, **bit düzeyinde aynı**. Geçiş bu ölçümden sonra yapıldı.

**r3w1'in val kümesi de koşu dizininden çıktı.** `build_val_with_names()` bir koşunun
`run_args.json`'unu okuyup görüntüleri yüklüyordu; ikisi de yalnız forward için gerekliydi.
Yeni `student_ts_baseline.val_from_published()` etiketleri, oy dağılımını ve dosya adlarını
zaten yayımlı iki artefakttan alıyor (`ferplus_jsd/ferplus_val_logits.pt` +
`configs/FERPlus_majority_metadata.csv`) ve fonksiyonları **ithal ediyor, kopyalamıyor**
(`tstar_stability.ferplus_kept` + `jsd_sensitivity.load_ferplus`). İki modülün etiket
vektörü fonksiyonun içinde ayrıca karşılaştırılıyor; ayrışırlarsa betik durur. Doğrulama:
n=3153, SHA-bölme A=1576 / B=1577 — yayımlanmış `split` ile birebir aynı.

### Kapsam — sessizce yayımlanmayacaklardı

**Aynı kör nokta ikinci kez.** `diagnostics/student_logits/` o gün doğdu ve public'te tek
izlenen dosyası yoktu; senkronun aday taraması yalnız izlenen dosyaların dizinlerini geziyor,
dolayısıyla dizin taramaya **hiç girmedi**. Ölçüldü: kova taramasında `student_logits`
aday sayısı **0**. K2'nin bütün amacı sessizce boşa çıkacaktı. `tests/` tam bu durumdaydı
(8 Ağu, madde 3.1) ve düzeltme aynı yerde: `EXTRA_SCOPE_DIRS`'e açıkça yazıldı.

Kova kuralı **dizine** bakıyor, ada değil — yarın 43. dosya yayımlanırsa elle bir listeye
eklenmesi gerekmesin:

| adım | A | B | C | D (kararsız) | girecek |
|---|---|---|---|---|---|
| dizin kapsam dışıyken | 162 | 32 | 94 | 0 | 195 |
| dizin kapsama girince | 162 | 33 | 94 | **42** | 195 |
| K2 kuralı eklendikten sonra | **205** | 32 | 94 | **0** | **237** |

Sınıflandırma A, çünkü **iddia taşıyorlar**: R3-1 ve R3-W1'in bütün sayıları bu dosyalardan
üretiliyor ve onlar olmadan iki tablo public depoda yeniden üretilemez.

### İkili dosyalarda bayt regex'i — iki yönlü hata

Senkron ilk koşuşta 42 npz'nin **4'ünü** ihlal sayıp yazmayı engelledi. Eşleşmelere bakıldı:

| dosya | eşleşme |
|---|---|
| `RAFDB_stage1_tempscale_T170_…_seed43.npz` | `Q:\N` |
| `RAFDB_stage1_tempscale_T220_…_seed42.npz` | `L:\v` |
| `RAFDB_vae9182_tempscale_T134_…_seed1.npz` | `Y:/b` |
| `RAFDB_vae9182_tempscale_T134_…_seed42.npz` | `e:/v` |

Dördü de **yanlış pozitif** — sıkıştırılmış float dizilerinde tesadüfen sürücü-harfi
biçimine benzeyen baytlar.

**Ve tersi, ki daha önemli:** aynı 42 dosyanın `meta.run_dir` alanı **gerçek** bir mutlak
yol taşıyor (`…\poster-var\results\unified_students\…`) ama `<U536` (UTF-32) saklandığı için
bayt regex'i onu **hiç görmüyor**. Yani bu kontrol ikili dosyalarda hem yanlış alarm verir
hem gerçek olanı kaçırır. Karar ve gerekçesi `public_repo_sync.BINARY_SUF`'un üstünde
yazılı: ikili uzantılar kontrolün dışında.

> **Açıkça beyan:** 42 yayımlanan npz'nin `meta` alanı bu makinenin koşu dizini yolunu
> taşıyor ve **temizlenmedi**. Temizlemek dosyayı yeniden paketlemek olurdu ve K2'nin 1.
> şartını (kaynakla bayt-özdeşlik, sha256 42/42) geçersiz kılardı. `MANIFEST.json` aynı
> bilgiyi depo-göreli biçimde ayrıca yayımlıyor. Bu bir kalıntı değil, iki şart arasında
> verilmiş bir seçim — gizlenmesin diye buraya yazılıyor.

### README

"554 KB" cümlesi ölçülerek genişletildi. Public depoda hâlihazırda yayımlı önbellek
**567.596 bayt = 554 KiB** (4 dosya); yeni 42 dosya **3.518.317 bayt**; toplam
**4.085.913 bayt ≈ 3,9 MB**. Cümle iki gruba ayrıldı, hangi tablonun neden onlara ihtiyaç
duyduğu, bayt-kopyası olmaları, sha256 kapısı ve MANIFEST yazıldı. "Model çıktısı, veri
kümesi içeriği değil" ifadesi somutlaştırıldı: her dosya bir logit matrisi (RAF-DB 3068,
FERPlus 3153 satır) ve etiket vektörüdür; görüntü, oy dağılımı, dosya adı yok.

---

## K3 — iki yer tutucu

**Tanımlıydı, ama örnekleri yanlıştı.** Paragraf `<DATASET_ROOT>` ve `<CHECKPOINT_ROOT>`'un
ikisini de anıyordu; ikincisi "the same way" diye geçiştirilmişti ve birinci örnek
(`train_root: <DATASET_ROOT>/rafdb_aligned`) **hiçbir config'de yok** — RAF-DB config'leri
`data/rafdb_aligned` yazıyor (zaten taşınabilir, yer tutucuya çevrilmedi).

Ölçüm:

| | dosya | eşleşme |
|---|---|---|
| `<DATASET_ROOT>` taşıyan config | 20 | 60 |
| `<CHECKPOINT_ROOT>` taşıyan config | 5 | 5 |
| ikisinden biri (tekil dosya) | **20** | 65 |
| `configs/` altında hâlâ sürücü harfi taşıyan dosya | **0** | 0 |

Düzeltilen paragraf: her iki yer tutucu için **ne olduğu** yazılı, örnekler configs'ten
ölçülmüş (`train_root: <DATASET_ROOT>/AffectNet+`,
`pretrained_local: <CHECKPOINT_ROOT>/best.pt`), niye iki ayrı kök olduğu bir cümleyle,
ve zaten depo-göreli olan config'lerin çevrilmediği ayrıca söylenmiş.

---

## Teyitler

### T1 — 15 mi 21 mi: **ikisi de dosya sayısı, ama farklı popülasyon ve farklı ANDAN**

Kısa cevap: **21/22 doğru olan, 15 yanlış eşleştirilmiş bir sayı.** İkisi de eşleşme değil
dosya sayar (eşleşme sayıları ayrı sütunda ölçüldü: 22 dosya = **100 eşleşme**), yani birim
karışıklığı yok — **daha kötüsü** var: `36→15` yazarken iki ayrı büyüklüğü tek okun iki
ucuna koydum.

| sayı | gerçekte ne | kaynak |
|---|---|---|
| **36** | kontrol turunda kapının bildirdiği kalan **dosya** (27'si bloke edilmiş onaylı aday + 9'u izlenen) | `2026-08-08_kontrol_turu.md:193` |
| **15** | kapı çıktısı **değil** — `[ \t]*$` regex sürümünün CRLF satır sonu yüzünden atladığı dosya sayısı | `2026-08-04_gonderim_gunu_dizisi.md:116` |
| **22** | bugün diskteki tarihli klasörde mutlak yol taşıyan dosya (20 beyanlı + 2 beyansız; bu rapor dahil) | `abs_path_gate.md` |

Bugünün iki tarafı birbiriyle tutarlı ve ölçüldü:

| taraf | soru | sayı |
|---|---|---|
| kaynak | senkronun yazacağı 469 metin dosyası, dönüşüm **öncesi** mutlak yol taşıyan | **140** |
| kaynak | dönüşüm **sonrası** kalan, beyanlı | **19** |
| kaynak | dönüşüm sonrası kalan, beyansız | **0** |
| hedef | tarihli klasörde diskte mutlak yol taşıyan | **22** = 19 + K1'in 2 dosyası + bu rapor |

Popülasyon ayrışması da ölçüldü: 469 = izlenen 279 (88 → 10 beyanlı) + onaylı eklenen 190
(52 → 9 beyanlı). Yani 19'un 10'u 3 Ağu'dan beri yayımda, 9'u 8 Ağu'da kapsama girdi.

**Süreç düzeltmesi.** 36 ve 15 anlık, kaydedilmemiş sayılardı; bugün dosya listeleri
olmadığı için ikisi kalem kalem uzlaştırılamıyor. Kapı artık çıktısını
`diagnostics/reports/abs_path_gate.{md,json}`'a yazıyor — depo günü "36'dan şuna indi,
kalanlar şunlar ve muaf" cümlesi o tablodan kurulur, hafızadan değil.

### T2 — iki boşluk: **ikisi de DÖNÜŞTÜRÜLDÜ**, beyanlı muafa alınmadı

| boşluk | kaynak (poster-var) | yayımlanan hâli |
|---|---|---|
| yorum içindeki yol | `configs/FerPlus.yaml:5` → `train_root: ~ #D:\lg\datasets\fer2013` | `train_root: ~ #<DATASET_ROOT>/fer2013` |
| | `configs/RAFDB_baseline.yaml:5` → `#D:\lg\datasets #set to ~, run valid only` | `#<DATASET_ROOT>/datasets #set to ~, run valid only` |
| çıplak depo kökü | `STATUS.md:14` → ``Audited repo: `poster-var` `` | ``Audited repo: `poster-var` `` |

`configs/` altında yorum içinde sürücü harfi taşıyan **hiçbir satır kalmadı** (ölçüldü:
`grep -rn "#.*[A-Za-z]:[\\/]" configs/*.yaml` boş). İkisi de açık değil, ikisi de muaf değil.

### T3 — mekanizma yan dosyası: **`EXPORTS`'a kayıtlıydı, `SOURCES`'a DEĞİLDİ; kaydedildi**

| izleme yeri | durum |
|---|---|
| `export_to_drive.EXPORTS` | **kayıtlıydı** (`export_to_drive.py:254`, 8 Ağu'da bandın kendi kontrolü yakalamıştı) |
| `table_diff_gate.SOURCES` | **kayıtlı DEĞİLDİ** — 199 koşu × 18 anahtar yayımlanıyor, hiçbir hücre kapısı okumuyordu |

Kaydedildi. Ham yan dosya değil **türevi** (`paper_tables/mechanism_specs.json`) kaydedildi:
199 × 18 ham hücre kapının hücre sayısını 885'ten ~4500'e çıkarır ve denetim sayısını
seyreltirdi; makaleye giren büyüklük zaten türev tablodur. **Sınır açıkça yazılı:** yan
dosyada, mekanizma tablosunda geçmeyen bir koşunun değeri sessizce değişirse bu kapı
kımıldamaz — ama öyle bir değişiklik makalede hiçbir sayıyı da oynatmaz, ki kapının görevi
orası.

Aynı turda ikinci artefakt da kaydedildi: `student_logits/MANIFEST.json` (42 sha256 + özdeşlik
sayacı). Bir kopya sessizce değişirse R3-1/R3-W1 hücreleri zaten kayardı; sha256'ları hücre
yapmak **nedeni** doğrudan gösterir — dosya mı değişti, boru hattı mı.

Kapı koşturuldu: **955 hücre (885'ten), 70 APPEARED, 0 MOVED / 0 CHANGED / 0 VANISHED.**
70'in tamamı iki yeni kaynağın ilk kaydı. K2'nin yol değişikliği bu eklemeden **önce** ve
yalnız başına sınandı (885/885) — sıra kasıtlı: yol değişikliği sayıyı oynatmasın diye önce
o, kapsam genişlemesi diye sonra bu.

### T3'ün üçüncü bulgusu (9 Ağu) — `selection_gain.json` hem KAYITSIZ hem BAYATTI

`parse_args` teyidi sırasında `selection_gain_estimator.py` ilk kez uçtan uca koşturuldu ve
çıktısı **değişti**. Sebep benim düzeltmem değil: artefakt **bayattı**. İçindeki sayılar 105
koşuluk bir popülasyondan üretilmişti, kampanya 199'a büyümüştü ve hiçbir şey bağırmadı —
çünkü `selection_audit/selection_gain.json` `SOURCES`'a **kayıtlı değildi**. `RESULTS_TABLES.md`
T8'in kaynak satırında anılıyor.

| büyüklük | eski (bayat) | yeni (güncel popülasyon) |
|---|---|---|
| `per_k[50].n_runs` | 105 | **199** |
| `per_k[100].n_runs` | 105 | **199** |
| `audit_deltas.b_best_minus_last.n` | 101 | **131** (donmuş denetim) |
| `audit_deltas.c_best_minus_swa.n` | 88 | **118** |
| K=50 `a2_pure_order_statistic` | 0,6418 ± 0,2186 | **0,6312 ± 0,1840** |
| K=100 `a2_pure_order_statistic` | 0,7680 ± 0,2857 | **0,7442 ± 0,2262** |
| K=50 `a1_max_all_minus_mean_lastK` | 0,8594 ± 0,4877 | **0,8078 ± 0,3803** |
| K=100 `a1_max_all_minus_mean_lastK` | 0,8133 ± 0,2844 | **0,7917 ± 0,2351** |
| K=50 `argmax_in_last_K_frac` | 0,3048 | **0,3417** |
| K=100 `argmax_in_last_K_frac` | 0,6476 | **0,6482** |
| `b_best_minus_last.d_acc` | 0,7919 ± 0,4662 | **0,7658 ± 0,4311** |
| `b_best_minus_last.d_ece` | −0,003597 ± 0,009243 | **−0,002879 ± 0,009219** |
| `c_best_minus_swa.d_acc` | 0,1270 ± 0,2500 | **0,1293 ± 0,2620** |
| `c_best_minus_swa.d_ece` | −0,001833 ± 0,010930 | **−0,000577 ± 0,011752** |

**MAKALE TARAFI İÇİN UYARI.** `2026-08-02_r2_2_canonical_sentences.md:64`, §5:402–409'un
sıra-istatistiği cümlesini `selection_gain.json`'a bağlıyor. Eğer o cümle yukarıdaki **eski**
sayıları taşıyorsa güncellenmesi gerekir. Tablo kapısı bunu yakalamadı ve yakalayamazdı:
`RESULTS_TABLES` hücreleri bu değerleri okumuyor (kapı `paper_tables.py` yeniden koşturulduktan
sonra da 955/955 sapma yok dedi). Yön hangi tarafa düşerse düşsün yazılıyor: yeni popülasyon
etkiyi bir miktar **küçültüyor** (a2 K=100: 0,768 → 0,744) ama işaretini ve büyüklük sırasını
değiştirmiyor.

Artefakt kaydedildi: `cells_from_selection_gain` → **969 hücre (955'ten), 14 APPEARED, 0
MOVED / 0 CHANGED / 0 VANISHED.** Bundan sonra aynı bayatlık MOVED olarak bağırır.

---

## Kapıların son çıktısı

### Level-1 — üç aşamada

| | 8 Ağu | 9 Ağu ara | 9 Ağu harness sonrası | **9 Ağu son** |
|---|---|---|---|---|
| geçti | 32 | 34 | 40 | **42** |
| **İHLAL** | **2** | **0** | **2** | **0** |
| muaf | 6 | 7 | 8 | 9 |
| **başka hata** | **8** | **9** | **0** | **0** |

Ortadaki iki sütun turun asıl bilgisi: `başka hata` sütunu "ihlal yok" demek değil, **"soru
sorulamadı"** demekti. 0'a indiğinde İHLAL 0 → 2 oldu, sonra ikisi de kapatıldı. Toplam
üretici 48 → 51 (`publish_student_logits.py`, `abs_path_gate.py`,
`publish_epoch_curves.py`).

**Beş harness arızası bulundu ve beşi de düzeltildi.** Hiçbiri bir sayıyı oynatmadı — her
düzeltmenin ardından ilgili artefakt bayt düzeyinde karşılaştırıldı:

| # | arıza | etkisi | düzeltme |
|---|---|---|---|
| 1 | `level1_gate.GUARD`'ın `glob` sarmalayıcısı `lambda self, pat` | Python 3.13'te `Path.rglob` içten `case_sensitive=` geçiyor → `TypeError` → **`rglob` kullanan her betik "başka hata"** | `**kw` eklendi |
| 2 | `parse_args()` — 4 betik | kapı `runpy` ile çağırıp yolu argv'de bırakıyor → `SystemExit` → soru sorulmuyor | `parse_known_args()`: `abs_path_gate`, `bootstrap_cis`, `public_repo_sync`, `student_ts_baseline` |
| 3 | `level1_gate.py` kendi listesinde | (2) düzeltilince kendini `runpy` ile koşturup **özyineleme** açacaktı (50 × 50 alt süreç) | açık `muaf`: "kapının kendisi" |
| 4 | cp1252 `UnicodeEncodeError` — 2 betik | betik sayıyı üretmeden ilk `print`'te düşüyordu | standart `reconfigure` bloğu: `order_stat_trend`, `tstar_stability` |
| 5 | `stats_convention` importu yol eklemesiz — 2 betik | yalnız CWD=`diagnostics/` iken çalışıyordu; **depo kökünden `ModuleNotFoundError`** (public depo okuru tam bu çağrıyı yapar) | `sys.path.insert` ROOT'tan sonra: `selection_gain_estimator`, `selection_robustness` |

Bayt-özdeşlik doğrulaması (5 betik yeniden koşturuldu):
`order_stat_trend.json` ÖZDEŞ · `tstar_stability.json` ÖZDEŞ · `selection_robustness.json`
ÖZDEŞ · `bootstrap_cis.json` ÖZDEŞ · `student_ts_baseline.json` **ÖZDEŞ** (`1129ad0c…`) ·
`selection_gain.json` **FARKLI — bayatlıktan, düzeltmeden değil** (aşağıda tablosu var).

### Tablo kapısı

**973 hücre / 973 taban · 0 MOVED · 0 CHANGED · 0 VANISHED.**

885 → 955 → 969 → 973: dört yeni kaynak (`mechanism_specs.json`,
`student_logits/MANIFEST.json`, `selection_gain.json`, `epoch_curves_MANIFEST.json`),
88 APPEARED, **hiç MOVED yok**. Her ekleme yalıtılmış koşturuldu ve her yol değişikliği
eklemeden önce tek başına sınandı — `float32` hatası tam bu yüzden yakalandı.

### Mutlak-yol kapısı — son beyanlı liste

**20 dosya, 68 eşleşme, 0 beyansız — KAPI GEÇTİ.** Birim: dosya.

| sınıf | dosya |
|---|---|
| **BEYAN EDİLMEMİŞ** | **0** ✅ |
| tek tek gerekçelendirilmiş kalıntı | 14 |
| üçüncü taraf (POSTERv2/CrossViT mirası) | 3 |
| tarihli rapor sınıfı | 3 |
| **toplam** | **20** |

Beyanlı 20'nin tamamı (üçüncü tarihli kayıt bu rapordur):

| dosya | sınıf |
|---|---|
| `diagnostics/DIAGNOSTIC_REPORT.md` | kalıntı |
| `diagnostics/reports/2026-08-01_calisma_durumu.md` | kalıntı |
| `diagnostics/reports/2026-08-08_final_devir.md` | tarihli |
| `diagnostics/reports/2026-08-08_kapanis_turu.md` | tarihli (bu rapor) |
| `diagnostics/reports/2026-08-08_kontrol_turu.md` | tarihli |
| `run_affectnetplus_unified_student.ps1` | kalıntı |
| `run_ferplus_dual_lr_sam.ps1` | kalıntı |
| `run_ferplus_foreground.ps1` | kalıntı |
| `run_ferplus_other_splits_10e_pretrain.ps1` | kalıntı |
| `run_ferplus_unified_student.ps1` | kalıntı |
| `run_rafdb_kd_resolution_compare.ps1` | kalıntı |
| `run_rafdb_nokd_resolution_compare.ps1` | kalıntı |
| `run_rafdb_unified_student.ps1` | kalıntı |
| `tools/build_ferplus_majority_metadata.py` | kalıntı |
| `tools/eval_rafdb_teacher_student_table.py` | kalıntı |
| `train_affectnetplus_kd.py` | kalıntı |
| `train_rafdb_kd.py` | kalıntı |
| `trails/posterv2/PosterV2_7cls.py` | üçüncü taraf |
| `trails/posterv2/ir50.py` | üçüncü taraf |
| `trails/posterv2/vit_vae_model.py` | üçüncü taraf |

Tam liste ve eşleşme sayıları: `diagnostics/reports/abs_path_gate.md`.

### Depo günü dizisinin birinci kapısı DEĞİŞTİ

`2026-08-04_gonderim_gunu_dizisi.md` 1c'nin birinci kapısı şuydu:

```
grep -rn "D:.5 temmuz claude" . --exclude-dir=.git | wc -l    # 0 OLMALI
```

Desen SADECE kampanya deposunun önekini yakalıyor. **Ölçüldü: o grep 0 derken tarihli
klasörde 22 dosya (100 eşleşme) mutlak yol taşıyordu** — başka veri kökleri, başka kullanıcı
ev dizinleri, UNC payları, JSON kaçışlı çift-ters-bölü. Yani depo günü bu kapı geçerdi ve
**yanlış** geçerdi. Kapı `diagnostics/abs_path_gate.py`'ye çevrildi; desen ve beyan sınıfları
`public_repo_sync`'ten ithal edilir (tek kaynak). Bu, dizinin kendi dersinin ikinci kez
doğrulanmasıdır: *kısmen çalışan bir kontrol, hiç çalışmayandan daha tehlikelidir.*

---

## Depo durumu

| kalem | sayı |
|---|---|
| izlenen dosya | 279 |
| onaylı eklenen | 241 |
| **depo toplamı** | **520** |
| diskte | 530 |
| fazla (kapsamda yok) | **10**, hepsi `__pycache__/*.pyc` — `.gitignore`'da (`__pycache__/`, `*.pyc`), depo içeriği değil |
| eksik (kapsamda var, diskte yok) | **0** |
| senkronun kendi doğrulaması | yazılacak hiçbir dosyada mutlak yol kalmadı |
| `diagnostics/student_logits/` diskte | 43 dosya (42 npz + MANIFEST), 3.544.541 bayt |
| `diagnostics/epoch_curves.npz` diskte | 1.237.133 bayt, sha256 public kopyayla **eş** |
| yayımlı model-çıktısı önbelleği toplamı | **5.323.046 bayt (5,32 MB)** — README'deki sayı |

---

## Mini ihraç

| kalem | değer |
|---|---|
| MANIFEST dosya sayısı | **144** (bu çalışmada 14 yazıldı, 130 zaten aynıydı) |
| toplam | 2726,4 KB |
| defter sha256 | `6e7573a538837523fb13d305b25809a9f6a5c9d3e3d9639028923390fbae2525` |
| defter satır | 199 |
| defter durumu | **önceki ihraçla aynı** |
| makale figürü | 1 yenilendi → `graphical_abstract.pdf` |

138 → 144: `student_logits/MANIFEST.json`, `epoch_curves_MANIFEST.json`,
`reports/abs_path_gate.{md,json}` ve bu rapor banda girdi. Yeni artefaktlar **doğdukları
turda** kaydedildi — bugünün dersi buydu. Kendi `.npz`'leri banda GİRMEZ (3,4 + 1,2 MiB
girdi yığını); bant sayı ve kanıt taşır, girdi taşımaz.

---

## Kapanış beyanı

**1. Repo tarafı hazır mı — EVET.** Dört kapının dördü geçiyor:

| kapı | sonuç |
|---|---|
| mutlak yol | 20 dosya / 68 eşleşme / **0 beyansız** — GEÇTİ |
| Level-1 | geçti 42 · **İHLAL 0** · muaf 9 · başka hata **0** |
| tablo | **973/973** · 0 MOVED / 0 CHANGED / 0 VANISHED |
| senkronun kendi doğrulaması | yazılacak hiçbir dosyada mutlak yol kalmadı |

Kapsam **520** dosya, eksik **0**, kapsam dışı fazlalık **0** (diskteki 10 `.pyc`
`.gitignore`'da). "İHLAL 0" bu kez **51 üreticinin 51'ine soru sorulmuş** hâliyle 0 — 8
Ağu'daki 0 öyle değildi, ve aradaki fark bu turun asıl kazancı.

**2. Windows'ta depo gününe kadar bekleyen iş — YOK.**

Bir yapısal boşluk **beyanlı olarak** duruyor, bekleyen iş değil: `public_repo_sync.py` hâlâ
hiç silmiyor, yani bir dosya A/B'den C'ye taşınırsa diskte kalır. Bu tur o durumu elle
kapattı. Bir `--prune-extras` bayrağı doğru mekanik cevaptır ve yazılmadı — ama kapanış onu
gerektirmiyor, çünkü `abs_path_gate.py` bu sınıfı yakalıyor ve runbook 1c'nin **birinci
kapısı**. Boşluk görünür, kapı kapalı.

**Makale tarafı için bir uyarı** çıktı — repo işi değil, ama beklemez: §5:402–409'un
sıra-istatistiği cümlesi `selection_gain.json`'a bağlı ve o artefakt **105 koşuluk bayat bir
popülasyondan** üretilmişti (şimdi 199). Güncel/eski değerler yukarıda tek tek yazılı;
cümledeki sayıların kontrol edilmesi gerekiyor. Artefakt artık kayıtlı, aynı bayatlık bir
daha sessiz kalmaz.

**3. Tek bekleyen dizi — `2026-08-04_gonderim_gunu_dizisi.md`, ön koşulları TAMAM.** Dizinin
birinci kapısı bu turda değişti (grep → `abs_path_gate.py`), çünkü eski hâli **yanlış
geçiyordu**: o grep 0 derken diskte 22 dosya (100 eşleşme) mutlak yol taşıyordu. Mutlak-yol
beyanlı listesi artık dizinin okuyabileceği bir dosyada duruyor
(`diagnostics/reports/abs_path_gate.md`), hafızada değil — depo günü "36'dan şuna indi,
kalanlar şunlar ve muaf" cümlesi oradan kurulur. Dizi gönderimden 1-2 gün önce koşturulabilir
ve dört kapısının dördü şu an geçiyor.

---

Üretici: elle yazıldı · ölçümler `publish_student_logits.py`, `abs_path_gate.py`,
`level1_gate.py`, `table_diff_gate.py`, `public_repo_sync.py`, `public_scope_buckets.py`,
`export_to_drive.py` çıktılarından
