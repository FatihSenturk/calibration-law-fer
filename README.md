# calibration-law-fer

Code, run manifests and pre-declaration records for

> **Teacher-Side Logit Scaling Governs Student Calibration in Knowledge
> Distillation: Dose-Response Evidence from Facial Expression Recognition**
> Muhammed Fatih Şentürk, Gülsüm Zeynep Gürkaş Aydın
> Department of Computer Engineering, Istanbul University-Cerrahpaşa
> *Under review at Neurocomputing.*

The paper's claim is that a teacher's **calibration**, not its accuracy, governs
what a distilled student inherits. This repository holds what is needed to check
that claim from the recorded evidence: the ledger of every finished run, the
frozen selection audit, the analysis scripts that turn them into the paper's
tables, and the pre-declarations that fixed each decision rule before its runs
were launched.

**Not included:** datasets, model checkpoints, `results/` run directories, raw
training logs, and the manuscript sources. See [Data](#data) and
[PROVENANCE.md](PROVENANCE.md).

**Which version this is.** This snapshot corresponds to the manuscript currently
under review; the submitted version will be tagged, and a DOI minted from that
tag on the day of submission.

---

## What can be reproduced, and at what cost

| level | what you get | what you need |
|---|---|---|
| **1. Tables and numbers** | every table and quoted number in the paper | this repository + Python. **No GPU, no dataset, no checkpoint.** |
| **2. Figures** | the paper's figure PDFs, regenerated and gated | as above, plus `PyMuPDF` |
| **3. Re-running an experiment** | a new run of any arm | a GPU, the datasets, and a teacher checkpoint (available on request) |

Level 1 works because the evidence is committed, not just the code: `runs.csv`
carries one row per finished run with every field derived from that run's own
artefacts, and `diagnostics/selection_audit/` carries the frozen N=131 audit set
quoted in the abstract.

### Level 1 — regenerate the tables

```
python -m venv .venv && .venv\Scripts\activate     # Windows
pip install -r requirements.txt

python diagnostics/paper_tables.py                 # -> diagnostics/paper_tables/RESULTS_TABLES.{md,json}
python diagnostics/table_diff_gate.py              # verifies the result cell-by-cell vs. the accepted baseline
```

`table_diff_gate.py` is the check that matters: it compares the freshly
generated tables against the committed baseline and reports any drifted cell. A
clean run means the tables in the paper and the tables this code produces are
the same tables.

### Level 2 — regenerate the figures

```
python diagnostics/export_paper_figures.py         # -> paper/figures/*.pdf (directory created if absent)
python diagnostics/verify_paper_figures.py         # hard gate: vector-only, TrueType, >= 7 pt, single page
```

Figure binaries are deliberately **not** committed — they are outputs, and the
gate above is what guarantees they are correct.

---

## Output → producing script

Everything below is Level 1 (CPU, no data) unless marked otherwise.
`D` = `diagnostics/`.

### Main tables

| output | script |
|---|---|
| `D/paper_tables/RESULTS_TABLES.{md,json}` (T1–T10) | `D/paper_tables.py` |
| `D/table_diff_gate/last_diff.md` (the cell-by-cell gate) | `D/table_diff_gate.py` |
| `D/paper_tables/t5_pairing_diff.*` (T5 pairing) | `D/t5_pairing_diff.py` |
| `D/paper_tables/denominator_table.*` (denominator conventions, seed-sd bars) | `D/denominator_table.py` |
| `D/paper_tables/section54_numbers.*` (§5.4) | `D/section54_numbers.py` |
| `runs.csv` (the run ledger itself) | `D/build_runs_ledger.py` — **needs the run directories** |

### Statistics and calibration analysis

| output | script |
|---|---|
| `D/paper_tables/inferential_tests.*` (§5.1 paired *t*, *d_z*, Holm) | `D/inferential_tests.py` |
| `D/paper_tables/headroom_review.*` (Eq. 8 headroom, three teachers) | `D/headroom_review.py` |
| `D/paper_tables/student_ts_baseline.*` (§5.6, post-hoc student scaling) | `D/student_ts_baseline.py` |
| `D/paper_tables/tstar_stability.*` (T\* split-half stability) | `D/tstar_stability.py` |
| `D/teacher_temperature_scaling/` (teacher T\* fits) | `D/teacher_temperature_scaling_fit.py` — **needs teacher checkpoints** |
| `D/seed_variance/` (seed-variance bars) | `D/seed_variance_ece.py` |
| `D/rafdb_calibration_backfill/` (ECE/MCE backfill, bin sensitivity) | `D/rafdb_calibration_backfill.py` |
| — the sd convention used throughout (sample sd, *n*−1) | `D/stats_convention.py` |

### Selection audit (§4 m6)

| output | script |
|---|---|
| `D/selection_audit/selection_audit.csv` (frozen, N=131) | `D/selection_audit_table.py` — cutoff frozen inside; **raises if the set drifts** |
| `D/selection_audit/selection_gain.json` (order-statistic estimate) | `D/selection_gain_estimator.py` |
| `D/paper_tables/order_stat_trend.*` (last-*K* window, detrended) | `D/order_stat_trend.py` |
| `D/selection_audit/selection_robustness.json` | `D/selection_robustness.py` |
| `D/selection_audit/selection_optimism_headline.json` | `D/selection_optimism_headline.py` |
| `D/selection_audit/ferplus_selection_audit.csv` (replication) | `D/ferplus_selection_audit.py` |

### Pre-declared verdicts

| output | script |
|---|---|
| `D/p2_gate_oracle/p2_verdict.{json,md}` (B2 oracle-gate diagnosis) | `D/p2_gate_oracle_verdict.py` |
| `D/p5_oracle_replication/` (P5 replication verdict) | `D/p5_oracle_replication_verdict.py` |
| `D/vich_isolation/vich_isolation_verdict.json` (B1 head isolation) | `D/vich_isolation_verdict.py` |
| `D/adaptive_t_headroom/` (adaptive-T headroom) | `D/adaptive_t_headroom_table.py` |

### Mechanisms, efficiency, FERPlus

| output | script |
|---|---|
| `D/paper_tables/mechanism_specs.*` (appendix spec table, machine-generated from each run's own `run_args.json`) | `D/mechanism_specs.py` |
| `D/paper_tables/mechanism_diagnostic.json` | `D/mechanism_diagnostic_figure.py` |
| `D/p5_efficiency/latency_benchmark.{csv,json}` | `D/latency_benchmark.py` — **needs checkpoints + a device** |
| `D/p5_efficiency/` (efficiency frontier, capacity law) | `D/efficiency_frontier.py`, `D/capacity_law_check.py`, `D/p5_efficiency_frontier.py` |
| `D/c4_efficiency_table/` | `D/c4_efficiency_table.py` |
| `D/ferplus_jsd/` (human-vote JSD, teacher/student grids) | `D/ferplus_human_vote_jsd.py`, `D/ferplus_student_jsd.py`, `D/ferplus_teacher_signed_grid.py` |
| `D/teacher_ece_grid/` | `D/teacher_ece_grid.py` — **needs teacher checkpoints** |

### Figures

| output | script |
|---|---|
| `paper/figures/*.pdf` (all figures, journal styling) | `D/export_paper_figures.py` |
| the figure gate (vector / fonts / type size / no in-figure title) | `D/verify_paper_figures.py` |
| individual producers | `D/reliability_diagram.py`, `D/perclass_calibration.py`, `D/vote_examples_figure.py`, `D/selection_distribution_figure.py`, `D/p1_two_teacher_overlay.py`, `D/p1_signed_miscalibration_overlay.py`, `D/two_dataset_overlay.py`, `D/p5_frontier_figure.py`, `D/ferplus_dual_axis_figure.py`, `D/graphical_abstract.py` |

### Training (Level 3 — GPU + data + checkpoints)

| what | entry point |
|---|---|
| teacher training | `main_encoder.py --c <config in configs/>` |
| RAF-DB distillation | `train_rafdb_kd.py` |
| AffectNet+ / FERPlus distillation | `train_affectnetplus_kd.py`, `train_ferplus_kd.py` |
| the exact command line of every published run | the `*.ps1` queue at the repository root named by the matching block in `diagnostics/PREREGISTRATIONS.md` |

**What Level 3 costs, measured.** The RAF-DB campaign in this repository is
**172 finished student runs = 575 GPU-hours** (mean 3.35 h/run on one RTX 5070;
runs executed two-at-a-time cost ~1.8× per run, which is why the mean exceeds the
~2.2 h a solo 400-epoch run takes), plus **16 teacher trainings = 49 GPU-hours**.
Reproducing a *single* arm is cheap; reproducing the campaign is not.

**What is deliberately not published, and why.**

| not here | why | on request |
|---|---|---|
| run directories under `results/` (checkpoints, per-epoch logs, confusion matrices) | size — hundreds of GB | yes |
| teacher checkpoints | size | yes |
| the per-run raw outputs under `results/` | size | yes |
| the datasets (RAF-DB, FERPlus) | licensed by their owners, not ours to redistribute | obtain from the original providers |

The cached model outputs under `diagnostics/` **are** included (5.3 MB in total): they let
you re-derive the joint-optimum, robustness, selection-gain and FERPlus-JSD tables without
any run directory. They are **model outputs computed on the validation split, not
redistributed dataset content** — no image, label or annotation from RAF-DB or FERPlus is
republished here.

Three groups make up that total.

| group | size | what it is |
|---|---|---|
| `diagnostics/ferplus_jsd/`, `diagnostics/teacher_ece_grid/` | 554 KB | four teacher/validation logit caches, here from the start |
| `diagnostics/student_logits/` | 3.4 MB | 42 student logit caches, added 8 Aug 2026 |
| `diagnostics/epoch_curves.npz` | 1.2 MB | per-epoch validation accuracy and loss — 199 runs, 76,700 epochs, added 9 Aug 2026 |

The logit caches each hold one logit matrix (3068 rows for RAF-DB, 3153 for FERPlus) and
its label vector. `epoch_curves.npz` holds three arrays per run — epoch number, validation
accuracy at that epoch, validation loss at that epoch. There are no images, no vote
distributions and no file names in any of them.

The **42 student caches** were added for one reason: without them,
`diagnostics/robustness_metrics.py` (the seven-metric dose–response inventory) and
`diagnostics/r3w1_joint_optimum.py` (the FERPlus joint-optimum test) read
`results/unified_students/`, so those two tables could **not** be reproduced here. They are
**byte copies**
of the caches written inside each run directory, not repackaged: the collector
(`diagnostics/publish_student_logits.py`) hashes source and copy separately and stops
unless the two sha256 digests are equal. `diagnostics/student_logits/MANIFEST.json` records
for each file which run directory it came from, its sha256, and the accuracy and ECE stored
in its own metadata — so the copy's provenance is checkable, not asserted.

One consequence of insisting on byte copies is stated rather than hidden: each `.npz` still
carries, inside its own `meta` field, the **absolute path of the run directory it was
written in** on the machine that trained it. It was not scrubbed, because scrubbing means
repacking, and repacking would void the sha256 identity that makes the copy provable in the
first place. `MANIFEST.json` publishes the same provenance in repository-relative form
(`results/unified_students/<run>/<timestamp>`), so nothing here depends on reading the
embedded string. Every one of the 42 shares the same root, `…\poster-var\results`: a local
directory layout and nothing else, with no user name and no credential in it.

`epoch_curves.npz` was written by `diagnostics/publish_epoch_curves.py` and is **not** a byte
copy — it is a repack, because the source is ten-column CSV and only three columns are used.
That is why its arrays are `float64` rather than `float32`, and the reason is worth stating
because it is not obvious: the training logs record `val_acc` at full double precision, and
rounding to `float32` makes distinct epoch accuracies compare equal. `argmax` then picks an
earlier epoch, and `argmax_in_last_K` moved by 1.5–2 points before the dtype was fixed. With
`float64` both consumers reproduce their previously published numbers exactly. A repack is
only safe once you have checked that it is.

**So please do not shrink this file.** `float32` halves it to 761 KB and the two tables it
feeds stop reproducing — that was measured, not feared.

This is the honest consequence: **a reader who clones this repository and runs the
analysis scripts gets Level 1 and Level 2, not Level 3.** Level 1 works precisely
because the evidence that the tables read — `runs.csv`, the frozen audit set, the
cached `paper_tables/` artefacts — is committed here rather than being regenerated
from the raw runs. Scripts that do reach into `results/` (the ledger builder, the
audit measurer, the queue generator) are included for inspection and will not run
end-to-end without the run directories; they are marked Level 3 above.

---

## Pre-declaration records

`diagnostics/PREREGISTRATIONS.md` is the campaign's central discipline, and the
reason several results in the paper are reported as null rather than quietly
dropped. The rule was **declare → commit → tag → launch**: before a queue of
runs started, its prediction *and* its decision rule were written down,
committed, and tagged. Nothing in the rule could then be adjusted after seeing a
result — and where a rule turned out to be looser than its declaration, it was
tightened rather than relaxed (the A2 kill-switch is the worked example).

Read it together with:

- `diagnostics/preregistration_blocks.csv` — a **human-authored declaration** of
  experimental intent, not something inferred from the data. Its header says so.
- `diagnostics/claims.md` — the paper's claim inventory and what backs each one.
- `PROVENANCE.md` — the tag hashes and dates from the working repository. This
  repository has a fresh single-commit history, so the timestamps that carry
  evidential weight are recorded there. It also states plainly what that record
  can and cannot prove.

Dates inside `PREREGISTRATIONS.md` are the declaration dates; where a
declaration precedes its runs, the corresponding tag in `PROVENANCE.md` is the
corroboration.

### A note on language

This campaign was conducted in Turkish, and its records were written in Turkish.
Everything a reader needs in order to follow the evidence is in English:

- **`diagnostics/PREREGISTRATIONS.md`** — translated for this release. The
  translation changes wording only; every date, artefact path, line number,
  threshold and measured value is carried over unchanged, and the Turkish
  original is retained in the private working repository.
- **All generated tables** — `RESULTS_TABLES.md` and every other output under
  `diagnostics/paper_tables/`, `p2_gate_oracle/`, `p5_oracle_replication/`,
  `p5_efficiency/`, plus `diagnostics/selection_audit/README.md`. These are
  produced by the scripts listed above, so their English lives in the producers
  rather than in a hand-edited copy: regenerating them reproduces it.
- **`diagnostics/claims.md`** — written in English from the start.

Left in Turkish on purpose: `BULGULAR.md`, `METHODS_DATA.md`,
`diagnostics/DIAGNOSTIC_REPORT.md` and `diagnostics/reports/` are the original
laboratory records, included verbatim rather than rewritten, because their value
is precisely that they were not written for an audience. Many source comments
are Turkish for the same reason.

---

## Environment

Everything here was run on **Python 3.13.10**, **PyTorch 2.10.0 (CUDA 12.8)**,
Windows 11, on a single NVIDIA RTX 5070 with an AMD Ryzen 9 7950X. Versions are
pinned in `requirements.txt`; the analysis layer needs only its CPU-only block.

Run scripts from the repository root — each resolves its own paths relative to
its own location. Scripts that read run artefacts expect them under `results/`,
which is not distributed; those are marked above.

---

## Data

**No dataset is redistributed here.** The paper uses two, each obtained from its
maintainers under their own terms:

- **RAF-DB** — <http://www.whdeng.cn/raf/model1.html> (request form, academic use)
- **FERPlus** — <https://github.com/microsoft/FERPlus> (labels; the images come
  from the FER2013 Kaggle release)

AffectNet is **not** needed; the arms that used it were removed before
publication (see [Scope](#scope)). One filename still points the wrong way:
`configs/RAFDB_teacher_affectnet_recipe.yaml` trains a **RAF-DB** teacher — it
only borrows AffectNet's augmentation recipe (`transforms_name: QCS-rafdb`) and
starts from no AffectNet weights (`pretrained_local: ~`).

`configs/FERPlus_majority_metadata.csv` is the derived label file for the strict
majority split used in the paper — a hard label is kept only when one emotion
holds **more than 50%** of the cleaned votes, which makes ties structurally
impossible. It is built from the public FER+ vote file by
`tools/build_ferplus_majority_metadata.py` and contains no image data.

Model checkpoints are excluded for size and are available on request from the
corresponding author.

**Where the config files expect your copy.** Because the datasets are licensed to
their owners and are not ours to redistribute, no config in `configs/` can point at
a real directory in this repository. Every dataset path is therefore written as the
placeholder `<DATASET_ROOT>` — **the directory holding your own copies of the image
sets** — for example `train_root: <DATASET_ROOT>/AffectNet+` and
`metadata: <DATASET_ROOT>/FERPlus_processed_metadata.csv`. A second placeholder,
`<CHECKPOINT_ROOT>`, marks **the directory holding locally pre-trained backbone
weights**, and appears only in the `pretrained_local:` field, e.g.
`pretrained_local: <CHECKPOINT_ROOT>/best.pt`. The two are separate because they are
separate things: a checkpoint root is not a dataset root, and on most machines they do
not live under the same parent. **Replace both with the paths to your own copies before
running anything at Level 3.** Configs whose data path is already repo-relative
(`train_root: data/rafdb_aligned`) are left as they are — nothing to substitute there,
you just place your copy under `data/`. The placeholder is
deliberate rather than a relative path that happens to resolve: a config that
silently points at an empty `data/` directory fails later and less clearly than one
that states outright that a path is required. Level 1 (regenerating every table and
number in the paper) needs none of this — it reads only the artefacts committed here.

---

## Scope

Every file here should be able to produce a table, a figure or a declared claim
in the paper. Material that could not be tied to one was removed before
publication rather than left for a reader to sort through — 111 files, 4.3 MB,
about half the original size:

- a parallel line of work on **AffectNet / AffectNet+** (launchers, configs,
  loader, cache and evaluation tools). AffectNet appears zero times in the
  paper's records and is not needed for anything here.
- **pre-campaign FERPlus arms** and their two superseded label constructions
  (`FERPlus_Created_metadata.csv`, `FERPlus_processed_metadata.csv`, 4.0 MB
  between them). The paper uses the strict-majority
  `FERPlus_majority_metadata.csv` only.
- **earlier-project configs** (`RAFDB_baseline`, `RAFDB_posterv2`, `RAFDB_var`,
  `FerPlus`, `FerPlus_posterv2`), superseded by the `*_recipe` / `*_vich_*`
  configs the paper uses.
- **Phase-0 / "unified" era launchers and reporting tools**, replaced by the
  `diagnostics/` layer above.

Two consequences worth stating. The Turkish laboratory records
(`BULGULAR.md`, `diagnostics/DIAGNOSTIC_REPORT.md`) still discuss some of the
removed material — they are historical logs and were not rewritten to match.
And `tools/build_repro_export.py` still lists a few removed filenames in its
content declaration: it is reproduced here as the tool that produced the
snapshot, so editing it would make it no longer that tool. See
[PROVENANCE.md](PROVENANCE.md).

---

## Licence

MIT — see [LICENSE](LICENSE). The teacher backbone under `trails/` and the
optimiser under `trials/` are derived from third-party projects and remain under
their own terms; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
