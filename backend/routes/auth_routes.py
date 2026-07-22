import os

from flask import Blueprint, request, jsonify
from database.db import db
from models.user import User
import bcrypt
import jwt
from datetime import datetime, timedelta
from config import Config
from middleware.auth_middleware import token_required

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

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

    return jsonify({"message": "User Created Successfully"})

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