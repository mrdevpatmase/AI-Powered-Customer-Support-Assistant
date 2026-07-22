from database.db import db
from datetime import datetime


class ChatHistory(db.Model):

    __tablename__ = "chat_history"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    question = db.Column(db.Text, nullable=False)

    answer = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(100))

    priority = db.Column(db.String(50))

    confidence = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)