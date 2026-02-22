import pytest

from app.services.token import TokenService
from app.services.jwt import JwtService
from app.services.errors.auth import InvalidRefreshToken
from app.repositories.refresh_token import RefreshTokenRepository


@pytest.mark.asyncio
async def test_create_session_success(test_db):
    db = test_db

    JwtService.SECRET_KEY = "test-secret"

    refresh_repo = RefreshTokenRepository(db)
    token_service = TokenService(
        jwt_service=JwtService,
        refresh_repo=refresh_repo,
        secret_key="test-secret",
    )

    session = await token_service.create_session("user123")

    assert session["access_token"] is not None
    assert session["refresh_token"] is not None

    # Confirma que salvou no Mongo
    stored = await db.refresh_tokens.find_one({"token": session["refresh_token"]})
    assert stored is not None


@pytest.mark.asyncio
async def test_refresh_session_success(test_db):
    db = test_db

    JwtService.SECRET_KEY = "test-secret"

    refresh_repo = RefreshTokenRepository(db)
    token_service = TokenService(
        jwt_service=JwtService,
        refresh_repo=refresh_repo,
        secret_key="test-secret",
    )

    session = await token_service.create_session("user123")

    refreshed = await token_service.refresh_session(session["refresh_token"])

    assert refreshed["refresh_token"] != session["refresh_token"]

    # Token antigo não deve mais existir
    old = await db.refresh_tokens.find_one({"token": session["refresh_token"]})
    assert old is None

    # Token novo deve existir
    new = await db.refresh_tokens.find_one({"token": refreshed["refresh_token"]})
    assert new is not None


@pytest.mark.asyncio
async def test_revoke_session_success(test_db):
    db = test_db

    JwtService.SECRET_KEY = "test-secret"

    refresh_repo = RefreshTokenRepository(db)
    token_service = TokenService(
        jwt_service=JwtService,
        refresh_repo=refresh_repo,
        secret_key="test-secret",
    )

    session = await token_service.create_session("user123")

    await token_service.revoke_session(session["refresh_token"])

    stored = await db.refresh_tokens.find_one({"token": session["refresh_token"]})

    assert stored is None


def test_create_reset_token_success(test_db):
    JwtService.SECRET_KEY = "test-secret"

    token_service = TokenService(
        jwt_service=JwtService,
        refresh_repo=None,  # não precisa aqui
        secret_key="test-secret",
    )

    token = token_service.create_reset_token("user123")

    user_id = token_service.verify_reset_token(token)

    assert user_id == "user123"
