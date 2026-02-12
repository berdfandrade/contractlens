from fastapi import APIRouter, Request
from app.templates.config import templates

router = APIRouter()


@router.get("/hello")
async def hello(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Home"}
    )


@router.get("/")
async def root():
    return {"message": "ContractLens API is alive"}
