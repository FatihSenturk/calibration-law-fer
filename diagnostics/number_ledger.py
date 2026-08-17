"""N13 — SAYI PROVENANS DEFTERI: makaledeki her tablo hucresi hangi alandan geliyor?

NEDEN. 17 Agu 2026'da uc ayri taraf sayisal hata yapti ve ucu de TESADUFEN yakalandi: biri PDF'e
baktigi icin, biri defterle karsilastirdigi icin, biri kendi hukmunu gozden gecirdigi icin.
Tesaduf bir savunma degil. Onceki tur bir prototipi olctu: "bu sayi havuzda var mi?" sorusu
makaledeki sayilarin %98.9'unu esliyor ama bayat degerlerin dordunden ucunu KACIRIYOR -- cunku
bayat bir deger de bir yerde vardir, eskiden dogruydu. Ve r=0.724 vakasinda sayi gercekti, dogru
artefaktaydi, yalniz YANLIS KOLA baglanmisti. Varlik kontrolu bunu asla yakalayamaz.

BU YUZDEN DEFTER DEGERI DEGIL, DEGER<->ALAN BAGINI kaydeder. Her basili sayi icin: hangi
artefakt, o artefaktin hangi alani, hangi yuvarlama, makalede nerede. Bag kurulmaya zorlandigi
anda yanlis bag GORUNUR hale gelir.

BU BETIK NE URETIR
  paper_tables/number_ledger.{md,json}      -- alan baglama (tablo hucreleri + manset)
  paper_tables/derived_registry.{md,json}   -- oran/fark gibi TURETILMIS nicelikler, pay/payda
Denetci ayri betiktir: `diagnostics/check_numbers.py` (ayni tarayiciyi ITHAL eder).

KAPSAM (beyan, bu tur)
  girer : paper/tables/*.tex butun hucreleri · ozetteki manset sayilar · supplementary S8-S11
  girmez: sections/*.tex duzyazisi (revizyon penceresi) · supplementary S1-S3 (bugunku headroom
          turunun sonucu oraya henuz islenmedi; degisecek bir hucreyi baglamak curuk)
  olcum degil (baglanmaz, sinifiyla beyan edilir): hiperparametreler (tau, alpha, lr, epoch,
          tohum kimlikleri), veri kumesi/populasyon sayimlari, sayfa/yil/DOI, mimari boyutlari,
          sutun basliklarindaki sayilar.

KAGIT AGACI. `--paper-root` ile verilir; kodda MUTLAK YOL YOK. Yol verilmezse (Level-1 kapisi
ureticileri argumansiz cagirir) betik MEVCUT defteri KORUR ve 0 doner -- artefakti bozmaz.

Kullanim: python diagnostics/number_ledger.py --paper-root "<...>/paper"
"""
import argparse
import json
import os
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "diagnostics"))

from paper_number_scan import scan_paper  # noqa: E402

D = ROOT / "diagnostics"
OUT_DIR = D / "paper_tables"

# --- artefakt kisaltmalari (yol depo kokune gore, `diagnostics/` altinda)
A_TDO = "p1_dose_response/two_dataset_overlay.json"
A_DRS = "paper_tables/dose_response_per_seed.json"
A_RT = "paper_tables/RESULTS_TABLES.json"
A_P4 = "p4_teacher_selection/p4_teacher_selection.json"
A_CSM = "paper_tables/control_sd_mde.json"
A_INF = "paper_tables/inferential_tests.json"
A_EFF = "paper_tables/efficiency_retention.json"
A_LAT = "p5_efficiency/latency_benchmark.json"
A_SG = "selection_audit/selection_gain.json"
A_OST = "paper_tables/order_stat_trend.json"
A_FSJ = "ferplus_jsd/ferplus_student_jsd.json"
A_R3W = "paper_tables/r3w1_joint_optimum.json"
A_JCA = "paper_tables/jsd_collapse_audit.json"
A_ASY = "paper_tables/asymmetry_estimand.json"
A_HR = "paper_tables/headroom_review.json"
A_CRIT = "paper_tables/criterion_applied.json"
# --- N14 (17 Agu 2026): kayitsiz 28 kalemin kapatilmasi icin acilan artefaktlar
A_NU = "paper_tables/noise_units.json"
A_TSS = "paper_tables/tstar_sensitivity.json"
A_TSP = "paper_tables/tstar_provenance.json"
A_SAI = "paper_tables/selection_audit_inference.json"

BINDINGS = []      # alan baglari
DERIVED = []       # turetilmis nicelikler
EXEMPT = []        # olcum-degil beyanlari
PROSE = []         # duzyazida beyan edilen tek tek baglar


def b(unit, sec, row, idx, artifact, path, rounding, ident=None):
    BINDINGS.append({"id": ident or f"{unit}.s{sec}.{row}.{idx}", "unit": unit, "section": sec,
                     "row": row, "idx": idx, "artifact": artifact, "path": path,
                     "rounding": rounding})


# Bazi manset sayilar duzyazida HARFLE yaziliyor ("roughly forty times the noise"). Capa
# kontrolu rakami arar; harfle yazilan degerler icin karsiligi BEYAN edilir.
SPELLED = {"40": "forty", "76": "seventy-six", "37": "thirty-seven", "27": "twenty-seven"}


def dv(ident, printed, kind, operands, rounding, where_unit, sec, row, idx, note="",
       where=None):
    DERIVED.append({"id": ident, "printed": printed, "formula": kind, "operands": operands,
                    "rounding": rounding, "unit": where_unit, "section": sec, "row": row,
                    "idx": idx, "note": note, "where_literal": where})


def pv(ident, artifact, path, rounding, where, note=""):
    """DUZYAZIDA duran bir sayinin alan bagi. Kapsam disi olan duzyazi TARANMAZ, ama tek tek
    beyan edilen cumleler baglanabilir: denetci o SATIRI okur ve alanin yuvarlanmis degerinin
    orada gectigini dogrular. r=0.724 vakasi tam bu yolla yakalanir -- sayi dogru, artefakt
    dogru, bag yanlissa yuvarlanmis deger o satirda GECMEZ."""
    PROSE.append({"id": ident, "artifact": artifact, "path": path, "rounding": rounding,
                  "where": where, "note": note})


def ex(unit, sec, row, idx, klass, why, opt=False):
    """`opt=True`: bu muafiyet bazi bloklarda hic jetona denk gelmeyebilir (orn. adinda
    basamak olmayan FERPlus basligi). Kalan muafiyetler eslesmezse SORUN olarak raporlanir --
    yoksa curumus bir muafiyet sessizce durur."""
    EXEMPT.append({"unit": unit, "section": sec, "row": row, "idx": idx,
                   "class": klass, "why": why, "optional": opt})


# =============================================================================
# 1 · tab_dose_response — uc blok, `two_dataset_overlay` tek kaynak
# =============================================================================
DOSE = [(0, "rafdb_stage1", ["0.85", "1.00", "1.34", "1.70", "2.20"]),
        (1, "rafdb_vae9182", ["0.85", "1.00", "1.34", "1.70", "2.20"]),
        (2, "ferplus", ["0.26", "0.51", "0.74", "1.00"])]
DOSE_COLS = [("teacher_ece", "teacher_ece", "4dp"), ("signed_gap", "signed_gap", "4dp"),
             ("ece_swa_mean", "by_ckpt.swa.ece_mean", "4dp"),
             ("ece_swa_sd", "by_ckpt.swa.ece_sd", "4dp"),
             ("ece_last_mean", "by_ckpt.last.ece_mean", "4dp"),
             ("ece_last_sd", "by_ckpt.last.ece_sd", "4dp"),
             ("acc_swa_mean", "by_ckpt.swa.acc_mean", "2dp"),
             ("acc_swa_sd", "by_ckpt.swa.acc_sd", "2dp")]
for sec, arm, rows in DOSE:
    for i, row in enumerate(rows):
        for k, (name, tail, rnd) in enumerate(DOSE_COLS):
            b("tab_dose_response", sec, row, k, A_TDO,
              f"arms.{arm}.points[{i}].{tail}", rnd,
              ident=f"tab_dose_response.{arm}.T{row}.{name}")
# blok basliklari: ogretmenin T=1'deki ECE'si + basilan T
for sec, arm, i_T1 in ((0, "rafdb_stage1", 1), (1, "rafdb_vae9182", 1)):
    b("tab_dose_response", sec, "§header", 1, A_TDO,
      f"arms.{arm}.points[{i_T1}].teacher_ece", "4dp",
      ident=f"tab_dose_response.{arm}.header.teacher_ece_T1")
    ex("tab_dose_response", sec, "§header", 0, "teacher_name_digits",
       "blok basliginda gecen ogretmen adinin icindeki basamak (Stage1 / VAE9182)", opt=True)
