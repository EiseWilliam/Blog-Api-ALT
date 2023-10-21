from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from typing import Annotated
from utils.oauth import get_current_user
from db.helper.interact import like_an_item

router = APIRouter()
    
@router.post("{article}/", status_code = status.HTTP_202_ACCEPTED)
async def like_article(article, user = Annotated[dict, Depends(get_current_user)]):
    feedback = like_an_item(article, user)
    if feedback == False:
        raise HTTPException()
    return {"message":"liked Article sucessfully"}
    
    
@router.post("{comment}/", status_code = status.HTTP_202_ACCEPTED)
async def like_article(comment, user = Annotated[dict, Depends(get_current_user)]):
    feedback = like_an_item(comment, user)
    if feedback == False:
        raise HTTPException()
    return {"message":"liked comment sucessfully"}
    
    

 
