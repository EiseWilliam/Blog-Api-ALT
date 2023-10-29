from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status


from ..db.helper.interact import like_an_item, remove_like, check_if_user_has_liked, users_that_liked_an_item
from ..models.responses import ErrorMessageResponse, MessageResponse
from ..utils.oauth import get_current_user

router = APIRouter()



@router.get("/articles/{slug}/likes", status_code=status.HTTP_200_OK)
async def get_likes_on_article(slug: str) -> Any:
    users = await users_that_liked_an_item(slug) 
    return {"likes": len(users), "liked_by": users}
    
# likes on a comment
@router.get("/articles/{slug}/{comment_id}", status_code=status.HTTP_200_OK)
async def get_likes_on_comment(comment_id: str) -> Any:
    users = await users_that_liked_an_item(comment_id, True) 
    return {"likes": len(users), "liked_by": users}


@router.post(
    "/articles/{slug}+",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        400: {"model": ErrorMessageResponse},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
        409: {"model": ErrorMessageResponse},
    },
)
async def like_article(
    slug: str, user: Annotated[dict, Depends(get_current_user)]
) -> Any:
    feedback = await like_an_item(slug, user["id"])  # type: ignore
    if feedback == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user have already liked this article",
        )
    return MessageResponse(message="liked article sucessfully")



@router.post(
    "/comments/{comment}+",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        400: {"model": ErrorMessageResponse},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
        409: {"model": ErrorMessageResponse},
    },
)
async def like_comment(comment: str, user: Annotated[dict, Depends(get_current_user)]):
    feedback = await like_an_item(comment, user["id"], True)  # type: ignore
    if feedback == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user has already liked this comment",
        )
    return {"message": "liked comment sucessfully"}

# remove like
@router.delete(
    "/articles/{slug}-",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        400: {"model": ErrorMessageResponse},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
    },
)
async def remove_like_article(
    slug: str, user: Annotated[dict, Depends(get_current_user)]
) -> Any:
    feedback = await remove_like(slug, user["id"])  # type: ignore
    if feedback == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user have not liked this article",
        )
    return MessageResponse(message="removed like on article sucessfully")


# remove like on a comment
@router.delete(
    "/comments/{comment}-",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        400: {"model": ErrorMessageResponse},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
    },
)
async def remove_like_comment(
    comment: str, user: Annotated[dict, Depends(get_current_user)]
):
    feedback = await remove_like(comment, user["id"], True)  # type: ignore
    if feedback == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user has not liked this comment",
        )
    return {"message": "removed like on comment sucessfully"}



