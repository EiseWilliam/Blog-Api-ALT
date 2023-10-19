from pydantic import BaseModel, EmailStr
from datetime import datetime


class Profile(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str
    photo: str | None = None
    
    
class UserProfileResponse(BaseModel):
    _id: str
    username: str | None = None
    email: EmailStr
    password: str
    profile: Profile = Profile(bio="This user hasn't set up their profile yet.")
    date_created: datetime
    date_updated: datetime