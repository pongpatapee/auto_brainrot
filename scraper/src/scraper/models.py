from typing import List

from pydantic import BaseModel


class RedditPostContent(BaseModel):
    title: str
    body: str
