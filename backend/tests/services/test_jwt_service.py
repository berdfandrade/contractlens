import pytest
from jose import jwt, JWTError

from app.services.jwt import JwtService


@pytest.fixture(autouse=True)
def jwt_secret():
    JwtService.SECRET_KEY = "test-secret"
    yield
    JwtService.SECRET_KEY = "test-secret"


def test_create_access_token_success():
    token = JwtService.create_access_token("123")

    assert token is not None

    decoded = jwt.decode(
        token,
        JwtService.SECRET_KEY,
        algorithms=[JwtService.ALGORITHM],
    )

    assert decoded["sub"] == "123"
    assert "exp" in decoded
    assert "iat" in decoded


def test_create_refresh_token_success():
    token = JwtService.create_refresh_token("123")

    assert token is not None

    decoded = jwt.decode(
        token,
        JwtService.SECRET_KEY,
        algorithms=[JwtService.ALGORITHM],
    )

    assert decoded["sub"] == "123"
    assert "exp" in decoded
    assert "iat" in decoded
    assert "jti" in decoded
    assert isinstance(decoded["jti"], str)


def test_refresh_token_is_unique():
    token1 = JwtService.create_refresh_token("123")
    token2 = JwtService.create_refresh_token("123")

    assert token1 != token2


def test_decode_token_success():
    token = JwtService.create_access_token("123")

    payload = JwtService.decode_token(token)

    assert payload["sub"] == "123"
    assert "exp" in payload
    assert "iat" in payload


def test_decode_invalid_token():
    with pytest.raises(JWTError):
        JwtService.decode_token("invalid.token.here")


def test_create_access_token_without_secret():
    JwtService.SECRET_KEY = None  # type: ignore

    with pytest.raises(Exception):
        JwtService.create_access_token("123")
