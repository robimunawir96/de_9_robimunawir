import pandas as pd
import psycopg2
import logging
from dotenv import load_dotenv
import os

load_dotenv()

def extract_clean_reviews():
    try:
        df_reviews = pd.read_csv('/opt/airflow/data/olist_order_reviews_dataset.csv', parse_dates=['review_creation_date'])
        df_orders = pd.read_csv('/opt/airflow/data/olist_orders_dataset.csv', parse_dates=['order_purchase_timestamp'])

        df = pd.merge(df_reviews, df_orders, on='order_id', how='left')
        df = df[['review_id', 'order_id', 'review_score', 'review_comment_title',
                 'review_comment_message', 'review_creation_date', 'customer_id', 'order_purchase_timestamp']]
        df = df.dropna(subset=['review_score'])  # Minimal pembersihan

        # Simpan ke PostgreSQL
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        cur = conn.cursor()
        cur.execute("DELETE FROM raw_reviews;")  # Kosongkan jika sudah ada
        conn.commit()

        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO raw_reviews (
                    review_id, order_id, review_score, review_comment_title,
                    review_comment_message, review_creation_date, customer_id, order_purchase_timestamp
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, tuple(row))

        conn.commit()
        cur.close()
        conn.close()
        logging.info("Extract & clean reviews selesai.")
    except Exception as e:
        logging.error(f"Gagal extract & clean reviews: {e}")
        raise
