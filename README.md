# İş Sağlığı ve Güvenliği (İSG) Takip Programı Tasarımı

Bu depo, **merkeze bağlı çoklu mutfak lokasyonları** için İSG süreçlerini uçtan uca yönetebilen bir takip programının tasarımını içerir.

## Kapsam
- Tüm lokasyonların ana ekranda izlenmesi
- İş kazası kayıtlarının girilmesi ve takibi
- Toplu çalışan listesi yükleme (CSV/Excel)
- Merkez ve lokasyon bazlı raporlama

Detaylar için: [`docs/isg-uygulama-tasarimi.md`](docs/isg-uygulama-tasarimi.md)

## Veri Modeli
Önerilen veritabanı şeması için: [`db/schema.sql`](db/schema.sql)

## Önerilen Sonraki Adım
Bu tasarım onaylandıktan sonra aşağıdaki teknik adımlar izlenebilir:
1. UI wireframe'lerinin Figma'da çizimi
2. Backend API'nin FastAPI / Node.js ile iskelet geliştirmesi
3. Frontend panelinin React + TypeScript ile geliştirilmesi
4. Lokasyon sorumluları ile pilot kullanım
