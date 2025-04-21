

# 🚀 Data Pipeline with Reddit, Airflow, Celery, Postgres, S3, AWS Glue, Athena, and Redshift

This project provides a comprehensive **data pipeline** solution to extract, transform, and load (ETL) Reddit data into a Redshift data warehouse. The pipeline leverages a combination of tools and services including **Apache Airflow**, **Celery**, **PostgreSQL**, **Amazon S3**, **AWS Glue**, **Amazon Athena**, and **Amazon Redshift**.

---

## 📌 Overview

The pipeline is designed to:

1. 📝 **Extract** data from Reddit using its API.
2. 🗃️ **Store** the raw data into an S3 bucket from Airflow.
3. 🔄 **Transform** the data using AWS Glue and Amazon Athena.
4. 📊 **Load** the transformed data into Amazon Redshift for analytics and querying.

---

## 🧩 Architecture

![RedditDataEngineering.png](assets%2FRedditDataEngineering.png)

1. **Reddit API**: Source of the data.
2. **Apache Airflow & Celery**: Orchestrates the ETL process and manages task distribution.
3. **PostgreSQL**: Temporary storage and metadata management.
4. **Amazon S3**: Raw data storage.
5. **AWS Glue**: Data cataloging and ETL jobs.
6. **Amazon Athena**: SQL-based data transformation.
7. **Amazon Redshift**: Data warehousing and analytics.

---

## ⚙️ Prerequisites

Before you begin, make sure you have:

- ✅ AWS Account with appropriate permissions for S3, Glue, Athena, and Redshift.
- ✅ Reddit API credentials.
- ✅ Docker Installation.
- ✅ Python 3.9 or higher.

---

## 📂 Project Structure

```bash
.
├── dags/
│   ├── etl_reddit_dag.py         

│   └── etl_global_dag.py         

├── etls/
│   ├── reddit_etl.py             

│   └── global_etl.py             

├── pipelines/
│   ├── reddit_pipeline.py         

│   ├── global_pipeline.py         

│   └── aws_s3_pipeline.py        

├── utils/
│   └── constants.py              

├── assets/
│   └── RedditDataEngineering.png   

├── reddit_pipeline_architecture.png  

└── README.md
```

---

## 🔧 How It Works

### 1. **Extract from Reddit API**

We use `praw` to extract top posts from subreddits:

```python
reddit = praw.Reddit(...)
top_posts = reddit.subreddit("dataengineering").top(limit=50)
```

### 2. **Transform with Pandas**

Clean and format the data:

```python
df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")
```

### 3. **Upload to Amazon S3**

Upload data to S3 either directly or after saving it locally:

```python
# Save locally (method 1)
df.to_csv("reddit.csv")

# Direct upload (method 2)
s3.put_object(Bucket=bucket, Key="reddit.csv", Body=csv_buffer.getvalue())
```




---

## 🐳 Docker & Celery Setup

To run the full-stack version using Docker + Celery:

1. Ensure Docker & Docker Compose are installed.
2. Clone this repository and run the following command:

```bash
docker-compose up --build
```

This will start the Airflow UI at [http://localhost:8080](http://localhost:8080).

---

## 📊 Sample Output (Stored in S3)

Once the pipeline is executed, you will find the raw Reddit data in your S3 bucket:

```
reddit-data-bucket/
│
├── raw/
│   └── reddit_20250421_183000.csv
│
└── redditfolder/
    └── reddit_20250421_183002.csv
```

---

## 📎 Requirements

- ✅ AWS Account (S3, Glue, Athena, Redshift permissions)
- ✅ Reddit API credentials (obtain from [Reddit Developer](https://www.reddit.com/prefs/apps))
- ✅ Python 3.9+
- ✅ Docker (for full-stack setup)
- ✅ IAM roles with permissions for Glue, S3, Redshift

---

## 🔑 Environment Configuration

Update the `utils/constants.py` file with your credentials:

```python
CLIENT_ID = "your_reddit_id"
SECRET = "your_reddit_secret"
AWS_ACCESS_KEY_ID = "your_aws_key"
AWS_SECRET_ACCESS_KEY = "your_aws_secret"
AWS_BUCKET_NAME = "your_bucket"
```



