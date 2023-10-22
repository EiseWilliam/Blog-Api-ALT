from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status
from models.objectid import CusObjectId
from db.helper.article import retrieve_article_by_slug, retrieve_article
from db.helper.comment import retrieve_comment
from schemas.response.user import CurrentUser

from config.settings import JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES


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


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> CurrentUser:
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



async def check_update_right(id: str, user_id: str, is_comment: bool = False):
    if is_comment:
        item = await retrieve_comment(id)
    else:
        item = await retrieve_article_by_slug(id) or await retrieve_article(id)

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
