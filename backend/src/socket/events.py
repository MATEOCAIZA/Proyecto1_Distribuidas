import time
from flask_socketio import emit, join_room, leave_room
from src.models.room import Room
from src.models.message import Message
from src.config.redis_client import redis_client
from src.workers.broadcast import broadcast_task
from src.middleware.rate_limiter import (
    check_message_rate,
    check_room_capacity,
    MAX_USERS_PER_ROOM,
    MESSAGE_WINDOW_SECONDS,
)

# Usuarios en memoria: { room_id: { socket_id: nickname } }
room_users: dict[str, dict] = {}

# Última actividad por sid (timestamp Unix)
last_activity: dict[str, float] = {}

# Timeout de inactividad (15 minutos)
INACTIVITY_TIMEOUT = 900


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

    # Iniciar tarea de verificación de inactividad (P13)
    socketio.start_background_task(_check_inactivity, socketio)

    @socketio.on("join_room")
    def on_join(data):
        room_id  = data.get("roomId", "")
        pin      = data.get("pin", "")
        nickname = data.get("nickname", "").strip()
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
        from flask import request as sio_request
        if existing and existing != sio_request.sid:
            emit("error", {"message": "Ya tienes una sesión activa"})
            return

        # 4. Nickname único en sala
        users_in_room = room_users.get(room_id, {})
        if nickname in users_in_room.values():
            emit("error", {"message": "Nickname ya está en uso"})
            return

        # 5. Verificar capacidad máxima de la sala (P17)
        if not check_room_capacity(room_users, room_id):
            emit("error", {
                "message": f"Sala llena (máx {MAX_USERS_PER_ROOM} usuarios)"
            })
            return

        # 6. Registrar sesión en Redis (1 hora)
        redis_client.setex(f"session:{client_ip}", 3600, sio_request.sid)

        # 7. Unir al room de SocketIO
        join_room(room_id)
        room_users.setdefault(room_id, {})[sio_request.sid] = nickname

        # 8. Guardar datos en sesión
        sio_request.environ["room_id"]   = room_id
        sio_request.environ["nickname"]  = nickname
        sio_request.environ["client_ip"] = client_ip

        # 9. Registrar actividad (P13)
        last_activity[sio_request.sid] = time.time()

        # 10. Enviar historial y datos de sala
        history = Message.get_history(room_id)
        emit("room_joined", {
            "room":    {"roomId": room["roomId"],
                        "name":   room["name"],
                        "type":   room["type"]},
            "history": history
        })

        # 11. Notificar lista de usuarios (usando start_background_task — P15)
        user_list = list(room_users[room_id].values())
        # socketio.start_background_task(
        #     broadcast_task, socketio, room_id, "user_list", {"users": user_list}
        # )
        socketio.emit("user_list", {"users": user_list}, room=room_id)

        # 12. Notificar que alguien entró
        socketio.emit("user_joined", {"nickname": nickname}, room=room_id, include_self=False)


    @socketio.on("send_message")
    def on_message(data):
        from flask import request as sio_request
        room_id  = sio_request.environ.get("room_id")
        nickname = sio_request.environ.get("nickname")
        content  = data.get("content", "").strip()

        if not room_id or not content:
            return

        # Rate limiting de mensajes (P17)
        if not check_message_rate(room_id, nickname):
            emit("error", {
                "message": f"Demasiados mensajes. Máx {MESSAGE_WINDOW_SECONDS}s entre ráfagas."
            })
            return

        # Actualizar actividad (P13)
        last_activity[sio_request.sid] = time.time()

        # Guardar en base de datos
        message = Message.create(
            room_id  = room_id,
            nickname = nickname,
            content  = content,
            msg_type = "text"
        )

        # Broadcast usando start_background_task (P15)
        emit('new_message',message,to=room_id)

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

        # Actualizar actividad (P13)
        last_activity[sio_request.sid] = time.time()

        # Guardar en base de datos
        message = Message.create(
            room_id  = room_id,
            nickname = nickname,
            content  = None,
            msg_type = "file",
            file_name = name,
            file_path = path,
            file_type = type
        )

        # Broadcast usando start_background_task (P15)
        emit('new_message',message,to=room_id)


    @socketio.on("load_more_messages")
    def on_load_more(data):
        """
        Paginación del historial — el frontend envía el timestamp
        del mensaje más antiguo que tiene para cargar los anteriores.
        (P14)
        """
        from flask import request as sio_request
        room_id = data.get("roomId", "")
        before  = data.get("before", None)

        if not room_id:
            return

        # Actualizar actividad (P13)
        if sio_request.sid in last_activity:
            last_activity[sio_request.sid] = time.time()

        messages = Message.get_history(room_id, limit=50, before=before)
        emit("more_messages", {
            "messages": messages,
            "hasMore":  len(messages) == 50
        })


    @socketio.on("disconnect")
    def on_disconnect():
        from flask import request as sio_request
        room_id   = sio_request.environ.get("room_id")
        nickname  = sio_request.environ.get("nickname")
        client_ip = sio_request.environ.get("client_ip")

        if not room_id:
            return

        # Limpiar usuario
        if room_id in room_users:
            room_users[room_id].pop(sio_request.sid, None)

        # Limpiar sesión Redis
        if client_ip:
            redis_client.delete(f"session:{client_ip}")

        # Limpiar registro de actividad (P13)
        last_activity.pop(sio_request.sid, None)

        # Notificar salida
        socketio.emit("user_left", {"nickname": nickname}, room=room_id)
        user_list = list(room_users.get(room_id, {}).values())
        socketio.emit("user_list", {"users": user_list}, room=room_id)

        leave_room(room_id)


def _get_ip():
    from flask import request as sio_request
    return (sio_request.environ.get("HTTP_X_FORWARDED_FOR") or
            sio_request.environ.get("REMOTE_ADDR", "unknown"))