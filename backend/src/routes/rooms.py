from flask import Blueprint, request, jsonify
from src.models.room import Room
from src.middleware.auth import token_required

rooms_bp = Blueprint("rooms", __name__)

@rooms_bp.route("/", methods=["POST"])
@token_required
def create_room():
    """Crear sala (solo administrador)."""
    data = request.get_json()
    name      = data.get("name", "").strip()
    pin       = data.get("pin", "")
    room_type = data.get("type", "")

    if not name:
        return jsonify({"error": "El nombre es requerido"}), 400

    try:
        room = Room.create(name, pin, room_type)
        return jsonify(room), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@rooms_bp.route("/", methods=["GET"])
@token_required
def list_rooms():
    """Listar todas las salas (solo administrador)."""
    rooms = Room.get_all()
    return jsonify(rooms)


@rooms_bp.route("/<room_id>/verify", methods=["POST"])
def verify_room(room_id):
    """Verificar PIN de sala (para usuarios)."""
    data = request.get_json()
    pin  = data.get("pin", "")

    room = Room.find_by_id(room_id)
    if not room:
        return jsonify({"error": "Sala no encontrada"}), 404

    if not Room.verify_pin(room, pin):
        return jsonify({"error": "PIN incorrecto"}), 401

    return jsonify({
        "roomId": room["roomId"],
        "name":   room["name"],
        "type":   room["type"]
    })

    