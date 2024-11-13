from pydantic import BaseModel, field_validator, validator


class StockValues(BaseModel):
    open: float = 0
    high: float = 0
    low: float = 0
    close: float = 0


class PolygonResponse(BaseModel):
    status: str
    stock_values: StockValues


class PerformanceData(BaseModel):
    five_days: float = 0
    one_month: float = 0
    three_months: float = 0
    year_to_date: float = 0
    one_year: float = 0

    @field_validator("*", mode="before")
    @classmethod
    def check_performance_data(cls, value):
        if isinstance(value, str):
            return float(value.replace("%", ""))
        return value


class MarketCap(BaseModel):
    currency: str
    value: float


class Competitor(BaseModel):
    name: str
    market_cap: MarketCap


class StockCreateSchema(BaseModel):
    company_code: str
    purchased_amount: int

    @field_validator("company_code", mode="before")
    def check_company_code_length(cls, value):
        if len(value) > 10:
            raise ValueError("company_code must be 10 characters or less")
        return value


class StockResponseSchema(BaseModel):
    status: str
    purchased_amount: int
    company_code: str
    company_name: str
    stock_values: StockValues
    performance_data: PerformanceData
    competitors: list[Competitor]


class StockPurchasedRequestSchema(BaseModel):
    amount: int

    @field_validator("amount", mode="before")
    def check_purchased_amount(cls, value):
        if value <= 0:
            raise ValueError("amount must be greater than zero")
        return value


class StockPurchasedResponseSchema(BaseModel):
    message: str
