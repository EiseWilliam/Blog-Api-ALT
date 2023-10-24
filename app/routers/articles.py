from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Annotated, Any
from models.responses import ArticleListResponseModel, ArticleResponseModel, MessageResponse
from schemas.articles import CreateArticle, UpdateArticle
from db.helper.article import create_article, delete_article_by_path, retrieve_article, update_article,get_n_articles, delete_article, retrieve_article_by_slug, update_article_slug
from db.serializer import article_list_entity
from db.helper.article import article_list_by_author
from utils.oauth import get_current_user, check_update_right
import time


router = APIRouter()

# Query operations
@router.get("/all", status_code=status.HTTP_200_OK, response_model = ArticleListResponseModel)
async def get_all_articles(n: int = 10) -> Any:
    list = await get_n_articles(n)
    if list:
        return  ArticleListResponseModel(articles = list, message=f"{len(list)} Articles retrieved successfully")
    else:
        return ArticleListResponseModel(articles = [], message="No Articles yet")


@router.get("/{user_id}/articles", status_code=status.HTTP_200_OK, response_model=ArticleListResponseModel)
async def get_articles_by_author(user_id: str) -> Any:
    articles = await article_list_by_author(user_id)
    if articles:
        return  ArticleListResponseModel(articles = articles, message=f"All {len(articles)} of user {user_id} Articles retrieved successfully")
    else:
        return ArticleListResponseModel(articles = [], message="No Articles yet")


@router.get("/", status_code=status.HTTP_200_OK, response_model=ArticleResponseModel)
async def get_article_by_id(article_id: str) -> Any:
    article = await retrieve_article(article_id)
    if article:
        return ArticleResponseModel(article = article, message="Article retrieved successfully") #type: ignore
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def Publish_article(
    article: CreateArticle, user: Annotated[dict, Depends(get_current_user)]
) -> dict:
    return_id = await create_article(article,user)
    if return_id == False:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Article creation failed",
        )
    else:
        return {"id": return_id,
                "message": "Article published successfully"}


@router.patch("/", status_code=status.HTTP_200_OK, response_model=ArticleResponseModel)
async def edit_article_by_id(
    article_id: str,
    article: Annotated[UpdateArticle, Body(...)],
    user: Annotated [dict, Depends(get_current_user)],
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
    if await check_update_right(article_id, user['id']):
        updated_article = await update_article(article_id, article)
        print(updated_article)
        if updated_article:
            return ArticleResponseModel(article = updated_article, message="Article updated successfully") #type: ignore
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

@router.delete("/", status_code=status.HTTP_200_OK, response_model = MessageResponse)
async def delete_article_by_id(article_id: str, user: dict = Depends(get_current_user)) -> dict:
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
    if check_update_right(article_id, user['id']):
        result = await delete_article(article_id)
        if result:
            return {"message": "Article deleted successfully"}
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





# 
# Path Operations
@router.patch("/{slug}", status_code=status.HTTP_200_OK, response_model=ArticleResponseModel)
async def edit_article_use_path(
    slug: str,
    article: Annotated[UpdateArticle, Body(...)],
    user: Annotated [dict, Depends(get_current_user)],
) -> Any:
    if await check_update_right(slug, user['id']):
        updated_article = await update_article_slug(slug, article)
        if updated_article:
            return ArticleResponseModel(article = updated_article, message="Article updated successfully") # type: ignore
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


@router.get("/{slug}s", status_code=status.HTTP_200_OK, response_model=ArticleResponseModel)
async def get_article_use_path(slug: str) -> Any:
    article = await retrieve_article_by_slug(slug)
    if article:
        return ArticleResponseModel(article = article, message="Article retrieved successfully") #type: ignore
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
        
@router.delete("/{slug}", status_code=status.HTTP_200_OK, response_model = MessageResponse)
async def delete_article_use_path(slug: str, user: dict = Depends(get_current_user)) -> dict:
    if await check_update_right(slug, user['id']):
        result = await delete_article_by_path(slug)
        if result:
            return {"message": "Article deleted successfully"}
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