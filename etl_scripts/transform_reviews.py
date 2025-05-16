import pandas as pd
import os
from dotenv import load_dotenv
import logging
from sqlalchemy import create_engine

load_dotenv()

def transform_reviews():
    try:
        # Buat connection string SQLAlchemy
        db_url = (
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
            f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )
        engine = create_engine(db_url)

        # Ambil data dari tabel raw_reviews
        df = pd.read_sql_query("SELECT * FROM raw_reviews", engine)

        # Transformasi sentimen berdasarkan skor review
        df['sentiment'] = df['review_score'].apply(
            lambda x: 'positive' if x >= 4 else ('neutral' if x == 3 else 'negative')
        )

        # Pilih kolom yang diperlukan
        df = df[['review_id', 'order_id', 'review_score', 'sentiment', 'review_creation_date']]

        # Simpan ke tabel analytics_reviews
        df.to_sql("analytics_reviews", engine, if_exists="replace", index=False)

        logging.info("Transformasi review selesai.")
    except Exception as e:
        logging.error(f"Gagal transform reviews: {e}")
        raise
