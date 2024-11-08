from airflow.decorators import task

from scraper.models import KinesisRedditData
from scraper.reddit import RedditScraper
from scraper.writers import LocalWriter

from airflow.utils.log.task_context_logger import logger


AWS_KINESIS_STREAM_NAME = "autoBrainrotDataStream"

@task
def local_reddit_scraper_task(is_local=False):
    writer = LocalWriter()
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

@task
def reddit_scraper_task():
    pass
