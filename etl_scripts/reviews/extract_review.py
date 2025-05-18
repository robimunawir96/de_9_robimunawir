import pandas as pd
import os
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)

def extract_review():
    try:
        engine = create_engine(
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )

        # Baca file csv
        reviews = pd.read_csv('/opt/airflow/data/olist_order_reviews_dataset.csv')

        # Bersihkan data: hapus null, duplikat, dan 'NaN' string
        reviews.dropna(inplace=True)
        reviews = reviews[~reviews['review_comment_message'].astype(str).str.lower().isin(['nan', 'none'])]
        reviews.drop_duplicates(inplace=True)

        # Simpan ke tabel raw_review
        reviews.to_sql("raw_review", engine, if_exists="replace", index=False)

        logging.info("Extract review selesai.")

    except Exception as e:
        logging.error(f"Gagal extract review: {e}")

if __name__ == "__main__":
    extract_review()
