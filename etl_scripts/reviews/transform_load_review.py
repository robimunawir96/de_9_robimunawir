import pandas as pd
import os
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)

def transform_load_review():
    try:
        engine = create_engine(
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )

        # Load data dari tabel raw_review dan tabel lain
        reviews = pd.read_sql("SELECT * FROM raw_review", engine)
        orders = pd.read_sql("SELECT order_id, customer_id, order_status FROM raw_orders", engine)
        customers = pd.read_sql("SELECT customer_id, customer_unique_id FROM raw_customers", engine)

        # Join datasets
        df = reviews.merge(orders, on='order_id', how='left')
        df = df.merge(customers, on='customer_id', how='left')

        # Kategori review berdasarkan review_score
        # berdasarkan dataset olist_order_reviews_dataset.csv skalanya 1-5
        def review_category(score):
            if score >= 4:
                return 'positive'
            elif score == 3:
                return 'neutral'
            else:
                return 'negative'

        df['review_category'] = df['review_score'].apply(review_category)

        # Filter status order yang valid
        df = df[df['order_status'].isin(['delivered', 'shipped', 'completed'])]

        # Simpan hasil transformasi
        df.to_sql("result_review", engine, if_exists="replace", index=False)

        logging.info("Transform review selesai.")

    except Exception as e:
        logging.error(f"Gagal transform review: {e}")

if __name__ == "__main__":
    transform_load_review()
