from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl_scripts.extract_rfm import extract_clean_rfm
from etl_scripts.transform_rfm import transform_rfm
from etl_scripts.load_rfm import load_rfm

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    dag_id='rfm_dag',
    default_args=default_args,
    description='ETL Segmentasi Pelanggan (RFM)',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['Segmentasi Pelanggan (RFM)']
) as dag:

    start_task = PythonOperator(
        task_id='start_rfm_pipeline',
        python_callable=lambda: print("Memulai ETL RFM...")
    )

    extract_task = PythonOperator(
        task_id='extract_rfm',
        python_callable=extract_clean_rfm
    )

    transform_task = PythonOperator(
        task_id='transform_rfm',
        python_callable=transform_rfm
    )

    load_task = PythonOperator(
        task_id='load_rfm',
        python_callable=load_rfm
    )

    end_task = PythonOperator(
        task_id='end_rfm_pipeline',
        python_callable=lambda: print("Selesai ETL RFM.")
    )

    start_task >> extract_task >> transform_task >> load_task >> end_task
