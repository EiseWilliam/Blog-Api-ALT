from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status


from ..db.helper.interact import like_an_item
from ..utils.oauth import get_current_user

router = APIRouter()
    
@router.post("{article}/", status_code = status.HTTP_202_ACCEPTED)
async def like_article(article, user = Annotated[dict, Depends(get_current_user)]):
    feedback = like_an_item(article, user)
    if feedback == False:
        raise HTTPException()
    return {"message":"liked Article sucessfully"}
    
    
@router.post("{comment}/", status_code = status.HTTP_202_ACCEPTED)
async def like_comment(comment, user = Annotated[dict, Depends(get_current_user)]):
    feedback = like_an_item(comment, user)
    if feedback == False:
        raise HTTPException()
    return {"message":"liked comment sucessfully"}
    
    

 
