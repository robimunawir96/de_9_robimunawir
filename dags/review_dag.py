from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Pastikan path ke script Python kamu bisa diimport
from etl_scripts.reviews.extract_review import extract_review
from etl_scripts.reviews.transform_load_review  import transform_load_review

default_args = {
    'owner': 'robi',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['robimunawir1@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='review_etl_dag',
    default_args=default_args,
    description='ETL review dan kepuasan pelanggan Olist',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['olist', 'Review', 'ETL'],
) as dag:
    
    start_task = PythonOperator(
        task_id='start_rfm_pipeline',
        python_callable=lambda: print("Memulai ETL Review...")
    )
    
    end_task = PythonOperator(
        task_id='end_rfm_pipeline',
        python_callable=lambda: print("Selesai ETL Riview.")
    )
    
    extract_task = PythonOperator(
        task_id='extract_review_data',
        python_callable=extract_review
    )

    transform_load_task = PythonOperator(
        task_id='transform_review_data',
        python_callable=transform_load_review
    )

    start_task >> extract_task >> transform_load_task >> end_task