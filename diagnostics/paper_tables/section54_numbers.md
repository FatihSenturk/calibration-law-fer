# Number set for the 5.4 rewrite (B1–B4)

Producer: `diagnostics/section54_numbers.py` · @swa · sample sd (n-1, Bessel-corrected), computed over seeds · treatment−control, paired within seed

## B1 — Gate variants against a class-weighting-matched control

| teacher / variant | Δacc (pp) | acc signs | ΔECE | ECE signs | n |
|---|---|---|---|---|---|
| primary/gate:mean_logvar | +0.065 *(n=1)* | `+` | -0.0027 *(n=1)* | `-` | 1 |
| primary/gate:oracle_error | -0.011 ± 0.722 | `-+-` | +0.0004 ± 0.0053 | `+-+` | 3 |
| primary/gate:target_logvar | -0.326 *(n=1)* | `-` | +0.0019 *(n=1)* | `+` | 1 |
| stage1/gate:mean_logvar | -0.065 *(n=1)* | `-` | +0.0000 *(n=1)* | `+` | 1 |
| stage1/gate:oracle_error | -0.217 ± 0.457 | `-+-` | +0.0015 ± 0.0036 | `+-+` | 3 |
| stage1/gate:target_logvar | +0.261 *(n=1)* | `+` | -0.0028 *(n=1)* | `-` | 1 |
| vae9182/gate:mean_logvar | -1.043 *(n=1)* | `-` | +0.0067 *(n=1)* | `+` | 1 |
| vae9182/gate:oracle_error | -0.228 ± 0.493 | `--+` | +0.0056 ± 0.0040 | `+++` | 3 |

Per seed (`gate:oracle_error`, the only n=3 arm):

| tohum | Δacc (pp) | ΔECE |
|---|---|---|
| 1 | -0.065 | +0.0038 |
| 42 | -0.782 | +0.0102 |
| 43 | +0.163 | +0.0028 |

> Only VAE9182's gate rows appear here: the `class_weight_mode=none` control exists for that teacher alone (see B3 and `PREREGISTRATIONS.md` A8).

## B2 — The cancellation arithmetic (all VAE9182, same three seeds, @swa)

| # | quantity | arm pair | ΔECE | signs | n |
|---|---|---|---|---|---|
| (i) | effect of class weighting on the **control's own** ECE | baseline `none` − baseline `effective_number` | **-0.0052 ± 0.0038** | `---` | 3 |
| (ii) | the gate's **real** damage | `gate:oracle_error` − baseline `none` | **+0.0056 ± 0.0040** | `+++` | 3 |
| (iii) | the diff reported before P2 | `gate:oracle_error` − baseline `effective_number` | **+0.0004 ± 0.0011** | `+-+` | 3 |

**The identity closes exactly:** (ii) + (i) = +0.0056 − 0.0052 = +0.0004 = (iii), residual -2.7e-19.

> **This is the sentence for the text.** Two independent errors were almost exactly cancelling each other: class weighting **worsens** the control's ECE by 0.0052, while the gate worsens the student's ECE by 0.0056. When the two meet in one difference, what remains is +0.0004 — indistinguishable from zero, and the three seeds' signs are mixed, `+-+`. Control hygiene here was therefore not a gesture of rigour but the result itself.

## B3 — T5'in yeni iskeleti

**Rows standing on three paired seeds (12):**

`primary/adaptive_t`, `primary/g2g_kl`, `primary/gate:oracle_error`, `primary/logit_std`, `stage1/adaptive_t`, `stage1/g2g_kl`, `stage1/gate:oracle_error`, `stage1/logit_std`, `vae9182/adaptive_t`, `vae9182/g2g_kl`, `vae9182/gate:oracle_error`, `vae9182/logit_std`.

**Tek tohum † (9):**

`primary/ctkd`, `primary/gate:mean_logvar`, `primary/gate:target_logvar`, `stage1/ctkd`, `stage1/gate:mean_logvar`, `stage1/gate:target_logvar`, `vae9182/ctkd`, `vae9182/g2g_kl+adaptive_t`, `vae9182/gate:mean_logvar`.

**Rows dropped for lack of a control (0):**

.

> All four dropped rows are `class_weight_mode=none` gate runs; stage1 and primary have no baseline in that mode. Differencing against the other mode's control would restore the two-variable situation P2 removed. Completing it costs 2 teachers × 3 seeds = 6 runs.

## B4 — The same runs against the contaminated control (as it will appear in the text)

| tohum | Δacc (pp) | ΔECE |
|---|---|---|
| 1 | +0.098 | -0.0008 |
| 42 | -0.033 | +0.0009 |
| 43 | -0.163 | +0.0012 |
| **ortalama** | **-0.033 ± 0.130** | **+0.0004 ± 0.0011** |
| signs | `-+-` | `+-+` |

For comparison, the same runs against the clean control: Δacc **-0.228 ± 0.493** pp `--+`, ΔECE **+0.0056 ± 0.0040** `+++`.

> **Wordings that can no longer be written:** "None does", "gating is null at the SWA checkpoint on every teacher", and any sentence calling the gate "neutral / no effect". The correct statement: **even with a perfect signal it degrades calibration consistently across three seeds.**

