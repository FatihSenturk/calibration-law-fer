# 19 Ağustos 2026 — okuma turu 1: tek küme dört ad, çakışan 0.74, iki açık kalem (N18)

**Tek cümlelik sonuç: dört ad gerçekten tek kümeyi gösteriyor ve "official test set" doğru ad;
0.74 hipotezi ÜÇ bağımsız ölçümle ÇÜRÜDÜ; Zenodo DOI'si zaten yayımda ve çözünüyor — bloke edici
değil; ölü dosya ölü ve onu görünmez kılan bir kod hatası üç betikte bulunup kapatıldı.**

Bu bir ölçüm turu. Aşağıda karar yok, sayı ve kanıt yolu var. Üç yerde sizin ön kabulünüzü
düzeltiyorum, bir yerde **kendi dünkü cümlemi**, bir yerde de kendi bugünkü ilk okumamı.

> Ölçümler yedi paralel ajanla toplandı, sonra her biri **çürütmeye çalışan** ikinci bir ajana
> verildi. Çürütme turu işe yaradı: aşağıdaki §2.4 ve §2.5 oradan çıktı ve **benim ilk okumamı
> kırdı**. Çürütmelerin hepsini artefaktı kendim açıp yeniden ölçtüm; ajan çıktısı kanıt değildir.

---

## 1 · Tek küme, dört ad — ölçüldü

### 1.1 Cevap üretici çıktısı olarak duruyor, raporda cümle olarak değil

Yeni üretici: **`diagnostics/split_identity.py`** → `paper_tables/split_identity.{md,json}`.
Gerekçe kampanyanın kendi kuralı: bir raporda elle yazılmış tablo bir **iddiadır**; bu sayıların
denetlenebilir olması için bir artefakt alanı gerekiyordu. Artık `table_diff_gate` de bu 15
hücreyi izliyor.

> **Level-1 / lisans.** RAF-DB meta CSV'si görüntü adı taşır ve yayımlanamaz. Varsayılan yol
> CSV'yi **okumaz**; yayımlanan sayım dosyasını okur
> (`split_identity/rafdb_fold_class_counts.json`, **364 bayt**, yalnız fold × etiket sayıları —
> içinde tek bir görüntü adı yok). CSV'yi okumak açık bir eylem: `--from-data`. İki yol da
> **bayt-özdeş** artefakt üretiyor (sha256 `48dacbbd9f350855`, iki koşuda da aynı).

### 1.2 Tek denklem

| veri kümesi | eğitim fold | raporlanan fold | resmî bölüm | n (eğitim) | n (raporlanan) | meta'da bölüm | ayrı held-out | seçim = raporlama |
|---|---|---|---|---|---|---|---|---|
| RAF-DB | `[2]` | `[3]` | `test/` | 12 271 | **3 068** | **2** | yok | **EVET** |
| FERPlus | `[0, 1]` | `[2]` | `FER2013Test` | 28 259 | **3 153** | **3** | **VARDI** | **EVET** |

Alan yolları: `split_identity.json → datasets.<ad>.{n_train, n_reporting, val_folds,
reporting_partition, n_partitions_in_metadata}`.

### 1.3 RAF-DB: fold 3 gerçekten resmî test bölümü — küme düzeyinde

Sayı eşitliği yetmez, **küme** eşitliği ölçüldü:

* fold 3'ün **3068 satırının 3068'i** `test/` altında, 0'ı `train/` altında; çapraz tablo tam
  köşegen (aynısı fold 2 / `train/` için).
* CSV-fold3 ile diskteki `test/` dizini **küme olarak eşit**: iki yönde de fark 0.
* fold 2 ∩ fold 3 = **0**; CSV'de yinelenen yol **0**.
* Metada **başka fold değeri yok** — yalnız 2 ve 3.
* Sınıf dağılımı RAF-DB'nin yayımlanmış test dağılımıyla **birebir**: Surprise 329 · Fear 74 ·
  Disgust 160 · Happiness 1185 · Sadness 478 · Anger 162 · Neutral 680 (toplam 3068). Makalenin
  "per-class counts match the published distribution exactly" cümlesi **doğrulandı**.

