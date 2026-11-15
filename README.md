
# Task API

Микросервис для управления задачами.

## Технологии

- Python 3.12
- FastAPI
- PostgreSQL 16
- Docker
- Docker Compose

## API

| Метод | URL | Описание |
|---|---|---|
| GET | /tasks | Получить все задачи |
| GET | /tasks/{id} | Получить задачу |
| POST | /tasks | Создать задачу |
| PATCH | /tasks/{id} | Изменить задачу |
| DELETE | /tasks/{id} | Удалить задачу |

## Запуск

Требуются Docker и Docker Compose.

1. Клонировать репозиторий.
2. Перейти в директорию проекта.
3. Создать файл конфигурации:

   cp .env.example .env

4. Запустить контейнеры:

   docker compose up -d --build

5. Проверить API:

   curl http://localhost:8001/tasks

API доступен по адресу http://localhost:8001/tasks
на компьютере, где запущен Docker.

## Обработка ошибок

- 400 — пустое обновление
- 404 — задача не найдена
- 422 — некорректные входные данные

## Архитектура

Приложение и PostgreSQL запускаются в отдельных
Docker-контейнерах через Docker Compose.

Dockerfile использует multi-stage сборку.
Данные PostgreSQL сохраняются в Docker volume.
