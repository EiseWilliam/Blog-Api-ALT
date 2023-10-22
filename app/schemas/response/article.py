from fastapi import Body
from pydantic import BaseModel, Field
from datetime import datetime


class ArticleResponse(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    slug: str = Field(..., min_length=5, max_length=100)
    body: str = Body(..., max_length=10000)
    categories: list = Field(...)
    author: str | dict
    date_published: str | datetime
    date_updated: str | datetime

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Article title",
                "slug": "article-title",
                "body": "Article body",
                "categories": [
                    "technology",
                    "science",
                    "politics" "entertainment",
                    "sports",
                ],
                "author": "user_id",
                "date_published": "2023-01-01 00:00:00",
                "date_updated": "2023-01-01 00:00:00",
            }
        }
