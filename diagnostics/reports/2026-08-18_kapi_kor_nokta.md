# 18 Ağustos 2026 — kapının kör noktası, defterin sayımı, depo hijyeni (N16)

**Tek cümlelik sonuç: kör nokta kapatıldı ve kapı ilk koşusunda bu sınıftan ALTINCI vakayı
kendiliğinden buldu; defterin özet tablosu artık toplanıyor; kapsam S1–S3'e genişledi ve kayıtsız
sayı 0'dan 8'e çıktı — sekizi de "bulunamadı", örtülmedi.** Yeni koşu yok, GPU yok.

Windows makinesindeki son tur olduğu için dört işin dördü de burada bitti.

---

## 1 · Kapının yapısal kör noktası — kapatıldı

### 1.1 Önce ölçüm: 58 üreticinin süre dağılımı

Geçen turun tek veri noktası "hiçbiri 900 s'ye çarpmıyor"du; üst sınır biliniyordu, dağılım
bilinmiyordu. Ölçüldü (`--measure`, her üretici bir kez, argümansız):

| | saniye |
|---|---|
| n | 52 |
| min | 0.04 |
| medyan | **0.21** |
| maks | **33.2** |
| toplam | 138 |

En pahalı beşi: `bootstrap_cis` 33.2 · `headroom_grid_audit` 24.6 · `teacher_ece_grid` 7.6 ·
`tstar_sensitivity` 6.1 · `asymmetry_estimand` 5.5.

**Ölçüm ayrımı belirledi, tersi değil.** Medyan 0.2 saniye ve en pahalısı 33 saniye olduğu için
"pahalı üretici" diye bir sınıf pratikte **çıkmadı**: Level-1 temiz olan 52 üreticinin tamamı
Katman A'ya sığıyor (eşik 90 s beyan edildi, hiçbiri yaklaşmıyor bile). Katman B'ye düşenler
süre yüzünden değil, **koşu ağacını okumak işi oldukları için** (Level-3, 8 üretici) düşüyor.
Yani sınıf sınırı zaten var olan bir beyanla çakıştı — ikinci bir liste uydurmaya gerek kalmadı.

### 1.2 Katman A — koş ve bayt karşılaştır

`producer_freshness_gate.py`, üretici→artefakt eşlemesini `export_to_drive.EXPORTS`ten, Level-3
beyanını `level1_gate.ALLOWED`dan **ithal** eder. İki tasarım kararı ölçümden çıktı:

**(a) Kapı artefaktı DEĞİŞTİRMEZ.** Koşudan önce baytlar anlık kopyalanır, koşudan sonra
karşılaştırılır ve dosya **her durumda** geri yazılır. Kapı ölçer, düzeltmez.

**(b) Üretici YAYIMLI DEPO KOŞULLARINDA koşturulur** — yani Level-1 GUARD'ı altında, koşu ağacı
erişilemezken. Bu titizlik değil, karşılaştırmanın *tanımlı* olması meselesi: ilk koşuda
`a12_realsignal_verdict` "BAYAT" göründü, oysa artefakt bayat değildi. Depodaki kopya koşu ağacı
erişilemezken yazılmıştı; bizim koşumuzda ağaç erişilebilirdi ve üretici fazladan tanı satırı
ekledi (`exit_check.param_gate_ran` false → true). **Ölçüm alanlarının hepsi aynıydı.** Ders:
artefaktın baytları "üretici + yayımlanmış girdiler"in fonksiyonu olmalı; özel koşu ağacının
varlığına bağlıysa hakem makinesinde başka bir dosya üretilir.

### 1.3 Katman B — kaynak parmak izi, ama `_provenance` DEĞİL

İstenen tasarım artefaktın içine yazma anında üreticisinin kaynak sha256'sını koymaktı. **İki
artefaktta bu yapılamaz** ve sebebi tasarımdan güçlü:

- `selection_audit.csv` **donmuş** (N=131, 31 Tem kesme). Damga basmak için üreticiyi koşturmak,
  donmuş dosyayı yeniden yazmak demek — kampanyanın en sert kuralı bu dosyanın asla yeniden
  yazılmaması.
