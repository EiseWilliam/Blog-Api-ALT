from db.database import User, Article, Comment
from db.serializer import user_entity, article_entity, comment_entity
from schemas.comments import CreateComment, UpdateComment
from utils.oauth import hash_password
from models.user import CreateUserInDB, UpdateUserInDB

from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime

# add a created timestamp
def create_user(user_data: CreateUserInDB) -> tuple|bool:
 
    # Insert the user data into the collection
    user_data.password = hash_password(user_data.password)
    user_data.email = user_data.email.lower()
    del user_data.confirm_password
    user = user_data.model_dump()
    user["date_created"] = datetime.now()
    user["date_updated"] = user["date_created"]
    result = User.insert_one(user)

    # Check if the insertion was successful
    if result.inserted_id:
        return result.inserted_id, user_data.email
    else:
        return False



# update user
def update_user(id: str, user_details) -> str | bool:
    user = User.find_one({"_id": ObjectId(id)})
    if user:
        user_data = user_details.model_dump(exclude_unset=True)
        user_data["date_updated"] = datetime.now()
        try:
            result = User.update_one({"_id": ObjectId(id)}, {"$set": user_data})
        except Exception as e:
            raise HTTPException(status_code=500, detail=f" {str(e)}")
        return result.upserted_id
    else:
        return False


# retreive user
def retreive_user(id: str) -> dict | None:
    user = User.find_one({"_id": ObjectId(id)})
    if user:
        # Serialize the user document into a dictionary
        serialized_user = user_entity(user)
        return serialized_user
    else:
        return None


# find user by email
def find_user(email: str) -> dict | None:
    user = User.find_one({"email": email.lower()})
    if user:
        # Serialize the user document into a dictionary
        serialized_user = user_entity(user)
        return serialized_user
    else:
        return None



# delete user from db
async def delete_user(user_id: str):
    user =  User.find_one({"_id": ObjectId(user_id)})
    if user:
        deleted = User.delete_one({"_id": ObjectId(user_id)})
        if deleted:
            return True
    return False
