from pydantic import BaseModel
from models.objectid import CusObjectId 

class Comment(BaseModel):
    article_id: CusObjectId
    user_id: CusObjectId
    content: str
    date_posted: str
    date_edited: str
    
class CreateComment(Comment):
    pass

class UpdateComment(Comment):
    pass