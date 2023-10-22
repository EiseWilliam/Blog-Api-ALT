# from fastapi import APIRouter, Depends, HTTPException, status, Body
# from typing import Annotated
# from schemas.articles import CreateArticle, UpdateArticle
# from db.helper.article import create_article, retrieve_article, update_article,get_n_articles, delete_article, retrieve_article_by_slug
# from utils.oauth import get_current_user, check_update_right
# from schemas.comments import CreateComment, UpdateComment
# from models.objectid import CusObjectId
# from db.helper.comment import add_comment, retrieve_comment, update_comment, delete_comment
# from db.serializer import comment_entity, comment_list_on_article
# from utils.oauth import get_current_user


# router = APIRouter()




# @router.put("/{slug}", status_code=status.HTTP_200_OK)
# async def edit_article_use_path(
#     slug: str,
#     article: Annotated[UpdateArticle, Body(...)],
#     user: bool = Depends(get_current_user),
# ) -> dict:
#     if check_update_right(slug, user['id']):
#         result = await update_article(slug, article)
#         if result:
#             return {"id": result,
#                     "message": "Article updated successfully"}
#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Article update failed",
#             )
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Only the Author can edit this article",
#         )


# @router.get("/{slug}", status_code=status.HTTP_200_OK)
# async def get_article(slug: str) -> dict:
#     article = await retrieve_article_by_slug(slug)
#     if article:
#         return article
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
#         )
        
# @router.delete("/{slug}", status_code=status.HTTP_200_OK)
# async def delete_article_use_path(slug: str, user: dict = Depends(get_current_user)) -> dict:
#     if check_update_right(slug, user['id']):
#         result = await delete_article(slug)
#         if result:
#             return {"message": "Article deleted successfully"}
#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail="Article delete failed",
#             )
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Only the Author can delete this article",
#         )
        
# # get all comments on an article
# @router.get("/{slug}", status_code=status.HTTP_200_OK)
# async def get_comments(slug: str) -> list:
#     comments = []
#     async for comment in comment_list_by_article(slug):
#         comments.append(comment)
#     return comments


 
# # comment on an article
# @router.post("/{slug}", status_code=status.HTTP_201_CREATED)
# async def post_comment_path(slug: str, comment: CreateComment, user_id: Annotated[str, Depends(get_current_user)]) -> dict:
#     comment_id = await add_comment(comment, slug, user_id)
#     if comment_id:
#         return {"id": comment_id,
#                 "message": "Comment posted successfully"}
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="failed to post your comment",
#         )
        
# # edit a comment on an article
# @router.put("/{slug}/{comment_id}", status_code=status.HTTP_200_OK)
# async def edit_comment_path(slug: str, comment_id: str, comment: Annotated[UpdateComment, Body(...)], user_id: Annotated[str, Depends(get_current_user)]) -> dict:
#     result = await update_comment(comment_id, comment)
#     if result:
#         return {"id": result,
#                 "message": "Comment edited successfully"}
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="failed to update your comment",
#         )
        
# # delete a comment on an article
# @router.delete("/{slug}/{comment_id}", status_code=status.HTTP_200_OK)
# async def delete_comment_path(slug: str, comment_id: str, user_id: Annotated[str, Depends(get_current_user)]) -> dict:
#     result = await delete_comment(comment_id)
#     if result:
#         return {"message": "Comment deleted successfully"}
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="failed to delete your comment",
#         )
    