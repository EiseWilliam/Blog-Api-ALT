from datetime import datetime

from pydantic import BaseModel


class CommentResponse(BaseModel):
    id: str
    content: str
    author: str
    date_posted: datetime
    date_updated: datetime