# Baslikta 'T*' diye basilan sayi 17 Agu'a kadar IKI FARKLI niceligi tasiyordu: Stage1'de
# DAGITILAN sicaklik (1.3406), VAE9182'de FIT (0.98294). Defter ikisini ayri alanlara baglayinca
# cakisma gorunur oldu ve makale tarafinda duzeltildi -- artik UC baslik da FIT degeri basiyor
# (T^*_NLL) ve dagitilan kol alt yazida ayrica adlandiriliyor. Bag da o yuzden tek alan ailesine
# tasindi: ucu de `tstar_sensitivity.results.<ogretmen>.published_full_nll`, yani alt yazidaki
# 1.3494 ile basliktaki 1.35 KANITLANABILIR bicimde ayni sayi.
# DIKKAT — BEYAN OLAN ALANA BAGLANMAZ. `tstar_sensitivity.results.*.published_full_nll` ve
# `.deployed_T` ELLE YAZILMIS sabit sozluklerdir (`tstar_stability.PUBLISHED`,
# `tstar_sensitivity.DEPLOYED`): "kampanyada su deger yayimlandi/dagitildi" BEYANI, olcum degil.
# Basili sayiyi oraya baglamak dairesel olurdu -- alan, basili sayinin elle yazilmis kopyasi.
# Bag bu yuzden OLCULEN fite kuruluyor: `T_star_nll`, uretici tarafindan hesaplanan tam-fold NLL
# optimumu (n=3068/3153).
for sec, t in ((0, "stage1"), (1, "vae9182"), (2, "ferplus")):
    b("tab_dose_response", sec, "§header", 2 if sec < 2 else 1, A_TSS,
      f"results.{t}.T_star_nll", "2dp",
      ident=f"tab_dose_response.{t}.header.T_star_fit")
b("tab_dose_response", 2, "§header", 0, A_TDO, "arms.ferplus.points[3].teacher_ece", "4dp",
  ident="tab_dose_response.ferplus.header.teacher_ece_T1")
# Alt yazi (17 Agu'da eklendi): dagitilan kol ile tam-fold fit yan yana adlandiriliyor. Ikisi de
# AYNI artefaktta duruyor -- cumlenin karsilastirdigi iki sayi tek kaynaktan geliyor.
DOSE_CAP = "under-confident so their corrections act in"
# 1.3406 = YARI-FOLD fit (dagitilan kolun kokeni), OLCULEN deger: `tstar_provenance` bu ayrimin
# artefakti ve iki fiti de kendisi hesapliyor. 1.3494 = tam-fold fit.
b("tab_dose_response", -1, DOSE_CAP, 1, A_TSP, "half_fold_fits.stage1", "4dp",
  ident="tab_dose_response.caption.stage1_half_fold_fit")
b("tab_dose_response", -1, DOSE_CAP, 2, A_TSS, "results.stage1.T_star_nll", "4dp",
  ident="tab_dose_response.caption.stage1_full_fold_fit")
b("tab_dose_response", -1, DOSE_CAP, 3, A_TSS, "results.vae9182.T_star_nll", "2dp",
  ident="tab_dose_response.caption.vae9182_fit")
ex("tab_dose_response", -1, DOSE_CAP, 0, "teacher_name_digits",
   "alt yazidaki 'Stage1' adinin icindeki basamak")
ex("tab_dose_response", -1, DOSE_CAP, 4, "hyperparameter",
   "kontrolun fit'ine en yakin EGITILMIS kol: T=1 -- tasarim degeri, olcum degil")

# =============================================================================
# 2 · app_seeds (S10) — tohum basina ogrenci ECE'si
# =============================================================================
SEEDS_ORDER = ["1", "42", "43"]
S10 = [(0, "rafdb_stage1", ["0.85", "1.00", "1.3406", "1.70", "2.20"]),
       (1, "rafdb_vae9182", ["0.85", "1.00", "1.3406", "1.70", "2.20"]),
       (2, "ferplus", ["0.26", "0.5063", "0.74", "1.00"])]
for sec, arm, rows in S10:
    for i, row in enumerate(rows):
        b("app_seeds", sec, row, 0, A_DRS, f"series.{arm}.points[{i}].teacher_ece", "4dp",
          ident=f"app_seeds.{arm}.T{row}.teacher_ece")
        b("app_seeds", sec, row, 1, A_DRS, f"series.{arm}.points[{i}].signed_gap", "4dp",
          ident=f"app_seeds.{arm}.T{row}.signed_gap")
        for k, s in enumerate(SEEDS_ORDER):
            b("app_seeds", sec, row, 2 + k, A_DRS,
              f'series.{arm}.points[{i}].per_seed["{s}"].ece', "4dp",
              ident=f"app_seeds.{arm}.T{row}.seed{s}")
        b("app_seeds", sec, row, 5, A_DRS, f"series.{arm}.points[{i}].ece_mean", "4dp",
          ident=f"app_seeds.{arm}.T{row}.mean")
        b("app_seeds", sec, row, 6, A_DRS, f"series.{arm}.points[{i}].ece_sd", "4dp",
          ident=f"app_seeds.{arm}.T{row}.sd")
    ex("app_seeds", sec, "§header", None, "teacher_name_digits",
       "blok basliginda gecen ogretmen adinin icindeki basamak", opt=True)
ex("app_seeds", -1, "T", None, "column_header",
   "sutun basligindaki tohum kimlikleri (1/42/43)", opt=True)

# =============================================================================
# 3 · app_sd (S8) + app_mde (S9) — control_sd_mde tek kaynak
# =============================================================================
CW = {"eff.": "effective_number", "none": "none"}
for ck_tex, ck in (("SWA", "swa"), ("best", "best"), ("last", "last")):
    for t_tex, t in (("Stage1", "stage1"), ("Primary", "primary"), ("VAE9182", "vae9182")):
        for cw_tex, cw in CW.items():
            row = f"{ck_tex} {t_tex} {cw_tex}"
            sel = f"rows[checkpoint={ck}][teacher={t}][class_weight_mode={cw}]"
            for k, (axis, field, rnd) in enumerate(
                    [("ece", "control_level", "4dp"), ("ece", "control_sd", "4dp"),
                     ("acc", "control_level", "3dp"), ("acc", "control_sd", "3dp")]):
                b("app_sd", -1, row, k, A_CSM, f"{sel}[axis={axis}].{field}", rnd,
                  ident=f"app_sd.{ck}.{t}.{cw}.{axis}_{field}")
            for k, (axis, field, rnd, sc) in enumerate(
                    [("ece", "mde_2sd", "4dp", 1), ("ece", "mde_pct_of_level", "1dp", 1),
                     ("acc", "mde_2sd", "3dp", 1), ("acc", "mde_pct_of_level", "1dp", 1)]):
                b("app_mde", -1, row, k, A_CSM, f"{sel}[axis={axis}].{field}", rnd,
                  ident=f"app_mde.{ck}.{t}.{cw}.{axis}_{field}")
ex("app_sd", -1, "checkpoint teacher cw", None, "column_header", "sutun basligi",
   opt=True)
ex("app_mde", -1, "checkpoint teacher cw", None, "column_header",
   "sutun basligi ($2\\sigma$ icindeki 2)")
ex("app_sd", -1, "All rows are three seeds ( 1 42 43 ) sample standard", None,
   "hyperparameter", "tohum kimlikleri ve tohum sayisi")
ex("app_mde", -1, "2 of the control arm absolutely and as a fraction of", None,
   "criterion_constant", "olcutun kendisi: 2 sigma (esik tanimi, olcum degil)")

# =============================================================================
# 4 · tab_mechanisms (T5) + tab_logitstd (T5a) — RESULTS_TABLES.T5
# =============================================================================
# Hangi hucre DOLU: `---` yazan hucre jeton uretmez, dolayisiyla jeton indisleri kayar.
# "G2G + adaptive T" satirinda yalniz VAE9182 dolu. N13'te "T5'te bu bilesik hucre YOK" diye
# kayitsiz birakilmisti; DUZELTME (17 Agu): T5 gercekten 21 hucre tasiyor ama bilesimi baska --
# stage1/primary yedi mekanizma, vae9182 ise `gate:target_logvar` yerine `g2g_kl+adaptive_t`.
# Yani hucre artefaktta VARDI, eksik olan beyandi. Tek tohumlu kol (n=1, sd=0), tabloda da
# dagger ile isaretli.
MECH_ROWS = [("Adaptive temperature", "adaptive_t", ["stage1", "primary", "vae9182"]),
             ("CTKD", "ctkd", ["stage1", "primary", "vae9182"]),
             ("G2G (class-space KL)", "g2g_kl", ["stage1", "primary", "vae9182"]),
             ("Gate mean logvar", "gate:mean_logvar", ["stage1", "primary", "vae9182"]),
             ("Gate target logvar", "gate:target_logvar", ["stage1", "primary"]),
             ("Gate oracle error", "gate:oracle_error", ["stage1", "primary", "vae9182"]),
             ("Logit standardisation", "logit_std", ["stage1", "primary", "vae9182"])]
for row, mech, teachers in MECH_ROWS:
    k = 0
    for t in teachers:
        cell = f'T5_mechanisms["{t}/{mech}"].swa'
        b("tab_mechanisms", -1, row, k, A_RT, f"{cell}.d_acc_mean", "2dp",
          ident=f"tab_mechanisms.{t}.{mech}.d_acc")
        b("tab_mechanisms", -1, row, k + 1, A_RT, f"{cell}.d_ece_mean", "4dp",
          ident=f"tab_mechanisms.{t}.{mech}.d_ece")
        k += 2
b("tab_mechanisms", -1, "G2G + adaptive T ^", 0, A_RT,
  'T5_mechanisms["vae9182/g2g_kl+adaptive_t"].swa.d_acc_mean', "2dp",
  ident="tab_mechanisms.vae9182.g2g_kl+adaptive_t.d_acc")
