from pydantic import BaseModel
from models.objectid import CusObjectId

class Comment(BaseModel):
    article_id: str
    user_id: str
    content: str
    date_posted: str
    date_edited: str
    
class CreateComment(Comment):
    pass

class UpdateComment(Comment):
    pass