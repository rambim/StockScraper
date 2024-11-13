import logging
import re

import requests
from bs4 import BeautifulSoup

from src.config.settings import get_settings
from src.schemas.stock_schemas import Competitor, MarketCap, PerformanceData

settings = get_settings()

logger = logging.getLogger(__name__)


class StockScraper:
    def __init__(self, stock_symbol: str):
        self.url = settings.SCRAPPER_URL
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
            "Connection": "keep-alive",
            "Host": "www.marketwatch.com",
            "Priority": "u=0, i",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "TE": "trailers",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        }
        self.soup = None
        self._fetch_data(stock_symbol)

    def _fetch_data(self, stock_symbol: str):
        response = requests.get(
            f"{self.url}/investing/stock/{stock_symbol}", headers=self.headers
        )

        response.raise_for_status()
        self.soup = BeautifulSoup(response.content, "html.parser")

    def get_company_name(self) -> str:
        return self.soup.find("h1", {"class": "company__name"}).get_text(strip=True)

    def get_competitors(self) -> list[Competitor]:
        competitors_table = self.soup.find(
            "table", {"aria-label": "Competitors data table"}
        )
        competitors = []
        for row in competitors_table.find("tbody").find_all("tr"):
            name = row.find("td", {"class": "w50"}).get_text(strip=True)
            market_cap = row.find("td", {"class": "number"}).get_text(strip=True)
            competitors.append({"name": name, "market_cap": market_cap})

        response = []
        for comp in competitors:
            currency, value = self.parse_currency(comp["market_cap"])
            response.append(
                Competitor(
                    name=comp["name"],
                    market_cap=MarketCap(
                        currency=currency,
                        value=value,
                    ),
                )
            )
        return response

    def get_performance(self):
        performance_table = self.soup.find(
            "table", {"class": "table table--primary no-heading c2"}
        )
        performance = {}
        for row in performance_table.find("tbody").find_all("tr"):
            period = row.find("td", {"class": "table__cell"}).get_text(strip=True)
            value = row.find(
                "li", {"class": "content__item value ignore-color"}
            ).get_text(strip=True)
            performance[period] = value

        return PerformanceData(
            five_days=performance["5 Day"],
            one_month=performance["1 Month"],
            three_months=performance["3 Month"],
            year_to_date=performance["YTD"],
            one_year=performance["1 Year"],
        )

    def parse_currency(self, value_str: str) -> tuple[str, float]:
        match = re.match(r"([^\d]+)?", value_str)
        if not match:
            return "", 0.0

        currency = match.group(1) or ""
        value = (
            value_str[match.end() :]
            .replace("T", "e12")
            .replace("B", "e9")
            .replace("M", "e6")
        )
        return currency, float(value)
