from fastapi import (
    APIRouter,
    Body,
    Depends,
    Form,
    HTTPException,
    Query,
    Response,
    status,
)
from typing import Annotated, Any


# from app.auth import oauth2
from ..db.helper.article import article_list_by_author, create_article
from ..db.helper.user import (
    create_user,
    delete_user,
    dynamic_user_search,
    find_user,
    retrieve_user,
    update_user,
)
from ..models.responses import (
    ArticleListResponseModel,
    ArticleResponseModel,
    ErrorMessageResponse,
    MessageResponse,
    PostRefrenceResponseModel,
    UserListResponseModel,
    UserResponseModel,
)
from ..schemas.articles import CreateArticle
from ..schemas.response.user import CurrentUser, UserProfileResponse
from ..schemas.users import UpdateUser, User, UserQuery
from ..utils.oauth import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    hash_password,
    verify_password,
)

router = APIRouter()


# get logged in user profile
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": UserResponseModel},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
        500: {"model": ErrorMessageResponse},
    },
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
@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
        500: {"model": ErrorMessageResponse},
    },
)
async def update_profile(
    user_details: UpdateUser, user: Annotated[dict, Depends(get_current_user)]
) -> Any:
    """
    Update the profile of the currently logged in user.
    """
    profile = await update_user(user["id"], user_details)  # type: ignore
    if profile == None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not Updated"
        )
    return MessageResponse(message="User profile updated successfully")


# get my articles
@router.get(
    "/articles",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": ArticleListResponseModel},
        401: {"model": ErrorMessageResponse},
    },
)
async def my_articles(user: Annotated[dict, Depends(get_current_user)]) -> Any:
    """
    Get the articles of the currently logged in user.
    """
    articles = await article_list_by_author(user["id"])
    if articles:
        return ArticleListResponseModel(
            articles=articles, message="Articles retrieved successfully"
        )
    else:
        return ArticleListResponseModel(articles=[], message="No articles found")


@router.post(
    "/article",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": PostRefrenceResponseModel},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
        500: {"model": ErrorMessageResponse},
    },
)
async def Publish_new_article(
    article: CreateArticle, user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    result = await create_article(article, user)
    if result == False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Article creation failed",
        )
    else:
        print(result)
        return {
            "message": "Article created successfully",
            "post": result,
        }  


# delete my account
@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
        500: {"model": ErrorMessageResponse},
    },
)
async def delete_account(user: Annotated[dict, Depends(get_current_user)]) -> dict:
    """
    delete my account
    """
    if await delete_user(user["id"]) == False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User not Deleted"
        )
    return {"status": "success", "message": "User Deleted Successfully"}


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


@router.get("/{user_id}", response_model=UserResponseModel, response_description="User profile retrieved successfully")
async def get_user_details(user_id: str) -> Any:
    details = retrieve_user(user_id)
    return UserResponseModel(user=details, message="User profile retrieved successfully") # type: ignore