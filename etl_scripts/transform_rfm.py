import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os
import logging

logging.basicConfig(level=logging.INFO)

def transform_rfm():
    try:
        engine = create_engine(f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")

        query = """
        SELECT o.customer_id, o.order_id, o.order_purchase_timestamp
        FROM raw_orders o
        WHERE o.order_status = 'delivered'
        """

        df = pd.read_sql(query, engine)
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

        snapshot_date = df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
        rfm = df.groupby('customer_id').agg({
            'order_purchase_timestamp': [
                lambda x: (snapshot_date - x.max()).days,  # Recency
                'count'                                   # Frequency
            ]
        })
        rfm.columns = ['recency', 'frequency']
        rfm = rfm.reset_index()

        # Tambahkan kolom monetary dummy (karena tidak ada nilai transaksi langsung di orders)
        rfm['monetary'] = rfm['frequency'] * 100

        # Segmentasi
        rfm['rfm_score'] = (
            rfm['recency'].rank(ascending=False) // (len(rfm) // 4 + 1)).astype(int).astype(str) + \
            (rfm['frequency'].rank(ascending=True) // (len(rfm) // 4 + 1)).astype(int).astype(str)

        rfm.to_sql("rfm_cleaned", engine, if_exists="replace", index=False)
        logging.info("Transformasi RFM selesai.")
    
    except Exception as e:
        logging.error(f"Gagal transform RFM: {e}")

if __name__ == "__main__":
    transform_rfm()
