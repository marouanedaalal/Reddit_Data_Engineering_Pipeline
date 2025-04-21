import pandas as pd

from etls.global_etl import connect_reddit, extract_posts, transform_data, upload_to_s3
from utils.constants import CLIENT_ID, SECRET


def reddit_pipeline(file_name: str, folder_name:str, subreddit: str, time_filter='day', limit=None):
    # connecting to reddit instance
    instance = connect_reddit(CLIENT_ID, SECRET, 'Airscholar Agent')
    # extraction
    posts = extract_posts(instance, subreddit, time_filter, limit)
    post_df = pd.DataFrame(posts)
    # transformation
    post_df = transform_data(post_df)
    # loading to s3
    upload_to_s3(post_df, file_name, folder_name)
