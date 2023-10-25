from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr



from ...schemas.users import Profile


class UserResponse(BaseModel):
    id: str
    username: Optional[str]
    email: EmailStr
    profile: Optional [Profile]
    date_created: datetime
    date_updated: datetime


