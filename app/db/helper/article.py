import re
import unicodedata
from bson import ObjectId
from datetime import datetime
from typing import Any
from fastapi import HTTPException, status

from ...schemas.articles import CreateArticle, UpdateArticle
from ..database import Article, Comment, User
from ..serializer import (article_entity, article_list_entity, comment_entity,
                           user_entity)


def slugify(string):
    """
    Slugify a unicode string.

    Example:

        >>> slugify(u"Héllø Wörld")
        u"hello-world"
    """
    return re.sub(r'[-\s]+', '-',
            str(
                re.sub(r'[^\w\s-]', '',
                    unicodedata.normalize('NFKD', string)
                    .encode('ascii', 'ignore')
                    .decode())
                .strip()
                .lower()))


async def unique_slug_id(title: str) -> str:
    """
    This function returns a slug that is unique to the database,
    it attaches a unique number to the slug if there is another article with same title
    """
    slug = slugify(title)
    # Check if the slug already exists in the database
    matches: int =  Article.count_documents({"slug": slug})
    if matches > 0:
        # Append a number to the end of the slug until it is unique
        count = 1
        while True:
            new_slug = f"{slug}-{count}"
            # Check if the new slug exists
            matches = Article.count_documents({"slug": new_slug})
            if matches == 0:
                return new_slug
            count += 1
    else:
        return slug


async def create_article(article_data: CreateArticle, user: dict) -> dict[str, str]:
    """
    Creates a new article in the database.

    Args:
        article_data (CreateArticle): The article data to be created.
        user (dict): The user creating the article.

    Returns:
        dict[str, str]: A dictionary containing the ID and slug of the newly created article.
    """
    # Generate the slug from the title
    article = article_data.model_dump()
    article["slug"] = await unique_slug_id(article["title"])
    article["author"] = user["id"]
    article["date_created"] = datetime.now()
    article["date_updated"] = article["date_created"]

    # Insert the article data into the collection
    try:
        result = Article.insert_one(article)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to create article,DB error; {str(e)}",
        )
    # Check if the insertion was successful
    return {"id": str(result.inserted_id),
            "slug": article["slug"]}


async def update_article(id: str, article_details: UpdateArticle) -> Any:
    """
    Updates an existing article in the database.

    Args:
        id (str): The ID of the article to be updated.
        article_details (UpdateArticle): The updated article data.

    Returns:
        Any: The updated article data.
    """
    article_data = article_details.model_dump(exclude_unset=True)
    article_data["date_updated"] = datetime.now()
    try:
        result =  Article.update_one({"_id": ObjectId(id)}, {"$set": article_data})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to update article,DB error; {str(e)}",
        )
    if result.acknowledged:
        return article_entity(Article.find_one({"_id": ObjectId(id)}))  # type: ignore


async def update_article_slug(slug: str, article_details: UpdateArticle) -> dict | None:
    """
    Updates an existing article in the database by its slug.

    Args:
        slug (str): The slug of the article to be updated.
        article_details (UpdateArticle): The updated article data.

    Returns:
        dict | None: The updated article data or None if the update was unsuccessful.
    """
    article_data = article_details.model_dump(exclude_unset=True)
    article_data["date_updated"] = datetime.now()
    try:
        result =  Article.update_one({"slug": slug}, {"$set": article_data})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to update article,DB error; {str(e)}",
        )
    if result.acknowledged:
        return article_entity(Article.find_one({"slug": slug}))  # type: ignore


async def retrieve_article_by_slug(slug_id: str) -> dict:
    """
    Retrieves an article from the database by its slug.

    Args:
        slug_id (str): The slug of the article to be retrieved.

    Returns:
        dict: The retrieved article data.
    """
    try:
        article = Article.find_one({"slug": slug_id})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to retrieve article,DB error {str(e)}",
        )
    return article_entity(article)


async def check_if_slug_exists(slug_id: str) -> bool:
    """
    Checks if an article with the given slug exists in the database.

    Args:
        slug_id (str): The slug to be checked.

    Returns:
        bool: True if an article with the given slug exists, False otherwise.
    """
    article = Article.find_one({"slug": slug_id})
    if article:
        return True
    return False


async def retrieve_article(article_id: str) -> dict | None:
    """
    Retrieves an article from the database by its ID.

    Args:
        article_id (str): The ID of the article to be retrieved.

    Returns:
        dict | None: The retrieved article data or None if the article was not found.
    """
    try:
        article = Article.find_one({"_id": ObjectId(article_id)})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to retrieve article,DB error {str(e)}",
        )
    if article:
        return article_entity(article)


async def get_n_articles(n: int) -> list:
    """
    Retrieves a list of the latest n articles from the database.

    Args:
        n (int): The number of articles to retrieve.

    Returns:
        list: A list of the latest n articles.
    """
    try:
        articles = list(article for article in Article.find().limit(n))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to retrieve articles,DB error; {str(e)}",
        )
    list_ = await article_list_entity(articles)
    return list_


async def article_list_by_author(user_id) -> list:
    """
    Retrieves a list of articles from the database by the author's ID.

    Args:
        user_id: The ID of the author.

    Returns:
        list: A list of articles written by the author.
    """
    try:
        articles = list(article for article in Article.find({"author": user_id}))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to retrieve articles,DB error; {str(e)}",
        )
    list_ = await article_list_entity(articles)
    return list_


async def delete_article(article_id: str):
    article = Article.find_one({"_id": ObjectId(article_id)})
    if article:
        try:
            Article.delete_one({"_id": ObjectId(article_id)})
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"failure to delete article,DB error; {str(e)}",
            )
        else:
            return True
        
async def delete_article_by_path(slug_id: str):
    article = Article.find_one({"slug": slug_id})
    if article:
        try:
            Article.delete_one({"slug": slug_id})
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"failure to delete article,DB error; {str(e)}",
            )
        else:
            return True
        
async def dynamic_article_search(query, category=None ):
    pass
    
