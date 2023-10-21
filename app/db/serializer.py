from typing import Generator
from bson.objectid import ObjectId
from db.database import User, Article, Comment
from schemas.users import Profile
from schemas.response.user import UserProfileResponse


# Database serializers
def profile_object(profile) -> Profile:
    return{
        "first_name": profile.get("first_name"),
        "last_name": profile.get("last_name"),
        "bio": profile.get("bio"),
        "contact": profile.get("contact"),
        "photo": profile.get("photo"),
    }
    
def full_profile_entity(user) -> UserProfileResponse:
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
        "title": article.get("title"),
        "slug": article.get("slug"),
        "body": article.get("body"),
        "author": article.get("author"),
        "categories": article.get("categories"),
        "date_published": article.get("date_created"),
        "date_updated": article.get("date_updated"),
    }


async def article_list_entity(article_list) -> list:
    list_ = [article_entity(article) for article in article_list]
    return list_

                   

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
