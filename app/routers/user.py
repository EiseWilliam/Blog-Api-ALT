from datetime import datetime, timedelta
from typing import Annotated
from bson.objectid import ObjectId
from decouple import config
from fastapi import APIRouter, Response, status, Depends, HTTPException, Body, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

# from app.auth import oauth2
from db.database import User
from db.helper.article import article_list_by_author
from db.helper.article import create_article
from db.helper.user import create_user, find_user,update_user, retreive_user, delete_user
from schemas.response.user import UserProfileResponse,CurrentUser
from schemas.users import UpdateUser
from schemas.articles import CreateArticle
from utils.oauth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
)


router = APIRouter()


# get logged in user profile
@router.get("/", status_code=status.HTTP_200_OK)
async def show_profile(user: CurrentUser = Depends(get_current_user)) -> UserProfileResponse:
    """
    Get the profile of the currently logged in user.
    """
    profile = retreive_user(user['id'])
    return profile

# update user profile
@router.put("/", status_code=status.HTTP_200_OK)
async def update_profile(user_details: UpdateUser, user: CurrentUser = Depends(get_current_user)) -> dict:
    """
    Update the profile of the currently logged in user.
    """
    profile = update_user(user['id'], user_details)
    if profile == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not Updated"
        )
    return {"message": "User Updated Successfully"}

# get my articles
@router.get("/articles", status_code=status.HTTP_200_OK)
async def my_articles(user: CurrentUser = Depends(get_current_user)) -> list[dict]:
    """
    Get the articles of the currently logged in user.
    """
    articles = article_list_by_author(user['id'])
    return articles

@router.post("/article", status_code=status.HTTP_201_CREATED)
async def Publish_new_article(
    article: CreateArticle, user_id: Annotated[str, Depends(get_current_user)]
) -> dict:
    return_id = await create_article(article,user_id)
    if return_id == False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Article creation failed",
        )
    else:
        return {"id": return_id,
                "message": "Article published successfully"}

# delete my account
@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_account(user: CurrentUser = Depends(get_current_user)) -> dict:
    """
    delete user account
    """
    if delete_user(user['id']) == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST , detail="User not Deleted"
        )
    return  {"message": "User Deleted Successfully"}