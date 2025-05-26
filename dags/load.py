from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime
from google.cloud import storage, bigquery
import logging
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="/opt/airflow/.env")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/airflow/data/reddit-sa-key.json"


def upload_to_gcs(bucket_name, source_file, destination_blob, **kwargs):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)
    logging.info(f"Uploaded {source_file} to gs://{bucket_name}/{destination_blob}")


def loading_to_BigQ():
    # Construct a BigQuery client object.
    client = bigquery.Client()
    table_id = "practical-bolt-460017-e3.reddit_dataset.reddit_data"
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        autodetect=True)
    uri = "gs://reddit-data-vinit/raw-data/cleaned_reddit_data.json"

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )
    load_job.result()  # Wait for the job to complete
    logging.info("Loaded data to BigQuery table:", table_id)
    

default_args = {
    'start_date': datetime(2023, 1, 1),
}

with DAG (dag_id='reddit_data_load',
          schedule_interval = '@daily',
          default_args = default_args,
          catchup= False,
          tags=["reddit"]) as dag:
    
    load1_task = PythonOperator(
        task_id= 'load_data_to_gcs',
        python_callable= upload_to_gcs,
        op_kwargs={
        'bucket_name': "reddit-data-vinit",
        'source_file': '/opt/airflow/data/cleaned_reddit_data.json',
        'destination_blob': 'raw-data/cleaned_reddit_data.json',
    })
        
    load2_task = PythonOperator(
        task_id= 'load_data_to_BigQ',
        python_callable= loading_to_BigQ,
)
    
    trigger_analyze = TriggerDagRunOperator(
    task_id='trigger_analyze_dag',
    trigger_dag_id='reddit_analyze_data',
    wait_for_completion=False,
    )

load1_task >> load2_task >> trigger_analyze