`n=3068` beş bağımsız yerden aynı çıkıyor: CSV/disk sayımı · koşu log'u
(`Dataset loaded: 12271 train, 3068 val.`) · `bootstrap_cis.json → results.*.point.n_val` ·
`student_logits/MANIFEST.json → runs.*.n_val` · `calibration_cache_audit.py:37`
(`RAFDB_N_VAL = 3068  # fold-3 official test split`).

Seçim ile raporlama **aynı `val_loader` nesnesi**: `train_rafdb_kd.py`de loader bir kez kuruluyor
ve epoch-içi `validate`, `best` seçimi, SWA, EMA, `metrics_best`, `metrics_last` — hepsi onu
alıyor; ikinci bir loader hiç kurulmuyor. Öğretmen tarafında da aynı (`main_encoder.py`).

**Sonuç: dört ad tek kümedir ve "RAF-DB's official test set" küme olarak DOĞRUDUR.**
Yanıltıcı olan ad değil, "validation"ın *kullanımı* adlandırıyor olması.

### 1.4 Sizin şüphelendiğiniz çelişki YOK — ama gerçek bir çelişki VAR, başka yerde

**Yok olan:** 04_experiments.tex:14–20 ikisini de aynı nefeste söylüyor ve uzlaştırıyor:

> "The evaluation partition is RAF-DB's *official test set* … no separate held-out set exists in
> our protocol. **We disclose this explicitly:** the same partition serves both for per-epoch
> validation and for reporting, which is common practice in FER but makes accuracy-selected
> checkpoints optimistically biased."

Yani §4:15–16 ile §4:128 çelişmiyor; §4 zaten açıkça beyan ediyor. Kalan sorun **ad çokluğu**, ve
asıl riskli yer §1:148: "best validation accuracy" uzlaştırıcı cümleden uzakta, tek başına duruyor.

**Var olan — ve bu bir protokol cümlesi, terim değil.** `03_methodology.tex:248–249`:

> "$T^{*}$ is fitted on the same evaluation fold on which students are later reported,
> **since neither dataset provides a third partition**"

Bu cümle **FERPlus için yanlış.** FERPlus'ın meta dosyasında **üç** bölüm var
(FER2013Train 25 060 · FER2013Valid 3 199 · FER2013Test 3 153) ve makalenin kendi §4'ü bunu
söylüyor: *"the canonical train and validation partitions, **merged**"*. Yani FERPlus üçüncü bir
bölüm **sağlıyor**; biz onu eğitime kattık. "Sağlamıyor" ile "kullanmadık" aynı şey değil.

| iddia | RAF-DB | FERPlus |
|---|---|---|
| "üçüncü bölüm sağlamıyor" | **DOĞRU** (meta'da 2 bölüm) | **YANLIŞ** (meta'da 3 bölüm) |
| ayrı held-out yok | veri kümesinin sonucu | **yordamın** sonucu |

Aynı aile: `05_results_discussion.tex:877` "a substitute for a third partition". Makale tarafı
sizin; ölçüm bu.

**Bir ad daha var ve iki veri kümesini birden kapsıyor:** "evaluation fold" (`03_methodology.tex:248,
260` · `supplementary.tex:236`) hem n=3068'i hem n=3153'ü adlandırıyor. Tek ada çekerken bunu
hesaba katmak gerekir — dört ad aslında iki veri kümesine yayılıyor.

**Makale ile depo arasındaki sayısal köprü tek sayı değil, en az üç:** 3 068 · 12 271 · ve
sınıf sayımlarından ikisi (`happiness $n{=}1185$`, `fear $n{=}74$`,
`05_results_discussion.tex:723–724`) — üçü de fold-3 satırıyla birebir.

### 1.5 Depo tarafı: eşleme yazıldı, yeniden adlandırma yapılmadı

