from datetime import datetime
from typing import Optional

from fastapi import Body
from pydantic import BaseModel, Field


class Author(BaseModel):
    id: str
    username: str
    email: str
    profile: dict| None
    date_created: datetime
class ArticleResponse(BaseModel):
    id: str 
    title: str
    slug: str 
    body: str = Body(..., max_length=10000)
    categories: list[str]
    author: Author | str
    date_published: datetime 
    date_updated: datetime

