from datetime import datetime
from app import db


class SavedMessage(db.Model):
    __tablename__ = "saved_messages"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey("messages.id"), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="saved_messages")
    message = db.relationship("Message")

    __table_args__ = (
        db.UniqueConstraint("user_id", "message_id", name="uq_user_message"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message.to_dict() if self.message else None,
            "saved_at": self.saved_at.isoformat(),
        }
