"""
broadcast.py — Worker de difusión de mensajes con ThreadPoolExecutor.

En lugar de crear un hilo nuevo por cada mensaje (costoso), se mantiene
un pool de hilos reutilizables. Esto elimina el overhead de creación de
hilos y reduce la latencia de broadcast.

Pool size: 4 hilos (ajustable con MAX_BROADCAST_WORKERS).
"""

import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

# Pool global reutilizado durante toda la vida del servidor
MAX_BROADCAST_WORKERS = int(os.getenv("MAX_BROADCAST_WORKERS", 4))
_pool = ThreadPoolExecutor(max_workers=MAX_BROADCAST_WORKERS, thread_name_prefix="broadcast")


def _emit_task(socketio, room_id: str, event: str, data: dict):
    """Tarea interna: emite el evento al room. Corre dentro del pool."""
    if "timestamp" not in data:
        data["timestamp"] = datetime.now(timezone.utc).isoformat()
    socketio.emit(event, data, room=room_id)


def broadcast_in_thread(socketio, room_id: str, event: str, data: dict):
    """
    Envía `data` como evento `event` a todos los clientes del `room_id`.

    La emisión se delega al ThreadPoolExecutor global, por lo que el
    handler WebSocket retorna de inmediato sin esperar la difusión.
    """
    _pool.submit(_emit_task, socketio, room_id, event, data)


def broadcast_with_db(socketio, room_id: str, event: str,
                      create_fn, create_kwargs: dict):
    """
    Variante que también ejecuta la escritura a BD dentro del hilo del pool,
    liberando al handler principal de cualquier espera de I/O.

    Args:
        create_fn:     función que persiste el mensaje (ej. Message.create).
        create_kwargs: argumentos para create_fn.
    """
    def _task():
        message = create_fn(**create_kwargs)
        _emit_task(socketio, room_id, event, message)

    _pool.submit(_task)