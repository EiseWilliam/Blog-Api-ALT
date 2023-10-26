from datetime import datetime
from fastapi import status
from fastapi import HTTPException


from ..database import Article, Comment, Like


def check_if_item_exists(item: str, is_comment: bool = False, is_slug: bool = True) -> bool:
    """
    Check if an item exists in the database.

    Args:
        item (str): The ID of the item to check.
        is_comment (bool, optional): Whether the item is a comment or not. Defaults to False.
        is_slug (bool, optional): Whether the item is a slug or not. Defaults to True.

    Returns:
        bool: True if the item exists, False otherwise.
    """
    match is_comment:
        case True:
            info = Comment.find_one({"_id": item})
            return info is not None
        case False:
            if is_slug:
                info = Article.find_one({"slug": item})
                return info is not None  
            info = Article.find_one({"_id": item})
            return info is not None


async def check_if_user_has_liked(
    item: str, user: str, is_comment: bool = False
) -> bool:
    """
    Check if a user has liked an article or comment.

    Args:
        item (str): The ID of the article or comment.
        user (str): The ID of the user.
        is_comment (bool, optional): Whether the item is a comment or an article. Defaults to False.

    Returns:
        bool: True if the user has liked the item, False otherwise.

    Raises:
        HTTPException: If the item does not exist.
    """
    if check_if_item_exists(item, is_comment):
        info = Like.find_one({"item_id": item, "user_id": user})
        return info is not None
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{'Comment' if is_comment else 'Article'} does not exist",
    )


async def users_that_liked_an_item(item: str, is_comment: bool = False):
    """
    Returns a list of user ids that have liked a given article or comment.

    Args:
        item (str): The id of the article or comment to check for likes.
        is_comment (bool, optional): Whether the item is a comment or an article. Defaults to False.

    Raises:
        HTTPException: If the item does not exist.

    Returns:
        List[str]: A list of user ids that have liked the item.
    """
    if check_if_item_exists(item, is_comment):
        likes = Like.find({"item_id": item })
        users_that_liked = [item["user_id"] for item in likes]
        return users_that_liked
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{'Comment' if is_comment else 'Article'} does not exist")


async def like_an_item(item: str, user: str, is_comment: bool = False) -> bool:
    """
    Like an item.

    Args:
        item (str): The ID of the item to like.
        user (str): The ID of the user who is liking the item.
        is_comment (bool, optional): Whether the item is a comment. Defaults to False.

    Raises:
        HTTPException: If the user has already liked the item.

    Returns:
        bool: True if the like was successfully inserted into the database, False otherwise.
    """
    if await check_if_user_has_liked(item, user, is_comment):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User has already liked this item",
        )
    try:
        insert = Like.insert_one(
            {"item_id": item, "user_id": user, "time_stamp": datetime.now()}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"DB error, {str(e)}"
        )
    return insert.acknowledged


async def remove_like(item: str, user: str, is_comment: bool = True) -> bool:
    """
    Removes a like from the database for a given item and user.

    Args:
        item (str): The ID of the item to remove the like from.
        user (str): The ID of the user who liked the item.
        is_comment (bool, optional): Whether the item is a comment or not. Defaults to True.

    Raises:
        HTTPException: If the user has not liked the item or if there is a database error.

    Returns:
        bool: True if the like was successfully removed, False otherwise.
    """
    if await check_if_user_has_liked(item, user, is_comment):
        try:
            info = Like.find_one_and_delete({"item_id": item, "user_id": user})
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail=f"DB error, {str(e)}",
            )
        return info.acknowledged
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User has not liked this item"
    )
