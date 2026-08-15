"""G3.1 + G3.2 — 2×-kontrol-sd ölçütünün resmîleştirilmesi ve yanlış-pozitif oranı.

İTİRAZ (Round-2 panel, DA-13): "established effect" ölçütü hiçbir yerde tanımlı değil ve
paydası seçilmiş görünüyor. Oracle zararı +0.0056±0.0040, KONTROLÜN tohum sd'sine (0.0027)
bölününce 2.1× ile barajı geçiyor; ama kendi EŞLEŞTİRİLMİŞ-FARK sd'sine (0.0040) bölününce
1.4× ile geçmiyor. Ölçüt yazılı olmadığı için okuyucu hangisinin kullanıldığını bilmiyor.

BU DOSYANIN YAPTIĞI ÜÇ ŞEY:
  1. Ölçütü açıkça yazar (pay, payda, işaret koşulu, eşik).
  2. T5'in ÜÇ TOHUMLU HER hücresine, iki eksende (ECE ve doğruluk), üç checkpoint'te
     MEKANİK uygular — seçici değil. Geçen de geçmeyen de aynı tabloda.
  3. Aynı hücreleri ALTERNATİF paydayla (eşleştirilmiş-fark sd'si) tekrar hesaplar, böylece
     DA-13'ün işaret ettiği fark her hücre için görünür olur.
  4. (G3.2) Ölçütün tohum-gürültüsü null'u altındaki yanlış-pozitif oranını simülasyonla
     verir ve T5'in hücre sayısıyla aile-bazlı FPR'yi hesaplar.

ÖLÇÜT (kampanyada fiilen kullanılan hâliyle, burada yazıya geçiriliyor):
    pay     = |ort eşleştirilmiş fark|            (mekanizma − kendi eşleşmiş kontrolü, tohum-içi)
    payda   = o öğretmenin KENDİ kontrol kolunun tohum sd'si, aynı metrikte ve aynı checkpoint'te
    işaret  = n tohumun n'sinde aynı işaret
    eşik    = pay/payda ≥ 2  VE  işaret koşulu  ->  "established"; aksi hâlde "unresolved"

Payda `denominator_table.control_arms()`'tan İTHAL edilir, yeniden yazılmaz; o fonksiyon
checkpoint parametreli olduğu için @swa dışındaki iki checkpoint de aynı tanımla üretilir.

Salt-okunur, GPU yok.
Çıktı -> diagnostics/paper_tables/criterion_applied.{md,json}
Kullanım: python diagnostics/criterion_applied.py
"""
import json
import statistics as st
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "diagnostics"))

from paper_tables import CKPTS, load_audit, load_runs, mechanism_table  # noqa: E402
from denominator_table import control_arms  # noqa: E402  -- TEK KAYNAK: payda tanımı
from t5_pairing_diff import build  # noqa: E402  -- TEK KAYNAK: tohum-tohum eşleştirme
from paper_tables import A_AUDIT_MECH  # noqa: E402
from stats_convention import SD_CONVENTION, sample_sd  # noqa: E402

OUT_DIR = ROOT / "diagnostics" / "paper_tables"
THRESHOLD = 2.0
N_SIM = 200_000          # G3.2; prompt >=10k istiyor, fazlası bedava
RNG_SEED = 20260806

HONESTY = (
    "> **Review-responsive, not pre-declared (5 Aug 2026).** Computed after the Round-2 panel "
    "report; no prediction was frozen beforehand. The pre-declaration inventory of §4.5 is "
    "unaffected — these analyses are reported as post-hoc re-analyses of existing artifacts."
)


def verdict(ratio, signs, n):
    """Ölçütün üç bileşeni. n<2 ise hüküm verilmez."""
    if ratio is None or n < 2:
        return "n/a"
    same = len(set(signs)) == 1 and len(signs) == n
    return "established" if (ratio >= THRESHOLD and same) else "unresolved"


def simulate_fpr(k, n=3, thr=THRESHOLD, reps=N_SIM, rng=None):
    """Tohum-gürültüsü null'u altında ölçütün tek-hücre yanlış-pozitif oranı.

    Null: mekanizmanın etkisi YOK; tohum-içi eşleştirilmiş farklar sıfır ortalamalı gürültü.
    Farkların tohum sd'si, kontrolün tohum sd'sinin k katı: s_d = k * sigma_c.
    Ölçüt |ort d| >= 2*sigma_c VE n/n aynı işaret istediği için, sigma_c=1 alıp d ~ N(0, k^2)
    çekmek genelliği bozmaz (ölçüt sigma_c'ye göre ölçek-değişmez).
    """
    d = rng.normal(0.0, k, size=(reps, n))
    mean_ok = np.abs(d.mean(axis=1)) >= thr           # sigma_c = 1
    sign_ok = (d > 0).all(axis=1) | (d < 0).all(axis=1)
    return float((mean_ok & sign_ok).mean())


