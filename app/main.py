from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from db.database import db
import uvicorn
from middleware.logger import CustomAPIRoute
from db.database import connect_to_db, close_db_connection
from middleware.errors import error_handler, http_422_error_handler

from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from routers import auth, articles, user, comments, blog

app = FastAPI()

origins = [
   config('CLIENT_ORIGIN'),
]



        # Add the middleware to the app
app.router.route_class = CustomAPIRoute

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.add_event_handler("startup", connect_to_db)
app.add_event_handler("shutdown", close_db_connection)
app.add_exception_handler(HTTPException, error_handler)



app.include_router(auth.router, tags=['Auth'], prefix='/auth')
app.include_router(user.router, tags=['User'], prefix='/user')
# app.include_router(blog.router, tags=['Blog'], prefix='/blog')
app.include_router(articles.router, tags=['Article'], prefix='/articles')
app.include_router(comments.router, tags=['Comments'], prefix='/articles')



@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to Blog API"}


@app.get("/api/test-mongodb-connection", status_code=200)
async def test_mongodb_connection():
    try:
        # Attempt to perform a simple database operation, like listing collections
        collections = []
        for collection in db.list_collection_names():
            collections.append(collection)
        return collections
    except Exception as e:
        # If an error occurs, return an error message
        raise HTTPException(status_code=500, detail=f"MongoDB connection failed: {str(e)}")

    


if __name__ == "__main__":
    uvicorn.run(app = "main:app", port=8000, reload=True)
