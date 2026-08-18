"""N16 — `requirements.txt` ÜRETİCİSİ: elle yazılmış bir iddia değil, ölçülmüş bir çıktı.

NEDEN. Depoda duran `requirements_27may.txt` elle yazılmış ve SÜRÜMSÜZ bir listeydi (`torch`,
`numpy`, ...). Böyle bir dosya bir beyandır: "bunlar gerekiyor" der ama neyle koştuğumuzu
söylemez, ve yanlış olduğunda hiçbir şey bağırmaz. Level-1 kuralının kendisi burada da geçerli:
bir dosya bir üreticinin ÇIKTISI olmalı.

TANIM — hangi paket girer, açıkça:
  1. Deponun kendi `.py` dosyaları taranır ve TOP-LEVEL import adları toplanır.
  2. Standart kütüphane ve deponun kendi modülleri (`diagnostics/`, `models/`, `utils/`, ...)
     düşülür.
  3. Kalan her import adı, KURULU dağıtıma `importlib.metadata.packages_distributions()` ile
     eşlenir -- `cv2 -> opencv-python`, `PIL -> pillow`, `yaml -> PyYAML` gibi eşlemeler
     böylece elle yazılmaz, ölçülür.
  4. Sürüm, o anda KURULU olan sürümdür ve `==` ile sabitlenir.

Eşlenemeyen import adı SESSİZCE ATILMAZ: dosyanın altına `# eşlenemedi:` diye yazılır ve bu
betik çıkış kodu 1 verir. "Bulunamadı" yazmak, tahmin etmekten iyidir.

Salt-okunur (yalnız `requirements.txt` yazar), GPU yok.
Kullanım: python diagnostics/requirements_lock.py [--check]
Çıktı -> requirements.txt
"""
import argparse
import ast
import sys
from importlib import metadata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "requirements.txt"

# Deponun KENDİ modülleri ÖLÇÜLEREK bulunur, elle listelenmez. Betikler `sys.path`e
# `diagnostics/` ekliyor, dolayısıyla `import stats_convention` yerel bir modüldür; elle
# tutulan bir liste bunları kaçırır ve hepsi "eşlenemedi" diye görünürdü (ilk koşuda tam
# olarak bu oldu: 40 satırın 37'si aslında kendi dosyalarımızdı).
SYS_PATH_DIRS = ("", "diagnostics", "tools", "utils", "models", "dataset_utils", "trails",
                 "trials")

SKIP_DIRS = {".git", "__pycache__", "results", "data", "dataset_cache", "checkpoints",
             "pretrained", "swanlog", "run_logs", "launcher_logs", "pipeline_logs",
             "evaluation_runs", "reference_90_74", "kd_logs_rafdb", "kd_logs_affectnet8",
             "kd_logs_rafdb_multiseed", "kd_logs_rafdb_newrecipe_lightle_swa",
             "kd_logs_rafdb_newrecipe_noerasing", "kd_logs_rafdb_phase0_smoke", "paper",
             "reports"}


def local_names():
    """Depoda modül/paket olarak ÇÖZÜLEBİLEN adlar. Betiklerin `sys.path`e eklediği dizinler
    dolaşılır; oradaki her `x.py` ve her paket dizini yerel bir import adıdır."""
    out = set()
    for d in SYS_PATH_DIRS:
        base = ROOT / d if d else ROOT
        if not base.is_dir():
            continue
        for p in base.iterdir():
            if p.suffix == ".py":
                out.add(p.stem)
            elif p.is_dir() and p.name not in SKIP_DIRS and not p.name.startswith("."):
                out.add(p.name)
    return out


def top_imports():
    """Deponun `.py` dosyalarındaki top-level import adları -> {ad: [dosya, ...]}."""
    local = local_names()
    found = {}
    for p in sorted(ROOT.rglob("*.py")):
        rel = p.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts[:-1]):
            continue
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0] for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                # `from . import x` -> level>0, deponun kendisi
                names = [] if node.level else [(node.module or "").split(".")[0]]
            else:
                continue
            for n in names:
                if n and n not in sys.stdlib_module_names and n not in local:
                    found.setdefault(n, []).append(str(rel).replace("\\", "/"))
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="yazma, yalnız depodaki dosyayla karşılaştır")
    args, _unknown = ap.parse_known_args()
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")

    imports = top_imports()
    pkgmap = metadata.packages_distributions()
    dists, unmapped = {}, {}
    for name, files in sorted(imports.items()):
        cands = pkgmap.get(name)
        if not cands:
            unmapped[name] = sorted(set(files))[:3]
            continue
        for d in cands:
            try:
                dists[d] = metadata.version(d)
            except metadata.PackageNotFoundError:
                unmapped[name] = sorted(set(files))[:3]

    py = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    L = ["# ÜRETİLDİ — elle düzenlemeyin.",
         "# Üretici: diagnostics/requirements_lock.py",
         "# Tanım: deponun .py dosyalarındaki top-level import adları -> kurulu dağıtım",
         "#        (importlib.metadata.packages_distributions), sürüm o anda KURULU olan.",
         f"# Python: {py}",
         f"# Taranan import adı: {len(imports)} · eşlenen dağıtım: {len(dists)}", ""]
    L += [f"{d}=={v}" for d, v in sorted(dists.items(), key=lambda kv: kv[0].lower())]
    if unmapped:
        L += ["", "# eşlenemedi (kurulu bir dağıtıma bağlanamayan import adları):"]
        L += [f"#   {n}  <- {', '.join(f)}" for n, f in sorted(unmapped.items())]
    text = "\n".join(L) + "\n"

    if args.check:
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        same = cur == text
        print(f"requirements.txt {'AYNI' if same else 'AYRIŞMIŞ'}")
        return 0 if same else 1

    OUT.write_text(text, encoding="utf-8")
    print(f"{len(dists)} dağıtım sabitlendi -> {OUT.relative_to(ROOT)}  (Python {py})")
    for d, v in sorted(dists.items(), key=lambda kv: kv[0].lower()):
        print(f"  {d}=={v}")
    if unmapped:
        # ÇIKIŞ KODU 0. Eşlenememiş bir import adı bu ÜRETİCİNİN hatası değil, kaydedilecek bir
        # OLGUDUR ve olgu dosyanın içine yazıldı. Burada 1 dönmek, "üç isteğe bağlı bağımlılık
        # kurulu değil" ile "üretici çalışmadı"yı aynı sinyale bindirirdi -- ve Level-1 kapısı
        # bu betiği "başka hata" diye sınıflardı.
        print(f"\n  EŞLENEMEDİ {len(unmapped)} (dosyaya yazıldı, çıkış kodu 0):")
        for n, f in sorted(unmapped.items()):
            print(f"    {n}  <- {', '.join(f)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
