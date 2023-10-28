from email.policy import HTTP
from fastapi import Depends, HTTPException, requests, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Annotated

from ..config.settings import (ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM,
                             JWT_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES)
from ..db.helper.article import retrieve_article, retrieve_article_by_slug
from ..db.database import User
from ..db.helper.comment import retrieve_comment
from ..schemas.response.user import CurrentUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return pwd_context.verify(password, hashed_pass)


def create_access_token(_id: str,email: str, expires_delta: int | None = None) -> str:
    if expires_delta is not None:
        expire_time = datetime.utcnow() + expires_delta
    else:
        expire_time = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    
    payload = {"id": str(_id),"email": email,  "expires": expire_time.isoformat()}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM);
     

def create_refresh_token(_id: str, email: str, expires_delta: int | None = None) -> str:
    if expires_delta is not None:
        expire_time = datetime.utcnow() + expires_delta
    else:
        expire_time = datetime.utcnow() + timedelta(minutes=int(REFRESH_TOKEN_EXPIRE_MINUTES))
    
    payload = {"id": str(_id),"email": email,  "expires": expire_time.isoformat()}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM);


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        user = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"}
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"}
        )
    return user

def get_current_user_optional(token: str| None = None) -> dict | None:
    if token == None:
        return None
    try:
        user = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if user is None:
            return None
    except JWTError:
        return None
    return user



def is_superuser(user: Annotated [dict, Depends(get_current_user)]) -> bool:
    user_dict = User.find_one({"_id": user["id"]})
    if user_dict is not None and user_dict.get("is_superuser") == True:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not an admin user")


async def check_update_right(id: str, user_id: str, is_comment: bool = False, is_slug: bool = False) -> dict:
    if is_comment:
        item = await retrieve_comment(id)
    else:
        match is_slug:
            case True:
                item = await retrieve_article_by_slug(id)
            case False:
                item = await retrieve_article(id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{'Comment' if is_comment else 'Article'} not found"
        )

    if item["author"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not authorized to update this {'comment' if is_comment else 'article'}"
        )

    return item
