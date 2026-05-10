import pytest
import json

def _flush_received(socket):
    #Descarta todos los mensajes acumulados en la cola del test client.
        socket.get_received()

def _create_test_room(client, auth_token, name="Sala Test Sockets", pin="1234", room_type="text"):
    #Crea una sala vía REST y retorna el roomId.
    header = {"Authorization": f"Bearer {auth_token}"}
    room_data = {"name": name, "pin": pin, "type": room_type}
    response = client.post(
        "/api/rooms/",
        data=json.dumps(room_data),
        content_type="application/json",
        headers=header,
    )
    assert response.status_code == 201, f"No se pudo crear la sala: {response.data}"
    return response.json["roomId"]

class TestRoomCreate:
    def test_create_text_room(self, client,auth_token):
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

    def test_create_media_room(self, client,auth_token):
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

class TestRoomJoin:
    def test_valid_access(self,client,auth_token,socket_client,socket_client_2):
        room_id=_create_test_room(client,auth_token)
        nickname = "tester"
        client1_data={
            "roomId" : room_id,
            "nickname" : nickname,
            "pin" : "1234"
        }
        client2_data={
            "roomId" : room_id,
            "nickname" : nickname+"2",
            "pin" : "1234"
        }
        access_data={
            "pin" : "1234"
        }

        #Verifica que el pin de acceso es correcto
        response=client.post(f'/api/rooms/{room_id}/verify', data=json.dumps(access_data),content_type="application/json")
        assert response.status_code == 200

        #Se une a la nueva sala primero el cliente 2, luego el 1
        socket_client_2.emit("join_room", client2_data)
        socket_client.emit("join_room", client1_data)

        #Recupera los eventos recibidos por cada socket y extrae los nombres.
        client_events = socket_client.get_received()
        client_2_events = socket_client_2.get_received()


        event_names = [event["name"] for event in client_events]
        event_names_2 = [event["name"] for event in client_2_events]

        #El cliente debe recibir el "room_joined"
        assert "room_joined" in event_names
        #El cliente que estaba antes debe ser notificado de la llegada del nuevo cliente
        assert "user_joined" in event_names_2



    def test_invalid_pin_access(self, client, auth_token):
        room_id=_create_test_room(client,auth_token)
        access_data={
            "pin":"1234568"
        }
        response=client.post(f'/api/rooms/{room_id}/verify', data=json.dumps(access_data),content_type="application/json")

        assert response.status_code == 401

    def test_invalid_room_access(self, client):
        room_id="ID1234"
        access_data={
            "pin":"1234568"
        }

        response=client.post(f'/api/rooms/{room_id}/verify', data=json.dumps(access_data),content_type="application/json")

        assert response.status_code == 404

    def test_duplicate_nickname_access(self,client,auth_token,socket_client,socket_client_2):
        room_id=_create_test_room(client,auth_token)
        nickname = "tester"
        client_data={
            "roomId" : room_id,
            "nickname" : nickname,
            "pin" : "1234"
        }
        access_data={
            "pin" : "1234"
        }

        #Verifica que el pin de acceso es correcto
        response=client.post(f'/api/rooms/{room_id}/verify', data=json.dumps(access_data),content_type="application/json")
        assert response.status_code == 200

        #Se une a la misma sala 2 veces seguidas
        socket_client.emit("join_room", client_data)
        socket_client_2.emit("join_room", client_data)

        #Recupera los eventos recibidos por cada socket y extrae los nombres.
        client_events = socket_client.get_received()
        client_2_events = socket_client_2.get_received()
        event_names = [event["name"] for event in client_events]
        event_names_2 = [event["name"] for event in client_2_events]

        #El cliente 1 debe recibir el "room_joined"
        assert "room_joined" in event_names
        #El cliente 2, debe recibir un error y ser rechazado de la conexion
        assert "room_joined" not in event_names_2
        assert "error" in event_names_2