b("tab_mechanisms", -1, "G2G + adaptive T ^", 1, A_RT,
  'T5_mechanisms["vae9182/g2g_kl+adaptive_t"].swa.d_ece_mean', "4dp",
  ident="tab_mechanisms.vae9182.g2g_kl+adaptive_t.d_ece")
# T5a (`tab_logitstd`) alt yazisinin dort gurultu-birimi orani. Tanim `noise_units.py`de:
# (|dECE|/sigma_ECE) ÷ (|dacc|/sigma_acc), her kol KENDI kontrol sd'siyle. Dordu de o
# artefaktin ALANI -- yeniden bolme yok, basili yuvarlak degerden turetme hic yok.
b("tab_mechanisms", 0, "23 in the narrowest SWA comparison", 0, A_NU,
  'nine_cell_grid["swa|primary"].ratio', "int", ident="tab_logitstd.caption.narrowest_swa")
b("tab_mechanisms", 0, "of 27 (mean 52", 0, A_NU, "summary.median", "int",
  ident="tab_logitstd.caption.median")
b("tab_mechanisms", 0, "of 27 (mean 52", 1, A_NU, "summary.mean", "int",
  ident="tab_logitstd.caption.mean")
b("tab_mechanisms", 0, "the all-checkpoint floor is 2.6", 0, A_NU, "summary.min", "1dp",
  ident="tab_logitstd.caption.floor")
for t_tex, t in (("Primary", "primary"), ("Stage1", "stage1"), ("VAE9182", "vae9182")):
    for k, ck in enumerate(("swa", "best", "last")):
        b("tab_mechanisms", 0, t_tex, k, A_RT,
          f'T5_mechanisms["{t}/logit_std"].{ck}.d_acc_mean', "2dp",
          ident=f"tab_logitstd.{t}.{ck}.d_acc")
        b("tab_mechanisms", 0, t_tex, 3 + k, A_RT,
          f'T5_mechanisms["{t}/logit_std"].{ck}.d_ece_mean', "4dp",
          ident=f"tab_logitstd.{t}.{ck}.d_ece")
# T5 dipnotu (bolum 0'in baslik satiri): alti kontrol tohum sd'si, ikisi aralik ucu olarak
# TEKRAR basiliyor. Onu da ayni alana bagliyoruz -- ayni sayinin iki kez yazilmasi da bir bag.
FOOT_SD = [(0, "stage1", "effective_number"), (1, "vae9182", "effective_number"),
           (3, "stage1", "effective_number"), (4, "primary", "effective_number"),
           (6, "vae9182", "effective_number"), (7, "stage1", "none"),
           (8, "primary", "none"), (10, "stage1", "none"), (11, "primary", "none"),
           (13, "vae9182", "none")]
for idx, t, cw in FOOT_SD:
    b("tab_mechanisms", 0, "§header", idx, A_CSM,
      f"rows[checkpoint=swa][teacher={t}][class_weight_mode={cw}][axis=ece].control_sd", "4dp",
      ident=f"tab_mechanisms.foot.{t}.{cw}.{idx}")
for idx in (2, 5, 9, 12):
    ex("tab_mechanisms", 0, "§header", idx, "teacher_name_digits",
       "dipnotta gecen ogretmen adinin icindeki basamak (Stage1 / VAE9182)")
ex("tab_mechanisms", 0, "§header", 14, "table_reference", "Supplementary Table S8 atfi")
ex("tab_mechanisms", 0, "§header", 15, "table_reference", "Supplementary Table S9 atfi")

# =============================================================================
# 5 · tab_selection — p4 recipe_step3_ranking
# =============================================================================
for i, (row, t) in enumerate((("Stage1", "stage1"), ("Primary", "primary"),
                              ("VAE9182", "vae9182"))):
    sel = f"recipe_step3_ranking.rows[teacher={t}]"
    b("tab_selection", -1, row, 0, A_P4, f"{sel}.teacher_acc", "2dp",
      ident=f"tab_selection.{t}.teacher_acc")
    b("tab_selection", -1, row, 1, A_P4, f"{sel}.teacher_ece", "4dp",
      ident=f"tab_selection.{t}.teacher_ece")
    b("tab_selection", -1, row, 2, A_P4, f"{sel}.T_star", "3dp",
      ident=f"tab_selection.{t}.T_star")
    b("tab_selection", -1, row, 3, A_P4, f"{sel}.student_by_ckpt.best.acc_mean", "2dp",
      ident=f"tab_selection.{t}.student_acc_mean")
    b("tab_selection", -1, row, 4, A_P4, f"{sel}.student_by_ckpt.best.acc_sd", "2dp",
      ident=f"tab_selection.{t}.student_acc_sd")
    b("tab_selection", -1, row, 5, A_P4, f"{sel}.student_by_ckpt.best.ece_mean", "4dp",
      ident=f"tab_selection.{t}.student_ece")
b("tab_selection", -1, "( 89.60 pp each) and the cost of the accuracy rule i", 0, A_P4,
  "recipe_step3_ranking.rows[teacher=stage1].student_by_ckpt.swa.acc_mean", "2dp",
  ident="tab_selection.swa_tie")
# Dipnot TEK mantiksal satir: [0] rho_s(acc,acc) [1] rho_s(-ECE,acc) [2] 0.52 pp maliyet
# [3] kazanan tam deger [4] dogruluk-kuralinin tam degeri.
SEL_FOOT = "_s(teacher acc. student acc.)"
# Dipnotun iki sira korelasyonu: uc ogretmen uzerinden. N13'te "artefakti yok" diye kayitsiz
# birakilmisti; yanlis -- `p4_teacher_selection` ikisini de HESAPLIYOR, yalniz beyan edilmemisti.
b("tab_selection", -1, SEL_FOOT, 0, A_P4,
  "recipe_step3_ranking.spearman_teacherACC_vs_studentACC", "2dp",
  ident="tab_selection.rho_teacherACC_studentACC")
b("tab_selection", -1, SEL_FOOT, 1, A_P4,
  "recipe_step3_ranking.spearman_negTeacherECE_vs_studentACC", "2dp",
  ident="tab_selection.rho_negTeacherECE_studentACC")
b("tab_selection", -1, SEL_FOOT, 3, A_P4,
  "recipe_step3_ranking.rows[teacher=vae9182].student_by_ckpt.best.acc_mean", "4dp",
  ident="tab_selection.best_winner_exact")
b("tab_selection", -1, SEL_FOOT, 4, A_P4,
  "recipe_step3_ranking.rows[teacher=stage1].student_by_ckpt.best.acc_mean", "4dp",
  ident="tab_selection.best_acc_rule_exact")

# =============================================================================
# 6 · tab_holm — inferential_tests.results (sirali)
# =============================================================================
# Makale satirlari p_Holm'e gore siralanmis; artefaktin liste sirasi baska. Esleme ADLA
# kuruldu (asagidaki indisler `inferential_tests.results` icindeki gercek satirlar):
#   1 vae9182/logit_std (kontrol) · 2 stage1/logit_std · 3 stage1 T* · 4 FERPlus T* ·
#   5 primary/logit_std · 6 vae9182 oracle gate
HOLM = [("1", 3), ("2", 1), ("3", 0), ("4", 5), ("5", 2), ("6", 4)]
for row, i in HOLM:
    sel = f"results[{i}]"
    b("tab_holm", -1, row, 0, A_INF, f"{sel}.mean", "4dp", ident=f"tab_holm.rank{row}.mean")
    b("tab_holm", -1, row, 1, A_INF, f"{sel}.sd", "4dp", ident=f"tab_holm.rank{row}.sd")
    b("tab_holm", -1, row, 2, A_INF, f"{sel}.t", "1dp", ident=f"tab_holm.rank{row}.t")
    b("tab_holm", -1, row, 3, A_INF, f"{sel}.p_holm", "4dp", ident=f"tab_holm.rank{row}.p_holm")

# =============================================================================
# 7 · tab_human — ferplus_student_jsd @swa
# =============================================================================
HUMAN = [("0.26", "0.26"), ("0.51", "0.5063"), ("0.74", "0.74"), ("1.00", "1.0")]
for row, key in HUMAN:
    cell = f'by_checkpoint.swa["{key}"]'
    b("tab_human", -1, row, 0, A_FSJ, f"{cell}.teacher_ece", "4dp",
      ident=f"tab_human.T{key}.teacher_ece")
    b("tab_human", -1, row, 1, A_FSJ, f"{cell}.ece[0]", "4dp",
      ident=f"tab_human.T{key}.student_ece_mean")
    b("tab_human", -1, row, 2, A_FSJ, f"{cell}.ece[1]", "4dp",
      ident=f"tab_human.T{key}.student_ece_sd")
    b("tab_human", -1, row, 3, A_FSJ, f"{cell}.jsd[0]", "4dp",
      ident=f"tab_human.T{key}.jsd_mean")
    b("tab_human", -1, row, 4, A_FSJ, f"{cell}.jsd[1]", "4dp",
      ident=f"tab_human.T{key}.jsd_sd")
    b("tab_human", -1, row, 5, A_FSJ, f"{cell}.entropy", "3dp",
      ident=f"tab_human.T{key}.entropy")
