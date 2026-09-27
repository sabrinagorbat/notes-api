from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///notes.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
    app.config["JSON_AS_ASCII"] = False
    CORS(app)
    db.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp, url_prefix="/api")

    with app.app_context():
        db.create_all()
        seed_data()  # ← добавляем

    return app


def seed_data():
    """Создаёт начальные заметки и теги, если база пустая"""
    from app.models import Note, Tag

    # Создаём теги
    if Tag.query.count() == 0:
        tags = [
            Tag(name="важное"),
            Tag(name="работа"),
            Tag(name="личное"),
            Tag(name="учёба"),
        ]
        db.session.add_all(tags)
        db.session.commit()
        print("✅ Созданы теги")

    # Создаём заметки
    if Note.query.count() == 0:
        work_tag = Tag.query.filter_by(name="работа").first()
        personal_tag = Tag.query.filter_by(name="личное").first()
        important_tag = Tag.query.filter_by(name="важное").first()

        notes = [
            Note(
                title="Добро пожаловать в Notes API",
                content="Это первая заметка, созданная автоматически",
                category="general",
                priority=1,
                tags=[personal_tag] if personal_tag else []
            ),
            Note(
                title="Рабочая задача",
                content="Подготовить отчёт по практике",
                category="work",
                priority=3,
                tags=[work_tag, important_tag] if work_tag else []
            ),
            Note(
                title="Личная заметка",
                content="Купить продукты: молоко, хлеб, яйца",
                category="personal",
                priority=2,
                tags=[personal_tag] if personal_tag else []
            ),
        ]
        db.session.add_all(notes)
        db.session.commit()
        print("✅ Созданы начальные заметки с тегами")
app = create_app()