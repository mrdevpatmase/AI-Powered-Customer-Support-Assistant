from flask import Blueprint, request, jsonify

from backend.middleware.auth_middleware import token_required
from backend.services.embedding_service import create_query_embedding
from backend.services.search_service import search
from backend.services.llm_service import ask_llm

from backend.models.chat_history import ChatHistory
from backend.database.db import db

chat = Blueprint("chat", __name__)


@chat.route("/ask", methods=["POST"])
@token_required
def ask():

    question = request.json.get("question", "").strip()
    normalized = question.lower()

    # ==========================
    # Greeting Handling
    # ==========================

    greetings = {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    }

    thanks = {
        "thanks",
        "thank you",
        "thx",
        "thankyou"
    }

    goodbyes = {
        "bye",
        "goodbye",
        "see you",
        "see ya"
    }

    if normalized in greetings:

        result = {
            "category": "General Information",
            "priority": "Low",
            "confidence": 100,
            "answer": (
                "👋 Hello!\n\n"
                "Welcome to ShopEase Customer Support.\n\n"
                "I can help you with:\n"
                "• Orders\n"
                "• Shipping\n"
                "• Refunds\n"
                "• Returns\n"
                "• Payments\n"
                "• Account-related issues\n\n"
                "How can I assist you today?"
            )
        }

    elif normalized in thanks:

        result = {
            "category": "General Information",
            "priority": "Low",
            "confidence": 100,
            "answer": "You're welcome! 😊 I'm happy to help. If you have any other ShopEase-related questions, just ask."
        }

    elif normalized in goodbyes:

        result = {
            "category": "General Information",
            "priority": "Low",
            "confidence": 100,
            "answer": "👋 Thank you for contacting ShopEase Customer Support. Have a great day!"
        }

    else:
        # ==========================
        # RAG Pipeline
        # ==========================

        embedding = create_query_embedding(question)

        chunks = search(embedding)

        context = "\n\n".join(chunks)

        result = ask_llm(context, question)

    # ==========================
    # Save Conversation
    # ==========================

    history = ChatHistory(
        user_id=request.user["id"],
        question=question,
        answer=result["answer"],
        category=result["category"],
        priority=result["priority"],
        confidence=result["confidence"]
    )

    db.session.add(history)
    db.session.commit()

    return jsonify(result)