Adı ben seçmiyorum; **eşlemeyi** yazdım:

* `RESULTS_TABLES.md`e (üreticisinden, `paper_tables.py`) **"One set, several names"** paragrafı
  eklendi: üç adın aynı bölümü gösterdiğini, `@best`in onun üzerinde seçildiğini ve ölçümün
  nerede olduğunu söylüyor.
* `diagnostics/claims.md`e aynı bulgu kaydedildi.
* **`selection_audit/README.md`e DOKUNULMADI** — o dosya bandda `HAND` işaretli ve tazelik
  kapısında `FROZEN`: "donmuş kümenin kendi belgesi, kesme gününe ait". Tarihli kayıt.

Depo bugün RAF-DB için "fold-3 validation split", FERPlus için **"reporting set"** diyor
(`jsd_collapse_audit.py:215`, `r3w1_joint_optimum.md:3`, `jsd_sensitivity.md:5`). Yani depoda da
iki veri kümesi iki ayrı ad taşıyor; tek ada çekmek isterseniz `split_identity` tablosu artık
hangi adın neye karşılık geldiğini ölçülmüş olarak veriyor.

---

## 2 · 0.74 — dört nicelik, ve hipotez ÇÜRÜDÜ

### 2.1 İki 0.74 aynı ızgara noktası değil, aynı nicelik hiç değil

| 0.74 | alan yolu | ızgara | ne ölçüyor |
|---|---|---|---|
| T\*_JSD | `jsd_sensitivity.json → results["(a) all rows"].T_jsd` (ve `ferplus_jsd.json → T_star_jsd.T`) | **196 nokta**, lo 0.1 · hi 4.0 · **adım 0.02** | ÖĞRETMENİN sıcaklığı ↔ insan oy dağılımına JSD'si |
| FERPlus NLL argmin | `robustness_metrics.json → series["FERPlus"].metrics.nll.argmin_T_modal` | **4 nokta**: 0.26 · 0.5063 · 0.74 · 1.0 | ÖĞRENCİ koşularının NLL'i, damıtma sıcaklığına karşı |

Farklı yanıt değişkeni, farklı taraf (öğretmen/öğrenci), farklı çözünürlük.

### 2.2 Çakışma İNŞA EDİLMİŞ — ızgara ölçüt-çivili

Kaba ızgaranın dört noktası rastgele değil; `ferplus_dual_axis.json → arms[*].role` ve
`r3w1_joint_optimum.json → arms[*].role` bunu **açıkça yazıyor**:

| T | ilan edilen rol |
|---|---|
| 0.26 | over-sharpened |
| **0.5063** | **T\*_ECE / T\*_NLL** |
| **0.74** | **T\*_JSD** |
| 1.0 | native |

Yani 0.74 ızgaraya **T\*_JSD olduğu için** kondu. "NLL de 0.74'e düşüyor" cümlesi, dört noktalı bir
ızgarada ve gerçekte **iki aday arasında** (T\*_ECE mi, T\*_JSD mi) verilen bir tercihtir; serbest
bir keşif değil. Komşuluk mesafeleri: 0.74−0.5063 = **0.2337**, 1.0−0.74 = **0.26** — ince
ızgaranın adımının (0.02) on katından fazla.

### 2.3 Yedi metriğin argmin'i — üç seri

| seri | metrik | modal argmin | tohumlar | oybirliği |
|---|---|---|---|---|
| RAF-DB stage1 | NLL · ECE ew-10/25 · ECE em-15 | 1.3406 | hepsi 1.3406 | evet |
| RAF-DB stage1 | Brier · ECE ew-15 · classwise | 1.3406 | biri **1.70** | **hayır** |
| RAF-DB vae9182 | beş ECE | 1.00 | hepsi 1.00 | evet |
| RAF-DB vae9182 | NLL · Brier | 1.00 | biri **0.85** / **1.3406** | **hayır** |
| FERPlus | **NLL** | **0.74** | 0.74 · 0.74 · 0.74 | evet |
| FERPlus | Brier · beş ECE | **0.5063** | hepsi 0.5063 | evet |

