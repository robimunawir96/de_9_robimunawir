# Data Engineering Proyek: Analisis E-commerce Olist

## Inisialisasi Docker
docker compose up airflow-init
docker compose up

## Deskripsi
Proyek ini menggunakan dataset e-commerce untuk menganalisis:
- Segmentasi Pelanggan berdasarkan RFM
- Analisis SLA Pengiriman & Kinerja Logistik
- Review & Kepuasan Pelanggan

## Teknologi
- Apache Airflow
- PostgreSQL
- Grafana
- Docker
- Python

## Struktur
- `dags/`: DAG Airflow
- `etl_scripts/`: Script Extract, Transform, Load
- `scripts/`: SQL pembuatan tabel
- `data/`: Dataset mentah (CSV)
- `logs/`: Log dari Airflow
