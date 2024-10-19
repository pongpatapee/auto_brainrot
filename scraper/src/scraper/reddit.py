import os

import praw
from dotenv import load_dotenv

load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID", ""),
    client_secret=os.getenv("CLIENT_SECRET", ""),
    user_agent="my user agent",
)
