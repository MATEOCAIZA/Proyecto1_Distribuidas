import pytest
import json


class TestAuth:
    def test_auth_normal(self, client):
        loginData = {
  "username": "admin",
  "password": "Admin123"
}
        response = client.post('/api/auth/login',data=json.dumps(loginData),content_type="application/json")
        data=response.json
        assert response.status_code == 200
        assert 'token' in data

    def test_auth_invalid(self, client):
        loginData = {
  "username": "admin",
  "password": "adminadmin"
}
        response = client.post('/api/auth/login',data=json.dumps(loginData),content_type="application/json")
        data=response.json
        assert response.status_code == 401
        assert "token" not in data

    def test_auth_invalid_try(self, client):
        loginData = {
  "username": "admin",
  "password": "adminadmin"
}
        #Login inválido
        login_response = client.post('/api/auth/login',data=json.dumps(loginData),content_type="application/json")
        data=login_response.json

        #Prueba de uso del endpoint para crear una sala
        room_data= {
  "name": "Sala General",
  "pin": "1234",
  "type": "text"
}
        create_room_response = client.post('/api/rooms/', data=json.dumps(room_data),content_type="application/json")
        assert login_response.status_code == 401
        assert "token" not in data
        assert create_room_response.status_code == 401


    