# REDDIT DATA PIPELINE USING GCP

This personal project showcases entire data pipeline for Reddit's hottest posts of single subreddit using **PRAW (Reddit public API)**, **Python**, **Apache Airflow**, **Docker** and **GCP Cloud Storage and BigQuery**. It is broken down into single ETL steps and scheduled using **Apache Airflow** and finally loaded on **BigQuery** DW for analysis.

---
# Technologies Used
- Python  
- NumPy    
- Docker  
- Apache Airflow
- GCP
- Numpy
- Pandas

---

## Folder Structure


  docker/ – Airflow setup, logs, and plugins
  
  dags/ - DAG python files for extract, transform and load
  
  data/ – Pulled reddit data in json
  
  scripts/ – Python ETL testing scripts
  
  notebook/ - Jupyter notebooks for analysis of the dataset
  
  visuals/ - Visualizing the insights and saving it's images
  
  .gitignore – Files to ignore in Git
  
  README.md – This file