from typing import List, Literal

from models import RedditPostContent
from reddit import reddit


def get_top_posts_urls(
    subreddit: str,
    limit: int = 10,
    time_filter: Literal["day", "week", "month", "year", "all"] = "week",
) -> List[str]:
    """
    returns a list of Urls
    """

    post_urls = []
    for submission in reddit.subreddit(subreddit).top(
        limit=limit, time_filter=time_filter
    ):
        post_urls.append(submission.url)

    return post_urls


def get_post_content(url: str) -> RedditPostContent:

    submission = reddit.submission(url=url)

    title = submission.title
    body = submission.selftext

    return RedditPostContent(title=title, body=body)


if __name__ == "__main__":

    # TODO: everytime a post is viewed add to DB to avoid dups
    post_urls = get_top_posts_urls("cscareers")
    post_content = get_post_content(post_urls[0])
    print(post_content)