- `latency_benchmark.json` **ölçülmüş süreler** taşıyor; yeniden koşmak yayımlanmış sayıları
  değiştirir. Damga uğruna veri değiştirilemez.

Yani "damgalamak için koştur" yolu, korumak istediğimiz artefaktları bozardı.

**Git geçmişi aynı soruyu daha iyi cevaplıyor:** *artefaktın en son yazıldığı commit'ten bu yana
üreticiye dokunan commit var mı?* Varsa "üretici değişti, artefakt yeniden üretilmedi"dir.
Yeniden koşturma yok, dosyaya yazma yok, donmuş artefakt güvende. Artefakt yine de
`_provenance` taşıyorsa o da doğrulanıyor (ileride damga eklenirse çalışsın diye).

### 1.4 Katman B'nin sınırı — peşinen

Kaynak parmak izi **yalnız üretici değişti**yi görür. **Girdi verisi değişti**yi görmez: bir koşu
eklenir, bir CSV tazelenir, bir logit önbelleği büyür — üreticinin kaynağı aynı kaldığı sürece bu
kapı sessizdir. Katman A ikisini de görür. Ayrıca yorum-satırı değişikliği de commit'tir, yani
yanlış pozitif verebilir; bedeli "üreticiyi bir kez koştur ve bak", ucuz.

Hangi artefaktın hangi katmanda olduğu `reports/producer_freshness.md`'de **tablo hâlinde**
duruyor: Katman B satırındaki her artefakt, bu yarım korumayla duruyor demektir.

**Katman B'de duran 12 artefakt — yani girdi-verisi değişikliğine karşı KORUNMAYANLAR:**
`selection_audit/selection_audit.csv` (donmuş) · `…/selection_audit_unfrozen.csv` ·
`…/README.md` · `…/ferplus_selection_audit.csv` · `p5_efficiency/latency_benchmark.json` ·
`epoch_curves_MANIFEST.json` · `student_logits/MANIFEST.json` · `runs.csv` ·
`paper_tables/run_mechanism_params.json` · `paper_tables/control_grid_refinement.{md,json}` ·
`replicate_queue_build.md`. Onikisi de koşu ağacını okumak işi olan üreticilerden; hiçbiri
Katman A'da koşturulamaz çünkü yayımlı depoda o ağaç yok.

### 1.5 Kabul ölçütü: kapı kendini kanıtladı

`--selftest` tarihsel vakayı geri koyar: `two_dataset_overlay.json`'un **42 `per_seed` bloğu**
silinir, Katman A koşturulur.

| senaryo | beklenen | bulunan |
|---|---|---|
| (taban) dokunulmamış artefakt | geçti | **geçti** |
| tarihsel vaka: 42 `per_seed` bloğu silindi | BAYAT | **BAYAT** |

### 1.6 Ve ilk koşuda ALTINCI vaka çıktı

Kapı, kurulduğu gün kendi var oluş sebebini doğruladı: donmuş artefaktlar beyan edilmeden önceki
koşusunda `selection_audit_table.py` **KAYNAK AYRIŞMASI** verdi — üretici, donmuş
`selection_audit.csv` yazıldığından beri commit almış. Bu bir kusur *değil*, dondurmanın tanımı;
`FROZEN` beyanı gerekçesiyle eklendi ve kapı artık onu ihlal saymıyor. Ama şunu gösterdi:
mekanizma gerçekten çalışıyor ve beyanı olmayan her ayrışmayı görüyor.

---

## 2 · Defterin özet tablosu — artık toplanıyor

Haklısınız: 617 + 16 + 90 = 723, beyan edilen toplam 719. **Kategoriler örtüşmüyordu** (bağlı ∩
muaf = 0, ölçüldü); sorun iki farklı muhasebeyi aynı sütuna koymaktı. `derived` ve `prose`
satırları **beyan** sayar; kapsam dışı düzyazıya çapalanmış bir beyan kapsam içi hiçbir jetonu
tüketmez.

Tablo ikiye ayrıldı. Jeton muhasebesi (bugünkü sayılarla):

    687 (bağlı) + 17 (kapsam içi türetilmiş) + 150 (muaf) + 8 (kayıtsız) = 862 jeton ✓

