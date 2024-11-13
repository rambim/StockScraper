from fastapi import FastAPI

from src.router.api import router as api_router
from src.utils.init_db import create_tables

app = FastAPI(
    title="Your API Title",
    description="Your API Description",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.on_event("startup")
def on_startup() -> None:
    """
    Initializes the database tables when the application starts up.
    """
    create_tables()


app.include_router(api_router)
