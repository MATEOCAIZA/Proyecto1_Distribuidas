from datetime import datetime


def broadcast_task(socketio, room_id: str, event: str, data: dict):
    if "timestamp" not in data:
        data["timestamp"] = datetime.utcnow().isoformat()

    socketio.emit(event, data, room=room_id)