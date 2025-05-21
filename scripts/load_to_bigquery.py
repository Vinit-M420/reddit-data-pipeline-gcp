from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

table_id = "practical-bolt-460017-e3.reddit_dataset.reddit_data"

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    autodetect=True
)

uri = "gs://reddit-data-vinit/raw-data/cleaned_reddit_data.json"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)

load_job.result()  # Wait for the job to complete

print("Loaded data to BigQuery table:", table_id)