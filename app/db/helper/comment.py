
from db.database import User, Article, Comment
from db.serializer import user_entity, article_entity, comment_entity, comment_list_entity
from schemas.comments import CreateComment, UpdateComment


from fastapi import HTTPException, status

from bson import ObjectId
from datetime import datetime

async def add_comment(comment: str, user_id: str, slug: str) -> str:
    comment_data = {}
    comment_data["content"] = comment
    comment_data["author"] = user_id
    comment_data["article"] = slug
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
    return str(result.inserted_id)


async def update_comment(id: str, comment_details: UpdateComment) -> str | bool:
    article_data = comment_details.model_dump(exclude_unset=True)
    article_data["date_updated"] = datetime.now()
    try:
        result =  Article.update_one({"_id": ObjectId(id)}, {"$set": article_data})
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"failure to update comment,DB error; {str(e)}",
        )
    return str(result.upserted_id)

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

# retreive comments on article
async def comment_list_on_article(slug_id: str) -> list:
    comments = list(comment for comment in Comment.find({"article": slug_id}))
    list_ = await comment_list_entity(comments)
    return list_
