import os
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from src.models.message import Message

upload_bp = Blueprint("upload", __name__)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "application/pdf"}
MAX_SIZE      = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB

@upload_bp.route("/<room_id>", methods=["POST"])
def upload_file(room_id):
    """Subida de archivos en salas multimedia."""
    if "file" not in request.files:
        return jsonify({"error": "No se envió archivo"}), 400

    file     = request.files["file"]
    nickname = request.form.get("nickname", "")

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