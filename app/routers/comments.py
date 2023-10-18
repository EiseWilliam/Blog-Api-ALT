from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Annotated
from schemas.comments import CreateComment, UpdateComment
from models.objectid import CusObjectId
from db.helper import add_comment, retrieve_comment, update_comment, delete_comment
from db.serializer import comment_entity, comment_list_by_article
from utils.oauth import get_current_user

router = APIRouter()


@router.get("/comments", status_code=status.HTTP_200_OK)
async def get_comments(article_id: CusObjectId) -> list:
    comments = []
    async for comment in comment_list_by_article(article_id):
        comments.append(comment)
    return comments


# comment in article
@router.get("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def get_comment(article_id: CusObjectId, comment: CusObjectId) -> dict:
    comment = retrieve_comment(article_id, comment)
    if comment:
        return comment
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )
 
# comment on an article
@router.post("/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(article_id: CusObjectId, comment: CreateComment, user_id: Annotated[str, Depends(get_current_user)]) -> dict:
    comment_data = comment.model_dump()
    comment_data["user_id"] = user_id
    comment_data["article_id"] = article_id
    comment_id = await add_comment(comment_data)
    if comment_id:
        return {"id": comment_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to post your comment",
        )
    
    