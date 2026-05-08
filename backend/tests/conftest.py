from src.app import create_app
import pytest
import json
@pytest.fixture(scope="session")
def app():
    app, socketio = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        yield client

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