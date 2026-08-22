"""Kalp atışı: "ne durumdayız" sorusunun dosyadan okunan cevabı.

NEDEN VAR (ide_prompt_export_bandi §5). "Bitti mi / kaçtayız / ne zaman biter" sorusu bugüne
kadar her seferinde sohbette soruldu ve her seferinde elle ölçülüp elle yazıldı. Bu betik onu
`repo_export/STATUS.md` dosyasına indiriyor: her ihraçta ve istendiğinde yeniden üretilir.

ÖLÇÜLEN vs BEYAN EDİLEN — ayrımı dosyanın kendisi de yazar:
  ölçülen  : hangi koşu canlı, kaçıncı epoch, saniye/epoch, bitmiş koşu sayısı, son ihraç anı
  beyan    : kuyruğun kaç koşu PLANLADIĞI ve bekleyen iş listesi (`diagnostics/status_queue.txt`)
Payda ölçülemez: diskte yalnız başlamış koşular görünür, planlanan sayı hiçbir dosyada yazmaz.
Tahmin etmek yerine beyan okunur -- `preregistration_blocks.csv` ile aynı gerekçe.

Çıktı -> diagnostics/status_heartbeat.md  (banttan `repo_export/STATUS.md` olarak ihraç edilir)
Kullanım: python diagnostics/status_heartbeat.py
"""
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "diagnostics"))

RUNS_DIR = ROOT / "results" / "unified_students"
DECL = ROOT / "diagnostics" / "status_queue.txt"
BLOCKS = ROOT / "diagnostics" / "preregistration_blocks.csv"
OUT = ROOT / "diagnostics" / "status_heartbeat.md"

# Bir koşu, günlüğü son bu kadar dakika içinde büyüdüyse "canlı" sayılır. Eğitim adımı
# ~21 sn olduğu için 10 dk fazlasıyla geniş; çökmüş bir koşuyu canlı göstermez.
LIVE_WINDOW_MIN = 10


def declaration():
    d, pending = {}, []
    if not DECL.exists():
        return d, pending
    mode = None
    for ln in DECL.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if s == "pending:":
            mode = "pending"
            continue
        if mode == "pending" and s.startswith("-"):
            pending.append(s.lstrip("- ").strip())
        elif "=" in s and mode != "pending":
            k, v = s.split("=", 1)
            d[k.strip()] = v.strip()
    return d, pending


def block_prefixes(block):
    """Beyan edilen bloğa ait koşu-adı önekleri (preregistration_blocks.csv'den)."""
    out = []
    if not BLOCKS.exists() or not block:
        return out
    for ln in BLOCKS.read_text(encoding="utf-8").splitlines():
        if ln.startswith("#") or "," not in ln:
            continue
        p = [x.strip() for x in ln.split(",")]
        if len(p) >= 2 and p[1] == block:
            out.append(p[0])
    return out


def latest_attempt(run_dir):
    subs = sorted([d for d in run_dir.iterdir() if d.is_dir()], key=lambda d: d.name)
    return subs[-1] if subs else None


def scan(prefixes):
    """(canlı koşu, tüm koşuların özeti) -- yalnız beyan edilen bloğun koşuları."""
    rows = []
    if not RUNS_DIR.exists():
        return None, rows
    for rd in sorted(RUNS_DIR.iterdir()):
        if not rd.is_dir() or not any(rd.name.startswith(p) for p in prefixes):
            continue
        att = latest_attempt(rd)
        if not att:
            continue
        log = att / "training_log.csv"
        if not log.exists():
            continue
        epochs = sum(1 for _ in log.open(encoding="utf-8", errors="replace")) - 1
        mt = datetime.fromtimestamp(log.stat().st_mtime)
        try:
            started = datetime.strptime(att.name, "%Y-%m-%d-%H-%M-%S")
        except ValueError:
            started = mt
        rows.append({"name": rd.name, "attempt": att.name, "epochs": epochs,
                     "log_mtime": mt, "started": started})
    now = datetime.now()
    live = None
    for r in rows:
        if (now - r["log_mtime"]) < timedelta(minutes=LIVE_WINDOW_MIN):
            if live is None or r["log_mtime"] > live["log_mtime"]:
                live = r
    return live, rows


