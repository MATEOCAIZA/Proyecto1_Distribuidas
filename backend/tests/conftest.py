import eventlet
eventlet.monkey_patch() # Debe ser la primera línea ejecutada en tus tests
from src.app import create_app
import pytest
import json
@pytest.fixture(scope="session")
def app_and_socket():
    app, socketio = create_app()
    app.config['TESTING'] = True
    yield app, socketio

@pytest.fixture(scope="function")
def client(app_and_socket):
    app, _ = app_and_socket
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def socket_client(app_and_socket, client):
    app, socketio = app_and_socket
    # Importante: al iniciar, el cliente se conecta automáticamente
    socket_test_client = socketio.test_client(app, flask_test_client=client)
    yield socket_test_client
    # Limpieza tras el test
    socket_test_client.disconnect()

@pytest.fixture(scope="function")
def auth_token(client):
        loginData = {
  "username": "admin",
  "password": "Admin123"
}
        response = client.post('/api/auth/login',data=json.dumps(loginData),content_type="application/json")
        data = response.json
        token = data['token']
        return token