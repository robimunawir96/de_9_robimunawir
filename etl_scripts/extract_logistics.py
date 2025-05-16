import pandas as pd
import psycopg2
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

def extract_clean_logistics():
    try:
        orders = pd.read_csv('/opt/airflow/data/olist_orders_dataset.csv', parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date'])
        order_items = pd.read_csv('/opt/airflow/data/olist_order_items_dataset.csv')
        sellers = pd.read_csv('/opt/airflow/data/olist_sellers_dataset.csv')
        products = pd.read_csv('/opt/airflow/data/olist_products_dataset.csv')

        # Gabungkan data
        df = orders.merge(order_items, on='order_id', how='left') \
                   .merge(sellers, on='seller_id', how='left') \
                   .merge(products, on='product_id', how='left')

        # Drop NaN di tanggal pengiriman
        df = df.dropna(subset=['order_delivered_customer_date'])

        # Simpan ke PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        cur = conn.cursor()
        cur.execute("TRUNCATE TABLE raw_logistics")  # Kosongkan tabel dulu

        insert_query = """
            INSERT INTO raw_logistics (
                order_id, customer_id, order_purchase_timestamp, order_delivered_customer_date,
                order_item_id, product_id, seller_id, shipping_limit_date, product_category_name
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        for _, row in df.iterrows():
            cur.execute(insert_query, (
                row['order_id'], row['customer_id'], row['order_purchase_timestamp'], row['order_delivered_customer_date'],
                row['order_item_id'], row['product_id'], row['seller_id'], row['shipping_limit_date'], row['product_category_name']
            ))
        conn.commit()
        cur.close()
        conn.close()
        logging.info("Extract & load raw_logistics success")
    except Exception as e:
        logging.error(f"Error during extract_clean_logistics: {e}")
        raise
