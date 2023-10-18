from pymongo import MongoClient, ASCENDING
from pymongo.server_api import ServerApi


uri = "mongodb://localhost:27017/"

  # Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))


try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print("Unable to connect to the MongoDB server.")

db = client.get_database("blog_alt")
User = db.get_collection("users")
User.create_index ([("email", ASCENDING) ], unique=True )
Article = db.get_collection("articles")
Comment = db.get_collection("comments")