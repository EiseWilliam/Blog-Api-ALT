from typing import Generator
from bson.objectid import ObjectId
from db.database import User, Article, Comment


# Database serializers
def profile_object(profile) -> dict:
    return{
        "first_name": profile.get("first_name"),
        "last_name": profile.get("last_name"),
        "bio": profile.get("bio"),
        "photo": profile.get("photo"),
    }
def full_profile_entity(user) -> dict:
    return {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "email": user.get("email"),
        "password": user.get("password"),
        "profile": profile_object(user.get("profile")),
        "date_created": user.get("date_created"),
        "date_updated": user.get("date_updated"),

    }

    
def user_entity(user) -> dict:
    return {
        "id": str(user.get("_id")),
        "username": user.get("username"),
        "email": user.get("email"),
        "password": user.get("password"),
        "profile": user.get("profile"),
        "date_created": user.get("date_created"),
        "date_updated": user.get("date_updated"),
    }


async def user_list_entity() -> Generator:
    async for user in User.find():
        yield user_entity(user)


def article_entity(article) -> dict:
    return {
        "id": str(article.get("_id")),
        "author": article.get("user_id"),
        "title": article.get("title"),
        "body": article.get("body"),
        "categories": article.get("categories"),
        "date_published": article.get("created_at"),
        "date_updated": article.get("updated_at"),
    }


async def article_list_entity() -> Generator:
    """Generates n list of articles
    :param n: Number of articles to generate
    :type n: int
    
    """
    for article_obj in Article.find():
        yield article_entity(article_obj)
        
            
async def article_list_by_author(user_id) -> Generator:
    """Generates list of articles by author
    
    """
    for article_obj in Article.find({"user_id": user_id}):
        yield article_entity(article_obj)




def comment_entity(comment) -> dict:
    return {
        "id": str(comment.get("_id")),
        "article": comment.get("article_id"),
        "author": comment.get("user_id"),
        "content": comment.get("content"),
        "date_posted": comment.get("created_at"),
        "date_updated": comment.get("updated_at"),
    }

            
            

async def comment_list_by_article(article_id) -> Generator:
    """Generates list of comment on an article
    
    """
    async for comment_obj in Comment.find({"article": article_id}):
        yield article_entity(comment_obj)
