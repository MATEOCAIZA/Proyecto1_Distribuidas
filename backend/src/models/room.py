import bcrypt
import uuid
from datetime import datetime
from src.config.database import rooms_collection

class Room:

    @staticmethod
    def create(name: str, pin: str, room_type: str) -> dict:
        """Crea una sala con PIN hasheado."""
        if len(pin) < 4:
            raise ValueError("El PIN debe tener al menos 4 dígitos")
        if room_type not in ["text", "multimedia"]:
            raise ValueError("Tipo de sala inválido")

        # Hashear el PIN
        hashed_pin = bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()

        room = {
            "roomId":    str(uuid.uuid4())[:8].upper(),
            "name":      name,
            "pin":       hashed_pin,
            "type":      room_type,
            "active":    True,
            "createdAt": datetime.utcnow()
        }

        rooms_collection.insert_one(room)
        return {
            "roomId": room["roomId"],
            "name":   room["name"],
            "type":   room["type"]
        }

    @staticmethod
    def find_by_id(room_id: str) -> dict | None:
        """Busca sala activa por ID."""
        return rooms_collection.find_one(
            {"roomId": room_id, "active": True},
            {"_id": 0}
        )

    @staticmethod
    def verify_pin(room: dict, pin: str) -> bool:
        """Verifica el PIN contra el hash."""
        return bcrypt.checkpw(pin.encode(), room["pin"].encode())

    @staticmethod
    def get_all() -> list:
        """Lista todas las salas sin exponer el PIN."""
        return list(rooms_collection.find({}, {"_id": 0, "pin": 0}))