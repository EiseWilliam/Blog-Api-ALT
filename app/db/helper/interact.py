

async def like_an_item(item: str, user: str, collection):
    collection.insertOne({"item": item, "user": user})