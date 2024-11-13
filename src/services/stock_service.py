from datetime import datetime

from fastapi import HTTPException
from fastapi.logger import logger
from redis import Redis
from requests.exceptions import HTTPError
from sqlalchemy.orm import Session

from src.config.settings import get_settings
from src.repository.stock_repository import StockRepository
from src.schemas.stock_schemas import (
    Competitor,
    PerformanceData,
    PolygonResponse,
    StockCreateSchema,
    StockPurchasedRequestSchema,
    StockPurchasedResponseSchema,
    StockResponseSchema,
    StockValues,
)
from src.services.polygon_api import PolygonAPI
from src.services.scraper import StockScraper

settings = get_settings()


class StockService:
    def __init__(
        self,
        session: Session,
    ):
        self.repository = StockRepository(session)
        self.redis_client = Redis.from_url(settings.REDIS_URL)

    def purchase_by_stock_symbol(
        self, stock_symbol: str, data: StockPurchasedRequestSchema
    ) -> StockPurchasedResponseSchema:
        stock_symbol = stock_symbol.upper()

        existing_stock = self.repository.get_by_stock_symbol(stock_symbol)
        try:
            if existing_stock:
                stock_update_data = StockCreateSchema(
                    purchased_amount=existing_stock.purchased_amount + data.amount,
                    company_code=existing_stock.company_code,
                )
                self.repository.update(existing_stock, stock_update_data)
            else:
                stock_create_data = StockCreateSchema(
                    purchased_amount=data.amount,
                    company_code=stock_symbol,
                )
                self.repository.create(stock_create_data)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"{e}")

        message = f"{data.amount} units of stock {stock_symbol} were added to your stock record"
        response = StockPurchasedResponseSchema(message=message)

        self.redis_client.delete(stock_symbol)
        return response

    def get_by_stock_symbol(self, stock_symbol: str) -> StockResponseSchema:
        stock_symbol = stock_symbol.upper()

        cached_data = self.redis_client.get(f"{stock_symbol}")
        if cached_data:
            return StockResponseSchema.model_validate_json(cached_data)

        company_name, competitors, performance = self._get_scraper_data(stock_symbol)
        polygon_response = self._get_polygon_data(stock_symbol)

        stocks = self.repository.get_by_stock_symbol(stock_symbol)

        response = StockResponseSchema(
            status=polygon_response.status,
            purchased_amount=stocks.purchased_amount if stocks else 0,
            company_code=stock_symbol,
            company_name=company_name,
            stock_values=polygon_response.stock_values,
            performance_data=performance,
            competitors=competitors,
        )

        self.redis_client.set(
            stock_symbol, response.model_dump_json(), ex=settings.REDIS_EXPIRATION
        )
        return response

    def _get_scraper_data(
        self, stock_symbol: str
    ) -> tuple[str, list[Competitor], PerformanceData]:
        company_name = ""
        competitors: list[Competitor] = []
        performance = PerformanceData()
        try:
            scraper = StockScraper(stock_symbol)
        except ConnectionError as e:
            logger.error(f"Failed to connect to the external data source: {e}")
            return company_name, competitors, performance

        try:
            company_name = scraper.get_company_name()
        except AttributeError as e:
            logger.error(f"Company name can't be scraped for {stock_symbol}: {e}")

        try:
            competitors = scraper.get_competitors()
        except AttributeError as e:
            logger.error(f"Competitors data can't be scraped for {stock_symbol}: {e}")

        try:
            performance = scraper.get_performance()
        except AttributeError as e:
            logger.error(f"Performance data can't be scraped for {stock_symbol}: {e}")

        return company_name, competitors, performance

    def _get_polygon_data(self, stock_symbol: str) -> PolygonResponse:
        try:
            polygon_api = PolygonAPI()
            polygon_response = polygon_api.get_stock_values(
                stock_symbol, datetime.now().strftime("%Y-%m-%d")
            )
        except HTTPError as e:
            polygon_response = PolygonResponse(
                status="error",
                stock_values=StockValues(),
            )
            logger.error(f"Failed to fetch stock values from Polygon.io: {e}")

        return polygon_response
