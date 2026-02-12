from fastapi import APIRouter

from .routes.auth import router as auth_router
from .routes.hello import router as hello_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(hello_router)
