import os
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from src.models.message import Message
from src.models.room import Room
from src.socket.events import room_users
from src.middleware.rate_limiter import check_file_rate, FILE_WINDOW_SECONDS

upload_bp = Blueprint("upload", __name__)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "application/pdf"}
MAX_SIZE      = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB

@upload_bp.route("/<room_id>", methods=["POST"])
def upload_file(room_id):
    """Subida de archivos en salas multimedia."""

    # ── P11: Verificar que la sala existe y es multimedia ──────────
    room = Room.find_by_id(room_id)
    if not room:
        return jsonify({"error": "Sala no encontrada"}), 404
    if room["type"] != "multimedia":
        return jsonify({"error": "Esta sala es de tipo texto, no permite archivos"}), 403

    if "file" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file     = request.files["file"]
    nickname = request.form.get("nickname", "")

    # ── P12: Verificar que el usuario está conectado a la sala ────
    # --- Desactivado por pruebas #
    users_in_room = room_users.get(room_id, {})
    if nickname not in users_in_room.values():
       return jsonify({"error": "No estás conectado a esta sala"}), 403

    # ── P17: Rate limiting de archivos ────────────────────────────
    if not check_file_rate(room_id, nickname):
        return jsonify({
            "error": f"Demasiados archivos. Espera {FILE_WINDOW_SECONDS}s."
        }), 429

    # Validar tipo
    if file.mimetype not in ALLOWED_TYPES:
        return jsonify({"error": "Tipo de archivo no permitido"}), 400

    # Validar tamaño
    file.seek(0, 2)  # Ir al final
    size = file.tell()
    file.seek(0)
    if size > MAX_SIZE:
        return jsonify({"error": "Archivo demasiado grande (máx 10MB)"}), 400

    # Guardar archivo de forma segura
    filename  = secure_filename(f"{room_id}_{file.filename}")
    save_path = os.path.join("uploads", filename)
    file.save(save_path)

    # Guardar mensaje en DB
    message = Message.create(
        room_id   = room_id,
        nickname  = nickname,
        msg_type  = "file",
        file_name = file.filename,
        file_path = f"/uploads/{filename}",
        file_type = file.mimetype
    )

    return jsonify(message), 201


@upload_bp.route("/files/<filename>")
def serve_file(filename):
    """Servir archivos subidos."""
    uploads_dir = os.path.abspath("uploads")  # ruta absoluta desde el CWD
    return send_from_directory(uploads_dir, filename)