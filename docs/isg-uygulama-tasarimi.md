# İSG Takip Programı Tasarımı

## 1) Amaç
Merkeze bağlı mutfak işletmelerinde iş sağlığı ve güvenliği süreçlerini merkezi bir sistemde toplamak:
- Tüm lokasyonların tek ekranda durum görünürlüğü
- İş kazalarının standart formatta kaydı
- Çalışan bilgilerinin toplu yüklenmesi
- Uygunsuzluk, aksiyon ve kapanış takibi

## 2) Kullanıcı Rolleri
1. **Merkez Admin**
   - Tüm lokasyonları görüntüler
   - Tüm kaza kayıtlarına erişir
   - Toplu çalışan içe aktarma yapar
   - Raporları dışa aktarır
2. **Lokasyon Yöneticisi**
   - Sadece kendi lokasyonunu görür
   - Kaza kaydı açar/günceller
   - Çalışan listesine lokasyon bazlı ekleme yapar
3. **İSG Uzmanı**
   - Kaza inceleme notları girer
   - Kök neden ve aksiyon planı oluşturur
4. **Okuyucu / Denetçi**
   - Sadece görüntüleme ve rapor alır

## 3) Ana Sayfa (Dashboard)
Kullanıcının ilk açılışta gördüğü ekran:
- **Lokasyon kartları listesi (grid)**
  - Lokasyon adı
  - İl/ilçe
  - Son 30 gün kaza adedi
  - Açık aksiyon adedi
  - Son denetim tarihi
  - Risk seviyesi (Düşük / Orta / Yüksek)
- **Filtreler**
  - Bölge, şehir, marka, risk seviyesi
  - Tarih aralığı
- **Harita görünümü (opsiyonel)**
  - Lokasyon pinleri
  - Renk kodlu risk durumu
- **Özet metrikler (üst bant)**
  - Toplam lokasyon
  - Aktif çalışan
  - Açık kaza incelemesi
  - Kapanmamış düzeltici faaliyet

> Kullanıcı beklentinize göre “tüm lokasyonları ana sayfada görebilme” gereksinimi bu dashboard yapısıyla karşılanır.

## 4) İş Kazası Kayıt Modülü
### 4.1 Zorunlu Alanlar
- Kaza No (otomatik)
- Lokasyon
- Kaza tarihi ve saati
- Kaza yeri (mutfak, depo, sevkiyat vb.)
- Etkilenen çalışan(lar)
- Olay tipi (kesik, yanık, düşme, çarpma, kimyasal maruziyet vb.)
- Olay açıklaması
- İlk müdahale bilgisi
- Hastane/rapor bilgisi (var/yok)
- İş gücü kaybı gün sayısı
- Kaza şiddeti (hafif/orta/ağır)
- Kaza nedeni (insan, ekipman, proses, çevre)

### 4.2 Süreç Akışı
1. Kaza kaydı açılır
2. İSG uzmanına otomatik bildirim gider
3. İnceleme ve kök neden analizi tamamlanır
4. Düzeltici/önleyici faaliyet (DÖF) atanır
5. Son tarih ve sorumlu belirlenir
6. Kapanış onayı ile kayıt kapanır

### 4.3 Ek Özellikler
- Dosya ekleme (fotoğraf, tutanak, doktor raporu)
- Benzer olay önerisi (aynı lokasyon/aynı neden)
- Geciken aksiyonlar için e-posta/uygulama içi uyarı

## 5) Toplu Çalışan Listesi Yükleme
### 5.1 Desteklenen Formatlar
- CSV
- XLSX (arka planda CSV’ye dönüştürülebilir)

### 5.2 Beklenen Kolonlar
- `employee_id` (zorunlu, tekil)
- `full_name` (zorunlu)
- `national_id` (opsiyonel, maskeleme önerilir)
- `location_code` (zorunlu)
- `department` (zorunlu)
- `position` (zorunlu)
- `employment_start_date` (zorunlu)
- `phone` (opsiyonel)
- `email` (opsiyonel)
- `is_active` (zorunlu: true/false)

