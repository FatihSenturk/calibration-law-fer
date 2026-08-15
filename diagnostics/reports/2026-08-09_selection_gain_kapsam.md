# selection_gain popülasyonu — sıra-istatistiği donmuş kümeye kısıtlandı

**Tarih:** 9 Ağu 2026
**Girdi:** `planning/ide_selection_gain_kapsam_2026-08-09.md`
**Karar (Fatih):** sıra-istatistiği bileşeni donmuş denetim kümesine kısıtlanacak; geniş
popülasyon silinmeyecek, robustluk satırı olarak duracak.

---

## 1. Varsayımın düzeltilmesi: eski 105, donmuş alt küme DEĞİLDİ

Soru şuydu: *"Sıra-istatistiği, donmuş `selection_audit.csv`'deki 131 koşunun epok-günlüğü
olan alt kümesi üzerinde hesaplansın. O alt kümenin n'i kaç? (Eski 105 buydu sanıyorum —
teyit et.)"*

**Teyit edilemedi — hipotez yanlış.** Ölçüm:

| soru | ölçülen |
|---|---|
| donmuş denetimdeki tekil (koşu, zaman damgası) çifti | **131** |
| bunlardan epok eğrisi yayımlı olan | **131** (hepsi) |
| `len(acc) ≥ 20` filtresini geçen | **131** |
| K=50 filtresini (`len(acc) ≥ 60`) geçen | **131** |
| K=100 filtresini (`len(acc) ≥ 110`) geçen | **131** |
| donmuş kümede olup geniş RAF-DB kümesinde olmayan | **0** (donmuş ⊂ geniş) |

Yani donmuş kümenin epok-günlüğü olan alt kümesi **131**, 105 değil. Hiçbir koşu
filtrelerden düşmüyor.

### O hâlde 105 neydi

Kökeni izlendi. Makalenin §5.6 paragrafı **üç ayrı yerden** besleniyor ve **ikisi farklı
popülasyon**:

| makaledeki değer | kaynak artefakt | popülasyon |
|---|---|---|
| K=50 ham `+0.642 ± 0.219` | `selection_gain.json` (**bayat**) | **n=105, geniş RAF-DB** (o günkü hâli) |
| K=100 ham `+0.768 ± 0.286` | `selection_gain.json` (**bayat**) | **n=105, geniş RAF-DB** |
| `argmax_in_last_K` %30 / %65 | `selection_gain.json` (**bayat**) | **n=105, geniş RAF-DB** (0,3048 / 0,6476) |
| de-trend `+0.640` / `+0.728` | `order_stat_trend.json` | **n=131, donmuş küme** ✅ |
| `best − last +0.77 ± 0.43` | `selection_gain.json` audit_deltas | **n=131, donmuş küme** ✅ |

Yani kayma tahmin edilenden bir adım daha derin: paragraf donmuş kümeyle açılıyor, ham
sıra-istatistiği ve argmax oranları **geniş-105**'ten geliyor, de-trend edilmiş sürüm ise
**donmuş-131**'den. Aynı cümlede iki popülasyon.

### Çapa uyuşmazlığı MASKELEDİ

`order_stat_trend.py` içinde bir çapa kontrolü var: `PUBLISHED_A2 = {50: 0.642, 100: 0.768}`
ve `ANCHOR_TOL = 0.02` — "küme uyuşmazsa DUR" demek için yazılmış. Donmuş-131'in değerleri
0,6445 / 0,7640; sapma **0,0025 / 0,0040**, toleransın altında. Çapa geçti ve popülasyon
uyuşmazlığını **görünmez kıldı**.

Çapa sayısı **düşürülmedi** — o hâlâ makalenin yayımlı değeri ve makale değişmeden onu
değiştirmek "beyan et, sonra uygula" sırasını bozar. Bunun yerine uyuşmazlık artefaktta
görünür kılındı: `anchor_population` ve `anchor_population_matches: false` alanları eklendi,
gerekçesi kodda yazılı. **§5.6 donmuş kümeye güncellenince bu iki sayı da güncellenmeli,**
yoksa çapa yanlış popülasyonu kutsamaya devam eder.

---

## 2–3. İstenen tablo: donmuş 131 (birincil) ve geniş 199 (robustluk)

`selection_gain_estimator.py`'nin birincil popülasyonu artık donmuş küme; geniş popülasyon
`per_k_rafdb_all` altında duruyor (silinmedi).

### Sıra istatistiği

