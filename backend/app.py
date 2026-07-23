from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask
from flask_cors import CORS

from config import Config
from database.db import db

from routes.auth_routes import auth
from routes.document_routes import document
from routes.chat_routes import chat
from routes.admin_routes import admin

app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Enable CORS
CORS(app)

# Environment variables
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Initialize Database
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    from models.user import User
    from models.document import Document
    from models.chat_history import ChatHistory

    db.create_all()

# Register Blueprints
app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(document, url_prefix="/api/document")
app.register_blueprint(chat, url_prefix="/api/chat")
app.register_blueprint(admin, url_prefix="/api/admin")


@app.route("/")
def home():
    return {
        "status": "Running",
        "project": "AI Powered Customer Support Assistant"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)