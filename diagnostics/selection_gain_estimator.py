"""Item 2: a CLEAN estimator of the epoch-selection artefact, from training logs only.

Three quantities, all needed, because each isolates something different:

  (a) selection_gain    -- how much accuracy you gain purely by taking the MAX of many noisy
                           per-epoch evaluations instead of a typical one. No model difference,
                           no checkpoint difference. This is the number the strong claim rests on.
  (b) best - last       -- UPPER BOUND: mixes (a) with any late-training drift/decay, because the
                           reference is a single final epoch.
  (c) best - swa        -- difference against a selection-free but genuinely DIFFERENT model
                           (SWA is a weight average, not an epoch), so it is not a pure
                           selection measurement at all.

TWO VARIANTS OF (a), and the distinction matters:
  a1  max(ALL epochs) - mean(last K)   <- the intuitive form, but NOT purely an order statistic:
                                          if the global max sits outside the last-K window, the
                                          comparison spans two different training regimes.
  a2  max(last K)     - mean(last K)   <- PURE order statistic: max of K draws vs the mean of the
                                          SAME K draws. No drift between the two windows by
                                          construction. This is the defensible number.
We report both plus the fraction of runs whose global argmax actually lies in the last-K window
(when that fraction is high, a1 ~ a2 and the intuitive form is safe).

ECE: training_log.csv logs epoch, train/val loss, train/val acc, lr -- there is NO per-epoch ECE
(create_training_log's field list), and per-epoch checkpoints are not kept (only best/last/swa).
So variant (a) is NOT COMPUTABLE for ECE from existing artefacts; it would require either
per-epoch ECE logging or per-epoch checkpoints, neither of which exists. What IS available:
  - (b) and (c) for ECE, from diagnostics/selection_audit/selection_audit.csv
  - a calibration-ADJACENT substitute: val_loss (cross-entropy NLL) IS logged per epoch, and NLL
    is a proper scoring rule that responds to calibration. Since epochs are selected by ACCURACY
    and not by loss, `val_loss at the accuracy-argmax epoch` minus `mean val_loss over last K`
    measures how atypical the selected epoch's calibration-sensitive loss is. Positive = the
    accuracy-selected epoch has WORSE NLL than a typical late epoch.

Read-only, zero GPU. Outputs -> diagnostics/selection_audit/selection_gain.json
"""
import csv
import json
import statistics as st
from pathlib import Path

from stats_convention import SD_CONVENTION, sample_sd

ROOT = Path(__file__).resolve().parents[1]
STUDENTS = ROOT / "results" / "unified_students"
AUDIT = ROOT / "diagnostics" / "selection_audit" / "selection_audit.csv"
OUT = ROOT / "diagnostics" / "selection_audit" / "selection_gain.json"
KS = (50, 100)


def read_log(p):
    ep, acc, loss = [], [], []
    for r in csv.DictReader(open(p, encoding="utf-8")):
        try:
            a, l = float(r["val_acc"]), float(r["val_loss"])
        except (KeyError, ValueError):
            continue
        ep.append(int(float(r["epoch"])))
        acc.append(a)
        loss.append(l)
    return ep, acc, loss


