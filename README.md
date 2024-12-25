# Проект “Погода“

`WeatherAPI` — это проект, предоставляющий простой и удобный REST API для работы с погодными данными, локациями и пользователями. Приложение позволяет добавлять, редактировать и просматривать информацию о локациях и пользователях, а также предоставляет базовые возможности авторизации.

Веб-интерфейс для проекта не подразумевается.

### Для запуска приложения

1. **Клонируйте репозиторий:**

   ```bash
   git clone https://github.com/namig41/WeatherAPI.git
   cd WeatherAPI
   ```

2. Установите все необходимые пакеты с помощью следующих команд:

   ```bash
   poetry shell
   poetry update
   ```

### Реализованные команды

- `make app` — запустить приложение и базу данных/инфраструктуру
- `make app-logs` — отслеживать логи в контейнере приложения
- `make app-down` — остановить приложение и всю инфраструктуру
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

Добавление нового пользователя в базу. Данные передаются в теле запроса в виде JSON с полями `login`, `email` и `password`. Пример ответа:

```json
{
    "login": "hardyluke",
    "email": "parrishjennifer@example.net",
    "password": "$5$rounds=535000$nuk5W9ZlYdbam0Cf$Ed2/LmObPb2mXxFNcf.7Gq/u1mxvLA/vnCE/WmFtpL3"
}
```

#### GET `/auth/login`

Вход пользователя с помощью логина и пароля. В ответе содержится `access_token` в куки.

HTTP-коды ответов:

- **200** — успешно

#### POST `/auth/logout`

Выход пользователя с помощью логина и пароля. В ответе содежиться access_token в куки:

HTTP коды ответов:
- Успех - 200
