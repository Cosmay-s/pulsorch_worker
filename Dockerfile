FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей
COPY pyproject.toml uv.lock /app/
RUN pip install uv==0.7.2 \
 && uv export -o requirements.txt --no-header --no-hashes \
 && pip install -r requirements.txt --no-cache-dir -U \
 && pip uninstall -y uv

COPY antworker /app/antworker

CMD ["python", "-m", "antworker.scheduler"]