from sqlalchemy.orm import Session

from src.models.stock_model import StockModel
from src.schemas.stock_schemas import StockCreateSchema


class StockRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: StockCreateSchema) -> StockCreateSchema:
        stock = StockModel(**data.model_dump(exclude_none=True))
        self.session.add(stock)
        self.session.commit()
        self.session.refresh(stock)
        return StockCreateSchema(**stock.__dict__)

    def update(self, stock: StockModel, data: StockCreateSchema) -> StockCreateSchema:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(stock, key, value)
        self.session.commit()
        self.session.refresh(stock)
        return StockCreateSchema(**stock.__dict__)

    def get_by_stock_symbol(self, stock_symbol: str) -> StockModel | None:
        return (
            self.session.query(StockModel)
            .filter_by(company_code=stock_symbol)
            .with_for_update()
            .first()
        )