HUM_FOOT = "Human annotator entropy"
b("tab_human", -1, HUM_FOOT, 0, A_FSJ, "human_mean_entropy", "3dp",
  ident="tab_human.human_entropy")

# =============================================================================
# 8 · tab_pooled — two_dataset_overlay.pooled_stats
# =============================================================================
for row, ck in (("SWA", "swa"), ("best", "best"), ("last", "last")):
    b("tab_pooled", -1, row, 0, A_TDO, f"pooled_stats.{ck}.spearman_abs_signed_gap", "3dp",
      ident=f"tab_pooled.{ck}.spearman_unsigned")
    # `r` (unsigned) sutunu 17 Agu'a kadar KAYITSIZDI: makalede duruyordu, hicbir artefakt
    # havuzlanmis 14 nokta uzerinde Pearson hesaplamiyordu. Karar (Fatih): sutunu silmek yerine
    # kaynagini uretmek -- `two_dataset_overlay.pearson`, Spearman'in yanina, ayni dongude.
    b("tab_pooled", -1, row, 1, A_TDO, f"pooled_stats.{ck}.pearson_abs_signed_gap", "3dp",
      ident=f"tab_pooled.{ck}.pearson_unsigned")
    b("tab_pooled", -1, row, 2, A_TDO, f"pooled_stats.{ck}.spearman_signed_gap", "3dp",
      ident=f"tab_pooled.{ck}.spearman_signed")
b("tab_pooled", -1, "Checkpoint _s (unsigned) r (unsigned) _s (signed)", None, None, None,
  None, ident="tab_pooled.header")
BINDINGS.pop()      # baslik satirinda sayi yok; yer tutucu geri alindi

ex("tab_pooled", -1, "calibration error over all 14 grid points", None, "population_count",
   "iki veri kumesinin izgara noktasi sayisi (14) -- olcum degil, sayim")

# =============================================================================
# 9 · tab_capacity — RESULTS_TABLES T10
# =============================================================================
CAP = [("width 0.50 scratch", "scratch w050"), ("width 0.75 scratch", "scratch w075"),
       ("width 1.00 scratch", "scratch w100ns"), ("width 1.00 pre-trained", "pretrained w100")]
CAP_PARAMS = {"scratch w050": 0.712, "scratch w075": 1.380,
              "scratch w100ns": 2.248, "pretrained w100": 2.248}
for row, cell in CAP:
    b("tab_capacity", -1, row, 1, A_RT, f'T10_capacity_cells.swa["{cell}"].acc_mean', "2dp",
      ident=f"tab_capacity.{cell}.acc_mean")
    b("tab_capacity", -1, row, 2, A_RT, f'T10_capacity_cells.swa["{cell}"].acc_sd', "2dp",
      ident=f"tab_capacity.{cell}.acc_sd")
    b("tab_capacity", -1, row, 3, A_RT, f'T10_capacity_cells.swa["{cell}"].ece_mean', "4dp",
      ident=f"tab_capacity.{cell}.ece_mean")
    b("tab_capacity", -1, row, 4, A_RT, f'T10_capacity_cells.swa["{cell}"].ece_sd', "4dp",
      ident=f"tab_capacity.{cell}.ece_sd")
    ex("tab_capacity", -1, row, 0, "architecture_dim",
       "ogrenci parametre sayisi (M) -- mimari boyutu, olcum degil")
CAP_FOOT = "Student-ECE range across the capacity axis"
b("tab_capacity", -1, CAP_FOOT, 1, A_RT, "T10_axis_spans.swa.capacity_span", "5dp",
  ident="tab_capacity.capacity_span")
b("tab_capacity", -1, CAP_FOOT, 2, A_RT, "T10_axis_spans.swa.teacher_span", "4dp",
  ident="tab_capacity.teacher_span")
ex("tab_capacity", -1, CAP_FOOT, 0, "architecture_dim",
   "3.16x parametre orani -- mimari boyut orani, olcum degil")

# =============================================================================
# 10 · tab_collapse — RESULTS_TABLES T11/T12
# =============================================================================
for row, key in (("T = 5.10", "T·τ = 5.10"), ("T = 10.20", "T·τ = 10.20")):
    b("tab_collapse", 0, row, 0, A_RT, f'T11_collapse.pairs["{key}"].mean', "4dp",
      ident=f"tab_collapse.{key}.mean")
    b("tab_collapse", 0, row, 1, A_RT, f'T11_collapse.pairs["{key}"].sd', "4dp",
      ident=f"tab_collapse.{key}.sd")
    ex("tab_collapse", 0, row, 2, "sign_count", "isaret sayaci 3/3 -- olcum degil, sayim")
    ex("tab_collapse", 0, row, 3, "sign_count", "isaret sayaci 3/3")
for row in ("0.1", "0.3", "0.5", "0.7", "0.9"):
    for k, s in enumerate(("42", "1", "43")):
        b("tab_collapse", 1, row, k, A_RT, f'T12_alpha.gaps["{row}"].by_seed["{s}"]', "4dp",
          ident=f"tab_collapse.alpha{row}.seed{s}")
    b("tab_collapse", 1, row, 3, A_RT, f'T12_alpha.gaps["{row}"].mean', "4dp",
      ident=f"tab_collapse.alpha{row}.mean")
b("tab_collapse", -1, "seed deviation 0.0024 ). Bottom: the benefit of pre-", 0, A_CSM,
  "rows[checkpoint=swa][teacher=stage1][class_weight_mode=effective_number][axis=ece].mde_2sd",
  "4dp", ident="tab_collapse.threshold_2bar")
ex("tab_collapse", 1, "T = 10.20", None, "column_header",
   "alpha bloguna ait sutun basligi (tohum kimlikleri 42/1/43); etiket ustteki satirdan tasindi")

# =============================================================================
# 11 · tab_efficiency — efficiency_retention + latency_benchmark
# =============================================================================
b("tab_efficiency", -1, "POSTER++ teacher", 0, A_EFF, "teacher.params_m", "3dp",
  ident="tab_efficiency.teacher.params_m")
b("tab_efficiency", -1, "POSTER++ teacher", 1, A_EFF, "teacher.flops_g", "3dp",
  ident="tab_efficiency.teacher.gmacs")
b("tab_efficiency", -1, "POSTER++ teacher", 2, A_EFF, "teacher.size_mb", "1dp",
  ident="tab_efficiency.teacher.size_mb")
b("tab_efficiency", -1, "POSTER++ teacher", 3, A_EFF, "teacher.acc", "2dp",
  ident="tab_efficiency.teacher.acc")
b("tab_efficiency", -1, "MobileNetV2Plus student", 0, A_EFF, "student.params_m", "3dp",
  ident="tab_efficiency.student.params_m")
b("tab_efficiency", -1, "MobileNetV2Plus student", 1, A_EFF, "student.flops_g", "3dp",
  ident="tab_efficiency.student.gmacs")
b("tab_efficiency", -1, "MobileNetV2Plus student", 2, A_EFF, "student.size_mb", "1dp",
  ident="tab_efficiency.student.size_mb")
b("tab_efficiency", -1, "MobileNetV2Plus student", 3, A_EFF, "by_checkpoint.swa.acc_mean",
  "2dp", ident="tab_efficiency.student.acc_mean")
b("tab_efficiency", -1, "MobileNetV2Plus student", 4, A_EFF, "by_checkpoint.swa.acc_sd",
  "2dp", ident="tab_efficiency.student.acc_sd")
b("tab_efficiency", -1, "ratio", 0, A_EFF, "compression.params_ratio", "1dp",
  ident="tab_efficiency.ratio.params")
b("tab_efficiency", -1, "ratio", 1, A_EFF, "compression.flops_ratio", "1dp",
  ident="tab_efficiency.ratio.flops")
b("tab_efficiency", -1, "ratio", 2, A_EFF, "compression.size_ratio", "1dp",
  ident="tab_efficiency.ratio.size")
b("tab_efficiency", -1, "ratio", 3, A_EFF, "headline.retention_pct_swa", "1dp",
  ident="tab_efficiency.ratio.retention")
# Gecikme dipnotu `\\emph{Latency ...}` ile basliyor, yani tarayici icin bir BOLUM basligi.
# Jetonlar: [0] fp32'nin 32'si, sonra her cihaz icin (yigin, hizlanma) ikilileri.
for k, (dev, batch) in enumerate((("cuda", 1), ("cuda", 32), ("cpu", 1), ("cpu", 32))):
    b("tab_efficiency", 0, "§header", 2 + 2 * k, A_LAT,
      f"speedups[device={dev}][batch={batch}][dtype=fp32].speedup", "2dp",
      ident=f"tab_efficiency.latency.{dev}_b{batch}")
    ex("tab_efficiency", 0, "§header", 1 + 2 * k, "hyperparameter",
       f"yigin boyutu b={batch} -- olcum degil")
ex("tab_efficiency", 0, "§header", 0, "dtype_name", "fp32 -- veri tipi adi, olcum degil")
EFF_CAP1 = "25.8 cheaper in multiply--accumulates but between 1.9"
b("tab_efficiency", -1, EFF_CAP1, 0, A_EFF, "compression.flops_ratio", "1dp",
  ident="tab_efficiency.caption.flops_ratio")
