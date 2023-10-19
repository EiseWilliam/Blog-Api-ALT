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
from db.helper.user import create_user, find_user,update_user, retreive_user, delete_user
from schemas.response.user import UserProfileResponse,CurrentUser
from schemas.users import UpdateUser
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