from typing import Optional
from fastapi import Body
from pydantic import BaseModel, Field
from datetime import datetime


class ArticleResponse(BaseModel):
    title: str
    slug: str 
    body: str
    categories: Optional[list]
    author: str 
    date_published: datetime
    date_updated: datetime

