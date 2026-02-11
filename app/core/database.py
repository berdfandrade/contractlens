from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client: AsyncIOMotorClient | None = None


async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(settings.mongo_url)


async def close_mongo_connection():
    global client
    if client:
        client.close()


def get_database():
    if client is None:
        raise RuntimeError("Mongo client is not initialized")
    return client[settings.db_name]