b("tab_efficiency", -1, EFF_CAP1, 1, A_LAT,
  "speedups[device=cuda][batch=1][dtype=fp32].speedup", "1dp",
  ident="tab_efficiency.caption.speedup_min")
b("tab_efficiency", -1, "and 4.4 faster in wall-clock time", 0, A_LAT,
  "speedups[device=cpu][batch=32][dtype=fp32].speedup", "1dp",
  ident="tab_efficiency.caption.speedup_max")
ex("tab_efficiency", -1, "and 4.4 faster in wall-clock time", 1, "benchmark_protocol",
   "olcum protokolu: yigin 32")
ex("tab_efficiency", -1, "and 4.4 faster in wall-clock time", 2, "benchmark_protocol",
   "olcum protokolu: 200 zamanlanmis yineleme")
ex("tab_efficiency", -1, "iterations after 50 warm-up on GPU", None, "benchmark_protocol",
   "olcum protokolu: isinma/yineleme sayilari")
ex("tab_efficiency", -1, "Measured on an idle machine", None, "hardware_name",
   "donanim adi (RTX 5070, Ryzen 9)")
ex("tab_efficiency", -1, "7950X 16 cores).", None, "hardware_name",
   "donanim adi ve cekirdek sayisi")

# =============================================================================
# 12 · tab_selection_audit — selection_gain + order_stat_trend
# =============================================================================
AUDIT_ROWS = [("RAF-DB best - last", "b_best_minus_last", "rafdb_best_last"),
              ("RAF-DB best - SWA", "c_best_minus_swa", "rafdb_best_swa")]
for row, key, slug in AUDIT_ROWS:
    for k, (field, sub, rnd) in enumerate([("d_acc", "mean", "2dp"), ("d_acc", "sd", "2dp"),
                                           ("d_ece", "mean", "4dp"), ("d_ece", "sd", "4dp")]):
        b("tab_selection_audit", -1, row, k, A_SG,
          f"audit_deltas.{key}.{field}.{sub}", rnd,
          ident=f"tab_selection_audit.{slug}.{field}_{sub}")
    b("tab_selection_audit", -1, row, 4, A_SG, f"audit_deltas.{key}.n", "int",
      ident=f"tab_selection_audit.{slug}.n")
# FERPlus satirlari (N14, 17 Agu): `selection_gain.audit_deltas` yalniz RAF-DB kirilimi tasiyor,
# ama ayni ESTIMAND FERPlus icin de uretilmis -- `selection_audit_inference` dort kontrastin
# hepsini ayni CSV'lerden ve ayni tanimla hesapliyor. YENI URETICI YAZILMADI: ikinci bir tanim
# getirmek yerine var olan alan baglandi. Iki artefaktin ORTUSEN sekiz RAF-DB degeri birebir
# ayni (bit duzeyinde dogrulandi, 17 Agu), yani bolunme bir tanim ayrismasi degil.
for row, con, slug in (("FERPlus best - last", "best-last", "ferplus_best_last"),
                       ("FERPlus best - SWA", "best-swa", "ferplus_best_swa")):
    sel = f'datasets["FERPlus"].contrasts["{con}"]'
    for k, (path, rnd) in enumerate(((f"{sel}.acc_pp.mean", "2dp"), (f"{sel}.acc_pp.sd", "2dp"),
                                     (f"{sel}.ece.mean", "4dp"), (f"{sel}.ece.sd", "4dp"),
                                     (f"{sel}.acc_pp.n", "int"))):
        b("tab_selection_audit", -1, row, k, A_SAI, path, rnd,
          ident=f"tab_selection_audit.{slug}." + ["d_acc_mean", "d_acc_sd", "d_ece_mean",
                                                  "d_ece_sd", "n"][k])
# Sira-istatistigi satirlari: 17 Agu'da makale tarafinda ACIKCA RAF-DB etiketi verildi (once
# birinci sutun bostu ve satir ustteki FERPlus etiketini miras aliyordu). Bag da o gun guncellendi
# -- eski etiketle duran beyan `binding_matched_nothing` veriyordu, yani denetci degisikligi gordu.
for k, K in enumerate(("50", "100")):
    b("tab_selection_audit", 0, f"RAF-DB K = {K}", 0, A_OST,
      f'results["{K}"].a2_raw.mean', "3dp", ident=f"tab_selection_audit.order_stat.K{K}.mean")
    b("tab_selection_audit", 0, f"RAF-DB K = {K}", 1, A_OST,
      f'results["{K}"].a2_raw.sd', "3dp", ident=f"tab_selection_audit.order_stat.K{K}.sd")
    b("tab_selection_audit", 0, f"RAF-DB K = {K}", 2, A_OST,
      f'results["{K}"].n_runs', "int", ident=f"tab_selection_audit.order_stat.K{K}.n")


MDE_CAP1 = "0.0024 (Stage1 eff.) to 0.0067 (Primary none)"
b("app_mde", -1, MDE_CAP1, 0, A_CSM, "mde_ece_swa_min", "4dp", ident="app_mde.cap.swa_min")
b("app_mde", -1, MDE_CAP1, 2, A_CSM, "mde_ece_swa_max", "4dp", ident="app_mde.cap.swa_max")
ex("app_mde", -1, MDE_CAP1, 1, "teacher_name_digits", "Stage1 adinin icindeki basamak")
MDE_CAP2 = "in absolute ECE and 3.2 % to 19.4 % (VAE9182 none) as a"
b("app_mde", -1, MDE_CAP2, 0, A_CSM, "mde_ece_swa_pct_min", "1dp",
  ident="app_mde.cap.swa_pct_min")
b("app_mde", -1, MDE_CAP2, 1, A_CSM, "mde_ece_swa_pct_max", "1dp",
  ident="app_mde.cap.swa_pct_max")
ex("app_mde", -1, MDE_CAP2, 2, "teacher_name_digits", "VAE9182 adinin icindeki basamak")
ex("app_mde", -1, "from the rounded columns can differ by 0.1 point.", None, "rounding_caveat",
   "yuvarlama uyarisinin kendisi (0.1 puan) -- olcum degil")

# --- app_predecl (S11): on-kayit provenans metadatasi. OLCUM DEGIL ve yapilandirilmis
# artefakti YOK (preregistration_blocks.csv yalniz kosu->blok eslemesi tasiyor, lead suresi
# tasimiyor). Bu turda beyanla kapsam disi; acik kalem olarak raporda yazildi.
for _r in ("Control teacher flat response", "Miscalibration pilot kill-switch",
           "Second-dataset replication", "Human-alignment arm",
           "Logit standardisation three seeds", "Oracle-gate extension", "T factorial",
           "Initialisation-matched capacity arm", "Learned-signal gate three seeds",
           "Student-scaling joint frontier", "Capacity sweep",
           "Oracle-gate diagnostic (original)", "Student-head isolation",
           "Control completion (two teachers)", "Over-confident dose--response"):
    for _s in (0, 1, 2, 3):
        ex("app_predecl", _s, _r, None, "preregistration_provenance",
           "on-beyan lead suresi / ongoru sayisi / bolum atfi -- olcum degil, saglama "
           "PREREGISTRATIONS.md + git zaman damgasi", opt=True)

# --- tab_collapse caption muafiyetleri ve olcut sabiti
ex("tab_collapse", -1, "Pre-declared factorial on the Stage1 teacher", None,
   "teacher_name_digits", "Stage1 adinin icindeki basamak")
ex("tab_collapse", -1, "order of magnitude above the pre-declared threshold", None,
   "criterion_constant", "olcut: 2x kontrol sd'si (esik tanimi)")
ex("tab_collapse", -1, "ECE(T = 1) - ECE(T = 1.34) within seed", None, "hyperparameter",
   "gap(alpha) tanimindaki sicakliklar T=1 ve T=1.34")
ex("tab_collapse", -1, "= 0.5 and reverses sign by = 0.9", None, "hyperparameter",
   "sert etiket agirligi alpha degerleri")

# =============================================================================
# 13 · abstract — manset sayilar
# =============================================================================
b("abstract", -1, "pooled Spearman = 0.79 ) while accuracy stays within", 0, A_TDO,
  "pooled_stats.swa.spearman_abs_signed_gap", "2dp", ident="abstract.pooled_rho")
b("abstract", -1, "stochastic-weight-averaging checkpoints because a 13", 0, A_SG,
  "audit_deltas.b_best_minus_last.n", "int", ident="abstract.audit_n_runs")
b("abstract", -1, "best-validation-accuracy selection inflates accuracy", 0, A_SG,
  "audit_deltas.b_best_minus_last.d_acc.mean", "2dp", ident="abstract.selection_inflation")
# Asimetri araligi: iki UC, ikisi de alan. Ozetin "1.8--2.0x"i, ARA DEGERLENDIRME yapilmamis
# (extrapole edilmemis) iki karsilastirmanin min/max'i -- artefaktin kendi ozet blogu.
b("abstract", -1, "over-confidence costs 1.8", 0, A_ASY,
  "summary.interpolated_only.absolute.min", "1dp", ident="abstract.asymmetry_min")
b("abstract", -1, "over-confidence costs 1.8", 1, A_ASY,
  "summary.interpolated_only.absolute.max", "1dp", ident="abstract.asymmetry_max")
b("abstract", -1, "standardisation harms calibration at a media", 0, A_NU, "summary.median",
  "int", ident="abstract.logitstd_noise_median")