ve ayrı bir tablo, kapsam dışı çapaya bağlı beyanlar: 4 türetilmiş + 1 düzyazı bağı. Toplam
türetilmiş beyan 21 = 17 + 4. Kural tablonun altında yazılı.

**Eski rapora tarihli not düşüldü, metni değiştirilmedi.** Orada da ölçtüm ve bulduğum sizinkinden
biraz farklı: `%96,1` **doğru**, yanlış olan **pay**. 689 = 590 + 10 + 1 + 88 (jeton + beyan
karışımı) ve 689/714 = %96,50. Doğru pay 686'dır: o günün artefaktından ölçüldü (commit
`20a255d`) — 10 türetilmiş beyanın 8'i kapsam içi jetona bağlıydı, 2'si düzyazı çapasıydı, ve
590 + 8 + 88 = 686, 686 + 28 = 714. 686/714 = **%96,08 ≈ %96,1**.

---

## 3 · Kapsam S1–S3'e genişledi

Beyan bayatlamıştı; hüküm S2'ye işlenmişti. Tarayıcıya iki şey eklendi: S2'nin **üç tablosu**
(`tab:app_argmin`, `tab:app_tstar`, `tab:app_jsd`) ve **bölüm düzyazısı** için ayrı bir bulucu.

> Bir tuzak: bölüm etiketleri `SUPP_BLOCKS`'a **konulamaz**. `find_block` bölüm etiketini görünce
> geriye doğru `\begin{table` arar, bulamazsa 0'a düşer ve sessizce önsözden itibaren her şeyi
> tarar — hata vermez, **yanlış** tarar. Ayrı bir bulucu yazıldı; tablo ortamlarının içi düşülüyor
> ki aynı jeton iki kez sayılmasın.

Kapsam **719 → 862 jeton** (+143): `specs` 45 · `robust` 44 · `app_tstar` 23 · `app_jsd` 20 ·
`app_argmin` 11 · `tables` **0**.

**S3 sıfır jeton verdi** ve bu da bir ölçüm: gövdesi yalnız `\input` ve `\ref`, tabloların kendisi
zaten kapsamdaydı.

**İstenen sayılar bağlandı.** 15 Ağustos'taki çelişkiyi üreten hücreler artık alan yolunda:

| basılı | alan |
|---|---|
| `+0.0023` `[+0.0000, +0.0080]` (kontrol) | `bootstrap_cis` → `results.vae9182.point/ci95.headroom_eq8` |
| `+0.0232` `[+0.0151, +0.0305]` (stage1) | `bootstrap_cis` → `results.stage1.…` |
| `+0.0213` `[+0.0154, +0.0280]` (primary) | `bootstrap_cis` → `results.primary.…` |
| `+0.1126` `[+0.1018, +0.1165]` (FERPlus) | `headroom_grid_audit` → `grids.run.headroom` / `.ci95` |
| `0.50`–`2.50` adım `0.02` | `headroom_grid_audit` → `grids.boot.grid.lo/hi/step` |
| `T=0.46` / `T=0.5063` | `grids.fine.T_argmin` / `grids.run.T_argmin` |

**Ve bir ayrımı burada kayda geçiriyorum:** `0.1126`'ya yuvarlanan **üç ayrı alan** var
(`bootstrap_cis`, `headroom_grid_audit`, `headroom_review`) ve makale S2 düzyazısında **koşu
ızgarası** üzerindeki değeri alıyor, `tab:app_tstar` tablosunda ise TS'in kaldırdığı ECE'yi
(`tstar_sensitivity.results.ferplus.ece_removed_by_ts`). İkisi ayrı bağlandı. 15 Ağustos'taki
çelişkinin çıkış noktası tam bu ayrımdı.

S1'in 45 jetonunun tamamı **hiperparametre / formül sabiti / kaynakça** — hiçbiri ölçüm değil,
26 gerekçeli muafiyet sınıfıyla beyan edildi. Tanım: bir sayı ancak bir koşunun **çıktısıysa**
ölçümdür; S1 koşuların **girdisini** yazıyor.

### Kalan 8 kayıtsız — örtülmedi

