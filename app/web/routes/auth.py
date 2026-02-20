from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.templates.config import templates

router = APIRouter()


@router.get("/login")
async def hello(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Home"}
    )


@router.get("/register")
async def create_account(request: Request):
    return templates.TemplateResponse(
        "create-account.html", {"request": request, "title": "Forgot password"}
    )


@router.get("/forgot-password")
async def forgot_password(request: Request):
    return templates.TemplateResponse(
        "forgot-password.html", {"request": request, "title": "Forgot password"}
    )
