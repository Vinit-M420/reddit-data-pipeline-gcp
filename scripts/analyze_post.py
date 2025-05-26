from google.cloud import bigquery, storage
import json
import os
from dotenv import load_dotenv
load_dotenv()

# Load constants
PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")
TABLE_ID = os.getenv("TABLE_IDT")
BUCKET_NAME = os.getenv("BUCKET_NAME")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
SQL_DIR = os.path.join(BASE_DIR, "..", "sql")     
OUTPUT_DIR = "output"

def run_query_and_save(query_file, output_filename):
    client = bigquery.Client(project=PROJECT_ID)

    # Load SQL from file
    query_path = os.path.join(SQL_DIR, query_file)
    with open(query_path, "r") as f:
        query = f.read()

    # Run query
    query_job = client.query(query)
    results = [dict(row) for row in query_job.result()]

    # Save locally as JSON
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    local_path = os.path.join(OUTPUT_DIR, output_filename)
    with open(local_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved results to {local_path}")
    return local_path

def upload_to_gcs(local_path, gcs_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)
    print(f"Uploaded to GCS: gs://{BUCKET_NAME}/{gcs_path}")
    

if __name__ == "__main__":
    avg_path = run_query_and_save("avg_upvotes.sql", "avg_upvotes.json")
    upload_to_gcs(avg_path, "analysis/avg_upvotes.json")

    top_path = run_query_and_save("top5_hottestpost.sql", "top5_hottestpost.json")
    upload_to_gcs(top_path, "analysis/top5_hottestpost.json")