### 2.4 Hipotez TUTMUYOR — üç bağımsız gerekçe

**(a) Hipotezin ekseni bu tabloyla sınanamaz.** Hipotez *hedef* tarafına dair: "dağılıma duyarlı
mı, hard etikete mi bakıyor". Oysa tablodaki **yedi metriğin hepsi hard one-hot hedefe karşı**
ölçülüyor — önbellekte etiketler tekil `int64`, Brier'ın hedefi `F.one_hot`, NLL'inki tamsayı
etiket, ECE'ler `preds == labels`. **İnsan oy dağılımını kullanan tek nicelik JSD ve o bu tabloda
yok.** İlk okumamda ekseni sessizce "tahmin vektörünün ne kadarı okunuyor"a çevirmiştim; o başka
bir sorudur. *(Bu düzeltme çürütme turundan geldi ve haklıydı.)*

**(b) O başka soruya göre bile ayrım kurulmuyor.** Brier tam olasılık vektörünü kullanıyor
(`calibration_metrics.py:62-67`, `((probs − onehot)**2).sum(dim=1)`) ve FERPlus'ta **0.5063'e**
düşüyor, üç tohumda oybirliğiyle. Yani "vektörün tamamını okuyan metrikler 0.74'e" de tutmuyor.

**(c) Öğretmen tarafında NLL ile JSD zaten AYRIŞIK — ve bu makalenin ön-beyanı.**
`jsd_sensitivity.json → declared_quantity` = *"separation: T\*_JSD > max(T\*_ECE, T\*_NLL)"*.
Ölçülen: T\*_JSD **0.74** · T\*_NLL **0.50** · T\*_ECE **0.46**;
`ferplus_jsd.json → abs_T_jsd_minus_T_nll` = **0.24**. Sürekli uydurmada
`tstar_sensitivity → results.ferplus.T_star_nll` = **0.50638**. Yani "NLL ve JSD birlikte düşüyor"
demek, S2'nin **ayrışma** bulgusuyla doğrudan çelişir.

### 2.5 Ayrıca: kalan tek gözlem de sanıldığı kadar sağlam değil

FERPlus'ta NLL'in 0.74'ü 0.5063'e tercihi **eşleşmeli** olarak:

| tohum | NLL(0.5063) | NLL(0.74) | fark |
|---|---|---|---|
| 1 | 0.355988 | 0.348234 | +0.007754 |
| 42 | 0.358049 | 0.337891 | +0.020157 |
| 43 | 0.350134 | 0.341870 | +0.008264 |

ortalama **+0.012059**, eşleşmeli farkın sd'si **0.007018** (n=3, df=2) → t = 2.976,
**iki yönlü p = 0.0968 — 0.05'te anlamlı değil.** Bugün ilk yazdığım "2.31 sd" oranı **yanlış
paydalıydı**: payı iki kol arası fark, paydası tek kolun kendi tohum sd'si idi; iki kol arası bir
farkın doğru ölçeği **eşleşmeli farkın** sd'sidir. Düzeltiyorum.

**Post-hoc ölçekleme sıralamayı tersine çeviriyor.** `r3w1_joint_optimum.json → arms[*]`:

