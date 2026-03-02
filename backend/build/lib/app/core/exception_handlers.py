from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from app.core.config import template_settings

templates = Jinja2Templates(directory=template_settings.TEMPLATE_DIR)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )

        if exc.status_code == 404:
            return templates.TemplateResponse(
                "404.html",
                {"request": request},
                status_code=404,
            )

        return templates.TemplateResponse(
            "error.html",
            {"request": request, "detail": exc.detail},
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=422,
                content={"detail": exc.errors()},
            )

        return templates.TemplateResponse(
            "validation-error.html",
            {"request": request, "errors": exc.errors()},
            status_code=422,
        )
