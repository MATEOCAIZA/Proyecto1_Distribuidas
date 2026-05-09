import pytest
import os
from pathlib import Path
import json

#Prueba no válida. Necesita nickname

class TestUpload:
    current_dir=Path(__file__).parent
    def test_valid_upload(self,client,auth_token):
        file_path = self.current_dir / "testfiles" / "testphoto.png"
        file_name="photo1.png"
        header={
            "Authorization" : f"Bearer {auth_token}"
        }
        room_list=client.get('/api/rooms/',headers=header)
        rooms = room_list.json
        room_id=rooms[0]['roomId']
        nickname="tester"
        client_data={
            "roomId" : room_id,
            "nickname" : nickname,
            "pin" : "1234"
        }

        with open(file_path, 'rb') as img:
            data = {
                'file': (img, file_name),
                'nickname' : nickname
                }
            result=client.post(f'/api/upload/{room_id}', data=data, content_type='multipart/form-data')
        
        
        res_data = result.json
        filepath = res_data['filePath']
        new_filename = filepath.lstrip('/uploads/')
        file_query = client.get(f'/api/upload/files/{new_filename}')
        assert result.status_code == 201
        assert file_query.status_code == 200
        assert file_query is not None


    def test_invalid_type_upload(self,client,auth_token):
        file_path = self.current_dir / "testfiles" / "music.mp3"
        file_name="song.mp3"
        header={
            "Authorization" : f"Bearer {auth_token}"
        }
        room_list=client.get('/api/rooms/',headers=header)
        rooms = room_list.json
        room_id=rooms[0]['roomId']
        nickname="tester"
        client_data={
            "roomId" : room_id,
            "nickname" : nickname,
            "pin" : "1234"
        }

        with open(file_path, 'rb') as img:
            data = {
                'file': (img, file_name),
                'nickname' : nickname
                }
            result=client.post(f'/api/upload/{room_id}', data=data, content_type='multipart/form-data')
        
        
        assert result.status_code == 400


    def test_invalid_size_upload(self,client,auth_token):
        file_path = self.current_dir / "testfiles" / "heavyfile.pdf"
        file_name="book.pdf"
        header={
            "Authorization" : f"Bearer {auth_token}"
        }
        room_list=client.get('/api/rooms/',headers=header)
        rooms = room_list.json
        room_id=rooms[0]['roomId']
        nickname="tester"
        client_data={
            "roomId" : room_id,
            "nickname" : nickname,
            "pin" : "1234"
        }

        with open(file_path, 'rb') as img:
            data = {
                'file': (img, file_name),
                'nickname' : nickname
                }
            result=client.post(f'/api/upload/{room_id}', data=data, content_type='multipart/form-data')
        
        
        assert result.status_code == 400