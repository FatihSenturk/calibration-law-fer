# Third-party notices

The MIT licence in `LICENSE` covers the code written for this paper. The
directories below contain code **derived from other projects** and are included
so that the teacher network can be constructed and the published runs can be
reproduced. They remain the work of their original authors, under their original
terms. Where files were modified for this work, the modification is stated.

## `trails/posterv2/` — POSTER++ teacher backbone

The teacher is POSTER++ (Mao et al., *POSTER++: A simpler and stronger facial
expression recognition network*), whose reference implementation is public at
<https://github.com/talented-Q/POSTER_V2>.

| file | origin | modified for this work |
|---|---|---|
| `PosterV2_7cls.py` | POSTER++ | yes — pretrained-backbone path made relative; head selection (`vae_head` / `vich_head`) routed through the config |
| `vit_vae_model.py` | POSTER++, itself derived from `timm`'s `vision_transformer.py` by Ross Wightman (Apache-2.0) — stated in the file header | yes — `VaeClassifier` / `VICHClassifier` variational heads added (these are this paper's contribution to the file) |
| `ir50.py` | ArcFace / InsightFace-lineage IR-50 backbone as vendored by POSTER++ | no — kept verbatim, including the original author's commented-out scratch code |
| `mobilefacenet.py` | MobileFaceNet as vendored by POSTER++ | no |
| `matrix.py` | POSTER++ | no |

## `trials/sam.py` — Sharpness-Aware Minimization

A compact reimplementation of SAM (Foret et al., ICLR 2021), following the
widely used reference implementation at <https://github.com/davda54/sam>
(MIT). Used only by the FERPlus teacher runs (`train_encoder_sam.py`).

## `models/mobilenetv2_plus.py` — student

Written for this work. It composes standard published blocks — MobileNetV2
inverted residuals (Sandler et al., CVPR 2018) and ECA channel attention
(Wang et al., CVPR 2020) — and its variational classification head (VICH) is
this paper's own.

## Runtime dependencies

`torch`, `torchvision`, `timm`, `thop`, `numpy`, `scipy`, `pandas`,
`scikit-learn`, `matplotlib`, `PyYAML`, `pillow`, `opencv-python`, `tqdm`,
`PyMuPDF` — each under its own licence, installed from PyPI, not vendored here.

## Datasets

RAF-DB, FERPlus and AffectNet are **not** redistributed in this repository.
Each is obtained from its maintainers under that maintainer's terms; see
"Data" in `README.md`.