# --- olcum olmayan kalan jetonlar (beyan)
ex("tab_holm", -1, "at n = 3 ( df = 2 )", None, "sample_size",
   "n=3 ve df=2 -- tasarim sayisi, olcum degil")
ex("tab_holm", -1, "The family was fixed on 1 August 2026", None, "date",
   "aile sabitleme tarihi (1 Agustos 2026)")
ex("tab_human", -1, "n = 3 ). Students are scored", None, "sample_size", "n=3")
ex("tab_mechanisms", 0, "those ratios are in Supplementary Table", None, "table_reference",
   "Supplementary Table S8 atfi")

# =============================================================================
# TURETILMIS NICELIKLER (derived_registry)
# =============================================================================
def op(artifact, path):
    return {"artifact": artifact, "path": path}


pv("methodology.entropy_pearson_T1", "ferplus_jsd/ferplus_jsd.json",
   "entropy_correlation.T1.pearson", "3dp", "sections/03_methodology.tex#per-sample entropy correlation is",
   note="'per-sample entropy correlation is r=0.724 at T=1' -- bag T=1 KOLUNA kurulu; dis "
        "inceleme bu sayinin yanlis kola atfedildigini bildirmisti")
dv("jsd_collapse", "37", "ratio",
   [op(A_R3W, 'arms["0.26"].jsd_arm[0] - arms["0.74"].jsd_arm[0]'),
    op(A_R3W, 'arms["0.74"].jsd_ts[0] - arms["0.26"].jsd_ts[0]')],
   "int", None, None, None, None,
   where="sections/05_results_discussion.tex#collapse onto a common value",
   note="'collapse onto a common value' cumlesi; N12'de olculdu")
dv("jsd_noise_ratio", "40", "ratio",
   [op(A_JCA, "numerator.value"), op(A_JCA, "R_noise.seed_sd_by_convention[\"mean sd\"]")],
   "int", None, None, None, None,
   where="sections/05_results_discussion.tex#times the noise",
   note="ayni alt bolumun govdesi: 'roughly forty times the noise'")
dv("capacity_vs_teacher_lever", "76", "ratio",
   [op(A_RT, "T10_axis_spans.swa.teacher_span"),
    op(A_RT, "T10_axis_spans.swa.capacity_span")],
   "int", "tab_capacity", -1, CAP_FOOT, 3,
   note="tab_capacity dipnotu: 'a factor of 76'")
dv("selection_cost_best", "0.52", "diff",
   [op(A_P4, "recipe_step3_ranking.rows[teacher=vae9182].student_by_ckpt.best.acc_mean"),
    op(A_P4, "recipe_step3_ranking.rows[teacher=stage1].student_by_ckpt.best.acc_mean")],
   "2dp", "tab_selection", -1, SEL_FOOT, 2)
dv("selection_cost_swa", "0.35", "diff",
   [op(A_P4, "recipe_step3_ranking.rows[teacher=vae9182].student_by_ckpt.swa.acc_mean"),
    op(A_P4, "recipe_step3_ranking.rows[teacher=stage1].student_by_ckpt.swa.acc_mean")],
   "2dp", "tab_selection", -1,
   "( 89.60 pp each) and the cost of the accuracy rule i", 1)
dv("selection_cost_last", "0.83", "diff",
   [op(A_P4, "recipe_step3_ranking.rows[teacher=vae9182].student_by_ckpt.last.acc_mean"),
    op(A_P4, "recipe_step3_ranking.rows[teacher=stage1].student_by_ckpt.last.acc_mean")],
   "2dp", "tab_selection", -1,
   "there 0.52 pp here and 0.83 pp at the last checkpoint.", 1)
dv("human_trade_ece", "+0.0159", "diff",
   [op(A_FSJ, 'by_checkpoint.swa["0.74"].ece[0]'),
    op(A_FSJ, 'by_checkpoint.swa["0.5063"].ece[0]')],
   "4dp", "tab_human", -1, HUM_FOOT, 1)
dv("human_trade_jsd", "-0.0051", "diff",
   [op(A_FSJ, 'by_checkpoint.swa["0.74"].jsd[0]'),
    op(A_FSJ, 'by_checkpoint.swa["0.5063"].jsd[0]')],
   "4dp", "tab_human", -1, HUM_FOOT, 2)
dv("collapse_ratio_5_10", "16.3", "ratio",
   [op(A_RT, 'T11_collapse.pairs["T·τ = 5.10"].mean'), op(A_RT, "T11_collapse.two_bar")],
   "1dp", "tab_collapse", 0, "T = 5.10", 4, note="|ort|/esik; isaret disi")
dv("collapse_ratio_10_20", "13.5", "ratio",
   [op(A_RT, 'T11_collapse.pairs["T·τ = 10.20"].mean'), op(A_RT, "T11_collapse.two_bar")],
   "1dp", "tab_collapse", 0, "T = 10.20", 4, note="|ort|/esik; isaret disi")

# --- N14 (17 Agu 2026): kayitsiz kalan turetilmis nicelikler
dv("selection_cost_best_caption", "0.52", "diff",
   [op(A_P4, "recipe_step3_ranking.rows[teacher=vae9182].student_by_ckpt.best.acc_mean"),
    op(A_P4, "recipe_step3_ranking.rows[teacher=stage1].student_by_ckpt.best.acc_mean")],
   "2dp", "tab_selection", -1, "there 0.52 pp here and 0.83 pp at the last c", 0,
   note="AYNI nicelik, ikinci gecis: alt yazi. Dipnottaki `selection_cost_best` ile ayni "
        "pay/payda; iki yerde basildigi icin iki kez kaydediliyor")
# Ozetin ECE azalmasi araligi: iki UC, ikisi de 'duzeltilmemis kol T=1' -> 'duzeltilmis kol T*'
# yuzde dususu. AYRI AYRI kaydedildi, cunku bir aralik tek bir olcum degil iki olcumdur.
dv("ece_reduction_min", "41", "pct_drop",
   [op(A_TDO, "arms.rafdb_stage1.points[1].by_ckpt.swa.ece_mean"),
    op(A_TDO, "arms.rafdb_stage1.points[2].by_ckpt.swa.ece_mean")],
   "int", "abstract", -1, "41 -- 76 % at no accuracy cost", 0,
   note="Stage1: T=1 -> T=1.3406 (dagitilan kol), @SWA ogrenci ECE'si")
dv("ece_reduction_max", "76", "pct_drop",
   [op(A_TDO, "arms.ferplus.points[3].by_ckpt.swa.ece_mean"),
    op(A_TDO, "arms.ferplus.points[1].by_ckpt.swa.ece_mean")],
   "int", "abstract", -1, "41 -- 76 % at no accuracy cost", 1,
   note="FERPlus: T=1 -> T=0.5063 (dagitilan kol), @SWA ogrenci ECE'si")
# Ozetin "accuracy stays within 0.51 pp"i: KOL ICI dogruluk acikligi, uc kolun EN GENISI.
# §3.6 ayni niceligi iki RAF-DB kolu icin veriyor (0.30 ve 0.51), yani estimand adlandirilmis.
dv("accuracy_band_widest_arm", "0.51", "diff",
   [op(A_TDO, "arms.rafdb_vae9182.points[2].by_ckpt.swa.acc_mean"),
    op(A_TDO, "arms.rafdb_vae9182.points[3].by_ckpt.swa.acc_mean")],
   "2dp", "abstract", -1, "pooled Spearman = 0.79 ) while accuracy stays within", 1,
   note="VAE9182 kolunun en yuksek (T=1.3406) ve en dusuk (T=1.70) @SWA dogrulugu; olculen kol "
        "aciklikleri 0.304 / 0.511 / 0.486, ozet en genisi basiyor")
# §3.2, DUZYAZI -- kapsam disi metinden TEK TEK beyanla iceri alinan iki uc. Fatih'in 17 Agu
# kurali: turetilmis nicelik asla basili yuvarlak degerden hesaplanmaz. Bu iki sayi 14 Agu'da
# tam o hatayla (0.0015/0.0220) yeniden uretilmisti; artik pay ve payda alan yolu.
dv("tstar_criterion_cost_min", "13", "ratio",
   [op(A_TSS, "results.ferplus.ece_removed_by_ts"), op(A_TSS, "results.ferplus.d_ece")],
   "int", None, None, None, None,
   where="sections/03_methodology.tex#times smaller than the ECE the scaling removes",
   note="FERPlus 13.31x -- uc ogretmenin en dusugu (primary 13.60, stage1 14.32)")
dv("tstar_criterion_cost_max", "14", "ratio",
   [op(A_TSS, "results.stage1.ece_removed_by_ts"), op(A_TSS, "results.stage1.d_ece")],
   "int", None, None, None, None,
   where="sections/03_methodology.tex#times smaller than the ECE the scaling removes",
   note="Stage1 14.32x -- uc ogretmenin en yuksegi; vae9182 disarida cunku TS orada ECE EKLIYOR")

# =============================================================================
# COZUMLEYICI + YUVARLAMA
# =============================================================================
class Unresolved(Exception):
    pass


