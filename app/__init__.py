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
    """Создаёт начальные заметки, если база пустая"""
    from app.models import Note

    if Note.query.count() == 0:
        notes = [
            Note(
                title="Добро пожаловать в Notes API",
                content="Это первая заметка, созданная автоматически",
                category="general",
                priority=1
            ),
            Note(
                title="Рабочая задача",
                content="Подготовить отчёт по практике",
                category="work",
                priority=3
            ),
            Note(
                title="Личная заметка",
                content="Купить продукты: молоко, хлеб, яйца",
                category="personal",
                priority=2
            ),
        ]
        db.session.add_all(notes)
        db.session.commit()
        print("✅ Созданы начальные заметки")


app = create_app()