# Pre-registration inventory — which prediction was frozen where, and was it before the result?

> **Translation note (public release).** This file is an English translation of the campaign's
> Turkish working document. The translation changes wording only: every date, artefact path, line
> number, threshold and measured value is carried over unchanged, and the Turkish original is
> retained in the private working repository. The other laboratory records in this repository
> (`BULGULAR.md`, `METHODS_DATA.md`, `diagnostics/DIAGNOSTIC_REPORT.md`, `diagnostics/reports/`)
> are still in Turkish and were deliberately not rewritten — see `README.md`.

Producer note: this file was written by hand, but every date inside it was read from the file
system (`stat` mtime + run directory name). To re-verify: compare `stat -c '%y' <artefact>` with
`ls -1d results/unified_students/<run>/*/`.

---

## ⚠️ First, the limit of the evidence — the paper will state it this way too

`poster-var` **is a git repository** (first commit 2026-07-11 22:37:46). But **no pre-registration
has a commit hash**, and the reason is not the absence of git: between 14 July 17:41 and 31 July
17:04 there is **not a single commit**, and every pre-registration below was frozen inside exactly
that gap. Their first entry into git is that same commit (`9b2d31c`, 31 Jul 17:04) — which, for
A1–A8, is *after* the results were obtained. So the commit history produces no evidence for these
pre-registrations; the measurement is in
`diagnostics/reports/2026-07-31_git_provenance.md`. Two independent timestamps remain unchanged:

1. **The artefact's mtime** — the last modification time of the `.ps1` / `.py` file carrying the
   prediction text. Weakness: mtime can be altered by hand, and editing the file afterwards moves
   it forward.
2. **The run directory's name** — `results/unified_students/<name>/<YYYY-MM-DD-HH-MM-SS>/`. The
   training script produces this stamp at its own start; it cannot be written or edited afterwards.

**Rule:** a pre-registration counts as "frozen before the result" only if (1) < (2), and the
prediction text must be **inside** that artefact. Both are shown below.

**`BULGULAR.md` is NOT pre-registration evidence.** Being a single continuously edited file, its
mtime (28 Jul 05:59) shows only the most recent edit; it proves nothing about when any section
inside it was written. The prediction texts in BULGULAR are **copies** of the artefacts below, not
their source. Only pre-registrations **with an artefact** will be called "pre-registered" in the
paper.

---

## A. Pre-registrations with an artefact (may be called "pre-registered" in the paper)

### A1 · B-007 — the flat-control prediction (VAE9182 dose-response)

| field | value |
|---|---|
| **artefact** | `rafdb_p1_vae9182_flatcontrol_queue.ps1`, lines 16-20 |
| **frozen** | 2026-07-24 18:05:30 |
| **first run started** | `2026-07-24-18-05-50` (**+20 seconds**) |
| **before the result** | ✅ **yes** |
| **outcome** | table T2 · confirmed (minimum at T=1.0, monotone damage for T>1) |

> "Prediction (calibration-conditioned headroom law, B-007): because there is little
> miscalibration to correct, this curve should be FLAT/shallow with its minimum near T=1.0 --
> NO deep dip like Stage1's (which improved -46% ECE at T\*=1.34). If VAE9182 at T=1.34 does NOT
> improve (or worsens), that is the headroom-proportional-to-miscalibration evidence..."

**Honest context:** this prediction was written **knowing** the outcome of the Stage1 arm (the
Stage1 grid ran on 23–24 Jul). That is not a flaw — the prediction concerns *a different teacher*
and is derived from the law — but it cannot be written up as "both arms were predicted blind". The
blind arm is VAE9182.

---

### A2 · B-010 — the miscalibration-injection kill-switch

| field | value |
|---|---|
| **artefact** | `rafdb_p3_then_miscal_chain.ps1`, lines 42-49 |
| **frozen** | 2026-07-25 14:35:43 |
| **first run started** | `2026-07-25-23-19-09` (**+8 h 43 min**) |
| **before the result** | ✅ **yes** |
| **outcome** | **NULL** — the kill-switch fired, the third seed was not spent |

> "KILL-SWITCH: 2 seeds first. If the ECE delta does not clear the native -0.0034 in BOTH
> seeds, stop -- do not spend the 3rd seed."

**Critical detail — I got my own rule wrong the first time I applied it.** The first version of the
kill-switch code said "PASS, spend the third seed", because it tested the *mean* against the bar
while the pre-registration said "in BOTH seeds". The corrected rule requires two criteria: (1)
**every seed** below the −0.0034 bar, and (2) consistent signs. Measured: `['+', '-']`, mean
−0.0021 ± 0.0045 (n=2, sample sd) → **both criteria fail**. This is not "loosening the rule after
seeing the result" but the opposite: the rule was tightened and the outcome turned NULL. The paper
should tell this story briefly.

---

### A3 · B-015 — FERPlus dose-response, three predictions at once

| field | value |
|---|---|
| **artefact** | `ferplus_dose_response_queue.ps1`, lines 38-41 |
| **frozen** | 2026-07-26 13:27:26 |
| **first run started** | `2026-07-26-13-27-45` (**+19 seconds**) |
| **before the result** | ✅ **yes** |
| **outcome** | **CONFIRMED** — 3/3 predictions, 3/3 checkpoints, 9/9 within-seed curves |

> "PRE-REGISTERED PREDICTION: student ECE is minimised at T=T\*~0.51, and rises at BOTH ends,
> with the T=1.0 end worst (largest |teacher gap|). Equivalently: student ECE is monotone in
> teacher ECE, and monotone in |signed teacher miscalibration|, exactly as on RAF-DB.
> FALSIFIED IF: the student-ECE argmin is not at T\*, or the ordering does not follow teacher ECE."

Three predictions in one paragraph: **P1** argmin at T\* · **P2** monotone in teacher ECE ·
**P3** the T=1.0 end is worst. Verification script `diagnostics/b015_verdict.py`, result
`diagnostics/selection_audit/b015_verdict.json` (`verdict.overall = "CONFIRMED"`).

**The strongest feature of this pre-registration is that FERPlus has the opposite sign:** the
RAF-DB teacher is over-confident, the FERPlus teacher under-confident. The prediction was derived
from RAF-DB and tested in a regime where **the correction acts in the opposite direction**.

---

### A4 · B-017 — human-vote-aligned temperature (T=0.74): two predictions + a mandatory scoring rule

| field | value |
|---|---|
| **artefact** | `ferplus_tjsd_queue.ps1`, lines 38-58 |
| **frozen** | 2026-07-27 12:56:29 |
| **first run started** | `2026-07-27-12-56-47` (**+18 seconds**) |
| **before the result** | ✅ **yes** |
| **outcome** | **P1 FALSIFIED**, **P2 CONFIRMED** (3/3 checkpoints) |

> "PRE-REGISTERED PREDICTION 1 ... student ECE at T=0.74 lands BETWEEN the T=0.26 and T=1.0
> students, preserving the ordering ECE(0.5063) < ECE(0.26) < ECE(0.74) < ECE(1.0)."
> "PRE-REGISTERED PREDICTION 2 ... student JSD is MINIMISED at T=0.74."

