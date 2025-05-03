FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY antworker/ ./antworker/
COPY pyproject.toml uv.lock ./

RUN pip install uv && uv pip install . --system --no-cache-dir

CMD ["python", "-m", "antworker.scheduler"]