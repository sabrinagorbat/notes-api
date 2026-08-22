from app import db 
from datetime import datetime 
from sqlalchemy.sql import func 
 
class User(db.Model): 
    __tablename__ = "users" 
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(80), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False) 
    created_at = db.Column(db.DateTime, server_default=func.now()) 
    notes = db.relationship("Note", backref="author", lazy=True) 
 
class Tag(db.Model): 
    __tablename__ = "tags" 
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), unique=True, nullable=False) 
 
class Note(db.Model): 
    __tablename__ = "notes" 
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(200), nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    category = db.Column(db.String(50), default="general") 
    priority = db.Column(db.Integer, default=1) 
    created_at = db.Column(db.DateTime, server_default=func.now()) 
    updated_at = db.Column(db.DateTime, onupdate=func.now()) 
    is_archived = db.Column(db.Boolean, default=False) 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True) 
 
    def to_dict(self): 
        return { 
            "id": self.id, 
            "title": self.title, 
            "content": self.content, 
            "category": self.category, 
            "priority": self.priority, 
            "created_at": self.created_at.isoformat() if self.created_at else None, 
            "updated_at": self.updated_at.isoformat() if self.updated_at else None, 
            "is_archived": self.is_archived, 
            "user_id": self.user_id 
        } 
