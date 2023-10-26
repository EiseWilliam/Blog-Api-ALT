from fastapi import APIRouter, Body, Depends, HTTPException, status
from typing import Annotated, Any


from ..db.helper.article import check_if_slug_exists, retrieve_article_by_slug
from ..db.helper.comment import (add_comment, delete_comment,
                               get_comments_on_article, retrieve_comment,
                               update_comment)
from ..db.serializer import comment_entity, comment_list_entity
from ..models.responses import (CommentListResponseModel, ErrorMessageResponse,
                              MessageResponse, PostRefrenceResponseModel)
from ..schemas.comments import CreateComment, UpdateComment
from ..utils.oauth import check_update_right, get_current_user

router = APIRouter()


# get all comments on an article
@router.get(
    "/{slug}/comments",
    status_code=status.HTTP_200_OK,
    response_model=CommentListResponseModel,
)
async def get_comments(slug: str) -> Any:
    comments = await get_comments_on_article(slug)
    if comments:
        return CommentListResponseModel(
            message=f"{len(comments)} comments on article '{slug}' retrieved successfully",
            comments=comments,
        )
    article = await check_if_slug_exists(slug)
    if article == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="article not found",
        )
    return CommentListResponseModel(
        message=f"no comments on article '{slug}' yet, become the first", comments=[]
    )


# comment on an article
@router.post(
    "/{slug}/comments",
    status_code=status.HTTP_201_CREATED,
    response_model=PostRefrenceResponseModel,
)
async def post_comment_path(
    slug: str,
    comment: Annotated[CreateComment, Body(...)],
    user: Annotated[dict[str, str], Depends(get_current_user)],
) -> Any:
    article = check_if_slug_exists(slug)
    if article:
        comment_ref = await add_comment(comment, user["id"], slug)
        if comment_ref:
            return PostRefrenceResponseModel(
                message="Comment posted successfully",
                post={"id": comment_ref, "article": slug},
            )
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
# check if user can edit or delete comment
@router.get("/{slug}/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def can_edit_or_delete(comment_id: str, user: Annotated[dict, Depends(get_current_user)]) -> bool:
    if await check_update_right(comment_id, user["id"], True):
        return True
    else:
        return False
    
@router.patch(
    "/{slug}/comments/",
    status_code=status.HTTP_200_OK,
    response_model=PostRefrenceResponseModel,
)
async def edit_comment_path(
    slug: str,
    comment_id: str,
    comment: Annotated[CreateComment, Body(...)],
    user: Annotated[dict, Depends(get_current_user)],
) -> Any:
    if await check_update_right(comment_id, user["id"], True):
        result = await update_comment(comment_id, comment)
        if result == True:
            return PostRefrenceResponseModel(
                message="Comment updated successfully",
                post={"id": comment_id, "article": slug},
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="failed to update your comment",
            )


# delete a comment on an article
@router.delete(
    "/{slug}/comments/",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        404: {"model": ErrorMessageResponse},
        401: {"model": ErrorMessageResponse},
    },
)
async def delete_comment_path(
    slug: str, comment_id: str, user_id: Annotated[str, Depends(get_current_user)]
) -> dict:
    result = await delete_comment(comment_id)
    if result:
        return {"message": "Comment deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
