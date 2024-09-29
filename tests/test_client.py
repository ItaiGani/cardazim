import pytest
import socket
import sys
import os
import struct

# setting imports from parent folder
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from card import Card
import client


class MockSocket:
    sent_data = []
    addr = None

    # pass the creation of socket
    def __init__(self, family=-1, type=-1, proto=-1, fileno=None):
        pass

    def connect(self, addr):
        MockSocket.addr = addr

    def send(self, data: bytes):
        MockSocket.sent_data = []
        MockSocket.sent_data.append(data)

    def recv(self, data: bytes):
        return Card.deserialize(data)
    
    def close(self):
        pass


@pytest.fixture
def mock_socket(monkeypatch):
    monkeypatch.setattr(socket, 'socket', MockSocket)




@pytest.mark.parametrize("ip, port", [
    ("1.2.3.4", 5789),
    ("127.0.0.1", 9999)
])
def test_runClient(ip, port, mock_socket):
    data = ("nAme", "creAtor", "images/elephant.jpeg", "what animal is in the picture?", "elephant")
    client.send_data(ip, port, data)
    card = Card.create_from_path(data[0], data[1], data[2], data[3], data[4])
    card.image.encrypt("securepassword")

    assert MockSocket.addr == (ip, port)
    assert MockSocket.sent_data == [struct.pack("<I", len(card.serialize())) + card.serialize()]