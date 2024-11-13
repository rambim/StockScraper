import logging
from datetime import datetime, timedelta

import requests

from src.config.settings import get_settings
from src.schemas.stock_schemas import PolygonResponse, StockValues

logger = logging.getLogger(__name__)

settings = get_settings()


class PolygonAPI:
    def __init__(self):
        self.BASE_URL = settings.POLYGON_URL
        self.headers = {"Authorization": f"Bearer {settings.POLYGON_API_KEY}"}

    def get_stock_values(self, stock_symbol: str, date: str) -> PolygonResponse:
        previous_business_day_str = self.get_previous_business_day(date)
        url = f"{self.BASE_URL}/open-close/{stock_symbol}/{previous_business_day_str}"

        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        response_json = response.json()

        return PolygonResponse(
            status=response_json["status"],
            stock_values=StockValues(**response_json),
        )

    def get_previous_business_day(self, date: str) -> str:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        previous_business_day = date_obj - timedelta(days=1)

        while previous_business_day.weekday() > 4:
            previous_business_day -= timedelta(days=1)

        return previous_business_day.strftime("%Y-%m-%d")