def _seg(path):
    """Yol ayristirici: `a.b[0].c`, `a["0.1"].b`, `rows[k=v][k2=v2].f`."""
    out, i, n = [], 0, len(path)
    buf = ""
    while i < n:
        c = path[i]
        if c == ".":
            if buf:
                out.append(("key", buf))
                buf = ""
            i += 1
        elif c == "[":
            if buf:
                out.append(("key", buf))
                buf = ""
            j = path.index("]", i)
            inner = path[i + 1:j]
            if inner.startswith('"') and inner.endswith('"'):
                out.append(("key", inner[1:-1]))
            elif "=" in inner:
                k, v = inner.split("=", 1)
                out.append(("sel", (k, v)))
            else:
                out.append(("idx", int(inner)))
            i = j + 1
        else:
            buf += c
            i += 1
    if buf:
        out.append(("key", buf))
    return out


def resolve(store, artifact, path):
    """Artefakt alanini coz. `a - b` bicimi iki alanin farkidir (turetilmis pay/payda)."""
    if " - " in path:
        a, bb = path.split(" - ", 1)
        return resolve(store, artifact, a.strip()) - resolve(store, artifact, bb.strip())
    if artifact not in store:
        p = D / artifact
        if not p.exists():
            raise Unresolved(f"artefakt yok: {artifact}")
        store[artifact] = json.loads(p.read_text(encoding="utf-8"))
    cur = store[artifact]
    for kind, val in _seg(path):
        # Zincirli seciciler SUZER (tek satira indirmez): `rows[a=x][b=y][c=z]` uc kosulu
        # birlikte uygular. Bir alan erisimi geldiginde liste tek elemanliysa acilir; degilse
        # beyan belirsizdir ve DURUR -- "ilkini al" sessiz bir yanlis bag uretirdi.
        if kind == "key" and isinstance(cur, list):
            if len(cur) != 1:
                raise Unresolved(f"{path}: alan erisimi {len(cur)} satirda belirsiz")
            cur = cur[0]
        try:
            if kind == "key":
                cur = cur[val]
            elif kind == "idx":
                cur = cur[val]
            else:
                k, v = val
                if isinstance(cur, dict):
                    cur = [dict(x, **{"__key": kk}) for kk, x in cur.items()]
                if k == "rank":
                    cur = [cur[int(v)]]
                else:
                    cur = [x for x in cur if str(x.get(k, x.get("__key"))) == v]
                if not cur:
                    raise Unresolved(f"secici {k}={v} hicbir satir sectmedi")
        except Unresolved:
            raise
        except Exception as e:
            raise Unresolved(f"{path}: {type(e).__name__} ({kind} {val})")
    if isinstance(cur, list) and len(cur) == 1:
        cur = cur[0]
    if isinstance(cur, bool) or not isinstance(cur, (int, float)):
        raise Unresolved(f"{path}: sayi degil ({type(cur).__name__})")
    return float(cur)


def fmt_round(value, rounding):
    """Beyan edilen yuvarlama. YARIYI YUKARI (LaTeX'te elle yazilan sayi boyle yuvarlanir)."""
    if rounding == "int":
        q = Decimal(1)
    else:
        nd = int(rounding.replace("dp", ""))
        q = Decimal(1).scaleb(-nd)
    return Decimal(repr(float(value))).quantize(q, rounding=ROUND_HALF_UP)


def printed_dec(s):
    return Decimal(s.replace("+", ""))


# =============================================================================
# ESLEME + ANA AKIS
# =============================================================================
def norm(s):
    return " ".join(str(s).split()).lower()


def match_tokens(toks, unit, section, row, idx):
    """Bir beyanin (unit, section, row-oneki, idx) esledigi jetonlar.

    Satir ONEKLE eslesir: dipnot/caption satirlarinin etiketi satirin tamamidir ve beyanda
    tamamini yazmak hem okunmaz hem kirilgan olurdu. Onek birden fazla jetona eslesirse bu bir
    HATADIR (belirsiz beyan) ve raporlanir -- sessizce ilki alinmaz.
    """
    r = norm(row)
    return [t for t in toks
            if t["unit"] == unit and t["section"] == section
            and (idx is None or t["idx"] == idx)
            and norm(t["row"]).startswith(r)]


def line_numbers(paper_root, where):
    """`sections/x.tex#capa cumlesi` -> capanin gectigi satir ve KOMSULARINDAKI sayi jetonlari.

    SATIR NUMARASINA CAPA ATILMAZ: bu betik ilk yazildiginda `:693` kullaniliyordu ve makale
    ayni gun duzenlenince capa kaydi (cumle 693-694'e yayildi). Capa artik cumlenin KENDI
    metni; pencere +-1 satir, cunku LaTeX cumleleri satir sonunda kirilir.
    """
    rel, anchor = where.split("#", 1)
    fp = Path(paper_root) / rel
    if not fp.exists():
        raise Unresolved(f"duzyazi dosyasi yok: {rel}")
    lines = fp.read_text(encoding="utf-8", errors="replace").splitlines()
    hits = [i for i, ln in enumerate(lines) if anchor in ln]
    if len(hits) != 1:
        raise Unresolved(f"{where}: capa {len(hits)} satirda gecti (tam 1 olmali)")
    i = hits[0]
    from paper_number_scan import COMMENT, NUM, strip_layout
    win = " ".join(lines[max(0, i - 1):i + 2])
    cleaned, _ = strip_layout(COMMENT.sub("", win))
    return NUM.findall(cleaned), f"{rel}:{i + 1}"


