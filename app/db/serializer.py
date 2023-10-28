
from ..schemas.response.user import UserProfileResponse
from ..schemas.users import Profile


# Database serializers
def profile_object(profile) -> Profile | dict:
    return{
        "first_name": profile.get("first_name"),
        "last_name": profile.get("last_name"),
        "bio": profile.get("bio"),
        "contact": profile.get("contact"),
        "photo": profile.get("photo"),
    }
    

def full_profile_entity(user) -> UserProfileResponse | dict:
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


async def user_list_entity(users) -> list[dict]:
    users_list = [user_entity(user) for user in users]
    return users_list



def article_entity(article: dict) -> dict:
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


async def article_list_entity(article_list) -> list[dict]:
    list_ = [article_entity(article) for article in article_list]
    return list_

                   

def comment_entity(comment) -> dict:
    return {
        "id": str(comment.get("_id")),
        "article": comment.get("article"),
        "author": comment.get("author"),
        "content": comment.get("content"),
        "date_posted": comment.get("date_posted"),
        "date_updated": comment.get("date_updated"),
    }

            
            

async def comment_list_entity(comment_list) -> list[dict]:
    list_ = [comment_entity(comment) for comment in comment_list]
    return list_