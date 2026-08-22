# Notes API

REST API для управления заметками с фильтрацией, поиском и пагинацией.

## Демо

[https://notes-api-ja0n.onrender.com/api/](https://notes-api-ja0n.onrender.com/api/)

## API Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/` | Приветствие |
| GET | `/api/health` | Проверка статуса |
| GET | `/api/notes` | Получить все заметки |
| GET | `/api/notes?category=work` | Фильтр по категории |
| GET | `/api/notes?search=текст` | Поиск по тексту |
| GET | `/api/notes?page=1&per_page=5` | Пагинация |
| POST | `/api/notes` | Создать заметку |
| GET | `/api/notes/{id}` | Получить заметку по ID |
| PUT | `/api/notes/{id}` | Обновить заметку |
| DELETE | `/api/notes/{id}` | Удалить заметку |
| GET | `/api/notes/stats` | Статистика |

## Технологии

- Python 3.10+
- Flask 3.1
- SQLAlchemy 2.0
- SQLite
- Gunicorn
- Render (деплой)

## Локальный запуск

```bash
# Клонирование
git clone https://github.com/sabrinagorbat/notes-api.git
cd notes-api

# Виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск
python run.py

## Пример запроса в Postman
Создать заметку (POST)
json
POST /api/notes
{
    "title": "Моя заметка",
    "content": "Текст заметки",
    "category": "work",
    "priority": 2
}
Ответ
json
{
    "id": 1,
    "title": "Моя заметка",
    "content": "Текст заметки",
    "category": "work",
    "priority": 2,
    "created_at": "2026-08-22T11:03:36",
    "updated_at": null,
    "is_archived": false
}
Получить все заметки (GET)
text
GET /api/notes
Получить статистику (GET)
text
GET /api/notes/stats
json
{
    "total": 5,
    "archived": 1,
    "categories": [
        {"name": "work", "count": 2},
        {"name": "personal", "count": 1}
    ]
}
🌍 Деплой
Проект развернут на Render.com

Ссылка: https://notes-api-ja0n.onrender.com