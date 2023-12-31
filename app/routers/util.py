# All routers here return boolean values
from typing import Annotated
from fastapi import Depends, status
from fastapi import APIRouter


from ..db.helper.interact import check_if_user_has_liked
from ..utils.oauth import check_update_right, get_current_user

router = APIRouter()


# check if user is authorized to edit article
@router.get("/{item_id}", status_code=status.HTTP_200_OK, response_model=bool)
async def is_authorized_to_edit(item_id: str, user: Annotated[dict, Depends(get_current_user)]) -> bool:
    if await check_update_right(item_id, user["id"]):
        return True
    return False

@router.get("/{slug}", status_code=status.HTTP_200_OK) 
async def can_edit_or_delete(slug: str, user: dict = Depends(get_current_user)) -> bool:
    if await check_update_right(slug, user["id"], is_slug=True):
        return True
    else:
        return False


# check if user has liked item
@router.get(
    "/articles/{slug}/liked?",
    status_code=status.HTTP_200_OK,
)
async def check_if_user_has_liked_article(
    slug: str, user: Annotated[dict, Depends(get_current_user)]
) -> bool:
    feedback = await check_if_user_has_liked(slug, user["id"])  # type: ignore
    return feedback


@router.get(
    "/comments/{comment}/liked?",
    status_code=status.HTTP_200_OK,
)
async def check_if_user_has_liked_comment(
    comment: str, user: Annotated[dict, Depends(get_current_user)]
) -> bool:
    feedback = await check_if_user_has_liked(comment, user["id"], is_comment=True)  # type: ignore
    return feedback
