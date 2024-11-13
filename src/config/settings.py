from pydantic_settings import BaseSettings

__SETTINGS = None


class Settings(BaseSettings):
    DATABASE_URI: str
    REDIS_URL: str
    POLYGON_API_KEY: str
    POLYGON_URL: str = "https://api.polygon.io"
    SCRAPPER_URL: str = "https://www.marketwatch.com"
    REDIS_EXPIRATION: int = 3600

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


def get_settings():
    global __SETTINGS
    if __SETTINGS is None:
        __SETTINGS = Settings()
    return __SETTINGS