def build(paper_root):
    """(payload, derived_entries) -- defterin tamami. check_numbers de bunu cagirir."""
    toks, dropped, files, secs = scan_paper(paper_root)
    store = {}
    entries, problems = [], []

    exempt_keys, exempt_rows = set(), []
    for e in EXEMPT:
        hit = match_tokens(toks, e["unit"], e["section"], e["row"], e["idx"])
        if not hit and not e.get("optional"):
            problems.append({"kind": "exempt_matched_nothing", "id": e["class"],
                             "detail": f"{e['unit']} {e['row'][:40]!r}"})
        for t in hit:
            exempt_keys.add(t["key"])
            exempt_rows.append({"key": t["key"], "class": e["class"], "why": e["why"],
                                "printed": t["printed"]})

    bound_keys = {}
    for bd in BINDINGS:
        hit = match_tokens(toks, bd["unit"], bd["section"], bd["row"], bd["idx"])
        if len(hit) != 1:
            problems.append({"kind": "binding_matched_nothing" if not hit else "ambiguous",
                             "id": bd["id"], "detail": f"{len(hit)} jeton · "
                                                       f"{bd['unit']} {bd['row'][:40]!r} "
                                                       f"idx={bd['idx']}"})
            continue
        t = hit[0]
        if t["key"] in bound_keys:
            problems.append({"kind": "double_bound", "id": bd["id"], "detail": t["key"]})
            continue
        try:
            exact = resolve(store, bd["artifact"], bd["path"])
        except Unresolved as e:
            problems.append({"kind": "unresolved_path", "id": bd["id"], "detail": str(e)})
            continue
        rounded = fmt_round(exact, bd["rounding"])
        pr = printed_dec(t["printed"])
        ok = rounded == pr
        bound_keys[t["key"]] = bd["id"]
        entries.append({"id": bd["id"], "printed": t["printed"], "artifact": bd["artifact"],
                        "path": bd["path"], "exact": exact, "rounding": bd["rounding"],
                        "rounded": str(rounded), "matches": ok,
                        "where": [f"paper/{t['file']}:{t['line']}"],
                        "token": t["key"], "row": t["row"], "idx": t["idx"]})
        if not ok:
            problems.append({"kind": "rounding_mismatch", "id": bd["id"],
                             "detail": f"basili {t['printed']} vs alan {exact!r} -> "
                                       f"{bd['rounding']} {rounded}"})

    dentries = []
    for d in DERIVED:
        try:
            vals = [resolve(store, o["artifact"], o["path"]) for o in d["operands"]]
        except Unresolved as e:
            problems.append({"kind": "unresolved_path", "id": d["id"], "detail": str(e)})
            continue
        if d["formula"] == "ratio":
            val = abs(vals[0]) / abs(vals[1])
        elif d["formula"] == "diff":
            val = vals[0] - vals[1]
        elif d["formula"] == "pct_drop":
            # yuzde AZALMA: (taban - duzeltilmis) / taban x 100. Payda ACIKCA TABAN -- bir oranin
            # paydasi cumlede adlandirilmali (17 Agu kurali), burada da alan yolu olarak duruyor.
            val = 100.0 * (vals[0] - vals[1]) / vals[0]
        else:
            problems.append({"kind": "unknown_formula", "id": d["id"], "detail": d["formula"]})
            continue
        rounded = fmt_round(val, d["rounding"])
        tok = None
        # YETKILI DEGER MAKALENIN KENDISI. Bir jetona baglanmis turetilmis nicelikte
        # karsilastirma, koda yazilmis `printed` ile degil MAKALEDE BASILI degerle yapilir --
        # aksi halde makale duzenlenince denetci sessiz kalirdi (kendi ozsinamasinda olctuk).
        if d["unit"]:
            hit = match_tokens(toks, d["unit"], d["section"], d["row"], d["idx"])
            if len(hit) == 1:
                tok = hit[0]
                bound_keys[tok["key"]] = d["id"]
            else:
                problems.append({"kind": "derived_matched_nothing", "id": d["id"],
                                 "detail": f"{len(hit)} jeton · {d['unit']} "
                                           f"{str(d['row'])[:40]!r} idx={d['idx']}"})
        pr = printed_dec(tok["printed"] if tok else d["printed"])
        ok = rounded == pr
        if tok and printed_dec(d["printed"]) != pr:
            problems.append({"kind": "derived_printed_drift", "id": d["id"],
                             "detail": f"defter {d['printed']} vs makale {tok['printed']}"})
        dentries.append({"id": d["id"], "printed": d["printed"], "formula": d["formula"],
                         "operands": d["operands"], "operand_values": vals,
                         "exact": val, "rounding": d["rounding"], "rounded": str(rounded),
                         "matches": ok, "note": d["note"],
                         "where": [f"paper/{tok['file']}:{tok['line']}"] if tok else []})
        if not ok:
            problems.append({"kind": "derived_mismatch", "id": d["id"],
                             "detail": f"basili {pr} vs yeniden hesap {val!r} -> {rounded}"})
        if d.get("where_literal"):
            try:
                nums, _loc = line_numbers(paper_root, d["where_literal"])
                word = SPELLED.get(str(rounded))
                spelled_ok = bool(word) and word in open(
                    Path(paper_root) / d["where_literal"].split("#")[0],
                    encoding="utf-8", errors="replace").read()
                if str(rounded) not in [x.lstrip("+") for x in nums] and not spelled_ok:
                    problems.append({"kind": "printed_not_found_at_location", "id": d["id"],
                                     "detail": f"{d['where_literal']}: {rounded} yok, "
                                               f"satirdaki sayilar {nums[:8]}"})
            except Unresolved as e:
                problems.append({"kind": "prose_location_bad", "id": d["id"],
                                 "detail": str(e)})

    pentries = []
    for pr in PROSE:
        try:
            exact = resolve(store, pr["artifact"], pr["path"])
        except Unresolved as e:
            problems.append({"kind": "unresolved_path", "id": pr["id"], "detail": str(e)})
            continue
        rounded = fmt_round(exact, pr["rounding"])
        row = {"id": pr["id"], "artifact": pr["artifact"], "path": pr["path"],
               "exact": exact, "rounding": pr["rounding"], "rounded": str(rounded),
               "where": [f"paper/{pr['where']}"], "note": pr["note"], "matches": None}
        try:
            nums, loc = line_numbers(paper_root, pr["where"])
            row["line_numbers"] = nums
            row["where"] = [f"paper/{loc}"]
            row["matches"] = str(rounded) in [x.lstrip("+") for x in nums]
            if not row["matches"]:
                problems.append({"kind": "printed_not_found_at_location", "id": pr["id"],
                                 "detail": f"{pr['where']}: {rounded} yok, satirdaki sayilar "
                                           f"{nums[:8]}"})
        except Unresolved as e:
            problems.append({"kind": "prose_location_bad", "id": pr["id"], "detail": str(e)})
        pentries.append(row)

    unbound = [t for t in toks if t["key"] not in bound_keys and t["key"] not in exempt_keys]
    payload = {
        "note": "review-responsive, not pre-declared",
        "scope": {"in": ["paper/tables/*.tex", "abstract", "supplementary S8-S11",
                         "individually anchored prose sentences (declared one by one)"],
                  "out": ["sections/*.tex prose, except the individually anchored sentences "
                          "(revision window)",
                          "supplementary S1-S3 (today's headroom verdict not applied yet)"],
                  "not_a_measurement": sorted({e["class"] for e in EXEMPT})},
        "paper_files": files, "sections": secs,
        "counts": {"tokens": len(toks), "bound": len(entries), "derived": len(dentries),
                   "exempt": len(exempt_keys), "unbound": len(unbound),
                   "layout_dropped": len(dropped),
                   "mismatch": sum(1 for e in entries if not e["matches"]),
                   "derived_mismatch": sum(1 for e in dentries if not e["matches"]),
                   "prose": len(pentries),
                   "problems": len(problems)},
        "entries": entries, "exempt": exempt_rows, "prose_entries": pentries,
        "unbound": [{"key": t["key"], "printed": t["printed"], "unit": t["unit"],
                     "row": t["row"], "idx": t["idx"],
                     "where": f"paper/{t['file']}:{t['line']}"} for t in unbound],
        "problems": problems,
        "dropped_layout_classes": sorted({d["class"] for d in dropped}),
    }
    return payload, dentries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-root", default=os.environ.get("VELD_PAPER_ROOT"))
    args, _unknown = ap.parse_known_args()
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")

    if not args.paper_root or not Path(args.paper_root).exists():
        print("kagit agaci verilmedi (--paper-root / VELD_PAPER_ROOT): mevcut defter KORUNDU, "
              "hicbir dosya yazilmadi.")
        return 0

    payload, dentries = build(args.paper_root)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "number_ledger.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT_DIR / "derived_registry.json").write_text(json.dumps(
        {"note": payload["note"],
         "counts": {"derived": len(dentries),
                    "mismatch": sum(1 for e in dentries if not e["matches"])},
         "entries": dentries}, indent=2, ensure_ascii=False), encoding="utf-8")
    write_md(payload, dentries)

    c = payload["counts"]
    print(f"jeton {c['tokens']} · bagli {c['bound']} · turetilmis {c['derived']} · "
          f"muaf {c['exempt']} · KAYITSIZ {c['unbound']} · uyusmazlik {c['mismatch']} · "
          f"sorun {c['problems']}")
    for p in payload["problems"][:45]:
        print(("  ! " + p["kind"].ljust(26) + " " + str(p.get("id", "")) + " " +
               str(p.get("detail", "")))[:158])
    if len(payload["problems"]) > 45:
        print(f"  ... +{len(payload['problems']) - 45} sorun")
    return 0


def write_md(payload, dentries):
    c = payload["counts"]
    L = ["# N13 — Number provenance ledger", "",
         "> **Review-responsive, not pre-declared (17 Aug 2026).** The ledger records the "
         "value-to-FIELD binding, not the value: a stale number exists somewhere too, so "
         "existence proves nothing.", "",
         "Producer: `diagnostics/number_ledger.py` · scanner: `diagnostics/paper_number_scan.py`"
         " · auditor: `diagnostics/check_numbers.py`", "",
         "| | count |", "|---|---|",
         f"| numeric tokens in scope | {c['tokens']} |",
         f"| bound to an artifact field | {c['bound']} |",
         f"| derived (ratio / difference) | {c['derived']} |",
         f"| declared not-a-measurement | {c['exempt']} |",
         f"| **unregistered** | **{c['unbound']}** |",
         f"| printed-vs-field mismatch | {c['mismatch']} |",
         f"| layout tokens dropped by the scanner | {c['layout_dropped']} |", "",
         "## Scope (declared)", "",
         "**In:** " + ", ".join("`" + x + "`" for x in payload["scope"]["in"]) + "  ",
         "**Out:** " + " · ".join(payload["scope"]["out"]) + "  ",
         "**Not a measurement:** "
         + ", ".join("`" + x + "`" for x in payload["scope"]["not_a_measurement"]),
         "", "## Unregistered numbers", ""]
    if payload["unbound"]:
        L += ["| printed | unit | row | where |", "|---|---|---|---|"]
        for u in payload["unbound"]:
            L.append(f"| `{u['printed']}` | {u['unit']} | {u['row'][:46]} | {u['where']} |")
    else:
        L.append("None — every in-scope number is bound, derived or declared.")
    L += ["", "## Mismatches", ""]
    bad = [e for e in payload["entries"] if not e["matches"]]
    if bad:
        L += ["| id | printed | field value | rounded | where |", "|---|---|---|---|---|"]
        for e in bad:
            L.append(f"| `{e['id']}` | {e['printed']} | {e['exact']:.6g} | {e['rounded']} | "
                     f"{e['where'][0]} |")
    else:
        L.append("None.")
    L += ["", "## Derived quantities", "",
          "| id | printed | formula | recomputed | ok |", "|---|---|---|---|---|"]
    for e in dentries:
        L.append(f"| `{e['id']}` | {e['printed']} | {e['formula']} | {e['exact']:.6g} | "
                 f"{'yes' if e['matches'] else '**NO**'} |")
    L += ["", "## Bindings", "",
          "| id | printed | artifact | path | rounding |", "|---|---|---|---|---|"]
    for e in payload["entries"]:
        L.append(f"| `{e['id']}` | {e['printed']} | `{e['artifact']}` | `{e['path']}` | "
                 f"{e['rounding']} |")
    (OUT_DIR / "number_ledger.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    dl = ["# N13 — Derived quantity registry", "",
          "Every printed ratio or difference, with its numerator and denominator as artifact "
          "field paths, so it can be recomputed from the ledger instead of from printed values. "
          "Two of today's three errors came from dividing rounded printed cells.", "",
          "| id | printed | formula | operands | recomputed | ok |",
          "|---|---|---|---|---|---|"]
    for e in dentries:
        ops = " ÷ ".join("`" + o["artifact"] + "` → `" + o["path"] + "`"
                         for o in e["operands"])
        dl.append(f"| `{e['id']}` | {e['printed']} | {e['formula']} | {ops} | "
                  f"{e['exact']:.6g} | {'yes' if e['matches'] else '**NO**'} |")
    (OUT_DIR / "derived_registry.md").write_text("\n".join(dl) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
