import psycopg2
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)

def load_logistics():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM analytics_logistics")
        count = cur.fetchone()[0]
        logging.info(f"Total record loaded to analytics_logistics: {count}")
        cur.close()
        conn.close()
    except Exception as e:
        logging.error(f"Error loading analytics_logistics: {e}")
        raise
