
# Этап 1. Установка зависимостей
FROM python:3.12-slim AS builder

WORKDIR /build

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Этап 2. Запуск приложения
FROM python:3.12-slim

WORKDIR /code

COPY --from=builder /opt/venv /opt/venv

COPY app ./app

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
