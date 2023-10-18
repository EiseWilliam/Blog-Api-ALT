from pydantic import BaseModel, EmailStr
from .objectid import CusObjectId
from datetime import datetime

class Profile(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str
    photo: str | None = None

class UserInDB(BaseModel):
    _id: CusObjectId
    username: str | None = None
    email: EmailStr
    password: str
    profile: Profile = Profile(bio="This user hasn't set up their profile yet.")
    date_created: datetime
    date_updated: datetime
    

    
class CreateUserInDB(UserInDB):
    date_created: datetime = datetime.now()


class UpdateUserInDB(UserInDB):
    date_updated: datetime = datetime.now()
