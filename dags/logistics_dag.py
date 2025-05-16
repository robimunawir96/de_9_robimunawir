import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from etl_scripts.extract_logistics import extract_clean_logistics
from etl_scripts.transform_logistics import transform_logistics
from etl_scripts.load_logistics import load_logistics

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='logistics_dag',
    default_args=default_args,
    description='ETL SLA Pengiriman & Kinerja Logistik',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['SLA Pengiriman & Kinerja Logistik']
) as dag:

    start_task = PythonOperator(task_id='start_logistics', python_callable=lambda: print("Mulai ETL logistik"))
    extract_task = PythonOperator(task_id='extract_logistics', python_callable=extract_clean_logistics)
    transform_task = PythonOperator(task_id='transform_logistics', python_callable=transform_logistics)
    load_task = PythonOperator(task_id='load_logistics', python_callable=load_logistics)
    end_task = PythonOperator(task_id='end_logistics', python_callable=lambda: print("Selesai ETL logistik"))

    start_task >> extract_task >> transform_task >> load_task >> end_task
