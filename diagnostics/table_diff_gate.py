"""C2: refuse to ship a silently-changed table number.

WHAT THIS EXISTS TO CATCH, STATED PRECISELY. On 2026-07-30 a filter change moved T10's headline
ratio from 76x to 3x. No internal check could have caught it: 3x is a perfectly plausible ratio,
every cell was internally consistent, every sd was finite, and no exception was raised. The only
thing that identified it was comparison against a REMEMBERED EARLIER VALUE. Self-validation cannot
detect a plausible wrong answer; only a baseline can. So the baseline is made explicit and
mechanical here instead of living in whoever happens to remember last week's number.

THE TWO TRIGGERS (the second was the actual tell in the T10 case):
  1. VALUE MOVED beyond the cell's own seed sd. The cell's sd is the natural yardstick: a shift
     smaller than the noise the cell already carries is not a finding, and a shift larger than it
     is either a new result or a bug -- either way a human should look. Cells with no sd (n=1, or
     a derived scalar like an axis ratio) fall back to REL_TOL.
  2. n CHANGED. Unconditional, no threshold. In the T10 case n went 3 -> 7 and that alone was
     sufficient signal; a cell silently gaining samples means its membership predicate changed.
     A cell appearing or disappearing is reported the same way.

This gate does NOT decide whether a change is right -- it only guarantees nobody finds out later.
Adding runs legitimately moves numbers; the workflow is: regenerate, read the diff, then
`--accept` to move the baseline forward with a note saying why.

Usage:
  python diagnostics/table_diff_gate.py                    # compare, exit 1 on any deviation
  python diagnostics/table_diff_gate.py --accept "P2/P3 runs added; deltas reviewed"
  python diagnostics/table_diff_gate.py --show             # print the current baseline's provenance

Outputs -> diagnostics/table_diff_gate/baseline.json  (+ last_diff.md on every comparison)
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

# This script echoes Turkish reasons and cell labels; the Windows console defaults to cp1252 and
# would raise UnicodeEncodeError on the first "ş" -- after the baseline file had already been
# written, i.e. it would fail loudly while having half-succeeded.
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).resolve().parents[1]
D = ROOT / "diagnostics"
OUT_DIR = D / "table_diff_gate"
OUT_DIR.mkdir(parents=True, exist_ok=True)
BASELINE = OUT_DIR / "baseline.json"
LAST_DIFF = OUT_DIR / "last_diff.md"

REL_TOL = 0.02   # fallback for cells with no sd: 2% relative, or 1e-4 absolute, whichever is larger
ABS_FLOOR = 1e-4


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def cells_from_tables(p):
    """T5 mechanism cells and T10 capacity cells + axis spans."""
    out = {}
    if not p.exists():
        return out
    d = json.loads(p.read_text(encoding="utf-8"))
    for key, row in d.get("T5_mechanisms", {}).items():
        for ck in ("swa", "best", "last"):
            c = row.get(ck)
            if not c or c.get("d_ece_mean") is None:
                continue
            out[f"T5/{key}/{ck}/d_acc"] = (c.get("d_acc_mean"), c.get("d_acc_sd"), c.get("n"))
            out[f"T5/{key}/{ck}/d_ece"] = (c.get("d_ece_mean"), c.get("d_ece_sd"), c.get("n"))
    for ck, cells in d.get("T10_capacity_cells", {}).items():
        for name, c in cells.items():
            out[f"T10/{name}/{ck}/acc"] = (c["acc_mean"], c["acc_sd"], c["n"])
            out[f"T10/{name}/{ck}/ece"] = (c["ece_mean"], c["ece_sd"], c["n"])
    for ck, s in d.get("T10_axis_spans", {}).items():
        for k, v in s.items():
            out[f"T10/axis/{ck}/{k}"] = (v, None, None)
    return out


def cells_from_capacity_law(p):
    out = {}
    if not p.exists():
        return out
    d = json.loads(p.read_text(encoding="utf-8"))
    sc = d.get("slope_comparison", {})
    for side in ("big", "small"):
        c = sc.get(side)
        if c:
            out[f"capacity_law/{side}/slope"] = (c["slope"], c.get("seed_noise_envelope"), None)
            out[f"capacity_law/{side}/r2"] = (c["r2"], None, None)
    if "slope_difference" in sc:
        out["capacity_law/slope_difference"] = (sc["slope_difference"],
                                               sc.get("combined_envelope"), None)
    return out


def cells_from_p2(p):
    out = {}
    if not p.exists():
        return out
    d = json.loads(p.read_text(encoding="utf-8"))
    for ck, c in d.get("by_checkpoint", {}).items():
        for arm in ("treat", "control"):
            a = c.get(arm, {})
            if a:
                out[f"P2/{arm}/{ck}/acc"] = (a["acc_mean"], a["acc_sd"], a["n"])
                out[f"P2/{arm}/{ck}/ece"] = (a["ece_mean"], a["ece_sd"], a["n"])
    for name, v in d.get("verdict", {}).items():
        if _num(v.get("measured")):
            out[f"P2/verdict/{name}/measured"] = (v["measured"], v.get("bar"), None)
    return out


def cells_from_headline(p):
    out = {}
    if not p.exists():
        return out
    h = json.loads(p.read_text(encoding="utf-8")).get("headline", {})
    if h:
        out["abstract/selection_optimism/d_acc"] = (h["d_acc_mean"], h["d_acc_sd"], h["n"])
        out["abstract/selection_optimism/d_ece"] = (h["d_ece_mean"], h["d_ece_sd"], h["n"])
    return out


def cells_from_dose_response(p):
    """T1-T4: the dose-response curves, i.e. the paper's central law.

    These were the first thing that should have been baselined and the last thing added -- the
    gate initially watched T5/T10 (where the two known defects happened) and left the core law
    unwatched, which is exactly the wrong bias: a gate should cover what matters most, not only
    where the last bug was.
    """
    out = {}
    if not p.exists():
        return out
    d = json.loads(p.read_text(encoding="utf-8"))
    for arm, a in d.get("arms", {}).items():
        for pt in a.get("points", []):
            T = pt.get("T")
            out[f"dose/{arm}/T={T:g}/teacher_ece"] = (pt["teacher_ece"], None, None)
            for ck, b in pt.get("by_ckpt", {}).items():
                out[f"dose/{arm}/T={T:g}/{ck}/student_ece"] = (b["ece_mean"], b.get("ece_sd"),
                                                               b.get("n"))
                if _num(b.get("acc_mean")):
                    out[f"dose/{arm}/T={T:g}/{ck}/student_acc"] = (b["acc_mean"], b.get("acc_sd"),
                                                                   b.get("n"))
    return out


def cells_from_r3_robustness(p):
    """R3-1: yedi metriğin doz-cevap değerleri (kol ortalamaları) + adım tutarlılığı.

    Bu blok olmadan R3 sayıları kapının DIŞINDA kalırdı: tablo yeniden üretildiğinde
    bir metrik sessizce kayabilir ve hiçbir şey bağırmazdı. Yeni bir tablo eklemek,
    onu buraya da eklemek demektir.
    """
    out = {}
    d = json.loads(p.read_text(encoding="utf-8"))
    for sname, s in d.get("series", {}).items():
        tag = sname.replace(" ", "_")
        for met, pm in s.get("metrics", {}).items():
            for T, mu in pm.get("mean", {}).items():
                out[f"R3-1/{tag}/{met}/T={T}"] = (mu, pm.get("sd", {}).get(T),
                                                 len(pm.get("by_seed", {})))
            out[f"R3-1/{tag}/{met}/steps"] = (pm.get("steps_consistent"), None,
                                              pm.get("steps_total"))
    return out


def cells_from_r3_tstar(p):
    """R3-2: dört öğretmenin iki T* değeri ve iki ECE farkı."""
    out = {}
    d = json.loads(p.read_text(encoding="utf-8"))
    for tag, r in d.get("results", {}).items():
        for k in ("T_star_nll", "T_star_ece", "abs_dT", "d_ece", "ece_removed_by_ts"):
            out[f"R3-2/{tag}/{k}"] = (r.get(k), None, None)
    return out


def cells_from_r3_jsd(p):
    """R3-3: her kesitin üç optimumu ve n'i."""
    out = {}
    d = json.loads(p.read_text(encoding="utf-8"))
    for name, r in d.get("results", {}).items():
        if not r.get("n"):
            continue
        tag = name.replace(" ", "_")
        for k in ("T_ece", "T_nll", "T_jsd"):
            out[f"R3-3/{tag}/{k}"] = (r.get(k), None, r.get("n"))
    return out


