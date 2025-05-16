import pandas as pd
import psycopg2
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

def transform_logistics():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )

        df = pd.read_sql_query("SELECT * FROM raw_logistics", conn, parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date'])

        # Hitung waktu pengiriman (delivery_days)
        df['delivery_days'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days

        # SLA terpenuhi jika delivery_days <= 10
        df['sla_met'] = df['delivery_days'] <= 10

        cur = conn.cursor()
        cur.execute("TRUNCATE TABLE analytics_logistics")  # Kosongkan dulu tabel hasil

        insert_query = """
            INSERT INTO analytics_logistics (
                order_id, seller_id, product_category_name, delivery_days, sla_met
            ) VALUES (%s,%s,%s,%s,%s)
        """

        for _, row in df.iterrows():
            cur.execute(insert_query, (
                row['order_id'], row['seller_id'], row['product_category_name'], int(row['delivery_days']), row['sla_met']
            ))

        conn.commit()
        cur.close()
        conn.close()
        logging.info("Transform & load analytics_logistics success")

    except Exception as e:
        logging.error(f"Error during transform_logistics: {e}")
        raise
