from pydantic import BaseModel

from app.routers import comments


from .response.article import ArticleResponse
from .response.comment import CommentResponse
from .response.user import UserResponse


# show profile
class UserResponseModel(BaseModel):
    status: str = "success"
    message: str = "user profile retrieved successfully"
    user: UserResponse
class UserListResponseModel(BaseModel):
    status: str = "success"
    message: str = "n users retrieved successfully"
    users: list[UserResponse]
    
class ArticleResponseModel(BaseModel):
    status: str = "success"
    message: str = "article retrieved successfully"
    article: ArticleResponse
class ViewArticleResponseModel(BaseModel):
    status: str = "success"
    message: str = "article retrieved successfully"
    article: ArticleResponse
    comments: list[CommentResponse]
class ArticleListResponseModel(BaseModel):
    status: str = "success"
    message: str = "n articles retrieved successfully"
    articles: list[ArticleResponse]

class CommentResponseModel(BaseModel):
    status: str = "success"
    message: str = "comment retrieved successfully"
    comment: CommentResponse
    
class CommentListResponseModel(BaseModel):
    status: str = "success"
    message: str = "n comments retrieved successfully"
    comments: list[CommentResponse] 

class PostRefrenceResponseModel(BaseModel):
    status: str = "success"
    message: str = "post successful"
    post: dict = {"id": "1", "article_path": "nice-article"}
    
class MessageResponse(BaseModel):
    status: str = "success"
    message: str = "request successful"
    
class ErrorMessageResponse(BaseModel):
    status: str = "error"
    message: str = "request failed"
    # detail: str = "here is what went wrong"
