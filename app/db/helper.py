from db.database import User, Article, Comment
from db.serializer import user_entity, article_entity, comment_entity
from schemas.comments import CreateComment, UpdateComment
from models.article import CreateArticleInDB, UpdateArticleInDB
from models.user import CreateUserInDB, UpdateUserInDB


from bson import ObjectId
from datetime import datetime


# add a created timestamp
def add_user(user_data: CreateUserInDB) -> str:
    try:
        # Insert the user data into the collection
        result = User.insert_one(user_data)

        # Check if the insertion was successful
        if result.inserted_id:
            return result.inserted_id
        else:
            return False

    except Exception as e:
        return str(e)


# update user
def update_user(id: str, user_details: UpdateUserInDB) -> dict:
    user = User.find_one({"_id": ObjectId(id)})
    if user:
        user_data = user_details.model_dump(exclude_unset=True)
        result = User.update_one({"_id": ObjectId(id)}, {"$set": user_data})
        return result.upserted_id
    else:
        return False


# retreive user
async def retrieve_user(user_id: str) -> dict:
    user = User.find_one({"_id": ObjectId(user_id)})
    if user:
        return user_entity(user)


# find user by email
def find_user(email: str) -> dict:
    try:
        user = User.find_one({"email": email})
        if user:
            # Serialize the user document into a dictionary
            serialized_user = user_entity(user)
            return serialized_user
        else:
            return None
    except Exception as e:
        return str(e)


# delete user from db
async def delete_user(user_id: str):
    user = await User.find_one({"_id": ObjectId(user_id)})
    if user:
        await User.delete_one({"_id": ObjectId(user_id)})
        return True


# ARTICLE HELPER FUNCTIONS
# ARTICLE HELPER FUNCTIONS
# ARTICLE HELPER FUNCTIONS


async def add_article(article_data: CreateArticleInDB) -> str:
    try:
        # Insert the user data into the collection
        result = await Article.insert_one(article_data)

        # Check if the insertion was successful
        if result.inserted_id:
            return result.inserted_id
        else:
            return False

    except Exception as e:
        return str(e)



async def update_article(id: str, article_details: UpdateArticleInDB) -> dict:
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


async def delete_article(article_id: str):
    article = await Article.find_one({"_id": ObjectId(article_id)})
    if article:
        try:
            await Article.delete_one({"_id": ObjectId(article_id)})
        except Exception as e:
            return str(e)
        else:
            return True


# COMMENT HELPER FUNCTIONS
# COMMENT HELPER FUNCTIONS


async def add_comment(comment_data: CreateComment) -> str|bool:
    try:
        # Insert the user data into the collection
        result = await Comment.insert_one(comment_data)

        # Check if the insertion was successful
        if result.inserted_id:
            return result.inserted_id
        else:
            return False
    except Exception as e:
        return str(e)


async def update_comment(id: str, comment_details: UpdateComment) -> str | bool:
    comment = await Comment.find_one({"_id": ObjectId(id)})
    if comment:
        comment_data = comment_details.model_dump(exclude_unset=True)
        result = await Comment.update_one({"_id": ObjectId(id)}, {"$set": comment_data})
        return result.upserted_id
    else:
        return False


async def retrieve_comment(comment_id: str) -> dict:
    comment = await Comment.find_one({"_id": ObjectId(comment_id)})
    if comment:
        return comment_entity(comment)


async def delete_comment(comment_id: str) -> str | bool:
    comment = await Comment.find_one({"_id": ObjectId(comment_id)})
    if comment:
        try:
            await Comment.delete_one({"_id": ObjectId(comment_id)})
        except Exception as e:
            return str(e)
        else:
            return True
