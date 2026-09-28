# Notes API

REST API для управления заметками с тегами, фильтрацией, поиском и пагинацией.

## 🌐 Демо

**API:** https://notes-api-ja0n.onrender.com/api/notes

**Health check:** https://notes-api-ja0n.onrender.com/api/health

**Теги:** https://notes-api-ja0n.onrender.com/api/tags

---

## 📚 API Эндпоинты

### Заметки (Notes)

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/notes` | Получить все заметки |
| GET | `/api/notes?category=work` | Фильтр по категории |
| GET | `/api/notes?search=текст` | Поиск по тексту |
| GET | `/api/notes?page=1&per_page=5` | Пагинация |
| POST | `/api/notes` | Создать заметку |
| GET | `/api/notes/<id>` | Получить одну заметку |
| PUT | `/api/notes/<id>` | Обновить заметку |
| DELETE | `/api/notes/<id>` | Удалить заметку |
| GET | `/api/notes/stats` | Статистика |

### Теги (Tags)

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/tags` | Получить все теги |
| POST | `/api/tags` | Создать тег |
| DELETE | `/api/tags/<id>` | Удалить тег |
| POST | `/api/notes/<id>/tags` | Добавить тег к заметке |
| DELETE | `/api/notes/<id>/tags/<tag_id>` | Убрать тег из заметки |
| GET | `/api/notes/by-tag/<name>` | **JOIN** — заметки по тегу |

---

## 🛠 Технологии

- **Python 3.14**
- **Flask 3.1** — веб-фреймворк
- **SQLAlchemy 2.0** — ORM
- **PostgreSQL** — база данных (на Render)
- **SQLite** — база данных (локально)
- **pytest** — тестирование
- **Docker** — контейнеризация
- **Gunicorn** — WSGI-сервер
- **Render.com** — хостинг
- **DBeaver** — работа с БД

---

## 🗄 Структура базы данных

### Таблица `notes`

| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Первичный ключ |
| title | String(200) | Заголовок |
| content | Text | Содержимое |
| category | String(50) | Категория |
| priority | Integer | Приоритет (1-3) |
| created_at | DateTime | Дата создания |
| updated_at | DateTime | Дата обновления |
| is_archived | Boolean | Архивная ли заметка |

### Таблица `tags`

| Поле | Тип | Описание |
|------|-----|----------|
| id | Integer | Первичный ключ |
| name | String(50) | Название тега |
| created_at | DateTime | Дата создания |

### Таблица `note_tags` (many-to-many)

| Поле | Тип | Описание |
|------|-----|----------|
| note_id | Integer | ID заметки |
| tag_id | Integer | ID тега |

---

## 🚀 Локальный запуск

### 1. Клонирование

```bash
git clone https://github.com/sabrinagorbat/notes-api.git
cd notes-api
```

### 2. Виртуальное окружение

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск

```bash
python run.py
```

API будет доступно по адресу: `http://127.0.0.1:5000/api/notes`

---

## 📝 Примеры запросов

### Создать заметку (POST)

```bash
curl -X POST http://127.0.0.1:5000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Моя заметка","content":"Текст","category":"work","priority":2}'
```

**Ответ (201 Created):**
```json
{
    "id": 1,
    "title": "Моя заметка",
    "content": "Текст",
    "category": "work",
    "priority": 2,
    "tags": []
}
```

### Получить все заметки (GET)

```bash
curl http://127.0.0.1:5000/api/notes
```

### Получить одну заметку (GET)

```bash
curl http://127.0.0.1:5000/api/notes/1
```

### Обновить заметку (PUT)

```bash
curl -X PUT http://127.0.0.1:5000/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Обновлённая","content":"Новое"}'
```

### Удалить заметку (DELETE)

```bash
curl -X DELETE http://127.0.0.1:5000/api/notes/1
```

### Статистика (GET)

```bash
curl http://127.0.0.1:5000/api/notes/stats
```

### Все теги (GET)

```bash
curl http://127.0.0.1:5000/api/tags
```

### Создать тег (POST)

```bash
curl -X POST http://127.0.0.1:5000/api/tags \
  -H "Content-Type: application/json" \
  -d '{"name":"важное"}'
```

### Добавить тег к заметке (POST)

```bash
curl -X POST http://127.0.0.1:5000/api/notes/1/tags \
  -H "Content-Type: application/json" \
  -d '{"name":"работа"}'
```

### JOIN — заметки по тегу (GET)

```bash
curl http://127.0.0.1:5000/api/notes/by-tag/работа
```

---

## 🧪 Тесты

```bash
pytest tests/ -v
```

**Результат:** `6 passed`

---

## 📊 Обработчик логов

```bash
cd scripts
python generate_logs.py
python log_parser_slow.py
python log_parser_fast.py
```

**Результат:** найдено ~5000 ошибок в файле из 100 000 строк.

---

## 🐳 Docker

```bash
docker build -t notes-api .
docker run -p 5000:5000 notes-api
```

---

## 🌍 Деплой на Render

### 1. Создайте PostgreSQL

- Render → **New +** → **PostgreSQL**
- Name: `notes-db`
- Plan: Free
- Скопируйте **Internal Database URL**

### 2. Создайте Web Service

- Render → **New +** → **Web Service**
- Source: GitHub репозиторий
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn run:app`
- Plan: Free

### 3. Добавьте переменные окружения

| Key | Value |
|-----|-------|
| `DATABASE_URL` | (Internal Database URL) |
| `SECRET_KEY` | (ваш секретный ключ) |

### 4. Deploy

Нажмите **"Create Web Service"** и дождитесь завершения.

---

## 📁 Структура проекта

```
my_pr/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── config.py
├── scripts/
│   ├── generate_logs.py
│   ├── log_parser_slow.py
│   └── log_parser_fast.py
├── tests/
│   └── test_api.py
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── run.py
└── README.md
```

---

## 🔗 Ссылки

- **API (демо):** https://notes-api-ja0n.onrender.com/api/notes
- **Health check:** https://notes-api-ja0n.onrender.com/api/health
- **Статистика:** https://notes-api-ja0n.onrender.com/api/notes/stats
- **Теги:** https://notes-api-ja0n.onrender.com/api/tags

