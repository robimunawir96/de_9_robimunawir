import pandas as pd
import os
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

def extract_rfm():
    try:
        engine = create_engine(
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
        
        # Load CSV
        customers = pd.read_csv('/opt/airflow/data/olist_customers_dataset.csv')
        orders = pd.read_csv('/opt/airflow/data/olist_orders_dataset.csv')
        order_items = pd.read_csv('/opt/airflow/data/olist_order_items_dataset.csv')

        # Bersihkan string 'NaN' (jika ada)
        customers.replace('NaN', pd.NA, inplace=True)
        orders.replace('NaN', pd.NA, inplace=True)
        order_items.replace('NaN', pd.NA, inplace=True)

        # Drop nilai null dan duplikat
        customers.dropna(inplace=True)
        orders.dropna(inplace=True)
        order_items.dropna(inplace=True)

        customers.drop_duplicates(inplace=True)
        orders.drop_duplicates(inplace=True)
        order_items.drop_duplicates(inplace=True)
        
        # Simpan ke PostgreSQL
        engine = create_engine(
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
        
        customers.to_sql("raw_customers", engine, if_exists="replace", index=False)
        orders.to_sql("raw_orders", engine, if_exists="replace", index=False)
        order_items.to_sql("raw_order_items", engine, if_exists="replace", index=False)

        logging.info("Ekstraksi dan pembersihan RFM (null, duplikat, 'NaN' string) selesai.")

    except Exception as e:
        logging.error(f"Gagal extract RFM: {e}")

if __name__ == "__main__":
    extract_rfm()
