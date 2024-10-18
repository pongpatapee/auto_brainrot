from typing import Literal

import requests
from bs4 import BeautifulSoup
from models import RedditPostContent


def verify_subreddit_url(url: str):
    pass


def scrape_subreddit(
    url: str,
    top_window: Literal["hour", "day", "week", "month", "year", "all"] = "week",
):
    # TODO: url verification and exception handling

    url = f"{url}/top/?t={top_window}"

    res = requests.get(subreddits[1])
    html_doc = res.text

    soup = BeautifulSoup(html_doc, "html.parser")

    post_links = soup.find_all("a", {"href": True, "slot": "full-post-link"})

    return post_links


if __name__ == "__main__":
    subreddits = [
        "https://www.reddit.com/r/learnpython",
        "https://www.reddit.com/r/cscareers",
    ]

    scrape_subreddit(subreddits[1])
