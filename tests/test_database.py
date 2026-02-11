import pytest
from app.core.database import connect_to_mongo, close_mongo_connection, get_database


@pytest.mark.asyncio
async def test_mongo_connection():
    await connect_to_mongo()

    db = get_database()

    result = await db.command("ping")

    assert result["ok"] == 1.0

    await close_mongo_connection()
