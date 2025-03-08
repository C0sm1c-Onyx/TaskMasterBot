# TaskMasterBot

TaskMasterBot - это система управления задачами с Telegram-ботом и REST API интерфейсом. Проект позволяет создавать задачи, управлять ими и получать уведомления о сроках выполнения.

## Технологический стек

- Python 3.13
- Django 5.1
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Aiogram
- Docker & Docker Compose

## Структура проекта

```
TaskMasterBot/
├── todo_list/
│   ├── core/                 # Основное приложение с моделями
│   │   ├── models.py        # Модели данных
│   │   ├── serializers.py   # Сериализаторы для API
│   │   ├── urls.py         # URL маршруты API
│   │   └── views.py        # Представления API
│   │
│   ├── auth_users/          # Приложение аутентификации
│   │   ├── models.py       # Модель пользователя
│   │   └── ...
│   │
│   ├── telegrambot/         # Telegram бот
│   │   ├── bot.py          # Основной файл бота
│   │   ├── handlers.py     # Обработчики команд
│   │   ├── services.py     # Сервисы для работы с API
│   │   ├── keyboards.py    # Клавиатуры бота
│   │   └── utils.py        # Вспомогательные функции
│   │
│   └── todo_list/          # Основной проект Django
│       ├── settings.py
│       ├── urls.py
│       └── celery.py
```

## Запуск проекта

### Предварительные требования

- Docker
- Docker Compose

### Настройка окружения

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd TaskMasterBot
```

2. Создайте файл .env в корневой директории проекта:
```env
POSTGRES_DB_NAME=your_db_name
POSTGRES_USER_NAME=your_db_user
POSTGRES_PASSWORD=your_db_password
TELEGRAM_BOT_TOKEN=your_bot_token
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_password
```

3. Запустите проект:
```bash
docker-compose up --build
```

## Функциональность

### Core App (Основное приложение)

Содержит основные модели и логику работы с задачами:

- **TGbotUser**: Модель пользователя Telegram
- **Category**: Категории задач
- **Task**: Задачи
- **Comment**: Комментарии к задачам

### Auth Users App (Приложение аутентификации)

Управление пользователями и аутентификацией:

- Кастомная модель пользователя
- JWT аутентификация
- Регистрация и подтверждение email

### Telegram Bot

Бот для управления задачами через Telegram:

- Создание задач
- Просмотр списка задач
- Добавление комментариев
- Просмотр комментариев
- Уведомления о сроках выполнения

Ссылка на бота: [@your_bot_name](https://t.me/your_bot_name)

### Celery Tasks

Celery используется для асинхронных задач:

- Отправка email уведомлений
- Проверка сроков выполнения задач
- Отправка уведомлений в Telegram о приближающихся дедлайнах

## REST API Documentation

### Аутентификация

#### Получение токена

```http
POST /api/v1/token/
Content-Type: application/json

{
    "username": "user",
    "password": "password"
}
```

### Пользователи Telegram

#### Получение пользователя
```http
GET /api/v1/get_user/{username}/
```

#### Создание пользователя
```http
POST /api/v1/create_tg_user/
Content-Type: application/json

{
    "username_id": "username",
    "chat_id": "chat_id"
}
```

### Задачи

#### Список задач пользователя
```http
GET /api/v1/task-list/{username}/
```

#### Создание задачи
```http
POST /api/v1/create-task/
Content-Type: application/json

{
    "user_id": "username",
    "task_title": "Title",
    "task_description": "Description",
    "start_date": "2025-03-06",
    "task_category_id": "category_id"
}
```

### Категории

#### Создание категории
```http
POST /api/v1/create-category/
Content-Type: application/json

{
    "category_name": "Category Name"
}
```

### Комментарии

#### Список комментариев к задаче
```http
GET /api/v1/list-comment/{task_id}/
```

#### Создание комментария
```http
POST /api/v1/create_comment/{task_id}/
Content-Type: application/json

{
    "comment": "Comment text",
    "username_id": "username",
    "task_id": "task_id"
}
```
