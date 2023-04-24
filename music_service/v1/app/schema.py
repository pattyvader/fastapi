from datetime import date
from pydantic import BaseModel

class MyBaseModel(BaseModel):
    class Config:
        orm_mode = True

class Music(MyBaseModel):
    title: str
    author: list
    release_data: date
    keywords: list