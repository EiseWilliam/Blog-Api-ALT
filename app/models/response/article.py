from datetime import datetime
from typing import Optional

from fastapi import Body
from pydantic import BaseModel, Field


class ArticleResponse(BaseModel):
    id: str 
    title: str
    slug: str 
    body: str = Body(..., max_length=10000)
    categories: list 
    author: str 
    date_published: datetime 
    date_updated: datetime

