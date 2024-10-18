from pydantic import BaseModel


class TtsInput(BaseModel):
    title: str
    body: str
