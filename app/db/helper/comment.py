from db.database import User, Article, Comment
from db.serializer import user_entity, article_entity, comment_entity
from schemas.comments import CreateComment, UpdateComment
from models.article import CreateArticleInDB, UpdateArticleInDB
from models.user import CreateUserInDB, UpdateUserInDB


from bson import ObjectId
from datetime import datetime

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
