from fastapi import FastAPI, Request
from app.api import api_router
from app.web import web_router
from app.core.database import connect_to_mongo, close_mongo_connection
from contextlib import asynccontextmanager
from app.core.exception_handlers import register_exception_handlers
from app.core.mounts import mount_static
from app.templates.config import templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="Contract lens", description="Api Contract Lens 1.0", lifespan=lifespan
)

register_exception_handlers(app)

mount_static(app)

app.include_router(api_router)
app.include_router(web_router)
