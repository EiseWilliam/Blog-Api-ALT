from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

class Comment(BaseModel):
    _id: ObjectId 
    slug: str
    user_id: str
    content: str
    date_posted: datetime
    date_edited: datetime