from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


def transform_reddit_posts():
    import json
    import logging
    
    logging.info("Importing extracted data for Transformation")
    with open("data/rough_redditapi_data.json", "r") as f:
        raw_posts = json.load(f)
    
    ## TRANSFORMATION ##
    # Imp fields
    logging.info("Starting data transformation...")
    fields = ["id", "subreddit", "title", "selftext", "ups", "downs",
            "upvote_ratio", "score", "edited", "suggested_sort"]

    cleaned_posts = []
    for post in raw_posts:
        cleaned_post = {field: post.get(field, None) for field in fields}
        cleaned_posts.append(cleaned_post)

    with open("data/cleaned_reddit_data.json", "w") as f:
        for post in cleaned_posts:
            json.dump(post, f)
            f.write("\n")
    logging.info("Saved transformed data to data/cleaned_reddit_data.json")       


default_args = {
    'start_date': datetime(2023, 1, 1),
}

with DAG (dag_id='reddit_data_transform',
          schedule_interval = '@daily',
          default_args = default_args,
          catchup= False,
          tags=["reddit"]) as dag:
    
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable= transform_reddit_posts,
        )
    
    trigger_load = TriggerDagRunOperator(
    task_id='trigger_load_dag',
    trigger_dag_id='reddit_data_load',
    wait_for_completion=False,)


transform_task >> trigger_load