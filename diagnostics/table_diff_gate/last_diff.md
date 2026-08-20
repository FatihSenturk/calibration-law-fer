# Table diff gate — last comparison

Baseline: **2026-08-20T16:31:27** — N19 (20 Agu, son tur): GOVDE DUZYAZISI defter kapsamina girdi. 102 sapma: 10 MOVED ve 92 APPEARED; CHANGED/VANISHED YOK -- hicbir OLCUM degeri degismedi, degisen kapsamin kendisi. MOVED olanlarin onu da defterin KENDI sayaclari: jeton 862 -> 1677, bagli 695 -> 1095, muaf 150 -> 496, turetilmis 21 -> 67, yerlesim 178 -> 340, KAYITSIZ 0 -> 23, uyusmazlik 0 -> 2. APPEARED olanlar yeni turetilmis kayitlar ve ferplus_abstention_entropy in butun-fold sayimlari (n_rows_all_folds 31412, rows_below_ten_all_folds 9204, share_below_ten_all_folds %29,3009) -- bu son uc alan bu turda YAZILDI cunku makalenin %29,3 sayisinin ureticisi yoktu. UYUSMAZLIK 2 ve IKISI DE GERCEK MAKALE KUSURU (ortulmedi): §1:151 ve §2:229 "+0.65" basiyor, alan 0.6445305842767274 yani 2 basamakta 0.64; 0.65 ancak CIFT YUVARLAMAYLA cikiyor (0.6445 -> 0.645 -> 0.65) ve makale ayni niceligi §4:150, §5:781, tab_selection_audit:25 te 3 basamakla DOGRU basiyor.  
Cells compared: 1635 (1603 in the baseline)

## Value moved by more than its own seed sd

| cell | old | new | diff | threshold | source of the threshold |
|---|---|---|---|---|---|
| `N13/count/derived` | 67.0000 | 72.0000 | +5.0000 | 1.4400 | 2% rel (no sd) |
| `N13/count/derived_in_scope` | 63.0000 | 68.0000 | +5.0000 | 1.3600 | 2% rel (no sd) |
| `N13/count/derived_mismatch` | 0.0000 | 1.0000 | +1.0000 | 0.0200 | 2% rel (no sd) |
| `N13/count/mismatch` | 2.0000 | 3.0000 | +1.0000 | 0.0600 | 2% rel (no sd) |
| `N13/count/problems` | 2.0000 | 4.0000 | +2.0000 | 0.0800 | 2% rel (no sd) |
| `N13/count/unbound` | 23.0000 | 0.0000 | -23.0000 | 0.0001 | 2% rel (no sd) |
| `N13/unbound_ids` | 23.0000 | 0.0000 | -23.0000 | 0.0001 | 2% rel (no sd) |

## Cells appeared / vanished

**appeared:** `G3.2/sim/family_wise_at_median_k`, `G3.2/sim/family_wise_at_own_k`, `G3.2/sim/family_wise_with_shared_component`, `G3.2/sim/independence_gap_own_k_minus_shared`, `G3.2/sim/n_family_cells`, `G3.2/sim/per_cell_rate_at_median_k`, `G3.2/sim/rho_other_pairs`, `G3.2/sim/rho_shared_control`, `N13/derived/s5.baseline_ece_ratio`, `N13/derived/s5.baseline_ece_ratio/ok`, `N13/derived/s5.composite_T_ferplus`, `N13/derived/s5.composite_T_ferplus/ok`, `N13/derived/s5.composite_T_stage1`, `N13/derived/s5.composite_T_stage1/ok`, `N13/derived/s5.composite_T_vae9182`, `N13/derived/s5.composite_T_vae9182/ok`, `N13/derived/s5.r2_floor`, `N13/derived/s5.r2_floor/ok`, `REL/T=1.3406/top_bin_n`, `REL/T=1.3406/top_bin_share_pct`, `REL/T=1/top_bin_n`, `REL/T=1/top_bin_share_pct`, `RMC/checksum_ok`, `RMC/n_code_state_verified`, `RMC/n_manifests`, `RMC/n_retroactive_unverified`, `RMC/n_unfinished`, `RMC/window_label`, `T8/K=100/argmax_in_last_K_count`, `T8/K=50/argmax_in_last_K_count`, `T8w/K=100/argmax_in_last_K_count`, `T8w/K=50/argmax_in_last_K_count`

