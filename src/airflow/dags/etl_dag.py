from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Importando as funções dos arquivos externos
from src.kafka.producer import extract_data
from src.spark.transform_data import transform_data
from src.mongodb.load_data import load_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Pipeline de ETL com Airflow, Kafka, Spark e MongoDB',
    schedule_interval=timedelta(minutes=10),
) as dag:

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id='load',
        python_callable=load_data,
    )

    extract_task >> transform_task >> load_task
