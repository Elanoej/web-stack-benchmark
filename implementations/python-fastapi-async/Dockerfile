FROM python:3.12-slim AS builder

RUN pip install uv

WORKDIR /app
COPY pyproject.toml uv.lock ./

RUN UV_SYSTEM_PYTHON=1 uv sync --frozen --no-dev --no-cache && \
    rm -rf /root/.cache


FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY app app
COPY entrypoint.py .

CMD ["python", "entrypoint.py"]
