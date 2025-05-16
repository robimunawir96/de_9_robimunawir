-- Tabel RAW
DROP TABLE IF EXISTS raw_customers;
CREATE TABLE IF NOT EXISTS raw_customers (
    customer_id VARCHAR PRIMARY KEY,
    customer_unique_id VARCHAR,
    customer_zip_code_prefix VARCHAR,
    customer_city VARCHAR,
    customer_state VARCHAR
);

DROP TABLE IF EXISTS raw_orders;
CREATE TABLE IF NOT EXISTS raw_orders (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    order_status VARCHAR,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

-- Tabel hasil ETL untuk RFM
DROP TABLE IF EXISTS rfm_cleaned;
CREATE TABLE IF NOT EXISTS rfm_cleaned (
    customer_id VARCHAR PRIMARY KEY,
    recency INTEGER,
    frequency INTEGER,
    monetary NUMERIC,
    rfm_score VARCHAR
);

-- Tabel untuk menyimpan data hasil ekstraksi mentah logistik
DROP TABLE IF EXISTS raw_logistics;
CREATE TABLE raw_logistics (
    order_id TEXT,
    customer_id TEXT,
    order_purchase_timestamp TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_item_id INT,
    product_id TEXT,
    seller_id TEXT,
    shipping_limit_date TEXT,
    product_category_name TEXT
);

-- Tabel untuk menyimpan hasil analisis logistik (transformed)
DROP TABLE IF EXISTS analytics_logistics;
CREATE TABLE analytics_logistics (
    order_id TEXT,
    seller_id TEXT,
    product_category_name TEXT,
    delivery_days INT,
    sla_met BOOLEAN
);

-- Tabel untuk menyimpan review mentah
DROP TABLE IF EXISTS raw_reviews;
CREATE TABLE raw_reviews (
    review_id TEXT,
    order_id TEXT,
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    customer_id TEXT,
    order_purchase_timestamp TIMESTAMP
);

-- Tabel untuk analisis review
DROP TABLE IF EXISTS analytics_reviews;
CREATE TABLE analytics_reviews (
    review_id TEXT,
    order_id TEXT,
    review_score INT,
    sentiment TEXT,
    review_creation_date TIMESTAMP
);
