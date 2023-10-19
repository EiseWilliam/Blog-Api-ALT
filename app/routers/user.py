from datetime import datetime, timedelta
from typing import Annotated
from bson.objectid import ObjectId
from decouple import config
from fastapi import APIRouter, Response, status, Depends, HTTPException, Body, Form
from fastapi.security import OAuth2PasswordRequestForm

# from app.auth import oauth2
from db.database import User
from db.serializer import user_entity
from db.helper.user import create_user, find_user
from schemas.response.user import UserProfileResponse
from utils.oauth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
)


router = APIRouter()


# get logged in user profile
@router.get("/profile", response_model = UserProfileResponse)
async def profile(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Get the profile of the currently logged in user.
    """
    profile = find_user(current_user['email'])
    return profile