| büyüklük | K | **donmuş 131 (birincil)** | geniş 199 (robustluk) | makale (geniş-105) |
|---|---|---|---|---|
| a2 = max(son K) − ort(son K) | 50 | **+0,644531 ± 0,203260** | +0,631220 ± 0,184049 | +0,642 ± 0,219 |
| a2 | 100 | **+0,763953 ± 0,258768** | +0,744200 ± 0,226152 | +0,768 ± 0,286 |
| a2 de-trend (OLS) | 50 | **+0,640246 ± 0,218167** | — | +0,640 |
| a2 de-trend | 100 | **+0,728036 ± 0,238320** | — | +0,728 |
| pencere sürüklenmesi | 50 | +0,146428 ± 0,515240 | — | — |
| pencere sürüklenmesi | 100 | −0,015466 ± 0,434982 | — | — |
| `argmax_in_last_K` | 50 | **0,343511 (%34,4)** | 0,341709 (%34,2) | %30 (0,3048) |
| `argmax_in_last_K` | 100 | **0,671756 (%67,2)** | 0,648241 (%64,8) | %65 (0,6476) |
| a1 = max(TÜM) − ort(son K) | 50 | **+0,838356 ± 0,441583** | +0,807787 ± 0,380253 | — |
| a1 | 100 | **+0,805754 ± 0,258099** | +0,791700 ± 0,235064 | — |
| val_loss(seçilen) − ort val_loss(son K) | 50 | **−0,015114 ± 0,024196** | −0,012822 ± 0,020708 | — |
| aynısı | 100 | **−0,013653 ± 0,016074** | −0,012256 ± 0,014320 | — |

De-trend edilmiş sürümler `order_stat_trend.py`'den; o betik zaten donmuş küme üzerinde
çalışıyordu ve geniş popülasyona hiç geçmemişti.

### Denetim deltaları (değişmedi, hep donmuş kümeydi)

| kontrast | n | Δacc (pp) | ΔECE |
|---|---|---|---|
| best − last | 131 | +0,765847 ± 0,431079 | −0,002879 ± 0,009219 |
| best − swa | 118 | +0,129273 ± 0,262039 | −0,000577 ± 0,011752 |

### Çapraz doğrulama — iki bağımsız betik, aynı küme, aynı sayı

`selection_gain_estimator.py` ve `order_stat_trend.py` a2'yi birbirinden bağımsız hesaplıyor
(biri `epoch_curves` üzerinden kendi döngüsüyle, diğeri kendi OLS boru hattıyla). Aynı donmuş
131 üzerinde:

| K | selection_gain | order_stat_trend | fark |
|---|---|---|---|
| 50 | 0,644530584277 ± 0,203259742562 | 0,644530584277 ± 0,203259742562 | **0,00e+00 / 0,00e+00** |
| 100 | 0,763953429709 ± 0,258768035354 | 0,763953429709 ± 0,258768035354 | **0,00e+00 / 0,00e+00** |

### Makaleye ne değişiyor (yorum değil, fark)

Donmuş kümeye geçince ham a2 **büyüyor** (0,642 → 0,6445 ve 0,768 → 0,7640; K=100'de biraz
küçülüyor), `argmax_in_last_K` **belirgin biçimde büyüyor** (%30 → %34,4 ve %65 → %67,2).
De-trend edilmiş değerler **değişmiyor** — onlar zaten donmuş kümedendi. Yani §5.6'nın
sayılarından yalnız ham a2 çifti ve iki argmax oranı güncellenecek; de-trend satırı olduğu
gibi kalıyor.

---

## 4. Geniş popülasyon korundu

`selection_gain.json` artık iki blok taşıyor ve hangisinin ne olduğu dosyanın içinde yazılı:

```json
"population": {
  "per_k": "frozen selection audit set (131 runs)",
  "per_k_rafdb_all": "all finished RAF-DB runs (199 runs)",
  "audit_deltas": "frozen selection audit set",
  "decision": "9 Aug 2026: the order-statistic component is restricted to the frozen set
               so that the total (b/c) and its component (a) come from the same runs.
               The wider population is kept as a robustness row, not as the paper's
               main sentence."
}
```

İkisi de tablo kapısına kayıtlı (`T8/…` birincil, `T8w/…` robustluk) — yayımlanan ama
izlenmeyen blok bırakılmadı.

---

## 5. Kapı kuralı sabitlendi: hata sınıfı boş değilken GEÇTİ raporlanmaz

