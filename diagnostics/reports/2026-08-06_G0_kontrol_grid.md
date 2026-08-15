# G0 — kontrol öğretmeni grid inceltmesi (6 Ağu 2026)

**Ön-kayıt durumu: YOK.** Bu koşular Round-2 hakem raporu (5 Ağu) görülmüşken planlandı.
`PREREGISTRATIONS.md` bölüm **B8**'e kaydedildi ve **makalede "pre-registered" DENMEYECEK**.
§4.5'in ön-beyan envanterine girmez.

Üretici: `diagnostics/control_grid_refinement.py` (commit `131ea73`, **sonuçlardan önce**) ·
tablo: `paper_tables/control_grid_refinement.md` · veri: `selection_audit_unfrozen.csv` @swa

---

## Sorulan soru

Panel R1-W11: kontrol öğretmeninin (VAE9182) kendi optimumu **T\*_NLL = 0.983** /
**T\*_ECE = 1.057** aralığında, ama ön-beyanlı falsifikasyon testinin grid'i
{0.85, 1.00, 1.34, 1.70, 2.20} — native'e **en yakın komşu 0.15 uzakta**. Yani *"iyi kalibre
öğretmen iç optimum göstermez"* tahmini, **başarısız olabileceği ölçekte sınanmamıştı**.
Hakem haklıydı: o çözünürlükte, gözlenen genişlikte bir sığ optimum **tanım gereği görünmezdi**.

G0 iki nokta ekledi: **0.95** ve **1.10** — native'e 0.05 ve 0.10 uzakta, ve öğretmenin kendi
iki optimumunu (0.983 / 1.057) arasına alacak şekilde.

## Beş noktalı seri (@swa, n=3)

| T | rol | öğrenci ECE | öğrenci doğruluk (pp) |
|---|---|---|---|
| 0.85 | ön-beyanlı grid | 0.0447 ± 0.0013 | 89.93 ± 0.06 |
| **0.95** | **eklendi (G0)** | **0.0296 ± 0.0027** | 90.07 ± 0.15 |
| 1.00 | native | 0.0330 ± 0.0020 | 89.95 ± 0.37 |
| **1.10** | **eklendi (G0)** | 0.0349 ± 0.0032 | 89.98 ± 0.22 |
| 1.3406 | ön-beyanlı grid | 0.0647 ± 0.0030 | 90.09 ± 0.29 |

T=1'e karşı, tohum içinde eşleştirilmiş (ölçüt G3.1: |ort ΔECE| ÷ σ_kontrol ≥ 2 **ve** tüm
tohumlar aynı işarette; σ_kontrol = 0.0020):

| T | ort ΔECE | işaretler | oran | hüküm |
|---|---|---|---|---|
| 0.85 | +0.0117 ± 0.0023 | `+++` | **5.87×** | KURULU (zarar) |
| 0.95 | −0.0033 ± 0.0042 | `--+` | 1.68× | ÇÖZÜNMEDİ |
| 1.10 | +0.0020 ± 0.0045 | `+-+` | 0.98× | ÇÖZÜNMEDİ |
| 1.3406 | +0.0317 ± 0.0029 | `+++` | **15.89×** | KURULU (zarar) |

## Hüküm — ve fazla okunmaması gereken yeri

**Ön-beyanlı tahmin yanlışlanmadı.** İki yeni noktanın ikisi de ölçütü karşılamıyor: 0.95 işaret
tutarlılığında düşüyor (`--+`), 1.10 hem işarette hem büyüklükte (0.98×).

**Ama "iç optimum yok" DENEMEZ, ve bu ayrım burada gerçekten önemli.** Beş noktalı serinin
**nokta-tahmin minimumu native T=1'de değil, T=0.95'te** (0.0296 vs 0.0330). Bu, öğretmenin
kendi **T\*_NLL = 0.983**'ünün hemen yanında sığ bir iç optimumun üreteceği şeklin ta kendisi.
Yani veri, "optimum yok" ile "optimum var ama 2× tohum gürültüsünden sığ" arasında **ayrım
yapmıyor**.

