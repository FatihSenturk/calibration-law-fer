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
    # --- N14 (17 Agu): bu turda BAGLANAN sayilar da geri konup denenmeli. Bir bag ancak
    # bozuldugunda yakalanabiliyorsa kurulmustur; kurulup denenmemis bag, kurulmamis bagdir.
    ("§3.2 olcut maliyeti orani '13--15' yazildi (13--14 yerine)",
     "sections/03_methodology.tex", [("$13$--$14$", "$13$--$15$")],
     "printed_not_found_at_location", 1),
    ("tab_pooled Pearson sutunu bayat (+0.930 -> +0.931)",
     "tables/tab_pooled.tex", [("$+0.930$", "$+0.931$")], "rounding_mismatch", 1),
    ("tab_selection_audit FERPlus satiri bayat (+0.50 -> +0.51)",
     "tables/tab_selection_audit.tex", [("$+0.50 \\pm 0.21$", "$+0.51 \\pm 0.21$")],
     "rounding_mismatch", 1),
    # --- N17 (18 Agu): son sekiz kayitsizin bagi. Kurulup denenmemis bag, kurulmamis bagdir.
    ("app_argmin uzlasi sayaci bayat (6/7 -> 5/7)",
     "supplementary.tex", [("& $6/7$ &", "& $5/7$ &")], "rounding_mismatch", 1),
    ("app_argmin FERPlus NLL istisnasi bayat (0.74 -> 0.75)",
     "supplementary.tex", [("NLL: $0.74$", "NLL: $0.75$")], "rounding_mismatch", 1),
    # --- N19b (20 Agu): son 23 kayitsizin bagi. Dort obegin dordu de temsil ediliyor ve uc
    # YENI KIP (`percent_of_fraction`, `sci_mantissa`, ve kapali-formdan gelen simulasyon
    # alanlari) burada sinaniyor. Kurulup denenmemis bag, kurulmamis bagdir.
    ("§4.7 tek-hucre atesleme orani bayat (3.5 -> 3.6) [percent_of_fraction]",
     "sections/04_experiments.tex", [("about $3.5\\%$", "about $3.6\\%$")],
     "rounding_mismatch", 1),
    ("§4.7 paylasilan kontrol korelasyonu bayat (+0.393 -> +0.390)",
     "sections/04_experiments.tex", [("$+0.393$", "$+0.390$")], "rounding_mismatch", 1),
    ("§4.8 manifest sayimi bayat (26 -> 27)",
     "sections/04_experiments.tex", [("), $26$", "), $27$")], "rounding_mismatch", 1),
    ("§5.1 en yuksek guven kutusundaki kutle bayat (89.9 -> 90.1)",
     "sections/05_results_discussion.tex", [("from $89.9\\%$", "from $90.1\\%$")],
     "rounding_mismatch", 1),
    ("§5.4 son-K icindeki maksimum orani bayat (34 -> 35) [percent_of_fraction]",
     "sections/05_results_discussion.tex", [("in $34\\%$", "in $35\\%$")],
     "rounding_mismatch", 1),
    # Bu vakada beklenen sinif `unregistered`: p-degerinin mantisi SATIRIN BASINDA duruyor,
    # dolayisiyla capa onu icermek zorunda (bkz. number_ledger'daki CAPA KURALI). Sayi
    # degisince capa dusher ve jeton kayitsiz kalir -- kapi yine kirmizi, ama sinifi farkli.
    # Olculen davranis bu; beklentiyi olcume uyduruyoruz, olcumu beklentiye degil.
    ("§5.5 p-degeri mantisi bayat (4.3 -> 4.4) [sci_mantissa, capa sayiyi iceriyor]",
     "sections/05_results_discussion.tex",
     [("$p{=}4.3\\times10^{-7}$", "$p{=}4.4\\times10^{-7}$")], "unregistered", 1),
]

