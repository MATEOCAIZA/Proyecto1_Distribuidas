from src.app import create_app
import pytest
@pytest.fixture(scope="session")
def app():
    app, socketio = create_app()
    app.config['TESTING'] = True
    yield app

@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client:
        yield client