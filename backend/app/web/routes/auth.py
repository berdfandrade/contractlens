from fastapi import APIRouter, Request, Depends, Form, HTTPException
from app.models import user
from app.services.auth import AuthService
from app.services.token import TokenService
from app.api.deps import get_auth_service, get_token_service
from fastapi.responses import HTMLResponse, RedirectResponse
from app.templates.config import templates
from app.models.user import UserCreate

router = APIRouter()


@router.get("/login")
async def hello(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Home"}
    )


@router.post("/login")
async def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    auth: AuthService = Depends(get_auth_service),
    token: TokenService = Depends(get_token_service),
):
    user = await auth.authenticate_user(email, password)

    if not user:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Login",
                "error": "E-mail ou senha inválidos",
                "email": email,
            },
            status_code=400,
        )

    session_data = await token.create_session(user["id"])

    session_id = session_data["session_id"]

    response = RedirectResponse("/dashboard", status_code=302)

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
    )

    return response


@router.get("/register")
async def create_account(request: Request):
    return templates.TemplateResponse(
        "create-account.html", {"request": request, "title": "Forgot password"}
    )


@router.post("/register")
async def register_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    auth: AuthService = Depends(get_auth_service),
):
    await auth.register_user(UserCreate(name=name, email=email, password=password))

    if not user:
        return templates.TemplateResponse(
            "create-account.html",
            {
                "request": request,
                "title": "Criar conta",
                "error": "E-mail já cadastrado",
                "email": email,
            },
            status_code=400,
        )

    return RedirectResponse("/login", status_code=302)


@router.get("/forgot-password")
async def forgot_password(request: Request):
    return templates.TemplateResponse(
        "forgot-password.html", {"request": request, "title": "Forgot password"}
    )


@router.get("/reset-password")
async def reset_password_page(request: Request, token: str):
    return templates.TemplateResponse(
        "reset-password.html",
        {
            "request": request,
            "token": token,
        },
    )
