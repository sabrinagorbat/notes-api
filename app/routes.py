from flask import Blueprint, request, jsonify
from app import db
from app.models import Note, Tag
from sqlalchemy import or_

bp = Blueprint("api", __name__)

@bp.route("/")
def home():
    return jsonify({"message": "Notes API", "status": "running"})


@bp.route("/health")
def health():
    return jsonify({"status": "healthy"})

@bp.route("/notes", methods=["GET"])
def get_notes():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    category = request.args.get("category")
    search = request.args.get("search")
    query = Note.query.filter_by(is_archived=False)
    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(or_(Note.title.ilike(f"%%{search}%%"), Note.content.ilike(f"%%{search}%%")))
    pagination = query.order_by(Note.created_at.desc()).paginate(page=page, per_page=per_page)
    return jsonify({
        "items": [note.to_dict() for note in pagination.items],
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages
    })

@bp.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Title and content required"}), 400
    note = Note(
        title=data["title"],
        content=data["content"],
        category=data.get("category", "general"),
        priority=data.get("priority", 1)
    )
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201

@bp.route("/notes/<int:note_id>", methods=["GET"])
def get_note(note_id):
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@bp.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()
    if "title" in data:
        note.title = data["title"]
    if "content" in data:
        note.content = data["content"]
    if "category" in data:
        note.category = data["category"]
    if "priority" in data:
        note.priority = data["priority"]
    if "is_archived" in data:
        note.is_archived = data["is_archived"]
    db.session.commit()
    return jsonify(note.to_dict())

@bp.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return "", 204

@bp.route("/notes/stats", methods=["GET"])
def get_stats():
    total = Note.query.count()
    archived = Note.query.filter_by(is_archived=True).count()
    categories = db.session.query(Note.category, db.func.count(Note.id)).group_by(Note.category).all()
    return jsonify({
        "total": total,
        "archived": archived,
        "categories": [{"name": c[0], "count": c[1]} for c in categories]
    })

# ============ TAGS ============

@bp.route("/tags", methods=["GET"])
def get_tags():
    """Получить все теги"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    pagination = Tag.query.order_by(Tag.name).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        "items": [tag.to_dict() for tag in pagination.items],
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages
    })


@bp.route("/tags", methods=["POST"])
def create_tag():
    """Создать тег"""
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    name = data["name"].strip().lower()
    if not name:
        return jsonify({"error": "Name cannot be empty"}), 400

    existing = Tag.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "Tag already exists"}), 409

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag.to_dict()), 201


@bp.route("/tags/<int:tag_id>", methods=["DELETE"])
def delete_tag(tag_id):
    """Удалить тег"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return "", 204


@bp.route("/notes/<int:note_id>/tags", methods=["POST"])
def add_tag_to_note(note_id):
    """Добавить тег к заметке"""
    note = Note.query.get_or_404(note_id)
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    name = data["name"].strip().lower()
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.flush()

    if tag not in note.tags:
        note.tags.append(tag)
        db.session.commit()

    return jsonify(note.to_dict()), 200


@bp.route("/notes/<int:note_id>/tags/<int:tag_id>", methods=["DELETE"])
def remove_tag_from_note(note_id, tag_id):
    """Удалить тег из заметки"""
    note = Note.query.get_or_404(note_id)
    tag = Tag.query.get_or_404(tag_id)

    if tag in note.tags:
        note.tags.remove(tag)
        db.session.commit()

    return jsonify(note.to_dict()), 200


@bp.route("/notes/by-tag/<tag_name>", methods=["GET"])
def get_notes_by_tag(tag_name):
    """Получить заметки по тегу (JOIN)"""
    notes = Note.query.join(Note.tags).filter(Tag.name == tag_name.lower()).all()
    return jsonify([note.to_dict() for note in notes])
