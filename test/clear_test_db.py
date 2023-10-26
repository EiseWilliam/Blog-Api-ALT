
from app.db.database import Article, Comment, User


def clear_user():
    emails = ["testuser0@example.com","testuser@example.com", "test@example.com","test1@example.com", "test2@example.com", "articletester@example.com", "articletester1@example.com"]
    deleted_users = User.delete_many({"email": {"$in": emails}})
    print(f"{deleted_users.deleted_count} users found and deleted")
    return True if deleted_users.deleted_count > 0 else False



