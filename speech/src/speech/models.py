from pydantic import BaseModel


class TtsInput(BaseModel):
    id: str
    title: str
    body: str
