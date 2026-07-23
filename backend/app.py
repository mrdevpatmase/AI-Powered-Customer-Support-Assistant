from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.config import Config
from backend.database.db import db

from backend.routes.auth_routes import auth
from backend.routes.document_routes import document
from backend.routes.chat_routes import chat
from backend.routes.admin_routes import admin


# ======================================
# Frontend Path
# ======================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

# ======================================
# Configuration
# ======================================

app.config.from_object(Config)

# Enable CORS
CORS(app)

# Environment Variables
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# ======================================
# Database
# ======================================

db.init_app(app)

with app.app_context():
    from backend.models.user import User
    from backend.models.document import Document
    from backend.models.chat_history import ChatHistory

    db.create_all()

# ======================================
# Register Blueprints
# ======================================

app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(document, url_prefix="/api/document")
app.register_blueprint(chat, url_prefix="/api/chat")
app.register_blueprint(admin, url_prefix="/api/admin")

# ======================================
# Frontend Routes
# ======================================

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static(path):

    file_path = os.path.join(app.static_folder, path)

    if os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)

    return send_from_directory(app.static_folder, "index.html")


# ======================================
# Run App
# ======================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)