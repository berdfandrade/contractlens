import pytest
from jose import jwt

from app.services.jwt import JwtService


@pytest.fixture(autouse=True)
def jwt_secret():
    JwtService.SECRET_KEY = "test-secret"
    yield
    JwtService.SECRET_KEY = None


def test_create_access_token_success():
    data = {"sub": "123", "type": "access"}

    token = JwtService.create_access_token(data)

    assert token is not None

    decoded = jwt.decode(
        token,
        JwtService.SECRET_KEY,  # type: ignore
        algorithms=[JwtService.ALGORITHM],
    )

    assert decoded["sub"] == "123"
    assert decoded["type"] == "access"
    assert "exp" in decoded


def test_create_refresh_token_success():
    data = {"sub": "123", "type": "refresh"}

    token = JwtService.create_refresh_token(data)

    assert token is not None

    decoded = jwt.decode(
        token,
        JwtService.SECRET_KEY,  # type: ignore
        algorithms=[JwtService.ALGORITHM],
    )

    assert decoded["sub"] == "123"
    assert decoded["type"] == "refresh"
    assert "exp" in decoded


def test_decode_token_success():
    token = JwtService.create_access_token({"sub": "123", "type": "access"})

    payload = JwtService.decode_token(token)

    assert payload["sub"] == "123"
    assert payload["type"] == "access"


def test_create_access_token_without_secret():
    JwtService.SECRET_KEY = None

    with pytest.raises(ValueError):
        JwtService.create_access_token({"sub": "123"})
