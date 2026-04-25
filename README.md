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
python app/app.py
```

4. Tarayıcıdan aç:
- http://127.0.0.1:5000

## CSV Örnek Şablon
```csv
employee_id,full_name,location_code,department,position,employment_start_date,is_active
E1001,Ahmet Yılmaz,LOC-IST-01,Mutfak,Aşçı,2023-04-05,true
E1002,Ayşe Demir,LOC-ANK-01,Depo,Depo Sorumlusu,2024-01-12,true
```

## Diğer Dokümanlar
- Detay tasarım: `docs/isg-uygulama-tasarimi.md`
- Geniş şema taslağı: `db/schema.sql`
