from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    email: EmailStr


class CreateUser(User):
    username: str
    password: str
    confirm_password: str


class Profile(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    bio: str
    contact: str | None = None
    photo: str | None = None


class UpdateUser(User):
    username: str | None = None
    profile: Profile | dict
