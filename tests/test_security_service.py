import pytest
from jose import jwt

from app.services.security import SecurityService


@pytest.mark.asyncio
async def test_create_access_token_success():

    # define secret fake
    SecurityService.SECRET_KEY = "test-secret"

    data = {"sub": "123"}

    token = SecurityService.create_access_token(data)

    assert token is not None

    decoded = jwt.decode(
        token, SecurityService.SECRET_KEY, algorithms=[SecurityService.ALGORITHM]
    )

    assert decoded["sub"] == "123"
    assert "exp" in decoded


def test_create_access_token_without_secret():

    SecurityService.SECRET_KEY = None

    with pytest.raises(ValueError):
        SecurityService.create_access_token({"sub": "123"})
