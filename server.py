import argparse
import sys
import socket
import threading
from connection import Connection
from card import Card
from card_manager import CardManager


def handle_client(conn: Connection, manager: CardManager):
    data = conn.receive_message()
    print(f"Current thread id = {threading.get_native_id()}")
    card = Card.deserialize(data)
    card.image.decrypt("securepassword")

    manager.save(card)

    conn.close()


def run_server(server_ip, server_port, database, images_dir):
    manager = CardManager(database, images_dir)
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((server_ip, server_port))
    serv.listen(5)
    while True:
        conn, addr = serv.accept()
        conn = Connection(conn)
        thread = threading.Thread(target=handle_client, args=(conn, manager))
        thread.start()


def get_args():
    parser = argparse.ArgumentParser(description='setup server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('database',type=str,
                        help='url containing database type and its path')
    parser.add_argument('images_dir', type=str,
                        help='directory where the images will be saved')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port, args.database, args.images_dir)
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())