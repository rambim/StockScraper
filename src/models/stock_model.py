from sqlalchemy import CheckConstraint, Column, Index, Integer, String

from src.config.database import Base


class StockModel(Base):
    __tablename__ = "stocks"

    company_code = Column(String(10), nullable=False, primary_key=True)
    purchased_amount = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "purchased_amount >= 0", name="check_purchased_amount_non_negative"
        ),
    )
