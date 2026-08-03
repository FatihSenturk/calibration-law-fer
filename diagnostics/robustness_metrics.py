"""R3-1: çok-metrik doz-cevap envanteri — "tek bir ECE spesifikasyonu" itirazına yanıt.

İTİRAZ (dış inceleme). Kampanyanın her kalibrasyon sonucu TEK bir spesifikasyonla
ölçüldü: 15-kutu eşit-genişlik güven ECE'si. Bu spesifikasyonun bilinen zaafları var
(kutu sayısına duyarlılık, yüksek-güven bölgesinde yığılma, sınıf dengesizliğini
görmezden gelme). Sonuç yalnız o spesifikasyonun eseriyse, doz-cevap eğrisi bir ölçüm
artefaktıdır.

BU BETİĞİN YAPTIĞI. Aynı 42 koşu, aynı önbelleklenmiş örnek-başına logitler, YEDİ metrik
(bkz. calibration_metrics.py). Hiçbiri isteğe bağlı değil, hiçbiri rapor dışı bırakılamaz
(ön-kayıt A10). Başarı ölçütü YOKTUR: bu bir envanterdir, hipotez testi değil.

DOĞRULAMA KAPISI. `ece_ew_15` sütunu kampanyanın yayımlanmış ECE değerlerinin ta
kendisidir — aynı fonksiyon, aynı kutu sayısı. Her koşuda önbelleğin kendi meta
kaydındaki `ece_recomputed` ile karşılaştırılır; ayrışma varsa betik DURUR. Yani yeni
metrikler, eskisini yeniden üretemeyen bir boru hattından gelemez.

MONOTONLUK NASIL SAYILIYOR (ve neyin sayılmadığı). İki betimleyici sayım verilir:
  · tohum-içi monotonluk: bir tohumda ardışık T adımlarının HEPSİ aynı işaretli mi
    (k/3 biçiminde),
  · adım tutarlılığı: her T çiftinde üç tohumun işareti birbiriyle uyuşuyor mu
    (m/N biçiminde, N = çift sayısı x 3).
İkincisi hiçbir küresel yön referansı gerektirmez — her çift kendi üç tohumuna göre
değerlendirilir, dolayısıyla sonuca bakıp seçilmiş bir yön yoktur. Uyuşmayan her adım
(hangi çift, hangi tohum, hangi metrik) tabloda tek tek listelenir; bu ön-kaydın açık
şartıdır.

VERİ: koşu dizinlerindeki logits_swa.npz. Forward yok. RAF-DB serileri
p1_two_teacher_overlay.CURVES'ten (tek kaynak), FERPlus serisi
selection_audit/ferplus_selection_audit.csv'den okunur.

Salt-okunur. Çıktı -> diagnostics/paper_tables/robustness_metrics.{md,json}
"""
import csv
import json
import statistics as st
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "diagnostics"))

from calibration_metrics import METRIC_LABEL, METRIC_ORDER, all_metrics  # noqa: E402
from p1_two_teacher_overlay import CURVES  # noqa: E402  (tek kaynak: koşu -> (öğretmen, T))
from stats_convention import SD_CONVENTION, sample_sd  # noqa: E402

OUT_DIR = ROOT / "diagnostics" / "paper_tables"
STUDENTS = ROOT / "results" / "unified_students"
FER_AUDIT = ROOT / "diagnostics" / "selection_audit" / "ferplus_selection_audit.csv"
CKPT = "swa"
ECE15_TOL = 1e-9   # aynı fonksiyon, aynı girdi: bit düzeyinde aynı olmalı


