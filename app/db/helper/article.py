from db.database import User, Article, Comment
from db.serializer import (
    user_entity,
    article_entity,
    article_list_entity,
    comment_entity,
)
from schemas.articles import CreateArticle, UpdateArticle
from slugify import slugify


from bson import ObjectId
from datetime import datetime
from pymongo.collection import Collection


async def unique_slug(title: str, ArticleDB: Collection) -> str:
    """
    This function returns a slug that is unique to the database,
    it attaches a unique number to the slug if there is another article with same title
    """
    slug = slugify(title)
    # Check if the slug already exists in the database
    matches: int = len(Article.find({"slug": slug}))
    if matches > 1:
        # Append a number to the end of the slug until it is unique
        new_slug = f"{slug}-{matches}"
        return new_slug
    return slug


async def create_article(article: CreateArticle, user_id: str) -> str:
    # Generate the slug from the title
    article = article.model_dump()
    article["slug"] = unique_slug(article["title"])
    article["user_id"] = user_id
    article["date_created"] = datetime.now()
    article["date_updated"] = article["date_created"]

    # Insert the article data into the collection
    result = Article.insert_one(article)

    # Check if the insertion was successful
    if result.inserted_id:
        return str(result.inserted_id)
    else:
        return False


async def update_article(id: str, article_details: UpdateArticle) -> dict:
    article = await Article.find_one({"_id": ObjectId(id)})
    if article:
        article_data = article_details.model_dump(exclude_unset=True)
        result = await Article.update_one({"_id": ObjectId(id)}, {"$set": article_data})
        return result.upserted_id
    else:
        return False


async def retrieve_article(article_id: str) -> dict:
    article = await Article.find_one({"_id": ObjectId(article_id)})
    if article:
        return article_entity(article)


async def article_list_by_author(user_id) -> list:
    """Returns list of articles by author"""
    articles = (article for article in Article.find({"user_id": user_id}))
    return article_list_entity(articles)


async def delete_article(article_id: str):
    article = await Article.find_one({"_id": ObjectId(article_id)})
    if article:
        try:
            await Article.delete_one({"_id": ObjectId(article_id)})
        except Exception as e:
            return str(e)
        else:
            return True