| T | `jsd_arm` (ham) | `jsd_ts` (öğrenci TS'li) |
|---|---|---|
| 0.26 | 0.073681 | **0.054045 ← en iyi** |
| 0.5063 | 0.058690 | 0.054274 |
| 0.74 | **0.053598 ← en iyi** | **0.054584 ← en kötü** |
| 1.0 | 0.055107 | 0.054545 |

O dosyanın kendi hükmü zaten: **"ALT YAZI YANLIŞLANDI"**.

**Ve "RAF-DB'de yedi metrik de 1.0'da" ifadesi KIRPILMIŞ ızgaranın ürünü.**
`control_grid_refinement.json` aynı kol için **T=0.95 ve T=1.1** kollarını taşıyor (üçer tohum) ve
`ece` sütunu `robustness_metrics`in `ece_ew_15`i ile **bit düzeyinde aynı** (0.85 → 0.0446753728,
1.0 → 0.0329572362, 1.3406 → 0.0646977626 — üçü de birebir). Ama:

| T | ECE (ew-15) | R3-1 ızgarasında? |
|---|---|---|
| 0.95 | **0.0296114439** | **hayır** |
| 1.0 | 0.0329572362 | evet |
| 1.1 | 0.0349119399 | **hayır** |

Yani ince ızgarada bu metriğin argmin'i **1.0 değil 0.95**. Koşular hayalî değil, diskte var; R3-1
sayımına girmemelerinin sebebi `student_logits/` altında T095/T110 npz'sinin **yayımlanmamış
olması** (43 dosya: 42 npz + MANIFEST). Diğer altı metrik için ince ızgarada ne olduğu
**bilinmiyor** — o önbellekler yayımlanmadan ölçülemez. **Bulunamadı, tahmin edilmedi.**

### 2.6 Sonuç

**Hipotez tutmuyor; makaleye iki cümle girmemeli.** Ayakta kalan tek betimleyici olgu şu ve dar:
*yedi metrikten yalnızca NLL, iki aday arasından T\*_JSD'yi seçiyor* — p = 0.0968, dört noktalı ve
ölçüt-çivili bir ızgarada, ve öğrenci post-hoc ölçeklendiğinde JSD sıralaması tersine dönüyor.
Bunun üzerine mekanizma cümlesi kurulmaz.

Küçük ek gözlem, hüküm değil: RAF-DB stage1 serisinin **seed 42** hücreleri başka adlı koşulardan
geliyor — T=1'de `RAFDB_vichteacher_stage1_9224_betaKD_…` (tohum ekisiz), T=1.3406'da
`RAFDB_stage1_tempscale_T1341_halfA_baseline_…` (`T1341`, `halfA`). Aynı yapılandırmanın üç tohumu
gibi okunuyor ama adlar öyle demiyor. Bunun bir yordam farkı mı yoksa yalnızca adlandırma mı
olduğunu **ölçmedim**.

---

## 3 · Zenodo DOI — bloke edici DEĞİL, kayıt yayımda

Ön kabulünüz tutmuyor ve **dünkü kendi §7 notum da yanlıştı** ("başlanmadı").

DOI: **`10.5281/zenodo.21947604`**. İki değil **üç** yerde basılı: `main_elsarticle.tex:251` ·
`sections/06_conclusion.tex:103` · **`main_print.tex:213`**.

İki bağımsız kayıt sisteminden ölçüm:

| kaynak | ne dedi |
|---|---|
| DataCite API `dois/10.5281/zenodo.21947604` | **state: `findable`** · registered **2026-08-15T11:30:30Z** · version `v1.0.0-submission` |
| Zenodo API `records/21947604` | `conceptdoi` **10.5281/zenodo.21947604** · sürüm DOI'si 10.5281/zenodo.**21947605** · publication_date **2026-08-15** · `isSupplementTo` → `github.com/FatihSenturk/calibration-law-fer/tree/v1.0.0-submission` · dosya `…-v1.0.0-submission.zip`, **8 917 550 bayt** |
| `https://doi.org/10.5281/zenodo.21947604` | 302 → `zenodo.org/doi/…` → **yayımlanmış kayıt** |

Yani makalede basılı olan **kavram DOI'si** (concept DOI) ve bu **doğru tercih**: her zaman en
yeni sürüme çözünür. Kayıt `v1.0.0-submission` etiketini arşivliyor, bizim etiketimiz `5cf2f27`ile
aynı — bugünkü `1af695f` arşivde **yok** ve olmamalı da; arşivlenen şey beyan edilen etiket.

**Yapılacak bir şey kalmadı.** "Adresi çektim, boş döndü" muhtemelen Zenodo'nun tarayıcı tarafı;
kayıt iki registry'de de canlı.

---

## 4 · `dataset_utils/image_dataset copy.py` — ve onu görünmez kılan hata

### 4.1 Dosya

**Kod olarak ölü.** Depo genelinde `import` / `importlib` / `runpy` / `exec` / config atfı
taraması: kopyaya **sıfır** çağrı. `image_dataset.py` ise üç yerden import ediliyor
(`dataset_utils/builder.py:11`, `tools/cache_teacher_outputs.py:40`,
`tools/verify_ferplus_swanlab.py:12`). Adında boşluk olduğu için modül olarak zaten import
edilemez.

Fark: 7 124 vs 8 108 bayt; 172 vs 184 satır (**toplam satır** farkı 12, `diff -u`da değişen satır
26). Kopyada `votes_sum` / `label_em` yok — yani FERPlus'ın 10-oy dağılımı boru hattı ondan
sonra eklenmiş **gibi görünüyor**; ama **bunu ölçmedim ve ölçülemedi**: iki dosya da aynı ilk
commit'te (`51b05bf`) girmiş ve 93 commit boyunca **ikisi de hiç değişmemiş**. Elde olan tek şey
kopyanın özellik alt-kümesi olması; "önce/sonra" sıralaması **bulunamadı**.

Ayrıca: `2026-08-03` raporu bu dosya için "şeffaflık adına README'ye *Files not tied to the paper*
bölümü olarak da yazıldı" diyor — **o bölüm yok.** poster-var'da `README.md` diye bir dosya yok,
public README'de de ne böyle bir bölüm ne kopyaya atıf var. Yani dosya public'e **beyansız**
gidiyor.

**Ölçüm silmeyi destekliyor; silmedim** — kararı ölçümden sonra vereceğiz demiştiniz, ve public
depodan silme onayınıza tabi. İki depoda da izleniyor; komut hazır.

### 4.2 `git ls-files` bölme hatası — depo kodunda VARDI, üç yerde

Dünkü hatam tesadüf değilmiş; aynı hata **üç üretici betikte** duruyordu:

| dosya | kod |
|---|---|
| `diagnostics/public_repo_staleness.py:117` | `["git","ls-files"] … .stdout.split()` |
| `diagnostics/public_repo_sync.py:375` | aynı |
| `diagnostics/public_scope_scan.py:99` | aynı |

Argümansız `.split()` boşluklu yolu ikiye bölüyor. **Zarar hayalî değil; kapıların kendi
raporlarında basılıydı:**

| artefakt | ne yazıyordu | doğrusu |
|---|---|---|
| `public_repo_staleness.md:167` | gerçek dosya "Yalnız poster-var'da" | public'te **izleniyor** |
| `public_repo_staleness.md:216-217` | `dataset_utils/image_dataset` + `copy.py` "Yalnız public'te" | **ikisi de yok** |
| `public_repo_sync_dryrun.md:39-40` | aynı iki hayalet "kaynakta yok, public'e özel — 6" | gerçek **4** |
| `public_repo_sync_dryrun.md:136` | gerçek dosya "aday, karar Fatih'in" | **zaten izleniyor** |
| `public_scope_scan.json` | `n_tracked` 574 / `n_commit_set` 575 | **573 / 573** |

Sonuncusu 18 Ağustos'ta **somut bir yanlış eyleme** yol açtı: `--add-approved`, zaten public'te
duran dosyayı "aday" sanıp yeniden yazdı — dün o dosyayı yanlışlıkla silmemin kökeni de bu.

Düzeltme: üçünde de `git ls-files -z` + NUL ile bölme (`-z` tırnaklamayı da kapatır, ASCII-dışı
adlar da doğru okunur). Düzeltme sonrası ölçülen: "yalnız public'te" **7 → 4** (LICENSE ·
PROVENANCE.md · README.md · THIRD_PARTY_NOTICES.md — dördü de gerçekten public'e özel),
"kaynakta yok" **6 → 4**, `dataset_utils` adayı **2 → 1**.

`export_to_drive.py` ve yeni tazelik kapısı bu hataya sahip değil (`splitlines()` kullanıyorlar).

### 4.3 Yan bulgu: tazelik kapısının "yan çıktı 0"ı belirsizdi

Dünkü **beyansız yan çıktı** sınıfı bugün bir koşuda **0** bildirdi, ama koşudan sonra
`paper/figures/graphical_abstract.pdf` yine kirliydi. Sebep tasarımın kendisinde: Katman A yalnız
**kendi koşusundan önce temiz olan** dosyaları yan çıktı sayar (kapı kullanıcının halihazırdaki
değişikliğini geri almaz), dolayısıyla dosya kapı başlamadan önce zaten kirliyse hiçbir üreticiye
atfedilemez ve sayı 0 görünür. Temiz ağaçta koşulduğunda kapı doğru davranıyor: `1` bildiriyor,
`graphical_abstract.py`ye atfediyor ve geri alıyor.

Kapı artık **koşu başındaki değişmiş dosya sayısını** da basıyor, ve yan çıktı 0 iken bu sayı
0 değilse rapora bir uyarı düşüyor: *"bu 0, 'hiç yan çıktı yok' değil, 'atfedilebilir yan çıktı
yok' demektir."* Bir kapının sessizliği okunabilir olmalı.

---

## 5 · Kayda: düzyazı hâlâ denetim dışı

Yazılı bırakıldı — `diagnostics/claims.md` (Open claims) ve bu rapor:

> `sections/*.tex` **821** sayı jetonu taşıyor ve defter bunları **taramıyor**. Bu bilinçli bir
> erteleme (okuma sürüyor; hareket eden hedefi bağlamak çürük bağ üretir), ama sonucu açıkça
> durmalı: **makalenin en çok değişen kısmı, denetimin görmediği kısımdır.** Tablolar, ek (S1–S3)
> ve öz kapsam içinde; gövde düzyazısı değil. Okuma bitince ilk iş o kapsam kararı.

---

## 6 · Kapılar

| kapı | sonuç |
|---|---|
| `check_numbers` | **GEÇTİ · çıkış 0** — kayıtsız **0**, uyuşmazlık 0 |
| `check_numbers_selftest` | **17/17** (düşmedi) |
| üretici tazeliği | **GEÇTİ** — Katman A 53 · Katman B 8 · BAYAT 0 · kaynak ayrışması 0 · ölçülemez 0 · başka hata 0 · beyansız yan çıktı 1 (§4.3) |
| tazelik öz sınaması | **2/2** |
| tablo diff | **1511/1511** — 15 sapma kabul edildi, hepsi APPEARED (`split_identity`); CHANGED/VANISHED/MOVED **yok** |
| Level-1 | **GEÇTİ** — geçti **59** (yeni üretici dahil) · İHLAL 0 · muaf 10 · başka hata 0 |
| figür | **10/10** |
| mutlak yol | **GEÇTİ** — beyansız 0 |
| public kapsam taraması | **İHLAL 0** |

Defter değişmedi: `jeton 862 · bagli 695 · turetilmis 21 · muaf 150 · KAYITSIZ 0` —
695 + 17 + 150 + 0 = 862.

---

## 7 · Sizin kararınızı bekleyen

1. **Tek ad** — ölçüm "official test set"i destekliyor; "evaluation fold" iki veri kümesini birden
   kapsadığı için tek ada çekerken kapsamı da seçmek gerekiyor (§1.4).
2. **`03_methodology.tex:248–249`** — "neither dataset provides a third partition" FERPlus için
   yanlış; iki satır düzeltme.
3. **`dataset_utils/image_dataset copy.py`** — ölü, iki depoda izleniyor, silme onayınıza tabi.
4. **T095/T110 logit önbelleklerinin yayımı** — yayımlanırsa R3-1 ince ızgarada da ölçülebilir
   (§2.5); yayımlanmazsa "yedi metrik 1.0'da" cümlesi kırpılmış ızgaraya bağlı kalır.
