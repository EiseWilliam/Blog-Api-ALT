from pydantic import BaseModel, EmailStr
from datetime import datetime



class User(BaseModel):
    email: EmailStr

class CreateUser(User):
    password: str
    confirm_password: str

    
class UpdateUser(User):
    profile: dict
    password: str

    
