from enum import Enum
from pydantic import BaseModel
from fastapi import Body, Form
from typing import Optional, Annotated
from datetime import datetime
from models.objectid import CusObjectId

from typing import List, Annotated
from pydantic import BaseModel, Field

class ArticleIn:
    pass
class Category(str, Enum):
    technology = "technology"
    science = "science"
    politics = "politics"
    entertainment = "entertainment"
    sports = "sports"

class Article(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    body: str = Body(..., max_length=10000)
    categories: List[Category] = Field(..., min_items=1, max_items=5)

class CreateArticle(Article):
    pass

class UpdateArticle(Article):
    pass
      
class ArticleList(BaseModel):
    article: List[Article]
