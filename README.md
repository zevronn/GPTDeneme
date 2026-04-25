# İSG Takip Programı (Demo)

Bu proje, merkeze bağlı mutfak işletmeleri için hazırlanmış **çalıştırılabilir demo** bir İSG takip uygulamasıdır.

## Özellikler
- Ana sayfada tüm lokasyonları kart görünümünde listeleme
- İş kazası kaydı ekleme
- CSV ile toplu çalışan yükleme (upsert)

## Kurulum ve Çalıştırma
> Gereksinim: Python 3.10+

1. Sanal ortam oluştur:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Bağımlılıkları yükle:
```bash
pip install -r requirements.txt
```

3. Uygulamayı başlat:
```bash
python app/app.py --host 0.0.0.0 --port 5000
```

4. Tarayıcıdan aç:
- Öncelik: http://localhost:5000
- Alternatif: http://127.0.0.1:5000

## HTTP 403 Hatası İçin Çözüm
Eğer `127.0.0.1 erişim reddedildi (HTTP ERROR 403)` görürseniz:

1. Uygulamayı host/port belirterek başlatın:
```bash
python app/app.py --host 0.0.0.0 --port 8080
```

2. Tarayıcıda `127.0.0.1` yerine `localhost` kullanın:
- http://localhost:8080

3. Kurumsal proxy/VPN varsa geçici kapatıp tekrar deneyin.

4. Hâlâ sorun varsa terminalde şunu kontrol edin:
```bash
curl -i http://localhost:8080
```
200 dönüyorsa uygulama çalışıyordur, sorun tarayıcı/proxy katmanındadır.

## CSV Örnek Şablon
```csv
employee_id,full_name,location_code,department,position,employment_start_date,is_active
E1001,Ahmet Yılmaz,LOC-IST-01,Mutfak,Aşçı,2023-04-05,true
E1002,Ayşe Demir,LOC-ANK-01,Depo,Depo Sorumlusu,2024-01-12,true
```

## Diğer Dokümanlar
- Detay tasarım: `docs/isg-uygulama-tasarimi.md`
- Geniş şema taslağı: `db/schema.sql`
