from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Body, Depends, Form, HTTPException, Response, status
from pydantic import Field


from ..config.settings import ACCESS_TOKEN_EXPIRES_IN, REFRESH_TOKEN_EXPIRES_IN

# from app.auth import oauth2
from ..db.database import User
from ..db.helper.user import create_user, find_user
from ..db.serializer import user_entity
from ..schemas.users import CreateUser, UpdateUser
from ..utils.oauth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    hash_password,
    verify_password,
)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    payload: CreateUser, response: Response
) -> dict:
    """
    Register a new user.

    Args:
        payload: A CreateUserSchema object containing the user's email, password, and password confirmation.

    Returns:
        A dictionary containing the status of the operation and the newly created user object.
    """
    # Check if user already exists
    user = find_user(payload.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already registered"
        )
    # Compare and confirm password
    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )
    # # Insert the new user into the database
    feedback = create_user(payload)

    if feedback == False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not Added"
        )
    # login user
    access_token = create_access_token(*feedback)
    # Create refresh token
    refresh_token = create_refresh_token(*feedback)

    # Store refresh and access tokens in cookie
    response.set_cookie(
        "access_token",
        access_token,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        REFRESH_TOKEN_EXPIRES_IN * 60,
        REFRESH_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "logged_in",
        "True",
        ACCESS_TOKEN_EXPIRES_IN * 60,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        False,
        "lax",
    )

    # Send both access
    return {
        "status": "success",
        "message": "User registered successfully!",
        "token": {"access_token": access_token, "token_type": "bearer"},
    }


# User sign in
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    payload: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
) -> dict:
    """_summary_

    Args:
        payload (LoginUserSchema): _description_
        response (Response): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        dict: _token_
    """

    # check if user exists
    user: dict = find_user(payload.username)  # type: ignore
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not registered"
        )

    if not verify_password(payload.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password"
        )

    # create access token
    access_token = create_access_token(user["id"], user["email"])
    # Create refresh token
    refresh_token = create_refresh_token(user["id"], user["email"])

    response.set_cookie(
        "access_token",
        access_token,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        REFRESH_TOKEN_EXPIRES_IN * 60,
        REFRESH_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        True,
        "lax",
    )
    response.set_cookie(
        "logged_in",
        "True",
        ACCESS_TOKEN_EXPIRES_IN * 60,
        ACCESS_TOKEN_EXPIRES_IN * 60,
        "/",
        None,
        False,
        False,
        "lax",
    )

    return {
        "status": "success",
        "message": "Logged in successfully!",
        "access_token": access_token,
        "token_type": "bearer"
    }


# user logout
@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response, user: Annotated[str, Depends(get_current_user)]
) -> dict:
    """_summary_

    Args:
        response (Response): _description_

    Returns:
        dict: _description_
    """
    # Clear cookies
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("logged_in")

    return {"status": "success", "message": "User logged out!"}
