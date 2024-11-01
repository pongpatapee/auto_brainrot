from pydantic import BaseModel


class RedditPostContent(BaseModel):
    id: str
    title: str
    body: str


class KinesisRedditData(BaseModel):
    version: str
    id: str  # reddit post id
    data: RedditPostContent
