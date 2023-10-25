from datetime import datetime
from pydantic import BaseModel, EmailStr


from ...schemas.users import Profile


class UserProfileResponse(BaseModel):
    id: str
    username: str | None = None
    email: EmailStr
    profile: Profile|dict|None = {}
    date_created: datetime
    date_updated: datetime
    
class CurrentUser(BaseModel):
    id: str
    email: EmailStr