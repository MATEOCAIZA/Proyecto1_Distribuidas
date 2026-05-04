from datetime import datetime
from src.config.database import messages_collection

class Message:

    @staticmethod
    def create(room_id: str, nickname: str,
               content: str = None, msg_type: str = "text",
               file_name: str = None, file_path: str = None,
               file_type: str = None) -> dict:
        """Guarda un mensaje en la base de datos."""
        message = {
            "roomId":    room_id,
            "nickname":  nickname,
            "content":   content,
            "type":      msg_type,
            "fileName":  file_name,
            "filePath":  file_path,
            "fileType":  file_type,
            "timestamp": datetime.utcnow().isoformat()
        }
        messages_collection.insert_one(message)
        message.pop("_id", None)  # Quitar _id de MongoDB para serializar
        return message

    @staticmethod
    def get_history(room_id: str, limit: int = 50) -> list:
        """Obtiene los últimos mensajes de una sala."""
        cursor = messages_collection.find(
            {"roomId": room_id},
            {"_id": 0}
        ).sort("timestamp", 1).limit(limit)
        return list(cursor)