SOURCES = [
    (D / "p1_dose_response" / "two_dataset_overlay.json", cells_from_dose_response),
    (D / "paper_tables" / "RESULTS_TABLES.json", cells_from_tables),
    (D / "paper_tables" / "robustness_metrics.json", cells_from_r3_robustness),
    (D / "paper_tables" / "tstar_sensitivity.json", cells_from_r3_tstar),
    (D / "paper_tables" / "jsd_sensitivity.json", cells_from_r3_jsd),
    (D / "p5_efficiency" / "capacity_law_check.json", cells_from_capacity_law),
    (D / "p2_gate_oracle" / "p2_verdict.json", cells_from_p2),
    (D / "selection_audit" / "selection_optimism_headline.json", cells_from_headline),
]


def collect():
    cells, missing = {}, []
    for path, fn in SOURCES:
        if not path.exists():
            missing.append(str(path.relative_to(ROOT)))
            continue
        cells.update(fn(path))
    return cells, missing


def tolerance(sd, value):
    """The cell's own seed sd, or a relative fallback when it has none."""
    if _num(sd) and sd > 0:
        return sd, "1x cell sd"
    return max(abs(value) * REL_TOL, ABS_FLOOR), f"{REL_TOL:.0%} rel (no sd)"


def compare(cur, base):
    changed, n_changed, appeared, vanished = [], [], [], []
    for k, (v, sd, n) in sorted(cur.items()):
        if k not in base:
            appeared.append(k)
            continue
        bv, bsd, bn = base[k]
        if n != bn:
            n_changed.append((k, bn, n, bv, v))
            continue
        tol, why = tolerance(sd if _num(sd) else bsd, v if _num(v) else 0.0)
        if _num(v) and _num(bv) and abs(v - bv) > tol:
            changed.append((k, bv, v, v - bv, tol, why))
    for k in sorted(base):
        if k not in cur:
            vanished.append(k)
    return changed, n_changed, appeared, vanished


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--accept", metavar="REASON",
                    help="bless the current numbers as the new baseline, recording why")
    ap.add_argument("--show", action="store_true", help="print the baseline's provenance and exit")
    args = ap.parse_args()

    cur, missing = collect()
    if not cur:
        raise SystemExit("no numbers collected -- are the table artifacts generated?")

    if args.show:
        if not BASELINE.exists():
            raise SystemExit("no baseline yet")
        b = json.loads(BASELINE.read_text(encoding="utf-8"))
        print(f"baseline accepted {b['accepted_at']}\n  reason: {b['reason']}\n"
              f"  cells : {len(b['cells'])}")
        return

    if args.accept or not BASELINE.exists():
        reason = args.accept or "initial baseline (no prior version on disk)"
        BASELINE.write_text(json.dumps({
            "accepted_at": dt.datetime.now().isoformat(timespec="seconds"),
            "reason": reason,
            "sources": [str(p.relative_to(ROOT)) for p, _ in SOURCES],
            "cells": {k: list(v) for k, v in cur.items()},
        }, indent=2), encoding="utf-8")
        print(f"baseline written: {len(cur)} cells\n  reason: {reason}")
        if missing:
            print("  NOTE missing sources (not in baseline): " + ", ".join(missing))
        return

    b = json.loads(BASELINE.read_text(encoding="utf-8"))
    base = {k: tuple(v) for k, v in b["cells"].items()}
    changed, n_changed, appeared, vanished = compare(cur, base)

    L = ["# Table diff gate — last comparison", "",
         f"Baseline: **{b['accepted_at']}** — {b['reason']}  ",
         f"Cells compared: {len(cur)} ({len(base)} in the baseline)", ""]
    if n_changed:
        L += ["## ⚠️ n CHANGED (unconditional warning — a cell's membership rule may have moved)",
              "", "| cell | n old→new | value old | value new |", "|---|---|---|---|"]
        for k, bn, n, bv, v in n_changed:
            L.append(f"| `{k}` | {bn}→{n} | {bv:.4f} | {v:.4f} |")
        L.append("")
    if changed:
        L += ["## Value moved by more than its own seed sd", "",
              "| cell | old | new | diff | threshold | source of the threshold |",
              "|---|---|---|---|---|---|"]
        for k, bv, v, d, tol, why in changed:
            L.append(f"| `{k}` | {bv:.4f} | {v:.4f} | {d:+.4f} | {tol:.4f} | {why} |")
        L.append("")
    if appeared or vanished:
        L += ["## Cells appeared / vanished", ""]
        if appeared:
            L.append("**appeared:** " + ", ".join(f"`{k}`" for k in appeared))
        if vanished:
            L.append("**vanished:** " + ", ".join(f"`{k}`" for k in vanished))
        L.append("")
    if not (changed or n_changed or appeared or vanished):
        L.append("✅ No deviation — every cell is at its baseline value.")
    LAST_DIFF.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"baseline {b['accepted_at']}  ({b['reason']})")
    print(f"cells: {len(cur)} now, {len(base)} in baseline")
    for k, bn, n, bv, v in n_changed:
        print(f"  n CHANGED  {k}: n {bn}->{n}, value {bv:.4f} -> {v:.4f}")
    for k, bv, v, d, tol, why in changed:
        print(f"  MOVED      {k}: {bv:.4f} -> {v:.4f}  ({d:+.4f}, tol {tol:.4f} = {why})")
    for k in appeared:
        print(f"  APPEARED   {k}")
    for k in vanished:
        print(f"  VANISHED   {k}")
    if missing:
        print("  NOTE missing sources: " + ", ".join(missing))

    total = len(changed) + len(n_changed) + len(appeared) + len(vanished)
    if total:
        print(f"\n{total} deviation(s). Read {LAST_DIFF.relative_to(ROOT)}, then re-run with "
              f'--accept "why" once you have checked each one.')
        sys.exit(1)
    print("\nNo deviation: every cell matches the accepted baseline.")


if __name__ == "__main__":
    main()
