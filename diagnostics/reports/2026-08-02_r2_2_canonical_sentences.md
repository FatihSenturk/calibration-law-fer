# R2-2 — İki açık sonucun kanonik cümleleri + §4 ilan envanteri (2 Ağu 2026)

Üretici: elle yazıldı, her sayı kaynak artefaktından doğrulandı (yollar her blokta).

## 1. Kill-switch pilotu (A2 · B-010) — makale cümleleri

Bağlam (doğrulanmış): iyi kalibre VAE9182'nin logitleri sabit T0=0.7311 ile keskinleştirilerek
Stage1'in doğal ECE'si (0.0378) yapay olarak enjekte edildi; `--adaptive-t-enable` AÇ/KAPA × 2
tohum. Kill-switch beyanı koşulardan **8 sa 43 dk önce** donduruldu (25 Tem 14:35:43, launcher
satır 42–49). Ölçülen: tohum-içi dECE **+0.0011 (seed 42)** ve **−0.0053 (seed 1)** →
ort **−0.0021 ± 0.0045** (n=2, örneklem sd; BULGULAR'daki ±0.0032 popülasyon-sd'dir,
kampanya konvansiyonu örneklem-sd), işaretler `+ −` tutarsız. Doğal bar: −0.0034 (B-004'ün
3/3 tutarlı adaptive_t etkisi). İnce nokta: switch kodunun ilk sürümü ortalamayı test edip
"3. tohumu harca" dedi; ön-kayıt metni "her iki tohumda da" dediği için kural per-seed'e
**sıkılaştırıldı** ve sonuç NULL'a döndü — sonuç görüldükten sonra gevşetme değil, tersi.

