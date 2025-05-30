from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from etl_scripts.logistics.extract_logistics import extract_logistics
from etl_scripts.logistics.transform_load_logistics import transform_load_logistics

default_args = {
    'owner': 'robi',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['robimunawir1@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='logistics_etl_dag',
    default_args=default_args,
    description='ETL untuk Analisis SLA Pengiriman dan Kinerja Logistik',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['olist', 'Logistics', 'ETL'],
    
) as dag:
    
    start_task = PythonOperator(
        task_id='start_rfm_pipeline',
        python_callable=lambda: print("Memulai ETL Logistics...")
    )
    
    end_task = PythonOperator(
        task_id='end_rfm_pipeline',
        python_callable=lambda: print("Selesai ETL Logistics.")
    )
    
    extract_task = PythonOperator(
        task_id='extract_logistics',
        python_callable=extract_logistics
    )

    transform_load_task = PythonOperator(
        task_id='transform_load_logistics',
        python_callable=transform_load_logistics
    )

    start_task >> extract_task >> transform_load_task >> end_task
