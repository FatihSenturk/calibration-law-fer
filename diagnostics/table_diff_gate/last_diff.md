# Table diff gate — last comparison

Baseline: **2026-08-20T17:37:36** — N19b (20 Agu, son 23): 39 sapma, hicbiri CHANGED/VANISHED degil -- yani ONCEDEN YAYIMLANMIS hicbir olcum degeri degismedi. 7 MOVED defterin KENDI sayaclari (kayitsiz 23 -> 0, turetilmis 67 -> 72, uyusmazlik 2 -> 3, turetilmis-uyusmazlik 0 -> 1, sorun 2 -> 4). 32 APPEARED yeni hucre: (a) G3.2/sim/* yanlis-pozitif simulasyonunun bes niceligi, artik MC degil KAPALI FORMDAN (Gauss-Legendre, ~1e-15) -- basili 0.543/0.740/0.007 200k ve 40k tekrarlik MC kosularindan geliyordu ve ucuncu basamak MC gurultusuydu; tam degerler 0.545/0.741/0.009 ve UCU DE bilerek kirmizi birakildi, uretici basiliyi tutturacak sekilde AYARLANMADI. (b) RMC/* kosu manifesti sayimi (90/26/62/2) ve PENCERE ETIKETI, etiket sayilan manifestlerin kendi zaman damgalarindan turetiliyor. (c) REL/*/top_bin en yuksek guven kutusundaki kutle (89.9/82.7) -- uretici bu iki sayiyi ekrana basiyor ama artefakta yazmiyordu. (d) T8*/argmax_in_last_K_count oranin PAYI (45/131, 88/131). (e) N13/derived/* bes yeni turetme: R^2 tabani (min, ASAGI yuvarlama), taban ECE orani, uc bilesik sicaklik. FERPlus bilesik sicakligi (3.06 vs 3.04) dorduncu acik kalem: 0.5063 x 6 = 3.0378, basili 3.06 ancak 0.51 x 6 ile cikar.  
Cells compared: 1643 (1635 in the baseline)

## Cells appeared / vanished

**appeared:** `PL/A1_lead_s`, `PL/A2_lead_s`, `PL/A3_lead_s`, `PL/A4_lead_s`, `PL/A7_lead_s`, `PL/A8_lead_s`, `PL/n_annotation_checked`, `PL/n_runs_csv_checked`

