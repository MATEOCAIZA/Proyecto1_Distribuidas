"""
Rate Limiter — Capacidades máximas para operaciones del chat.

Usa Redis para controlar:
  - Mensajes por usuario por ventana de tiempo
  - Archivos subidos por usuario por ventana de tiempo
  - Cantidad máxima de usuarios por sala
"""

from src.config.redis_client import redis_client

# ── Configuración de límites ──────────────────────────────────────
MAX_USERS_PER_ROOM = 50            # Usuarios simultáneos por sala

MAX_MESSAGES_PER_WINDOW = 10       # Mensajes permitidos
MESSAGE_WINDOW_SECONDS = 10        # Ventana de tiempo (segundos)

MAX_FILES_PER_WINDOW = 3           # Archivos permitidos
FILE_WINDOW_SECONDS = 60           # Ventana de tiempo (segundos)


def check_message_rate(room_id: str, nickname: str) -> bool:
    """
    Verifica si el usuario puede enviar un mensaje.
    Retorna True si está dentro del límite, False si lo excedió.

    Usa un contador en Redis con expiración automática (sliding window simplificado).
    """
    key = f"rate:msg:{room_id}:{nickname}"
    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, MESSAGE_WINDOW_SECONDS)
    return current <= MAX_MESSAGES_PER_WINDOW


def check_file_rate(room_id: str, nickname: str) -> bool:
    """
    Verifica si el usuario puede subir un archivo.
    Retorna True si está dentro del límite, False si lo excedió.
    """
    key = f"rate:file:{room_id}:{nickname}"
    current = redis_client.incr(key)
    if current == 1:
        redis_client.expire(key, FILE_WINDOW_SECONDS)
    return current <= MAX_FILES_PER_WINDOW


def check_room_capacity(room_users: dict, room_id: str) -> bool:
    """
    Verifica si la sala tiene espacio para un nuevo usuario.
    Retorna True si hay espacio, False si está llena.
    """
    return len(room_users.get(room_id, {})) < MAX_USERS_PER_ROOM
