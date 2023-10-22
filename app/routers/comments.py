from tabnanny import check
from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Annotated
from schemas.comments import CreateComment, UpdateComment
from models.objectid import CusObjectId
from db.helper.comment import add_comment, retrieve_comment, update_comment, delete_comment
from db.serializer import comment_entity, comment_list_by_article
from utils.oauth import get_current_user
from db.helper.article import retrieve_article_by_slug, check_if_slug_exists

router = APIRouter()


# get all comments on an article
@router.get("/{slug}", status_code=status.HTTP_200_OK)
async def get_comments(slug: str) -> list:
    comments = []
    async for comment in comment_list_by_article(slug):
        comments.append(comment)
    return comments


 
# comment on an article
@router.post("/{slug}", status_code=status.HTTP_201_CREATED)
async def post_comment_path(slug: str, comment: str, user: Annotated[dict, Depends(get_current_user)]) -> dict:
    article = check_if_slug_exists(slug)
    if article:
        comment_id = await add_comment(comment, slug, user["id"])
        if comment_id:
            return {"id": comment_id,
                    "message": "Comment posted successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="failed to post your comment",
            )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="article not found",
    )
        
# edit a comment on an article
@router.put("/{slug}/{comment_id}", status_code=status.HTTP_200_OK)
async def edit_comment_path(slug: str, comment_id: str, comment: Annotated[UpdateComment, Body(...)], user: Annotated[dict, Depends(get_current_user)]) -> dict:
    result = await update_comment(comment_id, comment)
    if result:
        return {"id": result,
                "message": "Comment edited successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to update your comment",
        )
        
# delete a comment on an article
@router.delete("/{slug}/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment_path(slug: str, comment_id: str, user_id: Annotated[str, Depends(get_current_user)]) -> dict:
    result = await delete_comment(comment_id)
    if result:
        return {"message": "Comment deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to delete your comment",
        )
    