Savunulabilir cümle: **"kontrol öğretmeni, tohum gürültüsünün iki katıyla çözünebilecek bir iç
optimum göstermiyor."** Savunulamaz cümle: *"kontrol öğretmeninin iç optimumu yoktur."*

**G0'ın asıl kazandırdığı bu.** Testin daha önce dişi yoktu: en yakın sınama noktası 0.15
uzaktaydı ve gözlenen büyüklükte (~0.003) bir optimumu yakalayamazdı. Şimdi grid 0.05
çözünürlüğünde ve iki yeni nokta öğretmenin kendi optimumlarını kuşatıyor. Tahmin,
**öldürebilecek bir testten geçti** — ama geçme biçimi "etki yok" değil, "etki ölçülemedi".

**U'nun kolları sağlam, tabanı değil.** 0.85 (5.87×) ve 1.3406 (15.89×) hücrelerinin ikisi de
3/3 işaretle kurulu. Doz-yanıt omurgası bundan etkilenmiyor; belirsiz olan yalnız native
çevresindeki düzlük.

**Doğruluk ekseni hiçbir şey söylemiyor:** beş nokta 89.93–90.09 pp arasında, tohum sd'leri
0.06–0.37. Beklendiği gibi — bu bir kalibrasyon iddiası, doğruluk iddiası değil.

## Çıkış kontrolü

| kalem | sonuç |
|---|---|
| beklenen grid × tohum | 5 × 3 = 15 |
| denetimde mevcut | 15 |
| **birden çok denemesi olan koşu (çökme izi)** | **1** |
| elenen yarım deneme | 1 |
| ad → parametre uyuşmazlığı | **0** |
| anahtar yok, belgelenmiş varsayılan kabul edildi | 3 |

**Çoklu-attempt kalemi ayrıca raporlandı, çünkü G0'ın bütün değeri buna bağlı.** 6 Ağu ~05:43
elektrik kesintisi `T110_seed42`'yi **399/400** epoch'ta öldürdü. O koşu **devam ettirilmedi,
epoch 0'dan temiz yeniden başlatıldı**: kesilip devam eden bir koşu optimizer durumu ve veri
sırası bakımından temiz koşuyla aynı değildir, ve G0'ın tek iddiası "tarif birebir aynı, yalnız
T farklı" olduğu için bu karşılaştırılabilirliği bozardı. Zaten mümkün de değildi —
`train_rafdb_kd.py`'de `--resume` yok ve `swa_student.pth` yazılmamıştı (SWA ortalaması yalnız
bellekte yaşıyordu). Yarım dizin `ABANDONED.json` ile işaretlendi, silinmedi, ve kaç epoch'ta
öldüğüyle tabloda görünüyor.

**Üç "varsayılana düşen anahtar" sessiz geçilmedi.** T=1 kolları `--teacher-temperature-scale`
bayrağı eklenmeden önce koşulmuş; anahtar `run_args.json`'da yanlış değerde değil, **hiç yok**.
Betik bunu uyuşmazlık saymıyor ama hangi koşuda hangi anahtarın varsayılana düştüğünü **tek tek
listeliyor** — "eksik anahtar ≠ yanlış değer", ama ikisi de görünür olmalı.

## Makaleye ne düşüyor

- §5'te kontrol argümanı **daha güçlü bir testle** desteklenebilir, ama ifadesi
  **"çözünebilir bir iç optimum yok"** olarak daraltılmalı.
- Bu satırlar **ön-beyanlı değil** ve öyle etiketlenmeli (B8).
- Tablo kapısı doğrulandı: **702/702, sapma yok** — 6 yeni koşu tek bir RESULTS_TABLES
  hücresine sızmadı, yani G0 §4.5 envanterinden yapısal olarak da uzak.

---

Kaynaklar: `paper_tables/control_grid_refinement.{md,json}` ·
`PREREGISTRATIONS.md` §B8 · kuyruk `rafdb_g0_control_grid_queue.ps1` (commit `9604c61`,
koşulardan önce)
