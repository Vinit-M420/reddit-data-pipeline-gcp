from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime, timedelta

def extract_reddit_posts():
    import requests
    import json
    import os
    import logging
    
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="/opt/airflow/.env") 
    logging.basicConfig(level=logging.DEBUG)
    
    CLIENT_ID = os.getenv("CLIENT_ID")
    SECRET_KEY = os.getenv("SECRET_KEY")
    USERNAME = os.getenv("API_USERNAME")
    PASSWORD = os.getenv("API_PASSWORD")

    api_access_data = {
        'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD
    }

    logging.info("Starting data extraction from Reddit API...")
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    headers = {'User-Agent': 'MyAPI/0.0.1'}
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=api_access_data, headers=headers)
   
    logging.debug("Token response status:", res.status_code)
    #print("Token response body:", res.text)
    res.raise_for_status()  # raise error if HTTP error
    
    TOKEN = res.json()['access_token']
    headers['Authorization'] = f'bearer {TOKEN}'
    res1 = requests.get('https://oauth.reddit.com/r/developersIndia/hot', headers=headers, params={'limit':'100'})

    ## EXTRACTION ##
    # Fetch and save raw Reddit post data 
    posts = res1.json()['data']['children']
    raw_posts = [post['data'] for post in posts]  # Extract only the 'data' part
    logging.info("Successfully fetched Reddit posts.")
    
    with open("data/rough_redditapi_data.json", "w") as f:
        json.dump(raw_posts, f, indent=2)  # Save as a proper list of post dictionaries

    # Load and clean the saved data 
    with open("data/rough_redditapi_data.json", "r") as f:
        raw_posts = json.load(f)
    logging.info("Saved extracted data to data/rough_redditapi_data.json")    
    

default_args = {
    'start_date': datetime(2023, 1, 1),
    
}

with DAG (dag_id='reddit_data_extract',
          schedule_interval = '@daily', #@once
          default_args = default_args,
          catchup= False,
          tags=["reddit"]) as dag:
    
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable= extract_reddit_posts,
        )
    
    trigger_transform = TriggerDagRunOperator(
    task_id='trigger_transform_dag',
    trigger_dag_id='reddit_data_transform',
    wait_for_completion=False,)
    

extract_task >> trigger_transform