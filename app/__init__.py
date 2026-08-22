from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:sabri@localhost:5432/notes_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    CORS(app)
    db.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app
