# Этап сборки (обратите внимание на одинаковый регистр 'FROM' и 'as')
FROM python:3.9-slim AS builder

# Установка системных зависимостей с очисткой кеша
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование только requirements.txt для лучшего кэширования
COPY requirements.txt .

# Установка зависимостей с явным указанием пути
RUN pip install --prefix=/install -r requirements.txt

# Этап выполнения
FROM python:3.9-slim

# Установка только необходимых runtime-зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Создание пользователя для безопасности
RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# Копирование установленных зависимостей из builder
COPY --from=builder /install /usr/local
# Копирование кода приложения
COPY --chown=appuser . .

# Переключение на непривилегированного пользователя
USER appuser

# Настройка переменных окружения
ENV PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}" \
    PYTHONPATH=/app

# Порт приложения
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]