"""N13 dogrulama — bugunun hatalarini GERI KOYUP denetcinin yakaladigini gosterir.

NEDEN AYRI BETIK. "Denetci calisiyor" iddiasi ancak bilinen hatalar geri konup yakalandiginda
kanitlanir. Bu betik makalenin bir KOPYASINI olusturur (Drive'daki kaynaga DOKUNMAZ), her
hatayi tek tek enjekte eder, `number_ledger.build()`u kopyaya karsi kosar ve beklenen ihlal
sinifinin ciktigini dogrular. Bag hatasi (r=0.724) makalede degil DEFTERDE oldugu icin orada
beyanin kendisi bozulur.

Kullanim: python diagnostics/check_numbers_selftest.py --paper-root "<...>/paper" [--work <dir>]
Cikis: 0 = butun senaryolar yakalandi · 1 = en az biri KACIRILDI
"""
import argparse
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "diagnostics"))

import number_ledger as NL  # noqa: E402

# (ad, dosya, [(eski, yeni)], beklenen ihlal sinifi, beklenen kalem sayisi)
PAPER_CASES = [
    ("tab_selection ECE sutunu bayat (0.0631 / 0.0606->0.0608 / 0.0274->0.0273)",
     "tables/tab_selection.tex",
     [("& 0.0627 \\\\", "& 0.0631 \\\\"), ("& 0.0606 \\\\", "& 0.0608 \\\\"),
      ("\\textbf{0.0274}", "\\textbf{0.0273}")],
     "rounding_mismatch", 3),
    ("tab_selection ogrenci dogrulugu bayat (89.75 -> 89.74)",
     "tables/tab_selection.tex", [("$89.75 \\pm 0.08$", "$89.74 \\pm 0.08$")],
     "rounding_mismatch", 1),
    ("tab_collapse turetilmis oran bozuk (16.3 -> 18.0)",
     "tables/tab_collapse.tex", [("$16.3\\times$", "$18.0\\times$")],
     "derived_mismatch", 1),
    ("§5.7 cokus carpani 40x geri kondu (37 yerine)",
     "sections/05_results_discussion.tex",
     [("a $37\\times$ collapse", "a $40\\times$ collapse")],
     "printed_not_found_at_location", 1),
    ("tab_pooled'a kayitsiz bir sayi eklendi",
     "tables/tab_pooled.tex", [("$+0.930$", "$+0.930$ & $+0.111$")],
     "unregistered", 1),
]


def apply_edits(work, rel, edits):
    p = work / rel
    s = p.read_text(encoding="utf-8")
    for old, new in edits:
        if old not in s:
            raise RuntimeError(f"enjeksiyon hedefi bulunamadi: {rel}: {old!r}")
        s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")


def run(work):
    payload, _d = NL.build(str(work))
    kinds = [p["kind"] for p in payload["problems"]]
    return payload, kinds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper-root", required=True)
    ap.add_argument("--work", default=None)
    args, _unknown = ap.parse_known_args()
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")

    base = Path(args.work or tempfile.mkdtemp(prefix="n13_selftest_"))
    src = Path(args.paper_root)
    rows = []

    # --- 0. temiz taban
    clean = base / "clean"
    if clean.exists():
        shutil.rmtree(clean)
    shutil.copytree(src, clean, ignore=shutil.ignore_patterns(
        "*.pdf", "*.aux", "*.log", "*.fls", "*.fdb_latexmk", "build", "arsiv", "submission",
        "figures", "figures_em*", "*.bbl", "*.blg", "*.out", "*.spl", "*.synctex.gz"))
    p0, k0 = run(clean)
    base_unreg = len(p0["unbound"])
    rows.append(("(taban) temiz kopya", "-", 0, len(k0), base_unreg,
                 "GECTI" if not k0 else "TABAN KIRLI"))
    ok = not k0

    for name, rel, edits, want, n_want in PAPER_CASES:
        w = base / ("case_" + str(len(rows)))
        if w.exists():
            shutil.rmtree(w)
        shutil.copytree(clean, w)
        apply_edits(w, rel, edits)
        pl, kinds = run(w)
        if want == "unregistered":
            got = len(pl["unbound"]) - base_unreg
        else:
            got = kinds.count(want)
        good = got >= n_want
        ok &= good
        rows.append((name, want, n_want, got, len(pl["unbound"]),
                     "YAKALANDI" if good else "KACIRILDI"))

    # --- bag hatasi: sayi dogru, artefakt dogru, BAG yanlis (r=0.724 vakasi)
    saved = dict(NL.PROSE[0])
    NL.PROSE[0]["path"] = "entropy_correlation.T074.pearson"
    pl, kinds = run(clean)
    got = kinds.count("unresolved_path") + kinds.count("printed_not_found_at_location")
    good = got >= 1
    ok &= good
    rows.append(("r=0.724 bagi T=1 yerine T=0.74 koluna kuruldu (DEFTER bozuldu)",
                 "unresolved_path / printed_not_found_at_location", 1, got,
                 len(pl["unbound"]), "YAKALANDI" if good else "KACIRILDI"))
    NL.PROSE[0].update(saved)

    # --- bayat alan: bagli alan artefaktta yok
    saved_b = dict(NL.BINDINGS[0])
    NL.BINDINGS[0]["path"] = NL.BINDINGS[0]["path"] + "_SILINDI"
    pl, kinds = run(clean)
    got = kinds.count("unresolved_path")
    good = got >= 1
    ok &= good
    rows.append(("bagli alan artefaktta yok (bayatlik)", "unresolved_path", 1, got,
                 len(pl["unbound"]), "YAKALANDI" if good else "KACIRILDI"))
    NL.BINDINGS[0].update(saved_b)

    w = max(len(r[0]) for r in rows)
    print(f"\n{'senaryo'.ljust(w)}  {'beklenen sinif':46s} bek  bulunan  kayitsiz  sonuc")
    for r in rows:
        print(f"{r[0].ljust(w)}  {r[1][:46]:46s} {r[2]:>3}  {r[3]:>7}  {r[4]:>8}  {r[5]}")
    print(f"\nSONUC: {'HEPSI YAKALANDI' if ok else 'EN AZ BIRI KACIRILDI'} "
          f"· calisma dizini {base}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
