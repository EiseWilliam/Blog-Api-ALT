import re
from typing import Any
import unicodedata
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.utils.oauth import get_current_user_optional

from ..db.database import Article


templates = Jinja2Templates(directory="src/templates")

def slugify(string):

    """
    Slugify a unicode string.

    Example:

        >>> slugify(u"Héllø Wörld")
        u"hello-world"

    """

    return re.sub(r'[-\s]+', '-',
            str(
                re.sub(r'[^\w\s-]', '',
                    unicodedata.normalize('NFKD', string)
                    .encode('ascii', 'ignore')
                    .decode())
                .strip()
                .lower()))


async def unique_slug_id(title: str, Collection) -> str:
    """
    This function returns a slug that is unique to the database,
    it attaches a unique number to the slug if there is another article with same title
    """
    slug = slugify(title)
    # Check if the slug already exists in the database
    matches: int =  Article.count_documents({"slug": slug})
    if matches > 0:
        # Append a number to the end of the slug until it is unique
        count = 1
        while True:
            new_slug = f"{slug}-{count}"
            # Check if the new slug exists
            matches = Article.count_documents({"slug": new_slug})
            if matches == 0:
                return new_slug
            count += 1
    else:
        return slug


def render(request: Request, template_name:str, data: dict[str, Any]={}, status_code:int=200, add_cookies:dict={}, delete_cookies:list=[]):
    """
    Renders a template with the given context and returns an HTMLResponse object.

    Args:
        request (HttpRequest): The HTTP request object.
        template_name (str): The name of the template to render.
        data (dict, optional): The context to use when rendering the template. Defaults to {}.
        status_code (int, optional): The HTTP status code to use for the response. Defaults to 200.
        add_cookies (dict, optional): A dictionary of cookies to set on the response. Defaults to {}.
        delete_cookies (list, optional): A list of cookie names to delete from the response. Defaults to [].

    Returns:
        HTMLResponse: The rendered template as an HTMLResponse object.
    """
    context = data.copy()
    context.update({"request": request})
    template = templates.get_template(template_name)
    html_str = template.render(context)
    response = HTMLResponse(html_str, status_code=status_code)
    if len(add_cookies.keys()) > 0:
        # set httponly cookies
        for k, v in add_cookies.items():
            response.set_cookie(key=k, value=v, httponly=True)
    # delete coookies
    if len(delete_cookies) > 0:
        for k in delete_cookies:
            response.delete_cookie(k)
    return response


def compile_context(request:Request, data:dict[str, Any]={}) :
    access_token = request.cookies.get("access_token")
    logged_in = request.cookies.get("logged_in")
    current = get_current_user_optional(access_token)
    context: dict = {
        "request": request,
        "data": data,
        "access_token": access_token,
        "logged_in": logged_in,
        "user": current,
    }
    return context


def is_htmx(request:Request):
    return request.headers.get("hx-request") == 'true'