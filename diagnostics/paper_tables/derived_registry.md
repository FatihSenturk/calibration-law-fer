# N13 — Derived quantity registry

Every printed ratio or difference, with its numerator and denominator as artifact field paths, so it can be recomputed from the ledger instead of from printed values. Two of today's three errors came from dividing rounded printed cells.

| id | printed | formula | operands | recomputed | ok |
|---|---|---|---|---|---|
| `jsd_collapse` | 37 | ratio | `paper_tables/r3w1_joint_optimum.json` → `arms["0.26"].jsd_arm[0] - arms["0.74"].jsd_arm[0]` ÷ `paper_tables/r3w1_joint_optimum.json` → `arms["0.74"].jsd_ts[0] - arms["0.26"].jsd_ts[0]` | 37.2342 | yes |
| `jsd_noise_ratio` | 40 | ratio | `paper_tables/jsd_collapse_audit.json` → `numerator.value` ÷ `paper_tables/jsd_collapse_audit.json` → `R_noise.seed_sd_by_convention["mean sd"]` | 39.8126 | yes |
| `capacity_vs_teacher_lever` | 76 | ratio | `paper_tables/RESULTS_TABLES.json` → `T10_axis_spans.swa.teacher_span` ÷ `paper_tables/RESULTS_TABLES.json` → `T10_axis_spans.swa.capacity_span` | 75.7089 | yes |
| `selection_cost_best` | 0.52 | diff | `p4_teacher_selection/p4_teacher_selection.json` → `recipe_step3_ranking.rows[teacher=vae9182].student_by_ckpt.best.acc_mean` ÷ `p4_teacher_selection/p4_teacher_selection.json` → `recipe_step3_ranking.rows[teacher=stage1].student_by_ckpt.best.acc_mean` | 0.521515 | yes |
| `selection_cost_swa` | 0.35 | diff | `p4_teacher_selection/p4_teacher_selection.json` → `recipe_step3_ranking.rows[teacher=vae9182].student_by_ckpt.swa.acc_mean` ÷ `p4_teacher_selection/p4_teacher_selection.json` → `recipe_step3_ranking.rows[teacher=stage1].student_by_ckpt.swa.acc_mean` | 0.347674 | yes |
| `selection_cost_last` | 0.83 | diff | `p4_teacher_selection/p4_teacher_selection.json` → `recipe_step3_ranking.rows[teacher=vae9182].student_by_ckpt.last.acc_mean` ÷ `p4_teacher_selection/p4_teacher_selection.json` → `recipe_step3_ranking.rows[teacher=stage1].student_by_ckpt.last.acc_mean` | 0.825727 | yes |
| `human_trade_ece` | +0.0159 | diff | `ferplus_jsd/ferplus_student_jsd.json` → `by_checkpoint.swa["0.74"].ece[0]` ÷ `ferplus_jsd/ferplus_student_jsd.json` → `by_checkpoint.swa["0.5063"].ece[0]` | 0.0158646 | yes |
| `human_trade_jsd` | -0.0051 | diff | `ferplus_jsd/ferplus_student_jsd.json` → `by_checkpoint.swa["0.74"].jsd[0]` ÷ `ferplus_jsd/ferplus_student_jsd.json` → `by_checkpoint.swa["0.5063"].jsd[0]` | -0.00509233 | yes |
| `collapse_ratio_5_10` | 16.3 | ratio | `paper_tables/RESULTS_TABLES.json` → `T11_collapse.pairs["T·τ = 5.10"].mean` ÷ `paper_tables/RESULTS_TABLES.json` → `T11_collapse.two_bar` | 16.3044 | yes |
| `collapse_ratio_10_20` | 13.5 | ratio | `paper_tables/RESULTS_TABLES.json` → `T11_collapse.pairs["T·τ = 10.20"].mean` ÷ `paper_tables/RESULTS_TABLES.json` → `T11_collapse.two_bar` | 13.5023 | yes |
| `selection_cost_best_caption` | 0.52 | diff | `p4_teacher_selection/p4_teacher_selection.json` → `recipe_step3_ranking.rows[teacher=vae9182].student_by_ckpt.best.acc_mean` ÷ `p4_teacher_selection/p4_teacher_selection.json` → `recipe_step3_ranking.rows[teacher=stage1].student_by_ckpt.best.acc_mean` | 0.521515 | yes |
| `ece_reduction_min` | 41 | pct_drop | `p1_dose_response/two_dataset_overlay.json` → `arms.rafdb_stage1.points[1].by_ckpt.swa.ece_mean` ÷ `p1_dose_response/two_dataset_overlay.json` → `arms.rafdb_stage1.points[2].by_ckpt.swa.ece_mean` | 41.4635 | yes |
| `ece_reduction_max` | 76 | pct_drop | `p1_dose_response/two_dataset_overlay.json` → `arms.ferplus.points[3].by_ckpt.swa.ece_mean` ÷ `p1_dose_response/two_dataset_overlay.json` → `arms.ferplus.points[1].by_ckpt.swa.ece_mean` | 76.3748 | yes |
| `accuracy_band_widest_arm` | 0.51 | diff | `p1_dose_response/two_dataset_overlay.json` → `arms.rafdb_vae9182.points[2].by_ckpt.swa.acc_mean` ÷ `p1_dose_response/two_dataset_overlay.json` → `arms.rafdb_vae9182.points[3].by_ckpt.swa.acc_mean` | 0.510646 | yes |
| `tstar_criterion_cost_min` | 13 | ratio | `paper_tables/tstar_sensitivity.json` → `results.ferplus.ece_removed_by_ts` ÷ `paper_tables/tstar_sensitivity.json` → `results.ferplus.d_ece` | 13.307 | yes |
| `tstar_criterion_cost_max` | 14 | ratio | `paper_tables/tstar_sensitivity.json` → `results.stage1.ece_removed_by_ts` ÷ `paper_tables/tstar_sensitivity.json` → `results.stage1.d_ece` | 14.3155 | yes |