# (ad, beyan kimligi, bozuk yol, beklenen sinif) -- DEFTERI bozan senaryolar: sayi dogru,
# artefakt dogru, BAG yanlis. Asagidaki vaka 17 Agu'da GERCEKTEN oldu: 'T*' adi bir baslikta
# fit degeri, komsu blokta dagitilan kolu tasiyordu. Ayni artefaktin KOMSU alani, ayni ad.
# ACIK, BEYANLI IHLALLER -- makale tarafinda duzeltilecek gercek kusurlar.
# Her kalem (sinif, kimlik). Liste TARIHLI degil YASAYANdir: kusur duzelince buradan silinir,
# ve silinmezse oz sinama "beyan curudu" der.
KNOWN_OPEN = [
    # 20 Agu 2026 sabah: §1:151 ve §2:229'daki "+0.65" cift yuvarlamasi. KAPANDI -- makale
    # "+0.645"--"0.764" olarak duzeltildi, beyanin yuvarlamasi 3dp'ye cekildi, iki bag yesile
    # dondu. Kayit burada birakilmiyor: liste YASAYANdir, kusur duzelince silinir.
    #
    # 20 Agu 2026 aksam (N19b) — DORT ACIK KALEM, ucu ayni sinifta:
    # (1-3) §4.7'nin uc simulasyon sayisi. Basili 0.543 / 0.740 / 0.007, `criterion_applied`in
    #       200k (aile) ve 40k (bagimli) tekrarlik MC kosularindan geliyordu ve UCUNCU BASAMAK
    #       Monte-Carlo gurultusuydu (200k'da aile-bazli oranin se'si ~0.004). Ayni olcut
    #       kapali forma indirgendi (`criterion_applied.fpr_exact`, Gauss-Legendre, ~1e-15) ve
    #       tam degerler 0.545 / 0.741 / 0.009 cikti. Uretici basiliyi TUTTURMAK icin
    #       ayarlanmadi; fark olculdu ve kirmizi birakildi.
    # (4)   §5.3'un FERPlus bilesik sicakligi: 0.5063 x 6 = 3.0378 -> 3.04, basili 3.06.
    #       3.06 ancak 0.5063'un iki basamaga yuvarlanmis hali (0.51) ile carpilinca cikiyor.
    ("rounding_mismatch", "s4.fpr_family_median_k"),
    ("rounding_mismatch", "s4.fpr_family_own_k"),
    ("rounding_mismatch", "s4.fpr_independence_gap"),
    ("derived_mismatch", "s5.composite_T_ferplus"),
]

