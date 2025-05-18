from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os

# Import fungsi ETL
from etl_scripts.rfm.extract_rfm import extract_rfm
from etl_scripts.rfm.transform_load_rfm import transform_load_rfm

default_args = {
    'owner': 'robi',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['robimunawir1@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='rfm_etl_dag',
    default_args=default_args,
    description='ETL Analisis Segmentasi RFM',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['olist', 'RFM', 'ETL'],
) as dag:

    start_task = PythonOperator(
        task_id='start_rfm_pipeline',
        python_callable=lambda: print("Memulai ETL RFM...")
    )
    
    end_task = PythonOperator(
        task_id='end_rfm_pipeline',
        python_callable=lambda: print("Selesai ETL RFM.")
    )
    
    extract_task = PythonOperator(
        task_id='extract_rfm',
        python_callable=extract_rfm
    )

    transform_load_task = PythonOperator(
        task_id='transform_load_rfm',
        python_callable=transform_load_rfm
    )
    

    start_task >> extract_task >> transform_load_task >> end_task
