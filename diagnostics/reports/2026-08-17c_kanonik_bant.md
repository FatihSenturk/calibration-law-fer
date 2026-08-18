# 17 Ağustos 2026 (c) — kanonik T\* ve ihraç bandı (N15)

**Tek cümlelik sonuç: iki karar da uygulandı ve kabul ölçütlerinin üçü de tuttu — öz sınama
11/11'den 13/13'e çıktı (azalmadı), kayıtsız sayı 0 kaldı, kapsam taraması ihlal 0 verdi. Bant
genişletmesi geri alınmadı.** Yeni koşu yok, GPU yok: tamamı önbellek/CPU/dosya.

Bir de karşı-ölçüm: **önerdiğiniz tolerans (basılı hassasiyet = 4 basamak → 5e-5) bugün
TUTMUYOR** — vae9182'nin ayrışması 1.46e-4, yani o eşiğin 2.9 katı. Eşiği elle koymak yerine
**makalenin kendi hassasiyetinden türettim**; gerekçesi ve ölçümü §1.3'te.

| çıktı | ne |
|---|---|
| `diagnostics/tstar_sensitivity.py` | kanonik üretici; yeni `cross_fit` bloğu = teyit kaydı |
| `paper_tables/number_ledger.{md,json}` | yeni `cross_checks` bloğu; T\* bağları kanoniğe çekildi |
| `diagnostics/check_numbers.py` | 4 yeni ihlal sınıfı (ayrışma / yuvarlama / röle / boşa düşen teyit) |
| `diagnostics/check_numbers_selftest.py` | **13/13** (11 + iki yeni teyit senaryosu) |
| `diagnostics/export_to_drive.py` | bant 6 artefakt genişledi (5 karar + 1 sonuç) |
| `diagnostics/table_diff_gate.py` | teyit kaydı ve eşiğin kendisi kapıya girdi |

---

## 1 — Karar 1: T\*_NLL birleştirilmedi, ilan edildi

### 1.1 Önce bir düzeltme: üç artefakt var, ama **iki** hesap

Geçen tur "p4 1.3493927 · tstar_sensitivity 1.3493829" diye iki kaynak bildirmiştim. İzi
sürdüm, tablo şu:

| kaynak | Stage1 T\* | nasıl elde ediyor |
|---|---|---|
| `tstar_sensitivity.results.stage1.T_star_nll` | 1.3493829 | **hesaplıyor** — `student_ts_baseline.fit_ts` (log-uzay Brent, [0.05, 10]) |
| `teacher_ece_grid.stage1.T_star` | 1.3493927 | **hesaplıyor** — `teacher_ece_grid.fit_temperature` |
| `p4_teacher_selection…T_star` | 1.3493927 | **röle** — `TEACHER_GRID[t]["T_star"]`'ı aynen kopyalıyor |
| `tstar_provenance.full_fold_fits.stage1` | 1.3493927 | **röle** — `temperature_fit.json`'ı okuyor |

Üçü de bit düzeyinde aynı (`grid == p4 == temperature_fit` → `True`, üç öğretmen için de). Yani
p4 bağımsız bir hesap **değil**; gerçek ikinci hesap `teacher_ece_grid`. Teyit kaydı bu yüzden
p4'e değil, **hesaplayan kaynağa** kuruldu; p4 ve `tstar_provenance` ise **röle** olarak ayrıca
kaydedildi ve kopya oldukları denetleniyor (bayat bir röle sessizce yanlış bir teyit üretirdi).

### 1.2 Kanonik ilan: `tstar_sensitivity`

Gerekçe sizin: T\*'ın adanmış üreticisi o, ve dağıttığı fit fonksiyonu kampanyanın kullandığı
fonksiyonun kendisi (`fit_ts`). `tab_selection`'ın `T^{*}` sütunu p4'ten kanoniğe çekildi;
`tab_dose_response`'un başlıkları zaten kanoniğe bağlıydı. Yayımlı üç değer değişmedi
(1.349 / 1.261 / 0.983 — kanonik değerlerle de aynı yuvarlanıyor).

### 1.3 Tolerans: elle yazılmadı, makalenin hassasiyetinden türetildi

Önerdiğiniz eşiği ölçtüm ve **tutmadığını** bildiriyorum:

| öğretmen | \|ΔT\*\| ölçülen | 4 basamak eşiği (5e-5) | sonuç |
|---|---|---|---|
| stage1 | 9.87e-06 | 5e-05 | geçer (5.1× marj) |
| primary | 4.05e-06 | 5e-05 | geçer (12× marj) |
| vae9182 | **1.46e-04** | 5e-05 | **GEÇMEZ (2.9× aşıyor)** |

