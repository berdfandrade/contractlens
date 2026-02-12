from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def hello():
    return {"message": "Hello World from /api"}


@router.get("/")
async def root():
    return {"message": "ContractLens API is alive"}