Önerilen İngilizce (1–2 cümle, §5'e):

> The deliberate-miscalibration pilot (a well-calibrated teacher artificially sharpened to the
> over-confident teacher's ECE, with adaptive-T toggled) was governed by a kill-switch frozen
> eight hours before launch: run two seeds first, and stop unless the ECE benefit clears the
> native $-0.0034$ in both. It fired --- the two seeds disagreed in sign ($+0.0011$ / $-0.0053$;
> mean $-0.0021 \pm 0.0045$) --- so the third seed was not spent and the pilot is recorded as
> null: injected miscalibration did not re-awaken the mechanism.

İsteğe bağlı ek cümle (dürüstlük hikâyesi, §4 m7'nin ruhuna uygun):

> (The first implementation of the switch tested the seed mean and would have passed; correcting
> it to the pre-declared per-seed form is a tightening, not a loosening, of the rule after
> seeing data.)

Kaynak artefaktlar: `rafdb_p3_then_miscal_chain.ps1` satır 42–49 ·
`diagnostics/PREREGISTRATIONS.md` A2 · `BULGULAR.md` B-010 FINAL (26 Tem 11:47).

## 2. Öğrenci-baş izolasyonu (B1) — makale cümleleri

Bağlam (doğrulanmış, `diagnostics/vich_isolation/vich_isolation_verdict.json`): aynı VAE9182
öğretmeni, aynı tarif; öğrencinin varyasyonel başı (VICH) düz lineer başla değiştirildi,
3 eşleştirilmiş tohum. d = linear − vich: **dECE +0.0062 ± 0.0015, 3/3 aynı işaret**
(+0.0059 / +0.0079 / +0.0049); **doğruluk değişmedi** (−0.02 ± 0.11 pp). Göreli:
lineer başın ECE'sinin (0.0335) **%18.6'sı** varyasyonel başla kalkıyor. PREREGISTRATIONS B1
hükmü: launcher'da tek tahmin cümlesi yok → **keşifsel etiketi ZORUNLU** ("önceden söylemiştik"
denemez).

Önerilen İngilizce (1–2 cümle, keşifsel etiketiyle):

> In an exploratory head-isolation comparison (not pre-declared), replacing the student's
> variational classification head with a plain linear head under the same well-calibrated
> teacher left accuracy unchanged ($-0.02 \pm 0.11$ pp) but raised student ECE by
> $+0.0062 \pm 0.0015$, the same sign in all three seeds: the variational head accounts for
> roughly $19\%$ of the linear student's calibration error, independently of the teacher-side
> effects that are this paper's subject.

Kaynak artefaktlar: `diagnostics/vich_isolation/vich_isolation_verdict.json` ·
`rafdb_vich_isolation_queue.ps1` · `diagnostics/PREREGISTRATIONS.md` B1.

## 3. §4 ilan envanteri — "N ilan / N rapor" cümlesi için

§4'ün (04_experiments.tex) ilan ettiği her analiz kalemi ve §5'teki karşılığı:

| # | §4'te ilan | §5 karşılığı | kaynak artefakt | durum |
|---|---|---|---|---|
| 1 | Seçim denetimi, 3 checkpoint, donmuş N=131 (m6) | §5 res_selection_audit + T8 + fig | `selection_audit.csv` | ✓ |
| 2 | Sıra-istatistiği K=50/100 (m6) | §5:402–409 | `selection_gain.json` (+ yeni `order_stat_trend.json`) | ✓ |
| 3 | Best–last / best–SWA (m6) | §5:400–401 | `selection_audit.csv` | ✓ |
| 4 | FERPlus best–last replikasyonu (m6) | §5:402 (+0.50±0.21) | `ferplus_selection_audit` | ✓ |
| 5 | Eşleştirilmiş t + d_z + Holm, 6 kontrast (m7) | §5.1 vd. (R0-2 işlendi) | `paper_tables/inferential_tests.*` | ✓ |
| 6 | Birincil grup-ayrışması testi (m7) | §5.1 | aynı | ✓ |
| 7 | Ön-beyan: düz-kontrol (A1) | §5:48–55 | `PREREGISTRATIONS.md` A1 | ✓ |
| 8 | **Ön-beyan: kill-switch pilotu (A2)** | **YOKTU** | bkz. §1 üstte | **cümle hazır** |
| 9 | Ön-beyan: FERPlus 3 tahmin (A3) | §5:75 | A3 | ✓ |
| 10 | Ön-beyan: insan-hizalama 2 tahmin (A4) | §5:240 | A4 | ✓ |
| 11 | **Keşifsel: öğrenci-baş izolasyonu (B1)** | yalnız etikette (§5:469), **sonuç yoktu** | bkz. §2 üstte | **cümle hazır** |
| 12 | Keşifsel: oracle-gate tanısı (B2) | §5:166–186 | `p2_verdict.json` | ✓ |
| 13 | Keşifsel: kapasite süpürmesi (B3) | §5:130–150 + T10 | `RESULTS_TABLES.json` | ✓ |
| 14 | Kısmen ön-beyanlı doz-yanıt (Stage1) | §5 doz-yanıt bölümü | A5/A6 | ✓ |
| 15 | Ön-beyanlı kontrol tamamlama ×2 (cw-eşli; oracle 3 öğretmen) | §5:169, §5:201 | A7/A8 | ✓ |
| 16 | Gecikme protokolü + oranlar (m9) | §5:449 vd. | `p5_efficiency/latency_benchmark.json` | ✓ |

**Sayım:** §4'te 16 kalem ilan; §5'te 14 raporlu; eksik 2'nin (A2, B1) kanonik cümleleri bu
raporda — eklenince **16/16**. Fatih'in "N ilan / N rapor" cümlesi için: *"Section 4 declares
sixteen analysis items; Section 5 reports all sixteen."* (İkisi eklendikten sonra doğru olur.)

Tarama yöntemi: 04/05_experiments tex dosyaları satır satır; §5 karşılıkları grep +
satır-numarası ile doğrulandı (derlenmiş PDF değil, kaynak tex).
