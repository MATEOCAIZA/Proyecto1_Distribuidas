"""
Tests para los eventos WebSocket definidos en src/socket/events.py.

Cubre: join_room, send_message, load_more_messages, disconnect,
       y escenarios multi-cliente (client ↔ server ↔ client2).
"""
import pytest
import json


#─── Helpers ────────────────────────────────────────────────────────


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


def _flush_received(socket_client):
    #Descarta todos los mensajes acumulados en la cola del test client.
    socket_client.get_received()


# ─── send_message ───────────────────────────────────────────────────


class TestSendMessage:
    """Escenarios del evento 'send_message'."""

    def test_send_message_broadcast(
        self, client, auth_token, socket_client, socket_client_2
    ):
        """Un mensaje enviado por client1 debe llegar a client2 en la misma sala."""
        room_id = _create_room(client, auth_token, name="Sala Msg Broadcast")

        # Ambos se unen
        socket_client.emit("join_room", {
            "roomId": room_id,
            "pin": "1234",
            "nickname": "Sender",
        })
        _flush_received(socket_client)

        socket_client_2.emit("join_room", {
            "roomId": room_id,
            "pin": "1234",
            "nickname": "Receiver",
        })
        _flush_received(socket_client_2)
        _flush_received(socket_client)  # limpiar user_joined que le llega a client1

        # Enviar mensaje
        socket_client.emit("send_message", {"content": "Hola mundo"})

        # client2 debe recibir new_message
        received_2 = socket_client_2.get_received()
        print("Eventos recibidos:")
        print(received_2)
        new_msgs = [r for r in received_2 if r["name"] == "new_message"]
        assert len(new_msgs) >= 1
        msg_data = new_msgs[0]["args"][0]
        assert msg_data["content"] == "Hola mundo"
        assert msg_data["nickname"] == "Sender"

    def test_send_empty_message_ignored(self, client, auth_token, socket_client):
        """Un mensaje vacío no genera broadcast."""
        room_id = _create_room(client, auth_token, name="Sala Empty Msg")

        socket_client.emit("join_room", {
            "roomId": room_id,
            "pin": "1234",
            "nickname": "EmptyUser",
        })
        _flush_received(socket_client)

        socket_client.emit("send_message", {"content": ""})

        received = socket_client.get_received()
        new_msgs = [r for r in received if r["name"] == "new_message"]
        assert len(new_msgs) == 0

    def test_send_message_without_room(self, socket_client):
        """Si el cliente no se unió a ninguna sala, el mensaje se ignora."""
        socket_client.emit("send_message", {"content": "Sin sala"})

        received = socket_client.get_received()
        new_msgs = [r for r in received if r["name"] == "new_message"]
        assert len(new_msgs) == 0


# ─── load_more_messages (paginación) ───────────────────────────────


class TestLoadMoreMessages:
    """Escenarios del evento 'load_more_messages' (P14)."""

    def test_load_more_returns_messages(self, client, auth_token, socket_client):
        """Solicitar historial anterior devuelve 'more_messages'."""
        room_id = _create_room(client, auth_token, name="Sala Historial")

        socket_client.emit("join_room", {
            "roomId": room_id,
            "pin": "1234",
            "nickname": "HistUser",
        })
        _flush_received(socket_client)

        socket_client.emit("load_more_messages", {
            "roomId": room_id,
            "before": None,
        })

        received = socket_client.get_received()
        more = [r for r in received if r["name"] == "more_messages"]
        assert len(more) >= 1
        data = more[0]["args"][0]
        assert "messages" in data
        assert "hasMore" in data

    def test_load_more_empty_room_id(self, socket_client):
        """Si no se envía roomId, el evento no devuelve nada."""
        socket_client.emit("load_more_messages", {"roomId": "", "before": None})

        received = socket_client.get_received()
        more = [r for r in received if r["name"] == "more_messages"]
        assert len(more) == 0


# ─── disconnect ─────────────────────────────────────────────────────


class TestDisconnect:
    """Escenarios del evento 'disconnect'."""

    def test_disconnect_notifies_room(
        self, client, auth_token, socket_client, socket_client_2
    ):
        """
        Cuando un usuario se desconecta, los demás en la sala
        reciben 'user_left' y un 'user_list' actualizado.
        """
        room_id = _create_room(client, auth_token, name="Sala Disconnect")

        # Ambos se unen
        socket_client.emit("join_room", {
            "roomId": room_id,
            "pin": "1234",
            "nickname": "Stayer",
        })
        _flush_received(socket_client)

        socket_client_2.emit("join_room", {
            "roomId": room_id,
            "pin": "1234",
            "nickname": "Leaver",
        })
        _flush_received(socket_client)
        _flush_received(socket_client_2)

        # Desconectar client2
        socket_client_2.disconnect()

        # client1 debe recibir user_left
        received = socket_client.get_received()
        left_events = [r for r in received if r["name"] == "user_left"]
        assert len(left_events) >= 1
        assert left_events[0]["args"][0]["nickname"] == "Leaver"


# ─── Multi-client: user_list broadcast ──────────────────────────────


class TestUserListBroadcast:
    """
    Verifica que la lista de usuarios se actualiza correctamente
    cuando un segundo cliente se une a la sala.
    """

    def test_user_list_updates_on_join(
        self, client, auth_token, socket_client, socket_client_2
    ):
        room_id = _create_room(client, auth_token, name="Sala UserList")

        socket_client.emit("join_room", {
            "roomId": room_id,
            "pin": "1234",
            "nickname": "First",
        })
        _flush_received(socket_client)

        # Segundo usuario se une
        socket_client_2.emit("join_room", {
            "roomId": room_id,
            "pin": "1234",
            "nickname": "Second",
        })

        # client1 debe recibir user_list con ambos usuarios
        received = socket_client.get_received()
        user_lists = [r for r in received if r["name"] == "user_list"]
        assert len(user_lists) >= 1
        users = user_lists[-1]["args"][0]["users"]
        assert "First" in users
        assert "Second" in users
