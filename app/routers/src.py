from typing import Annotated, Any
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import httpx

from app.utils.oauth import get_current_user_optional

from ..utils.util import render, compile_context
from .articles import get_all_articles, get_article_use_path

templates = Jinja2Templates(directory="src/templates")


router = APIRouter()




@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = await get_all_articles(10)
    data = data.articles
    context = compile_context(request, data)
    return templates.TemplateResponse("home.html", context)


@router.get("/login", response_class=HTMLResponse)
async def sign_in(request: Request):
    context = compile_context(request)
    return templates.TemplateResponse("auth/login.html", context)



@router.get("/register", response_class=HTMLResponse)
async def about(request: Request):
    context = compile_context(request)
    return templates.TemplateResponse("auth/register.html", context)


@router.get("/me", response_class=HTMLResponse)
async def my_profile(request: Request):
    context = compile_context(request)
    return templates.TemplateResponse("dashboard/me.html", context)


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def read_article(request: Request):
    data = await get_article_use_path(request.path_params["slug"])
    context = compile_context(request, data.article)
    return templates.TemplateResponse("view/article.html", context)




@router.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    pass
