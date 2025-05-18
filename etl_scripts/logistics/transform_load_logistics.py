import pandas as pd
import os
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)

def transform_load_logistics():
    try:
        engine = create_engine(
            f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
            f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )

        orders = pd.read_sql("SELECT * FROM raw_orders", engine)
        order_items = pd.read_sql("SELECT * FROM raw_order_items", engine)
        customers = pd.read_sql("SELECT * FROM raw_customers", engine)
        sellers = pd.read_sql("SELECT * FROM raw_sellers", engine)
        products = pd.read_sql("SELECT * FROM raw_products", engine)
        geolocation = pd.read_sql("SELECT * FROM raw_geolocation", engine)

        # Gabungkan data
        df = orders.merge(order_items, on="order_id", how="inner")
        df = df.merge(customers, on="customer_id", how="inner")
        df = df.merge(sellers, on="seller_id", how="inner")
        df = df.merge(products, on="product_id", how="left")  # product_id bisa NaN

        # Drop nilai kosong penting
        df.dropna(subset=[
            'order_estimated_delivery_date',
            'order_delivered_customer_date',
            'order_id',
            'customer_id',
            'seller_id'
        ], inplace=True)
        df.drop_duplicates(inplace=True)

        # Filter hanya yang status delivered
        df = df[df['order_status'] == 'delivered']

        # Konversi tanggal
        df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])
        df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])

        # Hitung SLA
        
        # SLA = order_estimated_delivery_date - order_delivered_customer_date
        # Hitung delivery_delay (selisih hari)
        df['delivery_delay'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days
        
        # Tentukan status pengiriman
        # <= 0 (on_time)
        # > 0 (late)
        df['logistics_status'] = df['delivery_delay'].apply(lambda x: 'on_time' if x <= 0 else 'late')
        
        # Buat agregasi sederhana: top 5 kategori produk dengan delay terbanyak
        product_delay = df[df['logistics_status'] == 'late'].groupby('product_category_name').size().sort_values(ascending=False).reset_index(name='late_count')
        
        # Output utama: hasil logistik
        result = df[[
            'order_id', 'customer_id', 'seller_id',
            'order_delivered_customer_date', 'order_estimated_delivery_date',
            'delivery_delay', 'logistics_status', 'product_id', 'product_category_name',
            'customer_city', 'customer_state', 'seller_city', 'seller_state'
        ]]

        # Simpan ke tabel transform
        result.to_sql("result_logistics", engine, if_exists="replace", index=False)
        product_delay.to_sql("result_logistics_top_product_delay", engine, if_exists="replace", index=False)

        logging.info(f"ETL logistik lengkap selesai. Total: {len(result)} baris.")
    
    except Exception as e:
        logging.error(f"Gagal transform logistics: {e}")

if __name__ == "__main__":
    transform_load_logistics()