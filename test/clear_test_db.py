
from app.db.database import Article, Comment, User


def clear_user():
    try:
        testuser = User.find_one_and_delete({"email": "test@example.com"})
        testuser1 = User.find_one_and_delete({"email": "test1@example.com"})
        testuser2 = User.find_one_and_delete({"email": "test2@example.com"})
        
        for user in [testuser, testuser1, testuser2]:
            if user:
                print(f"{user} found and deleted")
        return True
    except Exception as e:
        print(f"An exception occurred: {e}")
        return False