# ÖĞRENİLMİŞ SİNYALLER (B5, 14 Ağu). Ölçüt doğruluk ekseninde de uygulanıyor, ama yalnız
# gate'in ÖĞRENİLMİŞ sinyalli hücrelerine. `oracle_error` sentetik bir sinyal (hatadan
# türetilmiş bir üst-sınır tanılaması), öğrenilmiş bir sinyal değil; aileye girmemesi
# bir seçim değil, sınıf farkı. Liste ad ad değil DESEN olarak yazılıyor ki yarın altıncı
# bir öğrenilmiş sinyal koşulursa aile kendiliğinden büyüsün.
LEARNED_SIGNALS = ("gate:mean_logvar", "gate:target_logvar")


def family_cells(payload, ck="swa"):
    """Ölçütün fiilen uygulandığı hücreler: ECE ekseninde hepsi, doğruluk ekseninde
    yalnız öğrenilmiş-sinyal gate hücreleri. n<2 hücre hüküm almaz, aileye de girmez."""
    out = []
    for cell, by_ck in sorted(payload.items()):
        v = by_ck.get(ck) or {}
        if (v.get("n") or 0) < 2:
            continue
        axes = ["ece"] + (["acc"] if cell.split("/", 1)[1] in LEARNED_SIGNALS else [])
        for axis in axes:
            a = v.get(axis) or {}
            if not a.get("sd_paired") or not a.get("sigma_control"):
                continue
            out.append({"cell": cell, "axis": axis,
                        "k": a["sd_paired"] / a["sigma_control"],
                        "teacher": cell.split("/", 1)[0],
                        "verdict": a["verdict"]})
    return out


