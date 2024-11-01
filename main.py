from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Football Management API",
    description="API for managing football team data",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Welcome to Football Management API"}