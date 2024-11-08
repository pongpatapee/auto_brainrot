import os
from typing import List, Literal

import praw
from dotenv import load_dotenv
from scraper.models import RedditPostContent

load_dotenv()


class RedditScraper:
    def __init__(self) -> None:
        self.reddit = praw.Reddit(
            client_id=os.getenv("CLIENT_ID", ""),
            client_secret=os.getenv("CLIENT_SECRET", ""),
            user_agent="my user agent",
        )

    def get_top_posts_urls(
        self,
        subreddit: str,
        limit: int = 10,
        time_filter: Literal["day", "week", "month", "year", "all"] = "week",
    ) -> List[str]:
        """
        returns a list of Urls
        """

        post_urls = []
        for submission in self.reddit.subreddit(subreddit).top(
            limit=limit, time_filter=time_filter
        ):
            post_urls.append(submission.url)

        return post_urls

    def get_post_content(self, url: str) -> RedditPostContent:

        submission = self.reddit.submission(url=url)

        id = submission.id
        title = submission.title
        body = submission.selftext

        return RedditPostContent(id=id, title=title, body=body)