Sebebi vae9182'nin kendine özgü: kalibrasyon tabanında olduğu için NLL yüzeyi optimumun
çevresinde en düz olan öğretmen o, dolayısıyla iki optimize edici birbirinden en uzak oraya
düşüyor. Ama vae9182'nin T\*'ı makalede **4 basamakla hiç basılmıyor** — yalnız 3 (0.983) ve
2 (0.98) basamakla. 4 basamaklı eşiği ona uygulamak, makalenin talep etmediği bir hassasiyeti
denetlemek olurdu.

**Onun için tolerans nicelik başına türetiliyor:**

```
tol = 0.5 × 10^(-d),   d = o niceliğin MAKALEDE kullanıldığı EN SIKI yuvarlama
```

Yani ölçüt şu: *iki kaynak, basılan hiçbir hücreyi değiştirmeyecek kadar yakın olmalı.* Eşik
defterin kendi bağlarından okunuyor (`BINDINGS` içindeki yuvarlamalar), elle yazılmıyor —
bir tablo daha çok basamak basmaya başlarsa eşik **kendiliğinden sıkışır**:

| öğretmen | makaledeki yuvarlamalar | en sıkı | tolerans | ölçülen | marj |
|---|---|---|---|---|---|
| stage1 | 2dp · 3dp · 4dp | 4dp | 5.0e-05 | 9.87e-06 | 5.1× |
| primary | 3dp | 3dp | 5.0e-04 | 4.05e-06 | 123× |
| vae9182 | 2dp · 3dp | 3dp | 5.0e-04 | 1.46e-04 | 3.4× |

İkinci ve daha keskin kapı **yapısal**, sayısal değil: iki kaynak, o alana bağlı **her**
hücrenin beyan edilen yuvarlamasında **aynı** değere gitmek zorunda. Bugün üçünde de gidiyor.

### 1.4 Ayrışmanın anlamsız olduğunun kanıtı: T farkı değil, **amaç farkı**

Bir tolerans "yeterince küçük" diyor, ama küçüklüğün ölçütünü vermez. Kanonik üreticiye eklenen
`cross_fit` bloğu bu yüzden T'deki farkı değil, **`fit_ts`'in küçülttüğü amaç fonksiyonundaki**
farkı ölçüyor: iki aday optimumu NLL ayırt edebiliyor mu?

| öğretmen | \|ΔT\*\| | ΔNLL (teyit − kanonik) | ΔECE |
|---|---|---|---|
| stage1 | 9.87e-06 | **+0.00e+00** | +2e-07 |
| primary | 4.05e-06 | **+0.00e+00** | −2e-07 |
| vae9182 | 1.46e-04 | **+2.98e-08** | +3.8e-05 |

**NLL iki adayı ayırt edemiyor.** İki fit aynı optimumda, kendi yakınsama toleransları içinde;
kalan fark parametreleştirmenin (log-uzay vs lineer kutu), estimandın değil. Bu, "birleştirmeyin"
kararını da doğruluyor: birleştirilecek bir uyuşmazlık yok, korunacak bir çapraz doğrulama var.

FERPlus'ın ikinci bir fiti yok, o yüzden `cross_fit` bloğu da yok — olmayan bir teyidi varmış
gibi yazmak teyidin kendisini değersizleştirir.

### 1.5 Denetçiye giren dört yeni ihlal sınıfı

`cross_source_divergence` (tolerans aşıldı) · `cross_source_rounding_disagreement` (basılı
yuvarlamada ayrı değere gidiyorlar) · `cross_source_relay_drift` (kopyalayan artefakt ayrışmış) ·
`cross_check_unbound` (teyit beyanı makalede hiçbir hücreye denk gelmiyor, dolayısıyla eşiği
türetecek yuvarlama da yok).

Dördü de öz sınamada denendi (§3). Sonuncusu **istenmeden** çıktı: ilk enjeksiyon denemem
kanonik yolu bağsız bir alana çevirmişti ve `cross_source_divergence` beklerken
`cross_check_unbound` aldım — yani senaryo yanlıştı, mekanizma doğruydu. Senaryo düzeltildi ve
`cross_check_unbound` kendi başına bir senaryo olarak eklendi.

## 2 — Karar 2: bant genişletildi, lisans taraması ölçülerek yapıldı

**Beş dosya + bir tanesi Karar 1'in sonucu.** `teacher_ece_grid.json` sizin listenizde yoktu;
teyit kaydının **teyit eden** tarafı orada yaşıyor ve bantta olmayan bir teyit denetlenemez.

Lisans taraması, iddia değil ölçüm — altı dosyanın tamamında:

| ölçülen | sonuç |
|---|---|
| görüntü-adı anahtarı (`*_aligned`, `fer#######`, `.jpg/.png`) | **0** |
| mutlak yol | **0** |
| en büyük dizi | 196 sıcaklık noktası (`ferplus_jsd.sweep`) · 36 koşu satırı (`per_run`) |
| per-örnek dizi | **yok** — hepsi toplulaştırılmış (ortalama/sd/n) |

