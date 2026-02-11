import pytest

from app.core.database import connect_to_mongo, get_database
from app.services.user import UserService
from app.services.hash import HashService
from app.models.user import UserCreate


@pytest.mark.asyncio
async def test_create_user(test_db):
    db = test_db
    hash_service = HashService()
    user_service = UserService(db, hash_service)

    user = UserCreate(
        name="Bernardo",
        email="bernardo@email.com",
        password="#SecurePassword123",
    )

    created_user = await user_service.create_user(user)

    assert created_user["id"] is not None
    assert created_user["email"] == user.email
    assert "password" not in created_user
