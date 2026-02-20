from fastapi import APIRouter

from .routes.auth import router as web_auth_router

web_router = APIRouter()

web_router.include_router(web_auth_router)
