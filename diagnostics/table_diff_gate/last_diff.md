# Table diff gate — last comparison

Baseline: **2026-08-18T02:45:04** — N14 ucuncu tur (iki karar): 29 sapma, HEPSI APPEARED, CHANGED/MOVED/VANISHED YOK. Iki grup: (1) kanonik-vs-teyit kaydi -- tstar_sensitivity'nin yeni cross_fit blogu (confirm_T_star, abs_dT, d_nll, d_ece) ve defterin cross_checks blogu (uc nicelik icin kanonik deger, teyit degeri, ayrisma ve TOLERANS). Tolerans elle yazilmadi, makalenin kendi hassasiyetinden turetiliyor (0.5 x 10^-d, d = o nicelik icin kullanilan en siki yuvarlama), o yuzden esigin kendisi de kapida duruyor. (2) iki yeni sayac (cross_checks, cross_check_fail). Olculen ayrisma: stage1 9.87e-6 (tol 5e-5), primary 4.05e-6 (tol 5e-4), vae9182 1.46e-4 (tol 5e-4); amac fonksiyonu farki dNLL 0.00e+00 / 0.00e+00 / 2.98e-8, yani NLL iki adayi ayirt edemiyor.  
Cells compared: 1453 (1441 in the baseline)

## Value moved by more than its own seed sd

| cell | old | new | diff | threshold | source of the threshold |
|---|---|---|---|---|---|
| `N13/count/bound` | 617.0000 | 687.0000 | +70.0000 | 13.7400 | 2% rel (no sd) |
| `N13/count/derived` | 16.0000 | 21.0000 | +5.0000 | 0.4200 | 2% rel (no sd) |
| `N13/count/exempt` | 90.0000 | 150.0000 | +60.0000 | 3.0000 | 2% rel (no sd) |
| `N13/count/layout_dropped` | 166.0000 | 178.0000 | +12.0000 | 3.5600 | 2% rel (no sd) |
| `N13/count/tokens` | 719.0000 | 862.0000 | +143.0000 | 17.2400 | 2% rel (no sd) |
| `N13/count/unbound` | 0.0000 | 8.0000 | +8.0000 | 0.1600 | 2% rel (no sd) |
| `N13/unbound_ids` | 0.0000 | 8.0000 | +8.0000 | 0.1600 | 2% rel (no sd) |

## Cells appeared / vanished

**appeared:** `N13/count/derived_in_scope`, `N13/count/derived_prose_anchored`, `N13/derived/jsd_smallest_stratum_pct`, `N13/derived/jsd_smallest_stratum_pct/ok`, `N13/derived/robust_agreeing_steps`, `N13/derived/robust_agreeing_steps/ok`, `N13/derived/robust_agreement_pct`, `N13/derived/robust_agreement_pct/ok`, `N13/derived/tstar_criterion_cost_max_supp`, `N13/derived/tstar_criterion_cost_max_supp/ok`, `N13/derived/tstar_criterion_cost_min_supp`, `N13/derived/tstar_criterion_cost_min_supp/ok`