Measured @swa: ECE(0.5063)=0.0185 < **ECE(0.74)=0.0344** < ECE(0.26)=0.0587 < ECE(1.0)=0.0783.
So T=0.74 landed **below** T=0.26 → P1 failed. The JSD argmin is at T=0.74 → P2 passed.

**The error was in the pre-registration, not in the law.** In writing P1 I used teacher ECE as a
sign-blind ordering key, even though **I had already documented the direction asymmetry (T4)
myself**. T=0.26 is on the over-confident branch and T=0.74 on the under-confident one; applying
the asymmetry would have predicted exactly this result. The corrected statement of the law:
**student ECE is monotone in |signed gap|, separately within each branch.**

The same artefact also freezes the **mandatory two-axis scoring rule** ("Do NOT score these
students on hard-label ECE alone... a rigged test"), so T7's two-axis form is pre-registered as
well, not a defence added after seeing the result.

---

### A5 · B-016 — the bridge teacher, a two-band decision rule

| field | value |
|---|---|
| **artefact** | `diagnostics/bridge_teacher_check.py`, lines 46-47 (`HEAD_CENTER, RECIPE_CENTER, BAND = 0.015, 0.038, 0.010`) + `diagnostics/P0_teacher_recipe_diff_report.md` (2026-07-20 13:26) |
| **frozen** | 2026-07-20 13:41:12 |
| **teacher training started** | `2026-07-21-13-36-38` (**+23 h 55 min**) |
| **before the result** | ✅ **yes** — the measurement script was written before training of the model it would measure even began |
| **outcome** | ECE 0.0391 → **at the centre of the recipe band**, entirely outside the head band |

⚠️ **`bridge_teacher_check.json` CANNOT be used as evidence.** That file contains the bands but was
written on 21 Jul at 21:59, i.e. after `best.pt` (18:52) — it is output, not pre-registration. The
pre-registration evidence for the bands is **the script itself**.

---

### A6 · B-001/B-005 — the Stage1 dose-response

| field | value |
|---|---|
| **artefact** | `rafdb_p1_temperature_doseresponse_queue.ps1`, line 25 |
| **frozen** | 2026-07-23 10:34 |
| **first grid run** | `2026-07-23-10-35-11` (**+~1 min**) |
| **before the result** | ⚠️ **partly** |

> "Prediction (calibration thesis): student ECE is a U in T with a minimum near T\*=1.34"

**Why "partly":** the T=1.34 point had already been run on its own **before** the grid —
`RAFDB_stage1_tempscale_T1341_halfA_baseline_.../2026-07-21-11-14-32`, the B3 half-split
experiment. So "minimum near T\*=1.34" was not a blind prediction but a generalisation from a known
point. **The shape of the U** (rising at both ends) was blind; **the location of the minimum** was
not. The paper must state this distinction explicitly, otherwise the claim is overreaching.

### A7 · P1 — `logit_std` n=1 → n=3 (2026-07-29) — **CONFIRMED 3/3**

| field | value |
|---|---|
| **artefact** | `rafdb_p1_logit_std_seeds_queue.ps1`, lines 15-42 |
| **frozen** | 2026-07-29 01:23:40 |
| **first run started** | `2026-07-29-01-24-08` (**+28 seconds**) |
| **before the result** | ✅ **yes** |
| **prediction** | P1.1 ΔECE > 0 in all three teachers · P1.2 same sign in 3/3 seeds · P1.3 \|Δacc\|/acc_sd < \|ΔECE\|/ece_sd |
| **if falsified** | the phrase "the most destructive intervention" is withdrawn; if P1.3 fails, the "accuracy alone misleads" framing falls for this row |
| **outcome** | ✅ **P1.1, P1.2 and P1.3 all confirmed** (6 runs finished 2026-07-29 14:06) |

### A8 · P2 — gate:oracle_error n=1 → n=3 + the missing control (2026-07-29) — **PARTLY FALSIFIED (1/3)**

| field | value |
|---|---|
| **artefact** | `rafdb_p2_gate_oracle_seeds_queue.ps1`, lines 15-38 |
| **frozen** | 2026-07-29 01:26:59 |
| **first run started** | `2026-07-29-14-24-13` |
| **before the result** | ✅ **yes** (no run had started at the moment of freezing) |
| **prediction** | P2.1 and P2.2 NULL (\|Δ\| ≤ the control's seed sd) · P2.3 signs inconsistent |
| **if falsified** | the claim "the weighting axis is closed" falls and the paper is reframed |
| **runs** | 5/5 finished (`exit 0`), last run 2026-07-30 01:56:48 |
| **outcome** | ❌ **P2.1 falsified (1.10×)** · ❌ **P2.2 falsified (2.08×)** · ✅ **P2.3 confirmed** |

**Measurement** (@swa, 3 seeds, against a class-weighting-matched control —
`diagnostics/p2_gate_oracle/p2_verdict.md`):

| # | bar (control's seed sd) | measured | ratio | verdict |
|---|---|---|---|---|
| P2.1 Δacc | 0.207 pp | 0.228 pp | 1.10× | ❌ falsified |
| P2.2 ΔECE | 0.0027 | 0.0056 | 2.08× | ❌ falsified |
| P2.3 signs | — | acc `--+`, ECE `+++` | — | ✅ confirmed |

**How to read this verdict — the two axes do not say the same thing.**

- **On the accuracy axis the prediction failed literally but held in spirit.** Bar 0.207 pp,
  measured 0.228 pp: the excess is **0.021 pp**, far below what the design can resolve. On the same
  axis the signs are also inconsistent (`--+`, which is exactly what P2.3 catches). So one **cannot
  say** "the gate changes accuracy"; but because the frozen rule was literally violated, P2.1 still
  counts as falsified and will be reported as such. Loosening the bar afterwards would make the
  pre-registration meaningless.
- **On the calibration axis the prediction genuinely failed.** ΔECE = **+0.0056 ± 0.0040**, 2.08×
  the control's seed sd, with **the same sign in 3/3 seeds**. This is not a null: **even with a
  perfect signal, the gate consistently degrades calibration.**

**The framing was corrected accordingly.** "The weighting axis is closed because it has no effect"
is wrong; the correct statement is **"the weighting axis is closed because even with perfect
information it harms calibration"**. The gate is still dead as a contribution — but because it is
harmful, not because it is neutral. The "no headroom" sentences in the paper will be written to
carry this distinction.

> **The missing control was masking a real harm — the measured justification for the repair.**
> Same runs, same seeds; the only difference is which control they are differenced against:
>
> | control | ΔECE | signs | reading |
> |---|---|---|---|
> | `effective_number` (before P2) | +0.0004 ± 0.0011 | `+-+` | *looks* ECE-neutral |
> | `none` (the clean control P2 produced) | +0.0056 ± 0.0040 | `+++` | degrades calibration |
>
> Because class weighting worsens the control's **own** ECE by 0.0052 (measurement:
> `none − effective_number` = −0.0052 ± 0.0038, n=3), the gate's harm of the same magnitude came
> out near zero in the difference and the signs became mixed. A8's control repair was not a gesture
> of rigour but a correction that changed the result.

> **A8's second purpose — re-differencing the six gate rows — was ONLY 4/8 SATISFIED.**
> Because `kd_common.py` hard-errors on gate + class-weighted CE, **all** gate runs were run with
> `--class-weight-mode none`, yet T5 differenced them against the `effective_number` baseline. P2
> produced the missing control — **but only for the VAE9182 teacher.** Of the 8 gate runs on the
> 400e/SWA@200 budget, 4 (all VAE9182) moved onto the clean control; the 4 rows of stage1 and
> primary (`{stage1, primary} × {mean_logvar, target_logvar}`, seed 42) had no control in their own
> class-weighting mode and were therefore **dropped from T5**, to be reported in the supplementary
> material together with the size of the confound above. Completing them requires 2 teachers × 3
> seeds = **6 runs**; the experiment freeze is in force and they were not launched.
>
> The gate claim does not rest on those 4 rows: `gate:oracle_error` is the upper bound measured
> with a **perfect** signal, against a **clean** control, at **three seeds** — if even perfect
> information brings no gain, weaker signals cannot.

#### A8 completion · P4 — the missing `class_weight_mode=none` control for stage1 + primary (30 Jul 2026)

**This is NOT a prediction declaration but a control completion.** Written before the runs started.

| field | value |
|---|---|
| **artefact** | `rafdb_p4_noclassweight_controls_queue.ps1` |
| **scope** | 2 teachers (stage1, primary) × 3 seeds (42, 1, 43) = **6 runs** |
| **the only thing changed** | `--class-weight-mode none` (`effective_number` in the corresponding baseline); the recipe differs nowhere else — teacher, budget, α, τ and SWA are identical |
| **why** | the clean control produced by A8 was for VAE9182 only; T5's four gate rows (`{stage1, primary} × {mean_logvar, target_logvar}`) fell out of the table for lack of a control in their own class-weighting mode |

**Pre-registration status — stated plainly:** **no new prediction is attached** to these runs.
Whatever comes out, the four gate rows will enter T5 with a clean control and
`diagnostics/paper_tables/section54_numbers.md` B1/B3 will be updated accordingly. We write no
prediction because there is nothing to write: the quantity to be measured is the missing control of
an already reported arm, not a new hypothesis. In the paper these six runs will therefore **not** be
called a "pre-registered prediction"; they will be called a "pre-declared control completion".

**The result-chasing door is closed, with its reason:** which way the result comes out does not
change whether the rows enter the table. All four rows, whether ΔECE turns out positive or negative,
will be written into T5 in full and without a `†` mark. The purpose of the declaration is precisely
to lock this commitment in before the runs.

**Why now, with the freeze in force:** after A8's verdict the gate claim is no longer "neutral" but
**signed harm**, and it currently rests on one teacher — one condition. The paper's dose-response
law is convincing because it holds on two datasets with opposite pathologies; the harm claim
deserves the same treatment. A harm claim resting on a single condition would be exactly the thing
this paper argues against throughout.

**Duration — I measured it wrong twice and got it right on the third attempt; both errors are
recorded.**

1. **The first estimate (≈10.5–11 h) was wrong**, because it was extrapolated from P3's measured
   3.4–3.7 h paired runs — and **P3 was width 0.5**; these are width 1.0.
2. **The second "measurement" was also wrong.** I launched paired runs and took wall-clock over
   9–10 epochs, finding 49.8 s/epoch; then 57.5 s/epoch over 3 epochs sequentially. **Both were
   contaminated by process start-up cost** (556 MB teacher load + cudnn warm-up + dataloader setup,
   ~100 s; divided over 9 epochs that inflates each epoch by ~11 s). Wall-clock over few epochs does
   not measure a rate.
3. **The correct method** is a two-point difference, and the longer the window the better: epoch
   6 → 26, 20 epochs in 7.0 minutes → **21.0 s/epoch → 2.33 h/run**. (A shorter 8-epoch window gave
   21.3 s/epoch; a 1.4% difference, and the long window is taken as authoritative.) This is exactly
   consistent with P2's four sequential runs (2.34/2.29/2.31/2.28 h) — that was the real
   confirmation.

**Correction: my efficiency justification for switching to sequential was wrong.** Stripped of
start-up cost:

| layout | per run | all six runs | strength of evidence | risk |
|---|---|---|---|---|
| paired, workers 8 | ~4.2 h (≈38 s/epoch) | **≈12.7 h** (two concurrent streams, 3+3) | ⚠️ **weak** — *inferred* from tqdm's reported 36 s training + ~2 s validation; because the run was stopped there is **no** long-window wall-clock confirmation | crash radius 2 runs; error 1455 (ERROR_COMMITMENT_LIMIT) **occurred in P2 under exactly this layout** |
| **sequential, workers 12** *(used)* | 2.33 h | **14.0 h** | ✅ **strong** — a two-point wall-clock measurement over 20 epochs, additionally consistent with P2's four independent runs | crash radius 1 run |

So paired was not 2.8 h slower as I claimed but **~1.5 h faster** — except that this 1.5 h advantage
was not measured as robustly as the sequential figure; it is an inference. Sequential is kept
anyway, but now for **the right reason**: on a 14-hour job, changing the layout a second time for a
marginal 1.5 h would throw away the ~15 minutes already done and re-invite a failure mode (1455)
that has **actually occurred once** in this campaign; and `train_rafdb_kd.py` has no `--resume`. The
decision is defensible on **risk**, not on speed; the speed justification is withdrawn.

| field | value |
|---|---|
| **launched** | 2026-07-30 14:32:03, sequential `-Stream S -Workers 12`, `p4_noclassweight_sequential.log` |
| **measured rate** | 21.0 s/epoch (20-epoch window) → 2.33 h/run |
| **finished** | 2026-07-31 04:29:14, **6/6 `exit 0`** (2.29–2.39 h/run, 13.95 h total — the 14.0 h estimate held to within 3 minutes) |
| **outcome** | ✅ the four gate rows entered T5 with a clean control · ⚠️ **the harm claim did not replicate in the other two teachers** |

#### P4's result — the pre-declaration was written for exactly this

The four repaired rows (@swa, against the control in their own class-weighting mode, **all n=1**),
and the bar they are judged against (that teacher's `cw=none` control arm's own ECE seed sd, now
n=3):

| row | ΔECE | bar | ratio | reading |
|---|---|---|---|---|
| stage1 · `gate:mean_logvar` | +0.0000 | 0.0021 | 0.00× | within noise |
| stage1 · `gate:target_logvar` | −0.0028 | 0.0021 | 1.32× | outside noise but **in the opposite direction** (ECE improved) |
| primary · `gate:mean_logvar` | −0.0027 | 0.0033 | 0.80× | within noise |
| primary · `gate:target_logvar` | +0.0019 | 0.0033 | 0.57× | within noise |
| *(for comparison)* vae9182 · `gate:mean_logvar` | +0.0067 | 0.0027 | 2.48× | outside noise, in the harm direction |
| *(for comparison)* vae9182 · `gate:oracle_error` **n=3** | +0.0056 | 0.0027 | 2.08× | outside noise, **3/3 same sign** |

**Verdict: the calibration harm is established only for VAE9182 and does not replicate in the other
two teachers.** The signs of the four are mixed (`+`, `−`, `−`, `+`) and three lie inside their own
control's seed noise. The single exception points the other way. So the sentence I wrote after A8 —
**"even with a perfect signal it consistently degrades calibration"** — **cannot be generalised
across teachers**; what is established is narrower:

> **In a well-calibrated teacher (VAE9182), even with a perfect signal the gate degrades
> calibration (+0.0056, 2.08× the control's seed sd, 3/3 same sign, pre-registered).** In two
> over-confident teachers this **does not replicate** with real learned signals.

**"Did not replicate" does not mean "refuted"** — all four are n=1, and n=1 neither establishes nor
demolishes anything. There is also a scale difference that should not be overlooked: the stage1 and
primary controls' **own** ECE is 0.0745 / 0.0755, **2.7×** that of VAE9182 (0.0278). The same
absolute harm is 7.5% in relative terms there versus 20% for VAE9182 — so the effect may be present
there too and simply remain invisible within a larger and noisier baseline. Separating that requires
n=3 in those two arms (**4 runs**, not launched).

**How the paper will write it:** the harm claim will be given **conditional on a well-calibrated
teacher**; generalising phrases such as "in every teacher" or "consistently" will not be used. The
four rows stand in T5 in full, marked `†` (n=1) — that was the declaration's commitment and it was
honoured even though the result was unfavourable.

> **The paired launch was stopped at epoch 10 and the two half-run directories were deleted** (both
> lacked a `metrics_best.json`, so the ledger was already skipping them; but they had written a
> `best_checkpoint.pth` and the selection audit could have picked up a 10-epoch checkpoint).

#### A8 completion · P5 — attempting to replicate `gate:oracle_error` in stage1 and primary (31 Jul 2026)

**This is a RESOLUTION ATTEMPT, not a prediction.** Written before the runs started.

| field | value |
|---|---|
| **artefact** | `rafdb_p5_oracle_replication_queue.ps1` |
| **scope** | `gate:oracle_error` × {stage1, primary} × {42, 1, 43} = **6 runs** |
| **the only thing changed** | `--gate-enable --gate-uncertainty-source oracle_error`; its control is the same teacher's `class_weight_mode=none` baseline produced by P4, and the recipe differs nowhere else |

**What it tries to separate.** After P4 we have the following: with VAE9182, a perfect-signal gate
worsens ECE by +0.0056 (2.08× the control's seed sd, 3/3 same sign, pre-registered A8); with
stage1/primary, **real learned signals** show nothing at n=1. Two explanations cannot be told apart:
**(a)** the harm is specific to VAE9182, or **(b)** the harm is there too, but because the stage1 and
primary students' own ECE is 0.0745/0.0755 — **2.7×** VAE9182's 0.0278 — the same absolute harm is
7.5% rather than 20% in relative terms and stays invisible inside a noisier baseline.

**⚠️ Design correction: these 6 runs are not the "4 runs" I wrote earlier.** That figure was an
arithmetic error and is recorded here in corrected form. The right number is 6 for two reasons:
stage1 and primary have **no** `oracle_error` run at all (their existing gate rows are `mean_logvar`
and `target_logvar`), so 2 teachers × 3 seeds are entirely new. And **replication requires the same
manipulation**: with the established finding built on the oracle, testing it against real-signal
rows would be comparing apples to oranges — that asymmetry is exactly what made P4's null hard to
interpret. Raising the existing real-signal cells to n=3 is a separate and **different** question
(10 runs); this queue does not ask it.

**Pre-registration status:** no new prediction is attached. The oracle is an **upper bound** — if no
harm appears with perfect information, none can appear with any realisable signal — so this queue
carries no result to be "won".

**DECISION THRESHOLD — written now, not chosen afterwards.** Each arm is measured against its own
teacher's `cw=none` control's **own ECE seed sd** (@swa, paired within seed; bars from P4: stage1
**0.0021**, primary **0.0033**):

| criterion | outcome |
|---|---|
| same sign in 3/3 seeds **and** \|ΔECE\| ≥ 2× its own control's ECE seed sd | **ESTABLISHED** — harm present in that teacher |
| otherwise | **UNRESOLVED** |

**Both outcomes enter the text, and how each will be written is fixed now:**

- **If harm appears:** the claim broadens — *"even with a perfect signal it degrades calibration in
  more than one teacher"* — and the conditioning is removed.
- **If it stays null:** the conditioned claim (*"in a well-calibrated teacher"*) is kept, **and the
  null is written up as a positive finding**: in a teacher that has headroom (i.e. is badly
  calibrated) the gate's harm does not resolve, so the harm is conditional on the teacher's
  calibration starting point — which is **consistent with** the paper's calibration-conditioned
  transfer framing, not in spite of it.

**Estimated duration:** sequential, `--workers 12`, measured 2.33 h/run → **6 × 2.33 ≈ 14.0 h.**
(The ~9.2 h the user expected was for 4 runs; 6 runs take 14.0 h.)

| field | value |
|---|---|
| **declaration frozen** | 2026-07-31 14:14:11 (`rafdb_p5_oracle_replication_queue.ps1` mtime) |
| **first run started** | `2026-07-31-14-14-40` (**+29 seconds**) |
| **before the result** | ✅ **yes** |
| **queue finished** | 2026-08-01 04:12:28, 6/6 exit 0, all 400/400 epochs |
| **outcome** | **0/2 ESTABLISHED — UNRESOLVED in both arms** |

### P5 verdict (the frozen threshold applied literally)

| teacher | ΔECE @swa | signs | bar | 2×bar | \|ΔECE\|/bar | verdict |
|---|---|---|---|---|---|---|
| stage1 | **+0.0015** ± 0.0036 | `+-+` | 0.0021 | 0.0042 | 0.74× | **UNRESOLVED** |
| primary | **+0.0004** ± 0.0053 | `+-+` | 0.0033 | 0.0066 | 0.11× | **UNRESOLVED** |
| *reference: vae9182 (A8/P2)* | *+0.0056* | `+++` | *0.0027* | — | *2.08×* | *ESTABLISHED* |

The rule was an **AND**, and both arms failed **on both conditions**: the signs are not 3/3 (`+-+`),
and the magnitudes are below 2×bar. Not a marginal failure — stage1 sits at 0.74 of the bar, primary
at 0.11. The declared bars agreed with the ones re-measured from the data (stage1 0.0021, primary
0.0033), so the verdict does not depend on the choice of bar.

**The "if it stays null" text written in advance came into force** and is applied as written: the
conditioned claim (*"in a well-calibrated teacher"*) is kept. In addition, the reading committed to
in that same text: the harm is conditional on the teacher's calibration starting point; because the
stage1/primary students' own ECE (0.0745/0.0755) is 2.7× VAE9182's (0.0278), the same absolute harm
does not resolve against that noise floor. The (a)/(b) distinction in the declaration **could not be
separated** — this queue does not select (a); it only shows that it cannot exclude (b).

> ⚠️ **UNRESOLVED ≠ no effect.** The bar is **twice** the arm's own seed noise; an effect below it
> was not measured, which is not the same as being absent. The sentence *"the gate does not degrade
> calibration in stage1 and primary"* **cannot be written** from this data.

**D1's closing rationale will therefore be written in two legs:**
1. **Unconditional:** even with perfect information the gate yields no accuracy gain in **any**
   teacher (Δacc @swa: stage1 −0.22, primary −0.01, vae9182 −0.23 — all three ≤ 0). The closure
   rests mainly on this row, and P5 **strengthened** it by adding two teachers.
2. **Conditional on VAE9182:** the calibration harm was established there only.

Artefacts: `diagnostics/p5_oracle_replication/p5_verdict.{md,json}`,
`diagnostics/p5_oracle_replication_verdict.py`.

---

> **Permanent repair (code).** `class_weight_mode` is now a column in `runs.csv` and **part of the
> pairing key** in `paper_tables.py`. The reason is not only the gate rows: because P2 put a second
> legal control on disk, had the mode not entered the key, every (teacher, seed) cell would have had
> two controls and which one won would have come down to **dictionary order**. The ambiguity no
> longer passes silently; it raises a `RuntimeError`.

---

### A9 · P6 — the τ×T factorial + α modulation: which variable's law is it? (1 Aug 2026)

**The first full-chain pre-registration: declare → commit → tag → run.** All earlier
pre-registrations carry only an mtime plus a run-directory stamp (see the git note at the head of
this file); this declaration was committed before the runs and fixed with the `p6-predeclared` tag —
the first time a commit hash is part of the evidence chain.

| field | value |
|---|---|
| **artefact** | `rafdb_p6_tau_alpha_queue.ps1` (decision rules in the header, verbatim) |
| **scope** | Stage1 · RAF-DB · 3 seeds {42, 1, 43} · **42 new runs** (Grid 1: 18, Grid 2: 24) |
| **the only things changed** | only τ (`--temperature`), α (`--alpha`), T (`--teacher-temperature-scale`); the recipe is taken unchanged from the P1 dose-response queue |
| **reused** | the τ=6 column (T∈{0.85, 1.3406, 1.70} × 3 seeds, verified on disk) and the α=0.3 pair (baseline + tempscale_T134, 3 seeds each) |

**Grid 1 — τ×T (the reduction test).** Two matched T·τ pairs: (τ=3, T=1.70)↔(τ=6, T=0.85) →
5.10 and (τ=6, T=1.70)↔(τ=12, T=0.85) → 10.20.

- **P6.1 (collapse):** student ECE depends on (T,τ) only through the **product T·τ**.
  Decision rule (@swa, paired within seed): for each pair, |mean ΔECE| ≤ 2×bar AND the signs not
  3/3 in agreement → **COLLAPSE CONFIRMED** (for that pair); both pairs 3/3 same sign AND ≥2×bar →
  **COLLAPSE FALSIFIED** (the divergence is itself the finding: ranking information and softening
  are separate channels); anything else → **UNRESOLVED**, reported per pair, with no general claim
  written. **The bar is frozen now: 0.0012** (the ECE seed sd of the stage1/`effective_number`
  control arm @swa, `denominator_table.json`) → 2×bar **0.0024**.

**Grid 2 — α modulation (the listening channel).** Gap(α) := ECE(T=1) − ECE(T=1.3406), within seed.

- **P6.2 (monotonicity):** gap(α) decreases monotonically as α rises — over 5 α points {0.1, 0.3,
  0.5, 0.7, 0.9}, non-increasing at every successive step within each seed; CONFIRMED if it holds
  in **3/3 seeds**.
- **P6.3 (extremes):** gap(0.9) < gap(0.1), strict inequality, in **3/3 seeds**.

**Framing:** both outcomes are publishable; the thresholds will not be chosen afterwards. The runs
fall outside the audit cutoff — they do not enter T8 (the code blocks it), nor T1–T5 (T1/T2 use an
explicit name dictionary; T5's control pool is conditioned on α=0.3 + t_scale=1.0). They will have
their own tables (**T11/T12**). Estimated load 42 × ~2.33 h ≈ 98 h ≈ 2–6 Aug; it neither waits for
nor blocks the paper submission.

| field | value |
|---|---|
| **declaration frozen** | 2026-08-01 14:21:57 (`rafdb_p6_tau_alpha_queue.ps1` mtime) |
| **commit + tag** | `3d9dbee` · 2026-08-01 14:23:31 · tag `p6-predeclared` |
| **first run started** | `2026-08-01-14-23-45` (**+14 s after the commit**) |
| **before the result** | ✅ **yes — and for the first time with three independent stamps:** mtime < commit < run |
| **queue finished** | 2026-08-05 16:16 · **42/42**, all 400/400 epochs, 0 retries |
| **outcome** | **P6.1 COLLAPSE FALSIFIED · P6.2 NOT CONFIRMED (0/3) · P6.3 CONFIRMED (3/3)** |

**VERDICT (6 Aug 2026, after the queue closed at 42/42).** The applier was committed BEFORE
any result was read (`5f78cee`; the key-type fix `18a33ef` also preceded any reading).
Producer: `diagnostics/p6_verdict.py` → `diagnostics/paper_tables/p6_collapse_test.md`
(T11/T12).

- **P6.1 — COLLAPSE FALSIFIED.** In both matched pairs the signs agree 3/3 and the mean |ΔECE|
  exceeds the bar: −0.0391 ± 0.0032 for T·τ=5.10 (**16.30×** 2×bar) and −0.0324 ± 0.0029 for
  T·τ=10.20 (**13.50×**). Student ECE does not reduce to the product T·τ; τ and T are separate
  channels. In the declaration's own words: *the dissociation is itself the finding.*
- **The 2 Aug early reading reproduced BIT-IDENTICALLY.** All six ΔECE values and both pair
  verdicts agree (tolerance 1e-12). The declaration required this; because the decision logic
  is imported from `p6_1_early_reading.py` rather than copied, a copy-drift is structurally
  impossible.
- **P6.2 — NOT CONFIRMED (0/3 seeds).** gap(α) is not monotonically decreasing: in all three
  seeds the α=0.1→0.3 step RISES (+0.0100 / +0.0081 / +0.0055), and in two seeds 0.3→0.5 rises
  as well. The curve is non-monotone, with an **interior maximum near α≈0.5** followed by a
  steep fall.
- **P6.3 — CONFIRMED (3/3 seeds).** gap(0.9) < gap(0.1), strictly in all three: −0.0504 /
  −0.0611 / −0.0613.
- **The endpoints held but the stated reason did not — recorded separately.** The declaration's
  reasoning was that as α rises the student listens to the teacher less, so the intervention's
  effect should **decay** (α is the hard-label weight: `kd_common.py:440`,
  `loss = α·hard + (1−α)·soft`). What happens instead is not decay but a **sign reversal**: the
  gap peaks at +0.0327 at α=0.5 and falls to −0.0352 at α=0.9, i.e. at high α teacher-side
  pre-scaling actively **harms** the student, by a magnitude comparable to its peak benefit.
  P6.3's verdict is CONFIRMED — the rule compares the endpoints, not the path — but the
  predicted mechanism did not occur. Under the pre-registration discipline the verdict and the
  mechanism are reported separately.

> **Scope change (4 Aug 2026, before the data).** A9 was originally scoped to the thesis /
> third study and was not planned for the paper. The external review of 3 Aug 2026
> (`paper_review.md`, Reject→Major) named identification as its first computable gap, and the
> P6 collapse test answers it directly, so it **was brought into the paper**. Only the scope
> changed: the P6.1/P6.2/P6.3 rules and the 0.0012 bar were fixed on 1 Aug under the
> `p6-predeclared` tag, and when this note was written the queue stood at **26/42** with no
> verdict read. The rule was therefore declared before the data; the decision to publish came
> from a reviewer's gap, not from a result.

---

### A10 · R3 — external-review robustness round: a multi-metric inventory (4 Aug 2026)

**The full chain, for the second time: declare → commit → tag → compute.** No metric was
computed before this commit; `robustness_metrics.py`, `tstar_sensitivity.py`,
`jsd_sensitivity.py` and the FERPlus logit cache were all written **after** the declaration.

**Source:** `paper_review.md` identified three computable gaps — a single ECE specification,
an unquantified difference between the NLL fit of T* and the ECE argmin, and a FERPlus JSD
target that had never been tested on the conditional distribution. All three come out of
existing caches: **no training**, the P6 queue is untouched.

#### The declared frame (locked)

- **THERE IS NO SUCCESS CRITERION.** This is a robustness inventory, not a hypothesis test.
  No threshold, no "confirmed/falsified" verdict. Whatever comes out goes into the paper.
- **No computed metric may be withheld.** The list below is closed; a metric that is computed
  but does not appear in the table is a violation.
- **Monotonicity is reported per metric.** Any break is listed explicitly: which pair, which
  seed, which metric. Breaks may not be hidden or dismissed as "noise".
- The metric list, bin counts and slices are frozen **now**, not added after the computation.

#### Scope correction — before computing, by reading the disk

The scope line in the task text (*primary 5 arms · stage1 3 arms · VAE9182 5 arms · FERPlus
3 arms*) matches no structure in the repository. The real dose–response series, measured on
disk:

| series | T points | seeds | runs | cache |
|---|---|---|---|---|
| stage1 | 0.85 · 1.00 · 1.3406 · 1.70 · 2.20 | 42, 1, 43 | 15 | ✅ present (`logits_swa.npz`) |
| vae9182 | 0.85 · 1.00 · 1.3406 · 1.70 · 2.20 | 42, 1, 43 | 15 | ❌ to be built |
| ferplus | 0.26 · 0.5063 · 0.74 · 1.00 | 42, 1, 43 | 12 | ❌ to be built |
| **total** | | | **42** | |

The `primary` teacher **has no dose–response series** — every `tempscale_T*` run belongs to
stage1 or vae9182; primary has only mechanism arms (T5). The mechanism-arm reading does not
match the numbers either (each teacher has 4 arms at n=3). The scope was fixed to this table;
the correction was written **before a single metric was computed**.

#### R3-1 · Multi-metric dose–response (@swa)

Seven columns per run, from that run's own per-sample logit cache:

| metric | specification | source |
|---|---|---|
| NLL | mean, natural log | new |
| Brier | multiclass, full probability vector, one-hot target | new |
| ECE equal-width, 10 bins | on max-prob, first bin closed on the left | `confidence_ece(n_bins=10)` |
| ECE equal-width, 15 bins | *(the campaign's existing specification — reference column)* | `confidence_ece(n_bins=15)` |
| ECE equal-width, 25 bins | | `confidence_ece(n_bins=25)` |
| ECE equal-mass (adaptive), 15 bins | bin edges at confidence quantiles | new |
| Classwise-ECE | unweighted mean of the per-class top-1 ECE, 15 equal-width bins | new |

Equal-width ECE **will not be rewritten**; the existing `confidence_ece` is called (single
source), so the 15-bin column must reproduce the published ECE values exactly, and that is
reported as a verification gate.

Output: `diagnostics/paper_tables/robustness_metrics.{md,json}` — arm × seed raw values, arm
means with sd, a within-seed monotonicity count per metric (in the **9/9** form; 12/12 for
stage1 and vae9182, 9/9 for FERPlus — the real denominator is printed in the table), and the
source file path on every row.

**Cache construction and the device decision (declared).** The 27 missing caches will be
built through the existing audit gate in `student_logit_cache.py`: every write is validated
against that run's independently produced acc/ECE in `selection_audit.json`, and on any
deviation the file is **not written**. Construction will use **CUDA**, not CPU: as measured
in the module's own documentation, CPU carries a ~3e-4 device floor on ECE, a binned
statistic, and the existing 15 stage1 caches were built on CUDA — in a table half built on
CPU and half on CUDA, a 3e-4 difference between arms would be a hardware artefact rather than
a measurement. 7.4 GB is free on the GPU; the inference slows P6 by a few minutes and carries
no memory risk.

> **Correction (4 Aug, still before any metric was read).** The "CUDA everywhere" decision
> above was **wrong for FERPlus, and the gate caught it itself**. When the FERPlus cache was
> attempted on CUDA the audit gate stopped on the first run: accuracy 88.9629 against the
> audit's 88.9312 — a difference of exactly **0.0317 pp = 1/3153**, i.e. one single sample
> changing its prediction. The cause: `ferplus_selection_audit.py` runs on **CPU** by default
> (its own documentation says so), so the published FERPlus numbers are CPU numbers, and a
> CUDA cache would contradict the FERPlus table in the paper.
>
> The correct rule follows from the declaration's own reasoning — the goal was never "the same
> device everywhere" but **each series reproducing its own published audit**. Hence: the RAF-DB
> series on CUDA (their audits are CUDA), the FERPlus series on CPU (its audit is CPU).
> Comparisons are within series anyway; the absolute ECE difference between series is not a
> quantity in this inventory. The batch size was likewise matched to each series' own audit
> (RAF-DB 256, FERPlus 64), because a different summation order moves the last digit.

#### R3-2 · T* sensitivity (four teachers)

One line per teacher: `T*_NLL` (the deployed value) · `argmin-ECE(T)` (continuous, by Brent
on ECE(T)) · the ECE difference at the two points · `|T*_NLL − T*_ECE|`. **There is no
expectation**; whatever the difference is, is what gets written. FERPlus's 0.120/0.113 is
already known, which makes that row a correctness check on the producer as well. Output:
`diagnostics/paper_tables/tstar_sensitivity.{md,json}`.

#### R3-3 · FERPlus JSD sensitivity

Three slices of the evaluation fold: **(a)** all rows (the current result, reference) ·
**(b)** only rows whose vote sum is 10 · **(c)** the strata {6–7, 8–9, 10}. For each slice:
`T*_JSD`, the arm ordering (**is the separation between the ECE-optimal and JSD-optimal
points preserved?**), and n. Both the loss and the survival of the separation get written.
Output: `diagnostics/paper_tables/jsd_sensitivity.{md,json}`.

#### R3-4 · Closing P6 (after 42/42, ~5 Aug)

Once the queue finishes, A9's formal T11/T12 verdict will be applied **with the same producer
as the early reading** and the full sample; P6.1 must reproduce the early reading bit for bit
from the per-run cache. Output: `diagnostics/paper_tables/p6_collapse_test.md`. The scope
change is recorded under A9 above.

| field | value |
|---|---|
| **declaration frozen** | 2026-08-04 00:59:56 |
| **commit + tag** | `0b8ef2f` · 2026-08-04 00:59:56 · tag `r3-predeclared` |
| **computation started** | after the commit (the first producer file did not yet exist in it) |
| **before the result** | ✅ yes — no metric was computed before the commit |
| **outcome** | *(computed 4 Aug; see `paper_tables/robustness_metrics.md`, `tstar_sensitivity.md`, `jsd_sensitivity.md` and T13/T14/T15 in `RESULTS_TABLES.md`)* |

---

### A11 · R3-W1 — the dual-axis caption's "cannot be satisfied at once" claim (6 Aug 2026)

**Why.** In the Round-2 panel review of 5 Aug 2026, seat R3 (Perspective) raised a MAJOR item:
the caption of `fig_ferplus_dual.tex` states *"no arm occupies the lower-left corner: the two
objectives cannot be satisfied at once."* That is an **impossibility claim** resting on a
four-arm grid. The reviewer also named a cheap refutation candidate: distil at the
human-aligned T=0.74, then cross-fit a student-side temperature to repair ECE.

**What is computed.** R0-1's protocol (`student_ts_baseline.py`), **unchanged**: image names
are sha256'd and sorted by hex, first half A / second half B; T_s is fitted on one half by NLL
minimisation and measured on the other, in both directions; the combined row scores each sample
exactly once with the opposite half's T. Only the scope differs — R0-1 applied this to the T=1
arm alone; here it is applied to **all four dose-response arms** (T ∈ {0.26, 0.5063, 0.74,
1.0}), @swa, 3 seeds, on both axes (hard-label ECE and human JSD), same reporting set as
`ferplus_student_jsd`.

**Not a hypothesis test — a caption-adequacy check.** There is no success criterion; no computed
point may be left out of the report, and all four arms are written up.

**Definition of the "lower-left corner", fixed here before any number was seen.** The corner is
formed by the arms' own two best values: `ECE_min` := the lowest student ECE across arms, and
`JSD_min` := the lowest student JSD across arms. A point **occupies** the corner iff
`ECE ≤ ECE_min + bar_ECE` **and** `JSD ≤ JSD_min + bar_JSD`, where each bar = 2× the larger of
the two relevant seed sds.

**Decision rule (three branches, written in advance):**
- If any (arm + student-TS) point occupies the corner → the caption's *"cannot be satisfied at
  once"* is **FALSIFIED for recipes that include post-hoc scaling** and must be rewritten. Which
  arm did it, and by what margin, is reported.
- If none occupies it → the sentence **stands** for this family too; that strengthens rather
  than weakens the caption and is reported as such.
- If a point clears one axis but exceeds the bar on the other → **UNRESOLVED**; reported
  point-by-point, no general claim, and the caption is narrowed to "no *evaluated* arm".

**Scope limit, stated up front.** This check is only possible on FERPlus: RAF-DB has no clean
partition on which to fit a student-side temperature (§5.7's own reasoning). The result is
FERPlus-specific and will be written that way.

**No GPU, no training.** The four arms' @swa logits were already cached in their run
directories (4 Aug, during the R3-3 round); the computation is read-only on CPU.

| field | value |
|---|---|
| **declaration frozen** | 2026-08-06 00:38:04 (this block, before the producer file was written) |
| **commit** | `2d6bed2` · 2026-08-06 00:38:04 — `r3w1_joint_optimum.py` did **not** exist in it |
| **before the result** | ✅ yes — the corner definition and all three branches were written without seeing a single number |
| **outcome** | **CAPTION FALSIFIED** — `paper_tables/r3w1_joint_optimum.md` |

**VERDICT (6 Aug 2026).** The corner: `ECE_min = 0.0185` (T=0.5063 arm), `JSD_min = 0.0536`
(T=0.74 arm). Of the four (arm + student-TS) points, **one** occupies it: the **native T=1 arm
plus student-side TS**, at ECE 0.0203 (inside a 0.0035 bar) and JSD 0.0545 (inside a 0.0010
bar). The caption's *"the two objectives cannot be satisfied at once"* is therefore **not true**
for recipes that include post-hoc scaling, and will be rewritten.

- **The margin is narrow, and is written as such.** The winning point lies *above* the best
  arm's value on both axes (+0.0018 ECE, +0.0009 JSD) and clears the test only by staying
  inside seed noise. The defensible sentence is **"indistinguishable from both optima within
  seed noise"**, not "beats both". That suffices to falsify an impossibility claim — the caption
  says the objectives *cannot* both be met — but it is not a dominance result and will not be
  written as one.
- **The reviewer's own candidate did not pass.** T=0.74+TS clears ECE by +0.0022 but misses JSD
  by −0.0002. The arm that refutes the caption is the **cheapest recipe on the board**: native
  T=1, with no teacher-side intervention at all.
- **An unasked-for and more consequential finding: student-side TS collapses the JSD axis.**
  Before scaling, the four arms span 0.0201 in JSD (0.0536–0.0737); after a single cross-fitted
  student-side scalar they span 0.0005 (0.0540–0.0546) — a **37×** reduction, with all four
  landing on the same value within seed noise. On this dataset, then, almost the entire
  human-alignment difference between pre-scaling arms is a **confidence-scale** effect that one
  student-side scalar reproduces. §5.7 already reported the T=1 case; extending it to all four
  arms makes the pattern — not the single comparison — the finding. This cuts against the
  teacher-side lever, and is reported anyway.
- **R0-1 reproduced bit-identically** (the T=1 row, raw and TS, both axes, three seeds) — the
  split/fit/measure functions are imported from `student_ts_baseline.py`, so the code path is
  literally the same one.

---

## B. Those WITHOUT a pre-registration — will NOT be called "pre-registered" in the paper

### B4 · P3 — capacity × slope (2026-07-29) → **no prediction, but a question + analysis plan**

`rafdb_p3_capacity_slope_queue.ps1` was frozen 2026-07-29 01:28:02 and ran after P2. It contains
**deliberately no prediction**; what was frozen is the question and the **analysis plan**: at which
three temperatures the fit would be made, that `b_w050` would be compared with `b_2248` **over the
same three temperatures** (a 5-point fit against a 3-point fit would confound capacity with fit
support), and that an error bar for the slope would **not be fabricated** from a single seed pair.
The scratch/pretrained confound is also written down before the runs: `b_w050` and `b_2248` differ
in two things at once, and separating them requires a scratch dose-response at 2.248 M (4 runs, not
launched).

**Conclusion: P3 will be reported as exploratory.**

**The runs are finished** (4/4, `exit 0`, 2026-07-30 08:58:50). The analysis plan was applied
literally — `diagnostics/capacity_law_check.py` →
`diagnostics/p5_efficiency/capacity_law_check.{json,md}`, tabulated in `RESULTS_TABLES.md` T10a.

| capacity | init | temperatures | slope b | R² | largest residual | seed-noise envelope |
|---|---|---|---|---|---|---|
| 2.248 M | pretrained | 1.0 / 1.7 / 2.2 | **0.716** | 0.99997 | 0.00057 | ±0.022 |
| 0.712 M | scratch | 1.0 / 1.7 / 2.2 | **0.655** | 0.99996 | 0.00056 | ±0.058 |

Slope difference **−0.061**, the two envelopes summed **±0.080** → **the difference is not
resolvable.**

All three conditions of the frozen plan were honoured:

1. **`b_2248` was re-fitted over the same three temperatures** (the 5-point fit, b=0.714, was
   recorded only and not used in the comparison) — putting 5 points against 3 would confound
   capacity with fit support.
2. **No confidence interval was fabricated for the slope.** w050's T=1.7 and T=2.2 cells are n=2,
   i.e. one degree of freedom. Instead, a **worst-case envelope** was computed by pushing each cell
   mean by one measured seed sd in the direction that moves the slope most; it is labelled "not a
   confidence interval" in both the artefact and the table.
3. **The scratch/pretrained confound is in the open.** `b_w050` is scratch and `b_2248` pretrained —
   the two slopes differ in capacity *and* in initialisation. Separating them requires a scratch
   dose-response at 2.248 M (4 runs, not launched).

**What can be said:** the calibration transfer law also holds for a student 3.16× smaller —
monotone, and the largest residual of either fit (0.00057 / 0.00056) is **3.5–15.3× below** its own
cells' seed sd (sd range 0.0020–0.0087), so the linearity comes from the relationship itself rather
than from landing on three points. The law is **not a large-student artefact.**
*(Note: this originally read "an order of magnitude smaller"; because the ratio against the smallest
cell sd is 3.5×, that quantifier was too strong at the low end and was replaced by the measured
range.)*

**What cannot be said:** "the slope does not change with capacity." The noise envelope does not
resolve the −0.061 difference; the test was not performed and remains **inconclusive**. And in any
case two variables are moving at once (see 3).

> **P3 also exposed a piece of collateral damage (code, permanent repair).** P3's runs are named
> `RAFDB_vae9182_frontier_w050_tempscale_T{170,220}_*` and the ledger places them in the
> `dose_response` family because `t_scale ≠ 1.0`. Since `paper_tables.py`'s T10 cell filter looked
> only for `"frontier" in name`, those four runs **contaminated the `scratch w050` cell**: the cell
> went from n=3 to n=7 and its ECE from 0.0365 to **0.1079 ± 0.0737**, so T10's "capacity axis" span
> **swallowed the very temperature axis it was supposed to be compared against** — the ratio fell
> from 76× to **3×**. No error message appeared. The filter was corrected with a `t_scale == 1.0`
> condition, and a **seed-uniqueness** gate was added per cell (`RuntimeError`), because two runs at
> the same seed in one capacity cell means by definition that a second variable is moving.

### B1 · VICH head isolation → **NONE**

`rafdb_vich_isolation_queue.ps1` (2026-07-22 16:41, runs 2026-07-24 10:48) is **135 lines** and
contains not one prediction or expectation sentence (a `predict|expect|null|hypoth|pre-reg` scan
came back empty). The docstring of `diagnostics/vich_isolation_verdict.py` says "pre-registered null
expectation", but that script's mtime is from today (it was edited in this session) — evidential
value zero.

**Conclusion: the VICH isolation will be reported as exploratory.** The result itself is solid (same
sign in 3/3 seeds, ΔECE +0.0062 ± 0.0015, the VICH head removes 18.6% of the linear head's ECE) —
one simply cannot say "we said so in advance".

### B2 · The gate oracle upper bound → **partial (no numerical prediction)**

`run_rafdb_gate_signal_followup_queue.ps1` (2026-07-20 01:22, run 2026-07-20 08:19) freezes the
design rationale ("the oracle isolates 'is gating itself useful'... upper-bound") but **contains no
numerical bar or falsification condition**. The design is pre-registered, the prediction is not. The
paper may say "pre-registered upper-bound *design*", not "pre-registered prediction".

### B3 · The width frontier → **no prediction, a question**

`rafdb_width_frontier_queue.ps1` (2026-07-28 00:40, first run 05:50) was frozen before the result ✅
but its content is not a prediction, it is a **question**: "is the calibration law student-capacity
dependent, or does a 0.7 M student inherit teacher calibration the same way a 2.2 M one does?"
Because no prediction was written, whatever the outcome we cannot say "we predicted it". (What was
frozen instead is worth more: the confound itself — that the ImageNet weights load only at width
1.0, and that nine runs are therefore needed, was documented before the runs started.)

---

## C. Summary table

| # | pre-registration | artefact | frozen | first run | before? | outcome |
|---|---|---|---|---|---|---|
| A1 | B-007 flat control | `rafdb_p1_vae9182_flatcontrol_queue.ps1` | 24 Jul 18:05:30 | 24 Jul 18:05:50 | ✅ | confirmed |
| A2 | B-010 kill-switch | `rafdb_p3_then_miscal_chain.ps1` | 25 Jul 14:35:43 | 25 Jul 23:19:09 | ✅ | NULL (fired) |
| A3 | B-015 three predictions | `ferplus_dose_response_queue.ps1` | 26 Jul 13:27:26 | 26 Jul 13:27:45 | ✅ | CONFIRMED 3/3 |
| A4 | B-017 P1+P2 | `ferplus_tjsd_queue.ps1` | 27 Jul 12:56:29 | 27 Jul 12:56:47 | ✅ | P1 ✗ · P2 ✓ |
| **A7** | **P1 logit_std seeds** | `rafdb_p1_logit_std_seeds_queue.ps1` | **29 Jul 01:23:40** | **29 Jul 01:24:08** | ✅ **+28 s** | **CONFIRMED 3/3** |
| **A8** | **P2 gate:oracle + control** | `rafdb_p2_gate_oracle_seeds_queue.ps1` | **29 Jul 01:26:59** | **29 Jul 14:24:13** | ✅ | **P2.1 ✗ · P2.2 ✗ · P2.3 ✓** |
| **B4** | **P3 capacity × slope** | `rafdb_p3_capacity_slope_queue.ps1` | **29 Jul 01:28:02** | **30 Jul 01:56:49** | ⚠️ question, no prediction | **exploratory — slope difference unresolved** |
| A5 | B-016 two bands | `diagnostics/bridge_teacher_check.py` | 20 Jul 13:41:12 | 21 Jul 13:36:38 | ✅ | recipe band |
| A6 | B-001 the Stage1 U | `rafdb_p1_temperature_doseresponse_queue.ps1` | 23 Jul 10:34 | 23 Jul 10:35 | ⚠️ partly | confirmed |
| B1 | VICH isolation | — | — | — | ❌ **none** | exploratory |
| B2 | Gate oracle | `run_rafdb_gate_signal_followup_queue.ps1` | 20 Jul 01:22 | 20 Jul 08:19 | ⚠️ design | exploratory |
| B3 | Width frontier | `rafdb_width_frontier_queue.ps1` | 28 Jul 00:40 | 28 Jul 05:50 | ⚠️ question | ongoing |

**The phrase "pre-registered" will be used in the paper only for A1–A5, A7 and A8. A6 will be
described as "partially pre-registered". B1–B4 will be called exploratory.**

> **A8 is a falsified pre-registration, and it will stay that way.** Two of its predictions failed;
> rather than loosening the bars afterwards, the verdict was written as it came, because that is the
> only value a pre-registration has: being measured by the same rule when the prediction does not
> hold. In the paper A8 will be described as "pre-registered and falsified" — and the framing was
> corrected to fit the result (see the *"closed because it harms"* distinction under A8), not the
> result to fit the framing.