Kural üç kapının **koduna** yazıldı, çıktı biçimine dahil edildi. Her kapı artık ayrı bir
`SONUÇ` satırı basıyor ve hata sınıfını o satırda sayıyor.

| kapı | eskiden ne yapıyordu | şimdi |
|---|---|---|
| `level1_gate.py` | `başka hata` sütununu basıp yalnız İHLAL'e göre çıkış kodu veriyordu — 8 Ağu'da 9 kalem varken "İHLAL 0" dedi | `DECLARED_ERRORS` (**boş**) + `ERROR_CLASSES`; beyansız her "sorulamadı" kalemi kapıyı düşürür, `SONUÇ` satırı ikisini birlikte sayar |
| `table_diff_gate.py` | `NOTE missing sources: …` yazıp **ardından** "No deviation … accepted baseline" diyor ve çıkış kodu 0 döndürüyordu | `DECLARED_MISSING` (**boş**); okunamayan kaynak varsa GEÇTİ raporlanmaz, çıkış kodu 1 |
| `abs_path_gate.py` | `except OSError: continue` — okunamayan dosyayı sessizce atlıyordu | okunamayanlar sayılıp raporlanıyor; sıfır değilse kapı düşer |

Gerekçe üçünde de aynı ve kodda yazılı: **hata sınıfı "ihlal yok" demek değil, "soru
sorulamadı" demek.** 8 Ağu'da `başka hata 9` tam bu yüzden üç gerçek ihlali gizledi.

`DECLARED_ERRORS` ve `DECLARED_MISSING` bilerek boş. Bir kalem oraya yazılacaksa gerekçesi
"neden bu betiğe soru sormak MÜMKÜN DEĞİL" olmak zorunda; "şimdilik bakılmadı" gerekçe
değildir.

---

## 6. README

| istek | durum |
|---|---|
| `epoch_curves.npz`'nin float64 olduğu, gerekçesiyle | ✅ paragraf yazıldı: repack olduğu, float32'nin argmax seçimini değiştirdiği, ölçülmüş olduğu |
| "okuyucu küçültmek isteyebilir" uyarısı | ✅ **"So please do not shrink this file."** — 761 KB'a inince iki tablonun üretilemediği, ölçüldüğü yazılı |
| 199 / 76.700 güncel sayısı | ✅ tabloda: "199 runs, 76,700 epochs" |

Yayımlı model-çıktısı önbelleği toplamı README'de **5,3 MB** (ölçüldü: 5.323.046 bayt).

---

## Kapıların çıktısı

| kapı | sonuç |
|---|---|
| mutlak yol | 20 dosya / 68 eşleşme / beyansız **0** / okunamayan **0** — **KAPI GEÇTİ** |
| Level-1 | geçti 42 · İHLAL **0** · muaf 9 · başka hata **0** — **SONUÇ: GEÇTİ** |
| tablo | **983/983** · 0 MOVED / 0 CHANGED / 0 VANISHED |

Tablo kapısı bu turda **20 sapma** verdi ve hepsi kabul edildi: 8 `n CHANGED` + 2 `MOVED`
(ikisi de `n_runs` 199→131) + 10 `APPEARED` (T8w robustluk bloğunun ilk kaydı). Hiçbiri
bağımsız bir değer kayması değil; hepsi bilerek yapılan popülasyon değişiminin türevi. Kabul
gerekçesi tabanda tam metin olarak duruyor.

---

## Açık kalan tek kalem — makale tarafı

§5.6'nın ham a2 çifti ve iki `argmax_in_last_K` oranı geniş-105'ten geliyor; yukarıdaki
donmuş-131 değerleriyle güncellenmesi gerekiyor. T8'in `n = 105` satırı da **131** olacak.
Güncelleme yapıldıktan sonra `order_stat_trend.PUBLISHED_A2` çapası yeni değerlere
(0,6445 / 0,7640) çevrilmeli — aksi hâlde çapa eski popülasyonu kutsamaya devam eder ve
`anchor_population_matches` kalıcı olarak `false` kalır.

---

## EK — aynı gün, makale güncellemesinden SONRA

Yukarıdaki bölümler makale güncellenmeden önce yazıldı; bu ek ondan sonrasını kaydeder. Üstteki
"Açık kalan tek kalem" bölümü **olduğu gibi bırakıldı** (o saatin gerçeğiydi); kapandığı burada
yazılıdır.

Fatih: T8 ve §5.6 donmuş-131 değerlerine çevrildi (ham a2 +0,645 / +0,764, argmax %34 / %67).
Bunun üzerine çapa hizalandı.

