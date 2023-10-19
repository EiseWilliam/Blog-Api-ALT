from pydantic import BaseModel, Field 
from datetime import datetime
from models.objectid import CusObjectId

class ArticleIn:
    pass
class Article(BaseModel):
    author : str = Field(..., alias="user_id")
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