def main():
    runs = []
    for rn in sorted(STUDENTS.iterdir()):
        if not rn.is_dir():
            continue
        for ts in sorted(rn.iterdir()):
            mb, tl = ts / "metrics_best.json", ts / "training_log.csv"
            if not (mb.exists() and tl.exists()):
                continue
            if str(json.loads(mb.read_text()).get("dataset", "")).upper().replace("-", "") != "RAFDB":
                continue
            runs.append(ts)
    print(f"{len(runs)} finished RAF-DB runs with training logs\n")

    per_k = {k: {"a1": [], "a2": [], "loss": [], "argmax_in_window": 0, "n": 0} for k in KS}
    for ts in runs:
        ep, acc, loss = read_log(ts / "training_log.csv")
        if len(acc) < 20:
            continue
        gmax = max(acc)
        gargmax = acc.index(gmax)
        for k in KS:
            if len(acc) < k + 10:            # need a window plus some history
                continue
            win_acc, win_loss = acc[-k:], loss[-k:]
            d = per_k[k]
            d["a1"].append(gmax - st.mean(win_acc))
            d["a2"].append(max(win_acc) - st.mean(win_acc))
            d["loss"].append(loss[gargmax] - st.mean(win_loss))
            d["argmax_in_window"] += int(gargmax >= len(acc) - k)
            d["n"] += 1

    print("=== (a) PURE selection gain, from training logs (accuracy, pp) ===")
    out = {"sd_convention": SD_CONVENTION, "per_k": {}}
    for k in KS:
        d = per_k[k]
        if not d["n"]:
            continue
        out["per_k"][k] = {
            "n_runs": d["n"],
            "a1_max_all_minus_mean_lastK": {"mean": st.mean(d["a1"]), "sd": sample_sd(d["a1"])},
            "a2_pure_order_statistic": {"mean": st.mean(d["a2"]), "sd": sample_sd(d["a2"])},
            "argmax_in_last_K_frac": d["argmax_in_window"] / d["n"],
            "val_loss_at_selected_minus_mean_lastK": {"mean": st.mean(d["loss"]),
                                                     "sd": sample_sd(d["loss"])},
        }
        o = out["per_k"][k]
        print(f"  K={k:<4} n={d['n']}")
        print(f"    a2 PURE order statistic   max(last K) - mean(last K) = "
              f"{o['a2_pure_order_statistic']['mean']:+.3f} +/- {o['a2_pure_order_statistic']['sd']:.3f} pp"
              f"   <- defensible number")
        print(f"    a1 max(ALL) - mean(last K)                           = "
              f"{o['a1_max_all_minus_mean_lastK']['mean']:+.3f} +/- {o['a1_max_all_minus_mean_lastK']['sd']:.3f} pp")
        print(f"    global argmax lies inside the last-K window: {100*o['argmax_in_last_K_frac']:.0f}% of runs"
              + ("   (=> a1 ~ a2, intuitive form is safe)" if o['argmax_in_last_K_frac'] > 0.8
                 else "   (=> a1 spans two regimes, prefer a2)"))
        print(f"    val_loss(selected epoch) - mean val_loss(last K)     = "
              f"{o['val_loss_at_selected_minus_mean_lastK']['mean']:+.4f} +/- "
              f"{o['val_loss_at_selected_minus_mean_lastK']['sd']:.4f}"
              f"   (>0 = accuracy-selected epoch has WORSE NLL)")
        print()

    # (b) and (c) from the audit, for both accuracy and ECE
    by_run = {}
    for r in csv.DictReader(open(AUDIT, encoding="utf-8")):
        by_run.setdefault((r["run_name"], r["timestamp"]), {})[r["checkpoint"]] = r
    print("=== (b) upper bound and (c) vs SWA, from the checkpoint audit ===")
    out["audit_deltas"] = {}
    for ref in ("last", "swa"):
        tag = "b_best_minus_last" if ref == "last" else "c_best_minus_swa"
        dacc = [float(v["best"]["acc"]) - float(v[ref]["acc"]) for v in by_run.values()
                if "best" in v and ref in v]
        dece = [float(v["best"]["ece"]) - float(v[ref]["ece"]) for v in by_run.values()
                if "best" in v and ref in v]
        out["audit_deltas"][tag] = {
            "n": len(dacc),
            "d_acc": {"mean": st.mean(dacc), "sd": sample_sd(dacc)},
            "d_ece": {"mean": st.mean(dece), "sd": sample_sd(dece)}}
        print(f"  best - {ref:<5} (n={len(dacc)}): d_acc {st.mean(dacc):+.3f} +/- {sample_sd(dacc):.3f} pp"
              f"    d_ece {st.mean(dece):+.4f} +/- {sample_sd(dece):.4f}")

    out["ece_variant_a_note"] = (
        "NOT COMPUTABLE from existing artefacts: training_log.csv has no per-epoch ECE and no "
        "per-epoch checkpoints are retained (only best/last/swa). Would require per-epoch ECE "
        "logging or per-epoch checkpoints. The logged val_loss (NLL) is reported above as the "
        "closest available calibration-sensitive substitute.")
    print(f"\n  ECE variant (a): {out['ece_variant_a_note']}")

    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
