from datetime import datetime

from pydantic import BaseModel


class Author(BaseModel):
    id: str
    username: str
    email: str
    profile: dict| None
    date_created: datetime

class CommentResponse(BaseModel):
    id: str
    content: str
    author: Author
    date_posted: datetime
    date_updated: datetime