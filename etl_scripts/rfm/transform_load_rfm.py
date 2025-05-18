import pandas as pd
from sqlalchemy import create_engine
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def segment(row):
    r, f, m = row['r_score'], row['f_score'], row['m_score']
    
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif f == 5:
        return 'Loyal Customers'
    elif m == 5:
        return 'Big Spenders'
    elif r == 5 and f <= 2:
        return 'Recent Customers'
    elif r >= 3 and f >= 3:
        return 'Potential Loyalist'
    elif r <= 2 and f >= 3 and m >= 3:
        return 'At Risk'
    elif r == 1 and f >= 4 and m >= 4:
        return 'Can’t Lose Them'
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Hibernating'
    elif r == 1 and f == 1 and m == 1:
        return 'Lost'
    else:
        return 'Others'

def transform_load_rfm():
    try:
        # Setup koneksi ke PostgreSQL
        engine = create_engine(
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )

        # Load raw data
        customers = pd.read_sql('SELECT * FROM raw_customers', engine)
        orders = pd.read_sql('SELECT * FROM raw_orders', engine)
        order_items = pd.read_sql('SELECT * FROM raw_order_items', engine)

        # Merge data
        merged = orders.merge(customers, on='customer_id', how='inner') \
                       .merge(order_items, on='order_id', how='inner')

        # Konversi tanggal
        merged['order_purchase_timestamp'] = pd.to_datetime(merged['order_purchase_timestamp'])

        # Hitung nilai terakhir untuk Recency
        snapshot_date = merged['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

        # Hitung RFM
        rfm = merged.groupby('customer_unique_id').agg({
            'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
            'order_id': 'nunique',
            'price': 'sum'
        }).reset_index()

        rfm.columns = ['customer_unique_id', 'recency', 'frequency', 'monetary']

        # Skor RFM (1-5)
        rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5,4,3,2,1]).astype(int)
        rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5]).astype(int)
        rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1,2,3,4,5]).astype(int)

        # Gabungkan skor RFM
        rfm['rfm_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str) + rfm['m_score'].astype(str)

        # Segmentasi
        rfm['segment'] = rfm.apply(segment, axis=1)

        # Simpan ke database
        rfm.to_sql('result_rfm', engine, if_exists='replace', index=False)

        logging.info("Transformasi RFM selesai dan disimpan ke PostgreSQL.")

    except Exception as e:
        logging.error(f"Gagal transformasi RFM: {e}")

if __name__ == "__main__":
    transform_load_rfm()