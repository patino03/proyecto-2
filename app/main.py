from fastapi import FastAPI
from .routes import router

app = FastAPI(
    title="Football Management System",
    description="API for managing football teams, players, and coaches",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")