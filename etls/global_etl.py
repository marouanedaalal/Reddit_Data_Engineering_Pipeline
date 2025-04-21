import sys
import numpy as np
import pandas as pd
import praw
from praw import Reddit
from datetime import datetime
import os
import boto3
from io import StringIO

from utils.constants import POST_FIELDS, AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY, AWS_BUCKET_NAME


# Step 1: Connect to Reddit
def connect_reddit(client_id, client_secret, user_agent) -> Reddit:
    try:
        reddit = praw.Reddit(client_id=client_id,
                             client_secret=client_secret,
                             user_agent=user_agent)
        print("Connected to Reddit!")
        return reddit
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

# Step 2: Extract Posts from Reddit
def extract_posts(reddit_instance: Reddit, subreddit: str, time_filter: str, limit=None):
    subreddit = reddit_instance.subreddit(subreddit)
    posts = subreddit.top(time_filter=time_filter, limit=limit)
    
    post_lists = []
    for post in posts:
        post_dict = vars(post)
        post_data = {key: post_dict[key] for key in POST_FIELDS}
        post_lists.append(post_data)
        
    return post_lists

# Step 3: Transform Data
def transform_data(post_df: pd.DataFrame):
    post_df['created_utc'] = pd.to_datetime(post_df['created_utc'], unit='s')
    post_df['over_18'] = np.where((post_df['over_18'] == True), True, False)
    post_df['author'] = post_df['author'].astype(str)
    edited_mode = post_df['edited'].mode()
    post_df['edited'] = np.where(post_df['edited'].isin([True, False]), 
                                 post_df['edited'], edited_mode).astype(bool)
    post_df['num_comments'] = post_df['num_comments'].astype(int)
    post_df['score'] = post_df['score'].astype(int)
    post_df['title'] = post_df['title'].astype(str)
    
    return post_df

# Step 4: Check S3 connection
def check_s3_connection():
    try:
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY)
        # Try to list objects in the bucket
        response = s3.list_objects_v2(Bucket=AWS_BUCKET_NAME)
        if 'Contents' in response:
            print("S3 connection is successful!")
        else:
            print("S3 bucket is empty or cannot be accessed.")
        return True
    except Exception as e:
        print(f"Error connecting to S3: {e}")
        return False

# Step 5: Upload Data to S3 with Specific Folder Paths
def upload_to_s3(df, file_name, folder_name):
    if check_s3_connection():
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_ACCESS_KEY)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        # Add folder structure to the file path (Key)
        s3.put_object(Bucket=AWS_BUCKET_NAME, Key=f"{folder_name}/{file_name}", Body=csv_buffer.getvalue())
        print(f"Data uploaded to S3 at {folder_name}/{file_name}")
    else:
        print("Unable to upload to S3. Connection failed.")
