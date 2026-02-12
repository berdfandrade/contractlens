from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import connect_to_mongo, close_mongo_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await connect_to_mongo()
    yield
    # shutdown
    await close_mongo_connection()
