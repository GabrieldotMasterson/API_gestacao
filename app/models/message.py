from datetime import datetime
from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)  # daily, health, nutrition, curiosity, medical
    name = db.Column(db.String(100), nullable=False)
    emoji = db.Column(db.String(10), default="✨")
    messages = db.relationship("Message", back_populates="category", cascade="all, delete-orphan")

    def to_dict(self):
        return {"id": self.id, "slug": self.slug, "name": self.name, "emoji": self.emoji}


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    emoji = db.Column(db.String(10), default="🌸")
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    week_min = db.Column(db.Integer, default=1)   # semana gestacional mínima
    week_max = db.Column(db.Integer, default=42)  # semana gestacional máxima
    day_index = db.Column(db.Integer, default=0)  # índice para rotação diária
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship("Category", back_populates="messages")

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "emoji": self.emoji,
            "category": self.category.slug if self.category else None,
            "category_name": self.category.name if self.category else None,
            "week_min": self.week_min,
            "week_max": self.week_max,
        }
