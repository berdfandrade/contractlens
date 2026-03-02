from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service, get_token_service
from app.services.auth import AuthService
from app.services.token import TokenService
from app.models.login import LoginSchema
from app.models.user import UserCreate
from app.api.exceptions.auth import (
    invalid_credentials,
    user_already_exists,
    error_creating_user,
)
from app.services.errors.user import UserAlreadyExistsError, ErrorOnCreatingUser


router = APIRouter(prefix="/auth", tags=["🔒 Auth"])


@router.post("/login")
async def login(
    data: LoginSchema,
    auth: AuthService = Depends(get_auth_service),
    token: TokenService = Depends(get_token_service),
):
    user = await auth.authenticate_user(data.email, data.password)
    if not user:
        return invalid_credentials()

    session = await token.create_session(user["id"])
    return session


@router.post("/register")
async def register(
    data: UserCreate,
    auth: AuthService = Depends(get_auth_service),
):
    try:
        user = await auth.register_user(data)
        return user

    except UserAlreadyExistsError:
        return user_already_exists()

    except ErrorOnCreatingUser:
        return error_creating_user()
