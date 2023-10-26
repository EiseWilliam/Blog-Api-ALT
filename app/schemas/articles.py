from enum import Enum
from typing import Annotated, List, Optional

from fastapi import Body, Form
from pydantic import BaseModel, Field


class ArticleIn:
    pass
class Category(str, Enum):
    technology = "technology"
    tech = "tech"
    economy = "economy"
    science = "science"
    politics = "politics"
    geopoltics = "geopoltics"
    entertainment = "entertainment"
    sports = "sports"
    health = "health"
    education = "education"
    travel = "travel"
    food = "food"
    fashion = "fashion"
    lifestyle = "lifestyle"
    business = "business"
    finance = "finance"
    news = "news"
    
class Article(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    body: str = Body(..., max_length=10000)
    categories: list[Category] = Field(...)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Article title",
                "body": "Article body",
                "categories": ["technology", "tech", "politics", "entertainment", "sports"],
            }
        }





class CreateArticle(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    body: str = Body(max_length=10000)
    categories: list[Category] = Field(["technology", "tech"], title="Article categories")

class UpdateArticle(BaseModel):
    title: str | None  = Field("My Brilliant Article", min_length=5, max_length=100)
    body: str | None  = Body(None, max_length=10000)
    categories: list[Category] | None  = Field(None)

