from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/check-health", tags=["👨‍⚕️ Health Check"])
async def check_health():
    return {"message": "ContractLens API is alive"}
