from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas.stock_schemas import (
    StockPurchasedRequestSchema,
    StockPurchasedResponseSchema,
    StockResponseSchema,
)
from src.services.stock_service import StockService

router = APIRouter(prefix="/stock", tags=["stock"])


@router.post(
    "/{stock_symbol}", status_code=201, response_model=StockPurchasedResponseSchema
)
def purchase_stock(
    stock_symbol: str,
    data: StockPurchasedRequestSchema,
    session: Session = Depends(get_db),
) -> StockPurchasedResponseSchema:
    service = StockService(session)
    return service.purchase_by_stock_symbol(stock_symbol, data)


@router.get("/{stock_symbol}", status_code=200, response_model=StockResponseSchema)
def get_stocks(
    stock_symbol: str, session: Session = Depends(get_db)
) -> StockResponseSchema:
    service = StockService(session)
    return service.get_by_stock_symbol(stock_symbol)
