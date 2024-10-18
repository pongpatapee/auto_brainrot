from typing import List

from pydantic import BaseModel


class RedditPostContent(BaseModel):
    # status: Literal["pass", "failed"]
    title: str
    body: List[str]