### 5.3 Yükleme Kuralları
- Aynı `employee_id` varsa güncelleme yapılır (upsert)
- Geçersiz satırlar raporlanır, valid satırlar içe alınır
- Önizleme ekranı: “Toplam satır / Başarılı / Hatalı”
- Hata raporu indirilebilir (`row_number`, `error_reason`)

## 6) Temel Ekranlar
1. **Giriş / Yetkilendirme**
2. **Ana sayfa (lokasyon görünümü)**
3. **Lokasyon detay sayfası**
4. **İş kazası listeleme**
5. **Yeni kaza kaydı formu**
6. **Kaza detay + inceleme + aksiyonlar**
7. **Çalışan listesi**
8. **Toplu çalışan yükleme ekranı**
9. **Raporlar ve dışa aktarma**
10. **Ayarlar (rol, lokasyon, kategori yönetimi)**

## 7) Raporlama
- Lokasyon bazlı kaza sıklık oranı
- Kaza tipi dağılımı
- Kök neden kırılımı
- İş gücü kaybı toplam gün
- Aksiyon kapanış performansı (SLA)
- Aylık/çeyreklik trend grafikleri

Dışa aktarma: PDF ve Excel.

## 8) Bildirim ve Hatırlatmalar
- Yeni kaza kaydı açıldığında ilgili rol gruplarına bildirim
- Aksiyon son tarihinden 3 gün önce hatırlatma
- Gecikmiş aksiyonlar için günlük özet
- Aylık yönetim raporu e-posta planlaması

## 9) Güvenlik ve Uyumluluk
- Rol bazlı erişim kontrolü (RBAC)
- KVKK kapsamında kişisel veri minimizasyonu
- Hassas alanlar için maskeleme (TCKN, sağlık bilgisi)
- Audit log (kim, ne zaman, hangi kaydı değiştirdi)
- Yedekleme ve felaket kurtarma planı

## 10) Teknik Mimari Önerisi
- **Frontend:** React + TypeScript + Ant Design
- **Backend:** FastAPI (Python) veya NestJS (Node.js)
- **DB:** PostgreSQL
- **Dosya Depolama:** S3 uyumlu obje depolama
- **Kimlik Doğrulama:** JWT + refresh token
- **Raporlama:** Metabase/Power BI entegrasyonu (opsiyonel)

## 11) Örnek API Uçları
- `GET /api/locations` → tüm lokasyonlar
- `GET /api/dashboard/summary` → ana sayfa metrikleri
- `GET /api/incidents` → kaza listesi
- `POST /api/incidents` → yeni kaza kaydı
- `GET /api/incidents/{id}` → kaza detayı
- `POST /api/incidents/{id}/actions` → aksiyon ekleme
- `POST /api/employees/import` → toplu çalışan yükleme
- `GET /api/employees/import/{job_id}` → yükleme sonucu

## 12) MVP (İlk Yayın) İçeriği
1. Rol bazlı giriş
2. Lokasyon dashboard
3. Kaza kayıt ekleme/listeleme/detay
4. Toplu çalışan yükleme + hata raporu
5. Temel raporlar (kaza adedi, tip dağılımı, açık aksiyonlar)

## 13) Faz-2 Önerileri
- Mobil uygulama (lokasyondan hızlı bildirim)
- QR kod ile ekipman denetim takibi
- Eğitim modülü (zorunlu İSG eğitimleri)
- Kestirimsel analiz (yüksek riskli lokasyon tahmini)

---

## Ek: Örnek CSV Şablonu
```csv
employee_id,full_name,national_id,location_code,department,position,employment_start_date,phone,email,is_active
E1001,Ahmet Yılmaz,12345678901,LOC-IST-01,Mutfak,Aşçı,2023-04-05,5551234567,ahmet@example.com,true
E1002,Ayşe Demir,98765432100,LOC-ANK-02,Depo,Depo Sorumlusu,2024-01-12,5559876543,ayse@example.com,true
```