RAF-DB sözleşmesinin *"no part available to a third party"* maddesini ihlal eden bir türev yok:
dosyalar 3068 görüntülük fold üzerinde **özet** istatistik taşıyor, makalenin zaten bastığı
büyüklükler. Ve belirleyici olan şu — **altısı da hâlihazırda public GitHub deposunda izlenen
dosyalar**, yani Drive bandından daha geniş bir dağıtımda zaten duruyorlar; lisans sorusu bant
genişlemesinden önce de yanıtlanmıştı. Kapsam dışı bırakılan dosya **yok**.

Bant: 178 → **184 dosya**. İhraçta 6 yeni dosya, 0 çakışma.

### 2.1 Bant genişlemesinin beklenmeyen getirisi: Level-1 kapısı iki üreticiyi İLK KEZ gördü

Bandı genişletince Level-1 kapısı **DÜŞTÜ** — ve doğru sebeple. Kapı denetlediği üretici listesini
ihraç bandının üretici sütunundan türetiyor; iki artefaktı kayda geçirmek, üreticilerini ilk kez
kapının kapsamına aldı. İkisi de anında hata verdi:

```
başka hata  diagnostics/ferplus_human_vote_jsd.py — unrecognized arguments: D:\...\poster-var\...
başka hata  diagnostics/ferplus_student_jsd.py    — unrecognized arguments: D:\...\poster-var\...
```

Sebep deponun bilinen arıza sınıfı: kapı üreticileri `runpy` ile çağırıyor ve betiğin **yolu**
argv'de kalıyor; `parse_args` orada `SystemExit` atıyor. Sonuç, kapının kendi diliyle:
*"2 betiğe Level-1 sorusu hiç sorulmadı"* — yani bu iki üreticiye **hiç sorulmamış** bir soru
vardı ve bant genişlemesi onu sordurdu. Aynı arıza `student_ts_baseline.py` ve
`selection_gain_estimator.py`'de daha önce **gerçek bir ihlali saklamıştı**.

İkisi de `parse_known_args`'a çevrildi (deponun standart kuralı, gerekçesi koda yazıldı).
`ferplus_student_jsd.py`'de ek bir tuzak var ve yorumda anıldı: `--checkpoints nargs="+"`
olduğu için bilinmeyen konumsal argüman ona yutulabilirdi.

**Kayıt için:** "kayıtsız artefakt korumasız artefakttır" kuralı bu turda üçüncü kez, bu kez
**üretici tarafında** doğrulandı — artefaktı kayda geçirmek, üreticisini de denetime sokuyor.

### 2.2 Ve soru sorulunca gerçek bir Level-1 İHLALİ çıktı

`parse_known_args` düzeltmesinden sonra kapı iki üreticiye Level-1 sorusunu ilk kez sordu.
`ferplus_human_vote_jsd.py` **geçti**; `ferplus_student_jsd.py` **İHLAL** verdi:

```
RuntimeError: LEVEL1-VIOLATION: ...\results\unified_students
```

Bu artefakt `tab_human`'ın **29 basılı hücresini** besliyor. Sebep: betik pahalı işi (öğrenci
checkpoint'ini yükleyip skorlamak) önbelleğe alıyordu ama önbelleği **koşu dizininin içine**
yazıyordu (`results/.../student_jsd.json`), dolayısıyla üretici o ağaç olmadan hiç koşamıyordu.
Yani `tab_human`, "yayımlı depodan yeniden üretilebilir" değildi — bugün bandı genişletme
gerekçesi olarak yazdığınız cümlenin tam karşılığı.

Düzeltme, deponun kendi deseni (`publish_epoch_curves` → `selection_gain_estimator`, 9 Ağu):
satırlar `diagnostics/ferplus_jsd/ferplus_student_jsd_rows.json` olarak **yayımlandı** ve tablo
üretimi artık onları okuyor. Koşu ağacını taramak ayrı bir eylem: `--from-runs`.

**Bunu "hata olursa yayımlıya düş" diye yazmadım, bilerek.** Öyle yazsaydım betik ağaca yine
dokunur ve kapıyı ancak kapının kendi istisnasını yutarak geçerdi — yani kapıyı oynatmış
olurdum. Varsayılan yol artık koşu ağacına **hiç** dokunmuyor.

Doğrulama: `--from-runs` ile üretilen ve yayımlı satırlardan üretilen
`ferplus_student_jsd.json` **bayt düzeyinde aynı** (sha256 `421f9c5c…` her iki yolda da).

