FROM python:3.10-bookworm

WORKDIR /app

RUN apt update \
    && apt install -y --no-install-recommends python3-pip \
    && ln -sf python3 /usr/bin/python \
    && ln -sf pip3 /usr/bin/pip \
    && pip install --upgrade pip uv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml /app
RUN uv pip install --system --no-cache-dir -r pyproject.toml
COPY . /app/

CMD []