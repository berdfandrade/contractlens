from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="My FastAPI App",
    description="My FastAPI App",
)

app.include_router(router)


@app.get("/")
async def root():
    return {"message": "ContractLens API is alive"}