| alan | önce | sonra |
|---|---|---|
| `PUBLISHED_A2` | {50: 0.642, 100: 0.768} | **{50: 0.6445, 100: 0.7640}** |
| `ANCHOR_POPULATION` | geniş RAF-DB, n=105 (yayımlandığı günkü hâl) | **donmuş denetim kümesi** |
| `anchor_population_matches` | `false` | **`true`** |
| `ANCHOR_TOL` | 0.02 | **0.001** |
| ölçülen sapma | 0,0025 / 0,0040 | **3,1e-05 / 4,7e-05** |

`anchor_population_matches` elle çevrilen bir bayrak değil, iki tanımın karşılaştırması
(`ANCHOR_POPULATION == POPULATION`): çapa başka bir popülasyona geri alınırsa kendiliğinden
`false` olur.

**Tolerans neden daraltıldı.** 0,02 bu sabahki maskelemeyi mümkün kılan değerdi: gerçek bir
popülasyon uyuşmazlığı (0,0025 / 0,0040) eşiğin altında kaldı ve çapa GEÇTİ dedi. Yeni eşiğin
taşıması gereken tek şey makaledeki 4 haneli yuvarlama (~5e-05); yakalaması gereken şey
popülasyon kayması, ki donmuş-131 ile geniş-199 arasında **0,0133** (K=50) ve **0,0198** (K=100)
pp — ikisi de 0,001'in üstünde. Yani bugün maskelenen olay bu eşikle durdurulur. Gevşek bir çapa
çapa değildir.

### Beklenti tutmadı: 1 MOVED değil, 16 APPEARED

Beklenen "tablo kapısında 1 MOVED" **çıkmadı** — çapa değişikliği kapıda hiç görünmedi, çünkü
`diagnostics/paper_tables/order_stat_trend.json` **SOURCES'a kayıtlı değildi**. Yayımlı, Drive'a
ihraç edilen, genel depoda duran ve §5.6'nın **de-trend a2 çiftini taşıyan** bir artefakt kapının
tamamen dışındaydı — `selection_gain.json` ile birebir aynı sınıf, aynı günün ikinci vakası.
"Kayıtsız bir tablo korumasız bir tablodur" bugün **üçüncü** kez doğrulandı, bu kez çapanın
kendisi üzerinden.

Artefakt kaydedildi (`cells_from_order_stat_trend`), 16 sapmanın **tamamı APPEARED**: K başına 7
hücre (ham a2, de-trend a2, eğim, sürüklenme, `published_a2`, `anchor_dev`,
`anchor_pop_matches`) + 2 büyüme oranı. **MOVED yok**, çünkü popülasyon değişmedi: n=131 aynen,
a2 0,644531 / 0,763953 aynen, de-trend 0,640246 / 0,728036 aynen. Değişen tek şey çapa sabiti ve
tolerans — ve onlar da artık hücre.

**Çapanın kendisi de izleniyor.** `published_a2` / `anchor_dev` / `anchor_pop_matches` hücre
olarak kayıtlı; bundan sonra bir eşiğin gevşetilmesi ya da çapanın başka bir popülasyona geri
alınması da MOVED üretir. Denetim aracının sessizce zayıflatılması, bu sabah gerçekten olan bir
şeydi.

### İkinci düzeltme: sayı olmayan hücreler artık kıyaslanıyor

`compare()`'in koşulu `_num(v) and _num(bv)` ile başlıyordu; yani hüküm/durum dizgileri,
sha256'lar ve bool'lar tabana **yazılıyor ama hiç kıyaslanmıyordu** — `"GEÇTİ"` → `"DÜŞTÜ"`
dönmesi kapıyı kımıldatmazdı. Kaydedilip kıyaslanmayan hücre yalnızca görünüşte korunur; bu
turun kuralının aynı ailesi. Tam eşitlik kıyası eklendi. **Bu koşuda sayı olmayan hiçbir hücre
sapmadı**, yani geriye dönük denetim de temiz çıktı.

### Karar kayda geçti: README'ye AI ifşa cümlesi eklenmiyor

Fatih'in kararı. Gerekçe: **gereklilik yok, norm yok, doğrulama zaten kapılarla kurulu.** Bu
depoda bir sayının nasıl üretildiği cümleyle değil, üreticiyle kanıtlanıyor — her tablo satırı
`Producer:` alanı taşıyor, Level-1 kapısı 42 üreticinin koşu dizinlerine dokunmadığını her
koşuda yeniden ölçüyor, tablo kapısı 999 hücreyi tabana karşı tutuyor, mutlak-yol kapısı
yayımlanan her baytı tarıyor. Beyan yerine mekanizma. Karar bu turda uygulanmadı, yani README'de
böyle bir cümle yok ve eklenmeyecek.

