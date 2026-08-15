# Çalışmanın durumu — 1 Ağustos 2026, 02:20

Kampanyanın bütünü: neyin kurulduğu, neyin sonuçsuz olduğu, neyin uçuşta olduğu, neyin borç
kaldığı. P5 hükmü **bu rapora dahil değil** — 6/6 tamamlanmadan hiçbir P5 değeri okunmadı.

---

## 1. Tek bakışta

| eksen | durum |
|---|---|
| Koşu defteri | **131 koşu** donmuş denetim kümesinde (`AUDIT_CUTOFF 2026-07-31-06-00-00`) |
| Uçuşta | P5 oracle replikasyonu **5/6** bitti, sonuncusu ~04:19'da biter |
| Tablo kapısı | `table_diff_gate.py` → **266/266 hücre** baseline ile aynı, sapma yok |
| Figür kapısı | `verify_paper_figures.py` → **8 figür, 0 hata** (vektör, TrueType, ≥7 pt) |
| Versiyon kontrolü | git + uzak repo + 2 dondurma tag'i · çalışma ağacı temiz |
| Makale kanalı | tek yönlü ihraç bandı, 43 dosya, MANIFEST SHA-256'lı |
| Ana borç | `BULGULAR.md` (28 Tem'de kalmış), `claims.md` Open bölümü, gri provalar |

## 2. Kurulmuş bulgular — makalede "kuruluş" kalitesinde yazılabilir

**(a) Öğretmen kalibrasyonu nedensel, ve ucuza düzeltilebilir (Phase B3 — kampanyanın çapası).**
Stage1 öğretmenine post-hoc sıcaklık ölçeklemesi uygulandı; mimari, tarif, veri, tohum sabit.
Öğrenci half-B'de **89.63% / ECE 0.0558 → 90.22% / ECE 0.0293**. Tek değişken öğretmenin
kalibrasyonu olduğu için bu korelasyon değil müdahale sonucu. Kampanyanın en güçlü tek cümlesi.

**(b) Öğretmen ECE'si transferi yordar, öğretmen doğruluğu yordamaz (3/3 öğretmen, monoton).**
VAE9182 üçünün **en düşük doğruluklu** öğretmeni (91.82% vs 92.24/92.01) ama en iyi kalibre olanı
ve en iyi transfer edeni. Öğrenci ECE'leri: stage1 0.0745, primary 0.0755, vae9182 0.0278.
Seçim ölçütü "hangi öğretmen daha doğru" değil, "hangi öğretmen daha kalibre".

**(c) ECE farkı kafa mimarisinden değil, tarif yığınından geliyor (Phase C köprü öğretmeni).**
Köprü = VAE kafası + Primary'nin birebir VICH tarifi + aynı tohum. Ölçüm: **öz-doğruluk 92.47%,
ECE(T=1) 0.0391, T\* 1.253** → ön-kayıtlı **RECIPE bandına** (0.038±0.010) tam oturuyor, HEAD
bandına (0.015) yakın bile değil. Primary (0.0396 / T\*1.26) ile pratik olarak aynı; VAE9182'ye
(0.0136 / T\*0.98) hiç benzemiyor. Kafa tipini çevirmek kalibrasyonu **değiştirmiyor** → kafa
mimarisi eleniyor. "İyi olasılıksal kafa" hikâyesi bu makaleden çıkıyor, Study-2'ye gidiyor.
(Artık: VAE9182'nin üstünlüğü içinde tarif-mi-tohum-mu ayrıştırılmadı — EAAI'yi bloklamıyor.)

**(d) Seçim iyimserliği ölçüldü ve dondurma kümesine karşı dayanıklı.**
`best − last` = **+0.766 ± 0.431 pp**, N=131. Dahil etme kümesine duyarsız: 116/125/131 →
+0.781 / +0.769 / +0.766 (yayılım 0.015 pp). Bu yüzden **@swa birincil**, `best` değil —
`best` raporlanan görüntülerde argmax val-acc, yani doğruluk ekseninde seçim iyimserliği taşıyor.

**(e) Kapasite yasası küçük öğrencide de geçerli (T10a kalem i).** İki fit'in en büyük artığı
hücrelerin **en küçük** tohum sd'sinden bile kat kat küçük; doğrusallık fit'in üç noktaya
oturmasından değil ilişkinin kendisinden geliyor. "Yasa büyük-öğrenci artefaktı" alternatifi eleniyor.

**(f) Gate ölü — ama "işe yaramıyor" diye değil, "kalibrasyonu BOZUYOR" diye.** Üç sinyal
kalitesinde test edildi, mükemmel-bilgi (oracle) dahil. Bu, D1'in kapanış gerekçesi olarak
metne böyle yazılacak. **Uyarı:** zarar VAE9182'ye koşullu; stage1/primary'de tekrarlanmadı —
P5 tam olarak bunu ölçüyor.

## 3. Açıkça sonuçsuz / sınırlı — bu haliyle yazılacak, güçlendirilmeyecek

- **T10a kalem (ii): eğimin kapasiteyle değişip değişmediği ÖLÇÜLEMEDİ.** Fark gürültü zarfının
  içinde. *Çözünmüyor ≠ fark yok*: bu bir null bulgu değil, **yapılamamış bir test**. "Eğim
  kapasiteyle değişmiyor" cümlesi bu veriyle yazılamaz.
- **T10a init confound'u.** `b_w050` scratch, `b_2248` ön-eğitimli — iki eğim hem kapasitede hem
  başlatmada farklı. Ayrıştırmak 2.248 M'de scratch bir doz-yanıt gerektirir (**4 koşu,
  başlatılmadı, onay bekliyor**). Ayrıca w050'nin iki hücresi n=2.
