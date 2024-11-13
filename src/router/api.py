from fastapi import APIRouter

from src.router.v1 import stock

router = APIRouter(prefix="/api/v1")

router.include_router(stock.router)
