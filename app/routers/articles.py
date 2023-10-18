from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Annotated
from schemas.articles import CreateArticle, UpdateArticle, ArticleList
from db.helper import add_article, retrieve_article, update_article, delete_article
from db.serializer import article_list_entity, article_list_by_author
from models.objectid import CusObjectId
from utils.oauth import get_current_user, check_update_right


router = APIRouter()


@router.get("/articles", status_code=status.HTTP_200_OK, response_model=ArticleList)
async def get_articles(n: int = 5) -> dict:
    articles = []
    while len(articles) < n:
        async for article in article_list_entity():
            articles.append(article)
    return {"articles": articles}


@router.get("/articles/{article_id}", status_code=status.HTTP_200_OK)
async def get_article(article_id: str) -> dict:
    article = retrieve_article(article_id)
    if article:
        return article
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )


@router.get("/articles/author/{user_id}", status_code=status.HTTP_200_OK)
async def get_articles_by_author(user_id: str) -> list:
    articles = []
    async for article in article_list_by_author(user_id):
        articles.append(article)
    return articles


@router.post("/articles", status_code=status.HTTP_201_CREATED)
async def create_article(
    article: CreateArticle, user_id: Annotated[str, Depends(get_current_user)]
) -> dict:
    article_data = article.model_dump()
    article_data["user_id"] = user_id
    article_id = await add_article(article_data)
    if article_id:
        return {"id": article_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Article creation failed",
        )


@router.put("/articles", status_code=status.HTTP_200_OK)
async def edit_article(
    article_id: str,
    article: Annotated[UpdateArticle, Body(...)],
    can_edit: bool = Depends(check_update_right),
) -> dict:
    if can_edit:
        article_data = article.model_dump()
        result = await update_article(article_id, article_data)
        if result:
            return {"id": result}
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
