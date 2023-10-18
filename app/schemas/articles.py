from pydantic import BaseModel
from datetime import datetime
from bson import ObjectId as Objectid


class Article(BaseModel):
    title: str
    body: str
    categories: list

class CreateArticle(Article):
    date_published: datetime = datetime.now()
    date_modified: datetime = datetime.now()
    
    __exclude__ = ["date_published","date_modified"]
   

class UpdateArticle(Article):
    date_modified: datetime = datetime.now()

    __exclude__ = ["date_modified"]
    
    
class ArticleList(BaseModel):
    article: list[Article]