FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev 

COPY requirements.txt requirements-dev.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements-dev.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000" ,"src:app" ]
