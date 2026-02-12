import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.user import UserCreate
from app.services.hash import HashService
from app.services.user import UserService
from app.core.database import get_database


@pytest.mark.asyncio
async def test_login_success(test_db):

    hash_service = HashService()
    user_service = UserService(hash_service, db=test_db)

    await user_service.create_user(
        UserCreate(
            name="Bernardo",
            email="bernardo@test.com",
            password="123456",
        )
    )

    app.dependency_overrides[get_database] = lambda: test_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:

        response = await client.post(
            "/auth/login",
            json={
                "email": "bernardo@test.com",
                "password": "123456",
            },
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
