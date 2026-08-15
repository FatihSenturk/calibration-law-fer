# N5 — öğretmen-seçim maliyeti üç checkpoint'te

> Tek soru, tek tablo. Dış denetimin iddiası ile T6'nın notu aynı anda doğru olamazdı; ölçüldü,
> **ikisi de tam olarak doğru değilmiş**. Sayılar kanonik defterden; hiçbiri elle yazılmadı.

---

## 1 · Cevap

| | iddia | ölçüm |
|---|---|---|
| "maliyet @best 0.53, @swa 0.35" | ✅ **büyük ölçüde doğru** | @swa **0.3477** · @best **0.5215** · @last **0.8257** — tek fark, yayımlı 0.53'ün doğrusu **0.52** (kaynağı §3) |
| "bir ikili karşılaştırma checkpoint'ler arasında tersine dönüyor" | ❌ **TUTMADI** | mekanik tarandı: **0 tersine dönme** |
| T6: "the ranking is identical at all three checkpoints" | ⚠️ **yarı doğru** | en iyi öğretmen üçünde de aynı (`vae9182`) ✅, ama @swa'da 2./3. sıra **TAM EŞİT** — orada sıralama bir tam sıra değil |

---

## 2 · İstenen tablo

Öğrenci = her öğretmenin T=1 (ölçeklenmemiş) temel kolu, 3 tohum. Kol tanımı
`paper_tables.is_ablation_control` + `cw=effective_number` ile **ithal** edildi, yeniden yazılmadı.

| teacher | student acc @swa | @best | @last |
|---|---|---|---|
| **vae9182** | **89.95 ± 0.37** (n=3) | **90.28 ± 0.19** | **89.82 ± 0.17** |
| stage1 | 89.60 ± 0.34 | 89.75 ± 0.08 | 88.99 ± 0.10 |
| primary | 89.60 ± 0.13 | 89.57 ± 0.09 | 88.49 ± 0.26 |

| checkpoint | sıralama | ρ(öğretmen acc, öğrenci acc) | ρ(−öğretmen ECE, öğrenci acc) | yanlış-seçim maliyeti |
|---|---|---|---|---|
| **@swa** (birincil) | vae9182 > **{stage1 = primary}** | **−0.866** | **+0.866** | **0.3477 pp** |
| @best | vae9182 > stage1 > primary | −0.500 | +1.000 | 0.5215 pp |
| @last | vae9182 > stage1 > primary | −0.500 | +1.000 | 0.8257 pp |

Öğretmen tarafı (değişmedi): stage1 acc 92.2425 / ECE 0.0378 · primary 92.0143 / 0.0396 ·
vae9182 91.8188 / **0.0136**. Doğrulukla seçim → `stage1`; ECE ile seçim → `vae9182`; gerçekte
en iyi → **`vae9182`**, üç checkpoint'te de.

**Kuralın doğrulaması (uydurulmadığının kanıtı):** bu seçim kuralı stage1 ve vae9182 için
`p1_two_teacher_overlay`in T=1.00 satırlarıyla **birebir aynı koşu kümesini** veriyor ve T1/T2'nin
yayımlı @swa değerlerini (**89.60 ± 0.34** / **89.95 ± 0.37**) **tam olarak** yeniden üretiyor.
Eksik olan primary'nin aynı biçimli üç-tohumlu kolu, o da defterde mevcut.

---

## 3 · Yayımlı 0.53 nereden geldi — bayat yan tablo

`p4_teacher_selection_recipe.py` öğrenci sayılarını `seed_variance/seed_variance_table.json`'dan
okuyordu. O dosyanın üç kusuru vardı ve üçü birlikte N5'in sorduğu çelişkiyi üretti:

