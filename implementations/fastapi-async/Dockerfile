FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY app app

RUN pip install uv && uv sync --frozen --no-dev

COPY entrypoint.py .

EXPOSE 5000

CMD ["uv", "run", "python", "entrypoint.py"]
