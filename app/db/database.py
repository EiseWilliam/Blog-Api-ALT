from pymongo import ASCENDING, MongoClient
from pymongo.server_api import ServerApi
from decouple import config

URI = "mongodb://localhost:27017/"
# URI = config("DB_URL")

  # Set the Stable API version when creating a new client
client = MongoClient(URI, server_api=ServerApi('1'))

def connect_to_db():
    try:
        conn = client.server_info()
        print(f'Connected to MongoDB {conn.get("version")}')

    except Exception:
        print("Unable to connect to the MongoDB server.")

def close_db_connection():
    try:
        client.close()
        print("Connection to MongoDB closed.")
    except Exception:
        print("Unable to close connection to MongoDB.")


db = client.get_database("blog_alt")
User = db.get_collection("users")
User.create_index ([("email", ASCENDING) ], unique=True )
Article = db.get_collection("articles")
Comment = db.get_collection("comments")
Like = db.get_collection("likes")