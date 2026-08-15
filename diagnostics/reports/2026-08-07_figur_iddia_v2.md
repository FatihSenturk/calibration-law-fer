# Figür/betik iddia cümlesinin başlık v2 ile hizalanması + spot-check + derleme

**Tarih:** 7 Ağustos 2026 · **Girdi promptları:** `planning/ide_prompt_figur_iddia_v2.md`
(7 Ağu 00:29), `planning/ide_addendum_2026-08-07.md` (7 Ağu 12:50),
`planning/ide_iletim_ozeti_2026-08-08.md` (7 Ağu 15:49) · **Karar:** Fatih, seçenek 3 —
dördünü birden hizala.

---

## (a) Dört konumun diff'i

### 1. `diagnostics/graphical_abstract.py:42`

```diff
-HEADLINE_1 = "Teacher calibration governs student calibration"
+HEADLINE_1 = "Teacher-side logit scaling governs student calibration"
```

**Betiğin tamamı tarandı** (`causal`, `Causal Evidence`, eski başlık dizesi,
`teacher calibration governs`). Başlık-benzeri ikinci bir satır var ve **DEĞİŞTİRİLMEDİ**:

```python
HEADLINE_2 = "— causal evidence via prediction-preserving logit rescaling —"
```

> ⚠️ **Karar Fatih'e bırakıldı.** HEADLINE_2 v2 ile *çelişmiyor* — aksine müdahaleyi zaten
> doğru adlandırıyor. Ama HEADLINE_1 artık "logit scaling" dediği için ikisi yan yana
> **"logit scaling … logit rescaling"** diye tekrar ediyor. Bu bir doğruluk sorunu değil,
> bir üslup sorunu; ve grafik özetin ilk sayfa metni olduğu için ikame önerisini uygulamak
> yerine yazıyorum: örn. `"— causal evidence: the rescaling preserves every prediction —"`.
> Gönderim paketinin kelimelerini kendi başıma değiştirmedim.

### 2. `diagnostics/p1_two_teacher_overlay.py:244`

```diff
-    ax1.set_title("Teacher calibration governs student calibration", fontsize=10)
+    ax1.set_title("Teacher-side logit scaling governs student calibration", fontsize=10)
```

### 3. `diagnostics/two_dataset_overlay.py:351` (suptitle)

```diff
-    fig.suptitle("Teacher calibration governs student calibration in BOTH directions and on "
-                 "BOTH datasets\n"
+    fig.suptitle("Teacher-side logit scaling governs student calibration in BOTH directions "
+                 "and on BOTH datasets\n"
```

Yalnız özne değişti; **"BOTH directions / BOTH datasets" vurgusu korundu**, biçim ve
büyük-küçük harf düzeni aynen kaldı.

### 4. `ferplus_dose_response_queue.ps1:17` — **DEĞİŞTİRİLMEDİ, not düşüldü**

Bkz. (d).

---

## (b) Yeniden üretilen dosyalar

| dosya | durum |
|---|---|
| `paper/figures/graphical_abstract.pdf` | **değişti** (23 765 → 23 836 bayt) |
| `paper/figures/graphical_abstract.png` | değişti |
| `diagnostics/p1_dose_response/two_dataset_overlay_swa.png` | değişti (tanılama) |
| `diagnostics/p1_dose_response/two_teacher_overlay.png` | değişti (tanılama) |
| `paper/figures/two_dataset_overlay_swa.pdf` | **içerik değişmedi** — geri alındı |
| `paper/figures/two_teacher_overlay.pdf` | **içerik değişmedi** — geri alındı |
| `paper/figures/mechanism_diagnostic.pdf` | **kapsam dışı, içerik değişmedi** — geri alındı |
| `paper/figures/ferplus_dual_axis.pdf` | **içerik değişmedi** — geri alındı |
| `paper/figures/p5_frontier.pdf` | **içerik değişmedi** — geri alındı |

> **Neden beş PDF geri alındı.** `export_paper_figures.py` bütün figürleri yeniden yazıyor
> ve PDF'ler gömülü `CreationDate`/`ModDate` taşıdığı için **içerik aynıyken bile bayt olarak
> farklı** çıkıyorlar. İlk ihraç bu yüzden "6 figür yenilendi" dedi. Zaman damgalarını
> normalize edip karşılaştırdım: **yalnız `graphical_abstract.pdf` gerçekten değişti**, diğer
> beşi birebir aynı. Beşini geri aldım — aksi hâlde Drive aynası, kapsam dışı bırakılmış
> `mechanism_diagnostic` dahil, olmayan bir değişiklik bildirirdi.

---

## (c) Kapılar

| kapı | sonuç |
|---|---|
| `verify_paper_figures` | **10 figür, 0 başarısız** ✅ |
| `table_diff_gate` | **702/702, sapma yok** ✅ |

Bu tur hiçbir sayıya dokunmadı; tablo kapısının sapmasız çıkması beklenen davranıştı ve
doğrulandı.

---

## (d) B-007 yorumunda uygulanan kural

