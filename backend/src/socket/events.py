import time
from flask_socketio import emit, join_room, leave_room
from flask import request
from src.models.room import Room
from src.models.message import Message
from src.config.redis_client import redis_client

from src.workers.broadcast import broadcast_in_thread, broadcast_with_db

from src.middleware.rate_limiter import (
    check_message_rate,
    check_room_capacity,
    MAX_USERS_PER_ROOM,
    MESSAGE_WINDOW_SECONDS,
)

INACTIVITY_TIMEOUT = 900

# Usuarios en memoria: { room_id: { socket_id: nickname } }
room_users: dict[str, dict] = {}

# Última actividad por sid (timestamp Unix)
last_activity: dict[str, float] = {}


def _check_inactivity(socketio):
    """
    Tarea en background que revisa periódicamente (cada 60s)
    si hay usuarios inactivos y los desconecta.
    """
    while True:
        socketio.sleep(60)
        now = time.time()
        inactive_sids = [
            sid for sid, ts in list(last_activity.items())
            if now - ts > INACTIVITY_TIMEOUT
        ]
        for sid in inactive_sids:
            socketio.emit(
                "error",
                {"message": "Desconectado por inactividad"},
                to=sid
            )
            socketio.disconnect(sid)

def register_events(socketio):

    """Registra todos los eventos WebSocket."""

    socketio.start_background_task(_check_inactivity,socketio)

    @socketio.on("join_room")
    def on_join(data):
        room_id   = data.get("roomId", "")
        pin       = data.get("pin", "")
        nickname  = data.get("nickname", "").strip()
        client_ip = _get_ip()

        # 1. Buscar sala
        room = Room.find_by_id(room_id)
        if not room:
            emit("error", {"message": "Sala no encontrada"})
            return

        # 2. Verificar PIN
        if not Room.verify_pin(room, pin):
            emit("error", {"message": "PIN incorrecto"})
            return

        # 3. Sesión única por IP
        existing = redis_client.get(f"session:{client_ip}")
        if existing and existing != request.sid:
            emit("error", {"message": "Ya tienes una sesión activa"})
            return

        # 4. Nickname único en sala
        users_in_room = room_users.get(room_id, {})
        if nickname in users_in_room.values():
            emit("error", {"message": "Nickname ya está en uso"})
            return

        # 5. Registrar sesión en Redis (1 hora)
        redis_client.setex(f"session:{client_ip}", 3600, request.sid)

        # 6. Unir al room de SocketIO
        join_room(room_id)
        room_users.setdefault(room_id, {})[request.sid] = nickname

        # 7. Guardar datos en sesión
        request.environ["room_id"]   = room_id
        request.environ["nickname"]  = nickname
        request.environ["client_ip"] = client_ip

        # 8. Enviar historial y datos de sala
        history = Message.get_history(room_id)
        emit("room_joined", {
            "room":    {"roomId": room["roomId"],
                        "name":   room["name"],
                        "type":   room["type"]},
            "history": history
        })

        # 9. Notificar lista de usuarios
        user_list = list(room_users[room_id].values())
        socketio.emit("user_list",{"users": user_list},room=room_id)
        # 10. Notificar que alguien entró
        socketio.emit("user_joined", {"nickname": nickname}, room=room_id)


    @socketio.on("send_message")
    def on_message(data):
        room_id  = request.environ.get("room_id")
        nickname = request.environ.get("nickname")
        content  = data.get("content", "").strip()

        if not room_id or not content:
            return

        # La escritura a MongoDB Y el emit se hacen en el pool de hilos.
        # El handler retorna de inmediato — sin esperar I/O alguno.
        broadcast_with_db(
            socketio,
            room_id  = room_id,
            event    = "new_message",
            create_fn = Message.create,
            create_kwargs = dict(
                room_id  = room_id,
                nickname = nickname,
                content  = content,
                msg_type = "text"
            )
        )

    @socketio.on("send_file_message")
    def on_file_message(data):
        from flask import request as sio_request
        room_id  = sio_request.environ.get("room_id")
        nickname = sio_request.environ.get("nickname")
        path  = data.get("path", "").strip()
        type = data.get("type","").strip()
        name = data.get("file_name", "").strip()

        if not room_id or not path or not type or not name:
            return

        # Rate limiting de mensajes (P17)
        if not check_message_rate(room_id, nickname):
            emit("error", {
                "message": f"Demasiados mensajes. Máx {MESSAGE_WINDOW_SECONDS}s entre ráfagas."
            })
            return

        # BD + emit en el pool de hilos (P15) — handler retorna de inmediato
        broadcast_with_db(
            socketio,
            room_id  = room_id,
            event    = "new_message",
            create_fn = Message.create,
            create_kwargs = dict(
                room_id   = room_id,
                nickname  = nickname,
                content   = None,
                msg_type  = "file",
                file_name = name,
                file_path = path,
                file_type = type
            )
        )

    @socketio.on("load_more_messages")
    def on_load_more(data):
        """
        Paginación del historial — el frontend envía el timestamp
        del mensaje más antiguo que tiene para cargar los anteriores.
        (P14)
        """
        room_id = data.get("roomId", "")
        before  = data.get("before", None)

        if not room_id:
            return

        messages = Message.get_history(room_id, limit=50, before=before)
        emit("more_messages", {
            "messages": messages,
            "hasMore":  len(messages) == 50
        })


    @socketio.on("disconnect")
    def on_disconnect():
        room_id   = request.environ.get("room_id")
        nickname  = request.environ.get("nickname")
        client_ip = request.environ.get("client_ip")

        if not room_id:
            return

        if room_id in room_users:
            room_users[room_id].pop(request.sid, None)

        if client_ip:
            redis_client.delete(f"session:{client_ip}")

        socketio.emit("user_left", {"nickname": nickname}, room=room_id)
        user_list = list(room_users.get(room_id, {}).values())
        socketio.emit("user_list", {"users": user_list}, room=room_id)

        leave_room(room_id)


def _get_ip():
    return (request.environ.get("HTTP_X_FORWARDED_FOR") or
            request.environ.get("REMOTE_ADDR", "unknown"))