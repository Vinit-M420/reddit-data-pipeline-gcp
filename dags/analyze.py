from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os

def run_analyze_script():
    os.chdir("/opt/airflow")  # set working directory
    os.system("python scripts/analyze_post.py")

with DAG(
    dag_id="reddit_analyze_data",
    start_date=datetime(2023, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["reddit", "analysis"]
) as dag:

    run_analysis = PythonOperator(
        task_id="run_analyze_script",
        python_callable=run_analyze_script
    )