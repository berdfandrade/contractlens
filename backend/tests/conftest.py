import pytest
from testcontainers.mongodb import MongoDbContainer
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.jwt import JwtService

from app.core.database import set_database


@pytest.fixture(scope="session")
def mongo_container():
    with MongoDbContainer("mongo:7") as mongo:
        yield mongo


@pytest.fixture(autouse=True)
def setup_jwt():
    JwtService.SECRET_KEY = "test-secret"


@pytest.fixture
async def test_db(mongo_container):
    uri = mongo_container.get_connection_url()

    client = AsyncIOMotorClient(uri)
    db = client.test_db

    set_database(db)

    yield db

    await client.drop_database("test_db")
    client.close()
