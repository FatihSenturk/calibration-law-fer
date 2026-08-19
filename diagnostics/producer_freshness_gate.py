"""N16 — KAPININ YAPISAL KÖR NOKTASI: "üretici değişti, artefakt yeniden üretilmedi".

NEDEN VAR. `table_diff_gate` artefaktı KABUL EDİLMİŞ TEMEL ÇİZGİSİYLE karşılaştırır, üreticinin
TAZE ÇIKTISIYLA değil. Dolayısıyla bir üretici değişip artefakt yeniden üretilmediğinde hiçbir
kapı bağırmaz: temel çizgi de artefakt da eski, ikisi uyuşur. Bu sınıftan beş vaka yaşandı ve
BEŞİ DE ELLE yakalandı (0.53'ün bayat yan tablosu · `tab_selection`'ın ECE sütunu · Fig. 4'ün
PDF'i · `main_elsarticle.pdf` · `two_dataset_overlay`'in eksik 42 `per_seed` bloğu). Elle
yakalamak bir savunma değil, şansın adı.

RİSK PENCERESİ TAM ÖNÜMÜZDE: üreticilerin dokunulacağı tek dönem hakem revizyonu.

İKİ KATMAN, çünkü tek katman ölçüme takılır.

  KATMAN A — üreticiyi KOŞ, çıktıyı depodaki artefaktla BAYT düzeyinde karşılaştır.
      Ne yakalar: üretici değişikliğini DE, girdi verisi değişikliğini DE. Tam kontrol.
      Kime uygulanır: argümansız ve `results/` ağacı olmadan koşabilen üreticiler
      (Level-1 temiz olanlar) — ölçülen süreleri `--measure` ile kaydedilir.
      KAPI ARTEFAKTI DEĞİŞTİRMEZ: koşudan önce baytlar alınır, koşudan sonra karşılaştırılır ve
      dosya HER DURUMDA eski hâline geri yazılır. Kapı ölçer, düzeltmez.

  KATMAN B — KAYNAK PARMAK İZİ. Artefakt, yazıldığı anda üreticisinin kaynak sha256'sını
      `_provenance` bloğunda taşır; kapı üreticinin GÜNCEL hash'ini hesaplayıp karşılaştırır.
      Ne yakalar: yalnız ÜRETİCİ DEĞİŞTİ durumunu.
      NE YAKALAMAZ (sınır peşinen yazılıyor): GİRDİ VERİSİ değiştiyse görmez. Bir koşu eklenir,
      bir CSV tazelenir, bir logit önbelleği büyür -- üretici kaynağı aynı kaldığı sürece bu
      kapı sessiz kalır. Katman A ikisini de görür; Katman B ucuz ama YARIM bir kontroldür.
      Kime uygulanır: koşu ağacını okumak İŞİ olan (Level-3) üreticiler ve ölçülen süresi
      eşiği aşanlar -- yani koşturması pahalı olanlar.

HANGİ ARTEFAKT HANGİ KATMANDA olduğu raporda tablo hâlinde durur. Bugüne kadarki bütün
kazanımımız "kaçırdığımızı SAYABİLMEK"ten geldi; korunmayan bir artefakt varsa adıyla görünür.

Üretici->artefakt eşlemesi `export_to_drive.EXPORTS`ten türetilir (TEK KAYNAK), Level-3 beyanı
`level1_gate.ALLOWED`dan İTHAL edilir -- ikinci bir liste ikinci bir gerçek olurdu.

Kullanım:
    python diagnostics/producer_freshness_gate.py --measure   # süreleri ölç, sınıfları yaz
    python diagnostics/producer_freshness_gate.py             # kapı: ihlalde çıkış kodu 1
Çıktı -> diagnostics/reports/producer_freshness.{md,json}
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "diagnostics"))

# ÜRETİCİ->ARTEFAKT EŞLEMESİ ihraç bandından gelir (TEK KAYNAK) ve o dosya PUBLIC DEPODA YOK:
# bant Drive'a yazar, yayımlı depoya girmez. Import'u koşulsuz yapmak, public depoda bu betiği
# ham bir `ModuleNotFoundError` ile düşürüyordu -- yani okur için mekanizma görünür ama neden
# koşmadığı görünmez oluyordu. Beyanlı düşüş: çıkış kodu 2, "DENETLENEMEDI".
try:
    import export_to_drive as EX          # noqa: E402
    from level1_gate import ALLOWED, GUARD, producers  # noqa: E402  (Level-3 beyanı + kalkan)
    BAND_OK = True
except ModuleNotFoundError as _e:         # pragma: no cover - yalnız public depoda
    EX = None
    ALLOWED, GUARD, producers = set(), "", (lambda: [])
    BAND_OK = False
    BAND_ERR = str(_e)

OUT_MD = ROOT / "diagnostics" / "reports" / "producer_freshness.md"
OUT_JSON = ROOT / "diagnostics" / "reports" / "producer_freshness.json"
TIMINGS = ROOT / "diagnostics" / "reports" / "producer_timings.json"

# ÖLÇÜLEN süreye göre sınıf eşiği. Sayı `--measure` çıktısına bakılarak KONDU, tahminle değil:
# dağılım raporda basılıyor. Eşiği aşan üretici Katman B'ye düşer.
CHEAP_SECONDS = 90.0

# Koşturulması KAPININ KENDİ İŞİNİ bozacak betikler. Gerekçe zorunlu.
SKIP = {
    "diagnostics/export_to_drive.py": "bandın kendisi; koşmak Drive'a YAZMAK demek",
    "diagnostics/level1_gate.py": "kapı; kapıyı kapının içinden koşmak özyineleme",
    "diagnostics/producer_freshness_gate.py": "bu kapı",
    "diagnostics/status_heartbeat.py": "canlı saat: her koşuda zaman damgası değişir, "
                                       "bayt karşılaştırması tanımsız",
    "diagnostics/public_repo_sync.py": "public depoya yazar",
    "diagnostics/public_repo_staleness.py": "public depo durumunu okur, artefaktı zaman damgalı",
    "diagnostics/public_scope_scan.py": "public depo durumunu okur",
    "diagnostics/public_scope_buckets.py": "public depo durumunu okur",
    "diagnostics/table_diff_gate.py": "kapı; temel çizgi dosyasını yazar",
    "diagnostics/abs_path_gate.py": "kapı",
    "diagnostics/verify_paper_figures.py": "kapı",
    "diagnostics/check_numbers.py": "kapı",
    "diagnostics/number_ledger.py": "kâğıt ağacı olmadan defteri KORUR ve hiçbir şey yazmaz; "
                                    "bayt karşılaştırması bu betikte anlamsız",
}


# DONMUS ARTEFAKTLAR — Katman B'de kaynak ayrismasi BEKLENIR ve ihlal DEGILDIR.
# Donmus bir dosya, tam da ureticisi degismeye devam ederken degismesin diye dondurulmustur;
# "uretici o gunden beri degisti" cumlesi burada bir kusur degil, dondurmanin TANIMI.
FROZEN = {
    "diagnostics/selection_audit/selection_audit.csv":
        "DONMUS denetim kumesi (N=131, kesme 2026-07-31 06:00). Ureticinin sonraki commit'leri "
        "bu dosyayi ETKILEMEMELIDIR; tazelemek dondurmanin engellemek icin var oldugu sey.",
    "diagnostics/selection_audit/selection_audit_unfrozen.csv":
        "donmus kumenin ust kumesi; ayni kesme mantiginin disinda tutulur",
    "diagnostics/selection_audit/README.md":
        "donmus kumenin kendi belgesi; kesme gunune ait",
}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for blk in iter(lambda: fh.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def producer_artifacts():
    """`export_to_drive.EXPORTS`ten üretici -> artefakt listesi. Elle yazılmış (HAND) girdiler
    ve var olmayan dosyalar dışarıda; bir üreticinin birden çok artefaktı olabilir."""
    out = {}
    for entry in EX.EXPORTS:
        src = entry[0]
        prod = str(entry[2] if len(entry) > 2 else "")
        for part in prod.split(" + "):
            part = part.strip().split(" --")[0].strip()      # `x.py --from-runs` -> `x.py`
            if not (part.startswith("diagnostics/") and part.endswith(".py")):
                continue
            p = ROOT / src
            if p.exists():
                out.setdefault(part, [])
                if src not in out[part]:
                    out[part].append(src)
    return out


def run_producer(script, timeout):
    """Üreticiyi argümansız koştur. İki koşul, ikisi de zorunlu:

    1. İhraç kancası KAPALI (`REPO_EXPORT_SKIP`), aksi hâlde her koşu Drive'a yazar.
    2. KOŞU AĞACI ERİŞİLEMEZ (Level-1 GUARD'ı `level1_gate`ten İTHAL). Bu bir titizlik değil,
       karşılaştırmanın TANIMLI olması meselesi: ilk koşuda `a12_realsignal_verdict` "BAYAT"
       göründü, oysa artefakt bayat değildi -- depodaki kopya koşu ağacı ERİŞİLEMEZKEN
       yazılmıştı, bizim koşumuzda ise ağaç erişilebilirdi ve üretici fazladan tanı satırları
       ekledi (`exit_check.param_gate_ran` false -> true). Ölçüm alanlarının HEPSİ aynıydı.
       Yani artefaktın baytları "üretici + yayımlanmış girdiler"in fonksiyonu olmalı; özel koşu
       ağacının varlığına bağlıysa hakem makinesinde başka bir dosya üretilir. Kapı bu yüzden
       üreticiyi YAYIMLI DEPO KOŞULLARINDA çalıştırır.
    """
    env = {**os.environ, "REPO_EXPORT_SKIP": "1", "PYTHONIOENCODING": "utf-8"}
    t0 = time.perf_counter()
    r = subprocess.run([sys.executable, "-c", GUARD, str(ROOT / script)], cwd=ROOT,
                       capture_output=True, text=True, env=env, timeout=timeout,
                       encoding="utf-8", errors="replace")
    return time.perf_counter() - t0, r.returncode, ((r.stderr or "") + (r.stdout or ""))[-400:]


def worktree_dirty():
    """`git status --porcelain` -> {yol} kümesi. Kapının kendi temizliğini ölçmek için."""
    out = git("status", "--porcelain")
    return {ln[3:].strip().strip('"') for ln in out.splitlines() if ln.strip()}


def layer_a(script, arts, timeout, snapshot_dir):
    """Koş, bayt karşılaştır, HER DURUMDA geri yaz. Kapı artefaktı değiştirmez.

    BEYANSIZ YAN ÇIKTI (19 Ağu 2026'da ölçülerek eklendi). Anlık kopya YALNIZ bandın o üretici
    için BEYAN ETTİĞİ artefaktları kapsar. Bir üretici beyan edilmemiş bir dosya daha yazıyorsa
    kapı onu geri yazmaz ve ÇALIŞMA AĞACINI KİRLİ BIRAKIR. Gerçek vaka: `graphical_abstract.py`
    bantta yalnız `.png` ile duruyor ama `paper/figures/graphical_abstract.pdf` de yazıyor; iki
    koşu arasında farkın tamamı 3 bayt ve üçü de `/CreationDate` içinde -- yani içerik aynı, dosya
    bayt-yeniden-üretilebilir DEĞİL. Bu yüzden bir dosyanın bantta olmaması iki ayrı şey demek
    olabilir: unutulmuş olması, ya da (burada olduğu gibi) zaten bayt karşılaştırılamaz olması.
    Kapı bunu ÖLÇER ve raporlar; düşürmez, çünkü hüküm bandın kararıdır, kapının değil.

    Geri yazma kuralı: yalnız koşudan ÖNCE temiz olan izlenen dosyalar `git checkout --` ile
    geri alınır. Koşudan önce zaten değişmiş bir dosyaya DOKUNULMAZ -- kapı kullanıcının
    çalışmasını silmez.
    """
    dirty0 = worktree_dirty()
    before = {}
    for rel in arts:
        p = ROOT / rel
        snap = snapshot_dir / rel.replace("/", "__")
        shutil.copy2(p, snap)
        before[rel] = (sha256(p), snap)
    try:
        secs, rc, tail = run_producer(script, timeout)
    except subprocess.TimeoutExpired:
        for rel, (_h, snap) in before.items():
            shutil.copy2(snap, ROOT / rel)
        return {"layer": "A", "status": "zaman aşımı", "seconds": timeout, "changed": [],
                "note": f"> {timeout}s"}
    changed = []
    for rel, (h0, snap) in before.items():
        p = ROOT / rel
        h1 = sha256(p) if p.exists() else None
        if h1 != h0:
            changed.append({"artifact": rel, "stored": h0[:16],
                            "regenerated": (h1 or "-")[:16]})
        shutil.copy2(snap, p)                     # GERİ YAZ: kapı ölçer, düzeltmez
    # Kapının KENDİ anlık kopya dizini elenir: git onu boşken görmez, ilk kopyadan sonra
    # "yeni izlenmeyen dizin" diye bildirir ve üreticinin yan çıktısı gibi görünürdü.
    snap_rel = str(snapshot_dir.relative_to(ROOT)).replace("\\", "/")
    side = sorted(x for x in (worktree_dirty() - dirty0) - set(arts)
                  if not x.rstrip("/").startswith(snap_rel))
    for rel in side:
        git("checkout", "--", rel)                # yalnız ONCESINDE TEMIZ olanlar
    status = "BAYAT" if changed else ("geçti" if rc == 0 else "başka hata")
    return {"layer": "A", "status": status, "seconds": round(secs, 2), "changed": changed,
            "side_outputs": side, "returncode": rc, "note": "" if rc == 0 else tail}


def git(*args):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.stdout.strip() if r.returncode == 0 else ""


def layer_b(script, arts):
    """Kaynak parmak izi — GIT GEÇMİŞİNDEN, artefakta damga yazmadan.

    NEDEN DAMGA DEĞİL. İlk tasarım artefaktın içine yazma anında `_provenance.producer_sha256`
    koymaktı. İki artefaktta bu YAPILAMAZ ve sebebi tasarımın kendisinden güçlü:
      · `selection_audit.csv` DONMUŞ (N=131, 31 Tem kesme). Damga basmak için üreticiyi
        koşturmak, donmuş dosyayı yeniden yazmak demek -- kampanyanın en sert kuralı bu dosyanın
        asla yeniden yazılmaması.
      · `latency_benchmark.json` ÖLÇÜLMÜŞ SÜRELER taşıyor; yeniden koşmak yayımlanmış sayıları
        değiştirir. Damga uğruna veri değiştirilemez.
    Yani "damgalamak için koştur" yolu, korumak istediğimiz artefaktları bozardı.

    GIT GEÇMİŞİ AYNI SORUYU DAHA İYİ CEVAPLIYOR: artefaktın en son yazıldığı commit'ten BU YANA
    üreticiye dokunan commit var mı? Varsa "üretici değişti, artefakt yeniden üretilmedi"dir.
    Yeniden koşturma yok, dosyaya yazma yok, donmuş artefakt güvende.

    SINIR (peşinen): (a) yorum-satırı değişikliği de commit'tir, yani YANLIŞ POZİTİF verebilir --
    ama buradaki yanlış pozitifin bedeli "üreticiyi bir kez koştur ve bak", ucuz. (b) GİRDİ
    VERİSİ değiştiyse görmez; onu yalnız Katman A görür. (c) Artefakt commit'lenmemişse
    ölçülemez. Üçü de tabloda ayrı sınıf olarak görünür.
    Artefakt yine de `_provenance` taşıyorsa o da doğrulanır (ileride damga eklenirse çalışsın).
    """
    cur = sha256(ROOT / script)
    prod_commit = git("log", "-1", "--format=%H", "--", script)
    rows, unmeasurable, drift = [], [], []
    for rel in arts:
        art_commit = git("log", "-1", "--format=%H", "--", rel)
        row = {"artifact": rel, "artifact_commit": art_commit[:9] or None,
               "producer_commit": prod_commit[:9] or None}
        if not art_commit:
            row["note"] = "artefakt commit'lenmemiş; git geçmişinden ölçülemez"
            unmeasurable.append(rel)
            rows.append(row)
            continue
        # artefaktın son yazıldığı commit'ten BU YANA üreticiye dokunan commit sayısı
        n = git("rev-list", "--count", f"{art_commit}..HEAD", "--", script)
        row["producer_commits_since_artifact"] = int(n) if n.isdigit() else None
        if row["producer_commits_since_artifact"]:
            if rel in FROZEN:
                row["frozen"] = FROZEN[rel]      # beklenen ayrisma; ihlal degil
            else:
                drift.append(rel)
        # varsa damga da doğrulanır
        if rel.endswith(".json"):
            try:
                blob = json.loads((ROOT / rel).read_text(encoding="utf-8"))
                stamp = (blob.get("_provenance") or {}).get("producer_sha256") \
                    if isinstance(blob, dict) else None
                row["stamped"] = (stamp or "")[:16] or None
                if stamp and stamp != cur and rel not in drift:
                    drift.append(rel)
            except Exception as e:
                row["note"] = f"okunamadı: {e}"
        rows.append(row)
    status = ("KAYNAK AYRIŞMASI" if drift
              else ("ölçülemez" if unmeasurable else "geçti"))
    return {"layer": "B", "status": status, "producer_sha256": cur[:16], "artifacts": rows,
            "unstamped": unmeasurable, "drift": drift, "seconds": None, "changed": []}


def classify(script, timings):
    """Katman kararı: Level-3 beyanı VEYA ölçülen süre eşiği aşıyorsa B, yoksa A."""
    if script in ALLOWED:
        return "B", "Level-3 beyanlı: koşu dizinlerini okumak İŞİ"
    t = (timings or {}).get(script)
    if t is None:
        return "B", "süresi ÖLÇÜLMEDİ (--measure koşulmamış)"
    if t > CHEAP_SECONDS:
        return "B", f"ölçülen süre {t:.0f} s > {CHEAP_SECONDS:.0f} s eşiği"
    return "A", f"ölçülen süre {t:.1f} s"


def selftest():
    """KAPI KENDINI KANITLASIN: tarihsel vakayi geri koy, yakalandigini goster.

    Vaka (14->17 Agu): `two_dataset_overlay.py`ye 42 `per_seed` blogu eklendi ama artefakt
    yeniden uretilmedi. Butun kapilar sessiz kaldi -- temel cizgi de artefakt da eskiydi, ikisi
    uyusuyordu. Elle yakalandi. Burada o hal artefaktin BIR KOPYASI uzerinde geri konur (per_seed
    bloklari silinir), Katman A kosturulur ve BAYAT vermesi beklenir. Yakalayamiyorsa kapi
    yanlis katmandadir.
    """
    rel = "diagnostics/p1_dose_response/two_dataset_overlay.json"
    p = ROOT / rel
    snap_dir = ROOT / "diagnostics" / "reports" / "_freshness_selftest"
    if snap_dir.exists():
        shutil.rmtree(snap_dir)
    snap_dir.mkdir(parents=True)
    original = p.read_bytes()
    rows = []
    try:
        # taban: dokunulmamis artefakt BAYAT vermemeli
        base = layer_a("diagnostics/two_dataset_overlay.py", [rel], 900, snap_dir)
        rows.append(("(taban) dokunulmamis artefakt", "geçti", base["status"]))

        blob = json.loads(original.decode("utf-8"))
        n = 0
        for arm in blob.get("arms", {}).values():
            for pt in arm.get("points", []):
                for ck in pt.get("by_ckpt", {}).values():
                    if ck.pop("per_seed", None) is not None:
                        n += 1
        p.write_text(json.dumps(blob, indent=2), encoding="utf-8")
        hit = layer_a("diagnostics/two_dataset_overlay.py", [rel], 900, snap_dir)
        rows.append((f"tarihsel vaka: {n} `per_seed` blogu silindi", "BAYAT", hit["status"]))
    finally:
        p.write_bytes(original)
        shutil.rmtree(snap_dir, ignore_errors=True)

    ok = all(want == got for _n, want, got in rows)
    w = max(len(r[0]) for r in rows)
    print(f"\n{'senaryo'.ljust(w)}  {'beklenen':10} {'bulunan':10} sonuc")
    for name, want, got in rows:
        print(f"{name.ljust(w)}  {want:10} {got:10} "
              f"{'YAKALANDI' if want == got else 'KACIRILDI'}")
    print(f"\nSONUC: {'HEPSI YAKALANDI' if ok else 'EN AZ BIRI KACIRILDI'}")
    return 0 if ok else 1


def main():
    # reconfigure PARSER'DAN ÖNCE: `--help` metni Türkçe ve argparse onu parse sırasında
    # basıp çıkıyor; blok aşağıda kalırsa cp1252 konsolda `--help` UnicodeEncodeError ile
    # düşer (18 Ağu 2026'da ölçüldü). Kapının yardım metni de kapının parçasıdır.
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true",
                    help="tarihsel vakayi geri koyup kapinin yakaladigini goster")
    ap.add_argument("--measure", action="store_true",
                    help="her üreticiyi bir kez koşup süresini kaydet (sınıflandırma girdisi)")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--only", default=None, help="tek bir betik (hata ayıklama)")
    args, _unknown = ap.parse_known_args()
    if not BAND_OK:
        print("DENETLENEMEDI: üretici->artefakt eşlemesi `diagnostics/export_to_drive.py`den "
              f"türetiliyor ve bu depoda yok ({BAND_ERR}). Bant dosyası Drive'a yazdığı için "
              "yayımlı depoya girmez; kapı yalnız kampanya deposunda koşar. Çıkış 2.")
        return 2
    if args.selftest:
        return selftest()

    pa = producer_artifacts()
    scripts = [s for s in producers() if s not in SKIP and s in pa]
    if args.only:
        scripts = [s for s in scripts if s == args.only]
    timings = json.loads(TIMINGS.read_text(encoding="utf-8")) if TIMINGS.exists() else {}

    snapshot_dir = ROOT / "diagnostics" / "reports" / "_freshness_snapshot"
    if snapshot_dir.exists():
        shutil.rmtree(snapshot_dir)
    snapshot_dir.mkdir(parents=True)

    rows = []
    try:
        for i, script in enumerate(scripts, 1):
            layer, why = classify(script, timings if not args.measure else None)
            if args.measure:
                layer, why = ("B", "Level-3 beyanlı") if script in ALLOWED else ("A", "ölçüm")
            arts = pa[script]
            if layer == "A":
                r = layer_a(script, arts, args.timeout, snapshot_dir)
                if r.get("seconds") is not None:
                    timings[script] = r["seconds"]
            else:
                r = layer_b(script, arts)
            r.update({"script": script, "artifacts_n": len(arts), "why_layer": why,
                      "artifact_paths": arts})
            rows.append(r)
            print(f"  [{i}/{len(scripts)}] {r['layer']}  {r['status']:<18} {script}"
                  + (f"  ({r['seconds']:.1f}s)" if r.get("seconds") is not None else ""))
    finally:
        shutil.rmtree(snapshot_dir, ignore_errors=True)

    if args.measure:
        TIMINGS.write_text(json.dumps(dict(sorted(timings.items())), indent=2), encoding="utf-8")
        print(f"\nsüreler yazıldı -> {TIMINGS.relative_to(ROOT)}")

    stale = [r for r in rows if r["status"] == "BAYAT"]
    drifted = [r for r in rows if r["status"] == "KAYNAK AYRIŞMASI"]
    errs = [r for r in rows if r["status"] in ("başka hata", "zaman aşımı")]
    unstamped = [r for r in rows if r["status"] == "ölçülemez"]
    side = [r for r in rows if r.get("side_outputs")]
    write(rows, stale, drifted, errs, unstamped, timings, side)

    n_a = sum(1 for r in rows if r["layer"] == "A")
    print(f"\n  Katman A {n_a} · Katman B {len(rows) - n_a}")
    print(f"  BAYAT {len(stale)} · KAYNAK AYRIŞMASI {len(drifted)} · olculemez "
          f"{len(unstamped)} · başka hata {len(errs)} · beyansız yan çıktı {len(side)}")
    for r in side:
        print(f"    ~~ beyansız yan çıktı  {r['script']}  ->  {', '.join(r['side_outputs'])}")
    for r in stale + drifted + errs:
        print(f"    !! {r['status']:<18} {r['script']}  {r.get('changed') or r.get('drift') or r.get('note', '')}"[:170])
    bad = len(stale) + len(drifted) + len(errs)
    print(f"\n  SONUÇ: {'DÜŞTÜ' if bad else 'GEÇTİ'}  ({bad} kalem)")
    return 1 if bad else 0


def write(rows, stale, drifted, errs, unstamped, timings, side=()):
    ts = sorted(timings.values())
    L = ["# Üretici tazeliği — kapının yapısal kör noktası", "",
         "> **Sorun:** `table_diff_gate` artefaktı kabul edilmiş temel çizgisiyle karşılaştırır, "
         "üreticinin taze çıktısıyla değil. \"Üretici değişti, artefakt yeniden üretilmedi\" "
         "durumu bu yüzden bütün kapılardan geçer. Bu kapı tam o durumu ölçer.", "",
         "Üretici→artefakt eşlemesi `export_to_drive.EXPORTS`ten, Level-3 beyanı "
         "`level1_gate.ALLOWED`dan **ithal** edilir.", "",
         "| | |", "|---|---|",
         f"| denetlenen üretici | {len(rows)} |",
         f"| Katman A (koş + bayt karşılaştır) | {sum(1 for r in rows if r['layer'] == 'A')} |",
         f"| Katman B (kaynak parmak izi) | {sum(1 for r in rows if r['layer'] == 'B')} |",
         f"| **BAYAT** (artefakt üreticisinden geri) | **{len(stale)}** |",
         f"| **KAYNAK AYRIŞMASI** | **{len(drifted)}** |",
         f"| ölçülemez (Katman B, artefakt commit'lenmemiş) | {len(unstamped)} |",
         f"| başka hata / zaman aşımı | {len(errs)} |",
         f"| beyansız yan çıktı yazan üretici | {len(side)} |", ""]
    if side:
        L += ["## Beyansız yan çıktı", "",
              "Anlık kopya yalnız bandın BEYAN ETTİĞİ artefaktları kapsar. Aşağıdaki üreticiler "
              "koşunca beyan edilmemiş bir dosyayı daha değiştirdi; kapı bunları koşudan önce "
              "temiz olmaları koşuluyla `git checkout --` ile geri aldı, ama **bant beyanı ile "
              "üreticinin fiilî çıktısı ayrışıyor** demektir. Bir dosyanın bantta olmaması iki "
              "ayrı şey olabilir: unutulmuş olması, ya da bayt karşılaştırılamaz olması "
              "(ör. PDF'in `/CreationDate` damgası).", "",
              "| üretici | beyansız yazdığı dosya |", "|---|---|"]
        for r in side:
            L.append(f"| `{r['script']}` | {', '.join(f'`{x}`' for x in r['side_outputs'])} |")
        L.append("")
    if ts:
        L += ["## Ölçülen süreler (Katman A adayları)", "",
              f"n={len(ts)} · min {ts[0]:.1f} s · medyan {ts[len(ts) // 2]:.1f} s · "
              f"maks {ts[-1]:.1f} s · toplam {sum(ts):.0f} s · eşik **{CHEAP_SECONDS:.0f} s**", "",
              "En pahalı beş üretici:", "",
              "| üretici | saniye |", "|---|---|"]
        for k, v in sorted(timings.items(), key=lambda kv: -kv[1])[:5]:
            L.append(f"| `{k}` | {v:.1f} |")
        L.append("")
    L += ["## Katman B'nin SINIRI (peşinen)", "",
          "Kaynak parmak izi yalnız **üretici değişti**yi görür. **Girdi verisi değişti**yi "
          "görmez: bir koşu eklenir, bir CSV tazelenir, bir logit önbelleği büyür — üreticinin "
          "kaynağı aynı kaldığı sürece bu kapı sessizdir. Katman A ikisini de görür. Aşağıdaki "
          "tabloda B satırındaki her artefakt, bu yarım korumayla duruyor demektir.", "",
          "## Artefakt başına katman", "",
          "| üretici | katman | neden | artefakt | durum |", "|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["layer"], r["script"])):
        arts = "<br>".join("`" + a + "`" for a in r["artifact_paths"])
        L.append(f"| `{r['script']}` | **{r['layer']}** | {r['why_layer']} | {arts} | "
                 f"{r['status']} |")
    if stale or drifted:
        L += ["", "## İhlaller", "", "| üretici | sınıf | ayrıntı |", "|---|---|---|"]
        for r in stale:
            det = "; ".join(f"{c['artifact']} {c['stored']} → {c['regenerated']}"
                            for c in r["changed"])
            L.append(f"| `{r['script']}` | BAYAT | {det} |")
        for r in drifted:
            L.append(f"| `{r['script']}` | KAYNAK AYRIŞMASI | {', '.join(r['drift'])} |")
    if errs:
        L += ["", "## Koşamayanlar", "", "| üretici | sınıf | çıktı kuyruğu |", "|---|---|---|"]
        for r in errs:
            L.append(f"| `{r['script']}` | {r['status']} | `{str(r.get('note', ''))[-160:]}` |")
    L += ["", "---", "", "Üretici: `diagnostics/producer_freshness_gate.py` · süre ölçümü: "
          "`--measure` · **kapı artefaktı DEĞİŞTİRMEZ**: Katman A koşudan önce baytları "
          "anlık kopyalar ve koşudan sonra her durumda geri yazar.", ""]
    OUT_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    OUT_JSON.write_text(json.dumps(
        {"cheap_threshold_seconds": CHEAP_SECONDS,
         "counts": {"producers": len(rows), "stale": len(stale), "source_drift": len(drifted),
                    "unstamped": len(unstamped), "errors": len(errs)},
         "rows": rows}, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
