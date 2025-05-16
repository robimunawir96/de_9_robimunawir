import psycopg2
import os
import logging

logging.basicConfig(level=logging.INFO)

def load_rfm():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM rfm_cleaned")
        count = cur.fetchone()[0]
        logging.info(f"Total record RFM loaded: {count}")
        cur.close()
        conn.close()

    except Exception as e:
        logging.error(f"Error loading RFM: {e}")

if __name__ == "__main__":
    load_rfm()
