import logging
import logging.handlers

import boto3
from scraper.writers import KinesisStreamWriter
from scraper.models import KinesisRedditData
from scraper.reddit import RedditScraper

AWS_KINESIS_STREAM_NAME = "autoBrainrotDataStream"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
file_handler = logging.handlers.RotatingFileHandler(
    filename="logs/scraper.log", maxBytes=10 * 1024 * 1024, backupCount=5
)
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


if __name__ == "__main__":
    writer = KinesisStreamWriter(
        aws_session=boto3.Session(profile_name="auto_brainrot"),
    )
    scraper = RedditScraper()

    subreddits = ["AskReddit", "cscareerquestions"]
    for subreddit in subreddits:

        logger.info(f"Scraping posts from {subreddit} subreddit")
        posts = scraper.get_top_posts_urls(subreddit=subreddit, limit=1)
        for post in posts:

            content = scraper.get_post_content(post)
            data = KinesisRedditData(version="1.0", id=content.id, data=content)
            response = writer.write(dst_name=AWS_KINESIS_STREAM_NAME, data=data)

            logger.info(response)
