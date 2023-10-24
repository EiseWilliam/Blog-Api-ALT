from datetime import datetime, timedelta
from mailbox import Message
from typing import Annotated, Any
from unittest.mock import Base
from urllib import response
from bson.objectid import ObjectId
from decouple import config
from fastapi import (
    APIRouter,
    Query,
    Response,
    status,
    Depends,
    HTTPException,
    Body,
    Form,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from pydantic import Field

# from app.auth import oauth2
from db.helper.article import article_list_by_author
from db.helper.article import create_article
from db.helper.user import (
    create_user,
    find_user,
    update_user,
    retrieve_user,
    delete_user,
    dynamic_user_search,
)
from schemas.response.user import UserProfileResponse, CurrentUser
from schemas.users import UpdateUser, User, UserQuery
from schemas.articles import CreateArticle
from utils.oauth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from models.responses import ArticleListResponseModel, MessageResponse, PostRefrenceResponseModel, UserResponseModel, UserListResponseModel

router = APIRouter()


# get logged in user profile
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseModel,
    response_description="User profile retrieved successfully",
)
async def show_profile(user: Annotated[dict, Depends(get_current_user)]) -> Any:
    """
    Retrieve and return the user's profile.

    Args:
        Header token.

    Returns:
        Any: The response model containing the user's profile and a success message.
    """
    profile = retrieve_user(user["id"])  # type: ignore
    return UserResponseModel(user=profile, message="User profile retrieved successfully")  # type: ignore


# update user profile
@router.patch("/", status_code=status.HTTP_200_OK, response_model= MessageResponse)
async def update_profile(
    user_details: UpdateUser, user: Annotated[dict, Depends(get_current_user)]
) -> Any:
    """
    Update the profile of the currently logged in user.
    """
    profile = await update_user(user["id"], user_details)  # type: ignore
    if profile == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not Updated"
        )
    return MessageResponse(message="User profile updated successfully")


# get my articles
@router.get("/articles", status_code=status.HTTP_200_OK, response_model=ArticleListResponseModel)
async def my_articles(user: Annotated[dict, Depends(get_current_user)]) -> Any:
    """
    Get the articles of the currently logged in user.
    """
    articles = await article_list_by_author(user["id"])
    if articles:
        return ArticleListResponseModel(articles=articles, message="Articles retrieved successfully")  
    else:
        return ArticleListResponseModel(articles=[], message="No articles found")


@router.post("/article", status_code=status.HTTP_201_CREATED, response_model=PostRefrenceResponseModel)
async def Publish_new_article(
    article: CreateArticle, user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    result = await create_article(article, user)
    if result == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article creation failed",
        )
    else:
        return PostRefrenceResponseModel(post=result, message="Article created successfully")  # type: ignore


# delete my account
@router.delete("/", status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def delete_account(user: Annotated[dict, Depends(get_current_user)]) -> dict:
    """
    delete my account
    """
    if await delete_user(user["id"]) == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not Deleted"
        )
    return {"message": "User Deleted Successfully"}


# view other users profile
@router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_model=UserListResponseModel,
    response_description="Search results",
)
async def search_user_by_mail_or_username(
    query: Annotated[str, Query(..., min_length=4)]
) -> Any:
    """
    Search for users by username or email.
    """
    users = await dynamic_user_search(query)
    if users:
        return UserListResponseModel(users=users, message="Users found successfully")  # type: ignore
    else:
        return UserListResponseModel(users=[], message="No users found")
