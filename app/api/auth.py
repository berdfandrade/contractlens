from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service, get_token_service
from app.services.auth import AuthService
from app.services.token import TokenService
from app.models.login import LoginSchema

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(
    data: LoginSchema,
    auth: AuthService = Depends(get_auth_service),
    token: TokenService = Depends(get_token_service),
):
    user = await auth.authenticate_user(data.email, data.password)
    if not user:
        return ""

    session = await token.create_session(user["id"])
    return session
