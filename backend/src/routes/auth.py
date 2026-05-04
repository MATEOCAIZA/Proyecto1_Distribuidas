import jwt
import os
import datetime
from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login del administrador."""
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    # Validar credenciales contra el .env
    if (username != os.getenv("ADMIN_USER") or
            password != os.getenv("ADMIN_PASS")):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = jwt.encode(
        {
            "role": "admin",
            "exp":  datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        },
        os.getenv("JWT_SECRET"),
        algorithm="HS256"
    )

    return jsonify({"token": token})