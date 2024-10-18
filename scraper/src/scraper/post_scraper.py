import requests
from bs4 import BeautifulSoup
from models import RedditPostContent


def verify_reddit_post_url(url: str):
    pass


def extract_post_id(url: str):
    pass


def scrape_post(url: str) -> RedditPostContent:
    # TODO: add exeption hanlding

    res = requests.get(url)
    html_doc = res.text

    soup = BeautifulSoup(html_doc, "html.parser")

    # Parase reddit post title
    title_tag = soup.find("h1", {"slot": "title"})
    if not title_tag:
        title = ""
    else:
        title = title_tag.text.strip()

    main_div = soup.find("div", {"class": "text-neutral-content", "slot": "text-body"})

    body = []
    if main_div:
        paragraphs = main_div.find_all("p")
        body = [p.text.strip() for p in paragraphs]

    return RedditPostContent(title=title, body=body)


if __name__ == "__main__":
    # url = "https://www.reddit.com/r/learnpython/comments/qzr8ir/how_to_start_web_scraping_with_python/"
    url = "https://www.reddit.com/r/AITAH/comments/1g5o3dh/aita_for_calling_my_parents_selfish_for_having_me/"
    post_content = scrape_post(url)
    print(post_content)
