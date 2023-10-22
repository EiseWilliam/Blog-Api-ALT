import re
import unicodedata
from db.database import User, Article, Comment
from db.serializer import (
    user_entity,
    article_entity,
    article_list_entity,
    comment_entity,
)
from schemas.articles import CreateArticle, UpdateArticle




from bson import ObjectId
from datetime import datetime
from pymongo.collection import Collection
from fastapi import HTTPException, status


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



async def create_article(article_data: CreateArticle, user: dict) -> str:
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
    return str(result.inserted_id)
 


async def update_article(id: str, article_details: UpdateArticle) -> dict:
    article_data = article_details.model_dump(exclude_unset=True)
    article_data["date_updated"] = datetime.now()
    try:
        result =  Article.update_one({"_id": ObjectId(id)}, {"$set": article_data})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to update article,DB error; {str(e)}",
        )
    return result.upserted_id

async def retrieve_article_by_slug(slug_id: str) -> dict | None:
    article = Article.find_one({"slug": slug_id})
    if article:
        return article_entity(article)

async def check_if_slug_exists(slug_id: str) -> bool:
    article = Article.find_one({"slug": slug_id})
    if article:
        return True
    return False

async def retrieve_article(article_id: str) -> dict | None:
    article = Article.find_one({"_id": ObjectId(article_id)})
    if article:
        return article_entity(article)

async def get_n_articles(n: int) -> list:
    articles = list(article for article in Article.find().limit(n))
    list_ = await article_list_entity(articles)
    return list_

async def article_list_by_author(user_id) -> list:
    """Returns list of articles by author"""
    articles = list(article for article in Article.find({"author": user_id}))
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
