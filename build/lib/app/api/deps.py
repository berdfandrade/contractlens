from app.services.hash import HashService
from app.services.jwt import JwtService
from app.repositories.refresh_token import RefreshTokenRepository
from app.services.user import UserService
from app.services.token import TokenService
from app.services.auth import AuthService
from fastapi import Depends
from app.core.database import get_database


def get_hash_service():
    return HashService()


def get_jwt_service():
    return JwtService()


def get_refresh_repo(db=Depends(get_database)):
    return RefreshTokenRepository(db)


def get_user_service(
    hash_service=Depends(get_hash_service),
    db=Depends(get_database),
):
    return UserService(hash_service, db)


def get_token_service(
    jwt=Depends(get_jwt_service),
    repo=Depends(get_refresh_repo),
):
    return TokenService(jwt, repo)


def get_auth_service(
    user_service=Depends(get_user_service),
    hash_service=Depends(get_hash_service),
    jwt_service=Depends(get_jwt_service),
):
    return AuthService(user_service, hash_service, jwt_service)
