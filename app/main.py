import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from db.database import db
import uvicorn
from middleware.logger import CustomAPIRoute


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


app.include_router(auth.router, tags=['Auth'], prefix='/auth')
app.include_router(user.router, tags=['User'], prefix='/user')
app.include_router(blog.router, tags=['Blog'], prefix='/blog')
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
    

async def run_app():
    uvicorn.run(app = "main:app", port=8000, reload=True)

if __name__ == "__main__":
    asyncio.run(run_app())
