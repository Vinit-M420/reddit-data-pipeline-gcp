from google.cloud import storage
import os
from dotenv import load_dotenv
load_dotenv()

# Set path to your downloaded JSON key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

## Load Function
def upload_to_gcs(bucket_name, source_file, destination_blob):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)
    print(f"Uploaded {source_file} to gs://{bucket_name}/{destination_blob}")

## Uploading Cleaned post json file to GCS
source_file = os.path.join('C:/Work/reddit-de-project/data/', "cleaned_reddit_data.json")

upload_to_gcs(
    bucket_name="reddit-data-vinit",
    source_file = source_file,
    destination_blob="raw-data/cleaned_reddit_data.json"
)