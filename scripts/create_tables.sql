-- Tabel mentah hasil ekstraksi

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

CREATE TABLE IF NOT EXISTS raw_order_items (
    order_id VARCHAR,
    order_item_id INT,
    product_id VARCHAR,
    seller_id VARCHAR,
    shipping_limit_date TIMESTAMP,
    price NUMERIC,
    freight_value NUMERIC,
    PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE IF NOT EXISTS raw_customers (
    customer_id VARCHAR PRIMARY KEY,
    customer_unique_id VARCHAR,
    customer_zip_code_prefix VARCHAR,
    customer_city VARCHAR,
    customer_state VARCHAR
);

CREATE TABLE IF NOT EXISTS raw_sellers (
    seller_id VARCHAR PRIMARY KEY,
    seller_zip_code_prefix VARCHAR,
    seller_city VARCHAR,
    seller_state VARCHAR
);

CREATE TABLE IF NOT EXISTS raw_products (
    product_id VARCHAR PRIMARY KEY,
    product_category_name VARCHAR,
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
);

CREATE TABLE IF NOT EXISTS raw_geolocation (
    geolocation_zip_code_prefix VARCHAR,
    geolocation_lat NUMERIC,
    geolocation_lng NUMERIC,
    geolocation_city VARCHAR,
    geolocation_state VARCHAR
);


CREATE TABLE IF NOT EXISTS raw_reviews (
    review_id VARCHAR PRIMARY KEY,
    order_id VARCHAR,
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);


-- Tabel hasil transformasi RFM
CREATE TABLE IF NOT EXISTS result_rfm (
    customer_unique_id TEXT PRIMARY KEY,
    recency INT,
    frequency INT,
    monetary NUMERIC,
    r_score INT,
    f_score INT,
    m_score INT,
    rfm_score TEXT,
    segment TEXT
);

-- Tabel hasil transformasi Review
CREATE TABLE IF NOT EXISTS result_review (
    review_id TEXT,
    order_id TEXT,
    review_score INTEGER,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    customer_id TEXT,
    order_status TEXT,
    customer_unique_id TEXT,
    review_category TEXT
);

-- Tabel hasil transformasi Logistics
CREATE TABLE IF NOT EXISTS result_logistics (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    seller_id VARCHAR,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    delivery_delay INT,
    logistics_status VARCHAR, -- 'on_time' atau 'late'
    product_id VARCHAR,
    product_category_name VARCHAR,
    customer_city VARCHAR,
    customer_state VARCHAR,
    seller_city VARCHAR,
    seller_state VARCHAR
);

CREATE TABLE IF NOT EXISTS result_logistics_top_product_delay (
    product_category_name VARCHAR,
    late_count INT
);


