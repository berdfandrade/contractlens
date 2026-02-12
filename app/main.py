from fastapi import FastAPI
from app.api import router
from app.core.database import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="Contract lens", description="Api Contract Lens 1.0", lifespan=lifespan
)


app.include_router(router)
