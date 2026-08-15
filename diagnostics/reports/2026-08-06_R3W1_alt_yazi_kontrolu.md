# R3-W1 — çift-eksen alt yazısının imkânsızlık iddiası (6 Ağu 2026)

Round-2 panelinin (5 Ağu) en yüksek öncelikli, sıfır-maliyetli kalemi kapandı.

**İtiraz (R3/Perspektif koltuğu, BÜYÜK):** `fig_ferplus_dual.tex` alt yazısı *"no arm occupies
the lower-left corner: the two objectives cannot be satisfied at once"* diyor. Bu bir
**imkânsızlık iddiası**, ama dayanağı dört koldan ibaret bir grid. Hakem ucuz bir çürütme
adayı da önerdi: T=0.74'te damıt, ECE'yi öğrenci-tarafı TS ile onar.

**Ön-kayıt:** A11, commit `2d6bed2` (6 Ağu 00:38). Köşenin tanımı ve üç karar kolu **tek sayı
görülmeden** yazıldı; üretici dosyası o commit'te henüz yoktu.

---

## Sonuç: ALT YAZI YANLIŞLANDI

Köşe, kolların kendi iki en iyisi: **ECE_min = 0.0185** (T=0.5063) · **JSD_min = 0.0536** (T=0.74).

| aday | ECE | JSD | köşeyi işgal? |
|---|---|---|---|
| T=0.26 + TS | 0.0266 | 0.0540 | hayır (ECE −0.0049) |
| T=0.5063 + TS | 0.0296 | 0.0543 | hayır (ECE −0.0079) |
| **T=0.74 + TS** *(hakemin adayı)* | 0.0246 | 0.0546 | **hayır** (JSD −0.0002) |
| **T=1.0 + TS** *(native)* | **0.0203** | **0.0545** | **EVET** |

Alt yazının cümlesi post-hoc ölçekleme içeren tarifler için doğru değil; yeniden yazılmalı.

### Üç şey, sırayla

**1. Marj dar — ve öyle yazıldı.** Kazanan nokta iki eksende de en iyi kolun *üstünde* duruyor
(+0.0018 ECE, +0.0009 JSD); testi yalnız tohum gürültüsünün içinde kaldığı için geçiyor.
Savunulabilir cümle **"iki optimumdan da tohum gürültüsü içinde ayırt edilemez"**, "ikisini de
dövdü" değil. İmkânsızlık iddiasını yanlışlamaya bu yeter (alt yazı *cannot* diyor) ama bir
üstünlük sonucu değil ve öyle yazılmayacak.

**2. Hakemin kendi adayı geçmedi.** T=0.74+TS ECE'yi +0.0022 ile geçiyor, JSD'yi −0.0002 ile
kaçırıyor. Alt yazıyı çürüten kol, tahtadaki **en ucuz tarif**: öğretmen tarafında hiçbir
müdahale içermeyen native T=1. Yani hakem sonuçta haklı, mekanizmada değil.

**3. İstenmeyen ama daha ağır bulgu — TS, JSD eksenini çökertiyor.**

| | JSD aralığı |
|---|---|
| ölçeklemeden önce (4 kol) | 0.0536 – 0.0737 → **0.0201** |
| tek çapraz-uyarlanmış skaler sonrası | 0.0540 – 0.0546 → **0.0005** |

**37× daralma**; dört kol da aynı değere düşüyor. Bu veri kümesinde kollar arası insan-hizası
farkının neredeyse tamamı bir **güven-ölçeği** etkisi ve tek bir öğrenci-tarafı skaler onu
yeniden üretiyor. §5.7 bunun yalnız T=1 hâlini raporlamıştı; dört kola genişletilince bulgu
tek karşılaştırma değil, örüntünün kendisi oluyor.

Bu, öğretmen-tarafı kaldıracın aleyhine bir sonuç. Beyan "hesaplanan hiçbir nokta rapor dışı
bırakılamaz" diyordu; yazılıyor.

---

## Doğrulama

- **R0-1 birebir yeniden üretildi.** Yayımlanmış T=1 satırı (ham ve TS, iki eksen, üç tohum)
  tıpatıp aynı çıktı. Sebep yapısal: bölme, fit ve ölçüm fonksiyonları
  `student_ts_baseline.py`'den **ithal ediliyor**, kopyalanmıyor — kod yolu birebir aynı.
  (Aynı disiplin P6.1'de de uygulandı.)
- **Tablo kapısı: 459 → 482 hücre, 23 APPEARED, 0 MOVED, 0 VANISHED.** Dört kolun mevcut
  sayıları oynamadı.
- **Sızıntısız protokol korundu:** T_s raporlama kümesinde fit edilmedi; sha256(dosya adı)
  sıralı ikiye bölme, bir yarıda fit / diğerinde ölçüm, iki yönde, her örnek tam bir kez.
- **GPU yok, eğitim yok** — logitler 4 Ağu'daki R3-3 turundan önbellekli.

## Kapsam sınırı

Yalnız FERPlus. RAF-DB'de öğrenci-tarafı TS'i fit edecek temiz bir bölme yok — bu §5.7'nin
kendi gerekçesi, burada da geçerli.

---

## Makale tarafına düşen

1. **`fig_ferplus_dual.tex` alt yazısı yeniden yazılmalı.** "cannot be satisfied at once"
   cümlesi kalkacak. Önerim: *"no arm occupies the lower-left corner"* kalsın (bu doğru, dört
   kol için), ardından post-hoc ölçeklemenin köşeye tohum gürültüsü içinde ulaştığı eklensin.
2. **§5.7'nin argümanı gözden geçirilmeli.** JSD ekseninin çöküşü, "öğretmen-tarafı kaldıraç
   temsili şekillendiriyor, öğrenci-tarafı ölçekleme dokunamıyor" cümlesini bu veri kümesinde
   zayıflatıyor. §5.7 zaten öğrenci-tarafı TS'in JSD'de kazandığını dürüstçe raporluyordu;
   yeni tablo bunu tek karşılaştırmadan örüntüye çıkarıyor.
3. Kalan kaldıraç gerekçeleri **etkilenmiyor**: doğruluk (+0.40 pp damıtma, +0.53 pp öğretmen
   seçimi), temiz bölme gerektirmemesi, ve eğitim-zamanı hedefi şekillendirmesi.

Üretici: `diagnostics/r3w1_joint_optimum.py` · tablo: `paper_tables/r3w1_joint_optimum.md`
