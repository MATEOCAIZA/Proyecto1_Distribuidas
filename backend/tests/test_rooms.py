import pytest
import json

class TestRoomCreate:
    def test_create_textroom(self, client,auth_token):
        token = auth_token
        room_name="Sala General"

        #Prueba de uso del endpoint para crear una sala
        room_data= {
  "name": room_name,
  "pin": "1234",
  "type": "text"
}
        
        header={
            "Authorization" : f"Bearer {token}"
        }
        response = client.post('/api/rooms/', data=json.dumps(room_data),content_type="application/json", headers=header)
        room_list=client.get('/api/rooms/',headers=header)
        rooms = room_list.json
        room_created=False
        for room in rooms:
            if room['name'] == room_name:
                room_created = True
                break
        assert response.status_code == 201
        assert room_created == True

    def test_create_mediaroom(self, client,auth_token):
        token = auth_token
        room_name="Sala Multimedia"

        #Prueba de uso del endpoint para crear una sala
        room_data= {
  "name": room_name,
  "pin": "1234",
  "type": "multimedia"
}
        
        header={
            "Authorization" : f"Bearer {token}"
        }
        response = client.post('/api/rooms/', data=json.dumps(room_data),content_type="application/json", headers=header)
        room_list=client.get('/api/rooms/',headers=header)
        rooms = room_list.json
        room_created=False
        for room in rooms:
            if room['name'] == room_name:
                room_created = True
                break
        assert response.status_code == 201
        assert room_created == True

    def test_create_invalid_pin_room(self, client,auth_token):
        token = auth_token
        room_name="Sala PIN invalido"

        #Prueba de uso del endpoint para crear una sala
        room_data= {
  "name": room_name,
  "pin": "123",
  "type": "multimedia"
}
        
        header={
            "Authorization" : f"Bearer {token}"
        }
        response = client.post('/api/rooms/', data=json.dumps(room_data),content_type="application/json", headers=header)
        room_list=client.get('/api/rooms/',headers=header)
        rooms = room_list.json
        room_created=False
        for room in rooms:
            if room['name'] == room_name:
                room_created = True
                break
        assert response.status_code == 400
        assert room_created == False

    def test_create_invalid_type_room(self, client,auth_token):
        token = auth_token
        room_name="Sala tipo invalido"

        #Prueba de uso del endpoint para crear una sala
        room_data= {
  "name": room_name,
  "pin": "12345",
  "type": "music"
}
        
        header={
            "Authorization" : f"Bearer {token}"
        }
        response = client.post('/api/rooms/', data=json.dumps(room_data),content_type="application/json", headers=header)
        room_list=client.get('/api/rooms/',headers=header)
        rooms = room_list.json
        room_created=False
        for room in rooms:
            if room['name'] == room_name:
                room_created = True
                break
        assert response.status_code == 400
        assert room_created == False

    def test_create_duplicate_room(self, client,auth_token):
        token = auth_token
        room_name="Sala General" #Ya fue creada por la primera prueba

        #Prueba de uso del endpoint para crear una sala
        room_data= {
  "name": room_name,
  "pin": "12345",
  "type": "text"
}
        
        header={
            "Authorization" : f"Bearer {token}"
        }
        response = client.post('/api/rooms/', data=json.dumps(room_data),content_type="application/json", headers=header)
        new_room=response.json
        room_list=client.get('/api/rooms/',headers=header)
        rooms = room_list.json
        same_ids=False
        for room in rooms:
            if room['name'] == room_name:
                if room['roomId'] == new_room['roomId']:
                    same_ids = True
                break
        assert same_ids == False

class TestRoomAccess:
    def test_valid_access(self,client,auth_token):
        header={
            "Authorization" : f"Bearer {auth_token}"
        }
        access_data={
            "pin":"1234"
        }
        room_list=client.get('/api/rooms/',headers=header)
        rooms = room_list.json
        room_id=rooms[0]['roomId']

        response=client.post(f'/api/rooms/{room_id}/verify', data=json.dumps(access_data),content_type="application/json")

        assert response.status_code == 200


    def test_invalid_pin_access(self, client, auth_token):
        header={
            "Authorization" : f"Bearer {auth_token}"
        }
        access_data={
            "pin":"1234568"
        }
        room_list=client.get('/api/rooms/',headers=header)
        rooms = room_list.json
        room_id=rooms[0]['roomId']

        response=client.post(f'/api/rooms/{room_id}/verify', data=json.dumps(access_data),content_type="application/json")

        assert response.status_code == 401

    def test_invalid_room_access(self, client, auth_token):
        room_id="ID1234"
        access_data={
            "pin":"1234568"
        }

        response=client.post(f'/api/rooms/{room_id}/verify', data=json.dumps(access_data),content_type="application/json")

        assert response.status_code == 404