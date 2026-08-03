"""P4: an actionable teacher-SELECTION recipe based on teacher ECE, not teacher accuracy.

THE PRACTICAL PROBLEM. You have K candidate teachers and one GPU. Choosing by distilling a
student from each costs K x (4h+). Choosing by teacher accuracy is free -- and, on this
benchmark, WRONG: the most accurate teacher is not the best teacher.

THE RECIPE (all steps inference-only, no student training):
  1. Forward each candidate over the val split ONCE; cache logits.
  2. Compute ECE(T=1) and fit T* (NLL-optimal) from the cached logits -- closed form, free.
  3. RANK BY ECE, NOT ACCURACY.
  4. Read off the teacher-side headroom ECE(T=1) - ECE(T*). If it is meaningfully positive,
     distil with --teacher-temperature-scale T*: a free student-calibration gain that costs
     nothing at train time and does not touch architecture or recipe.
  5. Optionally predict the student's ECE before training it, via the fitted transfer relation
     below, to decide whether the candidate is worth a run at all.

This file quantifies steps 3 and 5 and reports the GPU cost the recipe avoids.

HONEST SCOPE: fitted on RAF-DB only, K=3 teachers for the ranking claim and 10 (teacher-ECE,
student-ECE) pairs from 2 teachers for the predictor. These are small n. The ranking claim is
reported as a rank correlation with its exact n, and the predictor is reported with
leave-one-out error, not in-sample error. Cross-dataset validation is NOT claimed.

Outputs -> diagnostics/p4_teacher_selection/
"""
import json
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "diagnostics"))
from stats_convention import SD_CONVENTION  # noqa: E402

OUT_DIR = ROOT / "diagnostics" / "p4_teacher_selection"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TEACHER_GRID = json.loads((ROOT / "diagnostics" / "teacher_ece_grid" / "teacher_ece_grid.json").read_text())
_SV = json.loads((ROOT / "diagnostics" / "seed_variance" / "seed_variance_table.json").read_text())
# seed_variance_table.json gained a top-level "sd_convention" stamp on 2026-07-28 and its cells
# moved under "cells". Accept both shapes so an older copy of the file still loads here.
SEED_VAR = _SV.get("cells", _SV)
OVERLAY = ROOT / "diagnostics" / "p1_dose_response" / "two_teacher_overlay.json"

# seed_variance_table keys -> teacher names in teacher_ece_grid
BASELINE_KEY = {"stage1": "T-A baseline", "primary": "T-B baseline", "vae9182": "T-C baseline"}
# Measured wall-clock for one 400e student KD run on this machine (RTX 5070), from the
# dose-response queue timings: ~4.3 h solo-equivalent per run.
HOURS_PER_STUDENT_RUN = 4.3


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    dx, dy = [a - mx for a in x], [b - my for b in y]
    den = (sum(a * a for a in dx) * sum(b * b for b in dy)) ** 0.5
    return sum(a * b for a, b in zip(dx, dy)) / den if den else float("nan")


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):           # average ranks over ties
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    return pearson(rank(x), rank(y))


