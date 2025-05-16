from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from etl_scripts.extract_reviews import extract_clean_reviews
from etl_scripts.transform_reviews import transform_reviews
from etl_scripts.load_reviews import load_reviews

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='reviews_dag',
    default_args=default_args,
    description='ETL Analisis Review & Kepuasan Pelanggan',
    tags=['Analisis Review & Kepuasan Pelanggan'],
    schedule_interval='@daily',
    catchup=False
) as dag:

    start = PythonOperator(
        task_id='start',
        python_callable=lambda: print("Mulai proses review...")
    )

    extract = PythonOperator(
        task_id='extract_reviews',
        python_callable=extract_clean_reviews
    )

    transform = PythonOperator(
        task_id='transform_reviews',
        python_callable=transform_reviews
    )

    load = PythonOperator(
        task_id='load_reviews',
        python_callable=load_reviews
    )

    end = PythonOperator(
        task_id='end',
        python_callable=lambda: print("Review pipeline selesai.")
    )

    start >> extract >> transform >> load >> end
