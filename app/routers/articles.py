
from typing import Annotated, Any
from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.routers.comments import get_article_comments


from ..models.responses import (
    ArticleListResponseModel,
    ArticleResponseModel,
    ErrorMessageResponse,
    MessageResponse,
    PostRefrenceResponseModel,
    ViewArticleResponseModel,
)
from ..schemas.articles import CreateArticle, UpdateArticle
from ..utils.oauth import check_update_right, get_current_user
from ..db.helper.article import (
    article_list_by_author,
    create_article,
    delete_article,
    delete_article_by_path,
    get_n_articles,
    retrieve_article,
    retrieve_article_by_slug,
    update_article,
    update_article_slug,
)



router = APIRouter()


# Query operations
@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=ArticleListResponseModel,
)
async def get_all_articles(page: int = 1,page_size: int = 10, sort_by: str | None = None, tags: str | None = None) -> Any:
    list = await get_n_articles(page,page_size,sort_by, tags)
    if list:
        return ArticleListResponseModel(articles=list,message=f"{len(list)} Articles retrieved successfully")
    else:
        return ArticleListResponseModel(articles=[], message="No Articles yet")

@router.get(
    "/{slug}/get",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": ArticleResponseModel},
        404: {"model": ErrorMessageResponse},
    },
)
async def get_article_use_path(slug: str) -> Any:
    article = await retrieve_article_by_slug(slug)
    if article:
        return ArticleResponseModel(article=article, message="Article retrieved successfully")  # type: ignore
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )


@router.get(
    "/{slug}/read",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": ViewArticleResponseModel},
        404: {"model": ErrorMessageResponse},
    },
)
async def get_full_article(slug: str) -> Any:
    article = await retrieve_article_by_slug(slug)
    comments = await get_article_comments(slug)
    if article:
        return {"status": "success",
                "message": "Article retrieved successfully",
                "article": article,
                "comments": comments}
        

@router.get(
    "/{user_id}/articles",
    status_code=status.HTTP_200_OK,
    response_model=ArticleListResponseModel,
)
async def get_articles_by_author(user_id: str) -> Any:
    articles = await article_list_by_author(user_id)
    if articles:
        return ArticleListResponseModel(
            articles=articles,
            message=f"All {len(articles)} of user {user_id} Articles retrieved successfully",
        )
    else:
        return ArticleListResponseModel(articles=[], message="No Articles yet")


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": ArticleResponseModel},
        404: {"model": ErrorMessageResponse},
    },
)
async def get_article_by_id(article_id: str) -> Any:
    article = await retrieve_article(article_id)
    if article:
        return ArticleResponseModel(article=article, message="Article retrieved successfully")  # type: ignore
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )



@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"model": PostRefrenceResponseModel},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
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


@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": ArticleResponseModel},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
    },
)
async def edit_article_by_id(
    article_id: str,
    article: Annotated[UpdateArticle, Body(...)],
    user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    """
    Edit an article with the given article_id and update it with the provided article data.

    Args:
        article_id (str): The ID of the article to be updated.
        article (UpdateArticle): The updated article data.
        user (bool): The current user making the request.

    Returns:
        dict: A dictionary containing the updated article data.

    Raises:
        HTTPException: If the user is not authorized to update the article or if the update fails.
    """
    if await check_update_right(article_id, user["id"]):
        updated_article = await update_article(article_id, article)
        if updated_article:
            return ArticleResponseModel(article=updated_article, message="Article updated successfully")  # type: ignore
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Article update failed",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only the Author can edit this article",
        )

@router.patch(
    "/{slug}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": ArticleResponseModel},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
    },
)
async def edit_article_use_path(
    slug: str,
    article: Annotated[UpdateArticle, Body(...)],
    user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    if await check_update_right(slug, user["id"], is_slug=True):
        updated_article = await update_article_slug(slug, article)
        if updated_article:
            return ArticleResponseModel(article=updated_article, message="Article updated successfully")  # type: ignore
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Article update failed",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only the Author can edit this article",
        )


@router.delete(
    "/{slug}",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
    },
)
async def delete_article_use_path(
    slug: str, user: dict = Depends(get_current_user)
) -> Any:
    if await check_update_right(slug, user["id"], is_slug=True):
        result = await delete_article_by_path(slug)
        if result:
            return MessageResponse(message= "Article deleted successfully")
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Article delete failed",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only the Author can delete this article",
        )

@router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
    },
)
async def delete_article_by_id(
    article_id: str, user: dict = Depends(get_current_user)
) -> Any:
    """
    Delete an article with the given article_id.

    Args:
        article_id (str): The ID of the article to be deleted.
        user (bool): The current user making the request.

    Returns:
        dict: A dictionary containing a success message.

    Raises:
        HTTPException: If the user is not authorized to delete the article or if the deletion fails.
    """
    if await check_update_right(article_id, user["id"]):
        result = await delete_article(article_id)
        if result:
            return MessageResponse(message= "Article deleted successfully")
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Article delete failed",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only the Author can delete this article",
        )