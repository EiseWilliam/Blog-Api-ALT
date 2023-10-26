from datetime import datetime
from fastapi import status
from fastapi import HTTPException


from ..database import Article, Comment, Like


async def check_if_user_has_liked(item: str, user: str, is_comment: bool = False) -> bool:
    # check if item exists
    match is_comment:
        case True:
            info = Comment.find_one({"_id": item})
            if info is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment does not exist",
                )
        case False:
            info = Article.find_one({"slug": item})
            if info is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Article does not exist",
                )
    info = Like.find_one({"item_id": item, "user_id": user})
    return info is not None


async def like_an_item(item: str, user: str, is_comment: bool = False) -> bool:
    if await check_if_user_has_liked(item, user, is_comment):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has already liked this item",
        )
    try:
        insert = Like.insert_one(
            {"item_id": item,
             "user_id": user, 
             "time_stamp": datetime.now()}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"DB error, {str(e)}"
        )
    return insert.acknowledged


async def remove_like(item: str, user: str, is_comment: bool = True) -> bool:
    if await check_if_user_has_liked(item, user, is_comment):
        try:
            info = Like.find_one_and_delete({"item_id": item, "user_id": user})
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"DB error, {str(e)}"
            )
        return info.acknowledged
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has not liked this item")
