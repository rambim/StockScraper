<div align="center"><h1>Stock Scraper 🖥️</h1></div>

### ✒️ Introduction
This project provides 2 endpoints for buying and retrieving stocks.

### ⚙️ Environment Variables

| Variable           | Description                          |
|--------------------|--------------------------------------|
| DATABASE_URI       | URI for the database connection      |
| REDIS_URL          | URL for the Redis instance           |
| POLYGON_API_KEY    | API key for Polygon.io               |
| POLYGON_URL        | Base URL for Polygon.io API          |
| SCRAPPER_URL       | URL for the stock scraper service    |
| REDIS_EXPIRATION   | Expiration time for Redis cache      |
| POSTGRES_USER      | Username for PostgreSQL database     |
| POSTGRES_PASSWORD  | Password for PostgreSQL database     |
| POSTGRES_DB        | Name of the PostgreSQL database      |

### 🔌 Application Installation
Ensure you have Docker Compose installed. To install, download the project, create a `.env` file in the root of the project with the environment variables, and then run the docker command:
```sh
docker-compose build --no-cache
```

### 📀 Start Application
To start the container, run the command:
```sh
docker-compose up -d
```

### 🧪 Run Tests
```sh
docker exec -ti fastapi_web pytest .
```

### ☑️ API Documentation
[API Documentation](http://localhost:8000/docs#/)

### 🛠️ Tools Used
- [Python 3.13](https://www.python.org/);
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Redis](https://redis-py.readthedocs.io/)
- [Requests](https://requests.readthedocs.io/en/master/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Uvicorn](https://www.uvicorn.org/)
- [psycopg2](https://www.psycopg.org/docs/)
- [pydantic-settings](https://docs.pydantic.dev/latest/settings/)
- [Gunicorn](https://docs.gunicorn.org/en/stable/)
- [Pytest](https://docs.pytest.org/en/latest/)
- [pytest-dotenv](https://pypi.org/project/pytest-dotenv/)
- [Ruff](https://beta.ruff.rs/docs/)
- [sqlalchemy-utils](https://sqlalchemy-utils.readthedocs.io/)
- [HTTPX](https://www.python-httpx.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 🧔 Project Owner
- Felippe Giuliani


