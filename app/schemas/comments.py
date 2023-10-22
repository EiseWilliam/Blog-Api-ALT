from pydantic import BaseModel
from models.objectid import CusObjectId

class Comment(BaseModel):
    article_id: str
    user_id: str
    content: str
    
class CreateComment(BaseModel):
    content: str

class UpdateComment(BaseModel):
    content: str