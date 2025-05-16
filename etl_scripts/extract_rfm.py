import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))

logging.basicConfig(level=logging.INFO)

def extract_clean_rfm():
    try:
        customers = pd.read_csv('/opt/airflow/data/olist_customers_dataset.csv')
        orders = pd.read_csv('/opt/airflow/data/olist_orders_dataset.csv')
        
        # Drop NA dan duplikat
        customers.dropna(inplace=True)
        orders.dropna(inplace=True)
        customers.drop_duplicates(inplace=True)
        orders.drop_duplicates(inplace=True)

        # Simpan ke PostgreSQL
        engine = create_engine(f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")
        customers.to_sql("raw_customers", engine, if_exists="replace", index=False)
        orders.to_sql("raw_orders", engine, if_exists="replace", index=False)

        logging.info("Ekstraksi dan pembersihan RFM selesai.")
    
    except Exception as e:
        logging.error(f"Gagal extract RFM: {e}")

if __name__ == "__main__":
    extract_clean_rfm()
