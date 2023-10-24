
from db.database import User, Article, Comment
from db.serializer import user_entity, article_entity, comment_entity, user_list_entity
from schemas.comments import CreateComment, UpdateComment
from schemas.users import CreateUser, UpdateUser, UserQuery
from utils.oauth import hash_password

from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime


# add a created timestamp
def create_user(user_data: CreateUser) -> tuple:
    """
    Inserts a new user into the database.

    Args:
        user_data: A CreateUser object containing the user's data.

    Returns:
        A tuple containing the inserted ID and the user's email.

    Raises:
        HTTPException: If the insertion failed.
    """
    user_data.password = hash_password(user_data.password)
    user_data.email = user_data.email.lower()
    del user_data.confirm_password
    user = user_data.model_dump()
    user["date_created"] = datetime.now()
    user["date_updated"] = user["date_created"]
    result = User.insert_one(user)

    if result.inserted_id:
        return result.inserted_id, user_data.email
    else:
        raise HTTPException(status_code=500, detail="Failed to create user")


# update user
async def update_user(id: str, user_details) -> bool:
    """
    Updates an existing user in the database.

    Args:
        id: The ID of the user to update.
        user_details: A dictionary containing the updated user data.

    Returns:
        True if the update was successful

    Raises:
        HTTPException: If the update failed.
    """
    user = User.find_one({"_id": ObjectId(id)})
    if user:
        user_data = user_details.model_dump(exclude_unset=True)
        user_data["date_updated"] = datetime.now()
        try:
            result = User.update_one({"_id": ObjectId(id)}, {"$set": user_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f" {str(e)}")
        return result.acknowledged
    else:
        raise HTTPException(status_code=404, detail="User not found")



# retrieve user
def retrieve_user(id: str) -> dict | None:
    """
    Retrieves a user from the database.

    Args:
        id: The ID of the user to retrieve.

    Returns:
        A dictionary containing the user's data.

    Raises:
        HTTPException: If the user was not found.
    """
    user = User.find_one({"_id": ObjectId(id)})
    if user:
        serialized_user = user_entity(user)
        return serialized_user
    else:
        raise HTTPException(status_code=404, detail="User not found")


# find user by email
def find_user(email: str) -> dict | None:
    """
    Finds a user in the database by email.

    Args:
        email: The email address of the user to find.

    Returns:
        A dictionary containing the user's data.
        None if the user was not found.
    """
    user = User.find_one({"email": email.lower()})
    if user:
        serialized_user = user_entity(user)
        return serialized_user



async def dynamic_user_search(query: str) -> list[dict]:
    """
    Searches the database for users whose name or email contains the given query.

    Args:
        query: The search query.

    Returns:
        A list of dictionaries containing the data of the matching users.
    """
    if len(query) < 4:
        return []

    users = User.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"email": {"$regex": query, "$options": "i"}},
        ]
    })

    serialized_users = await user_list_entity(users)
    return serialized_users
    


# delete user from db
async def delete_user(user_id: str) -> bool | None:
    """
    Deletes a user from the database.

    Args:
        user_id: The ID of the user to delete.

    Returns:
        True if the user was deleted, False otherwise.

    Raises:
        HTTPException: If the user was not found.
    """
    user = User.find_one({"_id": ObjectId(user_id)})
    if user:
        deleted = User.delete_one({"_id": ObjectId(user_id)})
        if deleted:
            return True
    else:
        raise HTTPException(status_code=404, detail="User not found")
