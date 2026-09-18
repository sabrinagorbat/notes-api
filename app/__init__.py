from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key")
    app.config["JSON_AS_ASCII"] = False
    CORS(app)
    db.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app

app = create_app()
