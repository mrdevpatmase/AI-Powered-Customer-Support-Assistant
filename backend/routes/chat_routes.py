from flask import Blueprint, request, jsonify

from middleware.auth_middleware import token_required

from services.embedding_service import create_query_embedding
from services.search_service import search
from services.llm_service import ask_llm

chat = Blueprint("chat", __name__)


@chat.route("/ask", methods=["POST"])
@token_required
def ask():

    question = request.json["question"]

    embedding = create_query_embedding(question)

    chunks = search(embedding)

    context = "\n\n".join(chunks)

    answer = ask_llm(context, question)

    return jsonify({
        "response": answer
    })