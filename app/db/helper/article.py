from db.database import User, Article, Comment
from db.serializer import user_entity, article_entity, article_list_entity, comment_entity
from schemas.articles import CreateArticle, UpdateArticle



from bson import ObjectId
from datetime import datetime


async def add_article(article_data: CreateArticle) -> str:
    try:
        # Insert the user data into the collection
        result = await Article.insert_one(article_data)

        # Check if the insertion was successful
        if result.inserted_id:
            return result.inserted_id
        else:
            return False

    except Exception as e:
        return str(e)



async def update_article(id: str, article_details: UpdateArticle) -> dict:
    article = await Article.find_one({"_id": ObjectId(id)})
    if article:
        article_data = article_details.model_dump(exclude_unset=True)
        result = await Article.update_one({"_id": ObjectId(id)}, {"$set": article_data})
        return result.upserted_id
    else:
        return False


async def retrieve_article(article_id: str) -> dict:
    article = await Article.find_one({"_id": ObjectId(article_id)})
    if article:
        return article_entity(article)



async def article_list_by_author(user_id) -> list:
    """Returns list of articles by author
    
    """
    articles = (article for article in Article.find({"user_id": user_id}))
    return article_list_entity(articles)


async def delete_article(article_id: str):
    article = await Article.find_one({"_id": ObjectId(article_id)})
    if article:
        try:
            await Article.delete_one({"_id": ObjectId(article_id)})
        except Exception as e:
            return str(e)
        else:
            return True


