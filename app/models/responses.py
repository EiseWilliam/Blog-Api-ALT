
from email import message
from pydantic import BaseModel
from models.response.article import ArticleResponse
from models.response.user import UserResponse


# show profile
class UserResponseModel(BaseModel):
    message: str
    user: UserResponse
class UserListResponseModel(BaseModel):
    message: str
    users: list[UserResponse]
    
class ArticleResponseModel(BaseModel):
    message: str
    article: ArticleResponse
    
class ArticleListResponseModel(BaseModel):
    message: str
    articles: list[ArticleResponse]
    
class PostRefrenceResponseModel(BaseModel):
    message: str
    post: dict[str,str]
    
class MessageResponse(BaseModel):
    message: str
