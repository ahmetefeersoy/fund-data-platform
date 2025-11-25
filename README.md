# Fund Data Platform

Türk fon verilerini işleyen, yatırım portföylerini yöneten ve analitik metrikler hesaplayan bir veri platformu.

## Mimari

- **Dagster**: Veri toplama ve analitik pipeline'ları
- **FastAPI**: Portföy yönetimi ve analitik API'leri
- **PostgreSQL**: Veri depolama (Supabase)
- **Docker**: Konteynerizasyon

## Özellikler

### Data Ingestion
- TEFAS web sitesinden günlük fon verilerini çeker
- En eski verileri temizler
- Fon fiyatları, kategoriler ve enstrüman dağılımlarını parse eder
- PostgreSQL'e kaydeder.

### Portfolio Management
- Portföy oluşturma, güncelleme, silme (CRUD)
- Portföylere fon pozisyonları ekleme (ağırlıklarla)
- Portföy listesi ve detay görüntüleme

### Analytics
- **Risk Analizi**: Portföy risk skorları hesaplama
- **Performance Analizi**: Fon performans metrikleri
- **Alert Sistemi**: Yüksek riskli portföyleri tespit etme

## Kurulum

### Gereksinimler
- Python 3.12+
- Docker & Docker Compose
- PostgreSQL (Supabase kullanılıyor)

### Lokal Kurulum

```bash
# Virtual environment oluştur
python -m venv .venv
.\.venv\Scripts\activate

# Bağımlılıkları yükle
pip install uv
uv pip install -r pyproject.toml

# .env dosyasını oluştur
# DATABASE_URL'i ekle
```

### Docker ile Çalıştırma

```bash
# Servisleri başlat
docker compose up -d

# Logları izle
docker compose logs -f

# Servisleri durdur
docker compose down
```

## API Endpoints

### Portfolios

**POST /portfolios**
```json
{
  "positions": [
    {"fund_code": "ABC", "weight": 0.5},
    {"fund_code": "XYZ", "weight": 0.5}
  ]
}
```

**GET /portfolios** - Tüm portföyleri listele

**GET /portfolios/{id}** - Portföy detayı

**PUT /portfolios/{id}** - Portföy güncelle

**DELETE /portfolios/{id}** - Portföy sil

**GET /portfolios/{id}/risk** - Portföy risk analizi

### Alerts

**GET /alerts/portfolios** - Yüksek riskli portföyler

**GET /alerts/funds** - Düşük performanslı fonlar

## Erişim

- **FastAPI**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Dagster UI**: http://localhost:3000
- **Health Check**: http://localhost:8000/health

## Proje Yapısı

```
src/
├── case_study/
│   ├── analytics/          # Risk ve performance hesaplamaları
│   ├── database/           # SQL şemaları
│   ├── fastapi/            # API servisi
│   │   └── routers/        # Endpoint'ler
│   └── utils/              # DB bağlantısı
└── dagster/
    ├── ingestion/          # Veri toplama job'ları
    └── analytics/          # Analitik job'lar
```

## Geliştirme

```bash
# FastAPI'yi dev modunda çalıştır
uvicorn src.case_study.fastapi.main:app --reload

# Dagster UI'ı başlat
dagster dev -w workspace.yaml

# Test portföyleri oluştur
python create_portfolios.py
```