| kaç | nerede | neden |
|---|---|---|
| 6 | `tab:app_argmin` metrik-uzlaşı sayaçları (`7/7`, `7/7`, `6/7`) | `robustness_metrics` bunları **md'ye basıyor** ama JSON alanı olarak tutmuyor |
| 1 | `tab:app_argmin` FERPlus NLL istisnası `0.74` | aynı sebep |
| 1 | S2 düzyazısı "üç tohum da NLL minimumunu `0.74`'te" | aynı sebep |

Sekizi de tek bir üreticiye bakıyor ve düzeltmesi belli: `robustness_metrics.py` uzlaşı
sayaçlarını JSON'a yazmalı. Tahmin edilmiş bağ yazmadım.

---

## 4 · Depo hijyeni

### 4.1 `.gitattributes` — ve ölçülerek geri alınan bir satır

İlk yazılan satır istendiği gibi `* text=auto eol=lf` idi. **Ölçüm onu çürüttü.** `eol=lf`
çalışma ağacını da LF'e zorlar; bu depodaki üreticiler `Path.write_text()` ile yazıyor ve
Windows'ta `\n` → `\r\n` çevriliyor. Sonuç yeni kapının koşusunda görüldü: `a12_verdict.md`
"BAYAT" göründü, diff 69 satırın 69'unu değişmiş gösterdi, **içerik birebir aynıydı** — tek fark
satır sonu. `eol=lf` ile her üretici koşusu çalışma ağacını kirletir ve Katman A kalıcı olarak
yanlış pozitif verir.