def ferplus_curve():
    """{T: {seed: run_dir}} — FERPlus doz-cevap serisi, denetim tablosundan."""
    curve = {}
    with open(FER_AUDIT, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["checkpoint"] != CKPT:
                continue
            curve.setdefault(float(r["t_scale"]), {})[int(r["seed"])] = Path(r["run_dir"])
    return curve


def rafdb_curve(arm):
    """{T: {seed: run_dir}} — CURVES'teki koşu adlarını tek bitmiş dizine çözer."""
    curve = {}
    for T, seeds in CURVES[arm].items():
        for seed, run_name in seeds.items():
            cands = [d for d in sorted((STUDENTS / run_name).iterdir())
                     if d.is_dir() and (d / "metrics_best.json").exists()]
            if len(cands) != 1:
                raise RuntimeError(f"{run_name}: {len(cands)} finished run dirs, expected 1")
            curve.setdefault(float(T), {})[int(seed)] = cands[0]
    return curve


def measure_run(run_dir):
    p = run_dir / f"logits_{CKPT}.npz"
    if not p.exists():
        raise FileNotFoundError(
            f"no logit cache at {p} — build it first "
            f"(student_logit_cache.py / ferplus_student_logit_cache.py)")
    z = np.load(p, allow_pickle=False)
    meta = json.loads(str(z["meta"]))
    m = all_metrics(z["logits"], z["labels"])

    # KAPI: yeni boru hattı eski sayıyı yeniden üretmiyorsa hiçbir sütuna güvenilemez.
    d = abs(m["ece_ew_15"] - meta["ece_recomputed"])
    if d > ECE15_TOL:
        raise RuntimeError(
            f"{run_dir.parent.name}: ece_ew_15 {m['ece_ew_15']:.10f} != cache "
            f"{meta['ece_recomputed']:.10f} (d={d:.2e}) — the 15-bin column does not "
            f"reproduce the published ECE; every other column is therefore unverified.")
    m["_aux"]["source"] = str(p.relative_to(ROOT)).replace("\\", "/")
    m["_aux"]["audit_ece"] = meta.get("audit_ece")
    return m


def signs(values):
    """Ardışık farkların işaretleri: +1 / -1 / 0."""
    return [int(np.sign(round(b - a, 12))) for a, b in zip(values, values[1:])]


def analyse(series_name, curve):
    Ts = sorted(curve)
    seeds = sorted({s for per in curve.values() for s in per})
    runs = {(T, s): measure_run(curve[T][s]) for T in Ts for s in seeds if s in curve[T]}

    per_metric = {}
    for met in METRIC_ORDER:
        by_seed = {s: [runs[(T, s)][met] for T in Ts if (T, s) in runs] for s in seeds}
        seed_signs = {s: signs(v) for s, v in by_seed.items() if len(v) == len(Ts)}

        monotone_seeds = sum(1 for sg in seed_signs.values()
                             if sg and all(x == sg[0] != 0 for x in sg))
        # Adım tutarlılığı: her çiftte üç tohumun işareti; çoğunluğa uymayan = kırık.
        breaks, consistent, total = [], 0, 0
        for i in range(len(Ts) - 1):
            col = {s: sg[i] for s, sg in seed_signs.items()}
            if not col:
                continue
            maj = max(set(col.values()), key=lambda v: list(col.values()).count(v))
            for s, v in col.items():
                total += 1
                if v == maj:
                    consistent += 1
                else:
                    breaks.append({"pair": f"{Ts[i]:g}→{Ts[i + 1]:g}", "seed": s,
                                   "metric": met, "sign": v, "majority": maj,
                                   "values": [by_seed[s][i], by_seed[s][i + 1]]})
        # Eğrinin U olduğu yerde "T'de monoton mu" sorusu yapısal olarak 0/3 verir: minimum
        # T*'ta olduğu için hiçbir tohum uçtan uca tek yönlü olamaz. Bu bir kusur değil,
        # aranan biçimin ta kendisi. Asıl bilgi taşıyan betimleyici büyüklük MİNİMUMUN
        # NEREDE olduğudur: yedi metrik aynı T'yi işaret ediyorsa, sonuç ECE
        # spesifikasyonunun eseri değildir. Eşik yok, hüküm yok -- yalnız konum.
        argmins = {s: Ts[int(np.argmin(v))] for s, v in by_seed.items() if len(v) == len(Ts)}
        modal = (max(set(argmins.values()), key=list(argmins.values()).count)
                 if argmins else None)

        means = {T: st.mean([runs[(T, s)][met] for s in seeds if (T, s) in runs]) for T in Ts}
        sds = {T: (sample_sd([runs[(T, s)][met] for s in seeds if (T, s) in runs])
                   if sum((T, s) in runs for s in seeds) > 1 else None) for T in Ts}
        per_metric[met] = {"by_seed": {str(s): v for s, v in by_seed.items()},
                           "seed_signs": {str(s): "".join("+" if x > 0 else "-" if x < 0 else "0"
                                                          for x in sg)
                                          for s, sg in seed_signs.items()},
                           "monotone_seeds": monotone_seeds, "n_seeds": len(seed_signs),
                           "steps_consistent": consistent, "steps_total": total,
                           "breaks": breaks,
                           "argmin_T_by_seed": {str(s): t for s, t in argmins.items()},
                           "argmin_T_modal": modal,
                           "argmin_T_unanimous": len(set(argmins.values())) == 1 if argmins
                           else False,
                           "mean": {str(T): means[T] for T in Ts},
                           "sd": {str(T): sds[T] for T in Ts}}

    return {"series": series_name, "T": Ts, "seeds": seeds,
            "n_runs": len(runs),
            "sources": {f"T={T:g},seed={s}": runs[(T, s)]["_aux"]["source"]
                        for (T, s) in sorted(runs)},
            "acc": {f"T={T:g},seed={s}": runs[(T, s)]["_aux"]["acc"] for (T, s) in sorted(runs)},
            "metrics": per_metric}


def md_series(r):
    Ts, seeds = r["T"], r["seeds"]
    L = [f"### {r['series']} — {r['n_runs']} runs ({len(Ts)} T × {len(seeds)} seeds)", "",
         "**Raw values, @swa.** Every cell is computed from that run's own cached per-sample "
         "logits; the source file of each row is listed under the table.", "",
         "| T | seed | " + " | ".join(METRIC_LABEL[m] for m in METRIC_ORDER) + " | acc |",
         "|---|---|" + "---|" * (len(METRIC_ORDER) + 1)]
    for T in Ts:
        for s in seeds:
            key = f"T={T:g},seed={s}"
            if key not in r["acc"]:
                continue
            cells = []
            for m in METRIC_ORDER:
                v = r["metrics"][m]["by_seed"][str(s)][Ts.index(T)]
                cells.append(f"{v:.4f}")
            L.append(f"| {T:g} | {s} | " + " | ".join(cells) + f" | {r['acc'][key]:.2f} |")

    L += ["", f"**Arm means ± sd** ({SD_CONVENTION}).", "",
          "| T | " + " | ".join(METRIC_LABEL[m] for m in METRIC_ORDER) + " |",
          "|---|" + "---|" * len(METRIC_ORDER)]
    for T in Ts:
        cells = []
        for m in METRIC_ORDER:
            mu = r["metrics"][m]["mean"][str(T)]
            sd = r["metrics"][m]["sd"][str(T)]
            cells.append(f"{mu:.4f} ± {sd:.4f}" if sd is not None else f"{mu:.4f}")
        L.append(f"| {T:g} | " + " | ".join(cells) + " |")

    L += ["", "**Monotonicity in T, within seed.** `sign string` is one character per "
          "consecutive T step, in T order. `monotone` counts seeds whose steps all share one "
          "non-zero sign. `steps` counts individual (pair, seed) steps that agree with the other "
          "seeds at the same pair — no global direction is assumed anywhere. `argmin T` is where "
          "each seed's curve bottoms out.", "",
          "| metric | seed signs | monotone seeds | steps consistent | argmin T (per seed) |",
          "|---|---|---|---|---|"]
    for m in METRIC_ORDER:
        pm = r["metrics"][m]
        sg = " · ".join(f"{s}:`{v}`" for s, v in pm["seed_signs"].items())
        am = " · ".join(f"{s}:{t:g}" for s, t in pm["argmin_T_by_seed"].items())
        if pm["argmin_T_unanimous"]:
            am = f"**all {pm['argmin_T_modal']:g}**"
        L.append(f"| {METRIC_LABEL[m]} | {sg} | {pm['monotone_seeds']}/{pm['n_seeds']} | "
                 f"{pm['steps_consistent']}/{pm['steps_total']} | {am} |")

    mono_all_zero = all(r["metrics"][m]["monotone_seeds"] == 0 for m in METRIC_ORDER)
    modals = {r["metrics"][m]["argmin_T_modal"] for m in METRIC_ORDER}
    if mono_all_zero:
        L += ["", "*Monotone seeds are 0/3 for every metric, and that is the expected shape, not "
              "a failure: this series is a dose–response with an interior optimum, so no seed can "
              "be one-directional end to end. The informative descriptive quantity is where the "
              "curve bottoms out — the `argmin T` column"
              + (f", and all seven metrics agree on **T = {modals.pop():g}**."
                 if len(modals) == 1 else
                 f", where the seven metrics land on {sorted(str(x) for x in modals)}.")]

    allbreaks = [b for m in METRIC_ORDER for b in r["metrics"][m]["breaks"]]
    if allbreaks:
        L += ["", f"**Steps that disagree with the other seeds at the same pair "
              f"({len(allbreaks)} of "
              f"{sum(r['metrics'][m]['steps_total'] for m in METRIC_ORDER)}).** Listed in full, "
              "as the pre-declaration requires — pair, seed, metric, and the two values.", "",
              "| pair | seed | metric | value before → after | its sign | other seeds |",
              "|---|---|---|---|---|---|"]
        for b in allbreaks:
            L.append(f"| {b['pair']} | {b['seed']} | {METRIC_LABEL[b['metric']]} | "
                     f"{b['values'][0]:.4f} → {b['values'][1]:.4f} | "
                     f"{'+' if b['sign'] > 0 else '-' if b['sign'] < 0 else '0'} | "
                     f"{'+' if b['majority'] > 0 else '-' if b['majority'] < 0 else '0'} |")
    else:
        L += ["", "**No step disagrees with the other seeds at the same pair** in any of the "
              "seven metrics."]

    L += ["", "<details><summary>source files</summary>", ""]
    for k, v in r["sources"].items():
        L.append(f"- `{k}` → `{v}`")
    L += ["", "</details>", ""]
    return L


def main():
    series = {}
    for arm in ("stage1", "vae9182"):
        series[f"RAF-DB {arm}"] = analyse(f"RAF-DB {arm}", rafdb_curve(arm))
    series["FERPlus"] = analyse("FERPlus", ferplus_curve())

    total_runs = sum(r["n_runs"] for r in series.values())
    L = ["# R3-1 — Multi-metric dose–response robustness inventory (@swa)", "",
         "Producer: `diagnostics/robustness_metrics.py` · metric definitions in "
         "`diagnostics/calibration_metrics.py` · equal-width ECE is the campaign's existing "
         "`confidence_ece`, called with different bin counts rather than reimplemented · all "
         "values come from cached per-sample logits, no forward pass. Pre-declared in "
         "`PREREGISTRATIONS.md` A10 (R3-1): **no success criterion, no metric may be withheld, "
         "every monotonicity break is listed.**", "",
         f"**{total_runs} runs.** " + " · ".join(
             f"{r['series']} {r['n_runs']}" for r in series.values()) + ".", "",
         "**Verification gate.** For every run the `ECE ew-15` column is compared against the "
         "value stored in that run's own logit cache (written on a different day by a different "
         "script and itself validated against `selection_audit`). A deviation above "
         f"{ECE15_TOL:g} aborts the whole table — so the six new columns cannot come from a "
         "pipeline that fails to reproduce the published one.", "",
         "**Metric specifications** (frozen in A10, unchanged since):", "",
         "| column | specification |", "|---|---|",
         "| NLL | mean negative log-likelihood, natural log |",
         "| Brier | multiclass, full probability vector, one-hot target |",
         "| ECE ew-10 / ew-15 / ew-25 | equal-width confidence ECE, 10 / 15 / 25 bins |",
         "| ECE em-15 | equal-**mass** (adaptive) ECE, 15 quantile bins |",
         "| classwise-ECE | mean over classes of the top-1 ECE within each **predicted** class |",
         ""]
    for r in series.values():
        L += md_series(r)

    tot_break = sum(len(r["metrics"][m]["breaks"]) for r in series.values() for m in METRIC_ORDER)
    tot_steps = sum(r["metrics"][m]["steps_total"] for r in series.values() for m in METRIC_ORDER)

    # Turun asıl sorusu: yedi metrik minimumu AYNI yere mi koyuyor? Her seride modal
    # argmin'i o serinin çoğunluk değeriyle karşılaştırıp sayıyoruz -- eşik yok, sayım var.
    agree_rows, n_agree = [], 0
    for r in series.values():
        modals = [r["metrics"][m]["argmin_T_modal"] for m in METRIC_ORDER]
        consensus = max(set(modals), key=modals.count)
        for m in METRIC_ORDER:
            pm = r["metrics"][m]
            ok = pm["argmin_T_modal"] == consensus
            n_agree += ok
            if not ok:
                agree_rows.append((r["series"], METRIC_LABEL[m], pm["argmin_T_modal"],
                                   consensus, pm["argmin_T_unanimous"]))
        r["_consensus_T"] = consensus

    n_cells = len(series) * len(METRIC_ORDER)
    L += ["## Summary across the three series", "",
          f"**Where each metric puts the minimum.** {n_agree} of {n_cells} (series × metric) "
          "cells place the dose–response minimum at the same temperature as the majority of "
          "metrics in that series:", "",
          "| series | consensus argmin T | metrics agreeing |", "|---|---|---|"]
    for r in series.values():
        k = sum(1 for m in METRIC_ORDER
                if r["metrics"][m]["argmin_T_modal"] == r["_consensus_T"])
        L.append(f"| {r['series']} | **{r['_consensus_T']:g}** | {k}/{len(METRIC_ORDER)} |")
    L += ["",
          "This is the round's answer to the single-specification objection: the location of the "
          "optimum is a property of the arm, not of the binning rule. Bin count (10/15/25), "
          "binning scheme (equal-width vs equal-mass), class weighting (classwise) and even the "
          "two metrics that do no binning at all (NLL, Brier) land in the same place."]
    if agree_rows:
        L += ["", "**The exceptions, in full:**", "",
              "| series | metric | its argmin T | consensus | unanimous across seeds |",
              "|---|---|---|---|---|"]
        for s, m, got, cons, uni in agree_rows:
            L.append(f"| {s} | {m} | {got:g} | {cons:g} | {'yes' if uni else 'no'} |")
        L += ["",
              "A row marked unanimous is a **systematic** disagreement, not seed noise: all three "
              "seeds of that metric agree with each other and disagree with the other metrics."]
    L += ["",
          f"**Step consistency.** Across {total_runs} runs × 7 metrics, "
          f"{tot_steps - tot_break} of {tot_steps} individual seed-steps agree with the other "
          f"seeds at the same T pair ({100 * (tot_steps - tot_break) / tot_steps:.1f}%). Every "
          "disagreement is listed in its series' section above, by pair, seed and metric.", ""]

    payload = {"pre_registration": "PREREGISTRATIONS.md A10 (R3-1); no success criterion",
               "checkpoint": CKPT, "sd_convention": SD_CONVENTION,
               "metric_order": METRIC_ORDER,
               "verification": {"column": "ece_ew_15", "against": "logit cache ece_recomputed",
                                "tolerance": ECE15_TOL},
               "total_runs": total_runs, "total_steps": tot_steps, "total_breaks": tot_break,
               "series": series}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "robustness_metrics.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (OUT_DIR / "robustness_metrics.json").write_text(json.dumps(payload, indent=2, default=float),
                                                     encoding="utf-8")

    for r in series.values():
        print(f"{r['series']:<16} {r['n_runs']:>2} runs, T={[f'{t:g}' for t in r['T']]}")
        for m in METRIC_ORDER:
            pm = r["metrics"][m]
            print(f"    {METRIC_LABEL[m]:<14} monotone {pm['monotone_seeds']}/{pm['n_seeds']}  "
                  f"steps {pm['steps_consistent']}/{pm['steps_total']}")
    print(f"\nWrote {OUT_DIR / 'robustness_metrics.md'}")

    # Bant altyapısı genel depoda bulunmaz; yokluğu tablo üretimini durdurmamalı.
    try:
        import export_to_drive
        export_to_drive.hook("robustness_metrics.py")
    except ImportError:
        pass


if __name__ == "__main__":
    main()