BINDING_CASES = [
    ("tab_dose_response basligi FIT yerine DAGITILAN kola baglandi (T*, 17 Agu vakasi)",
     "tab_dose_response.stage1.header.T_star_fit", "results.stage1.deployed_T",
     "rounding_mismatch"),
    # --- 18 Agu: "uc tohum da 0.74" cumlesi MODAL argmin'e degil OYBIRLIGI degerine bagli.
    # Ayrimin YASADIGINI gostermek icin bag, tohumlarin AYRISTIGI bir seriye cevriliyor
    # (RAF-DB vae9182/NLL: modal 1.0, oybirligi yok -> alan None). Beklenen unresolved_path:
    # yani FERPlus'ta bir gun bir tohum ayrisirsa cumle SESSIZCE modal'i takip etmez, defter
    # duser. Iki 0.74 tek alana baglanmis olsaydi bu senaryo YAKALANAMAZDI.
    ("oybirligi alani cokerse duzyazi bagi duser (0.74 modal'a KAYMAZ)",
     "robust.ferplus_nll_argmin_all_seeds",
     'series["RAF-DB vae9182"].metrics.nll.argmin_T_all_seeds', "unresolved_path"),
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
    # BEYANLI ACIK IHLALLER. Taban eskiden "sifir ihlal" olmak zorundaydi; 20 Agu 2026'da govde
    # duzyazisi kapsama girince defter MAKALEDE GERCEK bir kusur buldu (bkz. KNOWN_OPEN) ve
    # taban satiri "TABAN KIRLI" demeye basladi -- yani oz sinama, isini yaptigi icin kirmiziya
    # dondu. Cozum susturmak DEGIL: acik ihlaller ADIYLA beyan edilir ve taban "beyan edilenle
    # BIREBIR ayni mi" diye sorulur. Bir ihlal duzelirse beyan CURUR ve o da bildirilir --
    # yani liste sessizce yaslanmaz.
    got_open = sorted((pr["kind"], pr.get("id")) for pr in p0["problems"])
    want_open = sorted(KNOWN_OPEN)
    base_ok = got_open == want_open
    detail = "-" if base_ok else f"beklenen {want_open} vs bulunan {got_open}"
    rows.append(("(taban) temiz kopya + beyanli acik ihlaller", detail, len(want_open),
                 len(got_open), base_unreg, "GECTI" if base_ok else "TABAN BEYANLA UYUSMUYOR"))
    ok = base_ok

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
            # TABANA GORE SAY (20 Agu 2026, N19b). Bu satir eskiden MUTLAK sayiyordu:
            # `kinds.count(want) >= n_want`. Taban temizken dogruydu, ama taban BEYANLI acik
            # ihlaller tasimaya baslayinca (KNOWN_OPEN) her `rounding_mismatch` senaryosu
            # ENJEKSIYON YAKALANMASA BILE geciyordu -- tabanda zaten uc tane vardi. Yani oz
            # sinamanin kendisi, izledigi kusur yuzunden korlesmisti. Artik her senaryo
            # YALNIZ KENDI enjeksiyonunu olcuyor.
            got = kinds.count(want) - k0.count(want)
        good = got >= n_want
        ok &= good
        rows.append((name, want, n_want, got, len(pl["unbound"]),
                     "YAKALANDI" if good else "KACIRILDI"))

    # --- bag hatasi: sayi dogru, artefakt dogru, BAG yanlis (r=0.724 vakasi)
    saved = dict(NL.PROSE[0])
    NL.PROSE[0]["path"] = "entropy_correlation.T074.pearson"
    pl, kinds = run(clean)
    got = ((kinds.count("unresolved_path") - k0.count("unresolved_path"))
           + (kinds.count("printed_not_found_at_location")
              - k0.count("printed_not_found_at_location")))
    good = got >= 1
    ok &= good
    rows.append(("r=0.724 bagi T=1 yerine T=0.74 koluna kuruldu (DEFTER bozuldu)",
                 "unresolved_path / printed_not_found_at_location", 1, got,
                 len(pl["unbound"]), "YAKALANDI" if good else "KACIRILDI"))
    NL.PROSE[0].update(saved)

    # --- yanlis bag: dogru artefakt, KOMSU alan (N14)
    for name, ident, bad_path, want in BINDING_CASES:
        bd = next(x for x in NL.BINDINGS if x["id"] == ident)
        keep = dict(bd)
        bd["path"] = bad_path
        pl, kinds = run(clean)
        got = kinds.count(want) - k0.count(want)
        good = got >= 1
        ok &= good
        rows.append((name, want, 1, got, len(pl["unbound"]),
                     "YAKALANDI" if good else "KACIRILDI"))
        bd.update(keep)

    # --- teyit kaydi: ikinci kaynak ayrisirsa (N14). Bugun sessiz olan sey yarin SINYAL
    # olmali; sinanmayan bir esik, esik degildir. Teyit yolunu baska bir ogretmenin fitine
    # cevirerek ayrismayi zorluyoruz -- gercekci karsiligi, teyit artefaktinin baska bir
    # fold/ogretmenle yeniden uretilmesi.
    xc = next(x for x in NL.CROSS_CHECKS if x["id"] == "tstar_nll.stage1")
    keep_xc = dict(xc)
    xc["confirm"] = (xc["confirm"][0], "primary.T_star")
    pl, kinds = run(clean)
    got = kinds.count("cross_source_divergence") - k0.count("cross_source_divergence")
    good = got >= 1
    ok &= good
    rows.append(("teyit kaydi ayristi: ikinci kaynak toleransi asti",
                 "cross_source_divergence", 1, got, len(pl["unbound"]),
                 "YAKALANDI" if good else "KACIRILDI"))
    xc.update(keep_xc)

    # --- teyit beyani bosa dustu: kanonik yol makalede hicbir hucreye bagli degil, dolayisiyla
    # toleransi turetecek yuvarlama da yok. Teyit ettigini sandigin sey makalede gecmiyorsa
    # teyit bir sey ifade etmez -- bu yuzden SORUN olarak raporlanir, sessizce atlanmaz.
    # `T_star_ece` 18 Agu'da S2'nin app_tstar tablosuna BAGLANDI, yani artik bagsiz degil --
    # senaryo kendi on kabulunu kaybetmisti ve oz sinama bunu yakaladi. Bagsiz kalan bir alan
    # secildi: `abs_dT` makalede hicbir hucreye basilmiyor.
    xc["canonical"] = (xc["canonical"][0], "results.stage1.abs_dT")
    pl, kinds = run(clean)
    got = kinds.count("cross_check_unbound") - k0.count("cross_check_unbound")
    good = got >= 1
    ok &= good
    rows.append(("teyit beyani bosa dustu: kanonik yola bagli hucre yok",
                 "cross_check_unbound", 1, got, len(pl["unbound"]),
                 "YAKALANDI" if good else "KACIRILDI"))
    xc.update(keep_xc)

    # --- bayat role: teyit degerini KOPYALAYAN artefakt ayrismis
    keep_r = list(xc["relays"])
    xc["relays"] = [(xc["relays"][0][0], "recipe_step3_ranking.rows[teacher=primary].T_star")]
    pl, kinds = run(clean)
    got = kinds.count("cross_source_relay_drift") - k0.count("cross_source_relay_drift")
    good = got >= 1
    ok &= good
    rows.append(("bayat role: teyidi kopyalayan artefakt baska bir degeri tasiyor",
                 "cross_source_relay_drift", 1, got, len(pl["unbound"]),
                 "YAKALANDI" if good else "KACIRILDI"))
    xc["relays"] = keep_r

    # --- bayat alan: bagli alan artefaktta yok
    saved_b = dict(NL.BINDINGS[0])
    NL.BINDINGS[0]["path"] = NL.BINDINGS[0]["path"] + "_SILINDI"
    pl, kinds = run(clean)
    got = kinds.count("unresolved_path") - k0.count("unresolved_path")
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
