from datetime import datetime, date
from app import db


class UserProgress(db.Model):
    __tablename__ = "user_progress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    baby_name = db.Column(db.String(100), default="Bebê")
    due_date = db.Column(db.Date, nullable=True)
    pregnancy_start = db.Column(db.Date, nullable=True)  # data da última menstruação
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="progress")

    @property
    def current_week(self) -> int:
        if self.pregnancy_start:
            delta = date.today() - self.pregnancy_start
            week = delta.days // 7 + 1
            return max(1, min(42, week))
        if self.due_date:
            days_remaining = (self.due_date - date.today()).days
            week = 40 - (days_remaining // 7)
            return max(1, min(42, week))
        return 1

    @property
    def days_remaining(self) -> int:
        if self.due_date:
            delta = (self.due_date - date.today()).days
            return max(0, delta)
        return 0

    def to_dict(self):
        return {
            "baby_name": self.baby_name,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "pregnancy_start": self.pregnancy_start.isoformat() if self.pregnancy_start else None,
            "current_week": self.current_week,
            "days_remaining": self.days_remaining,
        }
