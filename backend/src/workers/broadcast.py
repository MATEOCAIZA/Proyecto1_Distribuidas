"""
broadcast.py — Worker de difusión de mensajes con hilos.

Usa threading.Thread (parchado por eventlet) para emitir eventos
WebSocket sin bloquear el handler principal del socket.
"""

import threading
from datetime import datetime, timezone


def broadcast_task(socketio, room_id: str, event: str, data: dict):
    """
    Emite un evento a todos los clientes de una sala.
    
    Diseñado para ejecutarse en un hilo separado via
    threading.Thread o socketio.start_background_task.
    """
    if "timestamp" not in data:
        data["timestamp"] = datetime.now(timezone.utc).isoformat()

    socketio.emit(event, data, room=room_id)


def broadcast_in_thread(socketio, room_id: str, event: str, data: dict):
    """
    Lanza broadcast_task en un hilo daemon independiente.

    El hilo es daemon=True para que no bloquee el cierre del servidor
    si el proceso principal termina.
    """
    t = threading.Thread(
        target=broadcast_task,
        args=(socketio, room_id, event, data),
        daemon=True
    )
    t.start()
    return t