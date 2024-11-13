from sqlalchemy import inspect

from src.config.database import engine
from src.models.stock_model import StockModel


def create_tables():
    inspector = inspect(engine)
    if not inspector.has_table('stock_model'):
        StockModel.metadata.create_all(bind=engine)
