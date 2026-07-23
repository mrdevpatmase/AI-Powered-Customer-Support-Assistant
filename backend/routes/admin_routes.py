from flask import Blueprint, jsonify
from sqlalchemy import func

from backend.database.db import db
from backend.models.chat_history import ChatHistory
from backend.models.user import User

admin = Blueprint("admin", __name__)


@admin.route("/dashboard", methods=["GET"])
def dashboard():

    total_users = User.query.count()

    total_queries = ChatHistory.query.count()

    shipping = ChatHistory.query.filter_by(category="Shipping").count()

    refund = ChatHistory.query.filter_by(category="Refund").count()

    payment = ChatHistory.query.filter_by(category="Payment").count()

    orders = ChatHistory.query.filter_by(category="Order").count()

    return jsonify({

        "total_users": total_users,

        "total_queries": total_queries,

        "shipping": shipping,

        "refund": refund,

        "payment": payment,

        "orders": orders

    })

@admin.route("/history", methods=["GET"])
def history():

    chats = ChatHistory.query.order_by(ChatHistory.created_at.desc()).all()

    data = []

    for chat in chats:

        user = User.query.get(chat.user_id)

        data.append({

            "id": chat.id,

            "user": user.name,

            "email": user.email,

            "question": chat.question,

            "answer": chat.answer,

            "category": chat.category,

            "priority": chat.priority,

            "confidence": chat.confidence,

            "created_at": chat.created_at.strftime("%d-%m-%Y %H:%M")

        })

    return jsonify(data)