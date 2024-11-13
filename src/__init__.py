from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src.router.api import router as api_router
from src.utils.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="Stocks API",
    description="API to manage stocks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(api_router)
