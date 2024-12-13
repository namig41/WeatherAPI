FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFEERED 1

WORKDIR /app

RUN apt-get update && \
    apt install -y python3-dev \
    gcc \
    musl-dev

# Копирование файлов
ADD pyproject.toml /app/

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

# Копирование остального кода
COPY /app/* /app/