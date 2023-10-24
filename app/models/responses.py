
from email import message
from telnetlib import STATUS
from pydantic import BaseModel
from models.response.comment import CommentResponse
from models.response.article import ArticleResponse
from models.response.user import UserResponse


# show profile
class UserResponseModel(BaseModel):
    status: str = "success"
    message: str = "user profile retrieved successfully"
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

class CommentResponseModel(BaseModel):
    message: str
    comment: CommentResponse
    
class CommentListResponseModel(BaseModel):
    message: str
    comments: list[CommentResponse]

class PostRefrenceResponseModel(BaseModel):
    message: str = "post successful"
    post: dict[str,str] = {"id": "1", "article": "nice-article"}
    
class MessageResponse(BaseModel):
    status: str = "success"
    message: str = "request successful"
    
class ErrorMessageResponse(BaseModel):
    status: str = "error"
    message: str = "request failed"