| # | kusur | ölçüm |
|---|---|---|
| 1 | **tek checkpoint** | içindeki sayılar `best_checkpoint.pth`ten, yani @best; makale birincil olarak @swa kullanıyor |
| 2 | **bayat** | mtime **2026-07-28** (P1/P2/P3/P4'ten önce); `T-A baseline` = **89.7436**, defterin aynı kolu @best'te **89.7545** → **0.011 pp** sapma |
| 3 | **anonim etiket** | `T-A/T-B/T-C` hangi öğretmen olduğu dosyadan geri kurtarılamıyordu |

Bayat değerle maliyet 90.2760 − 89.7436 = **0.5324 → "0.53"**; defterle 90.2760 − 89.7545 =
**0.5215 → 0.52**. Yani 0.53 hem yanlış checkpoint'in hem 0.011 pp'lik bir bayatlığın bileşimi.

`paper_tables.py` 2026-07-31'de T5a'nın paydasını **tam bu dosyadan** koparmıştı ("üç kampanya
evresi bayat, T-A/T-B/T-C ile hangi hücrenin hangisi olduğu kurtarılamıyor"); P4 o temizlikte
atlanmış. Artık P4 de defterden okuyor.

---

## 4 · @swa'daki beraberlik — gerçek, ve tesadüfi

`stage1` ve `primary` @swa'da **tam olarak eşit**: her ikisi de **89.602348 pp**. Kopyalanmış
koşu değil; tohum tohum farklılar, toplamları eşit:

| teacher | seed 1 | seed 42 | seed 43 | toplam doğru |
|---|---|---|---|---|
| stage1 | 2761 | 2742 | 2744 | **8247** / 9204 |
| primary | 2749 | 2753 | 2745 | **8247** / 9204 |

(3068 görüntülük fold-3 val × 3 tohum.) Sonuç: @swa'da sıralama **tam sıra değil**, dolayısıyla
"identical ranking at all three checkpoints" cümlesi **kazanan** için doğru, **tam sıra** için
değil. Bu yüzden `ranking_identical_across_ckpts` artefaktta artık **`false`** ve nedeni
(`ckpts_with_ties: ["swa"]`) yanında duruyor.

**İkili tersine dönme taraması** (elle göz kararı değil, mekanik): üç çiftin üçü de her
checkpoint'te aynı yönde → **`pairwise_reversals: []`**.

---

## 5 · Kalıcı hâle getirilenler

1. **P4 artık defterden okuyor.** `student_by_ckpt()` → `runs.csv` + seçim denetimi, üç
   checkpoint. Kol boş dönerse `RuntimeError` ile durur — ikinci bir kaynağa **sessizce
   düşmez** (bu turun tam olarak cezalandırdığı davranış).
2. **T6'nın notu artık hesaplanıyor.** Eskiden "the ranking is identical at all three
   checkpoints" düz bir iddiaydı, hiçbir şey üretmiyordu. Şimdi `per_checkpoint_verdict()`
   üretiyor: sıralama, beraberlikler, iki Spearman, checkpoint başına maliyet, tersine dönme
   taraması. Yeni **T6a** bloğu `RESULTS_TABLES`e girdi.
3. **T6/T6a kapıya kaydedildi.** `p4_teacher_selection.json` SOURCES'a girdi (**51 yeni hücre**,
   hepsi APPEARED, MOVED yok). Kayıtlı olsaydı bayat 0.53 haftalarca yaşamazdı — aynı ders
   üçüncü kez: kayıtsız tablo korumasız tablodur. Maliyet **checkpoint başına ayrı hücre**;
   tek hücreye sıkıştırmak N5'in açmak zorunda kaldığı karışıklığın ta kendisi olurdu.

---

## 6 · Makale tarafına düşen (promptun karar kuralına göre)

- **Maliyet:** birincil **0.35 pp @swa**; @best değeri **0.52** (0.53 değil) ve "artefakt/
  checkpoint'e bağlı" diye anılmalı; @last 0.83.
- **"Identical ranking" cümlesi:** kazanan için ayakta — *"the best teacher is the same at all
  three checkpoints"*. Tam sıra iddiası düşmeli; @swa'da 2./3. sıra eşit.
- **ρ değerleri checkpoint etiketiyle:** ρ(−öğretmen ECE, öğrenci acc) = **+1.000 @best/@last**,
  **+0.866 @swa** (beraberlik bağlı sıra ürettiği için). ρ(öğretmen acc, öğrenci acc) her
  checkpoint'te **negatif** — tarifenin ana iddiası üç checkpoint'te de ayakta.
- **Tersine dönme iddiası geri çekilebilir:** ölçülen 0.

---

## 7 · Kapılar

| kapı | sonuç |
|---|---|
| tablo | **1050/1050**, sapma yok (983 → 999 → **1050**; 51 yeni hücre kabul edildi) |
| Level-1 | geçti **42** · İHLAL **0** · muaf 9 · başka hata **0** |
| mutlak yol | 20 / 68 · beyansız **0** · okunamayan **0** — GEÇTİ |
| figür | 10/10, 0 failing (bu tur figüre dokunmadı) |

---

## 8 · Yan kayıt: başka bir eğitimle eşzamanlılık

Bu tur, **başka bir depoda süren bir eğitimle aynı anda** koştu
(`D:\affectnetplus-softfer`, `src.train --config configs/softfer_convnext_lr1.yaml`, 14 Ağu
22:12'den beri). Çakışma ölçüldü, varsayılmadı:

- N5 üreticisi `torch` bile **ithal etmiyor** (json/statistics/pathlib + defter okuma).
- Level-1 kapısının koşturduğu 42 üreticiden CUDA varsayılanı olan ikisi
  (`selection_audit_table`, `ferplus_selection_audit`) **muaf listesinde, hiç koşulmuyor**;
  koşan 5 torch betiği `map_location="cpu"` ile sabitli.
- Ölçüm: bir torch üreticisi koşarken VRAM **8428 → 8427 MiB** (dalgalanma diğer eğitimin).
  Benden **0 MiB**. Tur boyunca GPU 75-95% kullanımda kaldı ve eğitim etkilenmedi.
- Kapı üreticileri **sırayla** koşuyor (`for rel: subprocess.run`), aynı anda tek ekstra süreç;
  makinede 32 mantıksal CPU ve 31,7 GB boş RAM var.

---

Üretici: elle yazıldı · ölçümler `p4_teacher_selection_recipe.py`, `paper_tables.py`,
`table_diff_gate.py` çıktıları, `runs.csv`, seçim denetimi CSV'si ve
`seed_variance/seed_variance_table.json` (bayatlığın kanıtı olarak) üzerinden
