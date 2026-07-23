from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from backend.middleware.auth_middleware import token_required
from backend.database.db import db
from backend.models.document import Document
import os
from backend.services.pdf_service import extract_text
from backend.services.chunker import chunk_text
from backend.services.embedding_service import create_embeddings
from backend.services.vector_service import save_embeddings


document = Blueprint("document", __name__)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@document.route("/upload", methods=["POST"])
@token_required
def upload_pdf():

    if "file" not in request.files:
        return jsonify({"message": "No File"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No File Selected"}), 400

    filename = secure_filename(file.filename)

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    text = extract_text(filepath)

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    stored = save_embeddings(embeddings, chunks)

    print(f"Chunks : {len(chunks)}")
    print(f"Embeddings : {len(embeddings)}")
    print(f"Dimension : {len(embeddings[0])}")

    print(f"Total Chunks : {len(chunks)}")
    print(chunks[0])

    print("=" * 50)
    print(text[:1000])
    print("=" * 50)

    pdf = Document(
        filename=filename,
        filepath=filepath,
        uploaded_by=request.user["id"]
    )

    db.session.add(pdf)
    db.session.commit()

    return jsonify({
        "message": "PDF Uploaded",
        "filename": filename,
        "characters": len(text),
        "chunks": len(chunks),
        "embeddings": len(embeddings),
        "dimension": len(embeddings[0]),
        "stored_vectors": stored
    })