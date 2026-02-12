import pytest
from time import sleep
from app.services.token import TokenService


# Mocks simples para jwt_service e refresh_repo
class MockJWT:
    def create_access_token(self, data):
        return "access_token_mock"

    def create_refresh_token(self, data):
        return "refresh_token_mock"

    def decode_token(self, token):
        return {"sub": "user123"}


class MockRepo:
    async def save_token(self, **kwargs):
        pass

    async def get_token(self, token):
        return True

    async def rotate_token(self, old_token, new_token):
        pass

    async def delete_token(self, token):
        pass


@pytest.fixture
def token_service():
    return TokenService(MockJWT(), MockRepo(), secret_key="test-reset-secret")


def test_create_reset_token_success(token_service):
    token = token_service.create_reset_token("user123", expires_minutes=1)
    assert token is not None
    user_id = token_service.verify_reset_token(token)
    assert user_id == "user123"


def test_verify_reset_token_expired(token_service):
    # cria token com expiração curtíssima
    token = token_service.create_reset_token("user123", expires_minutes=0.01)
    assert token is not None

    # espera expirar
    sleep(1)

    user_id = token_service.verify_reset_token(token)
    assert user_id is None


def test_verify_reset_token_invalid(token_service):
    invalid_token = "token-invalido"
    user_id = token_service.verify_reset_token(invalid_token)
    assert user_id is None