def last_export():
    """Son ihraç anı, ihraç bandının kendi manifestinden. Drive bağlı değilse '-'."""
    try:
        import export_to_drive
        mf = Path(export_to_drive.DEFAULT_DEST) / "MANIFEST.txt"
        if not mf.exists():
            return "-"
        for ln in mf.read_text(encoding="utf-8", errors="replace").splitlines():
            if ln.startswith("ihrac zamani"):
                return ln.split(":", 1)[1].strip()
    except Exception:                                                        # noqa: BLE001
        pass
    return "-"


def band_scope():
    """BANT KAPSAMI BEYANI (23 Agu 2026 eki) -- hakemin indigi yerde durmali.

    Defterin isaret ettigi bir artefakt banda giremiyorsa bunun tarihli bir tur raporunda
    kalmasi yetmez: DOI'yi cozup veriyi arayan okur o rapora rastlamayabilir. Beyan bandin
    kok dosyasina, STATUS.md'ye iner. Rapor ic muhasebe, STATUS beyandir.

    Her satir OLCULUR: kaynak listesi defterin kendi beyanlarindan (BINDINGS/DERIVED/PROSE/
    SIGNS/CROSS_CHECKS), bant listesi `export_to_drive.EXPORTS`ten, muafiyetler
    `number_ledger.BAND_EXEMPT`ten, yeniden-uretilebilirlik `level1_gate.ALLOWED`ten.
    Hicbiri elle yazilmaz; olculemezse bu dosya "olculemedi" yazar, sessiz kalmaz.
    """
    import export_to_drive as EX
    import number_ledger as NL
    from level1_gate import ALLOWED

    banded, producer_of = set(), {}
    for e in EX.EXPORTS:
        src = e[0]
        rel = src[len("diagnostics/"):] if src.startswith("diagnostics/") else src
        banded.add(src)
        banded.add(rel)
        prod = str(e[2] if len(e) > 2 else "").split(" --")[0].strip()
        if prod.endswith(".py"):
            producer_of[rel] = prod

    sources = {}
    def add(a, i):
        sources.setdefault(a, set()).add(i)
    for x in NL.BINDINGS:
        add(x["artifact"], x["id"])
    for x in NL.DERIVED:
        for o in x["operands"]:
            add(o["artifact"], x["id"])
    for x in NL.PROSE:
        add(x["artifact"], x["id"])
    for x in NL.SIGNS:
        add(x["artifact"], x["id"])
    for x in NL.CROSS_CHECKS:
        add(x["canonical"][0], x["id"])
        add(x["confirm"][0], x["id"])
        for a, _p in x["relays"]:
            add(a, x["id"])

    # IKINCI KANAL: hakem bandi degil, GitHub/Zenodo arsivini indirir.
    published, pub_missing = None, []
    try:
        import subprocess
        from public_repo_sync import PUBLIC as _PUB
        if Path(_PUB).exists():
            r = subprocess.run(["git", "ls-files"], cwd=str(_PUB), capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
            if r.returncode == 0:
                published = set(r.stdout.split())
                pub_missing = sorted(a for a in sources
                                     if ("diagnostics/" + a) not in published
                                     and a not in published)
    except Exception:
        published = None

    missing = sorted(a for a in sources if a not in banded)
    exempt = [(a, NL.BAND_EXEMPT[a]) for a in missing if a in NL.BAND_EXEMPT]
    undeclared = [a for a in missing if a not in NL.BAND_EXEMPT]
    # Yayimli ama kosu agaci olmadan YENIDEN URETILEMEZ olanlar (Level-3 beyanli ureticiler).
    l3 = sorted({producer_of[a] for a in sources
                 if a in producer_of and producer_of[a] in ALLOWED})

    L = ["## Bant kapsamı — makaledeki sayıların kaynakları", "",
         f"Makaledeki sayı defteri (`diagnostics/number_ledger.py`) **{len(sources)}** artefakt "
         f"alanına bağlı. Bunların **{len(sources) - len(missing)}**'i bu ihraç bandında; "
         f"gerekçeli muaf **{len(exempt)}**; gerekçesiz eksik **{len(undeclared)}**.", "",
         "Kural kapıda: bir sayı bir alana bağlıysa o alanın dosyası da burada olmalı "
         "(`binding_source_unpublished`). Yayımlanamayan bir kaynak varsa adıyla ve "
         "gerekçesiyle aşağıda durur — sessizce eksik kalamaz.", ""]
    if exempt:
        L += ["| yayımlanamayan kaynak | gerekçe |", "|---|---|"]
        L += [f"| `{a}` | {w} |" for a, w in exempt]
        L += [""]
    if undeclared:
        L += ["> **UYARI — gerekçesiz eksik kaynak:** "
              + ", ".join(f"`{a}`" for a in undeclared), ""]
    if not exempt and not undeclared:
        L += ["Şu an muafiyet yok: defterin işaret ettiği her kaynak bantta.", ""]
    if published is None:
        L += ["> Public depo bu makinede okunamadı — ikinci kanal ÖLÇÜLMEDİ.", ""]
    elif pub_missing:
        L += ["> **UYARI — public depoda (DOI'den inen arşivde) bulunmayan kaynak:** "
              + ", ".join(f"`{a}`" for a in pub_missing), ""]
    else:
        L += [f"Aynı {len(sources)} kaynağın tamamı **public depoda** da izleniyor — bandın "
              "kendisi Drive'a gider, hakem ise DOI'yi çözüp GitHub/Zenodo arşivini indirir; "
              "kapı iki kanala birden bakar.", ""]
    if l3:
        L += ["**Yeniden üretim (ayrı bir soru).** Aşağıdaki üreticiler ölçümlerini ham koşu "
              "dizinlerinden (checkpoint / örnek-başına logit) yapar; bant onların "
              "**çıktısını** taşır, girdisini değil. Yayımlanan artefakt sayıyı "
              "**doğrulamaya** yeter, ham ağaç olmadan **yeniden üretmeye** yetmez:", ""]
        L += [f"- `{p}`" for p in l3]
        L += [""]
    return L


def build(export_time=None):
    """export_time: ihracın KENDİ damgası, varsa.

    NEDEN PARAMETRE. Kalp atışı "son ihraç" satırını MANIFEST'ten okur, ama export_to_drive
    bu fonksiyonu manifest'i YENİDEN YAZMADAN ÖNCE çağırır (STATUS.md'nin kendisi ihraç
    edilecek dosyalardan biri olduğu için). Sonuç: Drive'daki STATUS.md hep BİR İHRAÇ GERİDE
    kalıyordu -- 6 Ağu'da fark edildi, damga 4 Ağu 13:35'te takılı görünüyordu. Çağıran kendi
    zamanını biliyor; okumak yerine veriyor."""
    d, pending = declaration()
    queue = d.get("queue", "")
    total = int(d.get("total_runs", 0) or 0)
    per = int(d.get("epochs_per_run", 0) or 0)
    prefixes = block_prefixes(d.get("block", ""))
    live, rows = scan(prefixes) if prefixes else (None, [])
    done = sum(1 for r in rows if per and r["epochs"] >= per)

    now = datetime.now()
    if live and per:
        # Saniye/epoch'u CANLI koşudan almak, koşu yeni başlamışsa ETA'yı günlerce şişirir:
        # ilk epoch'un süresi model kurulumu + veri yüklemesini (~90 sn) de taşıyor, oysa
        # kararlı hız ~22 sn. 4 Ağu 12:5x'te bu tam olarak oldu -- epoch 1'den ölçülen
        # 114.9 sn/epoch ETA'yı 5 Ağu yerine 10 Ağu gösterdi. Bu satır banda gidiyor ve
        # planlama ona bakıyor, o yüzden yanlış olamaz.
        #
        # Çözüm: yeterince epoch birikene kadar BİTMİŞ koşuların ortancasını kullan
        # (onlarda başlatma maliyeti 400 epoch'a yayıldığı için ihmal edilebilir), ve
        # hızın nereden geldiğini satırda YAZ -- okuyan hangi sayıya baktığını bilsin.
        MIN_EPOCHS_FOR_RATE = 20

        def _rate(r):
            return ((r["log_mtime"] - r["started"]).total_seconds() / r["epochs"]
                    if r["epochs"] else None)

        live_rate = _rate(live) or 0
        hist = sorted(x for x in (_rate(r) for r in rows if r["epochs"] >= per) if x)
        if live["epochs"] >= MIN_EPOCHS_FOR_RATE or not hist:
            spe, rate_src = live_rate, "ölçülen"
        else:
            spe = hist[len(hist) // 2]
            rate_src = f"bitmiş {len(hist)} koşunun ortancası; canlı koşu daha {live['epochs']} epoch'ta"
        remaining = (per - live["epochs"]) + max(0, total - done - 1) * per
        eta = now + timedelta(seconds=remaining * spe) if spe else None
        gpu = (f"`{live['name']}` — epoch **{live['epochs']}/{per}** "
               f"({spe:.1f} sn/epoch, {rate_src})")
        prog = f"**{done}/{total}** bitti, 1 koşuyor, {max(0, total - done - 1)} sırada"
        eta_s = (eta.strftime("%d %b %H:%M") + f"  (kalan ~{remaining * spe / 3600:.1f} sa)"
                 if eta else "-")
    elif rows and per and done >= total:
        gpu, prog, eta_s = "boşta — kuyruk bitti", f"**{done}/{total}** bitti", "-"
    elif not prefixes:
        gpu, prog, eta_s = ("aktif kuyruk beyan edilmemiş "
                            "(`diagnostics/status_queue.txt`)", "-", "-")
    else:
        gpu = "boşta — canlı koşu yok (son günlük 10 dk'dan eski)"
        prog, eta_s = f"**{done}/{total}** bitti", "-"

    L = [f"# Durum — {now.strftime('%Y-%m-%d %H:%M')}", "",
         f"| | |", "|---|---|",
         f"| **GPU** | {gpu} |",
         f"| **kuyruk** | `{queue or '-'}` · {prog} |",
         f"| **ETA** | {eta_s} |",
         f"| **son ihraç** | {export_time or last_export()} |",
         f"| **bekleyen** | {len(pending)} kalem (aşağıda) |", ""]
    if d.get("note"):
        L += [f"> {d['note']}", ""]
    try:
        L += band_scope()
    except Exception as e:                       # sessiz kalma: olculemediyse onu yaz
        L += ["## Bant kapsamı", "",
              f"> ÖLÇÜLEMEDİ: {type(e).__name__}: {e}", ""]
    L += ["## Bekleyen iş", ""]
    L += [f"{i}. {p}" for i, p in enumerate(pending, 1)] or ["_(yok)_"]
    L += ["", "---", "",
          "Ölçülen: canlı koşu, epoch, sn/epoch, bitmiş sayısı, son ihraç anı. "
          "Beyan edilen: kuyruğun planladığı koşu sayısı ve bekleyen iş listesi "
          "(`diagnostics/status_queue.txt`) — payda diskte yazmaz, o yüzden tahmin edilmez.",
          "", f"Üretici: `diagnostics/status_heartbeat.py` · "
              f"kaynak koşu dizinleri: `results/unified_students/`", ""]

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    return {"gpu": gpu, "done": done, "total": total, "eta": eta_s, "pending": len(pending)}


def main():
    # Konsol cp1252; GPU satırı kuyruk boşaldığında Türkçe karakter taşıyor ('ş' cp1252'de yok
    # ve UnicodeEncodeError veriyordu). Dosya zaten utf-8 yazılıyor, kıran yalnız bu print'ti.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    r = build()
    print(f"GPU     : {r['gpu']}")
    print(f"kuyruk  : {r['done']}/{r['total']}")
    print(f"ETA     : {r['eta']}")
    print(f"bekleyen: {r['pending']} kalem")
    print(f"yazildi : {OUT}")


if __name__ == "__main__":
    main()