def dependence(payload, fam, rng, ck="swa", reps=40_000):
    """B5(c) — paylaşılan kontrolün bağımsızlık varsayımını ne kadar deldiğinin ÖLÇÜMÜ.

    İki parça: (1) aynı kontrol kolunu paylaşan hücrelerin eşleştirilmiş-fark
    vektörleri arasındaki gözlenen ortalama korelasyon, paylaşmayanlarla yan yana;
    (2) o ortak bileşen simülasyona konduğunda aile-bazlı oranın ne olduğu.

    Grup anahtarı (öğretmen, sınıf-ağırlığı): T5'in eşleştirme anahtarı da bu, yani
    aynı gruptaki her hücre AYNI ÜÇ kontrol koşusundan çıkarılıyor.
    """
    vecs, groups = {}, {}
    for c in fam:
        v = (payload[c["cell"]].get(ck) or {}).get(c["axis"]) or {}
        d = v.get("seed_deltas") or []
        if len(d) < 3:
            continue
        arr = np.asarray(d, dtype=float)
        if arr.std() == 0:
            continue
        vecs[(c["cell"], c["axis"])] = (arr - arr.mean()) / arr.std()
        groups[(c["cell"], c["axis"])] = (c["teacher"], v.get("control_arm"), c["axis"])

    keys = sorted(vecs)
    shared, other = [], []
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            r = float(np.corrcoef(vecs[a], vecs[b])[0, 1])
            (shared if groups[a] == groups[b] else other).append(r)
    rho_s = float(np.mean(shared)) if shared else 0.0
    rho_o = float(np.mean(other)) if other else 0.0

    # (2) ortak bileşenli simülasyon: grup içi eş-korelasyonlu null.
    by_group = {}
    for c in fam:
        v = (payload[c["cell"]].get(ck) or {}).get(c["axis"]) or {}
        by_group.setdefault((c["teacher"], v.get("control_arm"), c["axis"]), []).append(c["k"])
    rho = max(rho_s, 0.0)
    any_fire = np.zeros(reps, dtype=bool)
    for ks in by_group.values():
        g = rng.normal(0.0, 1.0, size=(reps, 3))                  # grubun ortak tohum yükü
        for k in ks:
            e = rng.normal(0.0, 1.0, size=(reps, 3))
            d = k * (np.sqrt(rho) * g + np.sqrt(1 - rho) * e)
            fire = (np.abs(d.mean(axis=1)) >= THRESHOLD) & (
                (d > 0).all(axis=1) | (d < 0).all(axis=1))
            any_fire |= fire
    return {"rho_shared": rho_s, "rho_other": rho_o, "n_shared": len(shared),
            "n_other": len(other), "rho_used": rho, "fam_dep": float(any_fire.mean()),
            "n_groups": len(by_group)}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    runs = load_runs()
    audit = load_audit(A_AUDIT_MECH)
    _lines, mech = mechanism_table(runs, audit)
    denom = {ck: control_arms(runs, audit, ck=ck) for ck in CKPTS}
    # Tohum-tohum farklar için aynı eşleştirme, İKİNCİ KEZ YAZILMADAN: `build(rule="new")`
    # T5'in anahtarını (öğretmen, tohum, sınıf-ağırlığı) kullanıyor ve `noise_units` de
    # oradan besleniyor. Ayrı bir eşleştirme yazmak iki tablonun ayrışmasına davetiye olurdu.
    paired = build(runs, audit, "new")[0]

    rows, payload = [], {}
    for key in sorted(mech):
        row = mech[key]
        t, cw = row["teacher"], row["control_class_weight_mode"]
        payload[key] = {}
        for ck in CKPTS:
            c = row.get(ck) or {}
            n = c.get("n") or 0
            arm = denom[ck].get((t, cw))
            out = {"n": n}
            for axis, mkey, skey, sgkey, dkey in (
                    ("ece", "d_ece_mean", "d_ece_sd", "d_ece_signs", "ece_sd"),
                    ("acc", "d_acc_mean", "d_acc_sd", "d_acc_signs", "acc_sd")):
                mean, sd_pair = c.get(mkey), c.get(skey)
                signs = c.get(sgkey) or ""
                sigma_c = arm[dkey] if arm else None
                r_ctrl = (abs(mean) / sigma_c) if (mean is not None and sigma_c) else None
                r_pair = (abs(mean) / sd_pair) if (mean is not None and sd_pair) else None
                pc = (paired.get((t, key.split("/", 1)[1])) or {}).get("by_ckpt", {}).get(ck)
                out[axis] = {"mean": mean, "sd_paired": sd_pair, "sigma_control": sigma_c,
                             "signs": signs, "n": n,
                             "ratio_vs_control_sd": r_ctrl, "ratio_vs_paired_sd": r_pair,
                             "verdict": verdict(r_ctrl, signs, n),
                             "verdict_if_paired_sd": verdict(r_pair, signs, n),
                             "seed_deltas": (pc or {}).get(f"d_{axis}_list") or [],
                             "control_arm": cw}
            payload[key][ck] = out
            if ck == "swa" and n >= 2:
                rows.append((key, out))

    # ---------- G3.2: yanlış-pozitif oranı
    rng = np.random.default_rng(RNG_SEED)
    ks_obs = [v["ece"]["sd_paired"] / v["ece"]["sigma_control"]
              for _k, v in rows if v["ece"]["sd_paired"] and v["ece"]["sigma_control"]]
    k_grid = [0.5, 1.0, 1.41, 2.0, 3.0]
    fpr = {k: simulate_fpr(k, rng=rng) for k in k_grid}
    k_med = float(np.median(ks_obs)) if ks_obs else None
    fpr_med = simulate_fpr(k_med, rng=rng) if k_med else None
    n_cells = len(rows)
    fam_med = (1 - (1 - fpr_med) ** n_cells) if fpr_med is not None else None

    # ---------- rapor
    L = ["# G3.1 + G3.2 — The 2×-control-sd criterion, written down and applied to every cell",
         "", HONESTY, "",
         f"Producer: `diagnostics/criterion_applied.py` · {SD_CONVENTION} · "
         f"denominators imported from `denominator_table.control_arms()`", "",
         "## G3.1 — The criterion, stated", "",
         "| component | definition |", "|---|---|",
         "| numerator | \\|mean paired difference\\| — mechanism minus **its own matched "
         "control**, within seed |",
         "| denominator | the seed sd of **that teacher's own control arm**, same metric, same "
         "checkpoint |",
         "| sign condition | all n seeds share the sign |",
         f"| threshold | ratio ≥ **{THRESHOLD:g}** *and* the sign condition → `established`; "
         "otherwise `unresolved` |", "",
         "The denominator is the **control arm's** seed sd, not the paired difference's own sd. "
         "Both are reported below for every cell, because the choice changes verdicts and the "
         "reader is entitled to see by how much.", "",
         "## Every three-seed cell of Table 3, @swa, ECE axis", "",
         "Applied mechanically — no cell is omitted for failing.", "",
         "| cell | mean ΔECE | signs | σ_control | ratio | verdict | σ_paired | ratio | verdict |",
         "|---|---|---|---|---|---|---|---|---|"]
    for key, v in rows:
        e = v["ece"]
        L.append(
            f"| `{key}` | {e['mean']:+.4f} | {e['signs']} | {e['sigma_control']:.4f} | "
            f"**{e['ratio_vs_control_sd']:.2f}×** | {e['verdict']} | "
            f"{e['sd_paired']:.4f} | {e['ratio_vs_paired_sd']:.2f}× | "
            f"{e['verdict_if_paired_sd']} |")

    n_est = sum(1 for _k, v in rows if v["ece"]["verdict"] == "established")
    n_est_p = sum(1 for _k, v in rows if v["ece"]["verdict_if_paired_sd"] == "established")
    flips = [k for k, v in rows
             if v["ece"]["verdict"] != v["ece"]["verdict_if_paired_sd"]]
    L += ["",
          f"**{n_est}/{n_cells}** cells are `established` under the control-sd denominator; "
          f"**{n_est_p}/{n_cells}** under the paired-difference denominator. "
          + (f"The verdict changes for **{len(flips)}** cell(s): "
             + ", ".join(f"`{k}`" for k in flips) + "."
             if flips else "No cell changes verdict between the two denominators."), ""]

    # doğruluk ekseni
    L += ["## The same cells, accuracy axis (@swa)", "",
          "| cell | mean Δacc (pp) | signs | σ_control | ratio | verdict |", "|---|---|---|---|---|---|"]
    for key, v in rows:
        a = v["acc"]
        L.append(f"| `{key}` | {a['mean']:+.3f} | {a['signs']} | {a['sigma_control']:.3f} | "
                 f"{a['ratio_vs_control_sd']:.2f}× | {a['verdict']} |")

    L += ["", "## G3.2 — What false-positive rate does this criterion carry?", "",
          "Simulation under a seed-noise null: the mechanism has **no** effect, so the within-seed "
          f"paired differences are zero-mean noise. Their seed sd is `k ×` the control's seed sd. "
          f"The criterion is scale-free in σ_control, so σ_control = 1 without loss of generality. "
          f"{N_SIM:,} replicates per k, n = 3 seeds, RNG seed {RNG_SEED}.", "",
          "| k = σ_paired / σ_control | per-cell false-positive rate |", "|---|---|"]
    for k in k_grid:
        L.append(f"| {k:.2f} | {fpr[k]:.4f} |")
    if k_med is not None:
        L += ["",
              f"The **observed** k across the {len(ks_obs)} three-seed ECE cells has median "
              f"**{k_med:.2f}** (range {min(ks_obs):.2f}–{max(ks_obs):.2f}). At that k the "
              f"per-cell false-positive rate is **{fpr_med:.4f}**, and over the "
              f"{n_cells} cells of Table 3 the family-wise rate — the chance that *at least one* "
              f"cell fires by chance — is **{fam_med:.3f}** "
              f"(1 − (1 − {fpr_med:.4f})^{n_cells}, independence assumed).", ""]
    # ---------- G3.3 (B5, 14 Ağu): AİLE 17 DEĞİL 22
    fam = family_cells(payload)
    ks_fam = [c["k"] for c in fam]
    fpr_fam = {}
    for c in fam:
        fpr_fam[c["cell"] + "|" + c["axis"]] = simulate_fpr(c["k"], rng=rng)
    p_list = list(fpr_fam.values())
    fam_exact = 1 - float(np.prod([1 - p for p in p_list]))
    n22 = len(fam)
    fam_flat = 1 - (1 - fpr_med) ** n22 if fpr_med is not None else None
    dep = dependence(payload, fam, rng)

    L += [f"### G3.3 — the family is **{n22}**, not {n_cells} (B5, 14 Aug 2026)", "",
          f"The criterion is applied on the ECE axis to the {n_cells} three-seed cells, **and "
          f"on the accuracy axis to the {n22 - n_cells} learned-signal gate cells** "
          f"(`{'`, `'.join(LEARNED_SIGNALS)}`; `oracle_error` is synthetic, not a learned "
          f"signal, so it is not in this family). Counting only the ECE axis understates the "
          f"family by {n22 - n_cells} tests.", "",
          "| family | n | family-wise rate |", "|---|---|---|",
          f"| ECE axis only (as published) | {n_cells} | {fam_med:.3f} |",
          f"| **ECE + learned-signal accuracy cells** | **{n22}** | "
          f"**{fam_flat:.3f}** |",
          f"| same {n22} cells, each at its **own** k | {n22} | {fam_exact:.3f} |", "",
          f"At the median per-cell rate the {n22}-test value is "
          f"1 − (1 − {fpr_med:.4f})^{n22} = **{fam_flat:.3f}**. Using each cell's own k "
          f"instead of the median gives **{fam_exact:.3f}** — the median understates it, "
          f"because the rate is convex in k and a handful of high-k cells carry most of "
          f"the risk.", "",
          "#### Sensitivity across the observed spread ratio", "",
          f"k = σ_paired/σ_control over the {n22} cells: **{min(ks_fam):.2f} … "
          f"{max(ks_fam):.2f}** (median {float(np.median(ks_fam)):.2f}). The per-cell rate "
          f"is not flat over that range — it moves by more than two orders of magnitude:", "",
          "| k | per-cell rate | which cell |", "|---|---|---|"]
    for c in sorted(fam, key=lambda c: c["k"])[:1] + \
            [sorted(fam, key=lambda c: c["k"])[len(fam) // 2]] + \
            sorted(fam, key=lambda c: c["k"])[-1:]:
        L.append(f"| {c['k']:.2f} | {fpr_fam[c['cell'] + '|' + c['axis']]:.4f} | "
                 f"`{c['cell']}` ({c['axis'].upper()}) |")
    L += ["",
          f"> The lowest-k cell fires by chance essentially never "
          f"({min(p_list):.4f}); the highest-k cell fires **{max(p_list):.3f}** of the "
          f"time. A single family-wise number therefore hides a very uneven distribution "
          f"of risk across the table.", "",
          "#### The independence assumption, measured", "",
          f"> **One sentence:** cells that share a control arm have mean pairwise "
          f"correlation **{dep['rho_shared']:+.3f}** across their three seeds "
          f"(n = {dep['n_shared']} pairs) against **{dep['rho_other']:+.3f}** for cells "
          f"that do not (n = {dep['n_other']} pairs), and re-simulating the {n22}-cell "
          f"family with that shared component inside each control group gives a "
          f"family-wise rate of **{dep['fam_dep']:.3f}** instead of the "
          f"**{fam_exact:.3f}** the independence product reports — so the published "
          f"figure is an upper bound, and the measured size of the gap is "
          f"{abs(fam_exact - dep['fam_dep']):.3f}.", "",
          "The correlation is not an artefact of small n alone: it is what the design "
          "**implies**. Every cell in a group is differenced against the *same three "
          "control runs*, so the control's seed noise enters every difference in that "
          "group with the same sign. Sharing the seed set (42/1/43) on the treatment side "
          "adds a second, smaller channel.", ""]

    L += ["Sources: `paper_tables.mechanism_table()` (cells) and "
          "`denominator_table.control_arms()` (denominators), both imported rather than "
          "reimplemented.", ""]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "criterion_applied.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (OUT_DIR / "criterion_applied.json").write_text(json.dumps(
        {"note": "review-responsive, not pre-declared", "sd_convention": SD_CONVENTION,
         "criterion": {"numerator": "|mean paired difference|",
                       "denominator": "control arm seed sd, same metric and checkpoint",
                       "sign_condition": "all n seeds share the sign",
                       "threshold": THRESHOLD},
         "cells": payload,
         "fpr": {"n_sim": N_SIM, "rng_seed": RNG_SEED, "by_k": fpr,
                 "k_observed_median": k_med, "k_observed_range": [min(ks_obs), max(ks_obs)]
                 if ks_obs else None,
                 "per_cell_at_observed_k": fpr_med, "n_cells": n_cells,
                 "family_wise_upper_bound": fam_med}},
        indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"ECE @swa: {n_est}/{n_cells} established (kontrol sd) | "
          f"{n_est_p}/{n_cells} (eşleştirilmiş sd) | hüküm değişen: {len(flips)}")
    for k in k_grid:
        print(f"  FPR k={k:.2f}: {fpr[k]:.4f}")
    if k_med:
        print(f"  gözlenen k medyan {k_med:.2f} -> hücre FPR {fpr_med:.4f}, "
              f"aile ({n_cells} hücre) {fam_med:.3f}")
    print(f"\nWrote {OUT_DIR / 'criterion_applied.md'}")


if __name__ == "__main__":
    main()