Bir düzeltme daha gerekti ve kapı onu da yakaladı: eklediğim Türkçe satırlar cp1252 konsolda
`UnicodeEncodeError` attı, betiğin çıktısı o güne kadar tümüyle İngilizce olduğu için deponun
standart `reconfigure` bloğu bu dosyada yoktu. Blok eklendi; `PYTHONIOENCODING=cp1252` ile
yeniden koşuldu ve artefaktın sha256'sı değişmedi.

**Bu alt bölümün özeti şu:** bandı genişletmek üç ayrı kusuru ardı ardına görünür kıldı —
sorulamayan Level-1 sorusu, gerçek bir Level-1 ihlali, ve bir kodlama hatası. Üçü de kapının
kendi işleyişiyle çıktı, elle değil.

## 3 — Kabul ölçütleri

| ölçüt | eşik | sonuç |
|---|---|---|
| öz sınama | 11/11 kalmalı | **13/13** — hiçbiri düşmedi, iki teyit senaryosu eklendi |
| kayıtsız sayı | 0 kalmalı | **0** |
| kapsam taraması | ihlal 0 | **0** (public depo, 564 izlenen dosya) |

Öz sınamanın yeni satırları: *teyit kaydı ayrıştı → `cross_source_divergence`* · *teyit beyanı
boşa düştü → `cross_check_unbound`* · *bayat röle → `cross_source_relay_drift`*. Sınanmayan bir
eşik, eşik değildir.

Defter sayımı: **719 jeton · 617 bağlı · 16 türetilmiş · 1 düzyazı bağı · 90 muaf · 0 KAYITSIZ ·
0 uyuşmazlık · 3 teyit kaydı (0 başarısız) · 0 sorun.** Denetçi çıkış 0.

## 4 — Kapılar

| kapı | sonuç |
|---|---|
| tablo farkı | **1441/1441 sapma yok** (1412 → 1441). 29 sapmanın **tamamı APPEARED**; CHANGED/MOVED/VANISHED yok |
| Level-1 | **geçti 58** · İHLAL 0 · muaf 10 · başka hata 0 · zaman aşımı 0 · sorulamadı 0 |
| figür | **10/10**, 0 failing |
| mutlak yol | beyansız **0** · okunamayan 0 |
| `check_numbers` | **çıkış 0** |
| `check_numbers_selftest` | **13/13**, çıkış 0 |

Kapıya giren 29 hücrenin özelliği: aralarında **eşiğin kendisi** var
(`N13/xcheck/*/tolerance`). Eşik makalenin hassasiyetinden türetildiği için tablolar değişince
sessizce kayabilir; kapıda durması o kaymayı görünür kılıyor.

## 5 — Sıraya yazılan: kapının yapısal kör noktası

Bu turda **yapılmadı**, spesifikasyonu `status_queue.txt`'e düştü.

Kör noktanın tanımı: kapı artefaktı **kabul edilmiş temel çizgisiyle** karşılaştırıyor,
**üreticinin taze çıktısıyla** değil. Dolayısıyla *"üretici değişti, artefakt yeniden
üretilmedi"* durumu kapıdan geçiyor. Bugüne kadar bu sınıftan beş vaka elle yakalandı: 0.53'ün
bayat yan tablosu · `tab_selection`'ın ECE sütunu · Fig. 4'ün PDF'i · `main_elsarticle.pdf` ·
ve `two_dataset_overlay.json`'un eksik 42 `per_seed` bloğu.

Sıradaki tur için ölçülecekler (bu turda ölçmedim, çünkü "şimdi yapma" dedin):
üreticiyi koş → çıktıyı depodaki artefaktla **bayt düzeyinde** karşılaştır; ve 58 üreticiyi
**ucuz / pahalı** diye ikiye ayır. Bugünkü tek veri noktası şu: Level-1 kapısı 58 üreticinin
tamamını argümansız koşuyor ve hiçbiri betik-başına 900 s zaman aşımına çarpmıyor (zaman aşımı
0), yani üst sınır bilinsin diye yazıyorum — ama **başına-düşen süre ölçülmedi** ve ayrım o
ölçüm yapılmadan yazılamaz.

Bugünkü tur bu adımın işe yarayacağının bir ön kanıtını da verdi: `ferplus_student_jsd.py`
düzeltilirken artefakt iki yoldan üretilip **bayt düzeyinde** karşılaştırıldı ve aynı çıktı.
Yani önerilen adım, bugün elle yaptığım doğrulamanın kapıya taşınmış hâli.

---

Üretici: `diagnostics/number_ledger.py` (kanonik/teyit beyanları) · kanonik T\* üreticisi:
`diagnostics/tstar_sensitivity.py` (`cross_fit`) · denetçi: `diagnostics/check_numbers.py` ·
öz sınama: `diagnostics/check_numbers_selftest.py` · bant: `diagnostics/export_to_drive.py`.
