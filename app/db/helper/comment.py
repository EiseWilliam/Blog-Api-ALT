from db.database import User, Article, Comment
from db.serializer import user_entity, article_entity, comment_entity
from schemas.comments import CreateComment, UpdateComment
from models.user import CreateUserInDB, UpdateUserInDB

from fastapi import HTTPException, status

from bson import ObjectId
from datetime import datetime

async def add_comment(comment_data: CreateComment, user_id: str, slug: str) -> str|bool:
    comment_data = comment_data.model_dump()
    comment_data["author"] = user_id
    comment_data["slug"] = slug
    comment_data["date_posted"] = datetime.now()
    comment_data["date_updated"] = comment_data["date_posted"]
    try:
        # Insert the user data into the collection
        result = Comment.insert_one(comment_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to create comment,DB error; {str(e)}",
        )
    return result.inserted_id


async def update_comment(id: str, comment_details: UpdateComment) -> str | bool:
    comment = Comment.find_one({"_id": ObjectId(id)})
    if comment:
        comment_data = comment_details.model_dump(exclude_unset=True)
        result = await Comment.update_one({"_id": ObjectId(id)}, {"$set": comment_data})
        return result.upserted_id
    comment_details = comment_details.model_dump()
    comment_details["date_updated"] = datetime.now()
    try:
        # Insert the user data into the collection
        result = Comment.insert_one(comment_details)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to update comment,DB error; {str(e)}",
        )
    return result.inserted_id

async def retrieve_comment(comment_id: str) -> dict:
    comment = Comment.find_one({"_id": ObjectId(comment_id)})
    if comment:
        return comment_entity(comment)


async def delete_comment(comment_id: str) -> bool:
    comment = Comment.find_one({"_id": ObjectId(comment_id)})
    if comment:
        try:
            Comment.delete_one({"_id": ObjectId(comment_id)})
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"failure to delete comment,DB error; {str(e)}",
            )
        else:
            return True
