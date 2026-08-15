# Başlık v2 — teyit raporu (4 Ağu 2026)

Kaynak: `planning/ide_prompt_baslik_v2.md` (4 Ağu 13:28).

**Yeni başlık (uygulanan dize):**
> Teacher-Side Logit Scaling Governs Student Calibration in Knowledge Distillation:
> Dose-Response Evidence from Facial Expression Recognition

Eski başlık, alt başlığıyla birlikte değişti: *"Teacher Calibration Governs Student
Calibration in Knowledge Distillation: **Causal** Evidence…"* → *"…: **Dose-Response**
Evidence…"*.

---

## Görev 1 — repo taraması: değişen dosyalar

| dosya | ne değişti |
|---|---|
| `public/calibration-law-fer/README.md:5-6` | makale başlığı bloğu → v2 (ana cümle + alt başlık) |
| `diagnostics/reports/2026-08-04_gonderim_gunu_dizisi.md:26` | kayıtlı yeniden-kurulum açıklaması → v2 |
| `diagnostics/reports/2026-08-04_gonderim_gunu_dizisi.md:95` | `gh repo create` komutundaki `--description` argümanı → v2 |

Bunlar başlığın geçtiği **tek** yerlerdi. Tarama iki depoda ve Drive'daki `repo_export`
klasöründe yapıldı; `PREREGISTRATIONS.md` dâhil tarihli beyan kayıtlarında başlık hiç
geçmiyor, dolayısıyla dokunulacak bir şey de çıkmadı — geriye dönük değiştirme riski oluşmadı.

## Görev 2 — depo açıklaması

`gh repo edit` ile güncellendi ve uzaktan **doğrulandı**:

```
Code and pre-declaration records for Teacher-Side Logit Scaling Governs Student Calibration in Knowledge Distillation (Neurocomputing submission)
```

Final dizideki kayıtlı yeniden-kurulum açıklaması da aynı dizeyle güncellendi (yukarıdaki
runbook satırları), yani gönderim günü depo yeniden kurulduğunda v2 açıklamayla açılacak.

## Görev 3 — STATUS bekleyen listesi

`diagnostics/status_queue.txt` dört gerçekle tazelendi:
1. **Başlık v2** kalemi eklendi (aşağıdaki açık kalemle birlikte),
2. **silme = gönderim günü final dizisinde**, v2 açıklamayla kurulacak,
3. **gönderim tarihi hedef değil** — P6 entegrasyonu + konsolide tur bitmeden tarih verilmiyor
   (önceki "~8–9 Ağu" satırı bu gerekçeyle düşürüldü),
4. **R3-4 planı değişmedi**, 42/42 sonrası.

Ayrıca figür rötuşları satırı gerçeğe çekildi: (a)(b)(c) 4 Ağu'da yapıldı ve doğrulandı.

---

## ⚠️ Açık kalem — senin kararın, ben değiştirmedim

Başlık artık mekanizmayı adlandırıyor (*teacher-side logit scaling*), ama **dört yerde** hâlâ
eski iddia cümlesi duruyor:

| dosya | satır | metin |
|---|---|---|
| `diagnostics/graphical_abstract.py` | 42 | `HEADLINE_1 = "Teacher calibration governs student calibration"` |
| `diagnostics/p1_two_teacher_overlay.py` | 244 | figür başlığı, aynı cümle |
| `diagnostics/two_dataset_overlay.py` | 351 | `suptitle`, "…in BOTH directions and on…" |
| `ferplus_dose_response_queue.ps1` | 17 | B-007 iddiasını anan yorum satırı |

**Bunlar başlık değil, iddia cümlesi** — o yüzden kendiliğimden dokunmadım; ikisi farklı
şeyler ve hangisinin kalacağı editoryal bir karar. Ama biri gözden kaçmasın diye söylüyorum:
**grafik özet gönderim paketine giriyor** ve başlığı "Teacher-Side Logit Scaling Governs…"
olan bir makalenin grafik özeti "Teacher calibration governs…" diyorsa, bu hakemin göreceği
türden bir tutarsızlık.

Üç seçenek:
1. **Değiştirme.** İddia hâlâ doğru: öğretmen kalibrasyonu öğrenciyi yönetiyor; başlık yalnız
   *nasıl manipüle ettiğimizi* adlandırıyor. Savunulabilir, ama okuyucu iki farklı cümle görür.
2. **Grafik özeti başlıkla hizala** — `HEADLINE_1` → "Teacher-side logit scaling governs
   student calibration". Tek satır, figürü yeniden üretirim (~1 dk).
3. **Dördünü birden hizala.** İki figür başlığı da değişir; `two_dataset_overlay`'in cümlesi
   "in BOTH directions" vurgusunu taşıdığı için orada yeniden yazım gerekir.

Söyle, hangisiyse uygularım. Not: `p1_two_teacher_overlay`'in başlığı ihraç edilen PDF'de
görünmüyor (dışa aktarımda figür-içi başlıklar kaldırılıyor), yani oradaki satır yalnız
tanılama PNG'sini etkiliyor.

---

## Doğrulama

- `table_diff_gate`: **432/432 hücre, sapma yok** — bu tur hiçbir sayıya dokunmadı.
- Depo açıklaması uzaktan okunarak doğrulandı.
- MANIFEST + heartbeat bu raporla **aynı ihraçta** gitti.
