import pytest
from app.services.user_service import UserService
from app.models.user import UserCreate
from app.core.database import connect_to_mongo, close_mongo_connection, get_database


@pytest.mark.asyncio
async def test_create_user():

    await connect_to_mongo()

    user = UserCreate(
        name="Bernardo",
        email="bernardo@email.com",
        password="#SecurePassword123",
    )

    created_user = await UserService.create_user(user)

    assert created_user["id"] is not None
    assert created_user["email"] == "bernardo@email.com"

    db = get_database()
    await db.users.delete_many({})

    await close_mongo_connection()
