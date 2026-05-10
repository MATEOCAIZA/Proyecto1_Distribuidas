import pytest
import os
from pathlib import Path
import json

def _flush_received(socket):
    #Descarta todos los mensajes acumulados en la cola del test client.
        socket.get_received()

def _create_room(client, auth_token, name="Sala Test Sockets", pin="1234", room_type="text"):
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

class TestUpload:
    current_dir=Path(__file__).parent

    def test_valid_upload(self,client,auth_token, socket_client, socket_client_2):
        file_path = self.current_dir / "testfiles" / "testphoto.png"
        file_name = "photo1.png"
        room_id = _create_room(client,auth_token,name="Sala Multimedia test",pin="1234",room_type="multimedia")
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

        #Se une a la nueva sala
        socket_client.emit("join_room", client1_data)
        socket_client_2.emit("join_room", client2_data)

        #Libera los eventos de los sockets, para capturar el envío y recepción de mensaje.

        with open(file_path, 'rb') as img:
            data = {
                'file': (img, file_name),
                'nickname' : nickname
                }
            result=client.post(f'/api/upload/{room_id}', data=data, content_type='multipart/form-data')
        
        res_data = result.json
        new_filepath = res_data['filePath']
        file_type = res_data['fileType']
        new_filename = new_filepath.lstrip('/uploads/')


        #Limpia eventos innecesarios
        _flush_received(socket_client)
        _flush_received(socket_client_2)

        socket_client.emit("send_file_message",{
             "path" : new_filepath,
             "type" : file_type,
             "file_name" : file_name
            })

        #Verifica que el archivo se guardó en la BD
        file_query = client.get(f'/api/upload/files/{new_filename}')
        assert result.status_code == 201
        assert file_query.status_code == 200
        assert file_query is not None


        #Verifica que otro cliente reciba el mensaje
        received_2 = socket_client_2.get_received()
        file_message = [r for r in received_2 if r["name"] == "new_message"][0]
        msg_data = file_message["args"][0]

        # # --- Verificaciones

        assert msg_data['type'] == "file"  #Se detecta como archivo
        assert msg_data['fileType'] == file_type #El tipo de archivo es correcto
        assert msg_data['filePath'] == new_filepath
        assert msg_data['fileName'] == file_name



    def test_invalid_type_upload(self,client,auth_token,socket_client,socket_client_2):
        file_path = self.current_dir / "testfiles" / "music.mp3"
        file_name="song.mp3"
        room_id = _create_room(client,auth_token,name="Sala Multimedia test",pin="1234",room_type="multimedia")
        nickname="tester"
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

        #Se une a la nueva sala
        socket_client.emit("join_room", client1_data)
        socket_client_2.emit("join_room", client2_data)

        with open(file_path, 'rb') as img:
            data = {
                'file': (img, file_name),
                'nickname' : nickname
                }
            result=client.post(f'/api/upload/{room_id}', data=data, content_type='multipart/form-data')
        
        
        assert result.status_code == 400


    def test_invalid_size_upload(self,client,auth_token,socket_client,socket_client_2):
        file_path = self.current_dir / "testfiles" / "heavyfile.pdf"
        file_name="book.pdf"
        room_id = _create_room(client,auth_token,name="Sala Multimedia test",pin="1234",room_type="multimedia")
        nickname="tester"
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

        #Se une a la nueva sala
        socket_client.emit("join_room", client1_data)
        socket_client_2.emit("join_room", client2_data)

        with open(file_path, 'rb') as img:
            data = {
                'file': (img, file_name),
                'nickname' : nickname
                }
            result=client.post(f'/api/upload/{room_id}', data=data, content_type='multipart/form-data')
        
        
        assert result.status_code == 400