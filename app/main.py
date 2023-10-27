
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles



from .middleware.errors import error_handler, http_422_error_handler
from .db.database import close_db_connection, connect_to_db, client
from .routers import articles, auth, blog, comments, user, interact, admin

app = FastAPI()


templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")


origins = [
    "http://localhost:3000",
]


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
app.include_router(admin.router, tags=['Super-user'], prefix='/dashboard')
# app.include_router(blog.router, tags=['Blog'], prefix='/blog')
app.include_router(articles.router, tags=['Article'], prefix='/articles')
app.include_router(comments.router, tags=['Comments'], prefix='/articles')
app.include_router(interact.router, tags=['Like'], prefix='/articles')





@app.get("/")
def home():
    return {"message": "Welcome to Blog API"}

# create the html index page
@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

@app.get("/about")
def about_page():
    return {"message": "Welcome to Blog API"}

@app.get("/api/test-mongodb-connection", status_code=200)
async def test_mongodb_connection():
    try:
        log = client.server_info()
        return {"message": "MongoDB connection successful",
                "server_info": log}
    except Exception as e:
        # If an error occurs, return an error message
        raise HTTPException(status_code=500, detail=f"MongoDB connection failed: {str(e)}")
