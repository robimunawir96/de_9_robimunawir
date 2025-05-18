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

## Kategori Segmen RFM:
| Segment                | Kriteria Umum       | Penjelasan Singkat                                       |
| ---------------------- | ------------------- | -------------------------------------------------------- |
| **Champions**          | R ≥ 4, F ≥ 4, M ≥ 4 | Pembeli paling aktif dan bernilai tinggi.                |
| **Loyal Customers**    | F = 5               | Sangat sering membeli, pelanggan setia.                  |
| **Big Spenders**       | M = 5               | Pengeluaran tinggi, walau frekuensi/recency biasa.       |
| **Recent Customers**   | R = 5, F ≤ 2        | Baru membeli, perlu dibina loyalitasnya.                 |
| **Potential Loyalist** | R ≥ 3, F ≥ 3        | Sering & cukup baru, berpotensi menjadi pelanggan setia. |
| **At Risk**            | R ≤ 2, F ≥ 3, M ≥ 3 | Pernah aktif tapi mulai pasif.                           |
| **Can’t Lose Them**    | R = 1, F ≥ 4, M ≥ 4 | Bernilai tinggi di masa lalu, tapi sudah tidak aktif.    |
| **Hibernating**        | R ≤ 2, F ≤ 2, M ≤ 2 | Tidak aktif, pembelian jarang dan nilai rendah.          |
| **Lost**               | R = 1, F = 1, M = 1 | Tidak pernah kembali, kontribusi rendah.                 |
| **Others**             | Selain di atas      | Segmen umum.                                             |
