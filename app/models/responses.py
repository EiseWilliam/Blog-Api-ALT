from pydantic import BaseModel
from models.response.user import UserResponse


# show profile
class UserResponseModel(BaseModel):
    user: UserResponse
    message: str
    