FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip uv

WORKDIR /app

COPY pyproject.toml /app
RUN uv pip install --system --no-cache-dir -r pyproject.toml

COPY . /app
CMD ["python", "app/app.py"]