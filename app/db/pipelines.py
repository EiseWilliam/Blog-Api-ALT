from bson import ObjectId


# article pipeline
def article_pipeline(
    article_id: str | None = None,
    slug: str | None = None,
    is_slug: bool = False,
    sort_by: str | None = None,
    page: int | None = None,
    page_size: int | None = None,
    tag: str | None = None,
):
    """
    This function creates an article aggregation pipeline.

    Args:
        article_id (str | None): The ID of the article to query.
        slug (str | None): The slug of the article to query.
        is_slug (bool): Whether the query is based on a slug or not.
        sort_by (str | None): The field to sort the results by.
        page (int | None): The page number to return.
        page_size (int | None): The number of articles to return per page.
        tag (list | None): A list of tags to filter the results by.

    Returns:
        list: A MongoDB aggregation pipeline.
    """
    if slug is None and article_id is None:
        pipeline = [
            {
                "$lookup": {
                    "from": "users",
                    "let": {"authorId": {"$toObjectId": "$author"}},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$authorId"]}}}
                    ],
                    "as": "authorDetails",
                }
            },
            {"$unwind": "$authorDetails"},
            {
                "$project": {
                    "_id": 1,
                    "date_updated": 1,
                    "date_created": 1,
                    "categories": 1,
                    "title": 1,
                    "body": 1,
                    "slug": 1,
                    "author": "$authorDetails",
                }
            },
        ]
    elif is_slug:
        pipeline = [
            {"$match": {"slug": slug}},
            {
                "$lookup": {
                    "from": "users",
                    "let": {"authorId": {"$toObjectId": "$author"}},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$authorId"]}}}
                    ],
                    "as": "authorDetails",
                }
            },
            {"$unwind": "$authorDetails"},
            {
                "$project": {
                    "_id": 1,
                    "date_updated": 1,
                    "date_created": 1,
                    "categories": 1,
                    "title": 1,
                    "body": 1,
                    "slug": 1,
                    "author": "$authorDetails",
                }
            },
        ]
    else:
        pipeline = [
            {"$match": {"_id": ObjectId(article_id)}},
            {
                "$lookup": {
                    "from": "users",
                    "let": {"authorId": {"$toObjectId": "$author"}},
                    "pipeline": [
                        {"$match": {"$expr": {"$eq": ["$_id", "$$authorId"]}}}
                    ],
                    "as": "authorDetails",
                }
            },
            {"$unwind": "$authorDetails"},
            {
                "$project": {
                    "_id": 1,
                    "date_updated": 1,
                    "date_created": 1,
                    "categories": 1,
                    "title": 1,
                    "body": 1,
                    "slug": 1,
                    "author": "$authorDetails",
                }
            },
        ]

    if tag is not None:
        pipeline.append(
            {"$match": {"categories": {"$regex": "|".join(tag.split(","))}}}
        )

    if sort_by is not None:
        pipeline.append({"$sort": {sort_by: -1}})

    if page is not None and page_size is not None:
        pipeline.append({"$skip": (page - 1) * page_size})
        pipeline.append({"$limit": page_size})

    return pipeline


# comment pipeline
def comment_pipeline(
    article_slug: str,
    sort_by: str | None = None,
):
    """
    This function creates a comment aggregation pipeline.

    Args:
        article_slug (str): The slug of the article to find its comments.
        sort_by (str | None): The field to sort the results by.

    Returns:
        list: A MongoDB aggregation pipeline.
    """
    pipeline = [
        {"$match": {"article": article_slug}},
        {
            "$lookup": {
                "from": "users",
                "let": {"authorId": {"$toObjectId": "$author"}},
                "pipeline": [{"$match": {"$expr": {"$eq": ["$_id", "$$authorId"]}}}],
                "as": "authorDetails",
            }
        },
        {"$unwind": "$authorDetails"},
        {
            "$project": {
                "_id": 1,
                "content": 1,
                "date_posted": 1,
                "date_updated": 1,
                "author": "$authorDetails",
            }
        },
    ]

    if sort_by is not None:
        pipeline.append({"$sort": {sort_by: -1}})

    return pipeline