Yorum **doğrudan alıntı değil, paraphrase** — yani prompt'un "yeniden yazabilirsin" kolu
geçerliydi. **Yine de yeniden yazılmadı**, yalnız not düşüldü. Gerekçe:

`ferplus_dose_response_queue.ps1` B-007'nin FERPlus dış-geçerlilik testinde **kanıt
zincirinin parçası** — koşulardan önce (26 Tem) dondurulup commit'lendi. Ön-beyan
artefaktlarının metnini geriye dönük değiştirmemek kampanyanın duran kuralı, ve prompt
yeniden yazmayı *zorunlu* değil *serbest* bırakmıştı. İki kural çakışınca daha koruyucu
olanı seçtim; bu bir yargı kararı, Fatih aksini isterse tek satırlık iş.

Eklenen not, satırın kendisine dokunmadan altına düştü ve hangi kuralın neden uygulandığını
yazıyor.

---

## (e) Beşinci-örnek taraması — tam eşleşme listesi

`grep -rn "calibration governs"` + `"governs student calibration"`, iki depo.

**Canlı konumlar (değiştirildi / not düşüldü):**

| konum | işlem |
|---|---|
| `poster-var/diagnostics/graphical_abstract.py:42` | değiştirildi |
| `poster-var/diagnostics/p1_two_teacher_overlay.py:244` | değiştirildi |
| `poster-var/diagnostics/two_dataset_overlay.py:351` | değiştirildi |
| `poster-var/ferplus_dose_response_queue.ps1:17` | not düşüldü, metin korundu |

**Tarihli kayıtlar — DOKUNULMADI:**

| konum | ne |
|---|---|
| `diagnostics/reports/2026-08-04_baslik_v2_teyit.md:58` | açık kalemi *bildiren* rapor satırı |
| `diagnostics/reports/2026-08-04_baslik_v2_teyit.md:66` | aynı raporun gerekçe paragrafı |

**Yaşayan dosyalar (iddia cümlesi değil, durum metni):** `diagnostics/status_queue.txt:26`
ve türevi `status_heartbeat.md:15` — bunlar açık kalemi *tarif eden* bekleyen-iş satırı;
kalem kapandığı için bu turda güncellendi.

### ⚠️ Public repro deposu — düzeltme TAŞINMADI ve otomatik taşınmayacak

`public/calibration-law-fer/` aynı dört konumu barındırıyor ve **dördü de hâlâ eski
cümlede**. Bu raporun ilk hâlinde "bir sonraki senkronda aynen taşınacak" yazıyordu;
**o cümle yanlıştı ve doğrulanmadan yazılmıştı.** Doğrulandığında çıkan tablo:

- Public depo **ayrı bir git deposu**, kendi tek commit'i var (`504d8d2`), çalışma ağacı temiz.
- poster-var'dan public'e **hiçbir senkron betiği yok** — arandı, bulunamadı.
- Gönderim günü dizisi (`2026-08-04_gonderim_gunu_dizisi.md`) **GitHub deposunu** silip
  yeniden kurmayı tarif ediyor; **dosyaları poster-var'dan yeniden kopyalamayı tarif
  etmiyor**. Yani "yeniden kurulacak" ≠ "güncellenecek".
