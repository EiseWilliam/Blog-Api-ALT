from fastapi import Body
from pydantic import BaseModel, Field
from datetime import datetime


class ArticleResponse(BaseModel):
    title: str
    slug: str 
    body: str
    categories: list
    author: str 
    date_published: datetime
    date_updated: datetime

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
