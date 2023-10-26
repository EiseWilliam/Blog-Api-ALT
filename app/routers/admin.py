from fastapi import APIRouter, Depends

from ..utils.oauth import is_superuser, get_current_user

router = APIRouter()

@router.get("/admin/users",)
async def get_users(current_user: dict = Depends(is_superuser)):
    # Your code to get all users
    pass

@router.get("/admin/users/{user_id}", dependencies=[Depends(is_superuser)])
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    # Your code to get a specific user by ID
    pass

@router.post("/admin/users", dependencies=[Depends(is_superuser)])
async def create_user(user: str, current_user: dict = Depends(get_current_user)):
    # Your code to create a new user
    pass

@router.put("/admin/users/{user_id}", dependencies=[Depends(is_superuser)])
async def update_user(user_id: str, user: str, current_user: dict = Depends(get_current_user)):
    # Your code to update a user by ID
    pass

@router.delete("/admin/users/{user_id}", dependencies=[Depends(is_superuser)])
async def delete_user(user_id: str, current_user: dict = Depends(get_current_user)):
    # Your code to delete a user by ID
    pass
