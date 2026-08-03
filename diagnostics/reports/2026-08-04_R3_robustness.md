# R3 — dış inceleme robustluk turu (4 Ağu 2026)

**Ön-kayıt:** `PREREGISTRATIONS.md` A10 · commit `0b8ef2f` · tag `r3-predeclared` ·
2026-08-04 00:59:56. **Hiçbir metrik bu commit'ten önce hesaplanmadı**; üç üretici de
beyandan sonra yazıldı. Başarı ölçütü yoktur — bu bir envanterdir, hipotez testi değil.

**Eğitim yok, P6 etkilenmedi.** Tümü kayıtlı logitlerden. GPU'ya dokunan tek iş 15 koşuluk
çıkarımdı (koşu başına 2.6 sn); P6 kuyruğu bu sırada 25→26'ya ilerledi, ETA 5 Ağu 19:42.

---

## Kapsam düzeltmesi — hesaptan önce

Görev metnindeki kapsam satırı (*primary 5 kol · stage1 3 kol · VAE9182 5 kol · FERPlus 3
kol*) depodaki hiçbir yapıyla eşleşmiyordu. Diskte ölçülen:

| iddia | gerçek |
|---|---|
| primary doz-cevap serisi, 5 kol | **yok** — tüm `tempscale_T*` koşuları stage1 ve vae9182'ye ait; primary'de yalnız mekanizma kolları var |
| stage1 3 kol | **5 T noktası** (0.85 · 1.00 · 1.3406 · 1.70 · 2.20) |
| VAE9182 5 kol | ✅ 5 T noktası |
| FERPlus 3 kol | **4 T noktası** (0.26 · 0.5063 · 0.74 · 1.00) |

Mekanizma-kolu okuması da tutmuyordu (n=3 olan kol sayısı her üç öğretmende de 4). Kapsam
**42 koşu** olarak sabitlendi ve düzeltme tek bir metrik hesaplanmadan önce beyana yazıldı.

---

## R3-1 — çok-metrik doz-cevap · `paper_tables/robustness_metrics.md` · T13

42 koşu × 7 metrik. **Turun cevabı tek satırda: 21 (seri × metrik) hücresinin 20'si
minimumu aynı yere koyuyor.**

| seri | uzlaşılan argmin T | uyuşan metrik |
|---|---|---|
| RAF-DB stage1 | **1.3406** (= Stage1'in kendi T\*'ı) | 7/7 |
| RAF-DB vae9182 | **1.00** (iyi kalibre öğretmen — manevra alanı yok) | 7/7 |
| FERPlus | **0.5063** (= FERPlus'ın T\*'ı) | 6/7 |

Kutu sayısı (10/15/25), kutulama şeması (eşit-genişlik vs eşit-kütle), sınıf ağırlıklandırma
(classwise) ve **hiç kutulama yapmayan iki metrik** (NLL, Brier) aynı yeri gösteriyor. Yani
optimumun yeri kolun özelliği, kutulama kuralının değil. Dış incelemenin 1. hesaplanabilir
eksiği bu tabloyla kapanıyor.

**Tek istisna, gizlenmiyor:** FERPlus'ta **NLL** minimumu 0.5063 yerine **0.74**'e koyuyor —
ve bunu **üç tohumda birden** yapıyor, yani tohum gürültüsü değil sistematik bir ayrışma.
Tabloda "unanimous: yes" diye işaretli.

> **Bir gözlem, bulgu değil:** 0.74, R3-3'te FERPlus öğretmeninin T\*_JSD'siyle aynı sayı.
> Aralarında gösterilmiş bir bağ yok; not ediyorum ki gözden kaçmasın.

**Monotonluk 0/3 çıktı ve bu beklenen biçimdir** — seri iç optimumlu bir doz-cevap, hiçbir
tohum uçtan uca tek yönlü olamaz. Bilgi taşıyan sayım adım tutarlılığı: **231 adımın
224'ü** (%97.0) aynı çiftteki öteki tohumlarla uyuşuyor. Uyuşmayan 7 adımın hepsi — hangi
çift, hangi tohum, hangi metrik, iki değeriyle — tabloda tek tek listeli. FERPlus'ta
**9/9, yedi metrikte de**.

---

## R3-2 — T\* fit kriteri duyarlılığı · `paper_tables/tstar_sensitivity.md` · T14

| öğretmen | T\*_NLL | T\*_ECE | \|ΔT\*\| | ΔECE (kriter maliyeti) | TS'in kaldırdığı ECE |
|---|---|---|---|---|---|
| stage1 | 1.3494 | 1.3198 | 0.0296 | +0.00154 | +0.02198 |
| primary | 1.2613 | 1.2441 | 0.0172 | +0.00146 | +0.01985 |
| vae9182 | 0.9831 | 1.0572 | 0.0741 | +0.00432 | **−0.00102** |
| ferplus | 0.5064 | 0.4530 | 0.0533 | +0.00846 | +0.11259 |

Üç öğretmende kriter seçiminin maliyeti, TS'in kaldırdığı ECE'nin **13–14'te biri** —
yani rapor edilen kalibrasyon kazançları hangi kriterle T\* bulunduğuna bağlı değil.

**Ama vae9182'de değil, ve bu makaleye girmeli.** Orada NLL optimumundaki TS, ECE'yi
**artırıyor** (0.01355 → 0.01457). İki kriter yalnız büyüklükte değil, düzeltmenin
**yönünde** ayrışıyor: ECE kriteri T=1'in *öte* yanında (1.0572) gerçek bir iyileşme
buluyor (0.01025). *"Fit kriteri önemsizdir"* cümlesi bu öğretmen için yazılamaz.

