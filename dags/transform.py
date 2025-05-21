from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def transform_reddit_posts():
    ## TRANSFORMATION ##
    # Imp fields
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