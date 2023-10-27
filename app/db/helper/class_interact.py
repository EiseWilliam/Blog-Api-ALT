from datetime import datetime
from fastapi import status
from fastapi import HTTPException
from typing import List


from ..database import Article, Comment, Like


class Item:
    def __init__(self, item_id: str, is_comment: bool = False, is_slug: bool = True):
        self.item_id = item_id
        self.is_comment = is_comment
        self.is_slug = is_slug

    def exists(self) -> bool:
        """
        Check if an item exists in the database.

        Returns:
            bool: True if the item exists, False otherwise.
        """
        match self.is_comment:
            case True:
                info = Comment.find_one({"_id": self.item_id})
                return info is not None
            case False:
                if self.is_slug:
                    info = Article.find_one({"slug": self.item_id})
                    return info is not None  
                info = Article.find_one({"_id": self.item_id})
                return info is not None


class LikeItem:
    def __init__(self, item_id: str, user_id: str, is_comment: bool = False):
        self.item_id = item_id
        self.user_id = user_id
        self.is_comment = is_comment

    def has_liked(self) -> bool:
        """
        Check if a user has liked an article or comment.

        Returns:
            bool: True if the user has liked the item, False otherwise.

        Raises:
            HTTPException: If the item does not exist.
        """
        item = Item(self.item_id, self.is_comment)
        if item.exists():
            info = Like.find_one({"item_id": self.item_id, "user_id": self.user_id})
            return info is not None
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{'Comment' if self.is_comment else 'Article'} does not exist",
        )

    def users_that_liked(self) -> List[str]:
        """
        Returns a list of user ids that have liked a given article or comment.

        Raises:
            HTTPException: If the item does not exist.

        Returns:
            List[str]: A list of user ids that have liked the item.
        """
        item = Item(self.item_id, self.is_comment)
        if item.exists():
            likes = Like.find({"item_id": self.item_id })
            users_that_liked = [item["user_id"] for item in likes]
            return users_that_liked
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{'Comment' if self.is_comment else 'Article'} does not exist")

    def like(self) -> bool:
        """
        Like an item.

        Raises:
            HTTPException: If the user has already liked the item.

        Returns:
            bool: True if the like was successfully inserted into the database, False otherwise.
        """
        if self.has_liked():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already liked this item",
            )
        try:
            insert = Like.insert_one(
                {"item_id": self.item_id, "user_id": self.user_id, "time_stamp": datetime.now()}
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"DB error, {str(e)}"
            )
        return insert.acknowledged

    def remove_like(self) -> bool:
        """
        Removes a like from the database for a given item and user.

        Raises:
            HTTPException: If the user has not liked the item or if there is a database error.

        Returns:
            bool: True if the like was successfully removed, False otherwise.
        """
        if self.has_liked():
            try:
                info = Like.find_one_and_delete({"item_id": self.item_id, "user_id": self.user_id})
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_501_NOT_IMPLEMENTED,
                    detail=f"DB error, {str(e)}",
                )
            return info.acknowledged
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User has not liked this item"
        )
