from ..schemas.response.user import UserProfileResponse
from ..schemas.users import Profile


# Database serializers
def profile_object(profile) -> Profile | dict:
    return {
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


# serializer for find and findone
def article_entity_lite(article) -> dict:
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

async def article_list_entity_lite(article_list) -> list[dict]:
    articles = [article_entity_lite(article) for article in article_list]
    return articles


# serializer for aggregate
def article_entity(result: dict) -> dict:
    return {
        "id": str(result["_id"]),
        "title": result["title"],
        "body": result["body"],
        "categories": result["categories"],
        "slug": result["slug"],
        "date_published": result["date_created"],
        "date_updated": result["date_updated"],
        "author": {
            "id": str(result["author"]["_id"]),
            "email": result["author"]["email"],
            "profile": result["author"].get("profile"),
            "username": result["author"]["username"],
            "date_created": result["author"]["date_created"],
        },
    }

async def article_list_entity(article_list) -> list[dict]:
    articles = [article_entity(article) for article in article_list]
    return articles

# serializer for aggregate
def comment_entity(result) -> dict:
    return {
        "id": str(result["_id"]),
        "author": {
            "id": str(result["author"]["_id"]),
            "email": result["author"]["email"],
            "profile": result["author"].get("profile"),
            "username": result["author"]["username"],
            "date_created": result["author"]["date_created"],
        },
        "content": result["content"],
        "date_posted": result["date_posted"],
        "date_updated": result["date_updated"],
    }

# serializer for find and findone
def comment_entity_lite(comment) -> dict:
    return {
        "id": str(comment.get("_id")),
        "article": comment.get("article"),
        "author": comment.get("author"),
        "content": comment.get("content"),
        "date_posted": comment.get("date_posted"),
        "date_updated": comment.get("date_updated"),
    }


async def comment_list_entity(comment_list) -> list[dict]:
    comments = [comment_entity(comment) for comment in comment_list]
    return comments


async def comment_list_entity_lite(comment_list) -> list[dict]:
    comments = [comment_entity_lite(comment) for comment in comment_list]
    return comments