Doğru olan `text=auto` (eol'süz): **depo içeriği** LF'te normalize edilir — Linux/macOS'ta
klonlayan hakem LF görür ve commit'lenmiş blob'un sha256'sı her platformda aynıdır — çalışma
ağacı ise platformun kendi konvansiyonunu alır, dolayısıyla üreticinin yazdığı ile depodaki dosya
aynı makinede eşleşir. Kapının ihtiyacı olan da bu. İkili dosyalar (`*.pdf`, `*.pt`, `*.npz`, …)
ayrıca `binary` olarak beyan edildi; sezgiye bırakılmadı.

### 4.2 `requirements.txt` — artık bir üreticinin çıktısı

`diagnostics/requirements_lock.py` yazıldı. Tanım açık: deponun `.py` dosyalarındaki **top-level
import adları** toplanır, standart kütüphane ve **ölçülerek bulunan** yerel modüller düşülür
(betikler `sys.path`e `diagnostics/` ekliyor, dolayısıyla `import stats_convention` yereldir —
elle tutulan bir liste bunu kaçırıyordu: ilk koşuda 40 satırın 37'si aslında kendi
dosyalarımızdı), kalan her ad `importlib.metadata.packages_distributions()` ile kurulu dağıtıma
eşlenir ve sürüm `==` ile sabitlenir.

**19 dağıtım sabitlendi**, Python 3.13.10. İki şeyi rapora yazıyorum çünkü dosyaya bakan biri
sorar: `numpy==2.4.0rc1` bir **sürüm adayı**, ve hem `opencv-python` hem `opencv-contrib-python`
kurulu (`cv2` ikisine birden eşleniyor). İkisi de ölçülen gerçek, düzeltilmedi.

**Eşlenemeyen üç ad dosyaya yazıldı**, atılmadı: `reportlab`, `svglib`, `svgwrite` — yalnız
`generate_kd_figure.py` kullanıyor ve bu ortamda kurulu değiller. Üretici bu yüzden çıkış kodu
**0** verir: "üç isteğe bağlı bağımlılık kurulu değil" ile "üretici çalışmadı" aynı sinyale
bindirilmemeli.

Eski `requirements_27may.txt` **silinmedi** — depodan silmek onayınıza tabi. Kararınızı bekliyor.

---

## 5 · Kabul ölçütleri

| ölçüt | eşik | sonuç |
|---|---|---|
| öz sınama | 13/13'ten düşmemeli | **14/14** (+ kör nokta senaryosu ayrı kapıda 2/2) |
| kayıtsız sayı | 0 kalmalı; çıkarsa sayısını yaz | **8** — S1–S3 genişlemesinden, hepsi §3'te adıyla |
| kapsam taraması | ihlal 0 | **0** |
| dört kapı | koşulmuş ve raporda | §6 |

Öz sınamada bir senaryo bu turda **kendi ön kabulunu kaybetti** ve sınama bunu yakaladı:
`cross_check_unbound` testi kanonik yolu `results.stage1.T_star_ece`'ye çeviriyordu, ama o alan
bugün S2'nin `app_tstar` tablosuna **bağlandı** — yani artık bağsız değil. Gerçekten bağsız kalan
bir alana (`abs_dT`) çevrildi.

---

## 6 · Kapılar

| kapı | sonuç |
|---|---|
| **üretici tazeliği (YENİ)** | **GEÇTİ** — Katman A 52 · Katman B 8 · BAYAT 0 · kaynak ayrışması 0 · ölçülemez 0 · başka hata 0 |
| üretici tazeliği — öz sınama | **2/2** (taban geçti · tarihsel vaka BAYAT) |
| tablo farkı | **1453/1453 sapma yok** (1441 → 1453). 19 sapmanın 7'si MOVED (defterin kendi sayaçları), 12'si APPEARED; **CHANGED/VANISHED yok** |
| Level-1 | **geçti 58** · İHLAL 0 · muaf 10 · başka hata 0 · zaman aşımı 0 |
| figür | **10/10**, 0 failing |
| mutlak yol | beyansız **0** · okunamayan 0 |
| public kapsam taraması | ihlal **0** |
| `check_numbers` | **çıkış 1** — 8 kayıtsız (S1–S3 genişlemesinden), 0 uyuşmazlık, 0 kayma |
| `check_numbers_selftest` | **14/14 yakalandı** |

`check_numbers`in kırmızı olması bu turda **doğru durum**: kapsam genişledi, sekiz sayının
kaynağı gösterilemiyor ve yeşil bir kapı onları görünmez yapardı.

---

## 7 · İstemediğiniz iş: `sections/*.tex` düzyazısının maliyeti

Bağlamadım — hareket eden hedefi bağlamak çürük bağ üretir. **Ölçtüm:**

| dosya | jeton | değeri kayıtlı bir artefaktta var | yok |
|---|---|---|---|
| `01_introduction` | 40 | 40 | 0 |
| `02_related_work` | 10 | 10 | 0 |
| `03_methodology` | 150 | 141 | 9 |
| `04_experiments` | 156 | 122 | 34 |
| `05_results_discussion` | 461 | 429 | 32 |
| `06_conclusion` | 4 | 3 | 1 |
| **toplam** | **821** | **745 (%90,7)** | **76** |

Üç not, üçü de kararı etkiler:

1. **Jeton sayısı tahmininizin neredeyse iki katı: ~470 değil 821.** Yerleşim jetonları
   (`\linewidth`, `pt`, `\multicolumn`) zaten düşülmüş hâlde.
2. **%90,7 bir ÜST SINIRDIR, bağlanabilirlik değil.** Bu sütun "bu değer 24 kayıtlı artefaktın
   herhangi birinde geçiyor mu" sorusunu soruyor — N13'te ölçtüğümüz **varlık kontrolünün**
   ta kendisi, ve o kontrol makalenin %98,9'unu eşlerken dört bayat değerin yalnız birini
   yakalamıştı. Gerçek bağlanabilirlik bundan düşük; kesin sayı ancak bağ kurulurken çıkar.
3. **Eşleşmeyen 76'nın büyük kısmı ölçüm değil**: görüntü boyutu (`224×224`), öğretmen adındaki
   basamak (`VAE9182`), binlik ayracıyla bölünen veri kümesi sayımları (`15{,}339` → `339`),
   yıl/epok. Ama içlerinde **gerçek ölçüm de var** ve üreticisi yok: `%29,3` ve `%37,3` (oy
   toplamı ondan az olan satırların oranı) hiçbir kayıtlı alana bağlanmıyor.

Karar okuma bitince verilecek; bu sayılar o kararın girdisi.

---

Üretici: `diagnostics/producer_freshness_gate.py` (`--measure` / `--selftest`) ·
`diagnostics/requirements_lock.py` · defter: `diagnostics/number_ledger.py` · tarayıcı:
`diagnostics/paper_number_scan.py`.
