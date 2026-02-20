from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/check-health")
async def root():
    return {"message": "ContractLens API is alive"}
