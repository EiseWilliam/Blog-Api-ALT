from pydantic import BaseModel
from objectid import CusObjectId


class Comment(BaseModel):
    _id: CusObjectId 
    article_id: CusObjectId
    user_id: CusObjectId
    content: str
    date_posted: str
    date_edited: str