from asyncio import streams
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status
from zmq import Message


from ..db.helper.interact import like_an_item, remove_like, check_if_user_has_liked
from ..models.responses import ErrorMessageResponse, MessageResponse
from ..utils.oauth import get_current_user

router = APIRouter()


@router.post(
    "/articles/{slug}+",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"model": MessageResponse},
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
            detail="You have already liked this article",
        )
    return MessageResponse(message="liked article sucessfully")


# remove like
@router.delete(
    "/articles/{slug}-",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"model": MessageResponse},
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
            detail="You have not liked this article",
        )


@router.post(
    "comments/{comment}+",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"model": MessageResponse},
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


# remove like on a comment
@router.delete(
    "comments/{comment}-",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"model": MessageResponse},
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


# check if user has liked item
@router.get(
    "/articles/{slug}/liked?",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        400: {"model": ErrorMessageResponse},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
    },
)
async def check_if_user_has_liked_article(
    slug: str, user: Annotated[dict, Depends(get_current_user)]
):
    feedback = await check_if_user_has_liked(slug, user["id"])  # type: ignore
    return feedback


@router.get(
    "/comments/{comment}/liked?",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": MessageResponse},
        400: {"model": ErrorMessageResponse},
        401: {"model": ErrorMessageResponse},
        404: {"model": ErrorMessageResponse},
    },
)
async def check_if_user_has_liked_comment(
    comment: str, user: Annotated[dict, Depends(get_current_user)]
):
    feedback = await check_if_user_has_liked(comment, user["id"], is_comment=True)  # type: ignore
    return feedback
