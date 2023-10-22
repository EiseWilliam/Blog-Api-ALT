from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Annotated
from schemas.articles import CreateArticle, UpdateArticle
from db.helper.article import create_article, delete_article_by_path, retrieve_article, update_article,get_n_articles, delete_article, retrieve_article_by_slug
from db.serializer import article_list_entity
from db.helper.article import article_list_by_author
from models.objectid import CusObjectId
from utils.oauth import get_current_user, check_update_right
from fastapi import Request, Response
from fastapi.routing import APIRoute
import time

class TimedRoute(APIRoute):
    def get_route_handler(self) :
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


router = APIRouter(route_class = TimedRoute)

# Query operations
@router.get("all/", status_code=status.HTTP_200_OK)
async def get_all_articles(n: int = 10) -> list[dict]:
    list = await get_n_articles(n)
    return  list


@router.get("/{user_id}/articles", status_code=status.HTTP_200_OK)
async def get_articles_by_author(user_id: str) -> list:
    articles = await article_list_by_author(user_id)
    return articles


@router.get("/", status_code=status.HTTP_200_OK)
async def get_article_by_id(article_id: str) -> dict:
    article = await retrieve_article(article_id)
    if article:
        return article
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


@router.put("/", status_code=status.HTTP_200_OK)
async def edit_article_by_id(
    article_id: str,
    article: Annotated[UpdateArticle, Body(...)],
    user: Annotated [dict, Depends(get_current_user)],
) -> dict:
    """
    Edit an article with the given article_id and update it with the provided article data.

    Args:
        article_id (str): The ID of the article to be updated.
        article (UpdateArticle): The updated article data.
        user (bool): The current user making the request.

    Returns:
        dict: A dictionary containing the ID of the updated article and a success message.

    Raises:
        HTTPException: If the user is not authorized to update the article or if the update fails.
    """
    if check_update_right(article_id, user['id']):
        result = await update_article(article_id, article)
        if result:
            return {"id": result,
                    "message": "Article updated successfully"}
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

@router.delete("/", status_code=status.HTTP_200_OK)
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
@router.put("/{slug}", status_code=status.HTTP_200_OK)
async def edit_article_use_path(
    slug: str,
    article: Annotated[UpdateArticle, Body(...)],
    user: Annotated [dict, Depends(get_current_user)],
) -> dict:
    if check_update_right(slug, user['id']):
        result = await update_article(slug, article)
        if result:
            return {"id": result,
                    "message": "Article updated successfully"}
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


@router.get("/{slug}s", status_code=status.HTTP_200_OK)
async def get_article_use_path(slug: str) -> dict:
    article = await retrieve_article_by_slug(slug)
    if article:
        return article
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )
        
@router.delete("/{slug}", status_code=status.HTTP_200_OK)
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