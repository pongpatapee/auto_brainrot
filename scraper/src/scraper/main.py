import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get(
    "https://www.reddit.com/r/tifu/comments/1g2trss/tifu_by_using_the_bathroom_at_my_dates_house/"
)

# Parsing the HTML
soup = BeautifulSoup(r.text, "html.parser")
# s = soup.find("h1", class_="title")
title_tag = soup.find("h1")
print(title_tag.text)

paragraphs = (
    soup.find("div", class_="text-neutral-content")
    .find("div")
    .find("div")
    .find_all("p")
)

for p in paragraphs:
    print(p)

print(len(paragraphs))

# post_content = content_tag.text if content_tag else "N/A"
# print(post_content)
#
