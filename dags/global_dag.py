import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

# Ensure the path is correctly set for external modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.global_pipeline import reddit_pipeline

default_args = {
    'owner': 'Marouane Daalal',
    'start_date': datetime(2025, 4, 20)
}

file_postfix = datetime.now().strftime("%Y%m%d_%H%M%S")

dag = DAG(
    dag_id='etl_global_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['reddit', 'etl', 'pipeline']
)

# extraction from reddit
extract = PythonOperator(
    task_id='reddit_extraction',
    python_callable=reddit_pipeline,
    op_kwargs={
        'file_name': f'reddit_{file_postfix}.csv',
        'folder_name': 'redditfolder',
        'subreddit': 'dataengineering',
        'time_filter': 'day',
        'limit': 100
    },
    dag=dag
)

extract