- **Gerçek-sinyal gate hücreleri n=1.** n=3'e çıkarmak **10 koşu** ister; başlatılmadı.
- **İsimlendirme kararsız.** UGKD/SAGE/GUIDE/GUARD dördü de gate-kahraman varsayımına dayanıyordu,
  D1=B ile dördü de öldü. Yeni ad g2g/kalibrasyon ekseninde olmalı — henüz seçilmedi.

## 4. Uçuşta

P5 oracle replikasyonu (2 öğretmen × 3 tohum = 6 koşu): **5/6 tamam** (stage1 ×3, primary
seed42+seed1), primary seed43 epoch 71/400'de, 21.9 sn/epoch, **ETA 04:19**. Donmuş karar kuralı
koşudan önce yazıldı ve değiştirilmedi: her kol kendi öğretmeninin `cw=none` kontrol ECE tohum
sd'sine karşı (bar stage1 **0.0021**, primary **0.0033**); *3/3 aynı işaret VE |ΔECE| ≥ 2× bar* →
KURULU, aksi halde ÇÖZÜNMEDİ. İki sonucun metni de önceden sabit.

## 5. Altyapı — bu kampanyanın asıl ürünü

- **`diagnostics/` katmanı:** koşu defteri, kâğıt tabloları, 266 hücrelik fark kapısı, donmuş
  seçim denetimi, payda tablosu, ön-kayıt envanteri + blok beyanları, 8 figür üreticisi + kapısı.
- **Payda konvansiyonu tek:** her tek-hücre oranı tedavinin **kendi kontrol kolunun** tohum sd'sine
  bölünür (öğretmen başına, aynı sınıf-ağırlığı kipinde, @swa). T5a'nın öğretmenler-arası iddiası
  havuzlanmış paydayı kullanır (acc 0.279 pp, ECE 0.0016). **Hangisinin kullanıldığı her cümlede
  yazılacak** — "74×" tam bu yazılmadığı için hiçbir konvansiyonla tutmuyordu.
- **Ön-kayıt zinciri:** `preregistration_blocks.csv` bir **beyandır, çıkarım değil** — koşu adından
  tahmin edilmez, elle ve tarihli yazılır; atanmamış koşu görünür bir boşluktur, sessiz varsayılan değil.
- **Yeni (31 Tem):** git commit'leri + uzak repo + `audit-frozen-131` / `p5-predeclared` tag'leri;
  tek yönlü Drive ihraç bandı + SHA-256'lı MANIFEST; ters kanal (raporlar dosya olarak);
  `STATUS.md` kalp atışı.

## 6. Borç — bitmiş çalışmanın bayat kalan kaydı

| artefakt | sorun |
|---|---|
| `BULGULAR.md` (28 Tem) | **En bayat dosya.** B-002 hâlâ "üç sinyalde de kazanç yok" diyor — P2'nin ECE-zarar bulgusuyla çelişiyor. B-014 hâlâ n=101 / +0.792 ± 0.464 pp; doğrusu **n=131 / +0.766 ± 0.431**. P1–P5 kampanyaları dosyada hiç yok. |
| `claims.md` Open bölümü | Üç kalemin üçü de kapanmış: köprü "RESOLVED" yazdığı hâlde Open'da duruyor; Phase B nedensel test ve Phase A tohum varyansı çoktan bitti. |
| `STATUS.md` (22 Tem) | §12 "kampanya fırlatmaya hazır değil" hükmü aşıldı; ya tazelenmeli ya "superseded" damgalanmalı. |
| `PREREGISTRATIONS.md` s.11 | *"poster-var git deposu değil"* — yanlış. Bölümün mantığı geçerli, yalnız gerekçe cümlesi değişecek (bkz. `reports/2026-07-31_git_provenance.md`). |
| Gri provalar | 5 PDF 31 Tem 12:15'te yenilendi, provalar 29 Tem 15:07'de kaldı → **5/8 bayat**. `verify_paper_figures.py --grey` bir kez koşturulacak. |
| `literature_fer_models.csv` | Bilinçli olarak boş; satırlar makalelerden transkribe edilecek — **kullanıcının kalemi**. |

## 7. Metne bağlayıcı geri çekmeler — makaleye elle taşınacak

1. **@best/@swa payda uyuşmazlığı.** Kalibrasyon/doğruluk oranı **58.8×**; özetteki "about seven
   times" ciddi bir **eksik** ifade. ≈59× olmalı.
2. **"0.82 pp" etiketi.** Sayı doğru (0.818) ama o, `vae9182/logit_std`'in **eşleştirilmiş Δacc
   sd'si**; "kontrolünün tohum yayılımı" değil. Etiket yanlıştı.
3. **T10 sözcüksel kirlenme.** `"frontier" in run_name` filtresi 76× oranını üretiyordu; bayrak
   tabanlı filtreyle **3×**.
4. **"tohum sd'sinin bir mertebe altında"** ve **verim (throughput) iddiası** — ikisi de geri çekildi.

Makale repo'da değil: `G:\My Drive\Claude\Makale\paper\`. §5.4 düzeltmeleri oraya elle taşınacak;
kaynaklar `paper_tables/section54_numbers.md`, `paper_tables/denominator_table.md`,
`figures/_updated_2026-07-30/README.md`.

## 8. Onay bekleyen GPU işi (deney dondurması yürürlükte)

- Gerçek-sinyal gate hücrelerini n=3'e çıkarmak — **10 koşu**
- 2.248 M'de scratch doz-yanıt (T10a init confound'u) — **4 koşu**

İkisi de başlatılmadı. Dondurma gereği yalnız onaylanmış kuyruk koşar.
