from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from db.database import db
import uvicorn

from middleware.logger import logger, log_requests

from routers import auth, articles, user, comments

app = FastAPI()

origins = [
   config('CLIENT_ORIGIN'),
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.middleware("http")(log_requests)

app = FastAPI()


app.include_router(auth.router, tags=['Auth'], prefix='/auth')
app.include_router(user.router, tags=['User'], prefix='/user')
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
    

# start uvicorn server
if __name__ == "__main__":
    uvicorn.run(app = "main:app", port=8000, reload=True)

