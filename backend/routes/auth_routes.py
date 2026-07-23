import os

from flask import Blueprint, request, jsonify
from backend.database.db import db
from backend.models.user import User
import bcrypt
import jwt
from datetime import datetime, timedelta
from backend.config import Config
from backend.middleware.auth_middleware import token_required

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    # Required fields
    if not name:
        return jsonify({"message": "Name is required"}), 400

    if not email:
        return jsonify({"message": "Email is required"}), 400

    if not password:
        return jsonify({"message": "Password is required"}), 400

    # Name length
    if len(name) < 2:
        return jsonify({"message": "Name must be at least 2 characters"}), 400

    # Password length
    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters"}), 400

    # Duplicate email
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    user = User(
        name=name,
        email=email,
        password=hashed
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User Created Successfully"}), 201

@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message": "Invalid Email or Password"}), 401

    if not bcrypt.checkpw(password.encode(), user.password.encode()):
        return jsonify({"message": "Invalid Email or Password"}), 401

    token = jwt.encode(
        {
            "id": user.id,
            "name": user.name,
            "role": user.role,
            "exp": datetime.utcnow() + timedelta(days=1)
        },
        Config.SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login Successful",
        "token": token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    })

@auth.route("/profile")
@token_required
def profile():

    return jsonify({
        "user": request.user
    })

@auth.route("/admin-login", methods=["POST"])
def admin_login():

    data = request.get_json()

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    if (
        data.get("email") != ADMIN_EMAIL or
        data.get("password") != ADMIN_PASSWORD
    ):
        return jsonify({
            "message": "Invalid Admin Credentials"
        }), 401

    token = jwt.encode(
        {
            "id": 0,
            "name": "Administrator",
            "email": ADMIN_EMAIL,
            "role": "admin",
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        Config.SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login Successful",
        "token": token,
        "user": {
            "id": 0,
            "name": "Administrator",
            "email": ADMIN_EMAIL,
            "role": "admin"
        }
    }), 200