
import re
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status

from app.db.pipelines import comment_pipeline



from ..database import Comment
from ..serializer import comment_entity, comment_entity_lite, comment_list_entity
from ...schemas.comments import CreateComment


async def add_comment(comment: CreateComment, user_id: str, slug: str) -> str:
    comment_data = comment.model_dump()
    comment_data["author"] = user_id
    comment_data["article"] = slug
    comment_data["date_posted"] = datetime.now()
    comment_data["date_updated"] = comment_data["date_posted"]
        # Insert the user data into the collection
    try:
        result = Comment.insert_one(comment_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to create comment, DB error; {str(e)}",
        )
    return str(result.inserted_id)


async def update_comment(id: str, comment_details: CreateComment) -> bool:
    article_data = comment_details.model_dump(exclude_unset=True)
    article_data["date_updated"] = datetime.now()
    result =  Comment.update_one({"_id": ObjectId(id)}, {"$set": article_data})
    return result.acknowledged

async def retrieve_comment(comment_id: str) -> dict | None:
    comment = Comment.find_one({"_id": ObjectId(comment_id)})
    if comment:
        return comment_entity_lite(comment)


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
    else:
        return False
# retreive comments on article

async def get_comments_on_article(slug) -> list:
    comments = list(comment for comment in Comment.aggregate(comment_pipeline(slug)))
    comments = await comment_list_entity(comments)
    return comments

