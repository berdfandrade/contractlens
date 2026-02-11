import pytest
from jose import jwt

from app.services.jwt import JwtService


@pytest.mark.asyncio
async def test_create_access_token_success():

    JwtService.SECRET_KEY = "test-secret"
    data = {"sub": "123"}
    token = JwtService.create_access_token(data)

    assert token is not None

    decoded = jwt.decode(
        token, JwtService.SECRET_KEY, algorithms=[JwtService.ALGORITHM]
    )

    assert decoded["sub"] == "123"
    assert "exp" in decoded


def test_create_access_token_without_secret():

    JwtService.SECRET_KEY = None

    with pytest.raises(ValueError):
        JwtService.create_access_token({"sub": "123"})
