import threading
from datetime import datetime

class BroadcastWorker(threading.Thread):
    """
    Hilo dedicado para procesar y emitir mensajes
    sin bloquear el servidor principal.
    """

    def __init__(self, socketio, room_id: str, event: str, data: dict):
        super().__init__(daemon=True)
        self.socketio = socketio
        self.room_id  = room_id
        self.event    = event
        self.data     = data

    def run(self):
        """Ejecuta el broadcast en un hilo separado."""
        # Agregar timestamp en el hilo
        self.data["timestamp"] = datetime.utcnow().isoformat()

        # Emitir a todos en la sala
        self.socketio.emit(
            self.event,
            self.data,
            room=self.room_id
        )