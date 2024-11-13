import pytest
from sqlalchemy_utils import create_database, database_exists, drop_database

from src.config.database import Base, engine


@pytest.fixture(scope="module", autouse=True)
def reset_database():
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
