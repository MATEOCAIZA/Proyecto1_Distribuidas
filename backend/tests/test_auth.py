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
        print(data)
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