import pytest

from app.services.user import UserService
from app.services.hash import HashService
from app.models.user import UserCreate


@pytest.mark.asyncio
async def test_create_user_success(test_db):
    db = test_db
    user_service = UserService(HashService(), db)

    user = UserCreate(
        name="Bernardo",
        email="bernardo@email.com",
        password="#SecurePassword123",
    )

    created_user = await user_service.create_user(user)

    assert created_user["id"] is not None
    assert created_user["email"] == user.email
    assert "password" not in created_user


@pytest.mark.asyncio
async def test_create_user_duplicate_raises(test_db):
    db = test_db
    user_service = UserService(HashService(), db)

    user = UserCreate(
        name="Ana",
        email="ana@email.com",
        password="#AnotherPassword123",
    )

    # Cria a primeira vez
    await user_service.create_user(user)

    # Segunda criação deve falhar
    with pytest.raises(ValueError) as exc_info:
        await user_service.create_user(user)
    assert "User already exists" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_user_by_id_success(test_db):
    db = test_db
    user_service = UserService(HashService(), db)

    user = UserCreate(
        name="Carlos",
        email="carlos@email.com",
        password="#Password123",
    )
    created_user = await user_service.create_user(user)

    fetched_user = await user_service.get_user(created_user["id"])

    if not fetched_user:
        raise ValueError("User not found")

    assert fetched_user["id"] == created_user["id"]
    assert fetched_user["email"] == created_user["email"]
    assert "password" not in fetched_user


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(test_db):
    db = test_db
    user_service = UserService(HashService(), db)

    fetched_user = await user_service.get_user(
        "000000000000000000000000"
    )  # ID inválido
    assert fetched_user is None


@pytest.mark.asyncio
async def test_get_user_by_email_success(test_db):
    db = test_db
    user_service = UserService(HashService(), db)

    user = UserCreate(
        name="Diana",
        email="diana@email.com",
        password="#SecretPassword123",
    )
    created_user = await user_service.create_user(user)

    fetched_user = await user_service.get_user_by_email(user.email)

    if not fetched_user:
        raise ValueError("User not found")

    assert fetched_user["id"] == created_user["id"]
    assert fetched_user["email"] == created_user["email"]
    assert "password" not in fetched_user


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(test_db):
    db = test_db
    user_service = UserService(HashService(), db)

    fetched_user = await user_service.get_user_by_email("notfound@email.com")
    assert fetched_user is None