İlk ürettiğim özet cümlesi "her öğretmende bir-iki mertebe küçük" diyordu; vae9182'de
yanlıştı. Üretici artık cümleyi iddia etmiyor, **hesaplıyor** — oranı çıkaramadığı satırda
"n/a — TS adds ECE" basıyor.

**stage1 LOCAL-MIN işaretli:** ECE(T) kutulu bir istatistik olduğu için parça-parça sabit;
sürekli Brent oradaki küresel minimumu ıskalıyor. Her satır 0.005 adımlı yoğun grid'e karşı
denetleniyor ve ıskalayan satır tabloda işaretli, grid değeri yanında.

---

## R3-3 — FERPlus JSD katman duyarlılığı · `paper_tables/jsd_sensitivity.md` · T15

Oy toplamı dağılımı: 6→6 satır · 7→22 · 8→182 · 9→966 · **10→1977** (toplam 3153).

| kesit | n | T\*_ECE | T\*_NLL | T\*_JSD | ayrışma korundu |
|---|---|---|---|---|---|
| (a) tüm satırlar | 3153 | 0.46 | 0.50 | 0.74 | evet |
| (b) oy = 10 | 1977 | 0.42 | 0.46 | 0.74 | evet |
| (c) katman 6–7 | 28 | 0.74 | 0.70 | 0.88 | evet |
| (c) katman 8–9 | 1148 | 0.46 | 0.54 | 0.74 | evet |
| (c) katman 10 | 1977 | 0.42 | 0.46 | 0.74 | evet |

**Beyan edilen büyüklük ayrışmadır** (T\*_JSD > her iki sert-etiket optimumu) ve **beş
kesitte de korunuyor**. Dahası T\*_JSD, n ≥ 1000 olan her kesitte **birebir 0.74** — foldun
%99.1'ini taşıyan katmanlar. İnsan hizalanması optimumu oy çözünürlüğüyle hiç kıpırdamıyor.

**Ayrı raporlanan bir kırık var:** ECE<NLL alt-sırası n=28'lik 6–7 katmanında ters dönüyor.
Bu beyandaki iddia **değil**, yayımlanmış tablonun tesadüfi bir alt-sırası. İkisini tek
bayrakta toplasaydım, %0.9'luk bir katmandaki bir ayrıntı, ana bulgu kırılmış gibi
okunurdu; bu yüzden tabloda iki ayrı sütun.

---

## Yolda yakalanan iki gerçek hata

**1. Bant yeni tabloları sessizce düşürüyordu.** `export_to_drive.py` dosyaları tek tek
sayıyor. `tstar_sensitivity.md` üretildi, betik "başarıyla ihraç edildi" dedi, dosya
Drive'a **hiç gitmedi** — ve eksik olan şey görünmediği için makale tarafı bunu bilemezdi.
Altı R3 çıktısı kaydedildi; üstüne `paper_tables/` içinde olup listede olmayan her dosyayı
bağıran bir kapı eklendi. Bant şimdi **76 dosya**, eksik yok.

**2. FERPlus önbelleği CUDA'da üretilemezdi — kapı yakaladı.** İlk deneme durdu: doğruluk
88.9629 vs denetimin 88.9312'si, fark **tam 1/3153**, yani tek bir örnek tahmin
değiştirmiş. Sebep: `ferplus_selection_audit.py` varsayılan CPU'da koşuyor, dolayısıyla
yayımlanmış FERPlus sayıları CPU sayıları. CUDA önbelleği makaledeki FERPlus tablosuyla
dördüncü hanede çelişirdi. Kural düzeltildi ve A10'a not düşüldü: **her seri kendi
yayımlanmış denetiminin cihazında ve batch'inde** önbelleğe alınır (RAF-DB CUDA/256,
FERPlus CPU/64). 27 önbelleğin hepsi kapıdan geçti.

---

## Doğrulama

- **15-kutu sütunu kapısı.** R3-1'in `ECE ew-15` sütunu, her koşuda o koşunun kendi
  önbelleğindeki `ece_recomputed` ile **1e-9** toleransında karşılaştırılıyor; sapma tabloyu
  durduruyor. Yani altı yeni sütun, eskisini yeniden üretemeyen bir boru hattından gelemez.
- **Önbellek kapısı.** 27 önbelleğin her biri, bağımsız üretilmiş `selection_audit`
  değerlerine karşı doğrulandı (acc 1e-3 pp, ECE 1e-4).
- **`table_diff_gate`:** 278 → **432 hücre**. 56 yeni hücre APPEARED, **0 MOVED, 0
  VANISHED** — mevcut hiçbir sayı kıpırdamadı. Taban çizgisi bu gerekçe içine yazılarak
  kabul edildi; R3 sayıları artık kapının içinde, bir daha sessizce kayamazlar.

## Makaleye ne giriyor

T13/T14/T15 olarak `RESULTS_TABLES.md`'ye işlendi (tek kaynak kuralı). Üç eksiğin üçü de
hesaplandı; **ikisi lehte kapandı** (metrik seçimi optimumun yerini değiştirmiyor; JSD
ayrışması oy çözünürlüğüne koşullu değil), **biri koşullu** (fit kriteri iyi kalibre
öğretmende yön değiştiriyor — bu artık makalede açıkça yazılacak bir sınır).

## Bekleyen

**R3-4**, P6 kuyruğu 42/42 olunca (ETA **5 Ağu 19:42**): T11/T12, A9'un resmî hükmü,
`p6_collapse_test.md`. A9'un kapsam değişikliği — makaleye alınması — kuyruk 26/42'deyken ve
hiçbir hüküm okunmadan PREREGISTRATIONS'a işlendi.
