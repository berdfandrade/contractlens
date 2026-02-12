from fastapi import FastAPI
from app.api.routes import router
from app.api.auth import router as auth_router
from app.api.routes import router as hello_router

app = FastAPI(
    title="My FastAPI App",
    description="My FastAPI App",
)

app.include_router(auth_router)
app.include_router(hello_router)


@app.get("/")
async def root():
    return {"message": "ContractLens API is alive"}
