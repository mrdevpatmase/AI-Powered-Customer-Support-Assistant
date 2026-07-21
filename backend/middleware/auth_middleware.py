import jwt
from functools import wraps
from flask import request, jsonify
from config import Config


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token Missing"}), 401

        try:
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            data = jwt.decode(
                token,
                Config.SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = data

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token Expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid Token"}), 401

        return f(*args, **kwargs)

    return decorated