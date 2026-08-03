"""R2-4/5: sıra-istatistiği penceresinde trend var mı? (K=50 → K=100 büyümesinin kaynağı)

SORU (R2 hakem turu): §4'ün saf sıra-istatistiği tahmini K=50'de +0.642, K=100'de +0.768 pp.
Büyüme son-K penceresindeki bir TRENDDEN mi (doğruluk hâlâ tırmanıyor → max−ort şişer),
yoksa salt mekanik mi (daha çok çekilişin maksimumu büyür)? Trend varsa detrend'li değer,
yoksa "plato" teyidi.

İKİ REFERANS:
  * Mekanik büyüme (iid Gauss altında): E[max−ort] ≈ σ·E[max of K std normals];
    K=50→100 oranı ≈ %8–9. Gözlenen büyüme bundan büyükse fazlası trend kokar.
  * Detrend: pencere içinde OLS doğrusu (acc ~ epoch) çıkarılır; artıkların
    max−ort'u = saf gürültü sıra-istatistiği. Trend katkısı = ham − detrend'li.

KAPSAM DONMUŞ DENETİM KÜMESİ: selection_audit.csv'nin (N=131) run_dir sütunundan.
DİKKAT — selection_gain_estimator.py kesme filtresi UYGULAMIYOR; bugün yeniden koşulsa
P5/P6 koşularını da katar ve §4'teki sayılar kayardı. Bu betik bu yüzden denetim CSV'sine
sabitlenir ve ham a2'yi §4 değerlerine karşı çapalar (tolerans 0.02 pp — §4 sayıları
üretildiğinde log'u olan koşu kümesi birebir aynı olmayabilir; sapma bundan büyükse DUR).

Salt-okunur, GPU yok. Çıktı -> diagnostics/paper_tables/order_stat_trend.{md,json}
"""
import csv
import json
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "diagnostics"))

from stats_convention import SD_CONVENTION, sample_sd  # noqa: E402

AUDIT = ROOT / "diagnostics" / "selection_audit" / "selection_audit.csv"
OUT_DIR = ROOT / "diagnostics" / "paper_tables"
KS = (50, 100)
PUBLISHED_A2 = {50: 0.642, 100: 0.768}   # §4 m6'daki değerler (pp)
ANCHOR_TOL = 0.02


def frozen_run_dirs():
    dirs = {}
    for r in csv.DictReader(open(AUDIT, encoding="utf-8")):
        dirs[(r["run_name"], r["timestamp"])] = Path(r["run_dir"])
    return sorted(set(dirs.values()))


def val_acc_series(run_dir):
    p = run_dir / "training_log.csv"
    if not p.exists():
        return []
    acc = []
    for r in csv.DictReader(open(p, encoding="utf-8")):
        try:
            acc.append(float(r["val_acc"]))
        except (KeyError, ValueError):
            continue
    return acc


def ols_residual_stats(win):
    """OLS acc ~ epoch-indeksi; (eğim, pencere-boyu sürüklenme, artık max−ort)."""
    k = len(win)
    xs = list(range(k))
    xbar, ybar = st.mean(xs), st.mean(win)
    sxx = sum((x - xbar) ** 2 for x in xs)
    b = sum((x - xbar) * (y - ybar) for x, y in zip(xs, win)) / sxx
    resid = [y - (ybar + b * (x - xbar)) for x, y in zip(xs, win)]
    return b, b * (k - 1), max(resid) - st.mean(resid)


def main():
    runs = frozen_run_dirs()
    print(f"donmuş denetim kümesi: {len(runs)} koşu dizini")

    agg = {k: {"a2": [], "slope": [], "drift": [], "a2_detr": []} for k in KS}
    for rd in runs:
        acc = val_acc_series(rd)
        for k in KS:
            if len(acc) < k + 10:
                continue
            win = acc[-k:]
            a2 = max(win) - st.mean(win)
            b, drift, a2_detr = ols_residual_stats(win)
            d = agg[k]
            d["a2"].append(a2)
            d["slope"].append(b)
            d["drift"].append(drift)
            d["a2_detr"].append(a2_detr)

    res = {}
    for k in KS:
        d = agg[k]
        m_a2 = st.mean(d["a2"])
        anchor_dev = abs(m_a2 - PUBLISHED_A2[k])
        if anchor_dev > ANCHOR_TOL:
            raise RuntimeError(f"K={k}: ham a2 {m_a2:.3f}, §4 {PUBLISHED_A2[k]} — sapma "
                               f"{anchor_dev:.3f} > {ANCHOR_TOL}. Küme uyuşmuyor, DUR.")
        res[k] = {"n_runs": len(d["a2"]),
                  "a2_raw": {"mean": m_a2, "sd": sample_sd(d["a2"])},
                  "published_a2": PUBLISHED_A2[k], "anchor_dev": anchor_dev,
                  "slope_pp_per_epoch": {"mean": st.mean(d["slope"]),
                                         "sd": sample_sd(d["slope"])},
                  "window_drift_pp": {"mean": st.mean(d["drift"]),
                                      "sd": sample_sd(d["drift"])},
                  "a2_detrended": {"mean": st.mean(d["a2_detr"]),
                                   "sd": sample_sd(d["a2_detr"])}}

    g_raw = res[100]["a2_raw"]["mean"] / res[50]["a2_raw"]["mean"]
    g_det = res[100]["a2_detrended"]["mean"] / res[50]["a2_detrended"]["mean"]

    L = ["# R2-4/5 — Trend analysis inside the order-statistic window", "",
         f"Producer: `diagnostics/order_stat_trend.py` · frozen audit set (N=131 runs, "
         f"those with a long enough log are in the table) · {SD_CONVENTION} · window = last K "
         f"epochs, OLS detrend.", "",
         "| K | n | raw a2 (max−mean) | §4 value | OLS drift (over the window) | "
         "**detrended a2** |",
         "|---|---|---|---|---|---|"]
    for k in KS:
        r = res[k]
        L.append(f"| {k} | {r['n_runs']} | {r['a2_raw']['mean']:+.3f} ± "
                 f"{r['a2_raw']['sd']:.3f} | +{r['published_a2']:.3f} | "
                 f"{r['window_drift_pp']['mean']:+.3f} ± {r['window_drift_pp']['sd']:.3f} pp | "
                 f"**{r['a2_detrended']['mean']:+.3f} ± {r['a2_detrended']['sd']:.3f}** |")
    L += ["",
          f"K=50→100 growth: raw {100 * (g_raw - 1):+.1f}% · detrended {100 * (g_det - 1):+.1f}% "
          "(the purely mechanical growth of an iid Gaussian maximum is ≈ +8–9%).", ""]
    payload = {"sd_convention": SD_CONVENTION, "results": {str(k): res[k] for k in KS},
               "growth_raw": g_raw, "growth_detrended": g_det}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "order_stat_trend.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (OUT_DIR / "order_stat_trend.json").write_text(json.dumps(payload, indent=2),
                                                  encoding="utf-8")
    for k in KS:
        r = res[k]
        print(f"K={k:<4} n={r['n_runs']}  ham {r['a2_raw']['mean']:+.3f}±{r['a2_raw']['sd']:.3f}"
              f"  sürüklenme {r['window_drift_pp']['mean']:+.3f}"
              f"  detrend {r['a2_detrended']['mean']:+.3f}±{r['a2_detrended']['sd']:.3f}")
    print(f"büyüme: ham {100 * (g_raw - 1):+.1f}%  detrend {100 * (g_det - 1):+.1f}%")
    print(f"Wrote {OUT_DIR / 'order_stat_trend.md'}")


if __name__ == "__main__":
    main()
