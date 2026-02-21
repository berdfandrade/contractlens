from fastapi import APIRouter

from .routes.auth import router as api_auth_router
from .routes.health import router as api_health_router

api_router = APIRouter(prefix="/api")

api_router.include_router(api_auth_router)
api_router.include_router(api_health_router)
