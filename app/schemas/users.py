from pydantic import BaseModel, EmailStr
from datetime import datetime
# import field
from pydantic import Field

class User(BaseModel):
    email: EmailStr


class CreateUser(User):
    username: str
    password: str
    confirm_password: str


class Profile(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    contact: str | None = None
    photo: str | None = None


class UpdateUser(BaseModel):
    username: str | None = None
    profile: Profile | None = None


class UserQuery(BaseModel):
    query: str = Field(..., description="Search query", min_length=4, max_length=50)