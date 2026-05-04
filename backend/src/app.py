import os
import eventlet
eventlet.monkey_patch()  # DEBE ir primero para async correcto

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv

from src.routes.auth   import auth_bp
from src.routes.rooms  import rooms_bp
from src.routes.upload import upload_bp
from src.socket.events import register_events

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, origins="*")

    # Carpeta para archivos subidos
    os.makedirs("uploads", exist_ok=True)

    # Registrar blueprints (rutas REST)
    app.register_blueprint(auth_bp,   url_prefix="/api/auth")
    app.register_blueprint(rooms_bp,  url_prefix="/api/rooms")
    app.register_blueprint(upload_bp, url_prefix="/api/upload")

    # Inicializar SocketIO con threading
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",
        async_mode="eventlet",  # Permite concurrencia real
        logger=True
    )

    # Registrar eventos WebSocket
    register_events(socketio)

    return app, socketio


if __name__ == "__main__":
    app, socketio = create_app()
    socketio.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 3001)),
        debug=True
    )