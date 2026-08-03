# R3-2 — T* fitting-criterion sensitivity (NLL vs. ECE argmin)

Producer: `diagnostics/tstar_sensitivity.py` · `T*_NLL` is the deployed fit (`student_ts_baseline.fit_ts`, the same function the campaign uses) · `T*_ECE` is the continuous argmin of ECE(T) found by bounded Brent over the **same** log-space interval [0.05, 10], so any difference is the criterion's and not the search box's · cached teacher logits, no forward pass. Pre-declared in `PREREGISTRATIONS.md` A10 (R3-2): **no expectation, no threshold** — the difference is reported as it falls.

| teacher | n | T\*_NLL | T\*_ECE | **\|ΔT\*\|** | ECE @T=1 | ECE @T\*_NLL | ECE @T\*_ECE | **ΔECE (criterion cost)** | ECE removed by TS | ratio | dense-grid check |
|---|---|---|---|---|---|---|---|---|---|---|---|
| stage1 | 3068 | 1.3494 | 1.3198 | **0.0296** | 0.03780 | 0.01582 | 0.01428 | **+0.00154** | +0.02198 | 14× | **LOCAL-MIN** (grid 0.01417 @T=1.335) |
| primary | 3068 | 1.2613 | 1.2441 | **0.0172** | 0.03958 | 0.01972 | 0.01827 | **+0.00146** | +0.01985 | 14× | ok (T=1.240) |
| vae9182 | 3068 | 0.9831 | 1.0572 | **0.0741** | 0.01355 | 0.01457 | 0.01025 | **+0.00432** | -0.00102 | **n/a — TS adds ECE** | ok (T=1.055) |
| ferplus | 3153 | 0.5064 | 0.4530 | **0.0533** | 0.12823 | 0.01564 | 0.00718 | **+0.00846** | +0.11259 | 13× | ok (T=0.455) |

**Reported as it fell.** The two criteria disagree by at most **0.0741** in T across the four teachers, and choosing the NLL optimum instead of the ECE optimum costs at most **0.00846** in ECE. In the 3 teachers where temperature scaling removes ECE at all, that cost is 13–14× smaller than the ECE the scaling removes (stage1 14×, primary 14×, ferplus 13×), so for those teachers the reported calibration gains do not depend on which criterion locates T*.

> ⚠️ **vae9182 is the exception, and it is not a rounding artefact.** This teacher is already at its calibration floor (ECE 0.01355 at T=1), and the NLL-fitted T*=0.9831 makes its ECE **worse**, not better (0.01355 → 0.01457, +0.00102). The ECE criterion instead finds T*=1.0572 — on the other side of 1 — and does reduce ECE to 0.01025. So the two criteria do not merely differ in magnitude here: they disagree about the **direction** of the correction. The sentence 'the fitting criterion does not matter' cannot be written for vae9182.

> ⚠️ **Non-smooth surface.** ECE(T) is a binned statistic and is piecewise constant in places, so the continuous optimiser can settle away from the global minimum. Rows marked LOCAL-MIN are exactly those; the dense-grid value (step 0.005, 0.1–3.0) is printed beside them and is the one to quote for those teachers.

