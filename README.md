# Проект Погода

`WeatherAPI` — это проект, предоставляющий простой и удобный REST API для работы с погодными данными, локациями и пользователями. Приложение позволяет добавлять, редактировать и просматривать информацию о локациях и пользователях, а также предоставляет базовые возможности авторизации.

### Для запуска приложения

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/namig41/WeatherAPI.git
   cd WeatherAPI
   ```

2. Реализованные команды для сборки проекта

- `make all` — запустить приложение
- `make app` — запустить микросервисы авторизации и погоды
- `make app-logs` — отслеживать логи в контейнере приложения
- `make app-down` — остановить приложение
- `make shell` — открыть интерактивную оболочку (bash) внутри контейнера

## REST API

### API для работы с локациями

#### GET `/locations`

Получение всех локаций. Пример ответа:

```json
{
  "locations": [
    {
      "name": "East Patricia",
      "latitude": "84.8735595",
      "longitude": "84.8735595"
    },
    {
      "name": "Wendyville",
      "latitude": "27.0962525",
      "longitude": "27.0962525"
    },
    {
      "name": "East Danielhaven",
      "latitude": "-78.0894145",
      "longitude": "-78.0894145"
    },
    {
      "name": "Moscow",
      "latitude": "55.751244",
      "longitude": "55.751244"
    }
  ]
}
```

#### GET `/locations/{name}`

Получение локации по имени. Пример ответа:

```json
{
  "name": "Moscow",
  "latitude": "55.751244",
  "longitude": "55.751244"
}
```

HTTP-коды ответов:

- **200** — успешно
- **400** — код партии отсутствует в адресе
- **404** — локация не найдена

#### POST `/locations`

Добавление новой локации в базу. Данные передаются в теле запроса в виде JSON с полями `name`, `latitude` и `longitude`. Пример ответа:

```json
{
  "name": "Moscow",
  "latitude": "55.751244",
  "longitude": "55.751244"
}
```

HTTP-коды ответов:

- **200** — успешно
- **500** — ошибка (например, база данных недоступна)

### API для работы с пользователями

#### GET `/users`

Получение всех пользователей. Пример ответа:

```json
{
  "users": [
    {
      "login": "hardyluke",
      "email": "parrishjennifer@example.net",
      "password": "$5$rounds=535000$nuk5W9ZlYdbam0Cf$Ed2/LmObPb2mXxFNcf.7Gq/u1mxvLA/vnCE/WmFtpL3"
    },
    {
      "login": "Philip Hunt",
      "email": "ibrady@example.net",
      "password": "n+gs)QM$_6"
    },
    {
      "login": "burgessdaniel",
      "email": "kevinhobbs@example.org",
      "password": "$5$rounds=535000$MDAQW.L05j2wUDP4$xHHtw0PlZpRKz0rI6F/h/wrvbyso1GX1Vj4KBthoRL/"
    }
  ]
}
```

#### GET `/users/{login}`

Получение пользователя по логину. Пример ответа:

```json
{
    "login": "hardyluke",
    "email": "parrishjennifer@example.net",
    "password": "$5$rounds=535000$nuk5W9ZlYdbam0Cf$Ed2/LmObPb2mXxFNcf.7Gq/u1mxvLA/vnCE/WmFtpL3"
}
```

#### POST `/users`

Добавление нового пользователя в систему. Данные передаются в теле запроса в виде JSON с полями `login`, `email` и `password`. Пример ответа:

```json
{
    "login": "hardyluke",
    "email": "parrishjennifer@example.net",
    "password": "$5$rounds=535000$nuk5W9ZlYdbam0Cf$Ed2/LmObPb2mXxFNcf.7Gq/u1mxvLA/vnCE/WmFtpL3"
}
```

### **`GET /auth/login`**  
Вход пользователя с помощью логина и пароля. В ответе содержится `access_token` в куки.  

#### **HTTP-коды ответов:**  
- **200** — Успешный вход.  
- **400** — Неверный формат запроса (например, отсутствуют обязательные параметры `username` или `password`).  
- **401** — Неверный логин или пароль.  
- **403** — Аккаунт заблокирован или доступ запрещён.  
- **500** — Ошибка сервера при обработке запроса.  

---

### **`POST /auth/logout`**  
Выход пользователя.  

#### **HTTP-коды ответов:**  
- **200** — Успешный выход.  
- **401** — Пользователь не авторизован или токен истёк.  
- **500** — Ошибка сервера при обработке запроса.  

## **Зависимости**  
### **Основные зависимости**  
- **Python**: ^3.10 — Основной язык программирования.  
- **FastAPI**: ^0.115.6 — Асинхронный веб-фреймворк.  
- **SQLAlchemy**: ^2.0.36 (с asyncio) — ORM для работы с базами данных.  
- **Alembic**: ^1.11.2 — Инструмент для миграции схем базы данных.  
- **punq**: ^0.7.0 — Библиотека для внедрения зависимостей.  
- **pydantic-settings**: ^2.6.1 — Упрощённое управление настройками с проверкой типов.  
- **pytest**: ^8.3.4 — Фреймворк для тестирования.  

### **Аутентификация и безопасность**  
- **jose**: ^1.0.0 — Библиотека для работы с JSON Web Token (JWT).  
- **python-jose**: ^3.3.0 — Поддержка JWT и JWE для безопасности.  
- **passlib**: ^1.7.4 — Библиотека для хэширования паролей.  
- **pyjwt**: ^2.10.1 — Работа с токенами JWT.  

### **Базы данных**  
- **psycopg2**: ^2.9.10 — Адаптер для PostgreSQL.  
- **asyncpg**: ^0.30.0 — Асинхронный драйвер для PostgreSQL.  

### **Очереди задач и фоновые процессы**  
- **celery**: ^5.4.0 (с Redis) — Очередь задач для выполнения фоновых процессов.  
- **aioredis**: ^2.0.1 — Асинхронный клиент для Redis.  
- **qredis**: ^1.1.0 — Лёгкий инструмент для работы с очередями в Redis.  

### **Сети и API**  
- **httpx**: ^0.28.1 — Асинхронный HTTP-клиент для работы с внешними API.  
- **aiogram**: ^3.16.0 — Фреймворк для разработки Telegram-ботов.  
- **python-multipart**: ^0.0.20 — Для обработки загрузки файлов в FastAPI.  
- **aiosmtplib**: ^3.0.2 — Асинхронный SMTP-клиент для отправки писем.  
- **email-validator**: ^2.2.0 — Для валидации адресов электронной почты.  

### **Логирование и мониторинг**  
- **structlog**: ^23.2.0 — Конфигурируемое структурированное логирование.  
- **flower**: ^2.0.1 — Панель мониторинга для Celery.  

### **Инструменты разработки**  
- **pre-commit**: ^4.0.1 — Инструмент для управления хуками pre-commit.  
- **black**: ^24.10.0 — Форматтер кода.  
- **ipython**: ^8.30.0 — Улучшенная интерактивная оболочка Python.  
- **types-passlib**: ^1.7.7.20240819 — Подсказки типов для passlib.  
- **faker**: ^33.1.0 — Генерация тестовых данных.  

---

## **Инфраструктура**  
### **Основные компоненты**  
- **Postgres**: База данных для хранения данных.  
- **RabbitMQ**: Система очередей для публикации событий.  
- **Redis**: Используется как кэш и бэкенд для Celery.  
- **Docker**: Контейнеризация для развёртывания.  

### **Логирование и мониторинг**  
- **Grafana**: Веб-интерфейс для мониторинга и визуализации данных.  
- **Loki**: Платформа для хранения и запросов логов.  
- **Vector.dev**: Инструмент для сбора логов и отправки их в Loki.  

---

## **Ключевые библиотеки Python**  
- **FastAPI**: Асинхронный фреймворк для разработки API.  
- **SQLAlchemy 2.0**: Современный ORM для работы с базами данных.  
- **Alembic**: Инструмент для миграции схем базы данных.  
- **punq**: Внедрение зависимостей для управления сервисами.  
- **didiator**: Посредник для координации логики приложения и публикации событий.  
- **adaptix** (dataclass_factory 3.0a0): Библиотека для сериализации и маппинга моделей.  
- **structlog**: Инструмент для настройки структурированного логирования.  
- **aio-pika**: Асинхронный клиент RabbitMQ для обработки сообщений. 
