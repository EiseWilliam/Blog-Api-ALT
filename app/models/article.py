from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from models.objectid import CusObjectId


class ArticleInDB(BaseModel):
    _id: CusObjectId
    user_id: CusObjectId
    body: str
    categories: list[str]
    date_published: datetime
    date_edited: datetime
    
    
class CreateArticleInDB(ArticleInDB):
    date_published: datetime = datetime.now()


class UpdateArticleInDB(ArticleInDB):
    date_edited: datetime = datetime.now()
    
    

