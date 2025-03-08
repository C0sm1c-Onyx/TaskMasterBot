# TaskMasterBot

TaskMasterBot - это система управления задачами с Telegram-ботом и REST API интерфейсом. Проект позволяет создавать задачи, управлять ими и получать уведомления о сроках выполнения.

## Технологический стек

- Python
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Aiogram
- Docker & Docker Compose

## Запуск проекта

### Настройка окружения

1. Клонируйте репозиторий:
```bash
git clone https://github.com/C0sm1c-Onyx/TaskMasterBot.git
cd TaskMasterBot
```

2. Отредактируйте файл .env в корневой директории проекта:
```env
POSTGRES_DB_NAME=your_db_name
POSTGRES_USER_NAME=your_db_user
POSTGRES_PASSWORD=your_db_password
```

3. Запустите проект:
```bash
docker-compose up --build
```

## Функциональность

### Core App (Основное приложение)

Содержит основные модели и логику работы с задачами:

- REST API для телеграм пользователей и отправки уведомлений
- REST API для категорий, задач и комментариев

### Auth Users App (Приложение аутентификации)

Управление пользователями и аутентификацией:

- Кастомная модель пользователя
- JWT аутентификация - после регистрации и активации по email
- Регистрация и подтверждение email

### Telegram Bot

Бот для управления задачами через Telegram:

- Создание задач
- Просмотр списка задач
- Добавление комментариев
- Просмотр комментариев
- Уведомления о сроках выполнения

Ссылка на бота: https://t.me/TodoListMasterBot

### Celery Tasks

- Проверка сроков начала исполнения задач
- Отправка уведомлений в Telegram о приближающихся дедлайнах

## REST API Documentation

### Аутентификация

#### Создание пользователя
```http
POST /api/v1/token/
Content-Type: application/json
{
    "email": "email-настоящий для подтверждения",
    "username": "username",
    "password": "password",
    "re_password": "re_password"
}
```

#### получение токена
```http
POST /api/v1/token/
Content-Type: application/json

{
    "username": "user",
    "password": "password"
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