- Üç figür betiğinin ikili karşılaştırması: **üçü de farklı** (public'te eski dize).

**Sonuç: müdahale edilmezse public repro deposu ESKİ iddia cümlesiyle yayımlanır** — yani
tam olarak bu turun kapatmaya çalıştığı tutarsızlık, hakemin veri-erişilebilirlik beyanından
gideceği artefaktta kalır.

**Kendi başıma düzeltmedim.** Sebebi: bu deponun *"tek commit, 279 dosya"* olması belgelenmiş
bir özellik ve gönderim günü dizisinin parçası; ikinci bir commit açmak o dizinin
varsayımını değiştirir. Karar Fatih'in. İki seçenek:
1. **Şimdi taşı** — üç dosyada aynı ikame, public depoda ikinci commit (tek commit özelliği düşer).
2. **Gönderim gününe bırak** — ama o zaman runbook'a *"poster-var'dan dosyaları yeniden kopyala"*
   adımı **açıkça eklenmeli**, yoksa unutulur; şu an runbook'ta böyle bir adım yok.

> **BEŞİNCİ CANLI KONUM YOK.** Beklenen küme birebir doğrulandı: 4 canlı + 2 tarihli kayıt.

---

## Spot-check (ek not, madde 1–2)

### §5.1 — reliability üst-bölme kütlesi ✅

Kaynak: `diagnostics/reliability/reliability_diagram.json` (stage1, @swa, 15 bölme, 3 tohum).

| kol | üst bölme n | toplam | oran | makale | eşleşme |
|---|---|---|---|---|---|
| T=1 | 8 278 | 9 204 | **0.8994** | 89.9% | ✅ |
| T=1.3406 | 7 616 | 9 204 | **0.8275** | 82.7% | ✅ |

Üst bölmenin kendi içi de bilgi taşıyor: T=1'de güven 0.9932'ye karşı doğruluk 0.9389
(aşırı güven), T*'ta 0.9760'a karşı 0.9603 — açık üçte ikiden fazla kapanıyor.

### §5.4 — per-class signed gap ✅ (altı değerin altısı)

Kaynak: `diagnostics/reliability/perclass_calibration.json`.

| makale ifadesi | ölçülen | eşleşme |
|---|---|---|
| happiness **+0.028**, n=1185 | **+0.0278**, n=1185 | ✅ |
| fear **+0.305**, n=74 | **+0.3048**, n=74 | ✅ |
| "eleven-fold range" | **11.0×** | ✅ |
| sık sınıflar sıfırı **T≈1.5**'te kesiyor | Happiness **1.457**, Neutral **1.463** | ✅ |
| anger/sadness **T≈1.7–1.8** | Sadness **1.699**, Anger **1.821** | ✅ |
| T=2.2'de disgust **+0.063**, fear **+0.165** | **+0.0629**, **+0.1655** | ✅ |
| T=2.2'de happiness **−0.110**, neutral **−0.126** | **−0.1103**, **−0.1262** | ✅ |

> **Tek boşluk (hata değil):** cümle sınıfları iki gruba ayırıyor (sık → T≈1.5,
> anger/sadness → T≈1.7–1.8) ama **Surprise (n=329) 1.622'de kesiyor** — iki grubun
> arasında ve hiçbirinde anılmıyor. Disgust ve Fear ise T=2.2'ye kadar hiç kesmiyor
> (`zero_crossing_T = None`), ki cümle bunu zaten "hâlâ aşırı güvenli" diye söylüyor.
> İsterseniz Surprise'ı ara bir kaleme eklemek cümleyi tamamlar.

---

## Derleme (ek not, madde 3)

> **Derleme BU MAKİNEDE YAPILAMADI.** `pdflatex`/`xelatex`/`lualatex`/`latexmk`/`bibtex`/
> `biber` — hiçbiri kurulu değil. Aşağıdaki sayılar **Mac tarafının kendi son derlemesinin
> logundan** okundu (`paper/main_elsarticle.log`, **7 Ağu 15:56** — iletim özetinden yedi
> dakika sonra), yani bu benim değil sizin derlemeniz. Hiçbiri repo tarafında bir tabloya,
> figüre veya sayıya kaynak yapılmadı; yalnız sizin sorduğunuz tanıyı geri bildiriyorum.

| kalem | değer |
|---|---|
| hata (`!`) | **0** |
| LaTeX Warning | **0** |
| Overfull `\hbox` / `\vbox` | **0 / 0** |
| Underfull `\hbox` | 2 (zararsız satır aralığı) |
| çözülmeyen `\ref` / atıf | **0** |
| çoklu tanımlı etiket | **0** |
| `sec:criterion` | **.aux'ta çözülmüş** ✅ |
| sayfa | **89** |

**İki not:**

1. **Sayfa sayısı 76 değil 89.** Ek notta "son bilinen: 76" yazıyordu; log 89 diyor. 13
   sayfalık artış bu turun metin eklemeleriyle (G0 daraltması, §5.7, yeni §5.2 paragrafı,
   Ek B) uyumlu görünüyor ama doğrulaması sizde — ben yalnız sayıyı bildiriyorum.
2. **Bu figür turu yeniden derleme GEREKTİRMİYOR.** Gerçekten değişen tek dosya
   `graphical_abstract.pdf`, ve `graphical_abstract` ne `main_elsarticle.tex`'te ne
   `sections/` altında ne de `.fls` kayıt listesinde geçiyor — ayrı bir gönderim kalemi.
   Belgedeki beş figürün PDF'i içerik olarak değişmedi. Yani derleme çıktısı bu turdan
   etkilenmez.

---

## Sorunuza cevap: `two_dataset_overlay` suptitle'ı ihraç edilen PDF'te görünüyor mu?

**Hayır — p1 ile aynı şekilde kaldırılıyor.** Sebep tesadüf değil, tasarım:
`export_paper_figures.py` ayrı bir dışa aktarıcı ve figürleri üretici betiğin PNG'sinden
değil, **JSON artefaktından yeniden çiziyor**; belgelenmiş 4. kuralı *"figür içinde başlık
yok — başlıklar LaTeX caption'ına aittir."* `fig_two_dataset_overlay()` kendi figürünü
sıfırdan kuruyor, dolayısıyla üreticinin `suptitle`'ı PDF'e hiç ulaşmıyor.

**Ölçümle de doğrulandı:** yeniden üretimden sonra `two_dataset_overlay_swa.pdf`, zaman
damgası normalize edildiğinde eski dosyayla **birebir aynı**. Yani figür yeniden üretimi
makale PDF'ini değiştirmiyor.

---

Üretici betikler: `diagnostics/{graphical_abstract,two_dataset_overlay,p1_two_teacher_overlay,
export_paper_figures,verify_paper_figures,table_diff_gate}.py`
