import pytest

from app.services.auth import AuthService
from app.services.user import UserService
from app.services.hash import HashService
from app.services.jwt import JwtService
from app.models.user import UserCreate
from app.services.errors.auth import EmailNotRegistered


@pytest.mark.asyncio
async def test_authenticate_user_success(test_db):
    hash_service = HashService()
    jwt_service = JwtService()
    user_service = UserService(hash_service, db=test_db)

    auth_service = AuthService(
        user_service=user_service,
        hash_service=hash_service,
        jwt_service=jwt_service,
    )

    password = "123456"

    await user_service.create_user(
        UserCreate(
            name="Bernardo",
            email="bernardo@test.com",
            password=password,
        )
    )

    user = await auth_service.authenticate_user(
        "bernardo@test.com",
        password,
    )
    assert user is not None
    assert user["email"] == "bernardo@test.com"


@pytest.mark.asyncio
async def test_authenticate_user_not_found(test_db):
    hash_service = HashService()
    jwt_service = JwtService()
    user_service = UserService(hash_service, db=test_db)

    auth_service = AuthService(
        user_service=user_service,
        hash_service=hash_service,
        jwt_service=jwt_service,
    )

    with pytest.raises(EmailNotRegistered):
        await auth_service.authenticate_user(
            "naoexiste@test.com",
            "123456",
        )


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(test_db):
    hash_service = HashService()
    jwt_service = JwtService()
    user_service = UserService(hash_service, db=test_db)

    auth_service = AuthService(
        user_service=user_service,
        hash_service=hash_service,
        jwt_service=jwt_service,
    )

    await user_service.create_user(
        UserCreate(
            name="Ana",
            email="ana@test.com",
            password="correct",
        )
    )

    user = await auth_service.authenticate_user(
        "ana@test.com",
        "wrong",
    )

    assert user is None
