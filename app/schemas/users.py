from datetime import datetime

# import field
from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr


class CreateUser(User):
    username: str = Field(min_length=4, max_length=15)
    password: str = Field(min_length=8, max_length=50)
    confirm_password: str = Field(min_length=8, max_length=50)


class Profile(BaseModel):
    first_name: str | None = ""
    last_name: str | None = ""
    bio: str | None = ""
    contact: str | None = ""
    photo: str | None = ""

class UpdateUser(BaseModel):
    username: str | None = None
    profile: Profile | None = None


class UserQuery(BaseModel):
    query: str = Field(..., description="Search query", min_length=4, max_length=20)