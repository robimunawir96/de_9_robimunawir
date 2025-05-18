import pandas as pd
import os
import logging
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)

def extract_logistics():
    try:
        engine = create_engine(
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
        
        # Load CSV
        sellers = pd.read_csv('/opt/airflow/data/olist_sellers_dataset.csv')
        products = pd.read_csv('/opt/airflow/data/olist_products_dataset.csv')
        geolocation = pd.read_csv('/opt/airflow/data/olist_geolocation_dataset.csv')

        # Bersihkan string 'NaN' (jika ada)
        sellers.replace('NaN', pd.NA, inplace=True)
        products.replace('NaN', pd.NA, inplace=True)
        geolocation.replace('NaN', pd.NA, inplace=True)

        # Drop nilai null dan duplikat
        sellers.dropna(inplace=True)
        products.dropna(inplace=True)
        geolocation.dropna(inplace=True)

        sellers.drop_duplicates(inplace=True)
        products.drop_duplicates(inplace=True)
        geolocation.drop_duplicates(inplace=True)
        
        # Simpan ke PostgreSQL
        sellers.to_sql("raw_sellers", engine, if_exists="replace", index=False)
        products.to_sql("raw_products", engine, if_exists="replace", index=False)
        geolocation.to_sql("raw_geolocation", engine, if_exists="replace", index=False)

        logging.info("Ekstraksi dan pembersihan Logistics (null, duplikat, 'NaN' string) selesai.")
        
    except Exception as e:
        logging.error(f"Gagal extract logistics: {e}")

if __name__ == "__main__":
    extract_logistics()