def linfit(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    return my - b * mx, b            # intercept, slope


def step3_ranking():
    """Would accuracy-ranking or ECE-ranking have picked the right teacher?"""
    rows = []
    for t, key in BASELINE_KEY.items():
        g, s = TEACHER_GRID[t], SEED_VAR[key]
        rows.append({"teacher": t, "teacher_acc": g["own_acc_pct"], "teacher_ece": g["ece_T1"],
                     "T_star": g["T_star"],
                     "teacher_headroom": g["ece_T1"] - min(g["fine_sweep"].values()),
                     "student_acc": s["acc_mean"], "student_ece": s["ece_mean"],
                     "student_acc_sd": s["acc_sd"], "n_seeds": s["n"]})
    t_acc = [r["teacher_acc"] for r in rows]
    t_ece = [r["teacher_ece"] for r in rows]
    s_acc = [r["student_acc"] for r in rows]
    s_ece = [r["student_ece"] for r in rows]
    # Higher teacher acc should mean higher student acc; LOWER teacher ECE should mean higher
    # student acc, so negate ECE to make "bigger = predicted better" for both criteria.
    out = {
        "rows": rows,
        "spearman_teacherACC_vs_studentACC": spearman(t_acc, s_acc),
        "spearman_negTeacherECE_vs_studentACC": spearman([-e for e in t_ece], s_acc),
        "spearman_teacherECE_vs_studentECE": spearman(t_ece, s_ece),
        "n_teachers": len(rows),
    }
    best_by_acc = max(rows, key=lambda r: r["teacher_acc"])["teacher"]
    best_by_ece = min(rows, key=lambda r: r["teacher_ece"])["teacher"]
    truly_best = max(rows, key=lambda r: r["student_acc"])["teacher"]
    out.update({"picked_by_accuracy": best_by_acc, "picked_by_ece": best_by_ece,
                "actually_best": truly_best,
                "accuracy_criterion_correct": best_by_acc == truly_best,
                "ece_criterion_correct": best_by_ece == truly_best,
                "cost_of_wrong_pick_pp": max(r["student_acc"] for r in rows)
                                         - next(r["student_acc"] for r in rows if r["teacher"] == best_by_acc)})
    return out


def step5_predictor():
    """Predict student ECE from teacher ECE, leave-one-out. Uses the dose-response points,
    where teacher ECE was MANIPULATED rather than merely observed."""
    if not OVERLAY.exists():
        return {"available": False, "reason": "two_teacher_overlay.json not built yet"}
    curves = json.loads(OVERLAY.read_text())["curves"]
    pts = [(p["teacher_ece"], p["student_ece_mean"], t, p["T"], p["n"])
           for t, ps in curves.items() for p in ps]
    x = [p[0] for p in pts]
    y = [p[1] for p in pts]
    a, b = linfit(x, y)

    loo_err = []
    for i in range(len(pts)):
        xi = x[:i] + x[i + 1:]
        yi = y[:i] + y[i + 1:]
        ai, bi = linfit(xi, yi)
        loo_err.append(abs((ai + bi * x[i]) - y[i]))
    return {
        "available": True, "n_points": len(pts),
        "intercept": a, "slope": b,
        "pearson": pearson(x, y), "spearman": spearman(x, y),
        "loo_mean_abs_error": st.mean(loo_err), "loo_max_abs_error": max(loo_err),
        "student_ece_range": [min(y), max(y)],
        "loo_error_as_pct_of_range": 100 * st.mean(loo_err) / (max(y) - min(y)),
        "points": [{"teacher": t, "T": T, "teacher_ece": xe, "student_ece": ye, "n_seeds": n}
                   for xe, ye, t, T, n in pts],
    }


def main():
    rank = step3_ranking()
    pred = step5_predictor()

    print("=== P4 step 3: which selection criterion picks the right teacher? ===")
    print(f"{'teacher':<10}{'teacher acc':<13}{'teacher ECE':<13}{'T*':<8}{'headroom':<11}"
          f"{'student acc':<14}{'student ECE'}")
    for r in sorted(rank["rows"], key=lambda r: -r["student_acc"]):
        print(f"{r['teacher']:<10}{r['teacher_acc']:<13.2f}{r['teacher_ece']:<13.4f}"
              f"{r['T_star']:<8.3f}{r['teacher_headroom']:<11.4f}"
              f"{r['student_acc']:<14.3f}{r['student_ece']:.4f}")
    print(f"\n  rank corr (teacher ACC  -> student ACC): {rank['spearman_teacherACC_vs_studentACC']:+.3f}")
    print(f"  rank corr (teacher ECE  -> student ACC): {rank['spearman_negTeacherECE_vs_studentACC']:+.3f}  (ECE negated)")
    print(f"  rank corr (teacher ECE  -> student ECE): {rank['spearman_teacherECE_vs_studentECE']:+.3f}")
    print(f"\n  pick by ACCURACY -> {rank['picked_by_accuracy']}  (correct: {rank['accuracy_criterion_correct']})")
    print(f"  pick by ECE      -> {rank['picked_by_ece']}  (correct: {rank['ece_criterion_correct']})")
    print(f"  actually best    -> {rank['actually_best']}")
    print(f"  cost of the accuracy-criterion mistake: {rank['cost_of_wrong_pick_pp']:.3f} pp student accuracy")
    print(f"  GPU cost avoided vs. distilling all {rank['n_teachers']} candidates: "
          f"{rank['n_teachers'] * 3 * HOURS_PER_STUDENT_RUN:.0f} h "
          f"({rank['n_teachers']} teachers x 3 seeds x {HOURS_PER_STUDENT_RUN} h) -> "
          f"replaced by {rank['n_teachers']} inference passes (~15 min each, CPU)")

    print("\n=== P4 step 5: predict student ECE from teacher ECE (leave-one-out) ===")
    if not pred["available"]:
        print(f"  unavailable: {pred['reason']}")
    else:
        print(f"  fit on n={pred['n_points']} manipulated points: "
              f"student_ECE = {pred['intercept']:+.4f} + {pred['slope']:.4f} * teacher_ECE")
        print(f"  Pearson {pred['pearson']:+.3f}   Spearman {pred['spearman']:+.3f}")
        print(f"  LOO mean |err| = {pred['loo_mean_abs_error']:.4f}  (max {pred['loo_max_abs_error']:.4f}); "
              f"student ECE spans {pred['student_ece_range'][0]:.4f}-{pred['student_ece_range'][1]:.4f}")
        print(f"  => LOO error is {pred['loo_error_as_pct_of_range']:.1f}% of the spanned range")
        n_partial = sum(1 for p in pred["points"] if p["n_seeds"] < 3)
        if n_partial:
            print(f"  NOTE: {n_partial}/{pred['n_points']} points are still <3 seeds; refit when complete.")

    # This file only PASSES THROUGH sds computed upstream (two_teacher_overlay.json), so the
    # stamp records the convention those numbers were produced under -- it does not re-derive it.
    payload = {"sd_convention": SD_CONVENTION,
               "recipe_step3_ranking": rank, "recipe_step5_predictor": pred,
               "hours_per_student_run": HOURS_PER_STUDENT_RUN}
    (OUT_DIR / "p4_teacher_selection.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT_DIR / 'p4_teacher_selection.json'}")


if __name__ == "__main__":
    main()
