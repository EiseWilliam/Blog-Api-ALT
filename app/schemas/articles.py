from enum import Enum
from typing import Annotated, List, Optional

from fastapi import Body, Form
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
    categories: list[Category] = Field(...)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Article title",
                "body": "Article body",
                "categories": ["technology", "science", "politics", "entertainment", "sports"],
            }
        }





class CreateArticle(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    body: Optional[str] = Body(None, max_length=10000)
    categories: Optional[list[Category]] = Field(None)

class UpdateArticle(BaseModel):
    title: str | None  = Field("My Brilliant Article", min_length=5, max_length=100)
    body: str | None  = Body(None, max_length=10000)
    categories: list[Category] | None  = Field(None)

