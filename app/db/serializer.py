from typing import Generator
from bson.objectid import ObjectId
from db.database import User, Article, Comment


# Database serializers
def user_entity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user.get("username"),
        "email": user["email"],
        "password": user["password"],
        "profile": user.get("profile"),
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
    }


async def user_list_entity() -> Generator:
    async for user in User.find():
        yield user_entity(user)


def article_entity(article) -> dict:
    return {
        "id": str(article["_id"]),
        "author": article["user_id"],
        "title": article["title"],
        "body": article["body"],
        "categories": article["categories"],
        "date_published": article["created_at"],
        "date_updated": article["updated_at"],
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
        "id": str(comment["_id"]),
        "article": comment["article_id"],
        "author": comment["user_id"],
        "content": comment["content"],
        "date_posted": comment["created_at"],
        "date_updated": comment["updated_at"],
    }

            
            

async def comment_list_by_article(article_id) -> Generator:
    """Generates list of comment on an article
    
    """
    async for comment_obj in Comment.find({"article": article_id}):
        yield article_entity(comment_obj)
