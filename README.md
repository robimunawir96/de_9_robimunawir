# 🛠️ Data Engineering untuk Insight E-Commerce
Proyek ini merupakan implementasi end-to-end data engineering dengan fokus pada segmentasi pelanggan, analisis logistik (SLA pengiriman), dan analisis kepuasan pelanggan menggunakan dataset e-commerce Olist.

## 📦 Deskripsi
Dataset yang digunakan berasal dari Olist Store Dataset. Dataset mencakup:
orders_dataset
customers_dataset
order_items_dataset
products_dataset
sellers_dataset
order_reviews_dataset
order_payments_dataset
geolocation_dataset
Semua file CSV diletakkan di dalam folder data/.

## 📊 Diagram Arsitektur Transformasi Data


🛠️ Teknologi yang Digunakan
| Teknologi          | Fungsi                                     |
| ------------------ | ------------------------------------------ |
| Python             | Scripting dan pemrosesan data              |
| Apache Airflow     | Orkestrasi ETL harian                      |
| PostgreSQL         | Database relasional untuk penyimpanan data |
| Docker             | Containerisasi environment                 |
| Grafana            | Visualisasi metrik dan analisis            |
| Pandas, SQLAlchemy | Manipulasi data dan koneksi database       |

## 📦 Kategori Segmen RFM:
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

## ✅ Status
| Komponen               | Status    |
| ---------------------- | --------- |
| Struktur Docker        | ✅ Selesai |
| ETL RFM                | ✅ Selesai |
| ETL Logistics (SLA)    | ✅ Selesai |
| ETL Review Pelanggan   | ✅ Selesai |
| PostgreSQL & Table Raw | ✅ Selesai |
| Dashboard Grafana      | ✅ Selesai |
| Dokumentasi            | ✅ Selesai |
