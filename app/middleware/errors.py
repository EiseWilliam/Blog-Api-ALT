from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


async def error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"error": exc.detail},
                        status_code=exc.status_code)