### Üçüncü bulgu: bayatlık raporu YANLIŞ DEPOYU ölçüyordu

"Kalan bir şey var mı" sorusu ölçülünce çıktı. `public_repo_staleness.py` hedefini **elle**
tutuyordu: `...\public\calibration-law-fer`. Oysa 8 Ağu'da `public_repo_sync.PUBLIC` tarihli
klasöre taşınmıştı (`calibration-law-fer_2026-08-08`) ve eskisi `PUBLIC_ROLLBACK` olarak geride
bırakılmıştı — **bu betik taşınmadı.**

| | dosya | son değişiklik |
|---|---|---|
| ölçtüğü (eski) | 289 | 2026-08-08 00:58 |
| yayımlanan (güncel) | 531 | 2026-08-09 16:31 |

Rapor her koşuda düzgünce üretiliyor, "**64 BAYAT**" gibi somut sayılar basıyor ve **Drive'a
ihraç ediliyordu**; yalnızca artık yayımlanmayan klasörü anlatıyordu. Yanlış soruyu doğru
cevaplayan bir rapor, cevapsız rapordan daha kötüdür: geçer not verir.

**İkinci kat.** Hedef düzeltilince 64 → 13'e indi, ama 13 de yanlıştı. Bu betiğin
normalleştiricisi yalnız `.py` dosyalarındaki `ROOT = Path(...)` satırını biliyordu; oysa
`public_repo_sync.transform` mutlak yolları **CSV/JSON/YAML/MD içinde de** yeniden yazıyor —
`runs.csv`'nin her satırındaki `run_dir` en büyük örneği (79.211 → 73.241 bayt, satır başına
~30 bayt, yani tam bir yol öneki). Ölçtüm: **13 dosyanın 13'ü de** eşitlemenin kendi
`transform`'uyla birebir açıklanıyor, bayatlık değil.

Yani iki araç aynı soruya iki cevap veriyordu (eşitleme "0 güncellenecek", rapor "64 BAYAT") ve
her biri kendi içinde tutarlıydı. İkisi de tek kaynağa bağlandı — hedef **ve** normalleştirici
`public_repo_sync`'ten ithal ediliyor, ikinci bir kopya tutulmuyor (`abs_path_gate` deseni).

| | önce | sonra |
|---|---|---|
| GERÇEK BAYAT | 64 (yanlış klasör) → 13 (yanlış normalleştirici) | **0** |
| aynı / satır sonu / uyarlama | 82 / 76 / 52 | **115 / 80 / 79** |

Toplam 274 ve **79 uyarlama** — eşitlemenin kendi çıktısıyla (`0 güncellenecek · 274 zaten aynı
· UYARLAMA 79`) birebir aynı. Artık çapraz doğrulanıyorlar.

### Ek sonrası kapılar

| kapı | sonuç |
|---|---|
| mutlak yol | 20 dosya / 68 eşleşme / beyansız **0** / okunamayan **0** — **KAPI GEÇTİ** |
| Level-1 | geçti 42 · İHLAL **0** · muaf 9 · başka hata **0** — **SONUÇ: GEÇTİ** |
| tablo | **999/999** · 0 MOVED / 0 CHANGED / 0 APPEARED / 0 VANISHED |

Hücre sayısı 983 → **999**.

Eşitleme: genel depoda 6 dosya güncellendi, 268 zaten aynı, yazılan hiçbir dosyada mutlak yol
kalmadı. Mini ihraç: **145 dosya** (11 yazıldı, 134 aynı), koşu defteri **değişmedi**
(`runs.csv` sha256 `6e7573a5…`, 199 satır) — yani sayılar aynı defterden. Tekrar koşuda 144/145
bayt bayt aynı; farklı çıkan tek dosya `STATUS.md`, çünkü ihraç zaman damgasıyla ihraçtan hemen
önce tazeleniyor (tasarım, `export_to_drive.py:458`).

---

Üretici: elle yazıldı · ölçümler `selection_gain_estimator.py`, `order_stat_trend.py`,
`publish_epoch_curves.py`, `level1_gate.py`, `table_diff_gate.py`, `abs_path_gate.py`
çıktılarından
