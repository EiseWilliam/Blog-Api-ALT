from math import e
from typing import Annotated, Any, Callable
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, HTTPException, Request, Depends, Response
from fastapi.routing import APIRoute
from fastapi.templating import Jinja2Templates
import httpx
from app.routers.user import get_user_details

from app.utils.oauth import get_current_user_optional

from ..utils.util import render, compile_context
from .articles import get_all_articles, get_article_use_path, get_full_article

templates = Jinja2Templates(directory="demo/templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request,page: int = 1,):
    data = await get_all_articles(page, sort_by="date_created")
    page = page
    data = data.articles
    context = compile_context(request, data, page=page)
    return templates.TemplateResponse("home.html", context)


@router.get("/login", response_class=HTMLResponse)
async def sign_in(request: Request):
    context = compile_context(request)
    return templates.TemplateResponse("auth/login.html", context)



@router.get("/register", response_class=HTMLResponse)
async def about(request: Request):
    context = compile_context(request)
    return templates.TemplateResponse("auth/register.html", context)


@router.get("/profile", response_class=HTMLResponse)
async def my_profile(request: Request):
    context = compile_context(request)
    return templates.TemplateResponse("dashboard/me.html", context)


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def read_article(request: Request):
    data = await get_full_article(request.path_params["slug"])
    context = compile_context(request, data)
    return templates.TemplateResponse("view/article.html", context)


@router.get("/profile/new", response_class=HTMLResponse)
async def publish_article_page(request: Request):
    context = compile_context(request)
    return templates.TemplateResponse("dashboard/new.html", context)


@router.get("/user/{user_id}", response_class=HTMLResponse)
async def view_userprofile_page(request: Request, user_id: str):
    data = await get_user_details(user_id)
    context = compile_context(request, data)
    return templates.TemplateResponse("view/user.html", context)



