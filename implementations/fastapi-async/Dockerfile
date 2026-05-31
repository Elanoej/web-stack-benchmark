FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY app app

RUN pip install uv && uv sync --frozen --no-dev

EXPOSE 8080

ENV WORKERS=${WORKERS:-6}

CMD uv run uvicorn app.main:app --host 0.0.0.0 --port 8080 --workers $WORKERS
